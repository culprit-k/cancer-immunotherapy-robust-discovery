# Novelty assessment

**Status (25 October 2026): NO-GO for the generic robustness-only paper as currently phrased. Conditional GO to investigate a more specific comparative or cross-cohort-transfer question.**

## Previous candidate now considered too incremental

The initial candidate was to repeat Morpheus discovery over patient-grouped resamples and model seeds, then report signed-target selection frequency, full-set Jaccard similarity, and held-out model-predicted CD8+ infiltration uplift. This remains useful as a reproducibility audit, but by itself it is not strong enough to support a high-novelty paper. Generic bootstrapping and target-set stability are established ideas, and several adjacent studies now overlap strongly.

## Relevant prior art already checked

### Morpheus (2025)
Spatial-proteomic counterfactual target discovery; patient-level train/validation/test splits; per-patch counterfactuals; median aggregation to whole-tumour strategies; in-silico evaluation on held-out patient samples; variation across samples including those from the same patient; sparsity sensitivity and selected in-vitro validation.

### PHAROS (bioRxiv preprint, September 2026)
Single-cell perturbation-model search for target-directed drug combinations. It uses sampled source/target batches, control comparisons, independent combinatorial perturbation evaluation and robustness-aware re-ranking. Combination search, sampling and reranking in general are therefore not distinctive contributions.

### Counterfactual directional cell-cell influence (MICCAI 2026)
Anzum et al., *A Counterfactual Framework for Directional Cell-Cell Interaction Analysis in Spatial Transcriptomics*. https://papers.miccai.org/miccai-2026/0006-Paper6105.html. Uses counterfactual neighbor replacement on spatial transcriptomics and reports held-out core evaluation plus core-level bootstrap uncertainty. This makes generic core-level resampling/uncertainty quantification particularly hard to claim as novel.

### SPAD-CFR (Biology, 2026)
Ding, Luo and Xiong, *Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments*. https://doi.org/10.3390/biology15141097. Proposes spatial point-cloud/diffusion counterfactual generation that jointly changes molecular profiles and coordinates, and includes melanoma immune-focused intervention hypotheses involving PD-1+ CD8+ T cells. A broad “counterfactual AI for spatial cancer immunotherapy” framing is now crowded.

### Other adjacent methods
- COMPASS (Nature Medicine, 2026): large multi-cohort immunotherapy response prediction/generalization.
- Jiang et al. (IJCAI 2024): robust-counterfactual methods and robustness dimensions.
- Takefuji (Cancer Letters, 2026 issue / online 2025): oncology feature-attribution/selection stability.
- Christodoulou and Sun (Expert Systems with Applications, 2026): uncertainty and counterfactual robustness.

See the expanded [existing-method comparison matrix](existing_methods_matrix.md) and [October 2026 addendum](related_work_addendum_2026.md).

## More defensible next questions to investigate (not yet validated)

1. **Intervention-level decision utility across methods:** For a common evaluation cohort and compatible intervention definitions, does a prespecified cross-method consensus select target sets that are more reproducible and have better held-out-patient model-predicted immune uplift than the strongest single-method baseline at a fixed target budget? Key risk: Morpheus and SPAD-CFR have different model structures/outcomes; do not compare unlike outputs as if they were the same intervention.
2. **Cross-cohort/platform transfer of intervention direction:** For genuinely shared molecular targets and a compatible endpoint, do signed target directions and predicted effect transfer across independent patient cohorts/platforms better than chance and better than within-cohort baselines? Key risk: data and outcomes may not be compatible, and cross-cohort prediction alone is already well studied.
3. **Mechanistic feasibility constraints:** Evaluate whether interventions that violate prespecified molecular/signalling constraints fail independent plausibility checks. Key risk: Morpheus itself points toward knowledge-graph constraints as a future extension, and other recent models are biologically informed; “add a graph regularizer” alone is not novel.

The right next step is a targeted literature and dataset feasibility comparison for these alternatives—not immediate algorithm invention.

## Decision rules

- **Proceed to a paper protocol** only after a specific gap survives the full supplement and prior-art audit, data rights are clear, and a reproducible benchmark exists.
- **Refine** if the topic is valuable but the main advance is an evaluation protocol rather than a new algorithm; state this accurately.
- **Pivot** if equivalent cross-method or transfer work exists, or available data cannot test the question.

## Intellectual-property caution

This repository is public. Public disclosure can affect patent options depending on jurisdiction and facts. No patentability conclusion is made; seek institutional technology-transfer or qualified patent-professional advice before disclosing enabling details of any genuinely distinct invention.
