# Literature review and prior-art audit

**Last updated:** 25 October 2026  
**Status:** Targeted, non-systematic review. Novelty is unverified. The generic robustness-only proposal is currently a no-go as the main paper contribution.

## Executive assessment

The research area is important, but the original proposition—repeat Morpheus target discovery over patient/core resamples and model seeds, then report target selection frequency, Jaccard similarity and held-out predicted uplift—looks too incremental by itself. Recent work already includes spatial counterfactual target discovery and aggregation (Morpheus), single-cell combination search with robust re-ranking (PHAROS), spatial transcriptomic counterfactual inference with core-level bootstrap (Anzum et al., MICCAI 2026), and generative spatial counterfactual tissue reprogramming that includes immune-focused hypotheses (SPAD-CFR, Biology 2026).

The next step is not to invent a score. It is to check whether a specific comparative decision-utility or cross-cohort/platform-transfer question has a real prior-art gap and compatible data.

## 1. Morpheus (2025): closest baseline

Wang ZJ et al. *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles.* Nature Biomedical Engineering. DOI: https://doi.org/10.1038/s41551-025-01357-0

Morpheus predicts CD8+ T-cell presence from spatial multiplexed tumour images and uses counterfactual optimization to propose molecular perturbations associated with increased predicted T-cell infiltration. The paper reports 159 melanoma cores from 69 patients and 209 CRC liver-metastasis sections from 30 patients. Selected predictions were tested in vitro.

Existing features directly relevant to our project:
- Patient-level train/validation/test splits.
- Counterfactual perturbations generated per image patch.
- Median aggregation from patchwise perturbations into whole-tumour strategies, with patient-level aggregation discussed.
- In-silico evaluation of strategies on held-out patient samples.
- Sensitivity to perturbation sparsity.
- Discussion of variation across tissue samples, including cores from the same patient.
- Suggested future testing of a strategy learned from a subset of a patient's samples on remaining samples.

**Implication:** patient-level splits, target combinations, sample heterogeneity and held-out evaluation cannot be claimed as novel. Main article Methods and public code were inspected; the separate supplementary PDF has not been read because the download redirect could not be retrieved in this runtime.

Resources:
- Paper: https://doi.org/10.1038/s41551-025-01357-0
- Code/reproduction: https://github.com/cellethology/morpheus-spatial
- Original melanoma data-for-analysis: https://doi.org/10.5281/zenodo.5994136
- Morpheus preprocessed data/model outputs: https://doi.org/10.22002/pr14s-wgk05

## 2. PHAROS (2026 preprint): target-directed combination search

*PHAROS: turning single-cell perturbation models into target-directed drug-combination screens.* bioRxiv preprint, September 2026. https://www.biorxiv.org/content/10.64898/2026.09.08.749477v1.full. Code: https://github.com/jbezney61/PHAROS

PHAROS uses a pretrained single-cell perturbation model to search drug combinations that move a starting cell state toward a specified target state. Its reported workflow includes controls, independent combinatorial perturbation-data evaluation, sampled batches and robustness-aware reranking.

**Implication:** a broad claim to drug-combination search, sampling-based reliability, or robust reranking would overlap substantially. PHAROS is a preprint, and its single-cell drug-state task is not identical to spatial-proteomic CD8+ infiltration counterfactuals.

## 3. Counterfactual spatial cell-cell influence (MICCAI 2026)

Anzum et al. *A Counterfactual Framework for Directional Cell-Cell Interaction Analysis in Spatial Transcriptomics.* MICCAI 2026. https://papers.miccai.org/miccai-2026/0006-Paper6105.html

The study uses a neighborhood-conditioned model and counterfactual neighbor replacement to estimate directional cell-cell influence. It describes a 38-core Xenium cholangiocarcinoma evaluation with held-out cores, permutation/spatial-shuffle controls and core-level bootstrap confidence intervals.

