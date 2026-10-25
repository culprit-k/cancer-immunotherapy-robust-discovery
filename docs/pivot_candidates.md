# Pivot-candidate update: prioritize decision fidelity under marker reconstruction

**Decision (25 October 2026):** generic robustness-only and broad cross-platform-transfer proposals are too crowded to carry a novelty claim on their own. Conditional GO for the specific virtual-marker / counterfactual recommendation-fidelity question, subject to prior-art and dataset gates.

## Ranked candidates

| Candidate | Question | Novelty risk | Feasibility | Decision |
|---|---|---|---|---|
| **1. Counterfactual recommendation fidelity under virtual marker reconstruction** | When whole protein channels are masked and reconstructed, do signed target recommendations and held-out model-predicted CD8 uplift remain faithful to a fully measured reference? Does an abstention rule detect unstable recommendations? | Medium–high risk; combines existing components, but the exact downstream decision-fidelity evaluation may be underexplored. Must search for direct overlap. | Medium only if a suitable public cohort, patient IDs, markers and a compatible baseline are found. | **Investigate first.** |
| 2. Cross-method intervention decision utility | Does a consensus across spatial counterfactual methods beat the best single method at a matched target budget? | High risk because methods output different objects/endpoints and this requires a defensible common scale. | Low–medium. | Defer unless a common test representation is clear. |
| 3. Cross-cohort/platform transfer of signed target direction | Do target directions transfer across independent cohorts and measurement platforms? | High risk; VirTues and related foundation models already cover cross-panel/technology transfer and independent biomarker prediction. | Data compatibility uncertain. | Do not lead with transfer alone. |
| 4. Generic patient-resampling target stability | Does repeated Morpheus discovery produce stable signed target sets? | Very high risk of being incremental. | Useful for reproducibility but compute-intensive and Morpheus supplemental audit is incomplete. | Retain only as a baseline/feasibility exercise. |

## Candidate 1: minimum valid design

- Start from a public spatial-proteomics cohort with fully measured channels that can be intentionally masked.
- Keep patient IDs and all nested cores/tiles/cells together in each split.
- Compare full measurement, observed-only reduced panel, simple imputation, and foundation-model reconstruction.
- Use the same target discovery method and target budget in every condition.
- Calculate both marker reconstruction metrics and downstream signed target-set fidelity, direction flips and held-out-patient model-predicted uplift fidelity.
- If justified by pilot results, test a reliability/abstention rule selected on validation data and report coverage versus recommendation error/regret.

Do not call the fully measured model output biological ground truth. A new algorithm should be proposed only after showing that established methods cannot answer the new decision-level question.

## Data search priority

First examine the current spora data catalogue and dataset terms. Filter by:
1. explicit right to use for research and publication of derived findings;
2. patient/core identifiers;
3. CD8/T-cell label that can be held out as an outcome;
4. enough candidate measured target markers to define a meaningful intervention budget;
5. known foundation-model training exposure, so the evaluation cohort is not accidentally used as a nominally held-out dataset.

The 12-patient anti-PD-1 melanoma spatial-mIF cohort may support a small exploratory external check, but it has only four responders and limited target-marker overlap. The 57-patient GSE300793 bulk RNA-seq cohort is also potentially useful for a pre-specified expression/relapse check, but it is not spatial protein ground truth.

## Stop rules

Stop or pivot if no eligible cohort exists, the model has unavoidable evaluation leakage, the target-discovery baseline cannot be reproduced, direct prior art already measures this exact decision-fidelity problem, or the result adds nothing beyond standard marker reconstruction metrics.
