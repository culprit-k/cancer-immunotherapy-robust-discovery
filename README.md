# Cancer Immunotherapy AI: Robust Target Discovery

**Project status:** Phase 1 — literature and feasibility audit. No novel method or therapeutic effect has been established yet.

## Research direction

We are investigating whether a reproducible computational framework can evaluate the **robustness of predicted cancer immunotherapy target combinations** across patient-level resampling, independent cohorts, and reasonable modelling choices.

### Provisional research question

When computational models propose molecular target combinations associated with improved antitumour immune activity, can a robustness-aware evaluation distinguish recommendations that remain stable across patient samples and modelling assumptions from recommendations that are fragile or poorly supported?

This is a hypothesis to investigate, not a verified literature gap or a claim of novelty.

## Why this requires a careful audit

- **Morpheus (2025)** already uses counterfactual learning on spatial tumour-protein data to propose perturbations associated with increased T-cell infiltration, with selected experimental validation.
- **COMPASS (2026)** already evaluates immunotherapy-response prediction across multiple clinical cohorts and models, including cross-cohort transfer.
- Therefore, neither counterfactual target discovery nor cross-cohort prediction alone is sufficient to establish novelty.

Our potential contribution must be compared directly with existing work on counterfactual robustness, feature-selection stability, combination-level stability, uncertainty quantification, and external validation.

## Planned workflow

1. Audit the literature and document overlapping methods.
2. Verify dataset access, patient identifiers, features, metadata, licensing, and sample sizes.
3. Reproduce a published baseline before proposing modifications.
4. Define patient-level resampling and leakage-safe evaluation.
5. Prespecify metrics and comparison criteria before examining final results.
6. Report negative results, limitations, and uncertainty honestly.

## Reproducibility principles

- Split by patient, not by correlated image patches or samples from the same patient.
- Keep discovery and evaluation data separated.
- Record data versions, preprocessing, random seeds, software versions, and experiment configurations.
- Do not interpret model stability as proof of biological causality or clinical efficacy.
- Do not upload restricted, identifiable, or unlicensed data.

## Initial literature

1. Wang et al. (2025). *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles.* Nature Biomedical Engineering. https://doi.org/10.1038/s41551-025-01357-0
2. Shen et al. (2026). *Generalizable AI predicts immunotherapy outcomes across cancers and treatments.* Nature Medicine. https://doi.org/10.1038/s41591-026-04502-7

## Repository map

- [Research question](docs/research_question.md)
- [Initial literature audit](docs/literature_review.md)
- [Novelty assessment](docs/novelty_assessment.md)
- [Dataset feasibility audit](docs/dataset_audit.md)
- [Preliminary analysis plan](docs/analysis_plan.md)
- [Data handling policy](data/README.md)

## Important status note

This repository records a research programme under development. It does not claim that a new algorithm has already been invented, that any target is therapeutically effective, or that the proposed method is patentable. The literature audit is preliminary and must be expanded before the study protocol is finalized.

This repository currently has no software license. Public visibility itself can still disclose information, so consider patent/IP implications before adding enabling technical details.
