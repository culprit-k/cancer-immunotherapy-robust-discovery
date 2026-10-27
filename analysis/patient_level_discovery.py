"""Patient-level exploratory association analysis for spatial HCC feature tables."""
from __future__ import annotations

from itertools import combinations
from math import comb
from typing import Sequence

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


def benjamini_hochberg(p_values: Sequence[float]) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values, preserving input order."""
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1 or not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("p_values must be a finite one-dimensional sequence in [0, 1]")
    n = p.size
    if n == 0:
        return np.array([], dtype=float)
    order = np.argsort(p, kind="mergesort")
    ranked = p[order] * n / np.arange(1, n + 1, dtype=float)
    adjusted_sorted = np.minimum.accumulate(ranked[::-1])[::-1]
    adjusted = np.empty(n, dtype=float)
    adjusted[order] = np.clip(adjusted_sorted, 0, 1)
    return adjusted


def aggregate_rois_to_patients(
    frame: pd.DataFrame, *, patient_col: str, outcome_col: str,
    feature_cols: Sequence[str], aggregation: str = "median",
) -> pd.DataFrame:
    """Collapse repeated ROIs to one patient row and reject conflicting outcomes."""
    if aggregation not in {"median", "mean"}:
        raise ValueError("aggregation must be 'median' or 'mean'")
    required = [patient_col, outcome_col, *feature_cols]
    missing = [c for c in required if c not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if not feature_cols or frame.empty:
        raise ValueError("input must be non-empty and include feature columns")
    if frame[patient_col].isna().any() or frame[outcome_col].isna().any():
        raise ValueError("patient identifiers and outcomes cannot be missing")
    if frame[patient_col].astype(str).str.strip().eq("").any():
        raise ValueError("blank patient identifiers are not allowed")
    inconsistent = frame.groupby(patient_col)[outcome_col].nunique()
    inconsistent = inconsistent[inconsistent != 1]
    if not inconsistent.empty:
        raise ValueError("outcome is inconsistent within patient(s): " +
                         ", ".join(map(str, inconsistent.index[:10])))

    numeric = frame.loc[:, feature_cols].apply(pd.to_numeric, errors="coerce")
    for c in feature_cols:
        if frame[c].notna().any() and numeric[c].notna().sum() == 0:
            raise ValueError(f"feature column is not numeric: {c}")
    working = pd.concat([
        frame[[patient_col, outcome_col]].reset_index(drop=True),
        numeric.reset_index(drop=True),
    ], axis=1)
    grouped = working.groupby(patient_col, sort=True, dropna=False)
    values = getattr(grouped[list(feature_cols)], aggregation)()
    result = pd.concat([
        grouped[outcome_col].first().rename(outcome_col),
        grouped.size().rename("n_rois"),
        values,
    ], axis=1).reset_index()
    result["feature_missing_fraction"] = result[list(feature_cols)].isna().mean(axis=1)
    return result


def _permutation_p(positive: np.ndarray, negative: np.ndarray, *,
                   n_permutations: int, rng: np.random.Generator) -> float:
    pooled = np.concatenate([positive, negative])
    n_pos = positive.size
    observed = float(positive.mean() - negative.mean())
    assignments = comb(pooled.size, n_pos)
    if assignments <= 20000:
        exceed = total = 0
        for idx in combinations(range(pooled.size), n_pos):
            mask = np.zeros(pooled.size, dtype=bool)
            mask[list(idx)] = True
            diff = float(pooled[mask].mean() - pooled[~mask].mean())
            exceed += abs(diff) >= abs(observed) - 1e-15
            total += 1
        return float(exceed / total)
    exceed = 0
    for _ in range(n_permutations):
        shuffled = rng.permutation(pooled)
        diff = float(shuffled[:n_pos].mean() - shuffled[n_pos:].mean())
        exceed += abs(diff) >= abs(observed) - 1e-15
    return float((exceed + 1) / (n_permutations + 1))


def _bootstrap_ci(positive: np.ndarray, negative: np.ndarray, *,
                  n_bootstrap: int, confidence: float,
                  rng: np.random.Generator) -> tuple[float, float]:
    pi = rng.integers(0, positive.size, size=(n_bootstrap, positive.size))
    ni = rng.integers(0, negative.size, size=(n_bootstrap, negative.size))
    diffs = positive[pi].mean(axis=1) - negative[ni].mean(axis=1)
    alpha = (1 - confidence) / 2
    lo, hi = np.quantile(diffs, [alpha, 1 - alpha])
    return float(lo), float(hi)


def screen_binary_features(
    patients: pd.DataFrame, *, patient_col: str, outcome_col: str,
    feature_cols: Sequence[str], positive_label: str, negative_label: str,
    n_permutations: int = 20000, n_bootstrap: int = 5000,
    confidence: float = 0.95, random_state: int = 20261027,
) -> pd.DataFrame:
    """Estimate patient-level effects, uncertainty, permutation p and FDR q-values."""
    if positive_label == negative_label:
        raise ValueError("positive_label and negative_label must differ")
    if n_permutations < 100 or n_bootstrap < 500:
        raise ValueError("use at least 100 permutations and 500 bootstrap samples")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be strictly between 0 and 1")
    missing = [c for c in [patient_col, outcome_col, *feature_cols]
               if c not in patients.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if patients[patient_col].duplicated().any():
        raise ValueError("patients table must contain exactly one row per patient")
    use = patients[patients[outcome_col].isin([positive_label, negative_label])].copy()
    n_pos = int((use[outcome_col] == positive_label).sum())
    n_neg = int((use[outcome_col] == negative_label).sum())
    if n_pos < 3 or n_neg < 3:
        raise ValueError(f"requires >=3 patients per group; found {n_pos} and {n_neg}")

    rng = np.random.default_rng(random_state)
    rows: list[dict[str, object]] = []
    for feature in feature_cols:
        vals = pd.to_numeric(use[feature], errors="coerce")
        valid = vals.notna() & np.isfinite(vals.to_numpy(dtype=float, na_value=np.nan))
        sub = use.loc[valid, [patient_col, outcome_col]].copy()
        sub["_x"] = vals.loc[valid].to_numpy(dtype=float)
        pos = sub.loc[sub[outcome_col] == positive_label, "_x"].to_numpy(dtype=float)
        neg = sub.loc[sub[outcome_col] == negative_label, "_x"].to_numpy(dtype=float)
        base = {
            "feature": feature, "n_positive": int(pos.size), "n_negative": int(neg.size),
            "missing_fraction": float(1 - valid.mean()),
        }
        if pos.size < 3 or neg.size < 3 or np.allclose(np.concatenate([pos, neg]), pos[0]):
            rows.append({**base, "mean_positive": float(np.mean(pos)) if pos.size else np.nan,
                         "mean_negative": float(np.mean(neg)) if neg.size else np.nan,
                         "mean_difference": np.nan, "median_difference": np.nan,
                         "rank_biserial_positive_vs_negative": np.nan, "ci_low": np.nan,
                         "ci_high": np.nan, "permutation_p": np.nan,
                         "leave_one_patient_out_sign_stability": np.nan,
                         "status": "insufficient or constant feature"})
            continue

        mean_diff = float(pos.mean() - neg.mean())
        median_diff = float(np.median(pos) - np.median(neg))
        u = float(mannwhitneyu(pos, neg, alternative="two-sided", method="auto").statistic)
        rank_biserial = float(2 * u / (pos.size * neg.size) - 1)
        lo, hi = _bootstrap_ci(pos, neg, n_bootstrap=n_bootstrap,
                               confidence=confidence, rng=rng)
        p = _permutation_p(pos, neg, n_permutations=n_permutations, rng=rng)

        # Leave-one-patient-out sign stability diagnoses dependence on one patient.
        x = sub["_x"].to_numpy(dtype=float)
        y = sub[outcome_col].to_numpy()
        signs = []
        expected = 1 if mean_diff > 0 else -1 if mean_diff < 0 else 0
        for i in range(len(sub)):
            keep = np.arange(len(sub)) != i
            pvals = x[keep & (y == positive_label)]
            nvals = x[keep & (y == negative_label)]
            if pvals.size and nvals.size:
                d = pvals.mean() - nvals.mean()
                signs.append(1 if d > 0 else -1 if d < 0 else 0)
        rows.append({
            **base, "mean_positive": float(pos.mean()), "mean_negative": float(neg.mean()),
            "mean_difference": mean_diff, "median_difference": median_diff,
            "rank_biserial_positive_vs_negative": rank_biserial,
            "ci_low": lo, "ci_high": hi, "permutation_p": p,
            "leave_one_patient_out_sign_stability": float(np.mean(np.asarray(signs) == expected)),
            "status": "exploratory",
        })

    result = pd.DataFrame(rows)
    result["bh_q_value"] = benjamini_hochberg(result["permutation_p"].fillna(1.0).to_numpy())
    result["analysis_warning"] = (
        f"Exploratory association only: {n_pos} positive and {n_neg} negative patients; "
        "not causal proof or validated clinical prediction."
    )
    return result.sort_values(["bh_q_value", "permutation_p", "feature"],
                              na_position="last").reset_index(drop=True)
