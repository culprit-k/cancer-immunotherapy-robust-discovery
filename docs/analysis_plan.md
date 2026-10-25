# Preliminary analysis plan

**Status:** Draft for feasibility planning. Final metrics and thresholds must be chosen before inspecting final evaluation results.

## Objective

Determine whether predicted target combinations are sensitive to patient sampling and reasonable modelling choices, and assess whether an explicit robustness analysis adds information beyond a reproduced baseline.

## Stage 0 — Reproducibility
- Record environment and data versions.
- Follow the published implementation and preprocessing.
- Reproduce at least one primary baseline result before modifying the method.
- Record deviations and unresolved discrepancies.

## Stage 1 — Patient-level resampling
- Repeat the target-discovery process on patient-level bootstrap or repeated subsamples.
- Keep all spatial samples belonging to the same patient together.
- Use fixed, documented random seeds.
- Do not tune procedures based on the final held-out results.

## Stage 2 — Candidate metrics
Subject to the dataset and baseline implementation:
- Per-target selection frequency.
- Pairwise Jaccard similarity between recommended target sets.
- Mean pairwise combination overlap across runs.
- Distribution of predicted objective change, not only the best score.
- Sensitivity to prespecified modelling configurations.
- Held-out patient prediction metrics appropriate to the endpoint, with uncertainty intervals.

The exact metrics should reflect the scientific question and avoid rewarding trivial or overly large combinations.

## Stage 3 — Baselines
Potential comparisons include:
- Published method without added robustness analysis.
- Simple frequency/rank aggregation across resamples.
- Relevant established stability-selection or uncertainty baselines, if applicable.
- A no-skill or simple reference where the outcome supports one.

The baseline set must be finalized after the literature and code audit.

## Stage 4 — Evaluation safeguards
- Separate model selection from final evaluation.
- Use patient-grouped splits.
- Report cohort size and class/endpoint imbalance.
- Report confidence intervals or distributions, not just point estimates.
- Perform sensitivity analyses only when scientifically justified and documented.
- Treat exploratory analyses as exploratory.

## Interpretation limits
Stable predictions can still be wrong. Spatial correlation and observational data do not establish that changing a target will cause increased T-cell infiltration. Computational results are hypothesis-generating and do not establish therapeutic efficacy or clinical utility.
