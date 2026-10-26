#!/usr/bin/env python3
"""Fail-closed scaffold for the first HCC–VirTues reconstruction pilot.

This intentionally does NOT import or call VirTues. It validates that the
required metadata are explicitly supplied before any model run. It prevents
silently guessing channel order, preprocessing, checkpoint identity, or mask
semantics. After these checks pass, use the pinned official VirTues inference
implementation to execute the preregistered crop/masking experiment.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

REQUIRED = {
    "image_dir": "Directory containing HCC TIFF images",
    "cell_mask_dir": "Directory containing cell masks",
    "stromal_mask_dir": "Directory containing stromal masks",
    "channel_map": "CSV mapping ordered image channels to marker and UniProt ID",
    "qc_json": "Full TIFF/mask QC JSON from the preflight utility",
    "checkpoint_path": "Local checkpoint weights file",
    "checkpoint_revision": "Exact immutable checkpoint revision/commit",
    "checkpoint_sha256": "Expected SHA-256 of checkpoint weights",
    "preprocessing_mode": "official_reproduction or normalized_domain_adaptation",
    "preprocessing_record": "Documented pipeline and statistics reference",
    "roi_id": "Predeclared ROI ID; do not choose based on outcomes",
    "seed": "Fixed random seed",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True,
                    help="JSON config with all REQUIRED keys")
    ap.add_argument("--out", type=Path, required=True,
                    help="Path to write a gate report")
    args = ap.parse_args()
    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    errors, warnings = [], []
    for key, description in REQUIRED.items():
        if key not in cfg or cfg[key] in (None, ""):
            errors.append(f"Missing {key}: {description}")
    for key in ("image_dir", "cell_mask_dir", "stromal_mask_dir", "channel_map", "qc_json", "checkpoint_path", "preprocessing_record"):
        if key in cfg and cfg[key] and not Path(cfg[key]).exists():
            errors.append(f"Path does not exist for {key}: {cfg[key]}")
    if cfg.get("preprocessing_mode") not in ("official_reproduction", "normalized_domain_adaptation"):
        errors.append("preprocessing_mode must be official_reproduction or normalized_domain_adaptation")
    if cfg.get("preprocessing_mode") == "normalized_domain_adaptation":
        warnings.append("Results must be reported as normalized-domain adaptation, not official preprocessing reproduction.")
    if cfg.get("checkpoint_path") and Path(cfg["checkpoint_path"]).is_file():
        actual = sha256(Path(cfg["checkpoint_path"]))
        expected = str(cfg.get("checkpoint_sha256", "")).lower().strip()
        if expected and actual != expected:
            errors.append(f"Checkpoint SHA-256 mismatch: expected {expected}, observed {actual}")
    report = {
        "gate": "PASS" if not errors else "BLOCKED",
        "errors": errors,
        "warnings": warnings,
        "config": {k: cfg.get(k) for k in REQUIRED},
        "checkpoint_sha256_observed": sha256(Path(cfg["checkpoint_path"])) if cfg.get("checkpoint_path") and Path(cfg["checkpoint_path"]).is_file() else None,
        "metrics": None,
        "interpretation": "No inference was run by this gate script. A PASS means metadata prerequisites were supplied, not that model compatibility or scientific validity has been proven."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 2

if __name__ == "__main__":
    raise SystemExit(main())
