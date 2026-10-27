#!/usr/bin/env python3
"""Validate the filename-derived HCC image-to-patient ROI crosswalk.

The ROI ordinal comes from the released image filename; outcomes remain patient-level.
Rows with unresolved status, duplicate image stems, duplicate patient/ROI-label keys,
or missing source references fail closed.
Required CSV columns: image_stem, patient_id, roi_label_from_filename, source_reference,
resolution_status. The source reference should identify the published patient row and image filename.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

REQUIRED = {
    "image_stem", "patient_id", "roi_label_from_filename",
    "source_reference", "resolution_status",
}


def validate(rows: list[dict[str, str]], expected_image_stems: set[str]) -> dict:
    errors: list[str] = []
    missing_cols = sorted(REQUIRED - set(rows[0].keys())) if rows else sorted(REQUIRED)
    if missing_cols:
        return {"gate": "BLOCKED", "errors": [f"Missing required columns: {missing_cols}"],
                "row_count": len(rows), "mapped_image_count": 0}
    seen_images: set[str] = set()
    seen_patient_roi_labels: set[tuple[str, str]] = set()
    resolved_images: set[str] = set()
    for i, row in enumerate(rows, start=2):
        image = row.get("image_stem", "").strip()
        patient = row.get("patient_id", "").strip()
        roi = row.get("roi_label_from_filename", "").strip()
        source = row.get("source_reference", "").strip()
        status = row.get("resolution_status", "").strip().lower()
        if not all((image, patient, roi, source, status)):
            errors.append(f"Row {i}: one or more required fields are blank.")
            continue
        if image in seen_images:
            errors.append(f"Row {i}: duplicate image_stem {image!r}.")
        seen_images.add(image)
        key = (patient, roi)
        if key in seen_patient_roi_labels:
            errors.append(f"Row {i}: duplicate patient/ROI-label key {key!r}.")
        seen_patient_roi_labels.add(key)
        if status != "resolved":
            errors.append(f"Row {i}: mapping for {image!r} is not resolved.")
        else:
            resolved_images.add(image)
    missing = sorted(expected_image_stems - seen_images)
    unexpected = sorted(seen_images - expected_image_stems)
    if missing:
        errors.append(f"Images missing from crosswalk: {missing}")
    if unexpected:
        errors.append(f"Crosswalk contains unknown image stems: {unexpected}")
    return {
        "gate": "PASS_FILENAME_DERIVED_PATIENT_ROI_CROSSWALK" if not errors else "BLOCKED",
        "errors": errors,
        "row_count": len(rows),
        "expected_image_count": len(expected_image_stems),
        "mapped_image_count": len(resolved_images),
        "missing_image_stems": missing,
        "unexpected_image_stems": unexpected,
        "critical_limit": "A pass checks completeness of filename-derived image-to-patient ROI labels. It does not establish an independent clinical record for every ROI; patient-level outcomes must be aggregated at patient level and patients must never be split across folds.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--crosswalk", type=Path, required=True, help="Source-backed CSV; do not guess mappings")
    ap.add_argument("--images-dir", type=Path, required=True, help="Directory containing image TIFFs")
    ap.add_argument("--out-json", type=Path, required=True)
    args = ap.parse_args()
    if not args.images_dir.is_dir():
        raise SystemExit(f"Images directory not found: {args.images_dir}")
    image_stems = {
        p.stem for p in args.images_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".tif", ".tiff"}
    }
    with args.crosswalk.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        # Preserve declared header even for empty CSVs.
        if reader.fieldnames and not rows:
            rows = [{name: "" for name in reader.fieldnames}]
            rows = []
            report = {"gate": "BLOCKED", "errors": ["Crosswalk has headers but no data rows."],
                      "row_count": 0, "mapped_image_count": 0}
        else:
            report = validate(rows, image_stems)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["gate"] == "PASS_FILENAME_DERIVED_PATIENT_ROI_CROSSWALK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
