# Experimental CPU SDPA compatibility helper for VirTues

**Date:** 27 October 2026  
**Status:** Experimental execution aid; not yet validated against the live Colab runtime or a real HCC image.

## Why this helper exists

The inspected VirTues source imports **flash_attn_varlen_qkvpacked_func** unconditionally, although **MHAwithPosEmb.forward()** also contains a standard PyTorch SDPA path. In the user's Colab environment, importing **virtues.modules.multiplex_virtues** failed with **ModuleNotFoundError: No module named 'flash_attn'**; PyTorch reports **2.11.0+cpu** and CUDA is unavailable.

A simple optional import is not enough: several VirTues blocks call the packed variable-length path by providing **cu_seq_len** and **max_seq_len**. The helper in **scripts/patch_virtues_cpu_sdpa.py** adds an experimental fallback that splits the packed sequence using the cumulative lengths and runs PyTorch SDPA independently over each segment.

## Safety properties

- Dry-run is the default. It does not change the source.
- **--apply** changes only **virtues/modules/layers/attention_flashattention.py**.
- Before writing, it creates a timestamped backup of the original file.
- It verifies the expected import and packed attention-call anchors, then compiles the patched source. If the upstream implementation differs, it fails closed without editing the file.
- The fallback checks that packed batches have **B=1**, query/key lengths match, and cumulative sequence boundaries are valid.
- The fallback uses dropout only in training mode, following the FlashAttention path's dropout convention.
- Unit tests cover dry-run non-mutation, backup/restore evidence, patch idempotence, syntax compilation, and fail-closed behavior on source drift.

## Use in Colab

Clone the project helper without changing the official VirTues checkout:

\`\`\`python
!git clone --branch hcc-virtues-audit-next-step https://github.com/culprit-k/cancer-immunotherapy-robust-discovery.git
!python /content/cancer-immunotherapy-robust-discovery/scripts/patch_virtues_cpu_sdpa.py --virtues-root /content/virtues_official
\`\`\`

Review the dry-run output first. If the source hash and target path are expected, apply the patch:

\`\`\`python
!python /content/cancer-immunotherapy-robust-discovery/scripts/patch_virtues_cpu_sdpa.py --virtues-root /content/virtues_official --apply
\`\`\`

Then run a minimal code-path smoke test before attempting to instantiate the complete model:

\`\`\`python
import torch
from virtues.modules.layers.attention_flashattention import MHAwithPosEmb

torch.manual_seed(7)
model = MHAwithPosEmb(
    embed_dim=16,
    num_heads=4,
    dropout=0.0,
    inbuilt_pos_emb=None,
).eval()

x = torch.randn(1, 7, 16)
cu = torch.tensor([0, 3, 7], dtype=torch.int32)
with torch.no_grad():
    y = model(
        query=x,
        key=x,
        value=x,
        cu_seq_len=cu,
        max_seq_len=4,
    )

assert y.shape == x.shape, (y.shape, x.shape)
assert torch.isfinite(y).all(), "Non-finite output"
print("Packed CPU SDPA smoke test: PASS", tuple(y.shape))
\`\`\`

This smoke test proves only that the patched packed-attention path executes on a tiny synthetic tensor. It is not checkpoint loading, a reconstruction result, or a biological result. The official VirTues model may expose additional dependency/configuration errors after the first import blocker is removed. CPU runtime may be very slow for real image-sized workloads.

## Scientific restrictions that remain

This patch does **not** resolve any HCC input compatibility gate. The released Salié HCC TIFFs are already normalized to [0,1]; that alone does not establish equivalence to the official VirTues/spora preprocessing path, which includes marker mapping and dataset statistics. Do not invert the normalized images or invent channel statistics. Do not run outcome analysis until ROI/patient mapping, marker-plane identity, mask semantics, checkpoint hash/exposure, and preprocessing are independently verified.

For the current evidence-based decision, see:
- docs/HCC_virtues_compatibility_review_2026-10-27.md
- docs/HCC_VirTues_next_step_gate_plan.md
- docs/hcc_preprocessing_and_checkpoint_exposure_decision_2026-10-25.md

## Upstream source check

On 27 October 2026, the official upstream file at https://github.com/bunnelab/virtues/blob/main/virtues/modules/layers/attention_flashattention.py was inspected through GitHub. The upstream blob SHA was `7a907156f995bddc0e371daad4c485abdb00a74b`; the expected import line, packed-QKV start anchor, and FlashAttention call-end anchor each occurred exactly once. This supports the helper's fail-closed patch targeting the observed upstream revision, but does not prove the user's local checkout is identical.

## Current validation status

The helper and its synthetic fixture tests passed locally in the assistant's isolated environment (6 tests). GitHub Actions was triggered on the research pull request; see the [Actions runs](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions). This is not a test against the user's Colab files. Actual upstream-source patching, model import, checkpoint loading, and HCC inference remain unverified until executed in the appropriate runtime.
