# Cancer Immunotherapy AI: Robust Target Discovery

**Project status (25 October 2026): NO-GO for the generic robustness-only paper as currently phrased; conditional GO to investigate a more specific comparative or transfer question. No novel method or therapeutic effect has been established.**

## Current research area

Cancer immunotherapy target discovery using computational models.

The first proposed paper was to measure how spatial-proteomic counterfactual target sets vary across patient-grouped resamples and model seeds. That is still a useful reproducibility audit, but it no longer looks strong enough by itself as a high-novelty paper: Morpheus (2025) already does spatial counterfactual target discovery and held-out-patient evaluation; PHAROS (a September 2026 preprint) searches target-directed combinations with sample-based robustness-aware reranking; a MICCAI 2026 method evaluates counterfactual spatial-cell influence with core-level bootstrap; and SPAD-CFR (Biology, 2026) proposes spatial counterfactual tissue reprogramming including melanoma immune-focused interventions.

## Current decision

- **No-go:** presenting bootstrap, Jaccard similarity, or repeated Morpheus runs alone as a novel algorithm.
- **Conditional next step:** investigate whether a more substantive question about cross-method intervention decision utility or cross-cohort/platform transfer is feasible with compatible data and endpoints.
- **Pilot may proceed for feasibility/familiarization:** use a small permitted tutorial/preprocessed artifact to reproduce a baseline, but the pilot is not evidence of novelty.
- **Scientific boundary:** model-predicted uplift is not observed therapeutic effect, causal evidence, clinical utility, or patient-specific treatment advice.

## Work completed in this repository

- First-pass literature, paper Methods, public-code, notebook, dataset and prior-method audits.
- Updated prior-art addendum for recent spatial counterfactual methods.
- Novelty assessment now explicitly records a no-go decision for the current generic robustness-only framing.
- Pivot candidates and a decision tree for choosing a stronger question.
- Written decision-gate protocol and reproducibility run log.
- Generic analysis helpers: target selection frequency, pairwise/full-set Jaccard, signed-direction consistency, patient-equal-weight predicted uplift, and patient-level bootstrap confidence intervals.
- Six synthetic unit tests for those helpers; recorded local result: **6 passed**. These tests validate generic metric code only—not Morpheus, its data, or a biological hypothesis.
- No raw data have been committed.

## Next steps, in order

1. Finish reading the full Morpheus supplementary PDF. Its download redirect could not be retrieved in the current execution environment.
2. Verify reuse terms for the exact code/data artifacts and build a dataset/method compatibility table.
3. Compare Candidate A (cross-method intervention decision utility) and Candidate B (cross-cohort/platform transfer) against current prior art.
4. If a small permitted tutorial bundle is obtainable in a network-enabled environment, reproduce a published baseline and record compute needs.
5. Select one primary question only after the compatibility/prior-art gate passes.

## Repository map

- [Research question and revised scope](docs/research_question.md)
- [Initial literature review](docs/literature_review.md)
- [Novelty assessment](docs/novelty_assessment.md)
- [Existing-method comparison matrix](docs/existing_methods_matrix.md)
- [October 2026 related-work addendum](docs/related_work_addendum_2026.md)
- [Pivot candidates](docs/pivot_candidates.md)
- [Morpheus code audit](docs/morpheus_code_audit.md)
- [Dataset feasibility and permissions](docs/dataset_audit.md)
- [Prespecified analysis plan](docs/analysis_plan.md)
- [Decision-gate protocol](docs/decision_gate_protocol.md)
- [Reproducibility run log](docs/reproducibility_run_log.md)
- [Analysis helper functions](analysis/target_stability.py)
- [Unit tests](tests/test_target_stability.py)
- [Data handling policy](data/README.md)

## Key prior-art links

1. Morpheus (2025), *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles*: https://doi.org/10.1038/s41551-025-01357-0
2. PHAROS (bioRxiv preprint, September 2026): https://www.biorxiv.org/content/10.64898/2026.09.08.749477v1.full
3. Anzum et al., MICCAI 2026, *A Counterfactual Framework for Directional Cell-Cell Interaction Analysis in Spatial Transcriptomics*: https://papers.miccai.org/miccai-2026/0006-Paper6105.html
4. Ding et al., Biology 2026, *Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments*: https://doi.org/10.3390/biology15141097
5. Original melanoma IMC data-for-analysis record: https://doi.org/10.5281/zenodo.5994136

## Data and intellectual property

Do not upload raw or restricted data to GitHub. The original melanoma data record's license field was not clear in this audit; verify reuse rights for the exact artifact. The article's CC BY-NC-ND license does not automatically license separate dataset or code assets.

This repository is public. If later work appears genuinely inventive, get qualified institutional/IP advice before disclosing enabling details. No patentability claim is made.
