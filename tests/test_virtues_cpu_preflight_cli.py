from pathlib import Path
import subprocess
import sys


def test_cpu_preflight_cli_help_is_available_without_model_dependencies():
    script = Path(__file__).parents[1] / "scripts" / "run_virtues_cpu_preflight_colab.py"
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "--virtues-root" in result.stdout
    assert "--checkpoint" in result.stdout
    assert "--marker-embeddings" in result.stdout
    assert "--apply-patch" in result.stdout
    assert "--out" in result.stdout


from scripts.run_virtues_cpu_preflight_colab import cpu_patch_ready


CPU_BEGIN = "# BEGIN CPU SDPA fallback (research compatibility patch)"
CPU_END = "# END CPU SDPA fallback (research compatibility patch)"


def test_preflight_allows_dry_run_when_fallback_is_already_applied():
    step = {"status": "PASS", "mode": "dry_run", "stdout": "Already patched; no file changed."}
    source = f"before\n{CPU_BEGIN}\nfallback code\n{CPU_END}\nafter"
    assert cpu_patch_ready(step, source)


def test_preflight_blocks_dry_run_when_fallback_is_not_applied():
    step = {"status": "PASS", "mode": "dry_run", "stdout": "Dry run only. No files changed."}
    assert not cpu_patch_ready(step, "original official source without fallback markers")


def test_preflight_blocks_if_patch_validation_failed_even_with_markers():
    step = {"status": "FAIL", "mode": "apply"}
    source = f"{CPU_BEGIN}\nfallback\n{CPU_END}"
    assert not cpu_patch_ready(step, source)
