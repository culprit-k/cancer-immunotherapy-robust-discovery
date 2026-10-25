# Reproducibility run log

**Last updated:** 25 October 2026  
**Status:** Main-article/public-code audit and synthetic helper-function tests completed; current robustness-only novelty proposal rejected as a standalone novelty claim; data/model reproduction still pending.

## Source audit completed

### Morpheus paper and public implementation
- Inspected the main published article/Methods PDF, Morpheus README, tutorial notebook, main.py, counterfactual-generation code, analysis helper, and TrustScore implementation.
- Confirmed the public tutorial path uses crc_tutorial.zip from Caltech Data Portal record ID pr14s-wgk05, a pretrained unet.ckpt, and patient_split.json.
- Confirmed the runnable example sets seed_everything(42); this is a fixed seeded starting setup, not robustness across seeds.
- Confirmed code tracks PatientID, ImageNumber and patch_id and maps perturbation outputs back to patient/image metadata.
- Confirmed TrustScore is a nearest-neighbour distance-based classifier-input trust score, not the stability of complete intervention sets across patient resamples/retrained models.
- Confirmed the generation helper chooses a decision threshold using the validation split before generating counterfactuals.
- The main article establishes patient-level splits, within-patient and across-patient median aggregation, in-silico held-out-patient evaluation, sensitivity to sparsity and marked sample variability.

### New nearby literature identified
- PHAROS (bioRxiv preprint, September 2026): single-cell perturbation-model search for target-directed combinations with controls, sampled batches, independent combinatorial data evaluation and robustness-aware reranking.
- Anzum et al., MICCAI 2026: counterfactual directional cell-cell influence in spatial transcriptomics, with held-out cores, permutation/spatial-shuffle controls and core-level bootstrap uncertainty.
- Ding et al., SPAD-CFR, Biology 2026: spatial point-cloud/diffusion counterfactual tissue reprogramming with molecular profiles and coordinates changed together, including melanoma immune-focused intervention hypotheses.
- Consequence: a generic paper that bootstraps/retrains Morpheus and reports selection frequency/Jaccard alone is now considered too incremental for a high-novelty contribution. See docs/related_work_addendum_2026.md and docs/pivot_candidates.md.

## Data and access trail
- The paper cites a melanoma dataset, original melanoma data-for-analysis, Morpheus-preprocessed data/model outputs, and a small CRC tutorial bundle. These are distinct resources.
- The original melanoma data-for-analysis record lists data_for_analysis.zip at approximately 7.1 GB and a code archive around 41 MB. The license field is not clear in the record; check terms before reuse/re-distribution.
- Morpheus reports 159 melanoma cores from 69 patients; CRC liver-metastasis cohort 209 cores from 30 patients; breast cohort 749 cores from 693 patients, with a marker panel described as unsuitable for the same therapeutic perturbation task.
- The separate supplementary PDF is available as a listed artifact from CaltechAUTHORS, but retrieval through its signed download redirect failed. The supplement has not been read and must not be reported as audited.

## What did not run
- No data archive was downloaded into this runtime.
- No Morpheus dependency environment was installed.
- No original checkpoint was loaded.
- No model training, counterfactual generation, full notebook reproduction or biological validation was performed.
- Direct network retrieval from this execution environment failed with name-resolution/network errors; this does not show the public data host is unavailable.

## Code added to this research repo
- analysis/target_stability.py: target selection frequency, pairwise/full-set Jaccard, signed-direction consistency, patient-equal-weight predicted uplift summary and patient-level bootstrap confidence intervals.
- tests/test_target_stability.py: six synthetic unit tests covering metric conventions, equal patient weighting, deterministic bootstrap and invalid inputs.
- Local unit-test command: python -m pytest -q
- Result: **6 passed** on synthetic inputs.
- These tests validate generic helper code only; they do not reproduce Morpheus or establish a scientific result.

## Updated next steps
1. Retrieve and read the complete Morpheus supplementary PDF.
2. Resolve license/terms for the exact data and code artifacts.
3. Build a dataset/method compatibility matrix for cross-method intervention decision utility and cross-cohort/platform transfer.
4. Run a small permitted baseline reproduction in a network-enabled environment, recording versions, checksums, hardware, runtime and deviations.
5. Choose one primary research question only after the prior-art and compatibility gates pass.


## 25 October 2026 — virtual-marker / recommendation-fidelity pivot

