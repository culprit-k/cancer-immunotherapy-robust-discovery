import io
from zipfile import ZipFile

import numpy as np
import pytest
import tifffile

from analysis.tiff_archive_qc import inspect_tiff_member, summarize_array


def test_summarize_array_reports_normalized_range_and_zero_fraction():
    result = summarize_array(np.array([[0.0, 0.25], [0.5, 1.0]], dtype=np.float32))
    assert result["min"] == pytest.approx(0.0)
    assert result["max"] == pytest.approx(1.0)
    assert result["p50"] == pytest.approx(0.375)
    assert result["zero_fraction"] == pytest.approx(0.25)
    assert result["fraction_below_zero"] == 0
    assert result["fraction_above_one"] == 0
    assert result["dtype"] == "float32"


def test_summarize_array_flags_values_outside_zero_one():
    result = summarize_array(np.array([[-1, 0, 2, 65535]], dtype=np.int32))
    assert result["min"] == -1
    assert result["max"] == 65535
    assert result["fraction_below_zero"] == pytest.approx(0.25)
    assert result["fraction_above_one"] == pytest.approx(0.5)


def test_summarize_mask_can_report_small_label_set():
    result = summarize_array(np.array([[0, 1], [2, 2]], dtype=np.uint8), include_unique_values=True)
    assert result["unique_value_count"] == 3
    assert result["unique_values"] == [0, 1, 2]


def test_empty_and_nonnumeric_arrays_are_rejected():
    with pytest.raises(ValueError):
        summarize_array(np.array([], dtype=np.float32))
    with pytest.raises(TypeError):
        summarize_array(np.array([["a", "b"]]))


def test_inspect_tiff_member_reads_only_metadata_and_summary():
    stream = io.BytesIO()
    tifffile.imwrite(stream, np.stack([
        np.array([[0, 1], [0, 1]], dtype=np.uint16),
        np.array([[1, 2], [3, 4]], dtype=np.uint16),
    ]), photometric="minisblack")
    with ZipFile(io.BytesIO(), mode="w") as archive:
        archive.writestr("stack.tiff", stream.getvalue())
        result = inspect_tiff_member(archive, "stack.tiff", inspect_all_pages=True)
    assert result["series_shape"] == [2, 2, 2]
    assert result["page_count"] == 2
    assert result["pages_inspected"] == 2
    assert result["page_summaries"][1]["max"] == 4