**Implication:** generic spatial counterfactual analysis and core-level bootstrap uncertainty already appear in closely related tumour-microenvironment work. Its output is a directional cell-cell influence score, not a full therapeutic target set intended to increase CD8+ infiltration. That difference may matter, but it must be justified scientifically rather than simply asserted.

## 4. SPAD-CFR (Biology, 2026): spatial counterfactual tissue reprogramming

Ding W, Luo Z, Xiong Y. *Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments.* Biology. DOI: https://doi.org/10.3390/biology15141097. Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC13406000/

SPAD-CFR uses a spatial point-cloud attention/diffusion framework to generate counterfactual tissue states in which molecular profiles and coordinates can change together. The article includes melanoma interventions involving PD-1+ CD8+ T cells and predicted localized bystander cytotoxic effects.

**Implication:** broad spatial counterfactual tissue reprogramming and immune-focused intervention hypotheses are now directly adjacent published work. SPAD-CFR has a different model and output from Morpheus, but “spatial counterfactual AI for cancer immunotherapy” is not a strong novelty claim.

## 5. COMPASS (Nature Medicine, 2026): cross-cohort response prediction

Shen W et al. *Generalizable AI predicts immunotherapy outcomes across cancers and treatments.* DOI: https://doi.org/10.1038/s41591-026-04502-7

COMPASS predicts immune-checkpoint-inhibitor response from bulk tumour transcriptomes, using biologically grounded immune concepts. The article reports evaluation across 16 clinical cohorts and 1,133 patients, following training on 10,184 tumours.

**Implication:** cross-cohort response prediction and generalization are already active areas. COMPASS is complementary prior art, not a direct spatial-proteomic perturbation benchmark: bulk RNA-seq outcome prediction cannot be pooled with spatial protein data without an explicit mapping.

## 6. Robust counterfactual explanations (IJCAI 2024)

Jiang J, Leofante F, Rago A, Toni F. *Robust Counterfactual Explanations in Machine Learning: A Survey.* IJCAI 2024. DOI: https://doi.org/10.24963/ijcai.2024/894

This survey covers robustness to model changes, model multiplicity, noisy execution and input changes.

**Implication:** counterfactual robustness is an established general machine-learning topic. An application-specific benchmark needs to show what standard metrics fail to capture and what scientific decision changes as a result.

## 7. Feature stability in oncology

Takefuji Y. *Stability of feature attribution: Contrasting supervised and unsupervised selection for radiopathomics and TCGA outcomes.* Cancer Letters, 2026 issue (online 2025). DOI: https://doi.org/10.1016/j.canlet.2025.218133

This work studies stability of feature attribution/selection in oncology.

**Implication:** a generic cancer-feature-stability score is insufficiently novel.

## 8. Uncertainty and counterfactual robustness (2026)

Christodoulou L, Sun C. *The impact of machine learning uncertainty on the robustness of counterfactual explanations.* Expert Systems with Applications (2026). DOI: https://doi.org/10.1016/j.eswa.2026.131198

This paper studies the influence of machine-learning uncertainty on counterfactual stability.

**Implication:** uncertainty-aware counterfactual stability is also established methodological prior art; adding uncertainty to a cancer application alone is unlikely to suffice.

## Revised decision and candidate pivots

**NO-GO for the generic robustness-only paper as currently framed.** The initial stability metrics and code are still useful for a reproducibility audit, but a high-novelty paper needs a more substantive question.

Candidates to evaluate next:
1. **Cross-method intervention decision utility:** whether a prespecified consensus across genuinely comparable spatial methods selects intervention sets with better held-out-patient model-predicted uplift than the strongest single method at a matched target budget.
2. **Cross-cohort/platform transfer of signed target direction:** whether target directions and predicted effects transfer to independent patients with genuinely shared markers and a compatible endpoint.
3. **Mechanistic admissibility of interventions:** whether prespecified molecular/signalling constraints improve independent plausibility, recognizing that knowledge-graph constraints and biologically informed spatial counterfactuals already exist.

