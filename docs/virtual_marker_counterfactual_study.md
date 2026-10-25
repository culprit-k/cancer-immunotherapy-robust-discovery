# Candidate study protocol: Counterfactual Recommendation Fidelity Under Virtual Marker Reconstruction

**Status (25 October 2026): candidate gap for targeted prior-art review and a feasibility pilot. Not a confirmed novelty claim, new algorithm, clinical validation, or patentability conclusion.**

## Working title

**What Happens When a Marker Is Missing? Counterfactual Target Discovery Under Virtual Staining in Spatial Immuno-oncology**

Alternative technical title: *Recommendation fidelity of spatial-proteomic counterfactual target discovery under whole-channel masking and foundation-model reconstruction.*

## Why this candidate replaces the generic robustness paper

The original proposal—repeat Morpheus with patient resampling and report target-set Jaccard—is too incremental on its own. The current literature already includes:
- **Morpheus (2025):** spatial-proteomic counterfactual target discovery, aggregation, held-out-patient evaluation and selected in-vitro validation.
- **SPAD-CFR (Biology, 2026):** generative spatial counterfactual tissue reprogramming.
- **Celcomen (ICLR 2025; related peer-reviewed publication in 2026):** spatial causal disentanglement and counterfactual perturbation modeling.
- **VirTues (Nature, 2026):** spatial-proteomics foundation model with marker reconstruction/virtual staining, cross-panel and cross-technology transfer, tissue-level biomarker discovery and response prediction.
- **Spatium (2026):** protein-language foundation modeling and reconstruction of missing spatial proteins.
- **TISSUE and related imputation work:** uncertainty-calibrated spatial expression reconstruction and evaluation of downstream analysis consequences.

These contributions make generic spatial counterfactual modeling, virtual staining, cross-panel transfer, imputation quality, or ordinary stability metrics insufficient novelty claims.

## Proposed gap to test

Existing work evaluates marker reconstruction and downstream tasks, while spatial counterfactual methods generate intervention hypotheses. The targeted question is whether reconstruction quality adequately predicts **downstream intervention-decision fidelity** when one or more entire marker channels are absent.

A reconstruction can have reasonable pixel/cell-level correlation yet alter which signed marker set the counterfactual optimizer recommends. We have not established from a full systematic review that this gap is unaddressed; this is a specific candidate for verification, not a claim of priority.

## Primary research question

When complete spatial-proteomic marker channels are masked and reconstructed by a foundation model, do counterfactual target-set recommendations and their held-out-patient model-predicted CD8+ infiltration changes remain faithful to the recommendations obtained from fully measured channels?

Secondary question: Can a prespecified reliability/abstention rule, calibrated using held-out measured markers, identify recommendations whose direction or predicted uplift changes materially under plausible marker reconstructions?

## Hypotheses

- **H1:** Marker reconstruction accuracy and downstream recommendation fidelity are not interchangeable; similar reconstruction error can accompany different signed intervention sets.
- **H2:** Whole-channel masking and realistic cross-panel missingness alter recommendations more than cell-wise random masking at comparable missing fractions.
- **H3:** A reliability rule using repeated reconstruction/model runs and target-set agreement can identify a subset of recommendations with lower measured-panel reference regret than a single-imputation recommendation, at a reported coverage cost.

These are falsifiable hypotheses. Do not assume they will be supported.

## Core design

### Unit and data

Use public spatial-proteomics datasets with:
1. genuine measured channels that can be hidden for retrospective validation;
2. cell/patch/core identifiers and patient IDs, or enough metadata to verify the grouping;
3. a measurable CD8/T-cell outcome or a defensible cell-state label;
4. at least several candidate perturbation markers with consistent identities and meaningful interpretation;
5. explicit reuse terms compatible with the planned analysis.

The spora dataset collection currently describes 35 cohorts, 5,477 patients and five imaging technologies. VirTues' own paper reports a 32-cohort, multi-technology corpus and notes that the Morpheus/Wang dataset is not redistributable in its harmonized corpus due to licensing restrictions. These are different counts and scopes; do not treat them as the same inventory.

Do **not** choose the main cohort until actual channel, patient and license metadata are audited. Do not use a dataset that the foundation-model weights already saw for a nominally independent generalization result unless the split is redesigned to avoid that leakage.

### Reference and comparison conditions

For each eligible cohort, create patient-grouped outer folds before preprocessing or discovery. On training patients, run the same target-discovery pipeline in the following conditions:

A. **Measured-channel reference:** all selected target/input markers are measured. This is a reference model output, not biological ground truth.

B. **Masked-panel baseline:** remove whole channels and run a model restricted to the observed panel, without imputing the missing channels.

C. **Simple reconstruction baseline:** use an uncomplicated, documented baseline supported by the data shape (for example, training-set median or marker-correlation regression). Do not assume a specific baseline is suitable until the pilot.

D. **Foundation-model reconstruction:** reconstruct the masked channels using VirTues or another selected model, without using held-out patients to fit or tune the imputation or counterfactual pipeline.

