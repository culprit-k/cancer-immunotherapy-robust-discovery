#!/usr/bin/env python3
"""Run outcome-blind spatial marker-state analysis over extracted HCC TIFF/mask folders.

This script uses only image stacks and cell-instance masks. It intentionally does
not load clinical outcomes or the stromal mask. All outputs must remain private.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd
import tifffile

from analysis.spatial_cell_features import (
    compute_spatial_marker_state_coupling,
    extract_cell_profiles,
)

IMAGE_EXTS = {".tif", ".tiff"}
MASK_SUFFIX_RE = {
    "cell": re.compile(r"(?i)(?:[_-](?:cellmask|cell_mask|cell-mask|cellmasks))$"),
    "stroma": re.compile(r"(?i)(?:[_-](?:stromamask|stroma_mask|stroma-mask|stromalmask|stromal_mask|stromal-mask|stromamasks))$"),
}


def canonical_stem(path: Path, kind: str) -> str:
    stem = path.stem
    if kind in MASK_SUFFIX_RE:
        stem = MASK_SUFFIX_RE[kind].sub("", stem)
    return stem


def files_by_stem(folder: Path, kind: str) -> dict[str, Path]:
    allowed = IMAGE_EXTS if kind == "image" else IMAGE_EXTS | {".png"}
    found: dict[str, Path] = {}
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        stem = canonical_stem(path, kind)
        if stem in found:
            raise SystemExit(f"duplicate canonical {kind} stem {stem!r}: {found[stem]} and {path}")
        found[stem] = path
    return found


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--images", required=True, type=Path, help="Extracted ICI_img_normalized directory")
    p.add_argument("--cell-masks", required=True, type=Path, help="Extracted ICI_cellmasks directory")
    p.add_argument("--reviewed-channel-map", required=True, type=Path,
                   help="Private CSV: plane_index0,marker,mapping_evidence,verification_status")
    p.add_argument("--output-dir", required=True, type=Path, help="Private local output directory")
    p.add_argument("--cytotoxic-markers", default="CD3,CD8a,GranzymeB")
    p.add_argument("--myeloid-associated-markers", default="CD68,CD163,CD204,Arginase1,PDL1")
    p.add_argument("--background-label", required=True, type=int,
                   help="Background value from the source-verified cell-mask codebook")
    p.add_argument("--confirm-mask-semantics", action="store_true",
                   help="Required acknowledgement that instance-mask and background semantics were verified")
    p.add_argument("--confirm-channel-map-review", action="store_true",
                   help="Required acknowledgement that plane mapping was checked against source evidence")
    p.add_argument("--k-neighbours", type=int, default=8)
    p.add_argument("--permutations", type=int, default=999)
    p.add_argument("--seed", type=int, default=20261027)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if not args.confirm_mask_semantics:
        raise SystemExit("BLOCKED: review mask codebook and overlays, then pass --confirm-mask-semantics")
    if not args.confirm_channel_map_review:
        raise SystemExit("BLOCKED: review plane-to-marker mapping, then pass --confirm-channel-map-review")
    for folder in (args.images, args.cell_masks):
        if not folder.is_dir():
            raise SystemExit(f"directory not found: {folder}")
    if not args.reviewed_channel_map.is_file():
        raise SystemExit(f"reviewed channel map not found: {args.reviewed_channel_map}")
    if args.permutations < 99:
        raise SystemExit("--permutations must be at least 99")

    markers_focal = [x.strip() for x in args.cytotoxic_markers.split(",") if x.strip()]
    markers_neighbour = [x.strip() for x in args.myeloid_associated_markers.split(",") if x.strip()]
    all_markers = sorted(set(markers_focal + markers_neighbour))
    if len(markers_focal) < 2 or len(markers_neighbour) < 2:
        raise SystemExit("specify at least two markers for each marker-state score")

    channel_map = pd.read_csv(args.reviewed_channel_map)
    images = files_by_stem(args.images, "image")
    masks = files_by_stem(args.cell_masks, "cell")
    shared = sorted(set(images) & set(masks))
    missing_mask = sorted(set(images) - set(masks))
    orphan_mask = sorted(set(masks) - set(images))
    if not shared:
        raise SystemExit("no matched image/cell-mask pairs found; inspect canonical filenames")

    outdir = args.output_dir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    profiles_dir = outdir / "cell_profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    failures: list[dict[str, str]] = []
    for i, stem in enumerate(shared, 1):
        try:
            image = tifffile.imread(images[stem])
            mask = tifffile.imread(masks[stem])
            if image.ndim != 3:
                raise ValueError(f"expected channel-first 3D stack (C,H,W), got shape {image.shape}")
            profiles = extract_cell_profiles(
                image, mask, channel_map, roi_id=stem, required_markers=all_markers,
                background_label=args.background_label, mask_semantics_verified=True,
            )
            score = compute_spatial_marker_state_coupling(
                profiles, cytotoxic_markers=markers_focal,
                myeloid_associated_markers=markers_neighbour,
                k_neighbours=args.k_neighbours, n_permutations=args.permutations,
                random_state=args.seed + i,
            )
            score["image_file"] = images[stem].name
            score["cell_mask_file"] = masks[stem].name
            results.append(score)
            # Private audit trail; raw cell profile CSVs may be large.
            profiles.to_csv(profiles_dir / f"{stem}_cell_profiles.csv", index=False)
        except Exception as exc:
            failures.append({
                "roi_stem": stem, "error_type": type(exc).__name__,
                "error": str(exc)[:1000],
            })

    result_file = outdir / "roi_spatial_marker_state_coupling.csv"
    if results:
        pd.DataFrame(results).to_csv(result_file, index=False)
    report = {
        "status": "PASS_OUTCOME_BLIND_FEATURE_EXTRACTION" if results and not failures and not missing_mask and not orphan_mask else "BLOCKED_OR_PARTIAL",
        "image_count": len(images), "cell_mask_count": len(masks),
        "matched_pair_count": len(shared), "successful_roi_count": len(results),
        "failed_roi_count": len(failures), "images_missing_masks": missing_mask,
        "orphan_masks": orphan_mask, "required_markers": all_markers,
        "cytotoxic_marker_set": markers_focal,
        "myeloid_associated_marker_set": markers_neighbour,
        "k_neighbours": args.k_neighbours, "permutations_per_roi": args.permutations,
        "random_seed_base": args.seed, "background_label": args.background_label,
        "outputs": [str(result_file), str(profiles_dir)],
        "claim_boundary": (
            "Outcome-blind ROI-level marker-state association only. No response labels, "
            "causal mechanism, validated cell typing, external validation or discovery claim."
        ),
        "failures": failures,
    }
    (outdir / "spatial_feature_extraction_manifest.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "failures"}, indent=2))
    if failures:
        print(f"Failed ROI examples: {failures[:5]}")
    return 0 if report["status"] == "PASS_OUTCOME_BLIND_FEATURE_EXTRACTION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
