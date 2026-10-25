# Reproducibility run log

**Last updated:** 25 October 2026  
**Status:** Public-code audit completed to a first-pass level; synthetic unit tests pass; data/model reproduction blocked and not yet performed.

## Source audit completed

### Morpheus paper and public implementation
- Inspected the main published article and Methods PDF, Morpheus README, tutorial notebook, `main.py`, counterfactual-generation code, analysis helper, and TrustScore implementation.
- Confirmed public tutorial path uses `crc_tutorial.zip` from Caltech Data Portal record `pr14s-wgk05`, a pretrained `unet.ckpt`, and `patient_split.json`.
- Confirmed top-level runnable example sets `seed_everything(42)`; this establishes a deterministic starting seed, not robustness across seeds.
- Confirmed the code tracks `PatientID`, `ImageNumber`, and `patch_id`, and the analysis helper maps patch counterfactuals back to patient/image metadata.
- Confirmed TrustScore is a nearest-neighbour distance-based classifier-input trust score; it is not a measure of stability of complete intervention sets across retrained models or patient resamples.
- Confirmed counterfactual-generation helper derives its decision threshold from a validation split, then generates perturbations for selected patches.
- The paper's methods include patient-level splits, within-patient aggregation, across-patient median strategies, and held-out-patient in-silico evaluation. Its results/discussion acknowledge variability between samples and samples from the same patient.

### Data and access trail
- The paper cites separate melanoma data, original melanoma data-for-analysis, preprocessed Morpheus data/model outputs, and a small CRC tutorial bundle. These should not be treated as interchangeable archives.
- The original melanoma data-for-analysis deposit is reported as approximately 7.1 GB, plus a code archive of roughly 41 MB. The source record's reuse/licence terms were not clear in this audit; check them before relying on or redistributing files.
- The paper reports 159 melanoma cores from 69 patients. The CRC liver-metastasis cohort has 209 cores from 30 patients and is described as available from authors on request. The paper describes a breast cohort of 749 cores from 693 patients, but says its marker panel is not suitable for the same perturbation analysis.
- PHAROS (bioRxiv preprint, September 2026) is an adjacent combination-search approach that uses multiple sampled cell groups and robustness-aware re-ranking. That means generic combination discovery, resampling, or ranking is not enough to claim novelty.

## What did not run
- No data archive was successfully downloaded into this runtime.
- No Morpheus dependency environment was installed.
- No original checkpoint was loaded.
- No model training, counterfactual generation, full notebook reproduction, or biological validation was run.
- The separate supplementary PDF was identified on the publisher repository trail, but the downloadable artifact was served through a signed redirect that this runtime could not retrieve. Its full text has **not** been audited.
- Attempts to retrieve public data via direct network access from the execution environment failed due name-resolution/network access errors. Do not interpret that as the public dataset itself being unavailable.

## Code added to this research repo
- `analysis/target_stability.py`: target selection frequency, pairwise/full-set Jaccard, signed-direction consistency, patient-equal-weight predicted uplift summary, and patient-level bootstrap confidence interval utilities.
- `tests/test_target_stability.py`: six synthetic unit tests covering metric conventions, equal patient weighting, deterministic bootstrap, and invalid input handling.
- Local unit-test command: `python -m pytest -q`
- Result: **6 passed** on synthetic inputs.
- These tests validate the helper functions only; they do **not** validate the Morpheus model, original data, or scientific hypothesis.

## Outstanding reproducibility steps
1. Retrieve and read the complete Morpheus supplementary PDF.
2. Resolve licences/terms for the exact dataset bundle and code version.
3. Obtain the tutorial bundle or other authorized preprocessed artifacts in an environment with network access.
4. Create a pinned Python 3.9–3.11 environment matching the published dependencies.
5. Reproduce a small known result and log wall-time, hardware, versions, logs, checksums and deviations.
6. Only then start the cached-output patient-resampling pilot and, if compute permits, the separate model-seed/full retraining experiment.
