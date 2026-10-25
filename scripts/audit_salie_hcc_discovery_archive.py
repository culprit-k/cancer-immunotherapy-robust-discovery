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
import sys
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


def source_license_summary(record: dict) -> dict:
    metadata = record.get("metadata", {})
    license_value = metadata.get("license")
    if isinstance(license_value, dict):
        license_id = license_value.get("id")
        license_title = license_value.get("title")
    elif isinstance(license_value, str):
        license_id = license_value
        license_title = license_value
    else:
        license_id = None
        license_title = None
    return {
        "metadata_license_raw": license_value,
        "license_id": license_id,
        "license_title": license_title,
        "license_field_present": license_value is not None,
    }


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

    # The 42-patient ICI set is a proposed external cohort, but its direct
    # Zenodo licence field has appeared blank. Query only its metadata here;
    # do not download those image data until its source-level terms are clear.
    external_meta_response = session.get(
        "https://zenodo.org/api/records/10794904", timeout=60
    )
    external_meta_response.raise_for_status()
    external_record = external_meta_response.json()
    if external_record.get("doi", "").lower() != "10.5281/zenodo.10794904":
        raise RuntimeError(
            f"Unexpected external Zenodo DOI: {external_record.get('doi')!r}"
        )

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
            infos = zf.infolist()
            names = [info.filename for info in infos]
            csv_infos = [
                info for info in infos
                if not info.is_dir() and Path(info.filename).suffix.lower() == ".csv"
            ]
            csv_inventory = [
                {"filename": info.filename, "size_bytes": info.file_size}
                for info in csv_infos
            ]
            # Prefer the known name, then a unique filename containing "panel".
            # If neither is unique, preserve the inventory in the report rather
            # than guessing or failing before a useful diagnostic artifact exists.
            panel_matches = [
                info.filename for info in csv_infos
                if Path(info.filename).name.lower() == "dccohort_panel.csv"
            ]
            selection_method = "exact_filename"
            if len(panel_matches) == 0:
                panel_matches = [
                    info.filename for info in csv_infos
                    if "panel" in Path(info.filename).name.lower()
                    and info.file_size <= 25 * 1024 * 1024
                ]
                selection_method = "unique_panel_name_fallback"
            panel_member = panel_matches[0] if len(panel_matches) == 1 else None
            fields = []
            rows = []
            panel_parse_error = None
            if panel_member:
                try:
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
                except (UnicodeDecodeError, csv.Error, OSError) as exc:
                    panel_parse_error = f"{type(exc).__name__}: {exc}"
                    fields = []
                    rows = []

            # Structural metadata QC; deliberately does not imply model compatibility.
            sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
            from analysis.panel_metadata_qc import audit_panel_structure

            panel_qc = (
                audit_panel_structure(fields, rows)
                if panel_member and not panel_parse_error
                else None
            )

            extension_counts = Counter(Path(name).suffix.lower() or "[no extension]" for name in names)
            top_dirs = sorted({name.split("/", 1)[0] for name in names if "/" in name})

    report = {
        "audit_type": "metadata_only_archive_integrity_and_panel_audit",
        "record_id": RECORD_ID,
        "doi": "10.5281/zenodo.10793609",
        "source_url": RECORD_URL,
        "source_title": record.get("metadata", {}).get("title"),
        "source_zenodo_api_license_metadata": source_license_summary(record),
        "source_published_license_mirror": "NLM Dataset Catalog reports CC BY 4.0; compare this with the direct Zenodo API metadata.",
        "external_ici_record_id": "10794904",
        "external_ici_doi": "10.5281/zenodo.10794904",
        "external_ici_zenodo_api_license_metadata": source_license_summary(external_record),
        "external_ici_archive_metadata_only": [
            {
                "filename": entry.get("key"),
                "size_bytes": entry.get("size"),
                "checksum": entry.get("checksum"),
            }
            for entry in external_record.get("files", [])
        ],
        "external_ici_images_downloaded": False,
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
        "csv_inventory": csv_inventory,
        "panel_file": panel_member,
        "panel_selection_method": selection_method,
        "panel_identification_status": (
            "identified_and_parsed" if panel_member and not panel_parse_error
            else "identified_but_parse_failed" if panel_member
            else "ambiguous_or_not_found"
        ),
        "panel_parse_error": panel_parse_error,
        "panel_candidate_filenames": panel_matches,
        "panel_columns": fields,
        "panel_row_count": len(rows),
        "panel_rows": rows,
        "panel_structural_qc": panel_qc,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_guardrail": "Raw images and masks were not uploaded or committed; only the panel metadata and integrity summary are emitted.",
        "interpretation_guardrail": "Panel structural QC checks only the table structure. It is not model inference, cell-label validation, marker-embedding compatibility, checkpoint exposure clearance, or proof that counterfactual target discovery is compatible.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
