# Existing-method comparison matrix

**Purpose:** compare the closest methods to avoid overclaiming novelty. This remains a targeted, non-exhaustive audit; the full Morpheus supplement has not yet been read.

| Method/paper | Data / task | Already covers | What might differ from our candidate (must be verified) |
|---|---|---|---|
| Morpheus (Nature Biomedical Engineering, 2025) | Spatial IMC tumour proteomics; counterfactual changes predicted to increase CD8+ T-cell infiltration | Patient-level splits; per-patch counterfactuals; constraints on whole-image perturbations; median aggregation into tumour strategies; in-silico held-out-patient evaluation; sensitivity to sparsity; selected in-vitro validation; discussion of within-patient sample variation | Repeated full discovery over patient/core-grouped resamples and multiple retrained model seeds, with complete signed target-set reliability metrics associated with held-out patient-level predicted uplift at a matched target budget. Supplement is not yet audited, so this is not a confirmed absence. |
| PHAROS (bioRxiv preprint, September 2026) | Single-cell perturbation model; target-directed drug-combination search | Sequential combination discovery; independent combinatorial data evaluation; controls; sampled source/target batches; robustness-aware re-ranking | Uses a different single-cell model/task and not spatial IMC patient/core data. Simple combination search, sampling, or robustness reranking is not a distinctive contribution. |
| COMPASS (Nature Medicine, 2026) | Bulk tumour transcriptomes and clinical immunotherapy cohorts; response prediction | Large multi-cohort response benchmark, multiple treatments/cancers, cross-cohort generalization | Not a direct spatial counterfactual intervention-set discovery pipeline. Relevant as generalization precedent, not a drop-in benchmark. |
| Jiang et al. (IJCAI 2024), robust-counterfactual survey | General machine learning | Robustness under input/model changes, model multiplicity and noisy execution; existing methods and metrics | Application-specific spatial/patient hierarchy might differ, but simply applying generic metrics is unlikely to establish novelty. |
| Takefuji (Cancer Letters, 2026 issue / online 2025), feature-attribution stability | Oncology feature attribution/selection in radiopathomics and TCGA | Shows attribution/selection stability in oncology is already studied | Whole intervention-set robustness is not identical to feature attribution stability; distinction must be operationally and empirically justified. |
| Christodoulou & Sun (Expert Systems with Applications, 2026), uncertainty and counterfactual robustness | General tabular/synthetic counterfactual settings | Examines how uncertainty impacts counterfactual stability | A cancer application alone is not enough; must show a meaningful methodological contribution. |

## Working distinction to test

Not “discover robust cancer targets” in general. Test whether, for spatial-proteomic counterfactual intervention sets, patient/core sampling variability and retraining variability can be separated, and whether the resulting stability information predicts how reproducible the model-predicted benefit is in untouched patients.

Primary baselines to implement, if the reproduction gate passes:
1. the published Morpheus single-run/median-strategy baseline;
2. a simple frequency/rank consensus over repeated discovery runs;
3. target-budget-matched random or sign controls where technically valid;
4. a no-change reference.

Report target-set size and signed direction as well as selection frequency and Jaccard similarity. A tiny/empty set can look stable, and stable predictions can still be wrong. All claimed uplift must remain labelled model-predicted unless there is independent experimental evidence.

## Decision

**HIGH-RISK / UNVERIFIED.** The exact candidate may be testable, but no novelty conclusion is justified yet. Full supplement inspection, targeted prior-art search and baseline reproduction are mandatory before method development.
