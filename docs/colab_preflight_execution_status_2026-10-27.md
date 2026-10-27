# Colab preflight status and execution handoff

**Updated:** 27 October 2026  
**Branch:** `hcc-virtues-audit-next-step`  
**Latest code commit:** `fc0203b39b67e99795487eb8737fdd66a37eefe9`

## What has been done

- Added a reversible, fail-closed helper for testing the official VirTues packed-attention code on CPU with PyTorch SDPA when FlashAttention is unavailable.
- Added synthetic unit tests for source-anchor validation, dry-run non-mutation, backup creation, idempotence, syntax validity, and equivalence to independent SDPA segments.
- Added a single preflight runner that checks source-tree presence, patch application, checkpoint SHA-256/size/tensor count, packed attention execution, strict state-dict loading, and a tiny synthetic forward.
- Fixed the preflight gate so a failed packed-attention smoke test cannot be treated as an import success and cannot proceed to checkpoint loading.
- Linked the helper and tests from the repository README.

## CI evidence

The following GitHub Actions runs completed successfully for commit `fc0203b`:

- [Analysis helper tests](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40499721699)
- [HCC pre-algorithm metadata-gate tests](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40499721676)
- [Additional HCC metadata-gate run](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40499717040)

These are repository CI tests. They do **not** mean the helper was run in the user's Colab, that the actual checkpoint loaded, or that HCC inference has run.

## Run in the existing Colab

This is a staged runbook. It deliberately stops short of HCC image inference.

1. Confirm the paths point to the existing official VirTues checkout and the private, locally downloaded checkpoint. Do not upload the checkpoint, patient-level clinical tables, or raw images to the public repository.

2. Clone/update only the helper repository:
   ```python
   !git clone --branch hcc-virtues-audit-next-step https://github.com/culprit-k/cancer-immunotherapy-robust-discovery.git /content/cancer-immunotherapy-robust-discovery
   ```
   If that destination already exists, do not clone over it; use `git -C /content/cancer-immunotherapy-robust-discovery pull` instead.

3. First perform the dry run (does not modify the official checkout):
   ```python
   !python /content/cancer-immunotherapy-robust-discovery/scripts/patch_virtues_cpu_sdpa.py --virtues-root /content/virtues_official
   ```
   Inspect the printed source hash and patch validation. If it fails, stop and share the full error; do not manually force the patch.

4. Apply only after reviewing the dry-run result:
   ```python
   !python /content/cancer-immunotherapy-robust-discovery/scripts/patch_virtues_cpu_sdpa.py --virtues-root /content/virtues_official --apply
   ```
   This writes a timestamped backup beside the source file.

5. Run the complete synthetic preflight. Substitute the actual existing local checkpoint and official marker-embedding directory if they differ:
   ```python
   !python /content/cancer-immunotherapy-robust-discovery/scripts/run_virtues_cpu_preflight_colab.py \
       --virtues-root /content/virtues_official \
       --checkpoint /content/hcc_virtues_private/checkpoints/virtues-imc14/model.safetensors \
       --marker-embeddings /content/virtues_official/assets/example_dataset/marker_embeddings \
       --out /content/virtues_cpu_preflight_report.json
   ```
   The runner hashes the checkpoint and writes a JSON report. Keep that report private if local paths reveal sensitive details. If the report is blocked, share the report text or only the failed step plus traceback; do not share raw clinical rows or checkpoint weights.

## Scientific decision remains unchanged

**No-go for direct pretrained VirTues inference on the released HCC normalized TIFFs.** The source data are PENGUIN-normalized to [0,1], whereas the official VirTues data contract includes marker mapping, clipping/log transformation, blur, and dataset/tissue statistics. The CPU patch addresses execution, not input-distribution compatibility.

Before any HCC inference, still required:
- authoritative ROI/patient crosswalk, including the ICI_24 and ICI_39 multiplicity conflicts;
- channel-order and marker/embedding mapping verification;
- mask semantics and full-cohort QC;
- a documented compatible input representation or an explicitly separate normalized-domain adaptation design;
- checkpoint exposure and licensing records frozen for the actual study;
- a preregistered development-only reconstruction pilot with a simple baseline and held-out patients.

No real-data reconstruction, immune-evasion target, clinical prediction, novelty, or patentability claim is established by these software tests.
