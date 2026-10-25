"""Metrics for measuring intervention-recommendation fidelity under marker-panel shift.

These functions are evaluation utilities, not a target-discovery algorithm.
Any uplift supplied to them must be labelled as model-predicted unless it
comes from a genuinely observed intervention experiment.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Hashable

import numpy as np
import pandas as pd


def _finite_vector(values: Sequence[float], name: str) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must be a non-empty one-dimensional sequence")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain only finite values")
    return array


def marker_reconstruction_metrics(
    measured: Sequence[float],
    reconstructed: Sequence[float],
) -> dict[str, float]:
    """Compare reconstructed marker values with truly measured held-out values.

    Inputs should be held-out cells/locations only. Report reconstruction
    metrics together with downstream recommendation fidelity; accurate
    reconstruction alone does not establish recommendation validity.
    """
    y_true = _finite_vector(measured, "measured")
    y_pred = _finite_vector(reconstructed, "reconstructed")
    if y_true.size != y_pred.size:
        raise ValueError("measured and reconstructed must have equal lengths")

    error = y_pred - y_true
    pearson = (
        float(np.corrcoef(y_true, y_pred)[0, 1])
        if np.std(y_true) > 0 and np.std(y_pred) > 0
        else float("nan")
    )
    spearman = float(pd.Series(y_true).corr(pd.Series(y_pred), method="spearman"))
    return {
        "n": int(y_true.size),
        "mae": float(np.mean(np.abs(error))),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "bias": float(np.mean(error)),
        "pearson_r": pearson,
        "spearman_r": spearman,
    }


def _validate_signed_targets(targets: Mapping[str, int], name: str) -> dict[str, int]:
    normalized: dict[str, int] = {}
    for marker, direction in targets.items():
        if direction not in (-1, 1):
            raise ValueError(f"{name}[{marker!r}] direction must be -1 or +1")
        normalized[str(marker)] = int(direction)
    return normalized


def intervention_set_fidelity(
    measured_panel_targets: Mapping[str, int],
    reconstructed_panel_targets: Mapping[str, int],
) -> dict[str, float | int]:
    """Compare signed target recommendations from measured vs reconstructed panels.

    The reference is a model output made without using held-out evaluation
    patients, not a known biological ground truth. A signed target encodes
    marker name and intervention direction (+1 increase, -1 decrease).
    """
    reference = _validate_signed_targets(measured_panel_targets, "measured_panel_targets")
    candidate = _validate_signed_targets(reconstructed_panel_targets, "reconstructed_panel_targets")

    ref_items = {(marker, direction) for marker, direction in reference.items()}
    cand_items = {(marker, direction) for marker, direction in candidate.items()}
    union = ref_items | cand_items
    intersection = ref_items & cand_items
    common_markers = set(reference) & set(candidate)
    flips = sum(reference[marker] != candidate[marker] for marker in common_markers)

    precision = len(intersection) / len(cand_items) if cand_items else (1.0 if not ref_items else 0.0)
    recall = len(intersection) / len(ref_items) if ref_items else (1.0 if not cand_items else 0.0)
    return {
        "n_reference_targets": len(reference),
        "n_candidate_targets": len(candidate),
        "signed_jaccard": 1.0 if not union else len(intersection) / len(union),
        "signed_precision": float(precision),
        "signed_recall": float(recall),
        "n_shared_markers": len(common_markers),
        "n_direction_flips": int(flips),
        "direction_agreement": (
            float(1.0 - flips / len(common_markers)) if common_markers else float("nan")
        ),
    }


def patient_uplift_fidelity(
    reference_uplift: Mapping[Hashable, float],
    reconstructed_uplift: Mapping[Hashable, float],
) -> dict[str, float | int]:
    """Compare per-patient model-predicted uplift from full vs reconstructed panels.

    Values must be aggregated to one value per patient, so patients with more
    cores/patches do not receive more weight. Patient IDs must match exactly.
    This is agreement with the full-measurement model, not an observed causal
    treatment effect.
    """
    if not reference_uplift:
        raise ValueError("reference_uplift must contain at least one patient")
    if set(reference_uplift) != set(reconstructed_uplift):
        raise ValueError("patient identifiers must match between both uplift maps")

    ids = list(reference_uplift.keys())
    ref = _finite_vector([reference_uplift[key] for key in ids], "reference_uplift")
    pred = _finite_vector([reconstructed_uplift[key] for key in ids], "reconstructed_uplift")
    error = pred - ref
    ref_sign = np.sign(ref)
    pred_sign = np.sign(pred)
    pearson = (
        float(np.corrcoef(ref, pred)[0, 1])
        if np.std(ref) > 0 and np.std(pred) > 0
        else float("nan")
    )
    spearman = float(pd.Series(ref).corr(pd.Series(pred), method="spearman"))
    return {
        "n_patients": int(len(ids)),
        "mae": float(np.mean(np.abs(error))),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "pearson_r": pearson,
        "spearman_r": spearman,
        "sign_agreement": float(np.mean(ref_sign == pred_sign)),
        "mean_reference_uplift": float(np.mean(ref)),
        "mean_reconstructed_uplift": float(np.mean(pred)),
        "mean_uplift_bias": float(np.mean(error)),
    }


def target_sets_from_runs(
    runs: Sequence[Iterable[tuple[str, int]]],
) -> list[dict[str, int]]:
    """Validate repeated target runs represented as (marker, direction) pairs."""
    if len(runs) == 0:
        raise ValueError("runs must contain at least one run")
    result: list[dict[str, int]] = []
    for index, run in enumerate(runs):
        mapping: dict[str, int] = {}
        for marker, direction in run:
            if marker in mapping:
                raise ValueError(f"duplicate marker {marker!r} in run {index}")
            if direction not in (-1, 1):
                raise ValueError(f"direction for {marker!r} in run {index} must be -1 or +1")
            mapping[str(marker)] = int(direction)
        result.append(mapping)
    return result
