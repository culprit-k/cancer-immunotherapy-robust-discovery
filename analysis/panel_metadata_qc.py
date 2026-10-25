"""Structural quality checks for spatial-proteomics marker panel tables.

These checks validate table consistency only; they do not establish biological
validity, marker-embedding compatibility, or model-input compatibility.
"""
from __future__ import annotations

from collections import Counter
from typing import Any


def audit_panel_structure(fields: list[str], rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Return deterministic structural QC for Channel/MetalTag/Target columns."""
    normalized_fields = {str(field).strip().lower() for field in fields if field}
    required_fields = {"channel", "metaltag", "target"}
    result: dict[str, Any] = {
        "required_columns_present": required_fields.issubset(normalized_fields),
        "missing_required_columns": sorted(required_fields - normalized_fields),
        "blank_required_cells": {},
        "duplicate_channel_values": [],
        "duplicate_metaltag_values": [],
        "duplicate_target_values": [],
        "channels_numeric_and_contiguous_from_1": False,
        "structural_qc_pass": False,
    }
    if not required_fields.issubset(normalized_fields):
        return result

    field_lookup = {str(field).strip().lower(): field for field in fields}
    for normalized_name in sorted(required_fields):
        actual_field = field_lookup[normalized_name]
        result["blank_required_cells"][actual_field] = [
            index + 2 for index, row in enumerate(rows)
            if not str(row.get(actual_field, "") or "").strip()
        ]

    for normalized_name, qc_key in (
        ("channel", "duplicate_channel_values"),
        ("metaltag", "duplicate_metaltag_values"),
        ("target", "duplicate_target_values"),
    ):
        actual_field = field_lookup[normalized_name]
        values = [
            str(row.get(actual_field, "") or "").strip().casefold()
            for row in rows
        ]
        counts = Counter(value for value in values if value)
        result[qc_key] = sorted(value for value, count in counts.items() if count > 1)

    try:
        channels = sorted(int(str(row[field_lookup["channel"]]).strip()) for row in rows)
        result["channels_numeric_and_contiguous_from_1"] = (
            channels == list(range(1, len(rows) + 1))
        )
    except (TypeError, ValueError, KeyError):
        result["channels_numeric_and_contiguous_from_1"] = False

    result["structural_qc_pass"] = bool(
        result["required_columns_present"]
        and not any(result["blank_required_cells"].values())
        and not result["duplicate_channel_values"]
        and not result["duplicate_metaltag_values"]
        and not result["duplicate_target_values"]
        and result["channels_numeric_and_contiguous_from_1"]
        and len(rows) > 0
    )
    return result
