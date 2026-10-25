"""Metadata-only TIFF sanity checks for multiplexed image archives.

No pixel arrays are written to the report. Only dimensions, storage types and
summary numeric diagnostics are returned.
"""
from __future__ import annotations

import io
from typing import Any
from zipfile import ZipFile

import numpy as np
import tifffile


def summarize_array(array: Any, *, include_unique_values: bool = False) -> dict[str, Any]:
    """Summarize one raster plane without retaining image pixels in the result."""
    values = np.asarray(array)
    if values.size == 0:
        raise ValueError("Cannot summarize an empty raster")
    if values.dtype.kind not in "biuf":
        raise TypeError(f"Unsupported raster dtype: {values.dtype}")

    numeric = values.astype(np.float64, copy=False)
    finite = np.isfinite(numeric)
    valid = numeric[finite]
    if valid.size == 0:
        raise ValueError("Raster contains no finite numeric values")

    result: dict[str, Any] = {
        "shape": [int(dimension) for dimension in values.shape],
        "dtype": str(values.dtype),
        "pixel_count": int(values.size),
        "finite_pixel_count": int(valid.size),
        "nonfinite_pixel_count": int(values.size - valid.size),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
        "p01": float(np.percentile(valid, 1)),
        "p50": float(np.percentile(valid, 50)),
        "p99": float(np.percentile(valid, 99)),
        "zero_fraction": float(np.count_nonzero(valid == 0) / valid.size),
        "fraction_below_zero": float(np.count_nonzero(valid < 0) / valid.size),
        "fraction_above_one": float(np.count_nonzero(valid > 1) / valid.size),
    }
    if include_unique_values:
        unique = np.unique(values)
        result["unique_value_count"] = int(unique.size)
        if unique.size <= 20:
            result["unique_values"] = [int(v) if np.issubdtype(unique.dtype, np.integer) else float(v) for v in unique]
        else:
            result["unique_values"] = None
    return result


def inspect_tiff_member(
    archive: ZipFile,
    member_name: str,
    *,
    inspect_all_pages: bool = True,
    include_unique_values: bool = False,
) -> dict[str, Any]:
    """Read a TIFF member from a ZIP and return metadata and plane summaries."""
    with archive.open(member_name, "r") as member:
        payload = member.read()

    with tifffile.TiffFile(io.BytesIO(payload)) as tiff:
        if not tiff.series:
            raise ValueError(f"TIFF has no image series: {member_name}")
        series = tiff.series[0]
        pages = list(series.pages)
        if not pages:
            raise ValueError(f"TIFF has no image pages: {member_name}")

        indices = list(range(len(pages))) if inspect_all_pages else [0]
        page_summaries = []
        for index in indices:
            page = pages[index]
            plane = page.asarray()
            summary = summarize_array(plane, include_unique_values=include_unique_values)
            summary["page_index_zero_based"] = int(index)
            page_summaries.append(summary)

        return {
            "series_shape": [int(dimension) for dimension in series.shape],
            "series_dtype": str(series.dtype),
            "page_count": len(pages),
            "pages_inspected": len(indices),
            "page_summaries": page_summaries,
        }
