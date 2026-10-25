# Decision-gate protocol: spatial cancer immunotherapy target discovery

**Status (25 October 2026): NO-GO for the generic robustness-only paper as currently framed. Conditional GO for investigating a more specific comparative or cross-cohort-transfer question. A small Morpheus pilot may still be run for feasibility and familiarity, but not as evidence of novelty.**

## Original idea audited

The initial candidate was a benchmark of complete spatial-proteomic target-set stability under patient-grouped resampling and model seeds, with held-out model-predicted CD8+ infiltration uplift. The idea is useful for reproducibility, but currently too incremental as a standalone novelty claim given:
- Morpheus (2025): spatial-proteomic counterfactual target discovery, patient-level splits, median strategy aggregation, held-out patient testing, and in-vitro validation.
- PHAROS (2026 preprint): target-directed single-cell drug-combination search with sampled batches, controls, and robustness-aware reranking.
- Anzum et al. (MICCAI 2026): counterfactual spatial cell-interaction inference with held-out cores and core-level bootstrap.
- Ding et al. (Biology 2026): spatial counterfactual tissue reprogramming, including melanoma immune-focused intervention hypotheses.

## Gate 0 — Prior-art audit

1. Read the complete Morpheus supplementary PDF and inspect all notebook cells/outputs. Current audit: main article Methods and public source/notebook code were inspected; the separate supplementary PDF was listed but its signed download redirect could not be retrieved in this runtime.
2. Search for intervention consensus, robust counterfactual sets, target-direction transferability, spatial perturbation models, and evaluation of combinations across independent cohorts.
3. Compare candidate questions against Morpheus, PHAROS, the MICCAI 2026 spatial counterfactual interaction paper, SPAD-CFR and other applicable work.
4. Record exact references, methods, endpoints and the distinction between model-predicted change and biological validation.

**Pass:** one narrow gap remains that cannot be described as a routine application of known stability/robustness metrics.  
**Fail/pivot:** an equivalent problem is already addressed or the intended contribution is merely bootstrapping/Jaccard reporting.

## Gate 1 — Dataset and method compatibility

Before choosing a new primary question, build a table with:
- data source/version and reuse terms;
- patient count and hierarchy (patient/core/section/patch/cell);
- modality, markers and intervention directions;
- model output and endpoint;
- available train/validation/test splits;
- ability to evaluate a candidate strategy on untouched patients;
- data license, download requirements, and compute cost.

Do not assume spatial protein, spatial transcriptomic and single-cell perturbation datasets can be pooled. Two methods only count as directly comparable if interventions and endpoints can be evaluated on a common, prespecified representation without post-hoc harmonization to favor one method.

## Gate 2 — Candidate questions to evaluate

### Candidate A: cross-method intervention decision utility
Question: does a prespecified, target-budget-matched consensus across compatible methods have better held-out-patient model-predicted immune uplift than the strongest single-method baseline?

Pass only if at least two methods produce comparable intervention representations and can be evaluated on the same held-out endpoint. Otherwise the comparison is invalid.

### Candidate B: cross-cohort/platform transfer of signed target direction
Question: do signed target directions and predicted effects transfer to an independent cohort/platform with shared markers and a compatible endpoint?

Pass only if target overlap, outcome definition and independent patient sampling are verified before examining results. Cross-cohort prediction in general is already well studied.

### Candidate C: mechanistic admissibility
Question: do prespecified molecular/signalling constraints identify more biologically plausible intervention hypotheses?

Do not lead with this unless a distinct formal gap exists; Morpheus discusses knowledge-graph constraints and recent spatial counterfactual work is biologically informed.

## Gate 3 — Baseline feasibility

Only after prior-art, data-rights and compatibility checks:
1. Obtain a permitted public tutorial/preprocessed artifact.
2. Reproduce a known baseline result.
3. Record environment, checksums, split, endpoint, hardware, runtime, and deviations.
4. If possible, run a small cached-output pilot before full retraining.
5. Label cached-output analysis separately from full pipeline retraining.

The current runtime could not retrieve the dataset archives because of network/name-resolution errors; no model or data run has occurred.

## Statistical and scientific safeguards

- Keep every core/patch from a patient in a single partition.
- Fit normalization, feature filtering and tuning only inside training/validation groups.
- Use untouched patients for final evaluation.
- Weight patients equally after summarizing nested cores/patches.
- Report target budget/size, signed directions, uncertainty and all failed/empty runs.
- A stable prediction is not necessarily correct; model-predicted uplift is not a measured treatment effect, causal finding or clinical utility.

## Decision

**Current decision:** do not publish the robustness-only question as a novelty-led study. First compare Candidate A and Candidate B against recent literature and dataset compatibility. Select one primary question only if a concrete gap remains and a fair evaluation is feasible.
