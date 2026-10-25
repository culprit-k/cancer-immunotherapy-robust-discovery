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
