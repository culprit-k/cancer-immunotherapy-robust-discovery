"""Tests for the fail-closed HCC ROI crosswalk validator."""
import unittest
from scripts.validate_hcc_roi_crosswalk import validate

FIELDS = ["image_stem", "patient_id", "roi_label_from_filename", "source_reference", "resolution_status"]


def row(image, patient, roi, source="supplementary-table-3", status="resolved"):
    return {
        "image_stem": image, "patient_id": patient, "roi_label_from_filename": roi,
        "source_reference": source, "resolution_status": status,
    }


class ValidateHccRoiCrosswalkTests(unittest.TestCase):
    def test_complete_source_backed_crosswalk_passes(self):
        result = validate([
            row("ROI_A", "P01", "ROI1"),
            row("ROI_B", "P02", "ROI1"),
        ], {"ROI_A", "ROI_B"})
        self.assertEqual(result["gate"], "PASS_FILENAME_DERIVED_PATIENT_ROI_CROSSWALK")

    def test_unresolved_row_is_blocked(self):
        result = validate([row("ROI_A", "P01", "ROI1", status="unresolved")], {"ROI_A"})
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("not resolved" in e for e in result["errors"]))

    def test_duplicate_image_is_blocked(self):
        result = validate([
            row("ROI_A", "P01", "ROI1"),
            row("ROI_A", "P01", "ROI2"),
        ], {"ROI_A"})
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("duplicate image_stem" in e for e in result["errors"]))

    def test_missing_image_is_blocked(self):
        result = validate([row("ROI_A", "P01", "ROI1")], {"ROI_A", "ROI_B"})
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertEqual(result["missing_image_stems"], ["ROI_B"])

    def test_duplicate_patient_roi_label_key_is_blocked(self):
        result = validate([
            row("ROI_A", "P01", "ROI1"),
            row("ROI_B", "P01", "ROI1"),
        ], {"ROI_A", "ROI_B"})
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("duplicate patient/ROI-label key" in e for e in result["errors"]))

    def test_missing_source_reference_is_blocked(self):
        result = validate([row("ROI_A", "P01", "ROI1", source="")], {"ROI_A"})
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("blank" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
