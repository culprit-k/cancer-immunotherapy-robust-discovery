# Initial literature audit

**Status:** Preliminary. This is a starting point, not a systematic review or exhaustive prior-art search.

## 1. Morpheus (2025)

Wang ZJ et al. *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles.* Nature Biomedical Engineering. DOI: https://doi.org/10.1038/s41551-025-01357-0

### Relevance
Morpheus predicts CD8+ T-cell presence from spatial multiplexed tumour images and uses counterfactual optimization to propose molecular perturbations associated with increased predicted T-cell infiltration. It applies the method to 159 image cores from 69 metastatic melanoma patients and 209 cores from 30 colorectal cancer liver-metastasis patients. Selected predictions were tested in vitro.

### Existing analyses relevant to our idea
- Patients are divided into training, validation, and test groups.
- Perturbations are generated per image patch and analyzed across patients.
- The authors describe variability across tissue samples, including different samples from the same patient.
- The discussion proposes deriving perturbations from a subset of a patient's samples and testing on remaining samples as future work.

### Implication
We cannot claim novelty for patient-level splits, counterfactual molecular perturbation, patient variation, or in-vitro validation. A possible narrower question is whether repeated full target-discovery runs under patient-level resampling and model changes can be evaluated systematically for complete-combination stability, beyond the analyses already reported. This needs further verification against the full supplement and code.

### Resources
- Paper: https://doi.org/10.1038/s41551-025-01357-0
- Reproduction repository: https://github.com/cellethology/morpheus-spatial
- Model/package code: https://github.com/neonine2/morpheus-spatial
- Melanoma dataset cited by paper: https://doi.org/10.5281/zenodo.5994135
- Original melanoma data-for-analysis deposit: https://doi.org/10.5281/zenodo.5994136
- Preprocessed data and model outputs cited by paper: https://doi.org/10.22002/pr14s-wgk05

## 2. COMPASS (2026)

Shen W et al. *Generalizable AI predicts immunotherapy outcomes across cancers and treatments.* Nature Medicine. DOI: https://doi.org/10.1038/s41591-026-04502-7

COMPASS predicts immune-checkpoint-inhibitor response from bulk tumour transcriptomes using biologically grounded immune concepts. The paper reports evaluation on 1,133 patients from 16 clinical cohorts and comparison with 22 methods.

### Implication
Generalization across cohorts, response prediction, interpretable immune concepts, and transfer evaluation are already active areas. A proposal limited to “make the model generalize across cohorts” would be inadequate. COMPASS is a complementary benchmark, not a directly interchangeable dataset for spatial-proteomic counterfactual perturbation discovery.

## 3. Robust counterfactual explanations (IJCAI 2024)

Jiang J, Leofante F, Rago A, Toni F. *Robust Counterfactual Explanations in Machine Learning: A Survey.* IJCAI 2024. DOI: https://doi.org/10.24963/ijcai.2024/894

This survey documents established approaches to counterfactual robustness under model changes, model multiplicity, noisy execution, and input changes. It describes measures such as validity after retraining.

### Implication
Counterfactual robustness is an established general ML topic. Any proposed method must be compared with existing robust-counterfactual approaches, not just a standard baseline.

## 4. Stability of feature attribution in oncology (2026 issue; online 2025)

Takefuji Y. *Stability of feature attribution: Contrasting supervised and unsupervised selection for radiopathomics and TCGA outcomes.* Cancer Letters. DOI: https://doi.org/10.1016/j.canlet.2025.218133

This paper investigates feature-selection/attribution stability in oncology and demonstrates that prediction accuracy and stability of selected features are different properties.

### Implication
A generic cancer-feature-stability score would not establish novelty. We need to identify a specific unmet need in the reliability of full therapeutic intervention sets.

## 5. Counterfactual uncertainty (2026)

Christodoulou L, Sun C. *The impact of machine learning uncertainty on the robustness of counterfactual explanations.* Expert Systems with Applications (2026). DOI: https://doi.org/10.1016/j.eswa.2026.131198

This work studies how aleatoric and epistemic uncertainty affect counterfactual explanations, reporting that accuracy alone does not ensure stable explanations. It is not cancer-specific but is directly relevant methodological prior art.

## 6. Candidate methodological gap to verify

Investigate whether existing methods adequately assess **the joint reliability of complete predicted molecular target combinations** in spatial tumour-immune data across patient-level resampling and model retraining, with separate assessment of:
- selection stability of individual targets and complete sets;
- predicted objective and uncertainty;
- generalization to held-out patients or compatible independent cohorts;
- biological plausibility and independent experimental evidence, where available.

This remains a candidate gap, not a verified one. Morpheus already has patient-level splits and discusses within-patient tissue variability, so we must establish exactly what its supplement and implementation do before proceeding.

## 7. Next review questions

1. Does Morpheus's full supplement quantify target/combination stability under patient resampling or model retraining?
2. Does the public reproduction notebook expose the full discovery pipeline and saved split metadata?
3. Can the proposed analysis be implemented with available preprocessed files, and what compute is required?
4. Do robust-counterfactual methods generalize to structured multi-target molecular interventions, or would adapting them be the contribution?
5. Is there an appropriate independent dataset with compatible spatial-proteomic markers and endpoints?
6. Is the proposed gap distinct enough to justify a paper, or should we pivot to a more defensible cancer question?

## Preliminary conclusion

The direction is scientifically relevant, but novelty is **not established**. The current best next step is a reproducibility and dataset feasibility check plus a focused comparison of complete-intervention-set robustness methods. We should proceed only if this produces a distinct, testable contribution.