These are hypotheses, not confirmed gaps. A method/dataset compatibility matrix is available at docs/method_dataset_compatibility.md. Do not compare methods whose intervention objects or endpoints are incompatible, and do not pool modalities just because they involve the same cancer.

## Reproducibility and data caveats

- No data archive has been downloaded or checked locally in this runtime.
- No Morpheus checkpoint has been loaded, and no original training/counterfactual-generation pipeline has been executed.
- The separate Morpheus supplementary PDF was located but not retrieved through its signed download redirect; the full supplement is not audited.
- The original melanoma data-for-analysis archive is about 7.1 GB, and its rights/license field was not clear in the audit; check exact use terms before substantive reuse or redistribution.
- Six synthetic unit tests for generic analysis helpers passed locally; these tests do not establish model performance or biological validity.

See also the [novelty assessment](novelty_assessment.md), [method/dataset compatibility matrix](method_dataset_compatibility.md), [related-work addendum](related_work_addendum_2026.md), and [reproducibility run log](reproducibility_run_log.md).


## 9. VirTues (Nature, 2026): spatial-proteomics foundation model and virtual staining

Wenckstern J et al. *The Virtual Tissues foundation model resolves spatial proteomics across scales.* Nature 657, 744–754 (2026). DOI: https://doi.org/10.1038/s41586-026-10884-y. Code and model weights: https://github.com/bunnelab/virtues.

VirTues provides marker-aware, multi-scale spatial-proteomics representations and supports marker reconstruction/virtual staining, cell segmentation and typing, niche annotation, spatial biomarker discovery and patient stratification. Its paper reports a core 15-IMC-cohort corpus (3,102 patients, 146 markers) and a larger multi-technology corpus of 32 cohorts spanning four technologies, more than 5,100 patients and 239 markers. It reports zero-shot transfer under panel/technology shifts and biomarkers for anti-PD-L1 chemo-immunotherapy response in triple-negative breast cancer, with independent-cohort survival stratification.

The public spora collection has since described 35 cohorts, 5,477 patients and five imaging technologies; do not treat those live platform counts as identical to the VirTues paper's model-training corpus.

**Implication:** generic virtual staining, cross-panel transfer and spatial-protein biomarker discovery are already established. The proposed angle must be narrower: whether imputation quality preserves a *downstream intervention recommendation*, not whether a marker can be reconstructed or a biomarker can be predicted. VirTues reports that the Morpheus/Wang data were obtained via access request and cannot be redistributed in the harmonized corpus because of licensing restrictions.

Resources:
- Paper: https://www.nature.com/articles/s41586-026-10884-y
- Code: https://github.com/bunnelab/virtues
- spora data documentation: https://spora.epfl.ch/docs/index.html
- spora benchmark suite: https://github.com/bunnelab/spora-bench

## 10. Spatium (2026): protein-language foundation model for spatial proteomics

*Spatium: A Protein Language Foundation Model for Spatial Proteomics.* https://pmc.ncbi.nlm.nih.gov/articles/PMC13419744/

This adjacent model reconstructs missing spatial protein signals using protein-language representations and evaluates whether reconstructed maps preserve tissue architecture. It makes generic "impute missing spatial protein markers" or "use protein embeddings for panel completion" inadequate as a novelty claim.

**Implication:** any new question should measure the consequences of imputation on downstream counterfactual decisions, beyond reconstruction accuracy and spatial-map quality.

## 11. Celcomen (Nature Communications, March 2026): spatial causal perturbation model

Megas S et al. *Celcomen: spatial causal disentanglement for single-cell and tissue perturbation modeling.* Nature Communications 17, 4126 (2026). DOI: https://doi.org/10.1038/s41467-026-69856-5. It uses a generative graph neural network and causal structure framework to disentangle intra-/inter-cellular gene programs and generate counterfactual spatial transcriptomic responses to perturbations, with simulation and tissue analyses.

