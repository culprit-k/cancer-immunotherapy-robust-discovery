# HCC biological prior-art and independent-validation gate

**Date:** 2026-10-27  
**Status:** targeted audit; not a systematic review. No new biological result established.

## Decision

The current Salié HCC imaging cohorts are suitable for a reproducible exploratory reanalysis, but they cannot by themselves support a strong novelty claim about broad immune architecture, spatial T-cell/myeloid neighbourhoods, or ICI response. The source publication already analysed those subjects in these same cohorts. The primary biological claim therefore needs to be narrower than “spatial organization determines immunotherapy response,” and any promising result must be tested against independent evidence.

## Relevant published work we must not rediscover

1. **Salié et al., Gut (2025), “Spatial single-cell profiling and neighbourhood analysis reveal the determinants of immune architecture connected to checkpoint inhibitor therapy outcome in hepatocellular carcinoma.”** This paper defined depleted, compartmentalized and enriched HCC immunotypes, spatial neighbourhoods, and clinical associations in the discovery and ICI cohorts that we currently audit. The public Zenodo records (DOIs 10.5281/zenodo.10793609 and 10.5281/zenodo.10794904) describe 54 and 42 HCC patients respectively. Our reanalysis of these images is not independent validation of those claims.  
   Sources: https://gut.bmj.com/content/74/3/451 ; https://zenodo.org/records/10793609 ; https://zenodo.org/records/10794904

2. **Ruf et al., Cell (2023), “Tumor-Associated Macrophages Trigger MAIT Cell Dysfunction at the HCC Invasive Margin.”** The paper used CODEX imaging, cellular profiling and experiments to identify a role for CSF1R+/PD-L1+ tumour-associated macrophages in MAIT-cell dysfunction near the tumour-to-liver interface. The related CODEX-IMAGING-OF-HCC collection is listed by TCIA. This is a possible independent imaging cohort for replication or for testing a genuinely different hypothesis; the macrophage–MAIT interaction itself is already published and cannot be presented as our discovery.  
   Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC10461130/ ; https://doi.org/10.7937/BH0R-Y074

3. **SPARC (2025 preprint), “Spatial multi-omics and deep learning reveal fingerprints of immunotherapy response and resistance in HCC.”** The work reports immune/lymphoid aggregate interfaces and extracellular-matrix-associated patterns related to response. Generic claims about lymphoid aggregates separated from tumour by ECM are therefore crowded prior art.  
   Source: https://pubmed.ncbi.nlm.nih.gov/40661489/

4. **Fang et al., npj Precision Oncology (2026), “Spatial proteomics identifies stromal FAP-α as a predictive biomarker for therapeutic efficacy in HCC.”** This study reports FAP-α enrichment in nonresponders and associations with M2-type macrophages and reduced T-cell infiltration, with mIF and IHC validation. The current 45-channel ICI panel does not contain FAP-α, so we cannot claim to measure it directly using this panel.  
   Source: https://doi.org/10.1038/s41698-026-01734-1

5. **“A Lymphoid-Enriched Spatial Immune Niche Defines an Immunotherapy-Responsive State in HCC” (Cancers, 2026).** This recent multi-omics paper reports a lymphoid-enriched niche and links a niche-derived programme to immunotherapy response across multiple cohorts. Another generic lymphoid-niche discovery would not be sufficiently novel.  
   Source: https://doi.org/10.3390/cancers18213442

## What remains testable

The current project can test whether a carefully defined **cell-state-conditioned spatial relationship** contributes information beyond total marker abundance, known immunotype and additive marker models. Our prototype feature is a continuous association between a cytotoxic-associated marker-state score and neighbouring myeloid-associated marker-state scores, compared with within-ROI spatial shuffles. This is only a measurement candidate. It is not yet a validated cell-type interaction, causal mechanism or novel discovery.

The analysis must:
- use a source-verified marker-to-plane map and mask codebook;
- compute spatial measurements without viewing ICI outcomes;
- aggregate ROIs to patient-level measurements before outcome inference;
- compare with simple marker-abundance and additive baselines;
- quantify uncertainty, multiple testing and leave-one-patient-out influence;
- use an independent cohort or orthogonal experiments before strong claims.

The 42-patient ICI cohort has only five PR cases in the extracted clinical table. It cannot support a high-dimensional PR classifier. The unresolved 84-versus-86 ROI discrepancy for ICI_24 and ICI_39 must be resolved from authoritative source records or handled by a frozen outcome-independent exclusion rule. Survival modelling must wait for source verification of the event/censor coding.

## Independent validation routes

- **TCIA CODEX-IMAGING-OF-HCC / Ruf et al.**: potentially useful for independent imaging-level reproducibility, but it does not automatically give independent immunotherapy-outcome validation; the TAM–MAIT biology is already known. Confirm exact sample count, available channels, terms, and annotation files before analysis. The collection is very large, so feasibility/storage must be assessed before downloading.
- **Fang et al. 2026 HCC cohort**: clinically relevant independent treatment cohort (86 patients receiving lenvatinib plus tislelizumab, with mIF and IHC validation cohorts described by the paper). No publicly accessible raw spatial data/feature table has yet been verified in this audit; contact authors or inspect supplements/data statements before treating it as obtainable.
- **Spora**: the HCC entry `salie2025spatial` is the same Salié study and is not independent of our current cohort. Its other HCC entry `ruf2023tumor` is the Ruf et al. collection above, not a new unstudied cohort.

## Go/no-go

**GO** for outcome-blind feature extraction and exploratory patient-level testing after data contracts pass.  
**NO-GO** for claiming a novel biological interaction, independent ICI validation, causality, clinical utility or patentability until the above evidence and cohort gates are satisfied.

A null result or failure to improve on the published phenotype and simple baselines is a valid research outcome. Do not tune the feature definition to maximise a result on the external outcome cohort.
