# Novelty assessment

**Status (25 October 2026): HIGH-RISK / UNVERIFIED. Conditional GO for a small feasibility pilot; NO-GO for claiming novelty or inventing a new algorithm yet.**

## Working candidate

**Patient-level reproducibility of spatial-proteomic counterfactual target combinations.**

Research question: Across patient-grouped resamples and model seeds, how reproducible are spatial-proteomic counterfactual target sets, and does a stability-aware consensus improve held-out-patient model-predicted CD8+ infiltration uplift over a published single-run median-strategy baseline, at a matched target budget?

This is a candidate question, not a validated gap, new algorithm, therapeutic recommendation, or patentability claim.

## What existing methods already cover

### Morpheus (2025)
Morpheus performs spatial-proteomic counterfactual target discovery, patient-level train/validation/test splitting, counterfactual generation at patch level, median aggregation into whole-tumour strategies, in-silico evaluation on held-out patient samples, sparsity sensitivity analyses, and in-vitro testing of selected combinations. It also discusses sample variation, including within a patient. Thus “AI discovers combinations,” “patient-level split,” “evaluate on held-out patients,” or “tumour heterogeneity” cannot be presented as new contributions.

### PHAROS (bioRxiv preprint, September 2026)
PHAROS searches target-directed drug combinations using a pretrained single-cell perturbation model, evaluates combination recovery against independent combinatorial perturbation datasets, compares against controls, and includes multiple sampled batches and robustness-aware re-ranking. It is a preprint and the task/modality differs from Morpheus, but it rules out a broad claim that combination search, multiple sampling, or robust re-ranking is novel by itself.

### Other adjacent methods
- COMPASS (Nature Medicine, 2026): large multi-cohort evaluation and cross-cohort generalization for immunotherapy outcome prediction.
- Jiang et al. (IJCAI 2024): survey of robust counterfactual explanations, including model/input changes and uncertainty dimensions.
- Takefuji (Cancer Letters, 2026 issue / online 2025): stability of feature attribution/selection in oncology.
- Christodoulou and Sun (Expert Systems with Applications, 2026): model uncertainty and counterfactual robustness.

These papers make generic robustness metrics, generic feature stability, cross-cohort prediction, or applying an existing method to cancer alone insufficient as a novelty claim.

## Candidate gap that remains to be tested

The most specific candidate is a hierarchical, patient-level reproducibility benchmark for spatial-proteomic intervention sets that separates:
1. variability caused by which patients/cores enter discovery;
2. variability caused by retraining/model initialization;
3. instability of each signed molecular target versus the full target combination;
4. the relationship between these reliability measures and held-out-patient model-predicted uplift at a matched target budget.

The main Morpheus article/code inspected so far appears to use fixed seeded splits and reports aggregation and held-out evaluation; we did not find a repeat-the-entire-pipeline resampling benchmark in the inspected sources. However, the separate supplement has not yet been read, and the broader literature search is not exhaustive. The gap is therefore not confirmed.

## What would not be novel on its own

- Applying AI to cancer or immunotherapy.
- Counterfactual generation or target-combination search.
- A patient-level split or held-out cohort.
- A bootstrap or a Jaccard score by itself.
- Stability selection or consensus ranking without a distinct scientific payoff.
- A dashboard/reporting framework without methodological insight.
- Claims that a stable model prediction is causal, biologically true, clinically useful, or patentable.

## Decision

**Current decision: refine and run a controlled feasibility pilot only.**

### Proceed to a full study only if
- The supplement and targeted prior-art search do not reveal an equivalent patient/core-level spatial combination robustness analysis.
- The published baseline can be reproduced or deviations are sufficiently understood.
- Patient identifiers, target marker definitions, directions and permitted data reuse are verified.
- The test can distinguish sample-sampling variability from model-seed variability without patient leakage.
- There is a predeclared baseline and evidence that the analysis changes a decision or result beyond a generic stability score.

### Pivot if
- Equivalent combination-stability analysis already exists.
- The dataset cannot support patient-level evaluation or has unclear use rights.
- The study can only report stability without independent held-out evaluation.
- The added analysis does not change conclusions relative to existing baselines.

## Intellectual-property caution

The project repository is public. Public disclosure can affect patent options depending on jurisdiction and facts. No patentability conclusion is made; if a genuinely distinct invention emerges, consult the institution's technology-transfer office or a qualified patent professional before disclosing enabling technical details.
