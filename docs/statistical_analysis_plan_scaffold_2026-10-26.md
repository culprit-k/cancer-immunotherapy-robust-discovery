# Analysis plan scaffold: HCC–VirTues
**Status:** draft scaffold; not frozen or registered because input compatibility and outcome semantics remain unresolved.

## Primary question
Does a prespecified spatial representation add reproducible patient-level information beyond established HCC spatial immune features for ICI outcome analysis?

## Analysis sequence
**A. Technical gate first.** Validate files, channel identities, mask alignment, preprocessing, checkpoint revision/hash/licence/exposure, and ROI-to-patient mapping. Do not inspect outcomes to choose ROIs or tune processing.

**B. Reconstruction pilot.** On a deterministic eligible ROI and fixed crop/mask pattern, compare predicted values only at masked pixels/channels against a simple tissue-area mean baseline. Report per-marker and pooled MSE/MAE, scored pixel counts, patient-level variation and failures. This is a technical task, not evidence of target discovery.

**C. Patient-level incremental analysis.** Only after A/B pass, decide whether the cohort is development or external evaluation. Freeze endpoints, covariates, features, split and thresholds first. All ROIs from a patient must remain in the same split. Do not tune on any cohort designated external.

## Endpoints and coding safeguards
- Treat best RECIST response categories and the source binary response field as separate source variables until their definitions are verified; prior extraction shows five positive values coinciding with PR, a cross-check only.
- Do not use the source field “Censored [0=yes]” as a PFS event indicator until verified against the data dictionary / article source.
- Preserve the source AFP unit as recorded until independently confirmed.
- Document treatment regimen, specimen timing, biopsy/resection status, ROI count, and missingness where available.
- Do not combine heterogeneous ICI regimens or time origins without a prespecified rationale.

## Split and validation rules
- Patient is the minimum independent split unit, not ROI or cell.
- Prefer an independent cohort for transportability. If only a single small cohort is available, label estimates exploratory and avoid using them to select the final model.
- All imputation, scaling, feature selection, calibration, threshold selection and hyperparameter tuning occur only inside development folds.
- Use grouped resampling or patient bootstrap for uncertainty; report intervals, not just point estimates.
- Never select a threshold using the evaluation cohort.
- Account for multiplicity and report all prespecified variants, including failures and negative results.

## Comparator ladder
1. Established categories / available CD8 density and compartment distribution.
2. Small interpretable spatial feature set.
3. Low-dimensional penalized model, where events and missingness permit.
4. VirTues representation without any proposed novel component.
5. Full proposed method.
6. Permuted-outcome and random-feature negative controls.
7. Ablations for each claimed novel component.

## Metrics
- Technical reconstruction: per-marker/pooled MSE and MAE, with scored-pixel counts and patient-level uncertainty.
- Binary outcomes, only if endpoint/event counts justify: discrimination and calibration with uncertainty; avoid AUC-only reporting.
- Survival, only if event/time definitions and event counts are verified: concordance and calibration at prespecified time horizons, with uncertainty.
- Incremental information: compare against the frozen comparator, not against a straw baseline.
- Robustness: performance/rank stability under documented marker dropout, ROI subsampling, panel shifts and plausible preprocessing sensitivity.

## Stop conditions
Stop downstream analyses if mappings remain ambiguous, checkpoint exposure is unacceptable/unknown for the claim, preprocessing is undocumented, the model cannot beat a simple baseline on held-out patients, estimates are unstable, or validation data cannot be kept untouched.

## Reporting
Use TRIPOD+AI for prediction-model reporting and REMARK principles for tumour-marker work as applicable. This is a protocol scaffold; the final plan must be versioned, signed off and frozen before any outcome-guided decisions.