**Implication:** spatial causal counterfactual generation and virtual-tissue perturbation modeling are already active, peer-reviewed directions. The project should not claim a new general spatial counterfactual model.

## 12. TISSUE and imputation consequences for downstream analysis

Svensson et al. developed TISSUE for uncertainty-calibrated spatial transcriptomic expression prediction, using conformal inference and assessing consequences for downstream inference. https://www.nature.com/articles/s41592-024-02184-y

A 2026 iScience benchmark compared eight imputation methods for spatial metabolomics under missingness, assessing both imputation accuracy and preservation of spatial clustering. https://doi.org/10.1016/j.isci.2026.115203

Virtual staining work has also explicitly examined whether image reconstruction improves downstream classification/segmentation rather than relying only on image similarity. https://doi.org/10.1364/BOE.576061

**Implication:** uncertainty calibration, generic downstream evaluation and imputation benchmarks are not new. The remaining candidate is the joint *decision fidelity* of a counterfactual intervention recommendation under whole-marker-channel missingness. That is a candidate gap, not a verified one.

## 13. Independent clinical-response data that may support secondary, not primary, analysis

### Pybus et al. (npj Precision Oncology, January 2026)
*Predicting anti-PD-1 immune checkpoint blockade response in melanoma patients with spatially aware machine learning models.* DOI: https://doi.org/10.1038/s41698-025-01250-8.

This study reports 12 stage-IV melanoma patients (4 responders, 8 non-responders), over 8 million cells, 14 proteins across two eight-marker multiplex-immunofluorescence panels, and 100 randomized model iterations. The reported feature-rich model had ROC AUC 0.76; the authors explicitly note the small cohort as a limitation. Processed data: https://doi.org/10.5281/zenodo.16898362. Code: https://github.com/goeckslab/Melanoma-ICB-mIF.

This cohort might help with exploratory external checks only if target markers overlap. It is too small to serve as the sole basis for a high-dimensional clinical-response model.

### GSE300793 and GSE300445 (2026 publication/data release)
The associated melanoma study reports 57 pretreatment bulk RNA-seq samples from stage-III primary melanoma patients and spatial transcriptomics on four primary tumours. GEO: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300793 and https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE300445. The study connects spatial tumour-immune ecosystems with adjuvant anti-PD-1 outcome.

These data could provide an exploratory molecular-expression/outcome check for a prespecified target signature, but bulk RNA measurements are not spatial protein measurements and cannot validate a protein intervention causally.

## 14. Revised research recommendation

**Do not proceed with the generic robustness-only or broad cross-platform-transfer idea as a novelty claim.** The most specific candidate still worth testing is:

> When one or more entire marker channels are absent and reconstructed by a spatial-proteomics foundation model, does the reconstruction preserve signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes?

The potential contribution is a **counterfactual recommendation-fidelity benchmark and reliability/abstention evaluation**, not a claim to invent virtual staining or spatial causal inference. Test whether marker-level reconstruction metrics fail to reveal changes in the recommended target set or predicted objective. Compare a fully measured reference, no-imputation baseline, simple imputation and foundation-model reconstruction. Apply strict patient-grouped splits and evaluate only on held-out patients.

The gap is not confirmed. A targeted search must still check if VirTues, SPORA, Spatium, Celcomen, TISSUE and related robust-counterfactual studies already evaluate this exact downstream intervention-fidelity question.

## Updated decision status

**CONDITIONAL GO for a narrow feasibility pilot, NOT a confirmed novelty claim.** First confirm an openly usable cohort with CD8/T-cell labels, candidate intervention channels, patient identifiers and explicit terms. Then run a small masked-channel reconstruction and downstream target-discovery test. Stop or pivot if no cohort permits a fair test or if an equivalent benchmark already exists.
