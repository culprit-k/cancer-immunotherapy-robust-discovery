#!/usr/bin/env python3
"""Generate private, outcome-blind image/mask QC previews before feature extraction.

This tool deliberately does not infer channel order, cell identities, or mask meaning.
It produces per-plane robust-scaled previews, a label-map visualization, and JSON
metadata for a human to compare with source documentation. Keep outputs private.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw


def robust_u8(a: np.ndarray) -> np.ndarray:
    x = np.asarray(a, dtype=np.float32)
    finite = np.isfinite(x)
    if not finite.any():
        return np.zeros(x.shape, dtype=np.uint8)
    lo, hi = np.quantile(x[finite], [0.01, 0.99])
    if hi <= lo:
        return np.zeros(x.shape, dtype=np.uint8)
    y = np.clip((x - lo) / (hi - lo), 0, 1)
    y[~finite] = 0
    return (255 * y).astype(np.uint8)


def save_plane_montage(image: np.ndarray, path: Path, max_cols: int = 5) -> list[dict[str, object]]:
    if image.ndim != 3:
        raise ValueError(f"expected (C,H,W) stack; observed {image.shape}")
    c, h, w = image.shape
    tile_w, tile_h, label_h = 220, 220, 28
    cols = min(max_cols, c)
    rows = (c + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    metadata = []
    for i in range(c):
        plane = image[i]
        preview = Image.fromarray(robust_u8(plane)).resize((tile_w, tile_h))
        x, y = (i % cols) * tile_w, (i // cols) * (tile_h + label_h)
        canvas.paste(preview.convert("RGB"), (x, y))
        draw.text((x + 5, y + tile_h + 4), f"plane {i} (candidate panel channel {i+1})", fill="black")
        finite = np.isfinite(plane)
        metadata.append({
            "plane_index0": i, "candidate_panel_channel_1based": i + 1,
            "shape": list(plane.shape), "dtype": str(plane.dtype),
            "finite_fraction": float(finite.mean()),
            "min": float(np.min(plane[finite])) if finite.any() else None,
            "p01": float(np.quantile(plane[finite], 0.01)) if finite.any() else None,
            "median": float(np.median(plane[finite])) if finite.any() else None,
            "p99": float(np.quantile(plane[finite], 0.99)) if finite.any() else None,
            "max": float(np.max(plane[finite])) if finite.any() else None,
        })
    canvas.save(path)
    return metadata


def save_label_preview(mask: np.ndarray, path: Path) -> dict[str, object]:
    if mask.ndim != 2:
        raise ValueError(f"expected 2D mask; observed shape {mask.shape}")
    labels, counts = np.unique(mask, return_counts=True)
    # Deterministic pseudo-colors are for visual inspection only, not cell typing.
    rng = np.random.default_rng(17)
    colors = rng.integers(35, 245, size=(len(labels), 3), dtype=np.uint8)
    colors[labels == 0] = 0
    index = np.searchsorted(labels, mask)
    rgb = colors[index]
    Image.fromarray(rgb).resize((mask.shape[1], mask.shape[0])).save(path)
    total = int(mask.size)
    return {
        "shape": list(mask.shape), "dtype": str(mask.dtype),
        "unique_label_count_including_zero": int(len(labels)),
        "zero_fraction": float(np.mean(mask == 0)),
        "negative_pixel_count": int(np.sum(mask < 0)),
        "smallest_labels": [
            {"label": int(v), "pixel_count": int(n), "fraction": float(n / total)}
            for v, n in sorted(zip(labels, counts), key=lambda z: z[1])[:20]
        ],
        "largest_labels": [
            {"label": int(v), "pixel_count": int(n), "fraction": float(n / total)}
            for v, n in sorted(zip(labels, counts), key=lambda z: z[1], reverse=True)[:20]
        ],
        "warning": "Label IDs and colors do not identify biological cell types; confirm semantics from source documentation.",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--image", required=True, type=Path)
    p.add_argument("--cell-mask", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args()
    if not args.image.is_file() or not args.cell_mask.is_file():
        raise SystemExit("image or cell-mask path does not exist")
    out = args.output_dir.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    image = tifffile.imread(args.image)
    mask = tifffile.imread(args.cell_mask)
    if image.ndim != 3:
        raise SystemExit(f"image is not a 3D stack: shape={image.shape}; inspect TIFF axes before proceeding")
    if mask.ndim != 2:
        raise SystemExit(f"cell mask is not 2D: shape={mask.shape}; inspect TIFF axes before proceeding")
    if image.shape[1:] != mask.shape:
        raise SystemExit(f"spatial dimensions differ: image={image.shape}, mask={mask.shape}")
    plane_meta = save_plane_montage(image, out / "plane_montage.png")
    mask_meta = save_label_preview(mask, out / "cell_mask_labels.png")
    manifest = {
        "image_path": str(args.image.resolve()), "cell_mask_path": str(args.cell_mask.resolve()),
        "image_shape_assumed_channel_first": list(image.shape),
        "image_dtype": str(image.dtype), "image_finite_fraction": float(np.isfinite(image).mean()),
        "cell_mask": mask_meta, "planes": plane_meta,
        "status": "VISUAL_QC_ONLY_NOT_VERIFIED",
        "must_not_infer": [
            "plane-to-marker mapping from panel row order alone",
            "cell-type identity from integer mask IDs",
            "background semantics from zero fraction alone",
            "preprocessing equivalence from displayed intensity ranges",
        ],
    }
    (out / "visual_qc_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": manifest["status"], "image_shape": list(image.shape),
        "mask_shape": list(mask.shape), "unique_mask_labels": mask_meta["unique_label_count_including_zero"],
        "zero_fraction": mask_meta["zero_fraction"],
        "outputs": ["plane_montage.png", "cell_mask_labels.png", "visual_qc_manifest.json"],
        "note": "These previews are QC aids only; do not mark channel mapping or mask semantics verified from them alone."
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
