# Next-step gate plan: HCC–VirTues
## Objective
Reach a defensible pre-inference go/no-go decision, then run a leakage-safe reconstruction pilot only if input compatibility and checkpoint provenance are documented.

## Technical preflight (completed 2026-10-27)

The official VirTues source at `2c9c6cba1ee796c4d8dff9329175c47e4a72f409` and pinned `virtues-imc14` weights passed a synthetic CPU preflight in GitHub Actions: checkpoint SHA-256, size and 356-tensor inventory matched; strict load passed with zero missing/unexpected keys; packed attention and synthetic forward passed. See [the run](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504248041) and [report](virtues_synthetic_preflight_report_2026-10-27.md). This tests software/checkpoint execution only; no HCC images were loaded.

## Gate 1 — Data identity and mapping
- Keep the source archive immutable and record SHA-256/MD5, archive source, download date and licence evidence.
- **Partially resolved:** the authoritative supplementary Table 3 reports expected counts of 2 ROIs for ICI_24 and 1 ROI for ICI_39, matching the corrected clinical-table counts (source: [Gut 2024 Supplementary Table 3](https://gut.bmj.com/content/gutjnl/early/2024/10/14/gutjnl-2024-332837/DC4/embed/inline-supplementary-material-4.pdf?download=true)). The archive filename inventory has 3 and 2 files respectively. The table gives counts/aggregate tissue area but not ROI filenames, so the extra file in each case is still not identified authoritatively; exclude these patients from outcome analysis until image-level identity is reconciled.
- Confirm one-to-one mapping of each image, cell mask, stromal mask, channel and patient.
- Validate image dimensions, dtype, finite-value range, channel ordering, mask labels and empty-mask behavior across all 86 triplets—not only a sample.
- Do not publish patient-level clinical rows in this public repository.

## Gate 2 — Checkpoint provenance
- Verify official repository, immutable revision, model architecture/configuration, weight SHA-256 and licence.
- Check the model training-data inventory for Salié HCC exposure. Do not treat a broad paper citation list as an accession-level certificate.
- Exclude virtues-sp32 for held-out HCC evaluation because it includes Salié HCC; do not approve virtues-sp31 until the omitted cohort is verified.

## Gate 3 — Input representation
- Published VirTues processing includes tissue-mask-aware 99th-percentile clipping, shifted log1p, dataset-wise channel standardization and Gaussian smoothing.
- HCC released TIFFs are PENGUIN-normalized to [0,1]. Do not assume this is invertible or equivalent.
- Preferred path: obtain documented original-scale inputs and the official processing metadata.
- Fallback: a clearly labeled normalized-domain adaptation pilot, with all assumptions explicit. It cannot be reported as reproduction of official VirTues preprocessing.

## Gate 4 — Reconstruction pilot
- Use only development patients for fitting/calibration and hold out patients, never random ROIs from the same patient.
- Mask one eligible marker channel at a time; compare reconstruction against the measured held-out channel.
- Include simple baselines and report per-marker error, calibration, uncertainty and patient-level variability.
- Predefine failure thresholds before running the pilot. Do not inspect external-cohort outcomes to tune the pipeline.

## Gate 5 — Outcome analysis (only after gates 1–4 pass)
- Freeze patient-level endpoint definitions, missing-data rules, baseline spatial immune features, eligible marker panel and evaluation split.
- Primary analysis: incremental information over established spatial immunotypes/features, not rediscovery of the known immunotype categories.
- Because only five PR/binary-response-positive cases are present, avoid high-dimensional supervised models; report descriptive estimates and uncertainty.
- Do not describe model-predicted CD8 changes as observed therapeutic effect, causal evidence, clinical utility or patient-specific advice.

## Decision

**NO-GO for official VirTues inference on released normalized TIFFs remains in place.** The synthetic software/model preflight is now complete in accessible CI, but data-specific compatibility gates remain unresolved: panel-to-plane order, UniProt mapping, stromal-mask code meaning, file-level identity for the two ROI-count discrepancies, and official preprocessing compatibility. No HCC inference, outcome model or biological discovery has been run.
