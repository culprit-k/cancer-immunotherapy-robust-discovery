#!/usr/bin/env python3
"""Verify a local VirTues weight file against the pinned Hugging Face file revision.

This tool verifies byte identity only. It does not establish that the checkpoint's
training-data exposure is eligible or that the input preprocessing is compatible.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PINNED_REPOSITORY = "bunnelab/virtues"
PINNED_PATH = "virtues-imc14/model.safetensors"
# Keep this aligned with resolve_virtues_imc14_checkpoint.py and the decision memo.
PINNED_REVISION = "43fd00fce052c46f9e0cc1a87f42806620632319"
PINNED_SHA256 = "714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f"


def sha256_file(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path, expected_sha256: str = PINNED_SHA256) -> dict:
    if not path.is_file():
        return {
            "gate": "BLOCKED_FILE_NOT_FOUND",
            "path": str(path),
            "error": "Checkpoint file does not exist at the supplied path.",
            "pinned_repository": PINNED_REPOSITORY,
            "pinned_path": PINNED_PATH,
            "pinned_revision": PINNED_REVISION,
            "expected_sha256": expected_sha256,
        }
    actual = sha256_file(path)
    matched = actual.lower() == expected_sha256.lower()
    return {
        "gate": "PASS_PINNED_FILE_HASH" if matched else "BLOCKED_HASH_MISMATCH",
        "path": str(path),
        "file_size_bytes": path.stat().st_size,
        "actual_sha256": actual,
        "expected_sha256": expected_sha256,
        "hash_matches": matched,
        "pinned_repository": PINNED_REPOSITORY,
        "pinned_path": PINNED_PATH,
        "pinned_revision": PINNED_REVISION,
        "critical_limit": "A matching SHA-256 verifies file identity only. It does not validate checkpoint training-cohort exposure, licence compliance, input-channel mapping, or preprocessing compatibility.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", type=Path, required=True, help="Path to the downloaded model.safetensors")
    parser.add_argument("--out-json", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.weights)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["gate"] == "PASS_PINNED_FILE_HASH" else 2


if __name__ == "__main__":
    raise SystemExit(main())
