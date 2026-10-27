# Project execution status — 27 October 2026

This is the operational snapshot for **Cancer Immunotherapy AI: Robust Target Discovery**. It separates repository/software evidence from work that requires the user's Colab archive and from claims that have not been established.

## Executive decision

**Current phase: pre-inference compatibility validation.** Archive/TIFF storage checks are encouraging, and the experimental CPU attention fallback is covered by synthetic tests, but real VirTues inference on HCC data has not been completed. Official VirTues inference on the released HCC normalized TIFFs remains **NO-GO** until their input representation is shown to match the official pipeline or original-scale compatible data are obtained. Do not invent or invert preprocessing statistics.

Current research candidate:

> When complete spatial-proteomics marker channels are missing and reconstructed, do signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes remain faithful to those produced from fully measured channels?

This is a candidate research question, not a confirmed novelty, causal mechanism, clinical prediction or patentability claim.

## Work completed and evidence

### 1. HCC source-data and structural QC

Recorded source-derived audit results:
- Discovery cohort archive HCC_DiscoveryCohort.zip: 1,541,132,381 bytes; MD5 a842fa253ac2f0eda3cbf4d41e1b0ec1. Archive checksum and 42-row panel structural checks passed in workflow [40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382).
- HCC ICI cohort structural report supplied from the user's Colab: 86 image stacks, 86 cell masks and 86 stromal masks; dimensions matched across each image/mask pair; each image reported as 45 channels in channel-first format, finite stored values between 0 and 1.
- The panel workbook had 45 channels (1–45). This establishes panel-table structure and channel count, **not** exact TIFF-plane-to-target ordering.
- HCC clinical extraction has 42 patients with response categories SD=27, PD=10 and PR=5; these are patient-level labels, not independent ROI outcomes.

Outstanding reconciliation:
- Clinical metadata lists 84 ROI entries, whereas 86 image/mask triplets were inventoried. ICI_24 has 2 listed clinical ROIs vs 3 released image files; ICI_39 has 1 listed vs 2 image files. Do not guess, discard or merge these records. Resolve against the primary source or quarantine affected ROIs.
- Mask file/value inspection is not a semantic codebook. Stromal-mask values reported as 3–9 and high instance-label counts must be interpreted using source documentation and representative overlays, not recoded by assumption.
- Preserve patient-level aggregation/splits: ROIs, tiles and cells from one patient must not cross partitions.

### 2. VirTues checkpoint and runtime

User's Colab output reports:
- Checkpoint path: /content/hcc_virtues_private/checkpoints/virtues-imc14/model.safetensors
- Approximate file size: 165.5 MiB; 356 tensors readable through safetensors metadata.
- PyTorch 2.11.0+cpu; CUDA unavailable.
- FlashAttention missing, and importing virtues.modules.multiplex_virtues failed.
- ESM, Biopython, spora_io, transformers and OmegaConf were reported available in the latest dependency inspection; verify any additional dependency errors after resolving the first import blocker.

Official candidate checkpoint identity to verify in the local runtime:
- Repository: bunnelab/virtues
- File: virtues-imc14/model.safetensors
- Immutable revision: 43fd00fce052c46f9e0cc1a87f42806620632319
- Expected SHA-256: 714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f
- Expected byte count: 173543728
- Published weight licence: CC BY-NC 4.0; check exact terms before any commercial/patent-related activity.

The 356 tensor names and size do not alone prove architecture compatibility. The preflight runner checks the full hash/size/tensor count, then strict-loads into the official default configuration and tests a small synthetic forward if those gates succeed. It does not open HCC images.

### 3. Compatibility helper

Added to this open branch:
- scripts/patch_virtues_cpu_sdpa.py: reversible, source-anchor-checked patch; dry run by default; applying it creates a timestamped backup.
- tests/test_patch_virtues_cpu_sdpa.py: tests idempotence, fail-closed behavior, dry-run non-mutation, backup creation and CPU SDPA fallback behavior.
- scripts/run_virtues_cpu_preflight_colab.py: synthetic preflight for source, checkpoint, attention path, strict state-dict load and tiny synthetic forward.
- tests/test_virtues_cpu_preflight_cli.py: verifies the CLI works independently of optional model dependencies.
- docs/virtues_cpu_sdpa_compatibility_patch_2026-10-27.md: scope, usage and scientific limitations.

On 27 October 2026 the official upstream attention file was checked at blob SHA 7a907156f995bddc0e371daad4c485abdb00a74b; the expected import and packed-attention anchors each occurred once. This validates patch targeting against that public source blob only; the user's local source may differ.

