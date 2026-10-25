# Decision-gate protocol: spatial cancer immunotherapy target-set reproducibility

**Status (25 October 2026): conditional GO for a narrow feasibility pilot; NO-GO for claiming novelty or inventing a new algorithm until the prior-art and reproduction gates pass.**

## Working title

**Patient-level reproducibility of spatial-proteomic counterfactual target combinations for predicted CD8+ T-cell infiltration**

This is a research question, not a confirmed novelty claim or therapeutic recommendation.

## Primary question

Across patient-grouped resamples and model random seeds, how reproducible are spatial-proteomic counterfactual target sets, and does a prespecified stability-aware consensus improve held-out-patient **model-predicted** CD8+ infiltration uplift over the published single-run median-strategy baseline at a matched target budget?

## Why the question is deliberately narrow

Morpheus already performs patient-level train/validation/test splitting, generates counterfactual perturbations, aggregates perturbations within patients and across patients, evaluates strategies in silico on test patients, and experimentally validates selected combinations. PHAROS (a 2026 preprint) searches drug combinations and includes sampled source/target groups and robust re-ranking. Therefore, general counterfactual discovery, combinations, patient-level validation, or generic resampling are not claimed as new. The possible candidate gap is the *hierarchical, patient-level reproducibility benchmark for spatial intervention sets*, if full supplement and broader prior-art searches confirm it.

## Gate 0 — Prior-art and baseline integrity

Before implementing a new method:

1. Read the complete Morpheus supplementary PDF and inspect all relevant notebook cells/outputs. Current audit: the main article Methods and public source/notebook code were inspected; the separate supplementary PDF was located but its content could not be retrieved in this runtime.
2. Search for prior methods covering robust counterfactual sets, intervention selection stability, repeated model retraining, patient/core hierarchical resampling, and uncertainty-aware spatial perturbations.
3. Record exact version/commit, article data sources, environment, preprocessing, split and optimization settings.
4. Reproduce at least one published result from the public tutorial bundle or authorized preprocessed artifacts before modifying the pipeline.
5. Resolve all data/repository usage terms before redistributing or relying on materials with unclear licensing.

**Pass:** a documented gap remains, and a published baseline can be reproduced or all reproduction deviations are characterized.  
**Fail/pivot:** an equivalent patient/core-level spatial combination stability analysis already exists, or the baseline cannot be reproduced well enough to assess added value.

## Gate 1 — Data and compute feasibility

Preferred cohort: Morpheus melanoma spatial-proteomics cohort (reported 159 cores from 69 patients). Count patients as the independent units; cores and patches are nested observations, not independent replicates.

First pilot:
- Use the published preprocessed data, saved split/model, and perturbations if licensing/access permit.
- Test data parsing, patient/core identifiers, marker definitions, perturbation directions, and model-prediction evaluation on a very small subset.
- Re-aggregate existing counterfactual outputs across patient resamples as a descriptive pilot. Clearly label this as **cached-output resampling**, not repeated full-pipeline robustness.
- Measure memory, runtime per patch/core, GPU/CPU needs, and whether a full repeat is feasible before requesting or downloading all raw data.

**Pass:** usable patient identifiers and a compatible endpoint are available, permissions are clear, and the baseline plus small end-to-end evaluation run.  
**Fail/pivot:** target markers or endpoint cannot be reconstructed, patient IDs are absent/incompatible, usage rights are unclear, or compute makes the full test infeasible. A cached-output-only analysis could still be scoped as an exploratory reanalysis, not a full retraining benchmark.

## Gate 2 — Prespecified analysis design

### Units and splits

