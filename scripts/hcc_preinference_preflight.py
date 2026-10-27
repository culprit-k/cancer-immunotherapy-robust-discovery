#!/usr/bin/env python3
"""Conservative pre-inference QC for HCC image/mask filename inventories.

This script checks inventory completeness and optional image headers. It does not
run VirTues, infer missing preprocessing parameters, or read patient outcomes.
Install optional image dependencies with: pip install tifffile numpy
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

IMAGE_SUFFIXES = {".tif", ".tiff"}
MASK_SUFFIXES = {".tif", ".tiff", ".png", ".npy"}


def stems(folder: Path, suffixes: set[str]) -> set[str]:
    if not folder.is_dir():
        raise FileNotFoundError(f"Not a directory: {folder}")
    return {p.stem for p in folder.iterdir() if p.is_file() and p.suffix.lower() in suffixes}


def inventory(images: Path, cell_masks: Path, stromal_masks: Path) -> dict[str, Any]:
    image_names = stems(images, IMAGE_SUFFIXES)
    cell_names = stems(cell_masks, MASK_SUFFIXES)
    stromal_names = stems(stromal_masks, MASK_SUFFIXES)
    all_names = sorted(image_names | cell_names | stromal_names)
    rows = []
    for name in all_names:
        rows.append({
            "stem": name,
            "has_image": name in image_names,
            "has_cell_mask": name in cell_names,
            "has_stromal_mask": name in stromal_names,
            "complete_triplet": name in image_names and name in cell_names and name in stromal_names,
        })
    return {
        "image_count": len(image_names),
        "cell_mask_count": len(cell_names),
        "stromal_mask_count": len(stromal_names),
        "union_stem_count": len(all_names),
        "complete_triplet_count": sum(row["complete_triplet"] for row in rows),
        "missing_image": sorted((cell_names | stromal_names) - image_names),
        "missing_cell_mask": sorted((image_names | stromal_names) - cell_names),
        "missing_stromal_mask": sorted((image_names | cell_names) - stromal_names),
        "rows": rows,
    }


def inspect_tiffs(images: Path, names: list[str]) -> list[dict[str, Any]]:
    try:
        import numpy as np
        import tifffile
    except ImportError as exc:
        raise RuntimeError("Header inspection requires numpy and tifffile") from exc
    results = []
    for name in names:
        path = next((p for p in images.iterdir() if p.stem == name and p.suffix.lower() in IMAGE_SUFFIXES), None)
        if path is None:
            continue
        try:
            arr = tifffile.imread(path)
            finite = np.isfinite(arr)
            results.append({
                "stem": name, "read_ok": True, "shape": list(arr.shape),
                "dtype": str(arr.dtype), "finite_fraction": float(finite.mean()) if arr.size else 0.0,
                "min": float(np.nanmin(arr)) if arr.size else None,
                "max": float(np.nanmax(arr)) if arr.size else None,
                "within_0_1": bool(arr.size and finite.all() and arr.min() >= 0 and arr.max() <= 1),
            })
        except Exception as exc:  # report and continue across inventory
            results.append({"stem": name, "read_ok": False, "error": f"{type(exc).__name__}: {exc}"})
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--images", type=Path, required=True)
    ap.add_argument("--cell-masks", type=Path, required=True)
    ap.add_argument("--stromal-masks", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--inspect-tiffs", action="store_true", help="Read every TIFF header/pixel array; may require substantial RAM.")
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    report = inventory(args.images, args.cell_masks, args.stromal_masks)
    with (args.outdir / "hcc_preflight_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(report["rows"][0]) if report["rows"] else ["stem", "has_image", "has_cell_mask", "has_stromal_mask", "complete_triplet"])
        writer.writeheader()
        writer.writerows(report["rows"])
    if args.inspect_tiffs:
        details = inspect_tiffs(args.images, sorted({r["stem"] for r in report["rows"] if r["has_image"]}))
        report["tiff_inspection"] = details
        report["tiff_read_failures"] = sum(not x.get("read_ok", False) for x in details)
        report["all_tiffs_finite"] = all(x.get("read_ok") and x.get("finite_fraction") == 1.0 for x in details)
    report["inventory_pass"] = report["complete_triplet_count"] == report["union_stem_count"] and not any(
        report[k] for k in ("missing_image", "missing_cell_mask", "missing_stromal_mask")
    )
    report["important_limit"] = "Passing filename QC does not certify channel mapping, mask semantics, checkpoint eligibility, or VirTues preprocessing compatibility."
    (args.outdir / "hcc_preflight_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in {"rows", "tiff_inspection"}}, indent=2))
    return 0 if report["inventory_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
