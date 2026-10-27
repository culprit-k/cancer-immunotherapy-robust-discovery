#!/usr/bin/env python3
"""Run local, non-destructive HCC panel/checkpoint/mask diagnostics in Colab.

This runner does not download data or model weights, modify source data, run model
inference, infer mask semantics, or claim training-cohort eligibility.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import numpy as np

def find_files(roots: list[Path], patterns: tuple[str, ...]) -> list[Path]:
    found = set()
    for root in roots:
        if root.exists():
            for pattern in patterns:
                found.update(p for p in root.rglob(pattern) if p.is_file())
    return sorted(found)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", action="append", type=Path, default=[])
    ap.add_argument("--panel", type=Path)
    ap.add_argument("--checkpoint", type=Path)
    ap.add_argument("--mask", type=Path, help="Optional single stromal mask .tif/.tiff")
    ap.add_argument("--out-dir", type=Path, default=Path("/content/hcc_virtues_audit/next_gate"))
    args = ap.parse_args()
    roots = args.root or [Path("/content/hcc_virtues_audit"), Path("/content/hcc_virtues_private")]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = {"non_destructive": True, "gates": {}, "warnings": [
        "Mask label values are descriptive only; this script does not map numeric IDs to biological classes.",
        "Panel completeness does not prove TIFF plane-to-marker identity.",
        "Checkpoint hash match does not prove training-data exposure or preprocessing compatibility."
    ]}
    panels = [args.panel] if args.panel else find_files(roots, ("ICICohort_panel.xlsx", "ICICohort_panel.csv"))
    panels = [p for p in panels if p and p.is_file()]
    if len(panels) == 1:
        out_csv = args.out_dir / "channel_map_panel_order.csv"
        out_json = args.out_dir / "panel_validation.json"
        cmd = [sys.executable, "scripts/validate_hcc_panel.py", "--panel", str(panels[0]),
               "--sheet", "Sheet1", "--expected-channels", "45",
               "--out-csv", str(out_csv), "--out-json", str(out_json)]
        run = subprocess.run(cmd, text=True, capture_output=True)
        report["gates"]["panel"] = {"path": str(panels[0]), "exit_code": run.returncode,
                                    "stdout": run.stdout, "stderr": run.stderr,
                                    "csv": str(out_csv), "json": str(out_json)}
    else:
        report["gates"]["panel"] = {"gate": "BLOCKED_FILE_NOT_UNIQUE",
                                    "matches": [str(p) for p in panels],
                                    "note": "Supply --panel with the exact workbook path if zero or multiple matches."}
    checkpoints = [args.checkpoint] if args.checkpoint else find_files(roots, ("model.safetensors",))
    checkpoints = [p for p in checkpoints if p and p.is_file() and "virtues-imc14" in str(p).lower()]
    if len(checkpoints) == 1:
        out_json = args.out_dir / "virtues_imc14_hash_check.json"
        cmd = [sys.executable, "scripts/verify_virtues_checkpoint.py", "--weights", str(checkpoints[0]),
               "--out-json", str(out_json)]
        run = subprocess.run(cmd, text=True, capture_output=True)
        report["gates"]["checkpoint_hash"] = {"path": str(checkpoints[0]), "exit_code": run.returncode,
                                              "stdout": run.stdout, "stderr": run.stderr,
                                              "json": str(out_json)}
    else:
        report["gates"]["checkpoint_hash"] = {"gate": "BLOCKED_FILE_NOT_UNIQUE",
                                              "matches": [str(p) for p in checkpoints],
                                              "note": "No checkpoint download is attempted. Supply --checkpoint with the exact virtues-imc14 model.safetensors path."}
    masks = [args.mask] if args.mask else find_files(roots, ("ICI_stromamasks*.tif", "ICI_stromamasks*.tiff", "*stromamask*.tif", "*stromamask*.tiff"))
    masks = [p for p in masks if p and p.is_file()]
    if len(masks) > 0:
        try:
            import tifffile
            mask_results = []
            for p in masks[:10]:
                arr = tifffile.imread(p)
                vals, counts = np.unique(arr, return_counts=True)
                mask_results.append({"path": str(p), "shape": list(arr.shape), "dtype": str(arr.dtype),
                                     "unique_values": [{"value": int(v), "pixels": int(c)} for v,c in zip(vals,counts)]})
            report["gates"]["stromal_mask_value_inventory"] = {
                "gate": "DESCRIPTIVE_ONLY_LABEL_SEMANTICS_UNRESOLVED",
                "masks_sampled": len(mask_results), "examples": mask_results,
                "note": "Observed values are not assigned to stroma/parenchyma classes."
            }
        except Exception as exc:
            report["gates"]["stromal_mask_value_inventory"] = {"gate":"BLOCKED_READ_ERROR","error":str(exc)}
    else:
        report["gates"]["stromal_mask_value_inventory"] = {"gate":"BLOCKED_NO_MASK_FOUND"}
    output = args.out_dir / "local_gate_summary.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"SUMMARY_JSON={output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
