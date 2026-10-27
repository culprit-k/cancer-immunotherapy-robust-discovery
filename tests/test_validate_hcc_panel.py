"""Integration tests for the HCC panel workbook validator."""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_hcc_panel.py"


class ValidateHccPanelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.panel = self.root / "panel.csv"
        self.out_csv = self.root / "ordered.csv"
        self.out_json = self.root / "report.json"

    def tearDown(self):
        self.tmp.cleanup()

    def write_panel(self, rows, fields=("Channel", "MetalTag", "Target")):
        with self.panel.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fields))
            writer.writeheader()
            writer.writerows(rows)

    def run_validator(self, expected_channels=3):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--panel", str(self.panel),
             "--expected-channels", str(expected_channels),
             "--out-csv", str(self.out_csv), "--out-json", str(self.out_json)],
            capture_output=True, text=True, check=False,
        )

    def test_valid_panel_exports_sorted_channel_map(self):
        self.write_panel([
            {"Channel": 3, "MetalTag": "tag3", "Target": "marker3"},
            {"Channel": 1, "MetalTag": "tag1", "Target": "marker1"},
            {"Channel": 2, "MetalTag": "tag2", "Target": "marker2"},
        ])
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(self.out_json.read_text(encoding="utf-8"))
        self.assertEqual(report["gate"], "PASS_PANEL_TABLE_ONLY")
        with self.out_csv.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["channel"] for row in rows], ["1", "2", "3"])
        self.assertIn("does not verify TIFF plane order", report["critical_limit"])

    def test_duplicate_channel_is_blocked(self):
        self.write_panel([
            {"Channel": 1, "MetalTag": "a", "Target": "A"},
            {"Channel": 1, "MetalTag": "b", "Target": "B"},
            {"Channel": 3, "MetalTag": "c", "Target": "C"},
        ])
        result = self.run_validator()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(self.out_json.read_text())["gate"], "BLOCKED")
        self.assertIn("Duplicate channel numbers", result.stdout)

    def test_blank_marker_field_is_blocked(self):
        self.write_panel([
            {"Channel": 1, "MetalTag": "a", "Target": "A"},
            {"Channel": 2, "MetalTag": "", "Target": "B"},
            {"Channel": 3, "MetalTag": "c", "Target": "C"},
        ])
        result = self.run_validator()
        self.assertEqual(result.returncode, 2)
        self.assertIn("MetalTag has blank values", result.stdout)

    def test_missing_required_column_is_blocked(self):
        self.write_panel([
            {"Channel": 1, "Target": "A"},
            {"Channel": 2, "Target": "B"},
            {"Channel": 3, "Target": "C"},
        ], fields=("Channel", "Target"))
        result = self.run_validator()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Missing required columns", result.stdout)


if __name__ == "__main__":
    unittest.main()
