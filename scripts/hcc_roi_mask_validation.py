#!/usr/bin/env python3
"""Outcome-blind structural QC for HCC ICI ROI images and masks.

This script checks filename pairing, shape agreement, and label-value summaries.
It does NOT infer biological meaning from mask values, map ROIs to patients,
or run VirTues. It writes metadata only; never copies source images to output.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import hashlib

import numpy as np
import pandas as pd
import tifffile


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def roi_key(path: Path) -> str:
    return path.stem


def index_tiffs(folder: Path) -> dict[str, Path]:
    if not folder.is_dir():
        raise FileNotFoundError(f"Required folder not found: {folder}")
    files = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {".tif", ".tiff"})
    out = {}
    for p in files:
        key = roi_key(p)
        if key in out:
            raise ValueError(f"Duplicate ROI key {key!r} in {folder}")
        out[key] = p
    return out


def summarize_mask(path: Path, max_labels_to_list: int = 20) -> dict:
    arr = tifffile.imread(path)
    if arr.ndim != 2:
        return {
            "shape": list(arr.shape), "dtype": str(arr.dtype), "ndim": int(arr.ndim),
            "unique_value_count": None, "zero_fraction": None,
            "min_value": None, "max_value": None,
            "first_nonzero_labels": [], "label_encoding": "UNVERIFIED_NON_2D_MASK",
            "sha256": sha256_file(path),
        }
    values, counts = np.unique(arr, return_counts=True)
    nonzero = [(int(v), int(c)) for v, c in zip(values, counts) if v != 0]
    return {
        "shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "ndim": 2,
        "unique_value_count": int(values.size),
        "zero_fraction": float(np.count_nonzero(arr == 0) / arr.size),
        "min_value": int(values[0]),
        "max_value": int(values[-1]),
        "nonzero_label_count": int(len(nonzero)),
        "first_nonzero_labels_by_value": nonzero[:max_labels_to_list],
        "largest_nonzero_label": int(values[-1]),
        "label_encoding": "UNVERIFIED_DO_NOT_INFER_CELL_COUNT",
        "sha256": sha256_file(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", required=True, type=Path, help="Folder containing normalized image TIFFs")
    parser.add_argument("--cell-masks", required=True, type=Path, help="Folder containing cell-mask TIFFs")
    parser.add_argument("--stromal-masks", required=True, type=Path, help="Folder containing stromal-mask TIFFs")
    parser.add_argument("--out", required=True, type=Path, help="Output directory for metadata-only reports")
    parser.add_argument("--clinical-roi-keys", type=Path, help="Optional CSV with a column named roi_key; does not establish mapping validity")
    args = parser.parse_args()

    images = index_tiffs(args.images)
    cells = index_tiffs(args.cell_masks)
    stromal = index_tiffs(args.stromal_masks)
    keys = sorted(set(images) | set(cells) | set(stromal))
    rows = []
    mask_rows = []
    for key in keys:
        ip, cp, sp = images.get(key), cells.get(key), stromal.get(key)
        row = {
            "roi_key": key,
            "image_found": ip is not None,
            "cell_mask_found": cp is not None,
            "stromal_mask_found": sp is not None,
            "image_shape": None,
            "cell_mask_shape": None,
            "stromal_mask_shape": None,
            "cell_mask_shape_matches_image": None,
            "stromal_mask_shape_matches_image": None,
            "pairing_status": "MISSING_FILE",
        }
        if ip:
            image = tifffile.imread(ip)
            row["image_shape"] = json.dumps(list(image.shape))
            row["image_dtype"] = str(image.dtype)
            row["image_ndim"] = int(image.ndim)
            row["image_sha256"] = sha256_file(ip)
            spatial_shape = tuple(image.shape[-2:]) if image.ndim == 3 else None
        else:
            spatial_shape = None
        for mask_type, mp in (("cell", cp), ("stromal", sp)):
            if mp:
                arr_shape = tuple(tifffile.imread(mp).shape)
                row[f"{mask_type}_mask_shape"] = json.dumps(list(arr_shape))
                row[f"{mask_type}_mask_shape_matches_image"] = bool(spatial_shape == arr_shape) if spatial_shape else False
                if mask_type == "cell":
                    mask_rows.append({"roi_key": key, "mask_type": mask_type, "path_name": mp.name, **summarize_mask(mp)})
                else:
                    mask_rows.append({"roi_key": key, "mask_type": mask_type, "path_name": mp.name, **summarize_mask(mp)})
        if ip and cp and sp:
            shape_ok = row["cell_mask_shape_matches_image"] and row["stromal_mask_shape_matches_image"]
            row["pairing_status"] = "PAIRED_SHAPES_MATCH" if shape_ok else "PAIRED_SHAPE_MISMATCH"
        rows.append(row)

    args.out.mkdir(parents=True, exist_ok=True)
    pairing_path = args.out / "roi_pairing_qc.csv"
    masks_path = args.out / "mask_label_summary.csv"
    pd.DataFrame(rows).to_csv(pairing_path, index=False)
    pd.DataFrame(mask_rows).to_csv(masks_path, index=False)

    report = {
        "roi_keys_union": len(keys),
        "images": len(images),
        "cell_masks": len(cells),
        "stromal_masks": len(stromal),
        "all_three_files_present": int(sum(r["image_found"] and r["cell_mask_found"] and r["stromal_mask_found"] for r in rows)),
        "all_three_shapes_match": int(sum(r["pairing_status"] == "PAIRED_SHAPES_MATCH" for r in rows)),
        "missing_or_mismatched_keys": [r["roi_key"] for r in rows if r["pairing_status"] != "PAIRED_SHAPES_MATCH"],
        "important_limit": "Filename/shape pairing does not prove clinical ROI mapping, mask semantics, channel mapping, or official VirTues compatibility.",
        "clinical_roi_keys_file_supplied": bool(args.clinical_roi_keys),
        "clinical_mapping_status": "NOT_VALIDATED_BY_THIS_SCRIPT",
    }
    (args.out / "qc_summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Saved metadata-only reports to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
