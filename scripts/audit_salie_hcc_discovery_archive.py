#!/usr/bin/env python3
"""Verify the CC BY 4.0 HCC discovery archive and report marker-panel metadata only.

Raw images/masks are kept in the ephemeral runner temp directory. Only the
checksum and the small panel metadata table are emitted to stdout/JSON.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

RECORD_ID = "10793609"
FILENAME = "HCC_DiscoveryCohort.zip"
EXPECTED_MD5 = "a842fa253ac2f0eda3cbf4d41e1b0ec1"
RECORD_URL = f"https://zenodo.org/records/{RECORD_ID}"
API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"


def sha256_and_md5(path: Path) -> tuple[str, str]:
    sha = hashlib.sha256()
    md5 = hashlib.md5()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            sha.update(block)
            md5.update(block)
    return sha.hexdigest(), md5.hexdigest()


def find_file_url(record: dict) -> tuple[str, int, str | None]:
    for entry in record.get("files", []):
        if entry.get("key") == FILENAME or entry.get("filename") == FILENAME:
            links = entry.get("links", {})
            url = links.get("content") or links.get("download") or links.get("self")
            if not url:
                raise RuntimeError("Zenodo API metadata had no direct file URL")
            checksum = entry.get("checksum")
            size = int(entry.get("size", 0))
            return url, size, checksum
    raise RuntimeError(f"{FILENAME} not found in Zenodo API file list")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    session = requests.Session()
    meta_response = session.get(API_URL, timeout=60)
    meta_response.raise_for_status()
    record = meta_response.json()
    if record.get("doi", "").lower() != "10.5281/zenodo.10793609":
        raise RuntimeError(f"Unexpected Zenodo DOI: {record.get('doi')!r}")
    download_url, advertised_size, advertised_checksum = find_file_url(record)

    with tempfile.TemporaryDirectory(prefix="salie_hcc_audit_") as temp_dir:
        archive = Path(temp_dir) / FILENAME
        response = session.get(download_url, stream=True, timeout=(30, 180))
        response.raise_for_status()
        downloaded = 0
        next_progress = 256 * 1024 * 1024
        with archive.open("wb") as stream:
            for chunk in response.iter_content(chunk_size=8 * 1024 * 1024):
                if chunk:
                    stream.write(chunk)
                    downloaded += len(chunk)
                    if downloaded >= next_progress:
                        print(f"Downloaded {downloaded:,} bytes of the HCC discovery archive", flush=True)
                        next_progress += 256 * 1024 * 1024

        actual_size = archive.stat().st_size
        file_sha256, file_md5 = sha256_and_md5(archive)
        if advertised_size and actual_size != advertised_size:
            raise RuntimeError(
                f"File-size mismatch: downloaded {actual_size}, Zenodo advertises {advertised_size}"
            )
        if file_md5.lower() != EXPECTED_MD5:
            raise RuntimeError(
                f"Known Zenodo MD5 mismatch: expected {EXPECTED_MD5}, got {file_md5}"
            )
        if advertised_checksum and ":" in advertised_checksum:
            algorithm, value = advertised_checksum.split(":", 1)
            if algorithm.lower() == "md5" and value.lower() != file_md5.lower():
                raise RuntimeError("Downloaded MD5 disagrees with current Zenodo API metadata")

        with zipfile.ZipFile(archive) as zf:
            names = zf.namelist()
            panel_matches = [
                name for name in names
                if Path(name).name.lower() == "dccohort_panel.csv"
            ]
            if len(panel_matches) != 1:
                raise RuntimeError(
                    "Expected exactly one DCCohort_panel.csv; found "
                    + json.dumps(panel_matches)
                )
            panel_member = panel_matches[0]
            with zf.open(panel_member, "r") as raw:
                import io
                text_stream = io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
                sample = text_stream.read(8192)
                text_stream.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=",;\\t")
                except csv.Error:
                    dialect = csv.excel
                reader = csv.DictReader(text_stream, dialect=dialect)
                fields = reader.fieldnames or []
                rows = [dict(row) for row in reader]

            extension_counts = Counter(Path(name).suffix.lower() or "[no extension]" for name in names)
            top_dirs = sorted({name.split("/", 1)[0] for name in names if "/" in name})

    report = {
        "audit_type": "metadata_only_archive_integrity_and_panel_audit",
        "record_id": RECORD_ID,
        "doi": "10.5281/zenodo.10793609",
        "source_url": RECORD_URL,
        "source_title": record.get("metadata", {}).get("title"),
        "source_published_license": "CC BY 4.0 per NLM Dataset Catalog; verify source-page attribution terms",
        "archive_filename": FILENAME,
        "archive_expected_md5": EXPECTED_MD5,
        "archive_actual_md5": file_md5,
        "archive_sha256": file_sha256,
        "archive_size_bytes": actual_size,
        "archive_size_bytes_advertised": advertised_size,
        "zenodo_api_checksum": advertised_checksum,
        "archive_integrity_match": file_md5.lower() == EXPECTED_MD5,
        "zip_entries_count": len(names),
        "top_level_directories": top_dirs,
        "extension_counts": dict(sorted(extension_counts.items())),
        "panel_file": panel_member,
        "panel_columns": fields,
        "panel_row_count": len(rows),
        "panel_rows": rows,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_guardrail": "Raw images and masks were not uploaded or committed; only the panel metadata and integrity summary are emitted.",
        "interpretation_guardrail": "Panel inspection is not model inference, cell-label validation, or proof that counterfactual target discovery is compatible.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
