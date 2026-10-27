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
    def __init__(self):
        self.dropout = 0.0
        self.training = False
        self.embed_dim = 16
        self.num_heads = 4
        self.head_dim = 4
        self.W_o = torch.nn.Identity()

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


def test_packed_cpu_fallback_matches_independent_sdpa_segments(source_fixture):
    torch = pytest.importorskip(
        "torch",
        reason="PyTorch is optional in lightweight CI; the Colab preflight executes this path.",
    )
    import torch.nn.functional as F

    namespace = {}
    exec(compile(patch_source(source_fixture), "patched_attention_fixture.py", "exec"), namespace)
    example = namespace["Example"]()

    torch.manual_seed(123)
    q = torch.randn(1, 7, 16)
    k = torch.randn(1, 7, 16)
    v = torch.randn(1, 7, 16)
    cu = torch.tensor([0, 3, 7], dtype=torch.int32)

    actual = example.forward(q, k, v, 1, 7, 7, cu, 4)

    expected_chunks = []
    for start, end in ((0, 3), (3, 7)):
        qs = q[:, start:end, :].view(1, end - start, 4, 4).transpose(1, 2)
        ks = k[:, start:end, :].view(1, end - start, 4, 4).transpose(1, 2)
        vs = v[:, start:end, :].view(1, end - start, 4, 4).transpose(1, 2)
        expected = F.scaled_dot_product_attention(qs, ks, vs, dropout_p=0.0)
        expected_chunks.append(
            expected.transpose(1, 2).contiguous().view(1, end - start, 16)
        )
    reference = torch.cat(expected_chunks, dim=1)

    assert actual.shape == (1, 7, 16)
    assert torch.isfinite(actual).all()
    torch.testing.assert_close(actual, reference, rtol=1e-6, atol=1e-6)
