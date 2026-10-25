#!/usr/bin/env python3
"""Resolve and hash the official VirTues IMC-only checkpoint without committing weights."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

REPO_ID = "bunnelab/virtues"
FILENAME = "virtues-imc14/model.safetensors"
PINNED_REVISION = "43fd00fce052c46f9e0cc1a87f42806620632319"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--revision",
        default=PINNED_REVISION,
        help="Immutable Hugging Face revision to resolve (defaults to the audited revision).",
    )
    args = parser.parse_args()

    api = HfApi()
    info = api.model_info(REPO_ID, revision=args.revision)
    revision = info.sha
    if not revision or len(revision) < 12:
        raise RuntimeError("Hugging Face did not return an immutable model revision")

    artifact = Path(
        hf_hub_download(repo_id=REPO_ID, filename=FILENAME, revision=revision)
    )
    manifest = {
        "repository": REPO_ID,
        "filename": FILENAME,
        "immutable_revision": revision,
        "file_sha256": sha256_file(artifact),
        "file_size_bytes": artifact.stat().st_size,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "weight_license": "CC BY-NC 4.0 (verify against the model card at use time)",
        "training_scope_as_published": "virtues-imc14: 14 IMC datasets",
        "purpose": "reproducibility manifest only; weights are not copied into this repository",
        "exposure_note": (
            "Published VirTues Methods place Salié et al. (reference 95) among "
            "the seven additional IMC cohorts in the extended 32-cohort corpus; "
            "the virtues-imc14 variant is the core 14-IMC corpus. This supports "
            "no direct Salié-study exposure for this checkpoint at the published "
            "corpus/reference level. It is not a machine-readable accession-to-"
            "training-run certificate."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
