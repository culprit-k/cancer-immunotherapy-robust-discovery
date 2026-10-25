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
- Publicly listed code repository in the article/resources: verify repository identity, licence, data access, and computational requirements during the audit.

## 3. Candidate methodological gap to verify

Investigate whether existing methods adequately measure the stability of *complete counterfactual therapeutic combinations* under patient-level resampling and modelling choices, while separately evaluating external generalization and uncertainty.

This is only a candidate gap. The audit must include prior work on:
- Counterfactual explanation robustness and validity.
- Stability selection and feature-selection stability.
- Set-valued or combination-level recommendation stability.
- Uncertainty estimation and calibration in biomedical ML.
- Spatial sampling, patient-level dependence, and data leakage.
- Independent validation of perturbation-based therapeutic hypotheses.

## 4. Questions for the next review pass

1. Does Morpheus already report relevant target- and combination-level stability analyses?
2. Do related counterfactual methods quantify uncertainty or stability of recommended interventions?
3. Are there published methods that directly evaluate the robustness of sets of perturbations across resamples?
4. Does COMPASS address any analogous reliability question that makes our planned contribution redundant?
5. Are at least two compatible independent datasets available, or should the study be framed as within-cohort robustness rather than cross-cohort validation?
6. Can the baseline be reproduced with the available hardware and accessible data?

## 5. Preliminary conclusion

The broad idea is relevant, but novelty is **not established**. The next step is a targeted review of the specific stability/robustness methods and a dataset feasibility audit before committing to an algorithm.
