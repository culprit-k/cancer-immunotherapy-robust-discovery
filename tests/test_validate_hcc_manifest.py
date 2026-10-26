import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_hcc_manifest import validate_manifest


class ManifestValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for folder in ("images", "cells", "stroma"):
            (self.root / folder).mkdir()
            (self.root / folder / "roi1.tif").write_bytes(b"synthetic-test-placeholder")
        self.manifest = self.root / "manifest.csv"
        self.channel_map = self.root / "channels.csv"
        self.write_manifest([{
            "patient_id": "P001", "roi_id": "R001",
            "image_path": "images/roi1.tif", "cell_mask_path": "cells/roi1.tif",
            "stromal_mask_path": "stroma/roi1.tif", "channel_map_version": "v1", "qc_status": "not_run"
        }])
        with self.channel_map.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["channel_index", "marker", "uniprot_id"])
            writer.writeheader()
            writer.writerow({"channel_index": 0, "marker": "CD8", "uniprot_id": "P01732"})

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self, rows):
        fields = ["patient_id", "roi_id", "image_path", "cell_mask_path", "stromal_mask_path", "channel_map_version", "qc_status"]
        with self.manifest.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_valid_metadata_manifest_passes_metadata_only(self):
        result = validate_manifest(self.manifest, self.channel_map, check_files=True, expected_roi_count=1)
        self.assertEqual(result["status"], "PASS_METADATA_ONLY")
        self.assertFalse(result["tensor_qc_performed"])
        self.assertFalse(result["inference_run"])

    def test_duplicate_patient_roi_is_blocked(self):
        row = {"patient_id": "P001", "roi_id": "R001", "image_path": "images/roi1.tif", "cell_mask_path": "cells/roi1.tif", "stromal_mask_path": "stroma/roi1.tif", "channel_map_version": "v1", "qc_status": "not_run"}
        self.write_manifest([row, row])
        result = validate_manifest(self.manifest)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("Duplicate patient/ROI" in error for error in result["errors"]))

    def test_unresolved_marker_mapping_is_blocked(self):
        with self.channel_map.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["channel_index", "marker", "uniprot_id"])
            writer.writeheader()
            writer.writerow({"channel_index": 0, "marker": "CD8", "uniprot_id": "unknown"})
        result = validate_manifest(self.manifest, self.channel_map)
        self.assertEqual(result["status"], "BLOCKED")

    def test_missing_file_is_blocked_when_requested(self):
        row = {"patient_id": "P001", "roi_id": "R001", "image_path": "missing.tif", "cell_mask_path": "cells/roi1.tif", "stromal_mask_path": "stroma/roi1.tif", "channel_map_version": "v1", "qc_status": "not_run"}
        self.write_manifest([row])
        result = validate_manifest(self.manifest, check_files=True)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any("does not exist" in error for error in result["errors"]))

    def test_expected_roi_count_mismatch_is_blocked(self):
        result = validate_manifest(self.manifest, expected_roi_count=86)
        self.assertEqual(result["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
