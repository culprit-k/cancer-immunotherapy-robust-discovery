"""Unit tests for the HCC ROI/clinical manifest audit gate."""
import unittest
from scripts.audit_hcc_roi_clinical_manifest import validate_manifest

def row(stem, patient, roi, *, response="PD", table_roi_count=1, read_status="OK"):
    return {
        "image_stem": stem, "patient_id": patient,
        "roi_label_from_filename": roi, "source_reference": "published Table 3 + filename",
        "resolution_status": "resolved", "read_status": read_status,
        "image_shape": "(45,100,100)", "image_finite_fraction": "1.0",
        "image_min": "0.0", "image_max": "1.0", "channels_45_first": "True",
        "has_cell_mask": "True", "has_stromal_mask": "True",
        "cell_spatial_match": "True", "stroma_spatial_match": "True",
        "table_roi_count": str(table_roi_count), "best_response": response,
        "response_binary": "1" if response == "PR" else "0", "PFS_months": "2.0", "OS_months": "5.0",
        "censored": "1", "etiology": "HCV", "immunotype": "Enriched",
        "clinical_outcome_level": "PATIENT_LEVEL_REPEATED_PER_ROI_DO_NOT_SPLIT_BY_ROI",
    }

class HccManifestTests(unittest.TestCase):
    def test_complete_manifest_passes(self):
        result = validate_manifest([
            row("P01_ROI1", "P01", "ROI1"),
            row("P02_ROI1", "P02", "ROI1", response="PR", table_roi_count=1),
        ], expected_patients=2, expected_images=2)
        self.assertEqual(result["gate"], "PASS")
        self.assertEqual(result["response_counts_patient_level"], {"PD": 1, "PR": 1})

    def test_roi_count_conflict_is_warning_not_silent_rewrite(self):
        result = validate_manifest([
            row("P01_ROI1", "P01", "ROI1", table_roi_count=2),
            row("P01_ROI2", "P01", "ROI2", table_roi_count=2),
            row("P01_ROI3", "P01", "ROI3", table_roi_count=2),
        ], expected_patients=1, expected_images=3)
        self.assertEqual(result["gate"], "PASS_WITH_DISCLOSED_ROI_COUNT_MISMATCHES")
        self.assertEqual(result["warnings"][0]["difference_image_minus_table"], 1)

    def test_inconsistent_patient_outcome_is_blocked(self):
        a = row("P01_ROI1", "P01", "ROI1")
        b = row("P01_ROI2", "P01", "ROI2", response="PR")
        result = validate_manifest([a, b], expected_patients=1, expected_images=2)
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("best_response" in e for e in result["errors"]))

    def test_failed_structural_row_is_blocked(self):
        result = validate_manifest([
            row("P01_ROI1", "P01", "ROI1", read_status="ERROR"),
        ], expected_patients=1, expected_images=1)
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("read_status" in e for e in result["errors"]))

    def test_duplicate_image_stem_is_blocked(self):
        result = validate_manifest([
            row("P01_ROI1", "P01", "ROI1"),
            row("P01_ROI1", "P01", "ROI1"),
        ], expected_patients=1, expected_images=2)
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any("duplicate image_stem" in e for e in result["errors"]))

if __name__ == "__main__":
    unittest.main()
