# Mathematical candidate screen before architecture freeze
**Date:** 2026-10-26. **Status:** hypothesis screen; no candidate is validated or locked.

## Why screen candidates now
The study has a small HCC ICI cohort (42 patients and five PR/binary-positive cases in the corrected table). A large supervised architecture trained on these labels would be underpowered. A genuinely complex method needs stronger independent spatial data and a synthetic benchmark, not just more layers.

## Three candidate families

### Candidate A — Uncertainty-calibrated panel transport
**Goal:** produce patient/ROI representations that remain interpretable when marker panels differ or channels are absent, and explicitly quantify out-of-domain uncertainty.

**Possible mathematical core:** learn a representation constrained by marker identity and spatial context; evaluate cross-panel reconstruction/representation consistency; calibrate prediction sets or abstention using held-out calibration data; penalize instability under predeclared marker-dropout transformations.

**Potential distinction:** uncertainty and stability are first-class outputs, not a decorative post-hoc score.

**Overlap / risk:** VirTues already uses marker-aware representations and cross-panel transfer. Conformal prediction, dropout robustness and domain adaptation are established techniques. A new architecture alone will not establish novelty. The claim must isolate a genuinely new objective or property and outperform VirTues/simple baselines.

**Data needed:** eligible source-scale or explicitly adapted images, marker maps, multiple panels/cohorts and true held-out patients/datasets.

### Candidate B — Hierarchical spatial interaction sensitivity
**Goal:** distinguish stable patient-level spatial interaction patterns from ROI sampling noise and rank candidate interactions for follow-up.

**Possible mathematical core:** a hierarchical model for cell/ROI/patient variation plus a graph-based sensitivity score with uncertainty, calibrated under synthetic nulls and spatial confounding.

**Potential distinction:** target hypotheses depend on interaction stability across ROIs/patients, not only feature attribution from one fitted model.

**Overlap / risk:** spatial graphs, neighbourhood analyses and explainability are established; sensitivity ranking is not causal evidence. The current 42-patient data cannot identify causal effects without intervention assumptions/data. Treat output as a hypothesis ranking only.

**Data needed:** validated cell masks, marker semantics, multiple ROIs per patient, independent cohorts, negative controls and ideally perturbation evidence.

### Candidate C — Cross-modal mechanistic evidence graph
**Goal:** rank target hypotheses only when spatial evidence triangulates with independent pathway, single-cell/spatial transcriptomic, and perturbational evidence.

**Possible mathematical core:** a provenance-aware evidence graph with modality-specific likelihoods, conflict handling, missing-evidence penalties and calibrated evidence aggregation.

**Potential distinction:** explicit handling of evidence dependence and contradiction, not simply concatenating all modalities into one predictor.

**Overlap / risk:** biomedical knowledge graphs and multi-omic integration are established. Double-counting evidence and publication bias are major risks. This candidate needs additional source datasets and a principled dependence model; it cannot be executed from the current image audit alone.

## Preliminary recommendation
Treat Candidate A as the first technical research candidate because it can be tested without pretending observational HCC outcomes establish causal targets. Keep B as a later mechanistic hypothesis module and C as a longer-term target-evidence layer. This is a sequencing recommendation, not a novelty claim or final algorithm decision.

## Candidate selection gate
Before implementation, give each candidate a preregistered specification containing: formal estimand, notation, assumptions, objective function, computational complexity, required data, strongest baseline, synthetic ground-truth tests, leakage tests, uncertainty calibration, ablation plan, and a kill criterion. Test on synthetic scenarios first. Reject any novelty statement that cannot be clearly separated from a baseline and disproven by data.

## Minimum mathematical standards
- Identify exactly which output is estimated and at what unit.
- Make assumptions explicit and show where parameters are not identifiable from observational data.
- Distinguish predictive attribution from intervention effects.
- Demonstrate calibration under distribution shift or emit an abstention result.
- Use ablations to show every extra term contributes measurable value.
- Prefer a lower-complexity model if the proposed one does not improve a preregistered measure.
