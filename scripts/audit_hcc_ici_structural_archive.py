#!/usr/bin/env python3
"""Outcome-blind aggregate structural audit of the public HCC ICI ZIP.

The script reads the archive in place, validates image/mask file pairing,
spatial shape alignment, stack channel counts, finite values, normalized range,
mask integer/2-D shape, and panel channel numbering. It writes aggregate-only
JSON and intentionally does not emit per-ROI filenames or patient rows.
It DOES NOT infer stromal-mask semantics, prove channel-plane biological
identity, validate VirTues preprocessing compatibility, or run a model.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import numpy as np
import pandas as pd
import tifffile

EXPECTED_MD5 = "d0b3242740b70c1355f67bc7bd176c6a"
IMAGE_DIR = "ICI_img_normalized"
CELL_DIR = "ICI_cellmasks"
STROMA_DIR = "ICI_stromamasks"
ROI_RE = re.compile(r"(?i)ICI[_-]?(\d+)[_-]ROI[_-]?(\d+)")


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def category(name: str) -> str | None:
    parts = {p.casefold() for p in PurePosixPath(name).parts}
    if IMAGE_DIR.casefold() in parts:
        return "image"
    if CELL_DIR.casefold() in parts:
        return "cell"
    if STROMA_DIR.casefold() in parts:
        return "stroma"
    return None


def canonical_stem(filename: str, kind: str) -> str:
    stem = PurePosixPath(filename).stem
    if kind == "cell":
        stem = re.sub(r"(?i)(?:[_-](?:cellmask|cell_mask|cell-mask|cellmasks))$", "", stem)
    elif kind == "stroma":
        stem = re.sub(r"(?i)(?:[_-](?:stromamask|stroma_mask|stroma-mask|stromalmask|stromal_mask|stromal-mask|stromamasks))$", "", stem)
    return stem


def read_tiff(zf: zipfile.ZipFile, name: str) -> np.ndarray:
    with zf.open(name, "r") as stream:
        return tifffile.imread(stream)


def summarize_panel(zf: zipfile.ZipFile, member: str) -> dict[str, Any]:
    raw = zf.read(member)
    bio = io.BytesIO(raw)
    if member.casefold().endswith((".xlsx", ".xls")):
        frame = pd.read_excel(bio, sheet_name=0)
    else:
        frame = pd.read_csv(bio)
    out: dict[str, Any] = {
        "member_present": True,
        "row_count": int(len(frame)),
        "columns": [str(c) for c in frame.columns],
        "channel_column_found": False,
        "channel_values_numeric": False,
        "channel_values_unique": False,
        "channels_are_1_to_45": False,
    }
    channel_col = next((c for c in frame.columns if str(c).strip().casefold() in {"channel", "channel_id", "channel_number"}), None)
    if channel_col is None:
        return out
    out["channel_column_found"] = True
    numeric = pd.to_numeric(frame[channel_col], errors="coerce")
    if numeric.notna().all() and np.all(np.equal(numeric.to_numpy(), np.floor(numeric.to_numpy()))):
        vals = [int(v) for v in numeric.tolist()]
        out["channel_values_numeric"] = True
        out["channel_values_unique"] = len(vals) == len(set(vals))
        out["channels_are_1_to_45"] = sorted(vals) == list(range(1, 46))
        out["channel_count"] = len(vals)
        out["duplicate_channel_count"] = len(vals) - len(set(vals))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--expected-md5", default=EXPECTED_MD5)
    args = ap.parse_args()

    archive = args.archive.resolve()
    if not archive.is_file():
        ap.error(f"Archive not found: {archive}")
    observed_md5 = md5_file(archive)
    report: dict[str, Any] = {
        "purpose": "aggregate outcome-blind structural QC; no HCC model inference",
        "archive_size_bytes": archive.stat().st_size,
        "expected_archive_md5": args.expected_md5,
        "observed_archive_md5": observed_md5,
        "archive_md5_match": observed_md5.lower() == args.expected_md5.lower(),
        "source_record": "https://doi.org/10.5281/zenodo.10794904",
        "counts": {},
        "panel": {},
        "image_tensor_qc": {},
        "cell_mask_qc": {},
        "stromal_mask_qc": {},
        "roi_count_discrepancy_check": {},
        "go_no_go": "BLOCKED",
        "limitations": [
            "This structural audit does not prove that TIFF plane order matches the panel semantically.",
            "Numeric stromal-mask labels are not assigned biological meaning by this script.",
            "The public image value range [0,1] is not evidence of compatibility with official VirTues preprocessing.",
            "The ICI_24 and ICI_39 image-level ROI identity discrepancies require authoritative crosswalk resolution.",
            "No model inference, patient outcome analysis, or biological claims are performed."
        ],
    }
    if observed_md5.lower() != args.expected_md5.lower():
        report["error"] = "Archive MD5 mismatch; no data inspection performed."
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({k: v for k, v in report.items() if k not in {"limitations"}}, indent=2))
        return 2

    with zipfile.ZipFile(archive, "r") as zf:
        members = [i.filename for i in zf.infolist() if not i.is_dir()]
        indexed: dict[str, dict[str, str]] = {"image": {}, "cell": {}, "stroma": {}}
        duplicates = {"image": 0, "cell": 0, "stroma": 0}
        directory_counts = Counter()
        panels = []
        for name in members:
            parts = PurePosixPath(name).parts
            if len(parts) > 1:
                directory_counts[parts[-2]] += 1
            kind = category(name)
            suffix = PurePosixPath(name).suffix.casefold()
            if kind and suffix in {".tif", ".tiff"}:
                key = canonical_stem(name, kind)
                if key in indexed[kind]:
                    duplicates[kind] += 1
                else:
                    indexed[kind][key] = name
            if PurePosixPath(name).name.casefold() in {"icicohort_panel.csv", "icicohort_panel.xlsx"}:
                panels.append(name)

        report["counts"] = {
            "archive_members": len(members),
            "image_tiffs": len(indexed["image"]),
            "cell_mask_tiffs": len(indexed["cell"]),
            "stromal_mask_tiffs": len(indexed["stroma"]),
            "duplicate_canonical_keys": duplicates,
            "top_level_component_file_counts": dict(sorted(directory_counts.items())),
        }

        image_keys = set(indexed["image"])
        cell_keys = set(indexed["cell"])
        stroma_keys = set(indexed["stroma"])
        complete = image_keys & cell_keys & stroma_keys
        report["counts"].update({
            "image_cell_stroma_complete_triplets": len(complete),
            "image_missing_cell_mask_count": len(image_keys - cell_keys),
            "image_missing_stromal_mask_count": len(image_keys - stroma_keys),
            "orphan_cell_mask_count": len(cell_keys - image_keys),
            "orphan_stromal_mask_count": len(stroma_keys - image_keys),
        })

        if panels:
            panel = summarize_panel(zf, sorted(panels)[0])
            panel["member_basename"] = PurePosixPath(sorted(panels)[0]).name
            report["panel"] = panel
        else:
            report["panel"] = {"member_present": False}

        img_ndim = Counter()
        img_dtype = Counter()
        image_channel_counts = Counter()
        image_range_ok = 0
        image_finite_ok = 0
        image_read_errors = 0
        spatial_shapes: Counter[tuple[int, int]] = Counter()
        cell_shape_matches = 0
        stroma_shape_matches = 0
        mask_read_errors = 0
        cell_ndim_2 = 0
        stroma_ndim_2 = 0
        cell_integer = 0
        stroma_integer = 0
        cell_label_counts = Counter()
        stroma_label_counts = Counter()
        cell_zero_fractions = []
        stroma_zero_fractions = []
        mask_alignment_checked = 0
        roi_by_patient = Counter()
        roi_parse_failures = 0

        for key in sorted(image_keys):
            match = ROI_RE.search(key)
            if match:
                roi_by_patient[int(match.group(1))] += 1
            else:
                roi_parse_failures += 1
            try:
                image = read_tiff(zf, indexed["image"][key])
                img_ndim[image.ndim] += 1
                img_dtype[str(image.dtype)] += 1
                if image.ndim == 3:
                    image_channel_counts[int(image.shape[0])] += 1
                    spatial_shapes[tuple(int(v) for v in image.shape[-2:])] += 1
                finite_ok = bool(image.size and np.isfinite(image).all())
                if finite_ok:
                    image_finite_ok += 1
                    if float(np.min(image)) >= 0 and float(np.max(image)) <= 1:
                        image_range_ok += 1
                image_spatial = tuple(image.shape[-2:]) if image.ndim == 3 else None
            except Exception:
                image_read_errors += 1
                image_spatial = None
                if "image" in locals():
                    del image
                continue

            for kind in ("cell", "stroma"):
                try:
                    mask = read_tiff(zf, indexed[kind][key])
                    if mask.ndim == 2:
                        if kind == "cell":
                            cell_ndim_2 += 1
                        else:
                            stroma_ndim_2 += 1
                        if image_spatial == tuple(mask.shape):
                            if kind == "cell":
                                cell_shape_matches += 1
                            else:
                                stroma_shape_matches += 1
                            mask_alignment_checked += 1
                        vals, counts = np.unique(mask, return_counts=True)
                        labels = cell_label_counts if kind == "cell" else stroma_label_counts
                        labels.update(int(v) for v in vals)
                        zero_fraction = float(np.mean(mask == 0)) if mask.size else 0.0
                        if kind == "cell":
                            cell_zero_fractions.append(zero_fraction)
                            if np.issubdtype(mask.dtype, np.integer):
                                cell_integer += 1
                        else:
                            stroma_zero_fractions.append(zero_fraction)
                            if np.issubdtype(mask.dtype, np.integer):
                                stroma_integer += 1
                    else:
                        mask_read_errors += 1
                    del mask
                except Exception:
                    mask_read_errors += 1
            del image

        report["image_tensor_qc"] = {
            "ndim_counts": dict(img_ndim),
            "dtype_counts": dict(img_dtype),
            "observed_channel_count_distribution": dict(image_channel_counts),
            "observed_spatial_shape_count": len(spatial_shapes),
            "all_images_finite_count": image_finite_ok,
            "images_with_all_values_in_0_1_count": image_range_ok,
            "image_read_errors": image_read_errors,
        }
        report["cell_mask_qc"] = {
            "2d_mask_count": cell_ndim_2,
            "integer_dtype_count": cell_integer,
            "unique_numeric_labels_union": sorted(cell_label_counts),
            "median_zero_fraction": float(np.median(cell_zero_fractions)) if cell_zero_fractions else None,
        }
        report["stromal_mask_qc"] = {
            "2d_mask_count": stroma_ndim_2,
            "integer_dtype_count": stroma_integer,
            "unique_numeric_labels_union": sorted(stroma_label_counts),
            "median_zero_fraction": float(np.median(stroma_zero_fractions)) if stroma_zero_fractions else None,
        }
        report["mask_shape_alignment"] = {
            "cell_mask_shape_matches_image_count": cell_shape_matches,
            "stromal_mask_shape_matches_image_count": stroma_shape_matches,
            "mask_alignment_pair_checks": mask_alignment_checked,
            "mask_read_errors_or_non_2d": mask_read_errors,
        }
        report["roi_count_discrepancy_check"] = {
            "roi_token_parse_failures": roi_parse_failures,
            "ICI_24_observed_image_roi_count": roi_by_patient.get(24, 0),
            "ICI_24_published_expected_roi_count": 2,
            "ICI_24_count_matches": roi_by_patient.get(24, 0) == 2,
            "ICI_39_observed_image_roi_count": roi_by_patient.get(39, 0),
            "ICI_39_published_expected_roi_count": 1,
            "ICI_39_count_matches": roi_by_patient.get(39, 0) == 1,
            "note": "Published Table 3 provides patient-level ROI counts but does not identify which archive filenames are extra; mismatches are not automatically corrected.",
        }

    counts = report["counts"]
    panel = report["panel"]
    report["go_no_go"] = "PASS_STRUCTURAL_ONLY" if (
        report["archive_md5_match"]
        and counts.get("image_tiffs") == 86
        and counts.get("cell_mask_tiffs") == 86
        and counts.get("stromal_mask_tiffs") == 86
        and counts.get("image_cell_stroma_complete_triplets") == 86
        and not any(duplicates.values())
        and counts.get("image_missing_cell_mask_count") == 0
        and counts.get("image_missing_stromal_mask_count") == 0
        and report["image_tensor_qc"].get("image_read_errors") == 0
        and report["image_tensor_qc"].get("all_images_finite_count") == 86
        and report["image_tensor_qc"].get("images_with_all_values_in_0_1_count") == 86
        and report["image_tensor_qc"].get("observed_channel_count_distribution") == {45: 86}
        and report["mask_shape_alignment"].get("cell_mask_shape_matches_image_count") == 86
        and report["mask_shape_alignment"].get("stromal_mask_shape_matches_image_count") == 86
        and report["mask_shape_alignment"].get("mask_read_errors_or_non_2d") == 0
        and report["cell_mask_qc"].get("integer_dtype_count") == 86
        and report["stromal_mask_qc"].get("integer_dtype_count") == 86
        and panel.get("row_count") == 45
        and panel.get("channels_are_1_to_45") is True
    ) else "REVIEW_REQUIRED"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["go_no_go"] in {"PASS_STRUCTURAL_ONLY", "REVIEW_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
