# Existing-method comparison matrix

**Purpose:** compare the closest methods and avoid overclaiming novelty. This is a targeted, non-exhaustive audit; the complete Morpheus supplementary PDF has not yet been read.

| Method/paper | Data / task | Already covers | Consequence for our proposal |
|---|---|---|---|
| Morpheus (Nature Biomedical Engineering, 2025) | Spatial IMC tumour proteomics; counterfactual perturbations predicted to increase CD8+ infiltration | Patient-level splits; per-patch counterfactuals; whole-image perturbation constraints; median aggregation into whole-tumour strategies; in-silico held-out-patient evaluation; sparsity sensitivity; selected in-vitro validation; within-patient sample variability | The baseline already includes patient validation and aggregation. Repeating resamples may be a useful audit but does not alone establish high novelty. Supplement remains unaudited. |
| PHAROS (bioRxiv preprint, September 2026) | Single-cell perturbation model; target-directed drug-combination search | Sequential combination discovery; controls; independent combinatorial perturbation evaluation; sampled source/target batches; robustness-aware reranking | Combination search, sampling and reranking are not novel by themselves. |
| Anzum et al., *A Counterfactual Framework for Directional Cell-Cell Interaction Analysis in Spatial Transcriptomics* (MICCAI 2026) | Xenium spatial transcriptomics, tumour cell-cell influence | Counterfactual neighbor replacement, held-out core evaluation, core-level bootstrap uncertainty, label-permutation/spatial-shuffle controls | Generic spatial counterfactual core-bootstrap stability is already present in related tumour-microenvironment work. Their endpoint is directional cell-cell influence, not intervention-set recommendation. |
| Ding et al., SPAD-CFR, *Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments* (Biology 2026) | Spatial single-cell point-cloud tissue simulations; cancer microenvironment reprogramming | Counterfactual tissue generation changing molecular profiles and coordinates; biologically informed spatial modelling; melanoma immune-focused intervention hypotheses involving PD-1+ CD8+ cells | A broad spatial counterfactual cancer-immunotherapy framing is crowded. Exact target sets and model-predicted CD8 uplift differ, but this must be established as a meaningful scientific distinction. |
| COMPASS (Nature Medicine, 2026) | Bulk tumour transcriptomes and clinical immunotherapy cohorts; response prediction | Large multi-cohort response benchmark, several cancers/treatments and cross-cohort generalization | Cross-cohort response prediction alone is not novel; this is not a direct spatial counterfactual comparator. |
| Jiang et al. (IJCAI 2024), robust-counterfactual survey | General ML | Robustness under model/input changes, model multiplicity and noisy execution | Generic robustness metrics are established; application-specific work must add more than standard metric transfer. |
| Takefuji (Cancer Letters, 2026 issue / online 2025), feature-attribution stability | Oncology feature attribution/selection | Stability of feature selection/attribution in oncology | Generic feature stability is not novel; whole intervention sets need a clearly justified distinction. |
| Christodoulou & Sun (Expert Systems with Applications, 2026), uncertainty and counterfactual robustness | General tabular/synthetic counterfactual settings | Examines effects of uncertainty on counterfactual stability | A cancer application alone is insufficient. |

## Revised candidate directions

1. **Cross-method intervention decision utility:** compare predicted molecular intervention sets only where the intervention representation and held-out endpoint are genuinely compatible; test whether a consensus adds value over the strongest single baseline at the same target budget.
2. **Cross-cohort/platform transfer of signed target directions:** restrict to markers and endpoints harmonized before looking at results, and test whether directions and predicted effect replicate in independent patients.
3. **Mechanistic admissibility of predicted targets:** assess a preregistered set of known pathway/interaction/perturbation constraints against model-generated recommendations. This needs extra prior-art review because Morpheus itself discusses knowledge-graph regularization as a possible extension.

These are candidate questions only. Do not develop a new algorithm until a separate prior-art and data-feasibility gate picks one.

## Decision

**NO-GO for the generic robustness-only paper as currently framed.** Conditional GO to investigate one of the more specific alternatives above. Any paper must distinguish model-predicted change from biological validation and clinical efficacy.
