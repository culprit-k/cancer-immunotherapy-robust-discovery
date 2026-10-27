#!/usr/bin/env python3
"""Audit the combined HCC ROI/QC and repeated patient-level clinical manifest.

This gate checks data linkage and structural QC. It reports ROI-count conflicts
from Supplementary Table 3 as disclosed warnings rather than silently rewriting
the source table. It never treats ROI rows as independent clinical observations.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REQUIRED = {
    "image_stem", "patient_id", "roi_label_from_filename", "source_reference",
    "resolution_status", "read_status", "image_shape", "image_finite_fraction",
    "image_min", "image_max", "channels_45_first", "has_cell_mask",
    "has_stromal_mask", "cell_spatial_match", "stroma_spatial_match",
    "table_roi_count", "best_response", "response_binary", "PFS_months",
    "OS_months", "censored", "clinical_outcome_level",
}
PATIENT_LEVEL_FIELDS = (
    "table_roi_count", "best_response", "response_binary", "PFS_months",
    "OS_months", "censored", "etiology", "immunotype",
)


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def validate_manifest(
    rows: list[dict[str, str]],
    expected_patients: int = 42,
    expected_images: int = 86,
) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if not rows:
        return {
            "gate": "BLOCKED", "errors": ["Manifest has no data rows."],
            "warnings": [], "image_rows": 0, "patient_count": 0,
        }
    missing = sorted(REQUIRED - set(rows[0].keys()))
    if missing:
        return {
            "gate": "BLOCKED", "errors": [f"Missing required columns: {missing}"],
            "warnings": [], "image_rows": len(rows), "patient_count": 0,
        }

    stems: set[str] = set()
    patients: dict[str, list[dict[str, str]]] = defaultdict(list)
    for line, row in enumerate(rows, start=2):
        stem = row["image_stem"].strip()
        patient = row["patient_id"].strip()
        roi_label = row["roi_label_from_filename"].strip()
        match = re.fullmatch(r"(.+)_ROI(\d+)", stem)
        if not stem or stem in stems:
            errors.append(f"Row {line}: blank or duplicate image_stem {stem!r}.")
        stems.add(stem)
        if not match:
            errors.append(f"Row {line}: image_stem does not end in _ROI<number>: {stem!r}.")
        else:
            if match.group(1) != patient:
                errors.append(f"Row {line}: filename prefix {match.group(1)!r} disagrees with patient_id {patient!r}.")
            if roi_label != f"ROI{match.group(2)}":
                errors.append(f"Row {line}: roi_label_from_filename disagrees with image_stem {stem!r}.")
        if row["resolution_status"].strip().lower() != "resolved":
            errors.append(f"Row {line}: patient/ROI linkage is not marked resolved.")
        if not row["source_reference"].strip():
            errors.append(f"Row {line}: missing source_reference.")
        if row["read_status"].strip().upper() != "OK":
            errors.append(f"Row {line}: image structural read_status is not OK.")
        shape_nums = re.findall(r"\d+", row["image_shape"])
        if len(shape_nums) != 3 or int(shape_nums[0]) != 45:
            errors.append(f"Row {line}: expected channel-first shape (45,H,W), got {row['image_shape']!r}.")
        if not truthy(row["channels_45_first"]):
            errors.append(f"Row {line}: channel-first 45-plane check failed.")
        for col in ("has_cell_mask", "has_stromal_mask", "cell_spatial_match", "stroma_spatial_match"):
            if not truthy(row[col]):
                errors.append(f"Row {line}: {col} is not true.")
        try:
            finite = float(row["image_finite_fraction"])
            lo, hi = float(row["image_min"]), float(row["image_max"])
            if finite != 1.0:
                errors.append(f"Row {line}: image has non-finite pixels.")
            if lo < 0 or hi > 1 or lo > hi:
                errors.append(f"Row {line}: expected normalised image range [0,1], got [{lo},{hi}].")
        except (TypeError, ValueError):
            errors.append(f"Row {line}: invalid image finite fraction or intensity range.")
        if "PATIENT_LEVEL" not in row["clinical_outcome_level"]:
            errors.append(f"Row {line}: patient-level outcome warning is missing.")
        try:
            binary_response = int(row["response_binary"])
            expected_binary = int(row["best_response"].strip() == "PR")
            if binary_response != expected_binary:
                errors.append(f"Row {line}: response_binary disagrees with best_response.")
        except (ValueError, TypeError):
            errors.append(f"Row {line}: invalid response_binary value.")
        patients[patient].append(row)

    if len(rows) != expected_images:
        errors.append(f"Expected {expected_images} image rows, found {len(rows)}.")
    if len(patients) != expected_patients:
        errors.append(f"Expected {expected_patients} patients, found {len(patients)}.")

    for patient, patient_rows in sorted(patients.items()):
        for field in PATIENT_LEVEL_FIELDS:
            vals = {r.get(field, "").strip() for r in patient_rows}
            if len(vals) > 1:
                errors.append(f"Patient {patient}: patient-level field {field!r} differs across ROI rows.")
        try:
            table_count = int(float(patient_rows[0]["table_roi_count"]))
        except (ValueError, TypeError, KeyError):
            errors.append(f"Patient {patient}: invalid or missing table_roi_count.")
            continue
        actual = len(patient_rows)
        if actual != table_count:
            warnings.append({
                "patient_id": patient,
                "table_roi_count": table_count,
                "image_file_count": actual,
                "difference_image_minus_table": actual - table_count,
            })

    response_counts = {}
    for patient_rows in patients.values():
        response = patient_rows[0].get("best_response", "").strip()
        response_counts[response] = response_counts.get(response, 0) + 1

    gate = "BLOCKED" if errors else (
        "PASS_WITH_DISCLOSED_ROI_COUNT_MISMATCHES" if warnings else "PASS"
    )
    return {
        "gate": gate,
        "errors": errors,
        "warnings": warnings,
        "image_rows": len(rows),
        "patient_count": len(patients),
        "response_counts_patient_level": dict(sorted(response_counts.items())),
        "critical_limit": "A pass verifies internal linkage and structural metadata only. It does not certify marker-to-plane order, mask label semantics, VirTues preprocessing compatibility, or clinical predictive validity.",
        "analysis_rule": "Outcomes repeat across ROI rows by patient; aggregate features to one patient record and keep each patient wholly within one evaluation fold.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--expected-patients", type=int, default=42)
    ap.add_argument("--expected-images", type=int, default=86)
    args = ap.parse_args()
    with args.manifest.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    report = validate_manifest(rows, args.expected_patients, args.expected_images)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["gate"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
