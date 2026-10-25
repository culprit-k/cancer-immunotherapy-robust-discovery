# Targeted prior-art and feasibility audit — 25 October 2026

## Executive decision

**Status: conditional feasibility pilot only; novelty is not established.** The broad question "does imputation preserve downstream analysis?" is already occupied. The defensible candidate is narrower: whether uncertainty in whole-channel virtual staining changes *signed spatial counterfactual intervention recommendations*, and whether a calibrated selective/abstention rule can identify cases where those recommendations are unreliable.

No real-data experiment, model inference, checkpoint audit, or biological validation was performed as part of this audit.

## Prior-art map and implications

| Work | What is already covered | Consequence for our claim |
|---|---|---|
| Morpheus, Nature Biomedical Engineering (2025), DOI 10.1038/s41551-025-01357-0 | Spatial-proteomic counterfactual perturbations intended to improve predicted CD8+ infiltration; held-out patient evaluation and selected in-vitro validation. | Do not claim spatial counterfactual target discovery, CD8 objective, target combinations, or patient-level testing as new. |
| VirTues, Nature (2026), DOI 10.1038/s41586-026-10884-y | Foundation model for spatial-proteomic marker reconstruction, virtual staining, cross-panel/technology transfer, biomarkers and cell phenotyping. The paper describes marker-masking experiments followed by downstream B-/T-cell phenotyping. | Generic virtual staining and preservation of downstream cell typing are not novel. |
| Spatium: A Protein Language Foundation Model for Spatial Proteomics (2026) | Protein imputation on held-out tissue sections and spatial-proteomics representations. | Generic spatial protein imputation or section-level validation is not novel. Check full methods and code before a final novelty claim. |
| CONCERT (bioRxiv preprint, 20 November 2025; DOI 10.1101/2025.11.08.686890) | Spatial-transcriptomics method combines spatial counterfactual perturbation-response prediction, missing-region imputation and calibrated predictive uncertainty. Different modality and task, but conceptually close to imputation-aware counterfactual prediction. | This is a material adjacent prior-art risk. The project must distinguish *intervention-set decision fidelity under complete protein-channel reconstruction* from generic imputation-plus-counterfactual prediction. |
| iScience spatial-metabolomics missing-data benchmark (2026), DOI 10.1016/j.isci.2026.115203 | Benchmarks reconstruction accuracy and preservation of downstream spatial clustering. | Downstream evaluation beyond reconstruction error is established; the novelty must be intervention decisions, not just adding a downstream metric. |
| Robust counterfactual explanation surveys and recent uncertainty-aware counterfactual work | Generic counterfactual robustness, uncertainty and stability. | A new stability score or uncertainty plot alone is not sufficient. |

### Sources reviewed

- Morpheus: https://www.nature.com/articles/s41551-025-01357-0
- VirTues article: https://www.nature.com/articles/s41586-026-10884-y
- VirTues code/model information and weight licences: https://github.com/bunnelab/virtues
- Spatium preprint (DOI 10.64898/2026.07.23.740264): https://pmc.ncbi.nlm.nih.gov/articles/PMC13419744/
- CONCERT preprint (DOI 10.1101/2025.11.08.686890): https://pmc.ncbi.nlm.nih.gov/articles/PMC12642540/
- Spatial metabolomics imputation benchmark: https://doi.org/10.1016/j.isci.2026.115203
- spora data/platform documentation: https://spora.epfl.ch/docs/
- BioImage Archive data-licence FAQ: https://www.ebi.ac.uk/bioimage-archive/help-faq/
- BioImage Archive policies: https://www.ebi.ac.uk/bioimage-archive/help-policies/
- spora benchmark licence: https://spora.epfl.ch/docs/bench/licence.html

This was a targeted search, not a systematic review. Search terms, conference proceedings, preprints, supplements and newer releases may reveal additional overlap.

## More precise hypothesis to test

**Primary hypothesis:** In spatial-proteomic cohorts with complete measured marker channels, whole-channel masking and reconstruction can produce acceptable marker-level reconstruction scores while materially changing the *identity or direction* of model-generated counterfactual target recommendations and their model-predicted CD8+ objective on the same held-out patients.

