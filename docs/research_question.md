# Research question and scope

## Working title

**Patient-Level Reproducibility of Spatial-Proteomic Counterfactual Target Combinations for Cancer Immunotherapy**

Possible paper subtitle: *Separating patient-sampling and model-seed variability in predicted interventions for CD8+ T-cell infiltration.*

## Primary question

Across patient-grouped resamples and model seeds, how reproducible are spatial-proteomic counterfactual target sets, and does a prespecified stability-aware consensus improve held-out-patient model-predicted CD8+ infiltration uplift over a reproduced published median-strategy baseline at a matched target budget?

## Hypothesis to test

The proposed target sets may vary due to two distinct sources: which patients/cores enter the discovery sample and which model seed/retraining run is used. A patient/core-hierarchical reproducibility analysis may characterize those sources separately and test whether the stability information is associated with more consistent predicted uplift on untouched patients.

This is an unverified hypothesis, not proof of a literature gap.

## Why this is not just “new AI for cancer”

Morpheus already proposes spatial-proteomic counterfactual perturbations, median-aggregates them into whole-tumour strategies, evaluates strategies in silico on held-out patients, and reports selected in-vitro experiments. PHAROS, a 2026 preprint, already searches for target-directed combinations using a single-cell perturbation model and includes robustness-aware re-ranking. General combination discovery and a generic stability metric are therefore not sufficient novelty claims.

The candidate distinction—if confirmed by the complete supplementary material and expanded prior art—is a spatial patient/core-hierarchical benchmark that separately varies patient sampling and model retraining, evaluates full signed intervention-set stability, and relates it to held-out-patient model-predicted uplift.

## Scope

- Computational hypothesis generation and reproducibility evaluation.
- Spatial-protein / imaging mass cytometry setting, initially the Morpheus melanoma cohort if licensing permits.
- Patient is the inferential unit; cores and patches are nested observations.
- Compare the published method with prespecified baselines under equal target budgets.
- Separate model-seed variability from patient-sampling variability.
- Evaluate on untouched patients; use an external cohort only if markers, endpoints, identifiers and reuse terms are compatible.

## Out of scope

- Patient-specific treatment advice.
- Claims of target causality or treatment efficacy based on model predictions alone.
- Claims of novelty before full prior-art and supplementary-material audit.
- Patentability conclusions.

## Key definitions

- **Signed target:** molecular marker plus proposed increase/decrease direction.
- **Selection stability:** frequency of a signed target across repeated discovery runs.
- **Combination stability:** overlap/consistency of complete signed target sets.
- **Patient-level predicted uplift:** predicted after-minus-before change summarized within each patient, without treating patches as independent patients.
- **Model-seed variability:** variation across independently initialized/retrained models under an otherwise fixed design.
- **Biological validity:** independent empirical evidence for the predicted perturbation; not implied by stability.
- **External generalization:** evaluation in independent patients/cohorts never used in discovery or model selection.

## Decision gate

Do not build a purportedly novel algorithm until (1) the full Morpheus supplement and targeted prior art are examined, (2) data rights and patient identifiers are verified, (3) a baseline is reproduced, and (4) a pilot demonstrates that a prespecified, leakage-safe patient-level evaluation is technically feasible and adds information beyond established baselines.
