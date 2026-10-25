# Preliminary analysis plan

**Status (25 October 2026): prespecified feasibility plan; conditional GO for a pilot only. Full study depends on prior-art, license, and baseline reproduction gates.**

## Objective

Evaluate whether variation in patient/core sampling and variation in model seeds/retraining change the complete signed molecular target sets proposed by spatial-proteomic counterfactual discovery, and whether a stability-aware consensus has better held-out-patient model-predicted CD8+ infiltration uplift than the reproduced published strategy at a matched target budget.

This is not a clinical treatment study. Predicted counterfactual change is not observed therapeutic effect or causal evidence.

## Stage 0 — Literature, permissions and reproduction
- Read the complete Morpheus supplement and expand the prior-art search (robust counterfactual sets, stability selection, intervention set stability, patient/core resampling, model-seed variability).
- Verify license/terms for the exact data and source-code artifacts.
- Reproduce at least one published Morpheus baseline result from an authorized public tutorial/preprocessed artifact.
- Record version, checksum, environment, patient split, preprocessing, thresholding and compute time.
- Do not invent a new algorithm before these gates pass.

## Stage 1 — Small feasibility pilot
- Prefer the 69-patient melanoma cohort (159 cores; 39 channels), treating patient as the independent unit.
- First validate patient/core/patch identifiers, target direction mapping, and aggregation.
- If permitted cached perturbations exist, re-aggregate across patient-grouped resamples as a cached-output descriptive pilot. Do not call this full pipeline robustness because the model is not retrained.
- Measure per-patch counterfactual cost before attempting repeated full discovery.
- Continue only when the endpoint, data terms and evaluation path are reproducible.

## Stage 2 — Leakage-safe study design
- Establish outer held-out patient folds before discovery. Keep all sections/cores/patches of a patient together.
- Use only inner grouped validation to select thresholds, preprocessing choices and other hyperparameters.
- Repeat patient-grouped training resamples and independently vary model initialization/seeds within each outer training fold.
- Never choose target sets or tune configurations using outer test patients.
- Prespecify run count/seed schedule after timing the pilot. Aim for at least 30 successful discovery runs per outer split if feasible; report fewer-run studies as exploratory and justify precision limits.
- Record failed runs; do not silently discard runs that yield empty/poor target sets.

## Stage 3 — Metrics
### Discovery stability
- Signed-target selection frequency.
- Direction consistency conditional on target selection.
- Pairwise Jaccard of complete signed target sets.
- Target set size/sparsity and proportion of empty sets.
- Separate effects of patient resampling versus model seeds.

### Held-out model-predicted uplift
- Apply each prespecified strategy to the same held-out patients.
- Calculate patch/core predicted changes, summarize within patient using the predeclared paper-compatible rule, then weight patients equally.
- Report mean, median, 10th percentile, fraction of patients with positive predicted change, and patient-level bootstrap confidence intervals.
- Report any target-budget differences and avoid selecting the best-performing seed after viewing test results.

A high stability score alone does not imply accuracy; stability metrics must be evaluated alongside held-out predicted uplift and target set size.

## Stage 4 — Baselines and controls
- Reproduced Morpheus single-run/published median-strategy baseline.
- Simple target-frequency/rank consensus built from discovery runs.
- Matched target-budget random/signed perturbation control when valid.
- No-change reference.

Finalize the exact strategy-generation and target-budget rules before inspecting outer-fold performance. If a baseline cannot be implemented fairly, document why instead of overstating results.

## Stage 5 — Statistical reporting
- Treat patient as the unit for uncertainty estimates; do not bootstrap patches as independent units.
- Report point estimates plus confidence intervals/distributions, fold/run-level results and all predeclared metrics.
- Separate patient-sampling uncertainty, model-seed variability, external-cohort generalization and biological validation.
- Report negative or null findings. Do not label a computational prediction as causal, experimentally validated, therapeutically effective or clinically useful without independent evidence.

## Decision gates
- Proceed: full supplement/prior-art audit leaves a specific gap; rights are clear; baseline is reproduced; pilot validates data and patient-level endpoint; compute supports the protocol.
- Refine: stability metrics are useful but add little beyond existing methods, or full retraining is too costly while cached outputs remain suitable for an explicitly exploratory reanalysis.
- Pivot: equivalent methods already exist, data rights/metadata are inadequate, or the scientific endpoint cannot be evaluated without leakage.
