# Initial literature audit

**Status:** Preliminary. This is a starting point, not a systematic review or exhaustive prior-art search.

## 1. Morpheus (2025)

Wang ZJ et al. *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles.* Nature Biomedical Engineering. DOI: https://doi.org/10.1038/s41551-025-01357-0

### Relevance
Morpheus trains a model to predict CD8+ T-cell infiltration from spatial multiplexed tissue measurements and applies gradient-based counterfactual optimization to propose changes associated with increased predicted infiltration. The paper evaluates melanoma and colorectal cancer liver-metastasis data and reports in-vitro validation of selected predictions.

### Implication
The project cannot claim novelty from counterfactual molecular perturbation, spatial tumour-protein modelling, or generating combinations associated with T-cell infiltration alone.

### Resources reported by the paper
- Code: https://github.com/neonine2/morpheus-spatial
- Melanoma dataset: https://doi.org/10.5281/zenodo.5994135
- Breast tumour dataset: https://doi.org/10.5281/zenodo.5850951
- Preprocessed data and model outputs: https://doi.org/10.22002/pr14s-wgk05
- The colorectal liver-metastasis dataset is described as available from the authors on request.

Access, licence, data structure, and reproducibility requirements must be checked before use.

## 2. COMPASS (2026)

Shen W et al. *Generalizable AI predicts immunotherapy outcomes across cancers and treatments.* Nature Medicine. DOI: https://doi.org/10.1038/s41591-026-04502-7

### Relevance
COMPASS predicts immune-checkpoint-inhibitor response from bulk tumour transcriptomes using biologically grounded immune concepts. The paper reports evaluation across 16 clinical cohorts and comparison with 22 methods, including leave-one-cohort-out and cohort-to-cohort transfer evaluations.

### Implication
Generalization across cohorts, response prediction, interpretable immune concepts, and transfer evaluation are already active areas. A proposal limited to “make the model generalize across cohorts” would be inadequate.

### Resources
- Article: https://www.nature.com/articles/s41591-026-04502-7
- Verify the official code repository, licence, data access, and computational requirements during the audit.

## 3. Robust counterfactual explanations (2024 survey)

Jiang J, Leofante F, Rago A, Toni F. *Robust Counterfactual Explanations in Machine Learning: A Survey.* Proceedings of IJCAI 2024. DOI: https://doi.org/10.24963/ijcai.2024/894

### Relevance
This survey reviews robustness of counterfactual explanations, including robustness to model changes, model multiplicity, noisy execution, and input changes. It discusses established metrics such as validity after retraining.

### Implication
Counterfactual robustness is already a well-developed general ML topic. A contribution must be more specific than “make counterfactuals robust.” We must test whether cancer-immunotherapy target combinations introduce a distinct problem that existing methods do not adequately cover.

## 4. Stability of feature attribution in oncology (2026 issue; online 2025)

Takefuji Y. *Stability of feature attribution: Contrasting supervised and unsupervised selection for radiopathomics and TCGA outcomes.* Cancer Letters. DOI: https://doi.org/10.1016/j.canlet.2025.218133

### Relevance
This paper studies stability of feature-selection/attribution results in oncology and highlights that prediction accuracy and stability of selected features are different properties.

### Implication
We cannot claim novelty merely by measuring stability of individual molecular features in cancer models. The audit must determine whether whole predicted intervention sets, intervention feasibility, and their out-of-sample biological objectives are treated differently in existing research.

## 5. Causal interpretation warning

Schölkopf et al. and related work on causal inference and counterfactual prediction in healthcare emphasize that predictive associations do not automatically identify causal intervention effects. One relevant overview is: https://www.nature.com/articles/s42256-020-0197-y

For this project, model-generated perturbations must be described as hypotheses unless supported by an appropriate causal design or experimental evidence.

## 6. Candidate methodological gap to verify

Investigate whether existing methods adequately assess **the joint reliability of complete predicted target combinations** in spatial tumour-immune data, across patient-level resampling and model perturbations, while also measuring biological plausibility and independent predictive validity.

This remains a candidate gap, not a verified one. The audit must compare:
- General robust-counterfactual methods.
- Stability-selection and feature-attribution methods.
- Methods for selecting sets or combinations of interventions.
- Uncertainty estimation and calibration.
- Patient-level dependence, spatial sampling, and data leakage.
- Experimental validation of predicted perturbations.

## 7. Questions for the next review pass

1. Does Morpheus already report target- and combination-level stability across resampled patients or retrained models?
2. Can general robust-counterfactual methods be applied to intervention sets, and what would remain missing in this cancer setting?
3. Are there published methods that directly evaluate the robustness of sets of molecular perturbations across resamples?
4. Does COMPASS or related immunotherapy work address analogous reliability questions?
5. Are at least two compatible independent datasets available, or should the study be framed as within-cohort robustness?
6. Can the baseline be reproduced with the available hardware and accessible data?

## 8. Preliminary conclusion

The broad idea is relevant, but novelty is **not established**. The literature already includes general counterfactual robustness and cancer feature-selection stability. We need a more precise comparison and dataset audit before deciding whether to proceed, refine, or pivot.
