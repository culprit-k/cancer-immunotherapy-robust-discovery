#!/usr/bin/env python3
"""Apply a reversible CPU SDPA fallback to the official VirTues attention module.

This is an experimental execution-compatibility aid, not the official VirTues
preprocessing pipeline and not evidence that normalized HCC TIFFs are compatible
with a pretrained checkpoint. It only addresses the FlashAttention import and
packed variable-length attention call in attention_flashattention.py.

Usage:
  python scripts/patch_virtues_cpu_sdpa.py --virtues-root /content/virtues_official
  python scripts/patch_virtues_cpu_sdpa.py --virtues-root /content/virtues_official --apply

By default it is dry-run only. With --apply it writes a timestamped backup and
modifies only virtues/modules/layers/attention_flashattention.py. It fails closed
if the expected upstream source signature has changed.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import os
from pathlib import Path
import sys

IMPORT_LINE = (
    "from flash_attn.flash_attn_interface import flash_attn_varlen_qkvpacked_func"
)
IMPORT_REPLACEMENT = '''try:
    from flash_attn.flash_attn_interface import flash_attn_varlen_qkvpacked_func
except ImportError:  # optional dependency; use the packed SDPA fallback below
    flash_attn_varlen_qkvpacked_func = None
'''

START_ANCHOR = "        qkv=torch.stack([Q.squeeze(0), K.squeeze(0), V.squeeze(0)], dim=1)"
END_ANCHOR = ").unsqueeze(0)  # (total_Q, H, D) collapsed over batch by varlen kernel"
BEGIN_MARKER = "        # BEGIN CPU SDPA fallback (research compatibility patch)"
END_MARKER = "        # END CPU SDPA fallback (research compatibility patch)"

FALLBACK_BLOCK = '''        # BEGIN CPU SDPA fallback (research compatibility patch)
        # Use independent SDPA calls for packed sequences when FlashAttention
        # is absent or tensors are on CPU. Sequence boundaries are preserved.
        # This does not validate or reproduce VirTues input preprocessing.
        if flash_attn_varlen_qkvpacked_func is None or not Q.is_cuda:
            if B != 1:
                raise RuntimeError(
                    "CPU SDPA fallback expects packed inputs with B=1; "
                    f"received B={B}."
                )
            if L != S:
                raise RuntimeError(
                    "Packed SDPA fallback requires equal query/key lengths; "
                    f"received L={L}, S={S}."
                )
            boundaries = [int(v) for v in cu_seq_len.detach().to("cpu").tolist()]
            if (not boundaries or boundaries[0] != 0 or boundaries[-1] != L
                    or any(a > b for a, b in zip(boundaries, boundaries[1:]))):
                raise ValueError(
                    "cu_seq_len must be nondecreasing, start at zero, and end at L."
                )
            lengths = [b - a for a, b in zip(boundaries, boundaries[1:])]
            if max_seq_len is not None and lengths and max(lengths) > int(max_seq_len):
                raise ValueError("max_seq_len is smaller than a packed sequence length.")

            qh = Q.transpose(1, 2)  # (B, H, L, D)
            kh = K.transpose(1, 2)
            vh = V.transpose(1, 2)
            chunks = []
            fallback_dropout = self.dropout if self.training else 0.0
            for start, end in zip(boundaries, boundaries[1:]):
                if end == start:
                    continue
                chunk = F.scaled_dot_product_attention(
                    qh[:, :, start:end, :],
                    kh[:, :, start:end, :],
                    vh[:, :, start:end, :],
                    dropout_p=fallback_dropout,
                )
                chunks.append(chunk)
            if not chunks:
                raise ValueError("cu_seq_len describes no non-empty sequences.")
            attn_out = torch.cat(chunks, dim=2).transpose(1, 2)  # (1, L, H, D)
        else:
            qkv = torch.stack([Q.squeeze(0), K.squeeze(0), V.squeeze(0)], dim=1)
            attn_out = flash_attn_varlen_qkvpacked_func(
                qkv=qkv,
                cu_seqlens=cu_seq_len,
                max_seqlen=max_seq_len,
                deterministic=True,
                dropout_p=self.dropout if self.training else 0.0,
            ).unsqueeze(0)  # (total_Q, H, D) collapsed over batch by varlen kernel
        # END CPU SDPA fallback (research compatibility patch)'''


def patch_source(source: str) -> str:
    """Return patched source or raise if the expected upstream code differs."""
    if BEGIN_MARKER in source and END_MARKER in source:
        return source
    if source.count(IMPORT_LINE) != 1:
        raise ValueError("Expected exactly one known FlashAttention import line; no changes made.")
    source = source.replace(IMPORT_LINE, IMPORT_REPLACEMENT, 1)
    start = source.find(START_ANCHOR)
    if start < 0:
        raise ValueError("Could not find expected packed-QKV call start; no changes made.")
    end = source.find(END_ANCHOR, start)
    if end < 0:
        raise ValueError("Could not find expected FlashAttention call end; no changes made.")
    end += len(END_ANCHOR)
    return source[:start] + FALLBACK_BLOCK + source[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--virtues-root", required=True, type=Path,
                        help="Root of the cloned official VirTues repo, e.g. /content/virtues_official")
    parser.add_argument("--apply", action="store_true",
                        help="Write a backup and apply the patch")
    args = parser.parse_args()

    target = args.virtues_root / "virtues/modules/layers/attention_flashattention.py"
    if not target.is_file():
        print(f"ERROR: expected attention module not found: {target}", file=sys.stderr)
        return 2

    original = target.read_text(encoding="utf-8")
    try:
        patched = patch_source(original)
        compile(patched, str(target), "exec")
    except Exception as exc:
        print(f"ERROR: patch validation failed; original file unchanged: {exc}", file=sys.stderr)
        return 2

    if patched == original:
        print("Already patched; no file changed.")
        return 0

    digest = hashlib.sha256(original.encode("utf-8")).hexdigest()
    print("Target:", target)
    print("Original source SHA-256:", digest)
    print("Patched source syntax: PASS")
    print("Mode:", "APPLY" if args.apply else "DRY RUN (no files changed)")
    if not args.apply:
        print("Dry run only. Re-run with --apply to make a backup and apply.")
        return 0

    timestamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = target.with_name(target.name + f".pre_cpu_sdpa_{timestamp}.bak")
    with backup.open("x", encoding="utf-8") as handle:
        handle.write(original)
    temp = target.with_suffix(target.suffix + ".tmp")
    try:
        temp.write_text(patched, encoding="utf-8")
        os.replace(temp, target)
    except Exception:
        if temp.exists():
            temp.unlink()
        print(f"ERROR: write failed. Original backup is at {backup}", file=sys.stderr)
        return 3

    print("Patch applied.")
    print("Backup:", backup)
    print("Restore by copying the backup over:", target)
    print("NOTE: this enables only a code-path test; it does not approve the HCC data/model pairing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
