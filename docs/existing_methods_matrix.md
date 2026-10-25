# Existing-method comparison matrix

**Purpose:** Track the closest methods and prevent overclaiming novelty. This matrix is preliminary and should be updated after reading full supplements and code.

| Method/paper | Data/modality | Main task | Already covers | Potentially unaddressed by that paper (to verify) |
|---|---|---|---|---|
| Morpheus (Nature Biomedical Engineering, 2025) | Spatial multiplexed tumour proteomics / IMC | Counterfactual molecular perturbations predicted to increase CD8+ T-cell infiltration | Patient-level train/validation/test split; per-patch counterfactuals; cohort-level combinations; in-silico test-patient evaluation; selected in-vitro validation | Repeated full discovery across patient/core resamples and retrained models with quantified full-combination stability, if not already in supplement/code |
| COMPASS (Nature Medicine, 2026) | Bulk tumour transcriptomes and clinical ICI cohorts | Predict ICI response across cohorts/cancers/treatments | Large cross-cohort response benchmark; biologically grounded concepts; generalization evaluation | Not a direct spatial-proteomic perturbation-combination discovery pipeline; its relevance is methodological overlap, not a drop-in comparator |
| Robust Counterfactual Explanations survey (IJCAI, 2024) | General ML methods | Robustness of counterfactual explanations | Model-change, model-multiplicity, noisy-execution, and input-change robustness; existing metrics and methods | Application-specific adaptation to structured spatial molecular intervention sets may be possible but must be shown to add more than routine application |
| Stability of Feature Attribution (Cancer Letters, 2026 issue) | Oncology feature attribution / radiopathomics and TCGA | Stability of feature selection/attribution | Shows prediction performance and feature stability differ | Whole intervention-set stability and spatial counterfactual objectives may differ, but this distinction requires verification |
| Uncertainty and counterfactual robustness (Expert Systems with Applications, 2026) | General ML tabular/synthetic benchmarks | Effects of aleatoric/epistemic uncertainty on counterfactual stability | Shows model uncertainty can substantially change counterfactuals | Cancer spatial target-set application may be distinct, but simple domain transfer alone is not strong novelty |
| PHAROS (bioRxiv preprint, September 2026) | Single-cell perturbation models and drug response data | Search/rank drug combinations that move cells toward a target state | Target-directed combination search; evaluation on two independent combinatorial perturbation datasets; exploratory patient-derived tumour analyses | Not the same spatial-proteomic task; we must avoid duplicating combination search and instead justify any distinct reliability evaluation |

## Preliminary assessment

No method in this matrix yet proves that the exact candidate question is already solved, but the overlap is substantial. **Status: refine and verify, not proceed to algorithm invention.**

A paper based only on applying bootstrap resampling and reporting Jaccard similarity might be too incremental. A stronger contribution would need a clear scientific reason why existing counterfactual robustness metrics are insufficient for spatial cancer intervention sets, plus evidence that the proposed evaluation changes conclusions or improves reliability.
