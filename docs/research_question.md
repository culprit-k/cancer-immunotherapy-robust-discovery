# Research question and scope

## Current research candidate

**What Happens When a Marker Is Missing? Counterfactual Target Discovery Under Virtual Staining in Spatial Immuno-oncology**

This is a provisional candidate for a focused benchmark study. It is not a confirmed literature gap or a claim that a new algorithm has been invented.

## Primary question

When one or more complete protein-marker channels are missing from spatial-proteomics panels and reconstructed by a foundation model, do the resulting signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes remain faithful to those obtained from fully measured channels?

## Secondary question

Can a prespecified reliability/abstention rule, calibrated using held-out measured markers, flag recommendations whose signed direction or model-predicted uplift changes materially under plausible marker reconstructions?

## Why this replaces the previous proposal

The generic patient-resampling/Jaccard study is too incremental as a high-novelty contribution. Existing work includes:
- Morpheus for spatial-proteomic counterfactual target discovery and held-out-patient evaluation.
- SPAD-CFR and Celcomen for spatial generative/counterfactual perturbation modeling.
- VirTues and Spatium for spatial-protein foundation modeling and reconstruction of missing channels.
- Spora benchmarks for virtual staining, cross-cohort and tissue-level evaluation.
- TISSUE and other imputation studies for uncertainty-aware reconstruction and downstream consequences.

VirTues already evaluates whether reconstructed marker channels preserve downstream cell phenotyping under marker masking. Therefore the narrower candidate is specifically the **counterfactual intervention-decision consequence** of virtual marker reconstruction: whether the signed target set changes and whether the target set's held-out model-predicted objective changes, not simply whether reconstructed markers or cell phenotypes are accurate.

This distinction is plausible but not yet confirmed by an exhaustive prior-art review.

## Hypotheses to test

1. Marker reconstruction accuracy and counterfactual recommendation fidelity may diverge: similar marker-level errors may lead to different signed target sets.
2. Whole-channel masking, which mimics real assay-panel differences, may distort recommendations more than cell-wise random masking at comparable missing fractions.
3. A validation-calibrated reliability/abstention rule may identify recommendations with lower disagreement or lower model-based reference regret, at the cost of reduced recommendation coverage.

No result is assumed in advance.

## Study scope

- Spatial-proteomics panel missingness and virtual staining.
- A published and reproducible counterfactual target-discovery baseline (Morpheus-style if compatible, or a clearly labelled surrogate if the original implementation cannot be fairly reproduced).
- Candidate data from the public spora collection or another cohort with explicit terms and required markers.
- Patient/core-grouped split and evaluation; cells/tiles are nested measurements, not independent patients.
- Full measured-channel reference, no-imputation baseline, simple imputation baseline, and foundation-model reconstruction condition.
- Secondary clinical response datasets only if marker overlap and endpoint interpretation support a fair exploratory analysis.

## Primary measures

- Signed target-set Jaccard similarity between the full-measurement reference and reconstructed-panel strategy.
- Signed precision/recall and direction-flip rate.
- Difference in held-out patient-level model-predicted CD8+ infiltration uplift.
- Marker-level MAE/RMSE/correlation as secondary measures.
- Optional coverage-versus-error/regret curve for an abstention rule.

All uplift is model-predicted unless independently measured in an intervention experiment. Agreement with a full-measurement model is not a known biological ground truth.

## Data and implementation gates

1. Read the full prior art on VirTues, Spatium, Spora, Celcomen, SPAD-CFR, Morpheus and counterfactual robustness.
2. Audit rigamonti2024integrating first as a potential held-out cohort (spora lists 108 patients / 158 IMC images and CD8 T-cell annotation), but verify panel target suitability, exact data terms and use of a VirTues checkpoint trained without the cohort. Audit hoch2022multiplexed as a biologically relevant development cohort, with explicit handling of possible VirTues exposure.
3. Confirm whether any foundation model was trained on the selected cohort; use a documented holdout or leave-one-dataset-out setup to avoid data leakage.
4. Reproduce a small baseline and one masked-marker reconstruction example before developing the full benchmark.
5. Decide if a genuine contribution remains after testing the pipeline against prior methods.

## Out of scope

- Claims of clinical treatment efficacy or causal target validation from observed marker associations.
- Direct pooling of spatial protein profiles and bulk RNA-seq.
- Reuse or redistribution of data without verified permission.
- Claims of novelty, patentability, or clinical utility before evidence.

## Decision

**Conditional GO for a feasibility pilot. No-go for claiming novelty until exact downstream intervention-recommendation fidelity is searched and a permitted dataset can support the test.**
