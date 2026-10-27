import numpy as np
import pandas as pd
import pytest

from analysis.spatial_cell_features import (
    compute_spatial_marker_state_coupling,
    extract_cell_profiles,
    validate_channel_map,
)


def valid_map():
    return pd.DataFrame({
        "plane_index0": [0, 1, 2, 3],
        "marker": ["CD3", "CD8a", "GranzymeB", "CD163"],
        "mapping_evidence": ["source table row 1", "source table row 2",
                             "source table row 3", "source table row 4"],
        "verification_status": ["verified"] * 4,
    })


def test_channel_map_requires_verified_evidence_and_unique_planes():
    m = valid_map()
    assert validate_channel_map(m, n_channels=4, required_markers=["CD3", "CD8a"])["CD8a"] == 1
    m.loc[0, "verification_status"] = "unverified"
    with pytest.raises(ValueError, match="not explicitly marked verified"):
        validate_channel_map(m, n_channels=4, required_markers=["CD3"])
    m = valid_map()
    m.loc[1, "plane_index0"] = 0
    with pytest.raises(ValueError, match="duplicate plane"):
        validate_channel_map(m, n_channels=4, required_markers=["CD3"])


def test_extract_profiles_uses_zero_based_mapping_and_sparse_labels():
    labels = np.array([[0, 2, 2], [7, 7, 0]], dtype=np.uint16)
    image = np.stack([
        np.array([[0, 2, 4], [6, 8, 0]], dtype=float),
        np.array([[0, 10, 20], [30, 50, 0]], dtype=float),
        np.full((2, 3), 2.0),
        np.full((2, 3), 8.0),
    ])
    got = extract_cell_profiles(
        image, labels, valid_map(), roi_id="R1",
        required_markers=["CD3", "CD8a"], background_label=0,
        mask_semantics_verified=True,
    ).set_index("cell_id")
    assert list(got.index) == [2, 7]
    assert got.loc[2, "CD3"] == pytest.approx(3.0)
    assert got.loc[7, "CD3"] == pytest.approx(7.0)
    assert got.loc[2, "CD8a"] == pytest.approx(15.0)
    assert got.loc[2, "cell_area_px"] == 2


def test_extract_fails_closed_when_mask_meaning_not_verified():
    image = np.ones((4, 2, 3))
    labels = np.array([[0, 1, 1], [2, 2, 0]], dtype=np.uint16)
    with pytest.raises(ValueError, match="semantics"):
        extract_cell_profiles(
            image, labels, valid_map(), roi_id="R",
            required_markers=["CD3"], background_label=0,
            mask_semantics_verified=False,
        )


def test_coupling_score_is_deterministic_and_claim_bounded():
    # Grid positions and varying marker scores provide an outcome-blind smoke test.
    n = 36
    x, y = np.meshgrid(np.arange(6), np.arange(6))
    focal = (x + 0.1 * y).ravel().astype(float)
    myeloid = (y + 0.1 * x).ravel().astype(float)
    frame = pd.DataFrame({
        "roi_id": ["R1"] * n,
        "centroid_x_px": x.ravel(),
        "centroid_y_px": y.ravel(),
        "CD3": focal,
        "CD8a": focal + np.linspace(0, 0.01, n),
        "GranzymeB": focal * 0.7 + np.linspace(0, 0.02, n),
        "CD163": myeloid,
        "CD68": myeloid * 0.8 + np.linspace(0, 0.03, n),
    })
    a = compute_spatial_marker_state_coupling(
        frame, cytotoxic_markers=["CD3", "CD8a", "GranzymeB"],
        myeloid_associated_markers=["CD163", "CD68"],
        k_neighbours=4, n_permutations=99, random_state=123,
    )
    b = compute_spatial_marker_state_coupling(
        frame, cytotoxic_markers=["CD3", "CD8a", "GranzymeB"],
        myeloid_associated_markers=["CD163", "CD68"],
        k_neighbours=4, n_permutations=99, random_state=123,
    )
    assert a["observed_spearman_rho"] == pytest.approx(b["observed_spearman_rho"])
    assert a["coupling_delta_vs_shuffle"] == pytest.approx(b["coupling_delta_vs_shuffle"])
    assert "not patient-level" in a["claim_boundary"]


def test_coupling_fails_for_too_few_cells_or_missing_marker():
    frame = pd.DataFrame({
        "centroid_x_px": [0, 1], "centroid_y_px": [0, 0], "A": [1, 2], "B": [3, 4]
    })
    with pytest.raises(ValueError, match="n_cells must exceed"):
        compute_spatial_marker_state_coupling(
            frame, cytotoxic_markers=["A"], myeloid_associated_markers=["B"],
            k_neighbours=2, n_permutations=99,
        )
    frame["centroid_x_px"] = np.arange(2)
    with pytest.raises(ValueError, match="n_cells must exceed"):
        compute_spatial_marker_state_coupling(
            frame, cytotoxic_markers=["MISSING"], myeloid_associated_markers=["B"],
            k_neighbours=2, n_permutations=99,
        )
