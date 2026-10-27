# Biology-first execution plan: evidence required for a real HCC immune-evasion finding

**Date:** 2026-10-27  
**Status:** hypothesis and analysis plan only; no biological result has been established.

## Main objective

The main paper must deliver a **reproducible, biologically interpretable tumour–immune relationship**, not merely a working foundation-model pipeline or an attractive counterfactual visualization.

AI is the discovery and prioritization tool. The biological claim must survive patient-level statistics, meaningful baselines, sensitivity analysis, and independent evidence. Until then, all candidate mechanisms remain hypotheses.

## Focused question

Among hepatocellular carcinoma (HCC) tissue regions, do combinations of spatially resolved protein features identify an immune-excluded or immune-depleted architecture more reliably and reproducibly than any individual marker or a regularized additive model—and do those same prespecified combinations show a consistent association with checkpoint-inhibitor outcome in an eligible, independent patient cohort?

This question must be narrowed further once the exact panel mapping, architecture labels, patient/ROI crosswalk and outcome dictionary are verified. Do not claim novelty for rediscovering the previously published depleted, compartmentalised and enriched HCC immune architectures.

## Candidate biological hypothesis (not a result)

A combination of (a) verified immune-cell abundance/activation markers, (b) tumour/stromal compartment features, and (c) spatial neighbourhood or boundary features may encode immune exclusion better than single-marker abundance alone.

This is deliberately a feature-family hypothesis, not a preselected marker list. We must not name a specific marker combination as a discovery until it is supported by source-verified panel mapping and held-out analysis. Do not assume cell types, compartment identities, or mask labels from numeric values.

## Primary endpoint and analysis hierarchy

### Stage 1 — establish an observable tissue phenotype

Use a source-defined architecture label if the cohort's published annotation and mapping are available and reliable. Otherwise, define a measurable phenotype before outcome analysis using only validated masks and marker channels—for example, immune-cell density within verified compartments or a predeclared immune-to-tumour/stromal spatial distribution summary. Do not derive a phenotype from outcome labels.

### Stage 2 — test whether combinations add information

At patient level, compare:
1. Clinical/covariate-only baseline where appropriate.
2. Each eligible marker separately.
3. Regularized additive model.
4. Prespecified pairwise/small-combination model.
5. AI-derived feature ranking or counterfactual method.

Use the same eligible patients and outer splits. Feature selection, scaling, missingness handling and tuning occur inside training folds only. Patient, not ROI/cell/pixel, is the inferential unit. Aggregate multiple ROIs with a frozen rule or use a justified hierarchical model.

### Stage 3 — establish robustness

For every selected combination, report:
- Selection frequency and rank stability across patient-level resamples.
- Effect direction and uncertainty, not only point estimates.
- Sensitivity to predeclared image/preprocessing choices and compartment aggregation rules.
- Comparison to single-marker/additive baselines.
- Patient-grouped permutation/negative controls.
- Missingness, exclusions, and failure cases.

The held-out ICI cohort must not be used to select features, thresholds, preprocessing or hyperparameters. If pretrained model exposure cannot be excluded, it cannot serve as an independent model-validation cohort.

### Stage 4 — test clinical relevance without overclaiming

Only after outcome definitions and eligibility are verified, test whether the frozen feature/combination associates with ICI outcome or survival. The current extraction has 42 patients and five PR cases; a complex response classifier is not credible at this sample size. Use low-dimensional, prespecified patient-level analysis, uncertainty intervals and explicit exploratory framing. Do not equate association with prediction utility or treatment benefit.

### Stage 5 — biological validation

A computational result is a candidate biological finding only if:
- The feature has an interpretable biological meaning supported by the panel and annotations.
- Its association is not explained by a simpler baseline or technical artifact.
- Direction and ranking persist under prespecified sensitivity tests.
- Independent evidence supports the mechanism (for example, a distinct published cohort, orthogonal assay, or later laboratory experiment).
- Any causal claim is separately tested experimentally. Counterfactual outputs alone are not causal evidence.

If no independent compatible cohort or orthogonal evidence is available, report a robust computational association/hypothesis, not a validated mechanism.

## Hard gates before analysis

- Exact channel-plane-to-marker map and marker identifiers verified from source records.
- Cell/stromal/parenchymal/interface mask semantics and overlays verified.
- ICI_24 and ICI_39 ROI discrepancies resolved from authoritative records or affected patients excluded by a rule frozen before outcomes are examined.
- Preprocessing is documented and biologically defensible. Do not call already PENGUIN-normalized data an official VirTues reproduction without demonstrating equivalence.
- Checkpoint exposure and licence are documented. If uncertain, label exposure unknown and do not claim independent pretrained-model validation.
- Clinical endpoint dictionary and missingness are frozen.
- Protocol, split seeds, feature definitions, metrics and stopping rules are committed before outcome-linked analysis.

## Success criteria

The study supports a candidate discovery only if all of the following hold:
1. A specific combination/relationship is identifiable and biologically interpretable.
2. It improves on relevant single-marker and additive baselines by a prespecified criterion, with uncertainty reported.
3. It is stable across patient resamples and reasonable prespecified sensitivity analyses.
4. It survives a genuinely held-out cohort or independent orthogonal evidence.
5. It is not a trivial re-statement of previously published HCC immune architectures or prior spatial-counterfactual methods.
6. The data provenance, licences, analysis code and exclusions are reproducible.

If these criteria fail, report a negative or feasibility result and revise the question rather than manufacture a discovery.

## Immediate next action

Complete the source-backed panel/mask/ROI/preprocessing gates and collect the user's actual Colab preflight output. No biological result can be honestly computed from repository metadata alone. Once the data contract is closed, implement a reproducible patient-level feature extraction and baseline-analysis pipeline before attempting a complex AI ranking.

## Claim boundary

At this stage:
- **Established:** public cohort structure and prior art constrain the design; current input/exposure gates are unresolved.
- **Hypothesized:** combinations of spatial tumour–immune features may capture immune exclusion beyond single markers.
- **Not established:** any marker combination, causal mechanism, independent validation, clinical utility, novelty, or patentability.
