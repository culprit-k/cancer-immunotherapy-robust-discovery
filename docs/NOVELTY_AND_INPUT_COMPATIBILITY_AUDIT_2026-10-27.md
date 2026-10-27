# Novelty, data compatibility, and publication-scope audit
**Date:** 2026-10-27  
**Status:** Evidence audit; no HCC model inference or biological findings.

## Decision

The defensible candidate paper is **not** “AI finds immune-evasion targets” in the broad sense. Counterfactual spatial-proteomics target perturbation has already been demonstrated by Morpheus (Wang et al., *Nature Biomedical Engineering*, 2025), and spatial counterfactual generation has expanded to diffusion/point-cloud methods in SPAD-CFR (Ding et al., *Biology*, 2026). VirTues (Nature, 2026) already targets generalization across marker panels/cohorts and spatial biomarker discovery.

The potential contribution here is a predeclared, patient-level evaluation of how stable and transportable pretrained-model-derived spatial perturbation hypotheses are in HCC, including negative findings, sensitivity to preprocessing/panel choice, and independent-cohort testing—only if the model/data gates pass and empirical results support it. We must not claim a new causal mechanism from observational images.

## Literature that materially constrains the novelty claim

1. **VirTues foundation model.** Wenckstern et al., *The Virtual Tissues foundation model resolves spatial proteomics across scales*, Nature 657, 744–754 (2026), DOI https://doi.org/10.1038/s41586-026-10884-y. The paper describes a marker-aware foundation model using ESM-2 protein-sequence embeddings, zero-shot transfer across panels/platforms, virtual staining/reconstruction, cell analysis, spatial biomarker discovery and independent-cohort evaluation. Therefore, neither “foundation model for spatial proteomics” nor “cross-panel inference” is novel by itself.
2. **Morpheus counterfactual perturbations.** Wang et al., *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles*, Nature Biomedical Engineering 9, 390–404 (2025), DOI https://doi.org/10.1038/s41551-025-01357-0. The method trains a T-cell infiltration predictor and optimizes image-level counterfactual changes; its candidate combinations were validated with in-vitro migration experiments. Any novelty here must extend beyond generating combinations predicted to increase CD8-positive T-cell presence.
3. **SPAD-CFR spatial counterfactual generation.** Ding et al., *Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments*, Biology 15(14), 1097 (2026), DOI https://doi.org/10.3390/biology15141097. It uses spatial point-cloud attention and diffusion to alter molecular profiles and coordinates in counterfactual-style tissue simulations, including breast cancer and melanoma use cases. The authors explicitly caution that latent-state and exogenous-noise assumptions cannot be verified from observational data alone, so simulated interventions are hypotheses rather than proof of causality.
4. **Established HCC spatial immunotypes.** Salié et al., *Spatial single-cell profiling and neighbourhood analysis reveal the determinants of immune architecture connected to checkpoint inhibitor therapy outcome in hepatocellular carcinoma*, Gut (2024), DOI https://doi.org/10.1136/gutjnl-2024-332837. It established depleted, compartmentalised and enriched spatial immune architectures and associations with ICI outcomes in the discovery/validation cohorts used here. The present project must not frame re-identification of these categories as a new discovery.
5. **HCC PENGUIN input processing.** The Gut 2024 Methods report that images were spillover-compensated, converted to stacks with steinbock, hot-pixel filtered, then channel-normalized using PENGUIN to [0,1], with unspecific background removed and percentile-based noise reduction. Per-channel percentiles/thresholds were chosen by manual inspection and applied across ROIs. The same paper describes the stromal/parenchymal maps as produced by an ilastik random-forest classifier, and interface compartment maps as separately drawn. See the full article and Methods: https://gut.bmj.com/content/gutjnl/early/2024/09/30/gutjnl-2024-332837.full.pdf.
6. **Official VirTues preprocessing differs.** The VirTues paper says each image is clipped channel-wise at the 99th percentile, transformed with shifted log1p, standardized channel-wise using dataset-level means/standard deviations computed over tissue-mask pixels, then Gaussian-smoothed (kernel 3, unit variance). This is not the same pipeline as the HCC PENGUIN normalization. Applying VirTues preprocessing to already PENGUIN-normalized images would be a normalized-domain adaptation, not a reproduction of its training preprocessing.

## Data and model gates

### Already completed
- Public virtues-imc14 checkpoint identity verified in a real GitHub Actions runner: exact byte size 173,543,728, SHA-256 714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f, 356 tensors.
- Official VirTues source pinned to 2c9c6cba1ee796c4d8dff9329175c47e4a72f409; strict checkpoint load passed with no missing/unexpected keys.
- CPU packed-attention smoke test passed with the reversible SDPA fallback.
- Synthetic model forward passed with finite output and expected shape. Full report: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504248041 and artifact https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504248041/artifacts/12734062500.
- Marker embeddings width is correctly 640, matching checkpoint projection tensor (512, 640); input check now derives width from the checkpoint.

