"""Create a post-hoc panel-shift fidelity report from held-out evaluation tables.

This utility does not run a model. It evaluates marker reconstruction outputs,
signed target recommendations, and patient-level model-predicted objective
values produced by a separately audited discovery pipeline.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

from analysis.panel_shift_metrics import (
    intervention_set_fidelity,
    marker_reconstruction_metrics,
    patient_reference_regret,
    patient_uplift_fidelity,
)


def _require_columns(frame: pd.DataFrame, columns: set[str], label: str) -> None:
    missing = sorted(columns - set(frame.columns))
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def _finite_mean(values: list[float]) -> float:
    """Mean over finite patient-level metrics; return NaN when none are defined."""
    array = np.asarray(values, dtype=float)
    array = array[np.isfinite(array)]
    return float(np.mean(array)) if array.size else float("nan")


def _json_safe(value: Any) -> Any:
    """Replace NaN/inf with null so the report is strict JSON."""
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (float, np.floating)):
        return float(value) if math.isfinite(float(value)) else None
    if isinstance(value, (int, np.integer)):
        return int(value)
    return value


def build_panel_shift_report(
    reconstruction: pd.DataFrame,
    predictions: pd.DataFrame,
    target_sets: Mapping[str, Mapping[str, int]],
    reference_name: str = "reference",
    candidate_name: str = "reconstructed",
) -> dict[str, Any]:
    """Build a fidelity report from prepared held-out tables.

    reconstruction columns:
        patient_id, marker, measured, reconstructed
    Each row should represent one held-out cell/location and one marker. Each
    marker's error metrics are computed within patient first, then macro-averaged
    across patients so patients with more cells do not dominate the primary error.

    predictions columns:
        patient_id, strategy, predicted_before, predicted_after
    Each row may represent a held-out core/tile/patch. Both named strategies
    must be evaluated on fully measured versions of the same held-out patients
    using the same evaluator. Rows are averaged within patient and strategy.

    target_sets maps strategy names to {marker: +1/-1} signed targets.
    """
    _require_columns(
        reconstruction, {"patient_id", "marker", "measured", "reconstructed"}, "reconstruction table"
    )
    _require_columns(
        predictions,
        {"patient_id", "strategy", "predicted_before", "predicted_after"},
        "predictions table",
    )
    if reference_name == candidate_name:
        raise ValueError("reference_name and candidate_name must be different")
    for name in (reference_name, candidate_name):
        if name not in target_sets:
            raise ValueError(f"target_sets is missing strategy {name!r}")

    if reconstruction.empty:
        raise ValueError("reconstruction table must not be empty")
    if predictions.empty:
        raise ValueError("predictions table must not be empty")
    if reconstruction[["patient_id", "marker", "measured", "reconstructed"]].isna().any().any():
        raise ValueError("reconstruction table contains missing values")
    if predictions[["patient_id", "strategy", "predicted_before", "predicted_after"]].isna().any().any():
        raise ValueError("predictions table contains missing values")

    for column in ("measured", "reconstructed"):
        values = pd.to_numeric(reconstruction[column], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"reconstruction column {column!r} must be numeric and finite")
    for column in ("predicted_before", "predicted_after"):
        values = pd.to_numeric(predictions[column], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"prediction column {column!r} must be numeric and finite")

    selected_predictions = predictions[
        predictions["strategy"].isin([reference_name, candidate_name])
    ].copy()
    if selected_predictions.empty:
        raise ValueError("no rows found for the requested reference/candidate strategies")

    selected_predictions["uplift"] = (
        pd.to_numeric(selected_predictions["predicted_after"], errors="raise")
        - pd.to_numeric(selected_predictions["predicted_before"], errors="raise")
    )
    patient_strategy = selected_predictions.groupby(
        ["patient_id", "strategy"], as_index=False
    )["uplift"].mean()
    matrix = patient_strategy.pivot(
        index="patient_id", columns="strategy", values="uplift"
    )
    for name in (reference_name, candidate_name):
        if name not in matrix.columns:
            raise ValueError(f"no held-out patient predictions found for strategy {name!r}")
    matrix = matrix[[reference_name, candidate_name]].dropna()
    if matrix.empty:
        raise ValueError("no patient has predictions for both strategies")
    if patient_strategy["patient_id"].nunique() != matrix.shape[0]:
        raise ValueError(
            "every patient must have predictions for both strategies; "
            "do not silently compare different patient sets"
        )

    per_marker: dict[str, Any] = {}
    metric_names = ("mae", "rmse", "bias", "pearson_r", "spearman_r")
    for marker, subset in reconstruction.groupby("marker", sort=True):
        patient_metrics = []
        for _, patient_subset in subset.groupby("patient_id", sort=False):
            patient_metrics.append(marker_reconstruction_metrics(
                pd.to_numeric(patient_subset["measured"], errors="raise").to_numpy(dtype=float),
                pd.to_numeric(patient_subset["reconstructed"], errors="raise").to_numpy(dtype=float),
            ))
        pooled_metrics = marker_reconstruction_metrics(
            pd.to_numeric(subset["measured"], errors="raise").to_numpy(dtype=float),
            pd.to_numeric(subset["reconstructed"], errors="raise").to_numpy(dtype=float),
        )
        per_marker[str(marker)] = {
            "n_patients": int(len(patient_metrics)),
            "n_values": int(len(subset)),
            "patient_macro": {
                name: _finite_mean([float(metrics[name]) for metrics in patient_metrics])
                for name in metric_names
            },
            "patients_with_defined_correlation": {
                name: int(sum(np.isfinite(float(metrics[name])) for metrics in patient_metrics))
                for name in ("pearson_r", "spearman_r")
            },
            "pooled_cells_secondary": pooled_metrics,
        }

    ref_uplift = {
        patient: float(value)
        for patient, value in matrix[reference_name].items()
    }
    candidate_uplift = {
        patient: float(value)
        for patient, value in matrix[candidate_name].items()
    }

    return _json_safe({
        "n_heldout_patients": int(matrix.shape[0]),
        "n_reconstruction_rows": int(len(reconstruction)),
        "n_markers_evaluated": int(reconstruction["marker"].nunique()),
        "marker_reconstruction": per_marker,
        "recommendation_fidelity": intervention_set_fidelity(
            target_sets[reference_name], target_sets[candidate_name]
        ),
        "patient_uplift_fidelity": patient_uplift_fidelity(
            ref_uplift, candidate_uplift
        ),
        "model_based_reference_regret": patient_reference_regret(
            ref_uplift, candidate_uplift
        ),
        "interpretation_guardrail": (
            "All uplift values are model-predicted. The full-measurement strategy is "
            "a model reference, not biological ground truth or an observed treatment effect."
        ),
    })


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate marker reconstruction and counterfactual recommendation fidelity."
    )
    parser.add_argument("--reconstruction-csv", required=True, type=Path)
    parser.add_argument("--predictions-csv", required=True, type=Path)
    parser.add_argument("--target-sets-json", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--reference-name", default="reference")
    parser.add_argument("--candidate-name", default="reconstructed")
    args = parser.parse_args()

    reconstruction = pd.read_csv(args.reconstruction_csv)
    predictions = pd.read_csv(args.predictions_csv)
    with args.target_sets_json.open("r", encoding="utf-8") as stream:
        target_sets = json.load(stream)
    report = build_panel_shift_report(
        reconstruction=reconstruction,
        predictions=predictions,
        target_sets=target_sets,
        reference_name=args.reference_name,
        candidate_name=args.candidate_name,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    with args.output_json.open("w", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
    print(f"Saved panel-shift fidelity report to {args.output_json}")


if __name__ == "__main__":
    main()
