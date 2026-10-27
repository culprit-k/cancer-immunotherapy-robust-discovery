from pathlib import Path
import subprocess
import sys

import pytest

from scripts.patch_virtues_cpu_sdpa import BEGIN_MARKER, END_MARKER, patch_source


IMPORT = "from flash_attn.flash_attn_interface import flash_attn_varlen_qkvpacked_func"
START = "        qkv=torch.stack([Q.squeeze(0), K.squeeze(0), V.squeeze(0)], dim=1)"
END = ").unsqueeze(0)  # (total_Q, H, D) collapsed over batch by varlen kernel"


@pytest.fixture
def source_fixture():
    return f'''import torch
import torch.nn.functional as F
{IMPORT}

class Example:
    def forward(self, Q, K, V, B, L, S, cu_seq_len, max_seq_len):
{START}
        attn_out = flash_attn_varlen_qkvpacked_func(
            qkv=qkv,
            cu_seqlens=cu_seq_len,
            max_seqlen=max_seq_len,
            deterministic=True,
            dropout_p=self.dropout if self.training else 0.0,
        {END}
        out = attn_out.reshape(B, -1, self.embed_dim)
        return self.W_o(out)
'''


def test_patch_adds_optional_import_and_packed_cpu_fallback(source_fixture):
    patched = patch_source(source_fixture)
    assert "except ImportError" in patched
    assert "flash_attn_varlen_qkvpacked_func = None" in patched
    assert BEGIN_MARKER in patched and END_MARKER in patched
    assert "F.scaled_dot_product_attention" in patched
    assert "boundaries[-1] != L" in patched
    compile(patched, "patched_attention.py", "exec")


def test_patch_is_idempotent(source_fixture):
    once = patch_source(source_fixture)
    twice = patch_source(once)
    assert twice == once


def test_unknown_upstream_signature_fails_closed(source_fixture):
    mutated = source_fixture.replace(START, "        qkv = different_implementation()")
    with pytest.raises(ValueError, match="packed-QKV call start"):
        patch_source(mutated)


def test_missing_import_fails_closed(source_fixture):
    mutated = source_fixture.replace(IMPORT, "# import removed")
    with pytest.raises(ValueError, match="FlashAttention import line"):
        patch_source(mutated)


def test_cli_dry_run_does_not_modify_original(tmp_path, source_fixture):
    root = tmp_path / "virtues"
    target = root / "virtues/modules/layers/attention_flashattention.py"
    target.parent.mkdir(parents=True)
    target.write_text(source_fixture, encoding="utf-8")
    before = target.read_bytes()

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parents[1] / "scripts/patch_virtues_cpu_sdpa.py"),
            "--virtues-root",
            str(root),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "DRY RUN" in result.stdout
    assert target.read_bytes() == before
    assert list(target.parent.glob("*.bak")) == []


def test_cli_apply_creates_backup_and_patches(tmp_path, source_fixture):
    root = tmp_path / "virtues"
    target = root / "virtues/modules/layers/attention_flashattention.py"
    target.parent.mkdir(parents=True)
    target.write_text(source_fixture, encoding="utf-8")
    original = target.read_text(encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parents[1] / "scripts/patch_virtues_cpu_sdpa.py"),
            "--virtues-root",
            str(root),
            "--apply",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Patch applied" in result.stdout
    backups = list(target.parent.glob("*.pre_cpu_sdpa_*.bak"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == original
    patched = target.read_text(encoding="utf-8")
    assert BEGIN_MARKER in patched
    compile(patched, str(target), "exec")
