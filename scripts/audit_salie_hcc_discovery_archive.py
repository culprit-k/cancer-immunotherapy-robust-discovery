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
import numpy as np
import tifffile

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



def inspect_tiff_member(zf: zipfile.ZipFile, filename: str, inspect_pixels: bool = False) -> dict:
    """Read TIFF metadata and optional sparse page statistics without exporting pixels."""
    result: dict = {"readable": False, "page_statistics": []}
    try:
        with zf.open(filename, "r") as stream:
            with tifffile.TiffFile(stream) as tif:
                if not tif.series:
                    raise RuntimeError("TIFF contains no image series")
                series = tif.series[0]
                pages = list(tif.pages)
                result.update({
                    "readable": True,
                    "series_count": len(tif.series),
                    "series_shape": [int(v) for v in series.shape],
                    "series_dtype": str(series.dtype),
                    "page_count": len(pages),
                    "page_shapes": sorted({
                        tuple(int(v) for v in page.shape) for page in pages
                    }),
                })
                if inspect_pixels and pages:
                    page_indices = sorted(set([0, len(pages) // 2, len(pages) - 1]))
                    for page_index in page_indices:
                        arr = pages[page_index].asarray()
                        if arr.size == 0:
                            continue
                        result["page_statistics"].append({
                            "page_index": int(page_index),
                            "shape": [int(v) for v in arr.shape],
                            "dtype": str(arr.dtype),
                            "min": float(np.min(arr)),
                            "p50": float(np.percentile(arr, 50)),
                            "p99": float(np.percentile(arr, 99)),
                            "max": float(np.max(arr)),
                            "fraction_zero": float(np.mean(arr == 0)),
                        })
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def inspect_tiff_structure(zf: zipfile.ZipFile, infos: list[zipfile.ZipInfo], panel_rows: int) -> dict:
    """Deterministically sample image stacks and masks; report summaries only."""
    tiff_infos = [
        info for info in infos
        if not info.is_dir() and Path(info.filename).suffix.lower() in {".tif", ".tiff"}
    ]
    directory_counts = Counter(
        info.filename.split("/", 1)[0] for info in tiff_infos if "/" in info.filename
    )
    image_infos = sorted(
        [info for info in tiff_infos if info.filename.startswith("DC_img_normalized/")],
        key=lambda info: info.filename.casefold(),
    )

    def evenly_spaced(items: list[zipfile.ZipInfo], maximum: int) -> list[tuple[int, zipfile.ZipInfo]]:
        if len(items) <= maximum:
            return list(enumerate(items))
        indices = sorted(set(round(i * (len(items) - 1) / (maximum - 1)) for i in range(maximum)))
        return [(index, items[index]) for index in indices]

    image_samples = []
    for index, info in evenly_spaced(image_infos, 12):
        meta = inspect_tiff_member(zf, info.filename, inspect_pixels=True)
        image_samples.append({
            "sample_index_in_sorted_image_list": index,
            "compressed_member_size_bytes": int(info.file_size),
            **meta,
        })

    mask_samples = {}
    for directory in ("DC_cellmasks", "DC_stromamasks"):
        items = sorted(
            [info for info in tiff_infos if info.filename.startswith(directory + "/")],
            key=lambda info: info.filename.casefold(),
        )
        mask_samples[directory] = [
            {
                "sample_index_in_sorted_directory_list": index,
                "compressed_member_size_bytes": int(info.file_size),
                **inspect_tiff_member(zf, info.filename, inspect_pixels=False),
            }
            for index, info in evenly_spaced(items, 3)
        ]

    readable_images = [item for item in image_samples if item.get("readable")]
    all_readable = bool(image_samples) and len(readable_images) == len(image_samples)
    page_counts = sorted({item.get("page_count") for item in readable_images})
    dtypes = sorted({item.get("series_dtype") for item in readable_images})
    shapes = sorted({tuple(item.get("series_shape", [])) for item in readable_images})
    sampled_pages_match_panel = (
        bool(readable_images)
        and all(item.get("page_count") == panel_rows for item in readable_images)
    )
    sampled_pixel_values = [
        stat
        for item in readable_images
        for stat in item.get("page_statistics", [])
    ]

    return {
        "audit_scope": "TIFF metadata for all entries; pixel statistics from deterministic sparse page samples only",
        "tiff_file_count_all_directories": len(tiff_infos),
        "tiff_file_counts_by_top_level_directory": dict(sorted(directory_counts.items())),
        "normalized_image_stack_count": len(image_infos),
        "sampled_normalized_image_stack_count": len(image_samples),
        "sampled_image_stacks_all_readable": all_readable,
        "sampled_image_series_shapes": [list(shape) for shape in shapes],
        "sampled_image_series_dtypes": dtypes,
        "sampled_image_page_counts": page_counts,
        "sampled_image_page_count_matches_panel_rows": sampled_pages_match_panel,
        "sampled_image_stacks": image_samples,
        "mask_tiff_samples_by_directory": mask_samples,
        "sampled_pixel_numeric_range": {
            "min": min((x["min"] for x in sampled_pixel_values), default=None),
            "max": max((x["max"] for x in sampled_pixel_values), default=None),
            "p99_min_across_sampled_pages": min((x["p99"] for x in sampled_pixel_values), default=None),
            "p99_max_across_sampled_pages": max((x["p99"] for x in sampled_pixel_values), default=None),
            "interpretation": "Stored pixel values only. Compare with the paper's semantic 0-1 normalization statement; integer TIFF storage may use an encoded integer scale, so do not rescale by assumption.",
        },
        "interpretation_guardrail": "Sparse TIFF sampling establishes storage shape/type/range but cannot restore original acquisition intensities or certify compatibility with VirTues preprocessing.",
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
            tiff_audit = inspect_tiff_structure(zf, infos, len(rows))

    report = {
        "audit_type": "metadata_only_archive_integrity_panel_and_sparse_tiff_audit",
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
        "tiff_structure_audit": tiff_audit,
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_guardrail": "Raw images and masks were not uploaded or committed; the report contains source metadata, panel metadata, TIFF metadata, and sparse sampled pixel summaries only.",
        "interpretation_guardrail": "Panel and sparse TIFF QC do not establish cell-label validity, canonical marker-embedding compatibility, equivalent preprocessing domains, checkpoint exposure by themselves, or biological validity. No model inference is performed.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