### Prior-art refinement
- VirTues (Nature, 2026) is not just a marker-reconstruction model: its Methods also tests whether downstream cell phenotyping remains stable under virtual-marker replacement. It removes/reconstructs CD20 and CD20+CD38 for B-cell phenotyping on Danenberg data and progressively masks T-cell markers for phenotyping on Cords data.
- Therefore, the candidate novelty boundary is narrower than "imputation affects downstream analyses": test whether virtual marker reconstruction changes **signed counterfactual intervention sets and their held-out-patient model-predicted objective**. This is still unverified and needs targeted prior-art review.
- VirTues uses the Hoch et al. melanoma cohort for cell-typing evaluation and notes that some phenotype evaluations align patient-level train/test splits with pretraining. Do not label Hoch as unseen-cohort validation with the standard published full VirTues model.

### Dataset shortlist
- hoch2022multiplexed: melanoma IMC, 35 patients / 50 images in the spora catalogue; most biologically relevant development candidate for chemokines and immune infiltration, subject to panel/license and VirTues exposure checks.
- allam2022spatially: lung IMC, 26 patients / 26 images and about 500 MB in the spora quick-download workflow; best small smoke-test candidate if markers and rights pass.
- moldoveanu2022spatially: melanoma IMC, 90 patients / 90 images; potential independent evaluation candidate, but target markers, outcome labels and model training exposure still need verification.
- xiao2022multiplexed: melanoma IMC, 26 patients / 158 images, anti-PD-1 context; potential external cohort subject to same checks.
- Exact cohort licenses vary. The catalogue was reviewed, but no dataset file was downloaded or inspected locally.

### Synthetic code tests
- Helper source and test files were copied from the current GitHub contents into an isolated local test directory because a direct GitHub clone failed in the execution environment due DNS/name-resolution errors.
- Ran pytest -q tests: **13 passed** (6 target-stability tests + 7 panel-shift metric tests) on synthetic data.
- Test coverage includes reconstruction MAE/RMSE/correlation, signed target-set overlap/direction flips, patient-level uplift fidelity, equal weighting through the patient-level inputs, deterministic bootstrap and invalid-input checks.
- This verifies the utility functions against synthetic cases only. It is not a test of VirTues, Morpheus, SPORA data, or a biological hypothesis. GitHub Actions status was not independently confirmed.

### Still not run
- No spatial data archive downloaded or checksummed.
- No VirTues weights or Morpheus checkpoint loaded.
- No masked-channel reconstruction on actual images/cells.
- No counterfactual target discovery or held-out-patient objective evaluated.
- No full Morpheus supplementary PDF audit; its downloadable artifact could not be retrieved in this runtime.


### Updated metric implementation and tests
- Added a paired patient-level reference-regret helper: compares the candidate and reference target strategies with the same evaluator on the same fully measured held-out patients; positive candidate-minus-reference values mean higher model-predicted uplift.
- Added two more unit tests for patient-level reference regret and mismatched patient IDs.
- Local test run of materialized copies of the committed helper/test source: **15 passed** (6 target-stability + 9 panel-shift tests) using synthetic data.
- The GitHub Actions workflow was corrected to install pandas as well as NumPy/pytest. Its actual hosted run status remains unverified.


### Reporting harness
- Added analysis/panel_shift_report.py, a CLI that accepts prepared marker-reconstruction values, held-out per-core/patch predictions for both strategies, and a JSON of signed target sets; it emits a strict JSON report for reconstruction metrics, target-set fidelity, patient-level uplift fidelity and paired model-based reference regret.
- Added three synthetic tests for the report builder, including matched-patient validation and required-column checks.
- Updated local synthetic test run after adding the report harness: **18 passed** (6 target-stability + 9 panel-shift metric + 3 report-builder tests).
- This harness only evaluates prepared outputs. It does not download data, run VirTues/Morpheus, reconstruct channels or generate counterfactual target sets.


### Patient-level reconstruction error correction
- Hardened the report harness to require patient_id in the reconstruction table, calculate marker reconstruction metrics within each patient, and report patient-macro-averaged error as the primary metric. Pooled-cell metrics are retained only as a secondary diagnostic.
- Added a synthetic test showing how a patient with many more cells would otherwise dominate the pooled error.
- Updated local synthetic suite: **19 passed** (6 target stability + 9 panel-shift metric + 4 panel-shift report tests). The locally materialized copies reflect the updated source and tests from GitHub.


### Patient-macro reconstruction error safeguard
- Updated the report schema to require `patient_id` for every reconstruction row.
- Per-marker MAE/RMSE/bias/correlation are now computed within each patient first and then macro-averaged across patients; pooled-cell metrics are explicitly secondary. This prevents patients with many more cells from dominating the primary reconstruction summary.
- Added a synthetic test that adds many rows to one patient and checks equal patient weighting.
- The previous local test run was **18 passed** before this latest test was added. The current committed suite should contain 19 tests, but a completed hosted CI run for the latest commit has not been verified; do not state 19 passed until CI or a local run confirms it.
