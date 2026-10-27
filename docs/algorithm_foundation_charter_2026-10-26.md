# Pre-algorithm research charter: robust spatial target discovery in HCC
**Version/date:** 0.1 / 2026-10-26  
**Status:** design charter; not a completed protocol, not a novelty certification, and not evidence that an algorithm works.

## 1. Purpose
Prepare a defensible foundation for a future mathematically ambitious AI system that investigates spatially organized mechanisms of resistance to immune-checkpoint inhibition (ICI) in hepatocellular carcinoma (HCC). The immediate task is not to maximize model complexity. It is to make the problem identifiable, the data traceable, the comparisons fair, and failure detectable.

## 2. Working scientific question
Can spatial-proteomic patterns yield reproducible, patient-level information about HCC ICI outcomes beyond established spatial immunotypes and simpler spatial immune features, while maintaining calibration and stability under region, panel, and cohort shifts?

This is a hypothesis to test—not a claim that VirTues or a future method adds information.

## 3. What cannot count as novelty by itself
The following are already established or too broad to support a novelty claim alone:
- rediscovering depleted, compartmentalized/compartmentalised, and enriched HCC immunotypes;
- showing that lymphoid-rich niches correlate with response;
- training a generic classifier on spatial images and reporting an internal AUC;
- reconstructing masked marker channels without proving held-out-patient value;
- highlighting a marker from SHAP/attention without stability, comparison, or external evidence;
- labelling an observational association “causal target discovery”.

Current literature includes the HCC spatial immunotype study (Gut 2025), VirTues (Nature 2026), and additional HCC spatial niche / biomarker studies appearing in 2026. The novelty map must be rechecked immediately before manuscript or public claims.

## 4. Candidate contribution space—not a locked algorithm
The future algorithm may be evaluated against a combination of these design goals:
1. **Spatial-mechanism representation:** preserve local cell neighbourhood, compartment, distance, and marker semantics instead of collapsing the sample to cell counts alone.
2. **Patient/ROI hierarchy:** treat multiple regions from one patient as clustered observations; estimate within-patient heterogeneity instead of allowing ROI leakage.
3. **Cross-panel and cross-cohort transport:** expose channel missingness, marker overlap, assay shift, and cohort shift as explicit variables rather than hidden preprocessing.
4. **Uncertainty-aware target ranking:** return uncertainty and stability for candidate pathways/markers, not a single deterministic list.
5. **Incremental value:** test whether the representation adds information after known immunotype, CD8 density/distribution, tumour/stroma composition, aetiology, and essential clinical variables.
6. **Counterfactual sensitivity as a hypothesis generator:** simulate marker/interaction removal only as a computational perturbation; do not equate it with biological intervention or causal effect.
7. **Mechanistic triangulation:** require independent cohorts, orthogonal molecular evidence, and ultimately experimental perturbation before high-confidence target language is justified.

A combination of known components is not automatically novel. The exact new mathematical object, objective, theorem/property, or validated empirical capability must be isolated and compared with the strongest relevant baselines.

## 5. Intended long-term system boundaries
**Inputs:** spatial-proteomics images and masks; verified panel/marker mapping; patient and ROI metadata; independently sourced clinical outcomes where permitted; optional external molecular and pathway evidence with versioned provenance.

**Core outputs:** (a) reconstruction / representation QC; (b) spatial phenotype estimates; (c) candidate interaction or target ranks with uncertainty and evidence provenance; (d) transportability and sensitivity reports; (e) an explicit abstain/insufficient-evidence result where appropriate.

**Not outputs:** patient-specific treatment recommendations, claims of treatment benefit from an untreated counterfactual, causal effects from non-interventional observations, or clinically validated decisions without prospective validation.

## 6. Mathematical obligations before implementation
The algorithm specification must state:
- observational unit and estimand (patient, ROI, cell, or marker);
- notation and assumptions, including missing channels and ROI sampling;
- an objective function and each term's biological/statistical rationale;
- identifiability limits and what data can or cannot identify;
- invariance/consistency properties sought and counterexamples where they fail;
- uncertainty method and calibration target;
- leakage boundaries and allowed information at each stage;
- computational complexity, failure modes, and a simpler falsifiable alternative;
- an ablation plan that can show each novel component is unnecessary;
- pseudocode and a deterministic reference implementation.

No equations should be added solely to make the method look sophisticated. Complexity is warranted only when it addresses a documented limitation and improves a preregistered metric.

## 7. Required baselines
At minimum, compare with:
- mean/median and assay-aware reconstruction baseline for masked-marker tasks;
- established spatial immunotype / CD8 abundance and parenchymal:stromal features where reconstructable;
- low-dimensional penalized regression and a small, transparent tree-based model where sample size permits;
- graph/spatial feature baselines not using VirTues;
- VirTues embeddings without the proposed novel component;
- a label-permutation / outcome-shuffle negative control;
- random-marker and random-edge ablations for any target-ranking claim.

The exact baseline set must be adjusted to verified data and frozen before outcomes are used for model selection.

## 8. Evidence ladder and claims
- **Level 0 — Data integrity:** input identity, mapping, image/mask integrity, rights and provenance.
- **Level 1 — Technical validity:** reproducible reconstruction / representation quality on patient-held-out data against simple baselines.
- **Level 2 — Incremental association:** prespecified patient-level association beyond established features, with uncertainty and multiplicity control.
- **Level 3 — External transport:** independent cohort, different acquisition or panel, and no tuning on evaluation data.
- **Level 4 — Mechanistic support:** orthogonal molecular evidence and biologically interpretable, repeatable perturbation predictions.
- **Level 5 — Causal/therapeutic target evidence:** functional perturbation and experimental validation; clinical claims would require further dedicated evidence.

Do not skip levels in wording. A Level 1 result cannot be marketed as target discovery.

## 9. Go/no-go criteria
Proceed to outcome analyses only when data mapping, preprocessing, checkpoint exposure, patient split, endpoint, and evaluation cohort status are resolved. Proceed to target ranking only if the method demonstrates stable incremental information. Stop or narrow the project if the available sample size cannot support the proposed complexity or if independent evaluation cannot be obtained.

## 10. Responsible research
Use only permitted data and model weights; follow the applicable licences. Keep patient-level rows, raw images/masks, credentials, and model weights out of the public repository unless explicit terms and disclosure review support publication. Preserve negative results and all prespecified model variants. Obtain relevant institutional approvals before accessing non-public clinical data or planning experimental work.