E. **Optional second imputation model:** include only if its access terms, compute and input/output interfaces are manageable. Spatium is an adjacent candidate, but adding it is not required for the first feasibility gate.

Emulate both:
- **whole-channel masking**, which mimics a real assay panel missing a marker;
- **cross-panel masking**, where the held-out set of removed channels approximates a second observed panel;
- optional **cell-wise masking** only as a diagnostic, not the principal real-world missing-panel simulation.

The exact masking rate must be selected from actual observed panel overlap before performance results are inspected.

### Target-discovery stage

Use a published, auditable baseline such as Morpheus-style CD8+ infiltration prediction and counterfactual generation, but first verify that the selected cohort format can be transformed into its required inputs and that its licensing permits reuse.

If the full Morpheus pipeline cannot be fairly reproduced, report that limitation and define a smaller, clearly named surrogate baseline. Do not describe a surrogate as a reproduction of Morpheus.

Keep the candidate intervention representation consistent across conditions: marker name, signed direction (increase/decrease), and target budget. Exclude the CD8 label channel from predictor inputs to avoid direct label leakage. Normalize marker aliases before comparison.

### Held-out evaluation

For every outer split:
1. derive target sets only from training patients;
2. select any thresholds/reliability cutoffs only within inner patient-grouped validation;
3. apply each strategy to the exact same untouched patients;
4. where possible, evaluate input variants against the fully measured reference data on the held-out patients;
5. average patch/core-level predictions within patient first, then give each patient equal weight;
6. keep a full record of empty sets, failed runs and model-seed variability.

Since no observed intervention outcome is available from static spatial images, predicted changes must be called **model-predicted uplift**. Agreement with the fully measured model is not proof of causal correctness or therapeutic efficacy.

## Prespecified outcomes

### Marker reconstruction
- Per-marker MAE and RMSE.
- Pearson and Spearman correlation, computed on held-out cells/locations.
- Error stratified by marker, panel, cohort, abundance and masking type when there are enough data.

### Recommendation fidelity (primary)
- Signed target-set Jaccard similarity versus the fully measured reference.
- Signed precision and recall.
- Target direction-flip rate among markers chosen by both conditions.
- Set size, target budget, and frequency of empty recommendations.

### Predicted-uplift fidelity (co-primary or key secondary, settle before test)
- Patient-level MAE/RMSE of reconstructed-panel versus measured-panel predicted uplift.
- Pearson/Spearman agreement and sign concordance of patient-level predicted uplift.
- Model-based decision regret: the difference between held-out predicted uplift for the strategy selected from reconstructed input and the reference strategy selected from fully measured input, under the same target budget. This is **reference-model regret**, not observed therapeutic regret.

### Reliability/abstention rule (only if H1/H2 support a real issue)
- Compute recommendation agreement across reconstruction perturbations/model seeds using training/validation only.
- Specify a rule that abstains or flags low-confidence recommendations rather than silently presenting them as reliable.
- Plot coverage versus target-set error and predicted-uplift regret on outer test patients.
- Compare with simple alternatives: single imputation, simple reconstruction, and selection frequency only.
- Choose reliability cutoffs on validation data; never optimize on outer test outcomes.

A useful primary contribution must show more than a new name for Jaccard: it must demonstrate how marker reconstruction changes an intervention decision and whether an evaluation/abstention rule improves reliability at a transparent coverage cost.

## Statistical safeguards

- Patient is the primary independent unit; cores/tiles/cells are nested observations.
- Keep all sections/cores/tiles from one patient in a single split.
- Resample patients, not cells, for confidence intervals of patient-level outcomes.
- Use paired comparison across conditions on the same outer-held-out patients.
- Report each cohort separately before any pooled summary; use a prespecified meta-analytic/stratified summary only if endpoints are compatible.
- Correct for multiple target-level hypothesis tests if target-level associations are analyzed.
- Do not infer causal intervention effects from observational marker correlations.
- Do not claim external clinical validation from a model output alone.

## Candidate data sources to audit

1. **spora [data] / VirTues:** public harmonized spatial-proteomics data across several cohorts and technologies; use the dataset browser and its precise dataset-level terms. Source: https://spora.epfl.ch/docs/index.html
2. **VirTues code and pretrained models:** https://github.com/bunnelab/virtues. It includes masked-channel reconstruction demos and model weights. Model weights have separate CC BY-NC 4.0 and MIT-licensed variants; follow each model/data license.
3. **Pybus et al. anti-PD-1 melanoma spatial mIF cohort:** 12 stage-IV patients, 14 protein markers across lymphoid/myeloid panels, 8 million-plus cells, public feature/analysis data at https://doi.org/10.5281/zenodo.16898362 and code at https://github.com/goeckslab/Melanoma-ICB-mIF. This is a small external clinical cohort; use only if marker overlap and data layout support the question, and treat clinical analysis as exploratory.
4. **GSE300793/GSE300445:** study reports 57 pre-treatment stage-III melanoma bulk RNA-seq samples and four Visium spatial tumors in the related study. Source: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300793 and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300445. This is not an interchangeable spatial-proteomics validation set; any use is secondary and requires modality-aware gene/protein interpretation.
5. **Morpheus melanoma dataset:** closest baseline, but the original data rights need specific verification and VirTues reports licensing restrictions on redistributing the Wang et al. dataset. Do not put restricted raw data into this public repository.

