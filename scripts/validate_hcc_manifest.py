#!/usr/bin/env python3
"""Fail-closed metadata validator for the HCC–VirTues ROI manifest.

This checks manifest consistency and optional path existence only. It does not
inspect TIFF tensor contents, prove mask alignment, validate biological marker
identity, establish checkpoint eligibility, or run VirTues inference.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {
    "patient_id", "roi_id", "image_path", "cell_mask_path",
    "stromal_mask_path", "channel_map_version", "qc_status",
}
CHANNEL_COLUMNS = {"channel_index", "marker", "uniprot_id"}


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            return [], []
        return list(reader), list(reader.fieldnames)


def validate_manifest(
    manifest_path: Path,
    channel_map_path: Path | None = None,
    check_files: bool = False,
    expected_roi_count: int | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, Any] = {
        "manifest_rows": 0,
        "unique_patients": 0,
        "unique_patient_roi_pairs": 0,
    }
    if not manifest_path.is_file():
        return {
            "status": "BLOCKED",
            "errors": [f"Manifest file does not exist: {manifest_path}"],
            "warnings": [],
            "counts": counts,
            "tensor_qc_performed": False,
            "checkpoint_verified": False,
            "inference_run": False,
        }

    rows, columns = read_csv(manifest_path)
    counts["manifest_rows"] = len(rows)
    missing_columns = sorted(REQUIRED_COLUMNS - set(columns))
    if missing_columns:
        errors.append("Missing required manifest columns: " + ", ".join(missing_columns))
    if not rows:
        errors.append("Manifest has no data rows")

    patient_ids: set[str] = set()
    pair_keys: list[tuple[str, str]] = []
    image_paths: list[str] = []
    mask_paths: list[str] = []
    for row_index, row in enumerate(rows, start=2):
        def val(key: str) -> str:
            return (row.get(key) or "").strip()

        missing_values = [key for key in REQUIRED_COLUMNS if not val(key)]
        if missing_values:
            errors.append(f"Row {row_index}: blank required values: {', '.join(sorted(missing_values))}")
        patient_id, roi_id = val("patient_id"), val("roi_id")
        if patient_id:
            patient_ids.add(patient_id)
        if patient_id and roi_id:
            pair_keys.append((patient_id, roi_id))
        for key in ("image_path", "cell_mask_path", "stromal_mask_path"):
            value = val(key)
            if value and chr(0) in value:
                errors.append(f"Row {row_index}: NUL byte in {key}")
            if value and check_files:
                candidate = Path(value)
                if not candidate.is_absolute():
                    candidate = manifest_path.parent / candidate
                if not candidate.is_file():
                    errors.append(f"Row {row_index}: {key} does not exist: {candidate}")
        image_paths.append(val("image_path"))
        mask_paths.extend([val("cell_mask_path"), val("stromal_mask_path")])

    pair_counts = Counter(pair_keys)
    duplicates = sorted([f"{patient}/{roi}" for (patient, roi), n in pair_counts.items() if n > 1])
    if duplicates:
        errors.append("Duplicate patient/ROI keys: " + ", ".join(duplicates))
    duplicate_images = sorted([path for path, n in Counter(x for x in image_paths if x).items() if n > 1])
    if duplicate_images:
        errors.append("Image paths reused across manifest rows: " + ", ".join(duplicate_images))
    if expected_roi_count is not None and len(rows) != expected_roi_count:
        errors.append(f"Expected {expected_roi_count} ROI rows but found {len(rows)}")

    counts["unique_patients"] = len(patient_ids)
    counts["unique_patient_roi_pairs"] = len(set(pair_keys))
    counts["unique_image_paths"] = len(set(x for x in image_paths if x))
    counts["unique_mask_paths"] = len(set(x for x in mask_paths if x))

    channel_summary: dict[str, Any] = {"checked": False}
    if channel_map_path is not None:
        if not channel_map_path.is_file():
            errors.append(f"Channel map file does not exist: {channel_map_path}")
        else:
            channel_rows, channel_columns = read_csv(channel_map_path)
            missing = sorted(CHANNEL_COLUMNS - set(channel_columns))
            if missing:
                errors.append("Missing channel-map columns: " + ", ".join(missing))
            if not channel_rows:
                errors.append("Channel map has no data rows")
            indexes: list[int] = []
            seen_markers: set[str] = set()
            for line, row in enumerate(channel_rows, start=2):
                idx_text = (row.get("channel_index") or "").strip()
                marker = (row.get("marker") or "").strip()
                uniprot = (row.get("uniprot_id") or "").strip()
                if not idx_text or not marker or not uniprot:
                    errors.append(f"Channel map row {line}: channel_index, marker, and uniprot_id are all required")
                    continue
                try:
                    indexes.append(int(idx_text))
                except ValueError:
                    errors.append(f"Channel map row {line}: channel_index must be an integer: {idx_text}")
                if marker.casefold() in seen_markers:
                    errors.append(f"Channel map row {line}: duplicate marker label: {marker}")
                seen_markers.add(marker.casefold())
                if uniprot.casefold() in {"na", "n/a", "unknown", "null", "none"}:
                    errors.append(f"Channel map row {line}: unresolved UniProt mapping for {marker}")
            if indexes:
                unique = sorted(set(indexes))
                if len(unique) != len(indexes):
                    errors.append("Channel map contains duplicate channel indexes")
                if unique not in (list(range(0, len(unique))), list(range(1, len(unique) + 1))):
                    errors.append("Channel indexes must be contiguous starting at 0 or 1")
            channel_summary = {
                "checked": True,
                "rows": len(channel_rows),
                "unique_channel_indexes": len(set(indexes)),
            }

    if not check_files:
        warnings.append("File existence was not checked; this is metadata-only validation.")
    warnings.append("This validator does not read image/mask arrays or prove spatial alignment.")
    warnings.append("Checkpoint provenance, licence, training exposure, preprocessing equivalence, and endpoint definitions require separate checks.")
    return {
        "status": "PASS_METADATA_ONLY" if not errors else "BLOCKED",
        "errors": errors,
        "warnings": warnings,
        "counts": counts,
        "channel_map": channel_summary,
        "tensor_qc_performed": False,
        "checkpoint_verified": False,
        "inference_run": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--channel-map", type=Path)
    parser.add_argument("--check-files", action="store_true")
    parser.add_argument("--expected-roi-count", type=int)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = validate_manifest(args.manifest, args.channel_map, args.check_files, args.expected_roi_count)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS_METADATA_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
