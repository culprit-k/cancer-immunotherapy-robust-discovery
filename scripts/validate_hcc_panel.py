#!/usr/bin/env python3
"""Validate an HCC IMC panel workbook and export an ordered channel-map CSV.

This validates workbook completeness/uniqueness only. It CANNOT prove that TIFF
plane index i corresponds to workbook Channel i; that requires source-level
confirmation or a known reference image. It does not access clinical outcomes.
Dependencies: pandas, openpyxl.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

REQUIRED_COLUMNS = {"Channel", "MetalTag", "Target"}

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--panel", type=Path, required=True, help="Panel .xlsx or .csv")
    ap.add_argument("--sheet", default="Sheet1", help="Excel worksheet name (default: Sheet1)")
    ap.add_argument("--expected-channels", type=int, default=45)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    args = ap.parse_args()

    import pandas as pd
    if args.panel.suffix.lower() == ".csv":
        df = pd.read_csv(args.panel)
    elif args.panel.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(args.panel, sheet_name=args.sheet)
    else:
        raise SystemExit("Panel must be .csv, .xlsx, or .xls")

    errors: list[str] = []
    missing_cols = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    if errors:
        report = {"gate": "BLOCKED", "errors": errors, "rows": int(len(df))}
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 2

    work = df.copy()
    work["Channel"] = pd.to_numeric(work["Channel"], errors="coerce")
    if work["Channel"].isna().any():
        errors.append("Channel contains missing or non-numeric values.")
    else:
        if not (work["Channel"] % 1 == 0).all():
            errors.append("Channel contains non-integer values.")
        channels = [int(x) for x in work["Channel"]]
        if len(channels) != len(set(channels)):
            errors.append("Duplicate channel numbers.")
        expected = set(range(1, args.expected_channels + 1))
        observed = set(channels)
        if observed != expected:
            errors.append(
                f"Channel set mismatch: missing={sorted(expected-observed)}, "
                f"unexpected={sorted(observed-expected)}"
            )

    for col in ("MetalTag", "Target"):
        vals = work[col].fillna("").astype(str).str.strip()
        if vals.eq("").any():
            errors.append(f"{col} has blank values at rows {list((vals[vals.eq('')].index + 2).astype(int))}.")

    if not errors:
        work = work.sort_values("Channel")
        export = work[["Channel", "MetalTag", "Target"]].copy()
        export["Channel"] = export["Channel"].astype(int)
        export.columns = ["channel", "metal_tag", "marker"]
        args.out_csv.parent.mkdir(parents=True, exist_ok=True)
        export.to_csv(args.out_csv, index=False, quoting=csv.QUOTE_MINIMAL)

    report = {
        "gate": "PASS_PANEL_TABLE_ONLY" if not errors else "BLOCKED",
        "panel_path": str(args.panel),
        "worksheet": args.sheet if args.panel.suffix.lower() in {".xlsx", ".xls"} else None,
        "rows": int(len(df)),
        "expected_channels": args.expected_channels,
        "errors": errors,
        "critical_limit": "PASS does not verify TIFF plane order or VirTues marker-embedding mapping.",
        "export_csv": str(args.out_csv) if not errors else None,
    }
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 2

if __name__ == "__main__":
    raise SystemExit(main())
