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


## 4. VirTues changes the cross-panel novelty assessment (Nature, 2026)

*The Virtual Tissues foundation model resolves spatial proteomics across scales.* https://doi.org/10.1038/s41586-026-10884-y. Code and weights: https://github.com/bunnelab/virtues.

VirTues supports marker reconstruction/virtual staining, cell and niche representations, biomarker discovery, patient stratification and cross-panel/cross-technology transfer. The paper reports a 32-cohort, >5,100-patient multi-technology corpus and an independent-cohort anti-PD-L1 biomarker application in triple-negative breast cancer. The current spora data website reports 35 cohorts/5,477 patients across five technologies; these are not identical corpus counts.

**Consequence:** generic cross-platform transfer and virtual staining are already heavily developed. A new study should focus on a downstream consequence not already covered by virtual-staining benchmarks—if a thorough search confirms one.

## 5. Spatium and Celcomen close additional gaps in the original framing

- **Spatium: A Protein Language Foundation Model for Spatial Proteomics** (2026): reconstructs missing spatial protein maps and evaluates preservation of tissue architecture. https://pmc.ncbi.nlm.nih.gov/articles/PMC13419744/
- **Celcomen: spatial causal disentanglement for single-cell and tissue perturbation modeling** (Nature Communications, March 2026), DOI https://doi.org/10.1038/s41467-026-69856-5: uses a causal generative graph neural network to model post-perturbation spatial transcriptomic states.

These works make generic missing-marker reconstruction and generic spatial counterfactual generation weak novelty claims.

## 6. Candidate gap requiring further verification

A narrower candidate is **counterfactual recommendation fidelity under whole-channel masking and virtual-marker reconstruction**: whether imputation metrics adequately indicate whether the signed intervention set and held-out-patient predicted objective remain consistent. This may connect the reconstruction and perturbation literatures in a useful way, but the current search is not exhaustive and does not establish priority.

A good experiment would compare:
1. fully measured marker-channel reference;
2. a reduced-panel model without imputation;
3. a simple imputation baseline;
4. a foundation-model reconstruction such as VirTues;
5. optional second imputer only if feasible.

Evaluate signed target-set fidelity, direction changes, and held-out-patient model-predicted uplift, while preventing patient and foundation-model training leakage. An optional abstention rule must demonstrate value against standard alternatives at a transparent coverage cost.

## 7. Potential independent clinical datasets—secondary only

- Pybus et al. (npj Precision Oncology, January 2026), DOI https://doi.org/10.1038/s41698-025-01250-8, report 12 stage-IV melanoma patients with spatial mIF (4 responders, 8 non-responders) and >8 million cells; processed data DOI https://doi.org/10.5281/zenodo.16898362. Small n and limited marker overlap constrain use to exploratory secondary analysis.
- GSE300793/GSE300445 describe 57 pretreatment bulk RNA-seq samples and four spatially profiled primary melanoma tumours. Bulk RNA is not a direct substitute for spatial protein measurement.

## Updated decision

**The old robustness-only study remains no-go as a novelty-led paper. Conditional go for a small feasibility pilot of counterfactual recommendation fidelity under marker reconstruction.** First identify a permitted spora cohort with CD8/T-cell labels, target markers, patient IDs and a measured reference. Stop if no fair cohort is available or if a direct version of this exact benchmark is found.
