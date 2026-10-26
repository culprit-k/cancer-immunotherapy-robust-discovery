# Targeted novelty landscape
**Date:** 2026-10-26. **Status:** targeted desk review, not a systematic review or novelty certification.

## Overall finding
A broad claim such as “AI discovers spatial biomarkers for HCC immunotherapy” is not defensible by itself. HCC spatial immunotypes, spatial niches, predictive biomarkers, and a general spatial-proteomics foundation model already exist. The future contribution must be a specific mathematical capability that can be disproven by strong baselines, not a pile-up of model components.

## High-priority prior work
1. **HCC spatial immunotypes:** Salié et al., Gut 2025, DOI 10.1136/gutjnl-2024-332837, describe depleted, compartmentalized and enriched spatial immune architectures associated with ICI outcomes, plus intratumour heterogeneity. This project's 42-patient ICI dataset comes from that study. Do not claim novelty for rediscovering those immunotypes or the broad immune-enrichment/outcome association. https://gut.bmj.com/content/74/3/451
2. **VirTues:** Gut et al., Nature 2026, DOI 10.1038/s41586-026-10884-y, describe a marker-aware, multi-scale spatial-proteomics foundation model with masked reconstruction, virtual marker prediction, niches and biomarker discovery. Generic transformer architecture, reconstruction, virtual staining and automated biomarker discovery are not sufficient novelty. https://www.nature.com/articles/s41586-026-10884-y
3. **Lymphoid-enriched HCC niche:** Cancers 2026, DOI 10.3390/cancers18213442, reports a lymphoid-enriched “Niche 9,” multi-omic support and a derived signature. It also notes limits around pooled spot-level response analysis and treatment-cohort mismatch in parts of the study. Generic lymphoid-niche discovery overlaps with this work. https://www.mdpi.com/2072-6694/18/21/3442
4. **FAP-alpha spatial biomarker:** npj Precision Oncology 2026, DOI 10.1038/s41698-026-01734-1, reports FAP-α-related spatial biomarker findings in HCC under lenvatinib plus tislelizumab. Do not promise to discover FAP or a generic CAF-resistance signal as the main novelty. https://www.nature.com/articles/s41698-026-01734-1
5. **Reporting standards:** TRIPOD+AI (BMJ 2024; DOI 10.1136/bmj-2023-078378) and REMARK (DOI 10.1093/jnci/djy088) support transparent reporting and validation; they are quality requirements, not novel contributions.

## Candidate gap to test—not yet validated
Robust, uncertainty-calibrated transfer of marker-aware spatial representations across panels and cohorts, with explicit separation of measured evidence, reconstruction estimates, outcome associations, and target hypotheses; incremental value must be tested beyond established immunotypes and simple spatial features.

This may still overlap with current research. Before choosing the final architecture, review VirTues code, supplementary methods and training-set manifests, then update the targeted literature search.

## Falsifiable primary hypothesis
A prespecified patient-level spatial representation, built without evaluation outcomes, improves a patient-level metric over established immunotype/CD8-spatial features and essential clinical covariates, while maintaining calibration and rank stability under realistic panel/missing-marker shifts.

The current cohort contains 42 patients and only five PR/binary-response-positive cases in the corrected extraction. It cannot support a large supervised model with credible internal performance estimation. Treat it as technical feasibility and clearly labelled exploration; external validation is necessary for stronger claims.

## Before claiming novelty
Record search strings, date, inclusion/exclusion rules, and extracted attributes for relevant papers: modality, patient count, endpoint, split unit, baselines, metrics, external validation, uncertainty, and experimental evidence. Review 2026/2027 papers again before submission. Narrow the claim if the evidence does not support it.

## Claim language
Until supported by experiments, say “candidate contribution” or “we propose to test.” Avoid “first,” “unprecedented,” “causal target,” “clinically useful,” or “state-of-the-art” without evidence. This document is not a patentability determination.