**Potential methodological contribution, only if supported by data:** A validation-calibrated selective recommendation rule that abstains when plausible reconstructions produce unstable signed target sets or unstable predicted uplift. It must be evaluated against simple baselines and must improve a prespecified decision-level metric at a fixed coverage or target budget. This is a hypothesis, not a confirmed novel method.

## Prespecified comparisons

1. Full measured panel (reference output from the same audited evaluator).
2. Observed-marker-only strategy, without reconstructed channel.
3. Simple imputation baseline.
4. Foundation-model reconstruction with complete target-channel masking.
5. Optional second imputer only if its inputs, training exposure and compute are practical.

Keep the patient set, evaluator, target budget, intervention constraints and target-selection threshold identical. Choose thresholds using training/validation data only. Report patient-level signed Jaccard, direction flips, target-set size and empty-set rate, patient-level predicted-uplift agreement, paired model-based reference regret, calibration and selective coverage/risk if abstention is tested. The full-panel output is a *model reference*, not biological ground truth; predicted uplift is not an observed causal treatment effect.

## Data/model exposure and licensing gate

### VirTues weights

The official repository lists:
- `virtues-sp32`: trained on 32 datasets; CC BY-NC 4.0 weights.
- `virtues-sp31`: trained on 31 datasets; MIT-licensed weights.
- `virtues-imc14`: trained on 14 IMC datasets; CC BY-NC 4.0 weights.

The model-weight licence is separate from the code licence and from the licence/terms for each dataset. BioImage Archive states that accessions can carry their own licence; where no licence is stated, its EMBL-EBI Terms of Use apply. Therefore inspect the exact cohort accession and terms instead of assuming either unrestricted use or a restriction. A dataset cannot be called held out merely because a benchmark uses a leave-one-dataset-out evaluation mode: the exact checkpoint and its training cohort list must be verified. The standard `virtues-sp32` checkpoint is not an independent test for any cohort included in its 32 training datasets. Commercial/patent intentions also require careful review of non-commercial weight restrictions and all underlying dataset terms.

### Candidate cohort

`rigamonti2024integrating` remains a *candidate*, not an approved test cohort. The spora catalogue/benchmark advertises CD4/CD8 T-cell labels and VirTues describes a leave-one-dataset-out reconstruction evaluation. Before choosing it, verify:
- the exact image/channel panel and whether the candidate intervention markers are actually measured;
- exact tissue/patient identifiers and that every split is patient-level;
- the exact leave-one-out checkpoint or a model retrained without this cohort;
- no overlap with pretraining/validation/test artifacts used in the selected model;
- dataset-specific reuse, derivative-work, publication and redistribution terms;
- whether there are enough independent patients and variation to support the planned endpoint.

Do not assume the software/platform licence grants rights to every cohort. Do not commit raw data or restricted model weights to this repository.

## Feasibility gates and stop conditions

**Gate 1 — novelty:** Read complete supplements and methods for VirTues, Spatium, CONCERT and Morpheus; search exact terms including “imputation-aware counterfactual”, “counterfactual fidelity”, “virtual staining”, “selective prediction”, “spatial perturbation” and “decision stability”. If a directly equivalent study exists, pivot.

**Gate 2 — permitted, exposed cohort:** Produce a documented marker crosswalk, dataset terms record and checkpoint training-exposure table. Stop if target channels or a meaningful CD8/T-cell endpoint are absent, or exposure cannot be resolved.

**Gate 3 — executable baseline:** Run a small masked-channel smoke test on a permitted subset, recording hashes, versions, hardware, runtime, memory and deviations. Then reproduce Morpheus or document why a scientifically valid surrogate is necessary.

**Gate 4 — meaningful decision impact:** Continue only if virtual reconstruction changes signed recommendations or predicted objectives enough to be measurable and a decision-aware rule adds value beyond reconstruction error and simple baselines. Otherwise report a negative feasibility result or pivot; do not inflate a null result into novelty.

## Current status

- Repository helper tests: 19 passed locally on the available source/test copies (25 October 2026). This is synthetic software validation, not biological evidence or proof that GitHub Actions passed.
- Real cohort downloaded/checksummed: no.
- Exact VirTues checkpoint exposure verified: no.
- Dataset reuse terms cleared: no.
- Morpheus baseline reproduced: no.
- Counterfactual discovery or real-data report run: no.
- Novelty or patentability established: no.
