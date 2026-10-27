#!/usr/bin/env python
"""Run a patient-level exploratory association screen from a private ROI feature table."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from analysis.patient_level_discovery import aggregate_rois_to_patients, screen_binary_features


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, help="Private ROI-level feature CSV")
    p.add_argument("--output-dir", required=True, help="Private output directory")
    p.add_argument("--patient-col", required=True)
    p.add_argument("--outcome-col", required=True)
    p.add_argument("--features", required=True, help="Comma-separated numeric feature columns")
    p.add_argument("--positive", required=True, help="Positive class label for binary contrast")
    p.add_argument("--negative", required=True, help="Negative class label for binary contrast")
    p.add_argument("--aggregation", choices=("median", "mean"), default="median")
    p.add_argument("--permutations", type=int, default=20000)
    p.add_argument("--bootstrap", type=int, default=5000)
    p.add_argument("--seed", type=int, default=20261027)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    feature_cols = [v.strip() for v in args.features.split(",") if v.strip()]
    if not feature_cols or len(feature_cols) != len(set(feature_cols)):
        raise SystemExit("feature list must be non-empty and contain no duplicates")
    source = Path(args.input).expanduser().resolve()
    out_dir = Path(args.output_dir).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"input file not found: {source}")
    out_dir.mkdir(parents=True, exist_ok=True)
    roi = pd.read_csv(source)
    if roi.empty:
        raise SystemExit("input feature table is empty")

    patients = aggregate_rois_to_patients(
        roi, patient_col=args.patient_col, outcome_col=args.outcome_col,
        feature_cols=feature_cols, aggregation=args.aggregation,
    )
    binary = patients[patients[args.outcome_col].isin([args.positive, args.negative])].copy()
    other_classes = sorted(set(patients[args.outcome_col].astype(str)) -
                           {args.positive, args.negative})
    counts = binary[args.outcome_col].value_counts().to_dict()
    if min(counts.get(args.positive, 0), counts.get(args.negative, 0)) < 3:
        raise SystemExit(f"not enough patients for exploratory contrast: {counts}; minimum 3/group")

    associations = screen_binary_features(
        binary, patient_col=args.patient_col, outcome_col=args.outcome_col,
        feature_cols=feature_cols, positive_label=args.positive, negative_label=args.negative,
        n_permutations=args.permutations, n_bootstrap=args.bootstrap, random_state=args.seed,
    )
    patients.to_csv(out_dir / "patient_level_features.csv", index=False)
    associations.to_csv(out_dir / "exploratory_associations.csv", index=False)
    manifest = {
        "input_file": str(source), "n_roi_rows": int(len(roi)),
        "n_patients_after_aggregation": int(len(patients)),
        "n_patients_in_binary_contrast": int(len(binary)),
        "group_counts": {str(k): int(v) for k, v in counts.items()},
        "outcome_classes_excluded_from_binary_contrast": other_classes,
        "patient_aggregation": args.aggregation, "n_features_tested": len(feature_cols),
        "n_permutations": args.permutations, "n_bootstrap": args.bootstrap,
        "random_seed": args.seed,
        "claim_boundary": "Exploratory association only; no causality, clinical utility, independent validation, novelty, or patentability is established.",
    }
    (out_dir / "analysis_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": "complete", "output_dir": str(out_dir),
        "n_patients": len(patients), "group_counts": manifest["group_counts"],
        "excluded_outcome_classes": other_classes,
        "outputs": ["patient_level_features.csv", "exploratory_associations.csv", "analysis_manifest.json"],
        "warning": manifest["claim_boundary"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
