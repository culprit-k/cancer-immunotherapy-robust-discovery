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
