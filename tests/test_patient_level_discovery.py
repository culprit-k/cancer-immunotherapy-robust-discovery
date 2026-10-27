import numpy as np
import pandas as pd
import pytest

from analysis.patient_level_discovery import (
    aggregate_rois_to_patients, benjamini_hochberg, screen_binary_features,
)


def test_bh_adjustment_is_monotone_in_sorted_p_values():
    p = np.array([0.04, 0.001, 0.02, 0.9])
    q = benjamini_hochberg(p)
    assert q[1] <= q[2] <= q[0] <= q[3]
    assert np.all((q >= 0) & (q <= 1))


def test_roi_aggregation_prevents_pseudoreplication_and_uses_median():
    frame = pd.DataFrame({
        "patient": ["P1", "P1", "P1", "P2", "P2"],
        "outcome": ["R", "R", "R", "NR", "NR"],
        "density": [1.0, 2.0, 100.0, 3.0, 5.0],
    })
    got = aggregate_rois_to_patients(
        frame, patient_col="patient", outcome_col="outcome",
        feature_cols=["density"], aggregation="median",
    ).set_index("patient")
    assert got.loc["P1", "density"] == pytest.approx(2.0)
    assert got.loc["P1", "n_rois"] == 3
    assert len(got) == 2


def test_aggregation_rejects_patient_with_conflicting_outcomes():
    frame = pd.DataFrame({"patient": ["P1", "P1"], "outcome": ["R", "NR"], "x": [1, 2]})
    with pytest.raises(ValueError, match="inconsistent"):
        aggregate_rois_to_patients(
            frame, patient_col="patient", outcome_col="outcome", feature_cols=["x"]
        )


def test_screen_returns_effect_uncertainty_fdr_and_influence():
    frame = pd.DataFrame({
        "patient": [f"P{i}" for i in range(12)],
        "outcome": ["R"] * 6 + ["NR"] * 6,
        "signal": [5.2, 5.3, 5.4, 5.1, 5.5, 5.2, 1.0, 1.2, 1.1, 0.9, 1.3, 1.0],
        "noise": [0.2, 0.1, 0.8, 0.4, 0.3, 0.9, 0.7, 0.2, 0.5, 0.1, 0.8, 0.4],
    })
    got = screen_binary_features(
        frame, patient_col="patient", outcome_col="outcome", feature_cols=["signal", "noise"],
        positive_label="R", negative_label="NR", n_permutations=500,
        n_bootstrap=500, random_state=7,
    ).set_index("feature")
    assert got.loc["signal", "mean_difference"] > 0
    assert got.loc["signal", "ci_low"] > 0
    assert 0 <= got.loc["signal", "bh_q_value"] <= 1
    assert got.loc["signal", "leave_one_patient_out_sign_stability"] == 1.0


def test_screen_rejects_multiple_rows_per_patient_and_tiny_classes():
    repeated = pd.DataFrame({
        "patient": ["P1", "P1", "P2", "P3", "P4", "P5"],
        "outcome": ["R", "R", "R", "NR", "NR", "NR"],
        "x": [1, 2, 3, 4, 5, 6],
    })
    with pytest.raises(ValueError, match="exactly one row"):
        screen_binary_features(
            repeated, patient_col="patient", outcome_col="outcome", feature_cols=["x"],
            positive_label="R", negative_label="NR", n_permutations=500, n_bootstrap=500,
        )
    tiny = repeated.drop_duplicates("patient").copy()
    with pytest.raises(ValueError, match="requires >=3"):
        screen_binary_features(
            tiny, patient_col="patient", outcome_col="outcome", feature_cols=["x"],
            positive_label="R", negative_label="NR", n_permutations=500, n_bootstrap=500,
        )
