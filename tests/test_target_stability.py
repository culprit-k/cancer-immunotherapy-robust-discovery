import math
import pytest

from analysis.target_stability import (
    bootstrap_mean_ci,
    mean_pairwise_jaccard,
    pairwise_jaccard_scores,
    patient_level_uplift,
    target_direction_consistency,
    target_selection_frequency,
)


def test_selection_frequency_counts_empty_runs_in_denominator():
    assert target_selection_frequency([{"A", "B"}, {"A"}, set()]) == {
        "A": pytest.approx(2 / 3),
        "B": pytest.approx(1 / 3),
    }


def test_pairwise_jaccard_values_and_empty_set_convention():
    values = pairwise_jaccard_scores([{"A", "B"}, {"B", "C"}, set()])
    assert values == pytest.approx([1 / 3, 0.0, 0.0])
    assert mean_pairwise_jaccard([set(), set()]) == 1.0
    assert math.isnan(mean_pairwise_jaccard([{"A"}]))


def test_direction_consistency_tracks_sign_not_absence():
    result = target_direction_consistency([
        {"A": 1, "B": -1},
        {"A": 1, "B": 1},
        {"B": -1},
    ])
    assert result == {"A": 1.0, "B": pytest.approx(2 / 3)}


def test_patient_uplift_weights_patients_equally_not_patches():
    out = patient_level_uplift(
        patient_ids=["P1", "P1", "P1", "P2"],
        predicted_before=[0.0, 0.0, 0.0, 0.5],
        predicted_after=[0.1, 0.1, 0.1, 0.4],
    )
    assert out["n_patients"] == 2
    assert out["patient_uplift"] == {"P1": pytest.approx(0.1), "P2": pytest.approx(-0.1)}
    assert out["mean"] == pytest.approx(0.0)
    assert out["fraction_positive"] == pytest.approx(0.5)


def test_bootstrap_ci_is_deterministic_and_ordered():
    left = bootstrap_mean_ci([-0.2, 0.1, 0.4, 0.8], n_boot=500, random_state=12)
    right = bootstrap_mean_ci([-0.2, 0.1, 0.4, 0.8], n_boot=500, random_state=12)
    assert left == right
    assert left[0] <= left[1]


def test_invalid_inputs_fail_loudly():
    with pytest.raises(ValueError):
        target_selection_frequency([])
    with pytest.raises(ValueError):
        target_direction_consistency([{"A": 0}])
    with pytest.raises(ValueError):
        patient_level_uplift(["P1"], [0.1, 0.2], [0.2, 0.3])