**Important:** A successful helper/CI test is not evidence that the patch has been applied in Colab, the checkpoint strict-loads, real HCC inference completes, or the data are compatible. The preflight runner uses only synthetic input and writes a private JSON report. It must not be described as biological model validation.

## Pre-inference scientific gate

Official VirTues expects a documented marker-to-UniProt mapping, marker embeddings, standardized spora_io input, channel/tissue statistics, tissue-aware 99th-percentile clipping, shifted log1p, Gaussian smoothing, dataset-wise standardization and fixed crops in the official example workflow. Public HCC image stacks are already PENGUIN-normalized to [0,1]. That range alone does not show equivalence to the official model input distribution, and the source TIFFs do not recover the pre-normalization intensity scale.

Permitted next routes:
1. **Preferred:** obtain original-scale/compensated intensity data and channel-specific preprocessing metadata from the study team; reproduce the official pipeline and document deviations.
2. **Fallback:** pre-register and label a separate *normalized-domain adaptation* study, with patient-level development/validation and direct comparison against simple baselines. This is not official VirTues preprocessing reproduction and requires its own scientific justification and rights review.
3. Switch to a cohort distributed in a compatible standard format only after its panel, labels, patient grouping, training exposure and use terms are checked.

Do not load the checkpoint against normalized HCC TIFFs for a nominal smoke test: passing tensors through code would not establish valid input compatibility.

## Novelty and method decision

The generic robustness/Jaccard-only idea is **not sufficient**. Existing work already covers spatial-proteomics counterfactual target discovery and patient-level evaluation (Morpheus); spatial-proteomics marker reconstruction and downstream tasks (VirTues); missing protein reconstruction with a spatial-proteomics foundation model (Spatium); and generative spatial counterfactual tissue reprogramming (SPAD-CFR). CONCERT and related uncertainty-aware imputation/counterfactual methods are additional conceptual neighbors.

The only current candidate is the narrower **decision-fidelity consequence of whole-marker-channel reconstruction**:
- masked-marker reconstruction MAE/RMSE and correlation on measured, held-out values;
- signed target-set fidelity at a fixed target budget (signed Jaccard, precision/recall, direction flips);
- patient-level model-predicted uplift agreement and model-based reference regret on the same untouched patients;
- optionally, a predeclared abstention/reliability curve if it beats simple baselines at equal coverage/target budget.

The full-measurement reference remains a model output, not biological ground truth. Model-predicted CD8 uplift is not an observed treatment effect or proof of causality. No target has been validated and novelty is unverified; the targeted literature audit is not systematic and cannot establish patentability.

## Immediate execution gates

1. Run scripts/run_virtues_cpu_preflight_colab.py in the user's existing Colab with --apply-patch. It should back up and patch only the attention module; test packed SDPA; hash/check the checkpoint; strict-load the model; run a tiny synthetic forward; and write /content/virtues_cpu_preflight_report.json.
2. Inspect that report. If import/model/checkpoint/synthetic forward fails, stop and diagnose the exact error. Do not run an HCC ROI yet.
3. Produce a private 45-row panel-to-plane/UniProt mapping verified against source metadata.
4. Resolve ICI_24 / ICI_39 from source records, or exclude those ROIs with an explicit preregistered rule and report the limitation.
5. Verify the stromal-mask codebook and representative overlays.
6. Confirm input preprocessing and checkpoint exposure.
7. Only after gates 3–6, run one fixed, outcome-blind 128×128 pilot ROI and score only masked pixels/channels against predeclared mean and marker-correlation baselines.
8. Run patient-level validation and the recommendation-fidelity study only if the pilot, permission and prior-art gates pass.

## Repository and governance

The audit work is on pull request [#2](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/pull/2), branch hcc-virtues-audit-next-step; main has not been changed or merged. Latest helper/CI links are available from the [Actions page](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions). No model weights or raw image/mask arrays should be committed to this public repository. Keep patient-level tables, identifying filenames, detailed QC output and preflight reports in the private Colab workspace.

## Primary references

- VirTues, Nature (2026): https://doi.org/10.1038/s41586-026-10884-y
- Morpheus, Nature Biomedical Engineering (2025): https://doi.org/10.1038/s41551-025-01357-0
- Spatium preprint (2026): https://doi.org/10.64898/2026.07.23.740264
- SPAD-CFR, Biology (2026): https://doi.org/10.3390/biology15141097
- Salié et al. HCC study: https://doi.org/10.1136/gutjnl-2024-332837
- HCC discovery archive: https://zenodo.org/records/10793609
- HCC ICI archive: https://zenodo.org/records/10794904
