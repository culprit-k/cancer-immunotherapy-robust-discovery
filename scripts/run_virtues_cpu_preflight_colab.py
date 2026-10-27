#!/usr/bin/env python3
"""One-command Colab preflight for the experimental VirTues CPU SDPA fallback.

This command can optionally apply the reversible patch, then checks the pinned
checkpoint hash/metadata, imports VirTues, runs a tiny packed-attention test,
strict-loads the checkpoint using the official config and example ESM embeddings,
and runs a tiny synthetic model forward. It never reads the HCC TIFFs.

A passing run is code/checkpoint smoke testing only. It is NOT proof of official
HCC preprocessing compatibility, cohort independence, target validity, or
biological/clinical performance.

Example:
  python scripts/run_virtues_cpu_preflight_colab.py \
    --virtues-root /content/virtues_official \
    --checkpoint /content/hcc_virtues_private/checkpoints/virtues-imc14/model.safetensors \
    --marker-embeddings /content/virtues_official/assets/example_dataset/marker_embeddings \
    --apply-patch \
    --out /content/virtues_cpu_preflight_report.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback
from typing import Any

EXPECTED_SHA256 = "714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f"
EXPECTED_SIZE_BYTES = 173543728
EXPECTED_TENSOR_COUNT = 356


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def exception_details(exc: BaseException) -> dict[str, str]:
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(limit=8),
    }


def run() -> tuple[dict[str, Any], int]:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--virtues-root", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--marker-embeddings", type=Path, required=True)
    parser.add_argument("--apply-patch", action="store_true",
                        help="Apply reversible source patch after creating a timestamped backup.")
    parser.add_argument("--expected-sha256", default=EXPECTED_SHA256)
    parser.add_argument("--expected-size-bytes", type=int, default=EXPECTED_SIZE_BYTES)
    parser.add_argument("--expected-tensor-count", type=int, default=EXPECTED_TENSOR_COUNT)
    parser.add_argument("--out", type=Path, default=Path("/content/virtues_cpu_preflight_report.json"))
    args = parser.parse_args()

    root = args.virtues_root.resolve()
    checkpoint = args.checkpoint.resolve()
    embeddings_dir = args.marker_embeddings.resolve()
    report: dict[str, Any] = {
        "purpose": "synthetic CPU/import/checkpoint preflight only; no HCC data are loaded",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "virtues_root": str(root),
        "checkpoint_path": str(checkpoint),
        "marker_embeddings_path": str(embeddings_dir),
        "patch_applied_by_this_run": False,
        "steps": {},
        "scientific_inference": "NOT_RUN",
        "biological_claims": "NONE",
        "overall": "BLOCKED",
    }
    failures = 0

    required_source = root / "virtues/modules/layers/attention_flashattention.py"
    model_source = root / "virtues/modules/multiplex_virtues.py"
    config_path = root / "configs/base_config.yaml"
    if not required_source.is_file() or not model_source.is_file() or not config_path.is_file():
        report["steps"]["source_tree"] = {
            "status": "FAIL",
            "detail": "Expected official VirTues source and configs/base_config.yaml were not all found.",
            "required": [str(required_source), str(model_source), str(config_path)],
        }
        failures += 1
    else:
        report["steps"]["source_tree"] = {"status": "PASS"}

    # Apply via the separately tested helper. A backup is created only when needed.
    patch_script = Path(__file__).with_name("patch_virtues_cpu_sdpa.py")
    if report["steps"]["source_tree"]["status"] == "PASS":
        cmd = [
            sys.executable, str(patch_script),
            "--virtues-root", str(root),
        ]
        if args.apply_patch:
            cmd.append("--apply")
        try:
            patch = subprocess.run(cmd, capture_output=True, text=True, check=False)
            report["steps"]["patch"] = {
                "status": "PASS" if patch.returncode == 0 else "FAIL",
                "return_code": patch.returncode,
                "stdout": patch.stdout[-6000:],
                "stderr": patch.stderr[-3000:],
                "mode": "apply" if args.apply_patch else "dry_run",
            }
            report["patch_applied_by_this_run"] = args.apply_patch and patch.returncode == 0 and "Patch applied." in patch.stdout
            if patch.returncode != 0:
                failures += 1
        except Exception as exc:
            report["steps"]["patch"] = {"status": "FAIL", **exception_details(exc)}
            failures += 1
    else:
        report["steps"]["patch"] = {"status": "BLOCKED", "detail": "Source tree gate failed."}
        failures += 1

    # Check model checkpoint identity before loading its tensors into a model.
    checkpoint_ok = False
    if not checkpoint.is_file():
        report["steps"]["checkpoint_identity"] = {
            "status": "FAIL", "detail": "Checkpoint file not found."
        }
        failures += 1
    else:
        observed_size = checkpoint.stat().st_size
        observed_sha = sha256_file(checkpoint)
        identity = {
            "path": str(checkpoint),
            "observed_size_bytes": observed_size,
            "expected_size_bytes": args.expected_size_bytes,
            "size_match": observed_size == args.expected_size_bytes,
            "observed_sha256": observed_sha,
            "expected_sha256": args.expected_sha256.lower(),
            "sha256_match": observed_sha.lower() == args.expected_sha256.lower(),
        }
        try:
            from safetensors import safe_open
            with safe_open(str(checkpoint), framework="pt", device="cpu") as safe_file:
                keys = list(safe_file.keys())
                identity["tensor_count"] = len(keys)
                identity["expected_tensor_count"] = args.expected_tensor_count
                identity["tensor_count_match"] = len(keys) == args.expected_tensor_count
                identity["first_20_tensor_names"] = keys[:20]
        except Exception as exc:
            identity["safetensors_metadata_error"] = exception_details(exc)
        checkpoint_ok = (
            identity["sha256_match"]
            and identity["size_match"]
            and identity.get("tensor_count_match", False)
        )
        identity["status"] = "PASS" if checkpoint_ok else "FAIL"
        report["steps"]["checkpoint_identity"] = identity
        if not checkpoint_ok:
            failures += 1

    # Test the exact CPU packed-attention execution path.
    import_ok = False
    if report["steps"].get("patch", {}).get("status") == "PASS" and report["steps"]["patch"].get("mode") == "apply":
        sys.path.insert(0, str(root))
        try:
            import torch
            report["environment"] = {
                "python": sys.version,
                "torch": torch.__version__,
                "cuda_available": torch.cuda.is_available(),
                "device_used": "cpu",
            }
            from virtues.modules.layers.attention_flashattention import MHAwithPosEmb

            torch.manual_seed(7)
            attention = MHAwithPosEmb(
                embed_dim=16, num_heads=4, dropout=0.0, inbuilt_pos_emb=None
            ).cpu().eval()
            x = torch.randn(1, 7, 16)
            cu = torch.tensor([0, 3, 7], dtype=torch.int32)
            with torch.no_grad():
                y = attention(
                    query=x, key=x, value=x,
                    cu_seq_len=cu, max_seq_len=4,
                )
            attention_pass = tuple(y.shape) == tuple(x.shape) and bool(torch.isfinite(y).all())
            report["steps"]["packed_attention_smoke"] = {
                "status": "PASS" if attention_pass else "FAIL",
                "input_shape": list(x.shape),
                "output_shape": list(y.shape),
                "finite": bool(torch.isfinite(y).all()),
                "segments": [3, 4],
                "device": str(y.device),
            }
            import_ok = attention_pass
            if not attention_pass:
                failures += 1
        except Exception as exc:
            report["steps"]["packed_attention_smoke"] = {"status": "FAIL", **exception_details(exc)}
            failures += 1
    else:
        report["steps"]["packed_attention_smoke"] = {
            "status": "BLOCKED",
            "detail": "Use --apply-patch to run import/smoke tests after a successful patch validation.",
        }
        failures += 1

    # Strict checkpoint load into the released default architecture, then a tiny synthetic forward.
    if import_ok and checkpoint_ok and embeddings_dir.is_dir():
        try:
            import torch
            from omegaconf import OmegaConf
            from safetensors.torch import load_file
            from virtues.modules.multiplex_virtues import MultiplexVirtues
            from virtues.utils.utils import load_marker_embeddings

            conf = OmegaConf.load(str(config_path))
            marker_embeddings = load_marker_embeddings(str(embeddings_dir))
            # The official checkpoint defines the required embedding width.
            # Do not hard-code 768: the pinned IMC14 checkpoint expects 640.
            projection_key = "encoder.prior_embedding_encoder.weight"
            if projection_key not in weights:
                # Load weights before model construction only to inspect the released projection.
                weights = load_file(str(checkpoint), device="cpu")
            projection = weights.get(projection_key)
            if projection is None or projection.ndim != 2:
                raise ValueError(f"Checkpoint is missing a 2-D {projection_key} tensor")
            expected_embedding_dim = int(projection.shape[1])
            if marker_embeddings.ndim != 2 or marker_embeddings.shape[1] != expected_embedding_dim:
                raise ValueError(
                    f"Marker embeddings must have shape (N, {expected_embedding_dim}) "
                    f"according to checkpoint tensor {projection_key}; observed {tuple(marker_embeddings.shape)}"
                )

            model = MultiplexVirtues(
                prior_bias_embeddings=marker_embeddings,
                prior_bias_embedding_type="esm",
                prior_bias_embedding_fusion_type="add",
                patch_size=int(conf.model.patch_size),
                model_dim=int(conf.model.model_dim),
                feedforward_dim=int(conf.model.feedforward_dim),
                encoder_pattern=str(conf.model.encoder_pattern),
                num_encoder_heads=int(conf.model.num_encoder_heads),
                decoder_pattern=str(conf.model.decoder_pattern),
                num_decoder_heads=int(conf.model.num_decoder_heads),
                num_hidden_layers=int(conf.model.num_decoder_hidden_layers),
                positional_embedding_type=str(conf.model.positional_embedding_type),
                dropout=float(conf.model.dropout),
                group_layers=conf.model.group_layers,
                norm_after_encoder_decoder=bool(conf.model.norm_after_encoder_decoder),
                verbose=False,
            ).cpu()

            weights = load_file(str(checkpoint), device="cpu")
            incompatible = model.load_state_dict(weights, strict=True)
            model.eval()

            # Small synthetic two-marker tile; this is a shape/runtime test only.
            torch.manual_seed(11)
            synthetic = torch.rand(2, 16, 16, dtype=torch.float32)
            channel_ids = torch.tensor([0, 1], dtype=torch.long)
            mask = torch.zeros(2, 2, 2, dtype=torch.bool)
            mask[0, 0, 0] = True
            mask[1, 1, 1] = True
            with torch.no_grad():
                output = model([synthetic], [channel_ids], [mask])
            decoded = output.decoded_multiplex[0]
            model_pass = tuple(decoded.shape) == tuple(synthetic.shape) and bool(torch.isfinite(decoded).all())
            report["steps"]["strict_checkpoint_load"] = {
                "status": "PASS",
                "strict": True,
                "missing_keys": list(incompatible.missing_keys),
                "unexpected_keys": list(incompatible.unexpected_keys),
                "model_config": {
                    "patch_size": int(conf.model.patch_size),
                    "model_dim": int(conf.model.model_dim),
                    "feedforward_dim": int(conf.model.feedforward_dim),
                    "encoder_pattern": str(conf.model.encoder_pattern),
                    "decoder_pattern": str(conf.model.decoder_pattern),
                    "positional_embedding_type": str(conf.model.positional_embedding_type),
                },
                "marker_embedding_shape": list(marker_embeddings.shape),
                "device": "cpu",
            }
            report["steps"]["synthetic_model_forward"] = {
                "status": "PASS" if model_pass else "FAIL",
                "input_shape": list(synthetic.shape),
                "mask_shape": list(mask.shape),
                "output_shape": list(decoded.shape),
                "finite": bool(torch.isfinite(decoded).all()),
                "device": str(decoded.device),
                "note": "Synthetic input only; not HCC inference or preprocessing validation.",
            }
            if not model_pass:
                failures += 1
        except Exception as exc:
            report["steps"]["strict_checkpoint_load_and_synthetic_forward"] = {
                "status": "FAIL", **exception_details(exc)
            }
            failures += 1
    else:
        missing = []
        if not import_ok: missing.append("packed attention import/smoke test did not pass")
        if not checkpoint_ok: missing.append("checkpoint identity failed")
        if not embeddings_dir.is_dir(): missing.append("marker embedding directory not found")
        report["steps"]["strict_checkpoint_load_and_synthetic_forward"] = {
            "status": "BLOCKED", "reasons": missing
        }
        failures += 1

    report["overall"] = "PASS_SYNTHETIC_PREFLIGHT_ONLY" if failures == 0 else "BLOCKED_OR_FAILED"
    report["final_warning"] = (
        "Even an overall PASS is only a synthetic CPU/model/checkpoint smoke test. "
        "It does not authorize inference on normalized HCC TIFFs, prove held-out cohort independence, "
        "or establish an immune-evasion mechanism, biomarker, clinical prediction, novelty, or patentability."
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nPrivate report written to: {args.out}")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(run())
