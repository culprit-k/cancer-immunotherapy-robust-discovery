# Research question and scope

**Project priority reset — 27 October 2026**

## Primary objective: discover a reproducible biological relationship

The central paper should test a specific biological relationship in tumour–immune spatial organization, with AI used to generate and interrogate candidate hypotheses. A successful inference pipeline alone is not the research result. No biological discovery has yet been established.

### Working question

**Does the spatial coupling between cytotoxic lymphocyte state and nearby suppressive myeloid state carry information about immune access or treatment outcome beyond total immune abundance, known HCC immunotype, and simple additive marker summaries?**

This is a **candidate hypothesis to test**, not a marker-level claim. The exact feature definition depends on verified marker-to-plane mapping, mask semantics and available cell annotations. It should not be named after CD8, Granzyme B, CD163, CD204, Arginase1 or any other marker unless the source mapping is validated and the analysis plan is frozen.

The reason to investigate a *state-conditioned spatial relationship*, rather than another global marker or a generic “immune-excluded” phenotype, is to test whether functional-state context adds information beyond counts and known architecture labels. Whether this is novel is **unknown** until a focused prior-art comparison is completed after the exact hypothesis and measurement are defined.

## Explicit prior-art constraints

The existing HCC discovery/ICI cohorts have already been used to define immune-depleted, compartmentalized and enriched architectures, spatial immune neighborhoods, the prognostic relevance of an enriched region, and myeloid/T-cell relationships. Other HCC papers have reported stromal FAP-alpha associations and TAM–MAIT dysfunction at the invasive margin. Therefore, we must not present any of these broad themes as novel in themselves.

The current 42-patient ICI cohort includes 27 SD, 10 PD and 5 PR patients in the derived clinical table. A complex PR classifier is not justified by five PR cases. The 84-vs-86 ROI discrepancy (ICI_24 and ICI_39) remains an explicit gate. The published cohort is useful for reproducible exploratory analysis, but alone cannot demonstrate independent discovery or validation of mechanisms already described in the source paper.

## Primary analysis sequence

1. **Freeze a measurable biological phenotype before inspecting response labels.** Start with source-backed cell/compartment identity and marker mapping. If labels are ambiguous, do not infer them from integer codes.
2. **Create patient-level summaries.** ROIs, cells and tiles are nested measurements, not independent outcomes. Aggregate using a predeclared rule or use a justified hierarchical model.
3. **Compare against simple baselines.** At minimum: total immune/cytotoxic abundance, each marker separately, regularized additive features, and a simple neighbourhood-frequency measure. The candidate spatial coupling score must add interpretable information beyond these baselines.
4. **Quantify uncertainty and influence.** Report effect size and confidence intervals, multiplicity correction, patient-level resampling, leave-one-patient-out direction stability, missingness, and negative controls.
5. **Validate independently.** Prefer an independent permitted HCC spatial cohort with usable marker overlap; otherwise use orthogonal published/experimental evidence and state clearly that it is not an independent outcome validation. Cohort/checkpoint training exposure must be disclosed.
6. **Test mechanism separately.** An association or model counterfactual is not a causal effect. Claims that a cell interaction drives immune escape require orthogonal experimental evidence.

## AI role

AI can support discovery by learning or ranking multivariate cell-state/spatial relationships, identifying feature interactions not captured by additive baselines, and prioritizing falsifiable hypotheses. It must not invent cell identities, infer channel ordering from expected biology, or be treated as ground truth. A foundation model is optional; direct outcome-blind image/cell analysis may be the more defensible first step if the VirTues input-compatibility gate remains blocked.

The missing-marker / counterfactual recommendation-fidelity analysis is now **secondary**. It may strengthen robustness evaluation but does not replace the biological objective.

## Hard data gates

- Exact panel-plane mapping with source evidence.
- Source-defined cell/stromal/tumour mask semantics and representative overlays.
- Resolution of ICI_24 / ICI_39 ROI discrepancies or exclusion under a frozen, outcome-independent rule.
- Documented image preprocessing and appropriate input compatibility.
- Clinical outcome dictionary, including event/censor definitions, verified from source metadata.
- Model-training exposure and licence review before any held-out-model claim.
- Frozen feature definitions, outcomes, contrasts, thresholds and statistical plan before response-linked analysis.

## Go / no-go criteria

A candidate biological finding proceeds only if it is interpretable, adds value beyond simpler explanations, survives prespecified sensitivity analyses and patient-level uncertainty analysis, and is corroborated in independent data or orthogonal evidence. If any criterion fails, the correct result is a negative/feasibility conclusion, not a post-hoc marker claim.

**Current status: hypothesis and executable analysis scaffolding only. No marker combination, causal mechanism, independent validation, clinical utility, novelty, or patentability is established.**