## Go/no-go criteria

### Proceed to a full study only if
- a focused prior-art search does not find an equivalent counterfactual recommendation-fidelity benchmark;
- at least one openly usable cohort has the needed measured markers, patient IDs and cell-level outcome;
- the foundation model's relationship to the evaluation cohort is known (training overlap is explicitly handled);
- the published/surrogate target-discovery baseline runs reliably on a small subset;
- the pipeline makes a decision-level comparison, not just reporting marker RMSE.

### Refine or pivot if
- the marker channels needed for target discovery are unavailable or not licensable;
- the imputer was trained on the evaluation cohort and no leakage-safe route is feasible;
- target-set results depend entirely on a model-predicted endpoint with no meaningful held-out assessment;
- no result changes the conclusion beyond existing imputation and robustness metrics;
- existing literature already reports the same downstream intervention-fidelity analysis.

## Status of actual execution

No new spatial dataset was downloaded, no VirTues/SPAD-CFR/Morpheus checkpoint was executed and no biological result has been measured in this project. The protocol and analysis helpers are design/preparation work only. The next concrete gate is dataset/channel/license inspection followed by a small, reproducible smoke test.


## Reproducible evaluation handoff

The repository now includes a post-hoc report builder at analysis/panel_shift_report.py. It does not train a model or perform imputation; it evaluates tables from a separately executed pipeline.

### Required derived files for each outer patient-held-out fold

1. **reconstruction.csv**: one row per held-out patient / cell or location / marker, with columns patient_id, marker, measured, reconstructed. The report computes per-patient marker errors first and macro-averages across patients; pooled-cell metrics are secondary only.
2. **heldout_predictions.csv**: columns patient_id, strategy, predicted_before, predicted_after. Each strategy must be evaluated on the same fully measured held-out patients using the same frozen evaluator. Rows may correspond to nested tiles/cores; the report averages uplift within patient before comparison.
3. **target_sets.json**: two strategy maps, reference and reconstructed, each mapping marker name to signed direction (1 for proposed increase; -1 for proposed decrease). The sets must have been generated without using the outer held-out patients.

Then run:

    python -m analysis.panel_shift_report \
      --reconstruction-csv data/derived/reconstruction.csv \
      --predictions-csv data/derived/heldout_predictions.csv \
      --target-sets-json data/derived/target_sets.json \
      --output-json reports/panel_shift_fidelity.json

Run the report independently per outer fold and summarize fold-level outcomes using a prespecified paired analysis. Do not concatenate patient sets that overlap between folds as if they were independent observations. The script's "reference regret" is the paired difference in model-predicted uplift, not an observed intervention or clinical effect.

The helper expects clean, held-out data already exported by the model pipeline. It cannot establish whether data leakage occurred; the analyst must enforce and document patient splits before producing these tables.


## Preferred dataset sequence after the catalogue audit

1. **First-choice candidate for the held-out recommendation-fidelity evaluation: rigamonti2024integrating.** The spora catalogue lists 108 patients and 158 IMC images, paired with H&E, and the spora-bench cell-annotation configuration includes CD4 T-cell and CD8 T-cell labels. The VirTues paper reports a leave-one-dataset-out, zero-shot marker-reconstruction evaluation on the Rigamonti et al. cohort. This gives a plausible route for evaluating downstream recommendation fidelity on a cohort not seen by the corresponding leave-one-out reconstruction model. This depends on using the correct leave-one-dataset-out checkpoint (or reproducing that training exclusion), verifying target marker channels, and confirming dataset/model permissions.
2. **Biological development cohort: hoch2022multiplexed.** This melanoma IMC cohort has 35 patients and 50 images and is based on a chemokine-milieu study of immunotherapy response. It is directly relevant to chemokines and immune infiltration, but VirTues already evaluates cell phenotyping on Hoch and its training exposure must be handled explicitly. It is not an unseen-cohort test for the standard full VirTues model by default.
3. **Small pipeline smoke test: allam2022spatially.** This lung IMC cohort has 26 patients and 26 images and is advertised by spora as approximately 500 MB. Use it only to validate loading, patient grouping and channel masking until the required target markers and T-cell labels are confirmed.
4. **Later alternatives:** moldoveanu2022spatially and xiao2022multiplexed, subject to the same checks.

Do not treat a paper's leave-one-dataset-out experiment as proof that a released default checkpoint was trained without that dataset. The exact checkpoint file and its recorded training cohort list must match the evaluation claim.