### Still unresolved and blocking HCC inference
1. **Channel order / marker identity:** validate the ordered plane-to-panel mapping from authoritative source metadata or tagged TIFF structure; do not infer it solely from equal counts or a sorted panel table. Map every measured target to an authoritative UniProt accession/sequence. The official VirTues README specifies per-target ESM-2 embeddings using esm2_t30_150M_UR50D; the 40 example embeddings are not proof that the 45-channel ICI panel is fully mapped.
2. **Mask semantics:** the public methods distinguish stromal/parenchymal maps and separately drawn interface maps. Numeric mask values observed in the files must not be assigned meaning without the authoritative label export/codebook; confirm how each mask corresponds to each sample and image.
3. **ICI ROI count discrepancies:** published Supplementary Table 3 reports 2 ROIs for ICI_24 and 1 ROI for ICI_39, while the archive filename inventory has 3 and 2 image ROI files. The paper table does not name the extra filenames; no ROI should be dropped by guesswork. Exclude these patients from outcome analysis until image-level identity is resolved.
4. **Panel-count discrepancy for the discovery cohort:** repository audit previously found 42 panel rows while the main paper describes a 41-plex panel. Reconcile whether the extra row is a non-protein/reference channel and document the actual image stack plane count and marker identities before using the discovery cohort.
5. **Input distribution:** normalized [0,1] images include background removal and per-channel threshold/percentile denoising; these operations are not invertible from the released images. No raw signal scale or exact per-channel PENGUIN parameters have yet been re-created from source records.
6. **Checkpoint exposure:** virtues-imc14 is preferable to the extended virtues-sp32 for this HCC evaluation because the published extended corpus includes Salié HCC data. The IMC-only checkpoint’s published corpus/reference inventory supports a preliminary non-exposure argument, not an accession-by-accession training certificate. Keep this limitation explicit.
7. **Licences:** discovery data are CC BY 4.0 and can be cited/used under that licence. The ICI dataset is publicly available and the article is CC BY 4.0, but confirm specific repository terms before redistributing data or derived files. VirTues IMC14 weights are CC BY-NC 4.0; do not upload the weights to GitHub.

## Publication route that is worth pursuing

### Primary endpoint
Patient-level stability of model-derived counterfactual candidate rankings under bootstrap resampling, preprocessing sensitivity settings and marker-panel restrictions. The ICI cohort remains external evaluation only and must not inform objective selection or tuning.

### Baselines and evaluation
- Use a patient-level split, never an ROI-level random split, for all outcome-linked analyses.
- Include simple spatial/channel-level baselines and a no-counterfactual control.
- For reconstruction pilots, report per-marker held-out MAE/RMSE against withheld pixels/channels, alongside baseline performance and patient-level variability.
- For candidate stability, report selection frequency, rank correlation and top-k set overlap across patient bootstrap samples and sensitivity settings, with uncertainty intervals.
- Report null/unstable candidates and negative outcomes. Do not infer causality, clinical benefit, druggability or patentability from predicted perturbations alone.
- Because the ICI cohort contains only 42 patients and few response-positive patients (five PR in the current extraction), avoid a high-dimensional supervised response model; outcome findings should be exploratory and patient-level.

### Go/no-go
- **GO:** outcome-blind structural QC and marker mapping are complete; strict synthetic preflight passes (done); preprocessing mode is explicitly declared; first held-out reconstruction pilot beats predeclared baselines; cross-cohort stability can be evaluated without using external outcomes for tuning.
- **NO-GO:** if panel mapping, stromal semantics, patient/ROI identity or input distribution remains ambiguous, do not label a VirTues result as official inference or publish biological target claims. A separately labelled normalized-domain adaptation may be considered only after the remaining identity/mask gates are closed and its input assumptions are documented.

## Source links
- VirTues (Nature 2026): https://doi.org/10.1038/s41586-026-10884-y
- Morpheus (Nat Biomed Eng 2025): https://doi.org/10.1038/s41551-025-01357-0
- SPAD-CFR (Biology 2026): https://doi.org/10.3390/biology15141097
- HCC spatial immunotypes (Gut 2024): https://doi.org/10.1136/gutjnl-2024-332837
- Discovery cohort: https://doi.org/10.5281/zenodo.10793609
- ICI cohort: https://doi.org/10.5281/zenodo.10794904
- PENGUIN: https://doi.org/10.1016/j.csbj.2024.10.048

**Scope note:** This is an analysis/novelty audit, not a results paper. As of this revision, no HCC reconstruction experiment, counterfactual, target ranking or clinical prediction has been run.
