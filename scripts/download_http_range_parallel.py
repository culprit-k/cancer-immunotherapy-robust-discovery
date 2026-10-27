#!/usr/bin/env python3
"""Download a large HTTP resource using verified parallel byte ranges.

Designed for public, immutable archives that support HTTP Range. Each chunk is
written to a temporary file, checked against Content-Range and expected length,
then concatenated in order. The final file can be checked against a pinned MD5.
No external download package is required.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def download_chunk(url: str, total: int, index: int, start: int, end: int,
                   workdir: Path, retries: int, timeout: int) -> dict:
    target = workdir / f"chunk_{index:05d}.part"
    expected = end - start + 1
    if target.is_file() and target.stat().st_size == expected:
        return {"index": index, "bytes": expected, "resumed": True}

    error = None
    for attempt in range(1, retries + 1):
        temp = target.with_suffix(".tmp")
        try:
            req = Request(url, headers={"Range": f"bytes={start}-{end}", "Accept-Encoding": "identity"})
            with urlopen(req, timeout=timeout) as response, temp.open("wb") as out:
                if response.status != 206:
                    raise RuntimeError(f"chunk {index}: expected HTTP 206, got {response.status}")
                wanted = f"bytes {start}-{end}/{total}"
                received = response.headers.get("Content-Range", "")
                if received.strip() != wanted:
                    raise RuntimeError(f"chunk {index}: Content-Range mismatch: {received!r}; expected {wanted!r}")
                count = 0
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    out.write(block)
                    count += len(block)
            if count != expected:
                raise RuntimeError(f"chunk {index}: received {count} bytes; expected {expected}")
            os.replace(temp, target)
            return {"index": index, "bytes": count, "resumed": False}
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            try:
                temp.unlink(missing_ok=True)
            except Exception:
                pass
            if attempt < retries:
                time.sleep(min(2 ** (attempt - 1), 12))
    raise RuntimeError(f"failed chunk {index} range {start}-{end} after {retries} attempts: {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--expected-size", required=True, type=int)
    parser.add_argument("--expected-md5", required=True)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--chunk-mib", type=int, default=16)
    parser.add_argument("--retries", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    if args.workers < 1 or args.chunk_mib < 1:
        parser.error("workers and chunk-mib must be positive")
    out = args.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    total = args.expected_size

    # Quick preflight confirms that the origin supports ranged reads before
    # launching the full parallel download.
    probe_end = min(1023 * 1024, total - 1)
    req = Request(args.url, headers={"Range": f"bytes=0-{probe_end}", "Accept-Encoding": "identity"})
    with urlopen(req, timeout=args.timeout) as response:
        if response.status != 206:
            raise RuntimeError(f"origin does not support HTTP range requests: HTTP {response.status}")
        expected_range = f"bytes 0-{probe_end}/{total}"
        if response.headers.get("Content-Range", "").strip() != expected_range:
            raise RuntimeError(
                f"range preflight mismatch: got {response.headers.get('Content-Range')!r}; "
                f"expected {expected_range!r}"
            )
        response.read()

    chunk_size = args.chunk_mib * 1024 * 1024
    ranges = []
    for index, start in enumerate(range(0, total, chunk_size)):
        end = min(total - 1, start + chunk_size - 1)
        ranges.append((index, start, end))

    # Keep chunks in a sibling directory so incomplete downloads never appear
    # at the final archive path.
    workdir = out.parent / (out.name + ".chunks")
    workdir.mkdir(parents=True, exist_ok=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [
            pool.submit(download_chunk, args.url, total, i, start, end,
                        workdir, args.retries, args.timeout)
            for i, start, end in ranges
        ]
        for done, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            result = future.result()
            results.append(result)
            if done == 1 or done % 4 == 0 or done == len(futures):
                print(json.dumps({
                    "progress_chunks": done,
                    "total_chunks": len(futures),
                    "progress_bytes": sum(x["bytes"] for x in results),
                    "progress_fraction": round(done / len(futures), 4),
                }), flush=True)

    temp_out = out.with_suffix(out.suffix + ".assembling")
    with temp_out.open("wb") as dest:
        for index, _, _ in ranges:
            path = workdir / f"chunk_{index:05d}.part"
            with path.open("rb") as src:
                while True:
                    block = src.read(8 * 1024 * 1024)
                    if not block:
                        break
                    dest.write(block)
    size = temp_out.stat().st_size
    actual_md5 = md5(temp_out)
    actual_sha = sha256(temp_out)
    result = {
        "output": str(out),
        "expected_size": total,
        "observed_size": size,
        "size_match": size == total,
        "expected_md5": args.expected_md5.lower(),
        "observed_md5": actual_md5.lower(),
        "md5_match": actual_md5.lower() == args.expected_md5.lower(),
        "sha256": actual_sha,
        "chunks": len(ranges),
        "workers": args.workers,
    }
    print(json.dumps(result, indent=2), flush=True)
    if size != total or actual_md5.lower() != args.expected_md5.lower():
        temp_out.unlink(missing_ok=True)
        return 2
    os.replace(temp_out, out)
    # Remove temporary chunks after the completed archive is atomically installed.
    import shutil
    shutil.rmtree(workdir, ignore_errors=True)
    print(f"VERIFIED_ARCHIVE={out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
