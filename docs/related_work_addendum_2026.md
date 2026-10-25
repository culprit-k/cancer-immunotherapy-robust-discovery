# New related work identified in the October 2026 prior-art update

**Purpose:** update the novelty gate with recent papers close to spatial counterfactual modelling. This is not an exhaustive systematic review.

## 1. A Counterfactual Framework for Directional Cell-Cell Interaction Analysis in Spatial Transcriptomics

- Anzum et al., MICCAI 2026.
- Open-access proceedings page: https://papers.miccai.org/miccai-2026/0006-Paper6105.html
- Code: https://github.com/Snigdha022/Counterfactual-Cell-Influence-Spatial-Transcriptomics
- The method uses a neighborhood-conditioned graph model and counterfactual neighbor replacement to infer directional cell-cell influence. It evaluates 38 Xenium cholangiocarcinoma cores with 25 training, 3 validation and 10 held-out cores, aggregating a directionality score at core level. It reports core-level bootstrap confidence intervals and tests against label-permutation/spatial-shuffle controls.
- **Implication:** core-level bootstrap, held-out spatial evaluation and counterfactual analysis are already used in closely related tumour-microenvironment research. Its endpoint is directional cell-cell influence, not a complete therapeutic target set predicted to improve CD8 infiltration; that distinction does not make a generic resampling study novel on its own.

## 2. Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments (SPAD-CFR)

- Ding, Luo and Xiong, Biology 2026; DOI: https://doi.org/10.3390/biology15141097
- Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13406000/
- The paper proposes a spatial point-cloud attention/diffusion framework that generates counterfactual tissue configurations with molecular profiles and coordinates changing together. It evaluates multiple tissue settings and describes melanoma interventions involving PD-1-positive CD8-positive T cells with predicted localized bystander cytotoxic effects.
- **Implication:** spatial counterfactual tissue reprogramming, biological constraints and immune-focused intervention hypotheses are now directly adjacent published work. The exact model and claimed effects differ from Morpheus, but a broad “counterfactual AI for spatial cancer immunotherapy” framing would be weak.

## 3. PHAROS

- Preprint, September 2026: https://www.biorxiv.org/content/10.64898/2026.09.08.749477v1.full
- Code: https://github.com/jbezney61/PHAROS
- PHAROS searches combinations of single-cell perturbations toward target cell states, assesses combinations against controls/independent combinatorial perturbation data, and includes sampled-batch and robustness-aware reranking options.
- **Implication:** target-directed combination discovery, sampled-batch variability, and reranking are already being pursued in a different single-cell perturbation regime.

## Revised novelty consequence

The current proposal—bootstrap/retrain Morpheus and report signed-target/Jaccard stability—has become a **high-risk, likely incremental** idea unless the complete Morpheus supplement and a broader prior-art search reveal a distinct unaddressed scientific question.

The current project should not proceed by relabeling standard resampling as a new algorithm. Next candidates to assess are:
1. an intervention-level reproducibility and *decision utility* benchmark across spatial methods, with matched target budgets and an untouched patient evaluation; or
2. cross-cohort/platform transfer of intervention direction and predicted effect, restricted to genuinely shared markers and a compatible outcome.

Both are hypotheses to investigate, not novelty claims. They need a new literature/data feasibility gate before implementation. Do not combine incompatible spatial-protein, spatial-transcriptomic and single-cell perturbation datasets without an explicit harmonization argument.

## Current decision

**NO-GO for the generic robustness-only paper as currently phrased. CONDITIONAL GO to pivot and investigate a more specific comparative/transfer question.** A feasibility pilot may still be useful to learn the Morpheus pipeline, but that pilot alone does not justify a novelty claim.
