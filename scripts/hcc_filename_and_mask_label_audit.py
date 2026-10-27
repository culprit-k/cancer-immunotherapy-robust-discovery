#!/usr/bin/env python3
"""Private, fail-closed HCC ICI filename and mask-label audit.

This script inventories filenames and reports mask encodings locally. It does not
infer ROI matches, assert mask semantics, modify images, or run VirTues. Keep
all generated CSV/JSON outputs in the private runtime; do not commit them.
"""
from __future__ import annotations
import argparse, csv, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROI_RE = re.compile(r"(?i)(ICI[_-]?\d{1,3})")
IMAGE_EXTS = {".tif", ".tiff"}
MASK_EXTS = {".tif", ".tiff", ".png", ".npy"}

def roi_tokens(name: str) -> list[str]:
    return [m.group(1).upper().replace("-", "_") for m in ROI_RE.finditer(name)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Root directory of extracted HCC ICI archive")
    ap.add_argument("--outdir", required=True, help="Private output directory; do not upload outputs")
    ap.add_argument("--mask-samples", type=int, default=12, help="Maximum masks to inspect for unique values")
    args = ap.parse_args()
    root, out = Path(args.root).resolve(), Path(args.outdir).resolve()
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")
    out.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in root.rglob("*") if p.is_file())
    rows, by_roi = [], defaultdict(list)
    for p in files:
        tokens = roi_tokens(p.name)
        row = {
            "relative_path": p.relative_to(root).as_posix(),
            "parent_dir": p.parent.relative_to(root).as_posix(),
            "filename": p.name,
            "suffix": p.suffix.lower(),
            "bytes": p.stat().st_size,
            "roi_tokens": ";".join(tokens),
        }
        rows.append(row)
        for token in set(tokens):
            by_roi[token].append(row)

    inventory = out / "private_filename_inventory.csv"
    with inventory.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else
                           ["relative_path","parent_dir","filename","suffix","bytes","roi_tokens"])
        w.writeheader(); w.writerows(rows)

    roi_summary = []
    for roi, entries in sorted(by_roi.items()):
        roi_summary.append({
            "roi_token": roi,
            "file_count": len(entries),
            "image_tiffs": sum(e["suffix"] in IMAGE_EXTS for e in entries),
            "mask_or_array_files": sum(e["suffix"] in MASK_EXTS for e in entries),
            "relative_paths": ";".join(e["relative_path"] for e in entries),
            "status": "REVIEW_REQUIRED_NOT_AUTOMATICALLY_PAIRED",
        })
    roi_csv = out / "private_roi_filename_summary.csv"
    with roi_csv.open("w", newline="", encoding="utf-8") as f:
        fields = ["roi_token","file_count","image_tiffs","mask_or_array_files","relative_paths","status"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(roi_summary)

    # Find likely mask folders by directory names; inspect a bounded sample only.
    mask_candidates = [p for p in files if p.suffix.lower() in MASK_EXTS and
                       any(k in str(p.parent).lower() for k in ("mask", "stroma", "cell"))]
    mask_report = []
    try:
        import numpy as np
        import tifffile
        from PIL import Image
        for p in mask_candidates[:max(0, args.mask_samples)]:
            try:
                if p.suffix.lower() in {".tif", ".tiff"}:
                    arr = tifffile.imread(p)
                elif p.suffix.lower() == ".npy":
                    arr = np.load(p, mmap_mode="r", allow_pickle=False)
                else:
                    arr = np.asarray(Image.open(p))
                vals, counts = np.unique(np.asarray(arr), return_counts=True)
                # Keep report compact; labels are not assigned biological meaning here.
                pairs = sorted(zip(vals.tolist(), counts.tolist()), key=lambda x: x[0])
                mask_report.append({
                    "relative_path": p.relative_to(root).as_posix(),
                    "shape": list(arr.shape),
                    "dtype": str(arr.dtype),
                    "unique_value_count": len(pairs),
                    "unique_values_and_counts_first_100": pairs[:100],
                    "interpretation": "UNVERIFIED_LABEL_ENCODING",
                })
            except Exception as e:
                mask_report.append({"relative_path": p.relative_to(root).as_posix(),
                                    "read_error": type(e).__name__ + ": " + str(e)[:250]})
    except ImportError as e:
        mask_report = [{"warning": "Install numpy, tifffile, and pillow to inspect mask values.",
                        "detail": str(e)}]

    summary = {
        "root_file_count": len(files),
        "roi_tokens_found": len(by_roi),
        "files_with_roi_tokens": sum(bool(r["roi_tokens"]) for r in rows),
        "likely_mask_files_found": len(mask_candidates),
        "mask_samples_inspected": len(mask_report),
        "important_limitations": [
            "Filename token matching is heuristic and is not an authoritative ROI crosswalk.",
            "No image-mask pixelwise alignment or biological mask semantics are established.",
            "No clinical table is read; do not use this output alone to resolve ICI_24 or ICI_39.",
            "No preprocessing, checkpoint loading, model inference, or outcome analysis is performed."
        ],
        "mask_samples": mask_report,
    }
    (out / "private_mask_label_diagnostics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k:v for k,v in summary.items() if k != "mask_samples"}, indent=2))
    print("Private outputs:")
    print(" -", inventory)
    print(" -", roi_csv)
    print(" -", out / "private_mask_label_diagnostics.json")
    print("Do not upload these files; they may contain patient-level filenames or paths.")

if __name__ == "__main__":
    main()
