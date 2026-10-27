# Targeted novelty landscape
**Date:** 2026-10-26. **Status:** targeted desk review, not a systematic review, complete novelty certification, or patentability opinion.

## Overall finding
A broad claim such as “AI discovers spatial biomarkers for HCC immunotherapy” is not defensible by itself. HCC spatial immunotypes, spatial niches, predictive biomarkers, deep-learning analyses of HCC response, and a general spatial-proteomics foundation model already exist. The future contribution must be a specific mathematical capability that can be disproven by strong baselines, not a pile-up of model components.

## High-priority prior work
1. **HCC spatial immunotypes:** Salié et al., Gut 2025, DOI 10.1136/gutjnl-2024-332837, describe depleted, compartmentalized and enriched spatial immune architectures associated with ICI outcomes, plus intratumour heterogeneity. This project's 42-patient ICI dataset comes from that study. Do not claim novelty for rediscovering those immunotypes or the broad immune-enrichment/outcome association. https://gut.bmj.com/content/74/3/451
2. **VirTues:** Gut et al., Nature 2026, DOI 10.1038/s41586-026-10884-y, describe a marker-aware, multi-scale spatial-proteomics foundation model with masked reconstruction, virtual marker prediction, niches and biomarker discovery. Generic transformer architecture, reconstruction, virtual staining and automated biomarker discovery are not sufficient novelty. https://www.nature.com/articles/s41586-026-10884-y
3. **HCC spatial multi-omics/deep learning:** the 2025 preprint *Spatial multi-omics and deep learning reveal fingerprints of immunotherapy response and resistance in hepatocellular carcinoma* describes spatially co-registered profiling and deep-learning-based response/resistance analysis. This makes generic “spatial AI for HCC ICI response” positioning especially weak. https://pmc.ncbi.nlm.nih.gov/articles/PMC12259099/ and https://pubmed.ncbi.nlm.nih.gov/40661489/
4. **Tumour–lymphoid interface transfer:** a 2026 Zenodo record for *Tumor-lymphoid aggregate interface structures predict immunotherapy response in hepatocellular carcinoma* describes external H&E validation data from two sites. This is active work on translating a spatial HCC immune signature to routine histology. https://zenodo.org/records/21616771
5. **Prospective TACE + ICI multi-omics:** *Multi-omics-driven personalized management of advanced HCC*, Cell Reports Medicine 2026, DOI 10.1016/j.xcrm.2026.103085, reports prospective TACE plus sintilimab work, paired IMC and an external mIHC cohort. It differs in treatment context from the current Salié cohort but occupies the broad multi-omics-response space. https://doi.org/10.1016/j.xcrm.2026.103085
6. **Lymphoid-enriched HCC niche:** Cancers 2026, DOI 10.3390/cancers18213442, reports a lymphoid-enriched “Niche 9,” multi-omic support and a derived signature, while noting limits around pooled spot-level response analysis and treatment-cohort mismatch in parts of the study. Generic lymphoid-niche discovery overlaps with this work. https://www.mdpi.com/2072-6694/18/21/3442
7. **FAP-alpha spatial biomarker:** npj Precision Oncology 2026, DOI 10.1038/s41698-026-01734-1, reports FAP-α-related spatial biomarker findings in HCC under lenvatinib plus tislelizumab. Do not promise to discover FAP or a generic CAF-resistance signal as the main novelty. https://www.nature.com/articles/s41698-026-01734-1
8. **Reporting standards:** TRIPOD+AI (BMJ 2024; DOI 10.1136/bmj-2023-078378) and REMARK (DOI 10.1093/jnci/djy088) support transparent reporting and validation; they are quality requirements, not novel contributions.

## What the current dataset can support
The Salié 42-patient ICI cohort is a previously published cohort, not independent validation of the source paper's immunotypes. It has 42 patients and only five PR/binary-response-positive cases in the corrected extraction, and the source table's 84 ROIs differ from 86 listed image/mask triplets. It is therefore not a credible stand-alone dataset for training and internally validating a high-dimensional response predictor. Its more defensible use is an exposure-screened representation-transfer and reproducibility evaluation, with clinical response analyses exploratory unless a separate appropriate cohort is obtained.

The expanded VirTues checkpoints containing the Salié cohort must not be presented as independent on this dataset. The IMC-only checkpoint remains a candidate only after exact revision/hash, licence and accession-level training exposure are checked. The checkpoint's corpus size/technology composition also differs from the expanded checkpoint; score differences alone cannot identify exposure as the cause.

## Candidate gap to test—not yet validated
A defensible candidate is **checkpoint-exposure-aware and preprocessing-aware transfer evaluation**, with patient-level aggregation and uncertainty, testing whether spatial representations are stable and add information beyond predeclared conventional immune architecture features when used on a different normalized-input domain. The eventual broader target-discovery system may extend this foundation with robustness and evidence-triangulation, but those claims must be tested independently and cannot be inferred from a single cohort.

This candidate may still overlap with current research. Before choosing the final architecture, review VirTues code, supplementary methods and training-set manifests, and complete a reproducible search across literature/preprints.

## Falsifiable hypothesis for the current HCC work
After all compatibility and provenance gates pass, a frozen, HCC-excluded IMC checkpoint will yield patient-level representations whose stability and concordance with established spatial immune features can be evaluated against simple baselines. Any claim of incremental clinical information must be evaluated without tuning on the held-out cohort and with uncertainty. The hypothesis may fail.

## Before claiming novelty
Record search strings, date, inclusion/exclusion rules, and extracted attributes for relevant papers: modality, cohort and patient count, endpoint, split unit, baselines, metrics, external validation, uncertainty, and experimental evidence. Re-check newer publications/preprints immediately before submission. Narrow the claim if the evidence does not support it.

## Claim language
Until supported by experiments, say “candidate contribution” or “we propose to test.” Avoid “first,” “unprecedented,” “causal target,” “clinically useful,” or “state-of-the-art” without evidence. Computational feature attribution, association, and simulated perturbation are not evidence of causal therapeutic efficacy.


## Fresh overlap check — VirTues published in Nature, 5 August 2026

The literature landscape must now treat VirTues as a published Nature foundation model, not only a preprint. The Nature methods explicitly include the Salié HCC ICI cohort among seven additional IMC cohorts used in the expanded multi-technology corpus. This rules out a broad novelty claim framed as “applying VirTues/spatial AI to the same HCC cohort” without a more specific methodological contribution, and it rules out `virtues-sp32` for held-out HCC evaluation. The current methodological angle remains a hypothesis: auditable checkpoint-exposure control, preprocessing-domain robustness, patient-level aggregation and uncertainty reporting. It is not yet established as novel or first; it requires a focused search against other 2025–2026 work.

Source: [Wenckstern et al., The Virtual Tissues foundation model resolves spatial proteomics across scales, Nature (2026)](https://www.nature.com/articles/s41586-026-10884-y). The HCC cohort was cited within the paper's description of the additional IMC datasets in the extended corpus.
