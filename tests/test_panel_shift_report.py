import pandas as pd
import pytest

from analysis.panel_shift_report import build_panel_shift_report


def _example_inputs():
    reconstruction = pd.DataFrame({
        "patient_id": ["P1", "P1", "P2", "P2", "P2", "P2", "P1", "P1", "P2", "P2"],
        "marker": ["CXCL9", "CXCL9", "CXCL9", "CXCL9", "CXCL9", "CXCL9",
                   "PDL1", "PDL1", "PDL1", "PDL1"],
        "measured": [1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 4.0, 3.0, 2.0, 3.0],
        "reconstructed": [1.0, 2.0, 11.0, 12.0, 11.0, 12.0, 3.8, 3.2, 2.1, 2.9],
    })
    prediction_rows = []
    uplifts = {
        "P1": {"reference": 0.4, "reconstructed": 0.3},
        "P2": {"reference": 0.2, "reconstructed": 0.25},
        "P3": {"reference": -0.1, "reconstructed": -0.2},
    }
    for patient, strategies in uplifts.items():
        for strategy, uplift in strategies.items():
            prediction_rows.extend([
                {"patient_id": patient, "strategy": strategy,
                 "predicted_before": 0.0, "predicted_after": uplift - 0.02},
                {"patient_id": patient, "strategy": strategy,
                 "predicted_before": 0.0, "predicted_after": uplift + 0.02},
            ])
    predictions = pd.DataFrame(prediction_rows)
    targets = {
        "reference": {"CXCL9": 1, "PDL1": -1, "LAG3": 1},
        "reconstructed": {"CXCL9": 1, "PDL1": 1, "TIM3": -1},
    }
    return reconstruction, predictions, targets


def test_panel_shift_report_builds_marker_target_and_patient_outputs():
    reconstruction, predictions, targets = _example_inputs()
    report = build_panel_shift_report(reconstruction, predictions, targets)
    assert report["n_heldout_patients"] == 3
    assert report["n_markers_evaluated"] == 2
    assert report["recommendation_fidelity"]["n_direction_flips"] == 1
    assert report["patient_uplift_fidelity"]["n_patients"] == 3
    assert report["model_based_reference_regret"]["mean_candidate_minus_reference"] == pytest.approx(-0.05)
    assert "model-predicted" in report["interpretation_guardrail"]


def test_marker_errors_are_macro_averaged_by_patient():
    reconstruction, predictions, targets = _example_inputs()
    report = build_panel_shift_report(reconstruction, predictions, targets)
    # P1's CXCL9 error is 0; P2's mean error is 10. Patients receive equal weight:
    # macro MAE = 5, whereas a pooled-cell metric would weight P2 more heavily.
    assert report["marker_reconstruction"]["CXCL9"]["n_patients"] == 2
    assert report["marker_reconstruction"]["CXCL9"]["patient_macro"]["mae"] == pytest.approx(5.0)


def test_panel_shift_report_rejects_missing_strategy_for_a_patient():
    reconstruction, predictions, targets = _example_inputs()
    predictions = predictions[~((predictions["patient_id"] == "P3") &
                                (predictions["strategy"] == "reconstructed"))]
    with pytest.raises(ValueError):
        build_panel_shift_report(reconstruction, predictions, targets)


def test_panel_shift_report_rejects_missing_required_columns():
    reconstruction, predictions, targets = _example_inputs()
    reconstruction = reconstruction.drop(columns=["reconstructed"])
    with pytest.raises(ValueError):
        build_panel_shift_report(reconstruction, predictions, targets)
