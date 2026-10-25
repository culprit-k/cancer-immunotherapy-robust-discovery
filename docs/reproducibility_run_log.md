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
