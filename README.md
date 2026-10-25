# Cancer Immunotherapy AI: Robust Target Discovery

**Project status (25 October 2026): conditional GO for a small feasibility pilot; no verified novelty claim, new algorithm, therapeutic effect, or patentability conclusion.**

## Current research candidate

**Patient-Level Reproducibility of Spatial-Proteomic Counterfactual Target Combinations for Cancer Immunotherapy**

Primary question: Across patient-grouped resamples and model seeds, how reproducible are spatial-proteomic counterfactual target sets, and does a prespecified stability-aware consensus improve held-out-patient **model-predicted** CD8+ infiltration uplift over the reproduced published median-strategy baseline at a matched target budget?

This is a candidate research question—not a confirmed literature gap. Morpheus already performs counterfactual target discovery, patient-level splitting, median aggregation and held-out-patient in-silico evaluation, with selected in-vitro validation. PHAROS (a September 2026 preprint) already searches target-directed drug combinations and uses sampled batches/robustness-aware re-ranking. A bootstrap/Jaccard score or “AI for cancer” alone would not be a strong novelty claim.

## Research gate decision

- **Conditional GO:** verify data/code rights, read the complete Morpheus supplementary PDF, reproduce at least one baseline result, and test a small feasibility subset.
- **Not cleared for full method development yet:** the separate supplement has not been read; the original data/model pipeline has not been executed; the proposed gap remains unverified.
- **Scientific boundary:** model-predicted uplift is not observed therapeutic effect, causal evidence, clinical utility, or patient-specific treatment advice.

## Work completed in this repository

- First-pass paper, public-code, notebook, dataset and prior-method audits.
- Written decision-gate protocol and reproducibility run log.
- Patient-aware evaluation helpers: target selection frequency, pairwise Jaccard for complete sets, signed-target direction consistency, patient-equal-weight predicted uplift, and patient-level bootstrap confidence intervals.
- Six synthetic unit tests for those generic helper functions; local result: **6 passed**. These tests do not reproduce or validate Morpheus or any biological hypothesis.
- No raw data have been committed.

## Next steps, in order

1. Retrieve/read the full supplementary PDF and confirm usage terms for the exact data and code.
2. Get the public tutorial/preprocessed artifacts in a network-enabled environment; record versions and checksums.
3. Reproduce a published baseline and measure runtime on a small subset.
4. Run cached-output resampling only as an explicitly descriptive first pilot; then separately run full discovery/retraining across patient-grouped resamples and model seeds if compute permits.
5. Evaluate every strategy on untouched patients and compare with prespecified baselines at a matched target budget.

## Repository map

- [Research question](docs/research_question.md)
- [Initial literature review](docs/literature_review.md)
- [Novelty assessment](docs/novelty_assessment.md)
- [Existing-method comparison matrix](docs/existing_methods_matrix.md)
- [Morpheus code audit](docs/morpheus_code_audit.md)
- [Dataset feasibility and permissions](docs/dataset_audit.md)
- [Prespecified analysis plan](docs/analysis_plan.md)
- [Decision-gate protocol](docs/decision_gate_protocol.md)
- [Reproducibility run log](docs/reproducibility_run_log.md)
- [Analysis helper functions](analysis/target_stability.py)
- [Unit tests](tests/test_target_stability.py)
- [Data handling policy](data/README.md)

## Initial literature and artifacts

1. Wang et al. (2025). *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles.* Nature Biomedical Engineering. https://doi.org/10.1038/s41551-025-01357-0
2. Shen et al. (2026). *Generalizable AI predicts immunotherapy outcomes across cancers and treatments.* Nature Medicine. https://doi.org/10.1038/s41591-026-04502-7
3. PHAROS (bioRxiv preprint, September 2026): https://www.biorxiv.org/content/10.64898/2026.09.08.749477v1.full
4. Original melanoma IMC data-for-analysis record: https://doi.org/10.5281/zenodo.5994136
5. Morpheus code and tutorial: https://github.com/cellethology/morpheus-spatial

## Data and intellectual property

Do not upload raw or restricted data to GitHub. The original melanoma data record's license field was not clear in this audit; verify reuse rights for the exact artifact. The article's CC BY-NC-ND license does not automatically license separate dataset or code assets.

This repository is public. If later work appears genuinely inventive, get qualified institutional/IP advice before disclosing enabling details. No claim about patentability is made here.
