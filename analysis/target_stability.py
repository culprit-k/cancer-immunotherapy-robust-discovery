"""Evaluation helpers for patient-aware stability audits of target sets.

These are generic measurement utilities, not a novel discovery algorithm.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from typing import Hashable, Iterable, Mapping, Sequence

import numpy as np


def _as_target_sets(target_sets: Sequence[Iterable[str]]) -> list[set[str]]:
    if len(target_sets) == 0:
        raise ValueError("target_sets must contain at least one discovery run")
    normalized: list[set[str]] = []
    for i, targets in enumerate(target_sets):
        try:
            normalized.append(set(targets))
        except TypeError as exc:
            raise TypeError(f"target set at index {i} is not iterable") from exc
    return normalized


def target_selection_frequency(target_sets: Sequence[Iterable[str]]) -> dict[str, float]:
    """Return each target's proportion of discovery runs in which it appears.

    The denominator includes every supplied run, including runs returning an
    empty set. Results are sorted by target name for deterministic output.
    """
    runs = _as_target_sets(target_sets)
    counts: Counter[str] = Counter(target for run in runs for target in run)
    n_runs = len(runs)
    return {target: counts[target] / n_runs for target in sorted(counts)}


def pairwise_jaccard_scores(target_sets: Sequence[Iterable[str]]) -> list[float]:
    """Return all pairwise Jaccard similarities between discovered target sets.

    The similarity of two empty sets is defined as 1.0; always report set size
    too, because an empty strategy can look stable under this convention.
    """
    runs = _as_target_sets(target_sets)
    scores: list[float] = []
    for left, right in combinations(runs, 2):
        union = left | right
        scores.append(1.0 if not union else len(left & right) / len(union))
    return scores


def mean_pairwise_jaccard(target_sets: Sequence[Iterable[str]]) -> float:
    """Return mean pairwise Jaccard similarity, or NaN when fewer than 2 runs exist."""
    scores = pairwise_jaccard_scores(target_sets)
    return float(np.mean(scores)) if scores else float("nan")


def target_direction_consistency(
    signed_target_runs: Sequence[Mapping[str, int]],
) -> dict[str, float]:
    """Return modal direction agreement for each target when selected.

    Each mapping uses +1 or -1 for the recommended direction of a target.
    Targets absent from a run do not enter their direction denominator; pair
    this metric with selection frequency so rare targets are not misread as
    reliable. A target's consistency is max(count(+1), count(-1)) / total.
    """
    if len(signed_target_runs) == 0:
        raise ValueError("signed_target_runs must contain at least one run")
    counts: dict[str, Counter[int]] = defaultdict(Counter)
    for run_index, run in enumerate(signed_target_runs):
        for target, direction in run.items():
            if direction not in (-1, 1):
                raise ValueError(
                    f"direction for {target!r} in run {run_index} must be -1 or +1"
                )
            counts[str(target)][direction] += 1
    return {
        target: max(counts[target].values()) / sum(counts[target].values())
        for target in sorted(counts)
    }


def patient_level_uplift(
    patient_ids: Sequence[Hashable],
    predicted_before: Sequence[float],
    predicted_after: Sequence[float],
) -> dict[str, object]:
    """Summarize model-predicted uplift after averaging patches within patients.

    This is a *predicted* counterfactual change, not an observed treatment effect.
    Each patient receives equal weight regardless of their number of patches.
    """
    before = np.asarray(predicted_before, dtype=float)
    after = np.asarray(predicted_after, dtype=float)
    ids = list(patient_ids)
    if before.ndim != 1 or after.ndim != 1:
        raise ValueError("predicted_before and predicted_after must be one-dimensional")
    if len(ids) != before.size or before.size != after.size:
        raise ValueError("patient_ids and prediction arrays must have equal lengths")
    if before.size == 0:
        raise ValueError("at least one patch-level prediction is required")
    if not (np.isfinite(before).all() and np.isfinite(after).all()):
        raise ValueError("prediction arrays must contain only finite values")

    grouped: dict[Hashable, list[float]] = defaultdict(list)
    for patient, delta in zip(ids, after - before):
        grouped[patient].append(float(delta))
    by_patient = {patient: float(np.mean(deltas)) for patient, deltas in grouped.items()}
    values = np.asarray(list(by_patient.values()), dtype=float)
    return {
        "n_patients": int(values.size),
        "patient_uplift": by_patient,
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "q10": float(np.quantile(values, 0.10)),
        "fraction_positive": float(np.mean(values > 0)),
    }


def bootstrap_mean_ci(
    patient_effects: Sequence[float],
    confidence: float = 0.95,
    n_boot: int = 2000,
    random_state: int = 0,
) -> tuple[float, float]:
    """Percentile bootstrap CI for the mean of independent patient-level effects."""
    effects = np.asarray(patient_effects, dtype=float)
    if effects.ndim != 1 or effects.size == 0:
        raise ValueError("patient_effects must be a non-empty one-dimensional sequence")
    if not np.isfinite(effects).all():
        raise ValueError("patient_effects must contain only finite values")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be strictly between 0 and 1")
    if n_boot < 100:
        raise ValueError("n_boot must be at least 100")
    rng = np.random.default_rng(random_state)
    indices = rng.integers(0, effects.size, size=(n_boot, effects.size))
    means = effects[indices].mean(axis=1)
    tail = (1.0 - confidence) / 2.0
    low, high = np.quantile(means, [tail, 1.0 - tail])
    return float(low), float(high)
