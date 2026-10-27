import numpy as np
import pytest
import tifffile
from PIL import Image

from scripts.preview_hcc_image_mask_qc import robust_u8, save_label_preview, save_plane_montage


def test_robust_u8_handles_constant_and_nonfinite_arrays():
    assert np.array_equal(robust_u8(np.ones((3, 3))), np.zeros((3, 3), dtype=np.uint8))
    result = robust_u8(np.array([[0.0, 1.0], [np.nan, 2.0]], dtype=float))
    assert result.dtype == np.uint8
    assert result[1, 0] == 0
    assert result.max() == 255


def test_plane_montage_reports_zero_based_planes(tmp_path):
    stack = np.arange(3 * 8 * 9, dtype=np.float32).reshape(3, 8, 9)
    path = tmp_path / "montage.png"
    meta = save_plane_montage(stack, path)
    assert path.is_file()
    assert [row["plane_index0"] for row in meta] == [0, 1, 2]
    assert [row["candidate_panel_channel_1based"] for row in meta] == [1, 2, 3]
    assert Image.open(path).size[0] > 0


def test_label_preview_reports_labels_without_assigning_cell_types(tmp_path):
    mask = np.array([[0, 1, 1], [2, 2, 0]], dtype=np.uint16)
    path = tmp_path / "mask.png"
    meta = save_label_preview(mask, path)
    assert path.is_file()
    assert meta["unique_label_count_including_zero"] == 3
    assert meta["zero_fraction"] == pytest.approx(2 / 6)
    assert "do not identify biological cell types" in meta["warning"]


def test_qc_script_rejects_nonmatching_spatial_dimensions(tmp_path):
    from scripts.preview_hcc_image_mask_qc import main
    import sys

    image_path = tmp_path / "image.tiff"
    mask_path = tmp_path / "mask.tiff"
    tifffile.imwrite(image_path, np.zeros((2, 8, 9), dtype=np.uint16))
    tifffile.imwrite(mask_path, np.zeros((7, 9), dtype=np.uint16))
    monkeypatch_args = [
        "preview_hcc_image_mask_qc.py", "--image", str(image_path),
        "--cell-mask", str(mask_path), "--output-dir", str(tmp_path / "out"),
    ]
    old_argv = sys.argv
    try:
        sys.argv = monkeypatch_args
        with pytest.raises(SystemExit, match="spatial dimensions differ"):
            main()
    finally:
        sys.argv = old_argv
