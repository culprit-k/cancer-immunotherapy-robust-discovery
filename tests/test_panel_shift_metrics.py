import math

import pytest

from analysis.panel_shift_metrics import (
    intervention_set_fidelity,
    marker_reconstruction_metrics,
    patient_uplift_fidelity,
    target_sets_from_runs,
)


def test_marker_reconstruction_metrics_exact_prediction():
    result = marker_reconstruction_metrics([1, 2, 4, 8], [1, 2, 4, 8])
    assert result["n"] == 4
    assert result["mae"] == pytest.approx(0)
    assert result["rmse"] == pytest.approx(0)
    assert result["pearson_r"] == pytest.approx(1)
    assert result["spearman_r"] == pytest.approx(1)


def test_marker_reconstruction_metrics_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        marker_reconstruction_metrics([1, 2], [1])


def test_intervention_fidelity_penalizes_changed_target_direction():
    result = intervention_set_fidelity(
        {"CXCL9": 1, "PDL1": -1, "LAG3": 1},
        {"CXCL9": 1, "PDL1": 1, "TIM3": -1},
    )
    assert result["n_direction_flips"] == 1
    assert result["n_shared_markers"] == 2
    assert result["direction_agreement"] == pytest.approx(0.5)
    assert result["signed_jaccard"] == pytest.approx(1 / 5)
    assert result["signed_precision"] == pytest.approx(1 / 3)
    assert result["signed_recall"] == pytest.approx(1 / 3)


def test_intervention_fidelity_empty_sets_are_handled():
    result = intervention_set_fidelity({}, {})
    assert result["signed_jaccard"] == 1.0
    assert math.isnan(result["direction_agreement"])


def test_patient_uplift_fidelity_compares_equal_weighted_patient_values():
    result = patient_uplift_fidelity(
        {"A": 0.2, "B": -0.1, "C": 0.4},
        {"A": 0.1, "B": -0.2, "C": 0.3},
    )
    assert result["n_patients"] == 3
    assert result["mae"] == pytest.approx(0.1)
    assert result["sign_agreement"] == pytest.approx(1.0)


def test_patient_uplift_fidelity_requires_matching_patient_ids():
    with pytest.raises(ValueError):
        patient_uplift_fidelity({"A": 0.1}, {"B": 0.1})


def test_target_runs_validate_directions_and_duplicates():
    assert target_sets_from_runs([[("A", 1)], [("A", -1), ("B", 1)]]) == [
        {"A": 1},
        {"A": -1, "B": 1},
    ]
    with pytest.raises(ValueError):
        target_sets_from_runs([[("A", 0)]])
    with pytest.raises(ValueError):
        target_sets_from_runs([[("A", 1), ("A", -1)]])


def test_patient_reference_regret_compares_same_patients_and_evaluator():
    from analysis.panel_shift_metrics import patient_reference_regret

    result = patient_reference_regret(
        {"P1": 0.4, "P2": 0.2, "P3": -0.1},
        {"P1": 0.3, "P2": 0.25, "P3": -0.2},
    )
    assert result["n_patients"] == 3
    assert result["mean_candidate_minus_reference"] == pytest.approx(-0.05)
    assert result["fraction_candidate_lower"] == pytest.approx(2 / 3)
    assert result["mean_absolute_difference"] == pytest.approx(0.08333333333333333)


def test_patient_reference_regret_rejects_patient_mismatch():
    from analysis.panel_shift_metrics import patient_reference_regret

    with pytest.raises(ValueError):
        patient_reference_regret({"P1": 0.1}, {"P2": 0.1})