- Group every core, section, and patch from a patient into the same partition.
- Establish an outer held-out patient set or outer grouped folds before discovery. Never use the outer set to choose targets, thresholds, features, aggregation rules, or hyperparameters.
- Fit normalization and any feature filtering only inside training partitions.
- Use inner patient-grouped validation for model/threshold selection.
- Compare target discovery across patient resamples *inside* the training portion of each outer fold.
- Repeat model seeds separately from patient resamples so that sampling variability and optimizer/initialization variability can be distinguished.
- Prespecify run counts and seeds after the compute pilot; aim for at least 30 successful discovery runs per outer split if computationally reasonable. If fewer, justify the reduced precision and treat results as exploratory.
- Keep one final evaluation protocol fixed. Do not choose the best-looking seed or target set from outer-fold results.

### Target representation

A target should include the molecular marker and signed direction (increase/decrease), not just the marker name. Normalize names against the source marker table. Distinguish:
- selection frequency of each signed target;
- direction consistency conditional on selection;
- overlap of complete signed target sets;
- size and sparsity of each set;
- fraction of model-predicted uplift that remains positive in held-out patients.

### Primary estimand

For each held-out patient, average patch/core-level model-predicted change according to the paper's prespecified aggregation rule; then weight patients equally. Report the mean, median, 10th percentile, and fraction of patients with positive predicted change. These are **model-predicted counterfactual changes**, not observed treatment effects or proof of causal efficacy.

### Primary reliability outcomes

1. Selection frequency for each signed target.
2. Pairwise Jaccard similarity of complete signed target sets; report set size alongside it because tiny/empty sets may appear stable.
3. Direction consistency for each molecular target, alongside how frequently that target is selected.
4. Between-run variability in held-out-patient predicted uplift.
5. Distribution of per-patient predicted uplift and uncertainty intervals obtained by resampling patients, not patches.

Jaccard similarity and selection frequencies are established generic metrics; using them alone is not the claimed methodological contribution.

## Gate 3 — Baselines and controls

At minimum compare, using the same outer split, allowed target budget and endpoint:
- **Published baseline:** Morpheus single-run / published median-across-patient strategy as reproduced.
- **Simple consensus baseline:** rank or select signed targets by frequency across discovery runs, using a prespecified frequency threshold and a fixed target budget.
- **Matched random/sign control:** target sets with matched set size and permissible directions, where this control is scientifically and computationally valid.
- **No-change reference:** predicted before-versus-after change is zero by definition.

Do not compare a large combination to a tiny combination without matching or transparently reporting target budgets. Record when a comparison is not fair or cannot be implemented.

## Gate 4 — Main evaluation and robustness claims

- Use the exact same held-out patients for each method within an outer fold.
- Report patient-level effect distributions and confidence intervals, not just the best patch or mean over all patches.
- Test whether stability metrics are associated with higher held-out predicted uplift or less downside variation; do not assume that stability means correctness.
- Distinguish sampling robustness from random-seed/model robustness and from external-cohort generalization.
- If the original saved model is used only once, do not describe that analysis as retraining robustness.
- If only held-out model predictions are used, do not describe them as biological validation.
- Use an independent cohort only after checking compatible markers, outcome definitions, and patient metadata; bulk RNA-seq outcomes cannot be silently pooled with spatial protein data.

## Go/no-go decision criteria

**Proceed to full study** only if the supplement/prior-art audit leaves a specific, meaningful gap; the baseline is reproducible; and the pilot confirms the patient-level evaluation is technically valid.

**Refine** if the reliability question is valuable but current metrics add little beyond existing methods. Focus on what changes in the scientific conclusion, not on inventing a label for a generic score.

**Pivot** if equivalent spatial target-set resampling is already demonstrated, if the available data cannot support the estimand, or if the only outcome is unstable model-generated prediction with no credible evaluation.

## Reproducibility, ethics and IP

Keep raw data out of GitHub unless the source license explicitly permits redistribution. Record retrieval date, accession/version, checksum, environment and deviations. This is computational hypothesis generation; no patient-specific treatment, clinical efficacy, target causality, or patentability is established. The project repository is public, so consult an institutional technology-transfer office or qualified patent professional before disclosing enabling details if an invention genuinely emerges.
