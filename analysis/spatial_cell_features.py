"""Outcome-blind, ROI-level spatial marker-state coupling features.

Inputs must have passed the cohort's channel-plane and cell-instance mask audits.
This module does not assign biological cell identities. Its score is an association
between marker-state scores across neighbouring segmented objects, not a causal
or cell-type-specific mechanism.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import rankdata, spearmanr


def validate_channel_map(
    channel_map: pd.DataFrame,
    *,
    n_channels: int,
    required_markers: Sequence[str],
) -> dict[str, int]:
    """Validate an explicitly reviewed map from image plane to marker.

    Required columns: plane_index0, marker, mapping_evidence, verification_status.
    Rows are accepted only when status is exactly 'verified' and evidence is nonempty.
    This metadata gate cannot independently prove a human's verification.
    """
    required_cols = {"plane_index0", "marker", "mapping_evidence", "verification_status"}
    missing = required_cols - set(channel_map.columns)
    if missing:
        raise ValueError(f"channel map missing columns: {sorted(missing)}")
    if channel_map.empty:
        raise ValueError("channel map is empty")
    if channel_map["plane_index0"].isna().any() or channel_map["marker"].isna().any():
        raise ValueError("plane_index0 and marker cannot be missing")
    planes = pd.to_numeric(channel_map["plane_index0"], errors="coerce")
    if planes.isna().any() or not np.equal(planes.to_numpy(), np.floor(planes.to_numpy())).all():
        raise ValueError("plane_index0 must contain integer, zero-based plane indices")
    if planes.duplicated().any():
        raise ValueError("duplicate plane_index0 entries")
    if channel_map["marker"].astype(str).str.strip().eq("").any():
        raise ValueError("blank marker names are not allowed")
    if channel_map["marker"].duplicated().any():
        raise ValueError("duplicate marker names are not allowed")
    if ((planes < 0) | (planes >= n_channels)).any():
        raise ValueError("plane_index0 falls outside image channel dimension")
    status = channel_map["verification_status"].astype(str).str.strip().str.lower()
    if not status.eq("verified").all():
        raise ValueError("channel map contains entries not explicitly marked verified")
    evidence = channel_map["mapping_evidence"].fillna("").astype(str).str.strip()
    if not evidence.ne("").all():
        raise ValueError("every mapping row requires source evidence")
    result = dict(zip(channel_map["marker"].astype(str), planes.astype(int)))
    absent = sorted(set(required_markers) - set(result))
    if absent:
        raise ValueError(f"required markers absent from verified map: {absent}")
    return result


def extract_cell_profiles(
    image: np.ndarray,
    cell_labels: np.ndarray,
    channel_map: pd.DataFrame,
    *,
    roi_id: str,
    required_markers: Sequence[str],
    background_label: int,
    mask_semantics_verified: bool,
) -> pd.DataFrame:
    """Compute per-cell mean intensities and centroids from a (C,H,W) stack.

    The caller must explicitly confirm that the mask is an instance-label mask
    and supply the documented background label. No biological type labels are
    inferred. Intensities are kept in the supplied image scale without hidden
    normalization or thresholding.
    """
    if not mask_semantics_verified:
        raise ValueError("cell-instance mask semantics must be source-verified first")
    img = np.asarray(image)
    labels = np.asarray(cell_labels)
    if img.ndim != 3:
        raise ValueError("image must have shape (C, H, W)")
    if labels.ndim != 2 or labels.shape != img.shape[1:]:
        raise ValueError("cell_labels must be 2D and spatially match image")
    if not np.issubdtype(labels.dtype, np.integer):
        raise ValueError("cell_labels must be an integer instance-label array")
    if not np.isfinite(img).all():
        raise ValueError("image contains non-finite values")
    if np.any(labels < 0):
        raise ValueError("negative cell instance labels are not supported")
    marker_planes = validate_channel_map(
        channel_map, n_channels=img.shape[0], required_markers=required_markers
    )
    ids, inverse = np.unique(labels.ravel(), return_inverse=True)
    counts = np.bincount(inverse, minlength=ids.size).astype(np.int64)
    nonbackground = ids != background_label
    ids = ids[nonbackground]
    counts = counts[nonbackground]
    if ids.size < 2:
        raise ValueError("ROI must contain at least two non-background cell objects")

    # Rebuild object indices after excluding background; this avoids iterating over
    # sparse raw labels and avoids any assumption that labels are consecutive.
    flat_labels = labels.ravel()
    keep = flat_labels != background_label
    object_ids, inverse_keep = np.unique(flat_labels[keep], return_inverse=True)
    obj_counts = np.bincount(inverse_keep, minlength=object_ids.size).astype(np.int64)
    yy, xx = np.indices(labels.shape)
    x_sum = np.bincount(inverse_keep, weights=xx.ravel()[keep], minlength=object_ids.size)
    y_sum = np.bincount(inverse_keep, weights=yy.ravel()[keep], minlength=object_ids.size)
    out = pd.DataFrame({
        "roi_id": str(roi_id),
        "cell_id": object_ids.astype(np.int64),
        "cell_area_px": obj_counts,
        "centroid_x_px": x_sum / obj_counts,
        "centroid_y_px": y_sum / obj_counts,
    })
    for marker in required_markers:
        plane = marker_planes[marker]
        values = img[plane].ravel()[keep].astype(np.float64, copy=False)
        sums = np.bincount(inverse_keep, weights=values, minlength=object_ids.size)
        out[marker] = sums / obj_counts
    return out


def _rank_score(frame: pd.DataFrame, markers: Sequence[str]) -> np.ndarray:
    if not markers:
        raise ValueError("at least one marker is required for each score")
    missing = [m for m in markers if m not in frame.columns]
    if missing:
        raise ValueError(f"marker columns missing from cell profiles: {missing}")
    scores = []
    for marker in markers:
        values = pd.to_numeric(frame[marker], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"marker {marker} contains missing/non-finite values")
        scores.append(rankdata(values, method="average") / max(1, len(values)))
    return np.mean(np.vstack(scores), axis=0)


def _nearest_neighbour_mean(points: np.ndarray, values: np.ndarray, k: int) -> np.ndarray:
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must have shape (n_cells, 2)")
    n = len(points)
    if n <= k:
        raise ValueError(f"n_cells must exceed k={k}; found {n}")
    tree = cKDTree(points)
    _, indices = tree.query(points, k=min(n, k + 1))
    result = np.empty(n, dtype=float)
    for i in range(n):
        candidates = np.atleast_1d(indices[i]).astype(int)
        candidates = candidates[candidates != i]
        if candidates.size < k:
            # Duplicate coordinates / ties can make the initial k+1 query miss a
            # self-excluded neighbour; fetch the full ordered list for this cell.
            candidates = np.asarray(tree.query(points[i], k=n)[1], dtype=int)
            candidates = candidates[candidates != i]
        nearest = candidates[:k]
        result[i] = float(np.mean(values[nearest]))
    return result


def compute_spatial_marker_state_coupling(
    cell_profiles: pd.DataFrame,
    *,
    cytotoxic_markers: Sequence[str],
    myeloid_associated_markers: Sequence[str],
    k_neighbours: int = 8,
    n_permutations: int = 999,
    random_state: int = 20261027,
) -> dict[str, object]:
    """Calculate ROI-level marker-state coupling versus within-ROI spatial shuffles.

    The focal-cell score is the mean within-ROI percentile rank of the requested
    cytotoxic-associated markers. The neighbourhood score is the mean percentile
    rank of myeloid-associated markers among the k nearest cell centroids.
    The statistic is Spearman rho between these scores. The null shuffles the
    neighbourhood-state scores across fixed coordinates. Its p-value is an ROI
    diagnostic only; inferential tests must use patient-level aggregation.
    """
    needed = {"centroid_x_px", "centroid_y_px"}
    if not needed.issubset(cell_profiles.columns):
        raise ValueError(f"cell profiles require columns: {sorted(needed)}")
    if cell_profiles.empty:
        raise ValueError("cell_profiles is empty")
    if cell_profiles[["centroid_x_px", "centroid_y_px"]].isna().any().any():
        raise ValueError("cell centroids contain missing coordinates")
    points = cell_profiles[["centroid_x_px", "centroid_y_px"]].to_numpy(dtype=float)
    if not np.isfinite(points).all():
        raise ValueError("cell centroids must be finite")
    if k_neighbours < 1:
        raise ValueError("k_neighbours must be at least 1")
    if n_permutations < 99:
        raise ValueError("n_permutations must be at least 99")

    focal = _rank_score(cell_profiles, cytotoxic_markers)
    neighbour_state = _rank_score(cell_profiles, myeloid_associated_markers)
    neighbours = _nearest_neighbour_mean(points, neighbour_state, k_neighbours)
    if np.ptp(focal) == 0 or np.ptp(neighbours) == 0:
        raise ValueError("coupling score is undefined because a rank score is constant")
    observed = float(spearmanr(focal, neighbours).statistic)
    rng = np.random.default_rng(random_state)
    null = np.empty(n_permutations, dtype=float)
    for i in range(n_permutations):
        shuffled = rng.permutation(neighbour_state)
        shuffled_neighbours = _nearest_neighbour_mean(points, shuffled, k_neighbours)
        null[i] = float(spearmanr(focal, shuffled_neighbours).statistic)
    null_median = float(np.median(null))
    delta = observed - null_median
    p_value = float((1 + np.sum(np.abs(null - null_median) >= abs(delta))) / (n_permutations + 1))
    return {
        "roi_id": str(cell_profiles["roi_id"].iloc[0]) if "roi_id" in cell_profiles else "",
        "n_cells": int(len(cell_profiles)),
        "k_neighbours": int(k_neighbours),
        "cytotoxic_markers": list(cytotoxic_markers),
        "myeloid_associated_markers": list(myeloid_associated_markers),
        "observed_spearman_rho": observed,
        "shuffle_null_median_rho": null_median,
        "coupling_delta_vs_shuffle": float(delta),
        "shuffle_null_q025": float(np.quantile(null, 0.025)),
        "shuffle_null_q975": float(np.quantile(null, 0.975)),
        "roi_shuffle_p_value_descriptive_only": p_value,
        "random_seed": int(random_state),
        "claim_boundary": (
            "Continuous marker-state spatial association only; no cell type was inferred, "
            "and this ROI-level shuffle p-value is not patient-level biological inference."
        ),
    }
