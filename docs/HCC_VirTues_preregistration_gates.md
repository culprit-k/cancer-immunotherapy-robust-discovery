# Preregistration gates for the HCC–VirTues reconstruction pilot

## Status
Protocol scaffold only. No model has been run and thresholds are not yet frozen because source-level input and checkpoint compatibility remain unresolved. Do not describe this document as a completed preregistration.

## Hypothesis
Conditional on a verified input pipeline and eligible checkpoint, pretrained spatial-proteomics representations may reconstruct masked marker channels with useful patient-held-out fidelity. Reconstruction fidelity alone will not establish target-discovery fidelity or clinical relevance.

## Required before pilot execution
1. Freeze a machine-readable manifest mapping patient, ROI, image, channel, cell mask and stromal mask.
2. Resolve the two reported ROI discrepancies against source records.
3. Document the exact checkpoint repository, immutable revision, weight SHA-256, architecture/configuration, licence and training-exposure evidence.
4. Record the input transform, including clipping, log transform, standardization statistics, smoothing, tissue mask and channel order. If using PENGUIN-normalized inputs, call it a distinct adaptation and do not claim official preprocessing reproduction.
5. Split by patient, not ROI; keep all ROIs from one patient in one partition.
6. Define eligible markers and exclude channels whose mapping or measurement compatibility is uncertain.
7. Predefine a simple baseline, per-marker reconstruction metrics, uncertainty summaries and failure thresholds before inspecting held-out results.
8. Keep the 42-patient ICI cohort untouched during development and tuning.

## Minimum reporting
- Number of patients and ROIs in each split.
- Per-marker and patient-level errors with uncertainty intervals.
- Baseline comparison and missing/failed image accounting.
- Sensitivity to normalization assumptions.
- All deviations from this plan.

## Stop criteria
Stop before downstream outcome analysis if image/channel/mask mapping is ambiguous, checkpoint training exposure cannot be assessed, the transform is undocumented, the model cannot outperform a simple baseline on held-out patients, or uncertainty is too large to support reliable decisions.

## Interpretation boundary
Reconstructed intensities are model estimates, not measured biology. Model-predicted CD8 infiltration changes are not observed treatment effects, causal evidence, clinical utility, or patient-specific advice.