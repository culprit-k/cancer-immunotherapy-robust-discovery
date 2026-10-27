# Targeted prior-art update — 27 October 2026

**Review type:** targeted web and article-methods audit, not a PRISMA systematic review.  
**Decision:** generic spatial counterfactual discovery, marker reconstruction, downstream prediction, and ordinary robustness scores are not novel by themselves. The intervention-recommendation fidelity question remains a *candidate only*; no priority, novelty or patentability claim is established.

## Search scope

Targeted searches run on 27 October 2026 included:
- spatial proteomics marker imputation + counterfactual target discovery;
- whole-channel masking / virtual staining + intervention-set fidelity;
- imputation-aware counterfactual modeling / recommendation fidelity;
- spatial-proteomics foundation models + downstream evaluation;
- spatial tissue counterfactual perturbation / immune response prediction;
- uncertainty-calibrated spatial imputation + downstream analysis.

This search was designed to identify close methods, not to estimate a complete publication count. It did not exhaust all indexes, citation networks, supplements, patents or unpublished work. A direct non-hit for the exact phrase “intervention-set fidelity” would not prove that the underlying idea is new.

## Closest existing work and implication

### Morpheus — direct spatial-proteomics counterfactual baseline

Wang et al., *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles*, Nature Biomedical Engineering (2025), DOI 10.1038/s41551-025-01357-0. The method trains a classifier to predict CD8+ T-cell presence from multiplex tissue images and optimizes counterfactual input changes intended to increase the classifier's predicted probability of CD8+ T-cell presence. The paper includes held-out-patient evaluation and selected experimental validation.

**Implication:** “AI discovers tumour protein perturbations to increase predicted CD8 infiltration” is not our novelty. The Morpheus code/supplement and permission constraints still need to be inspected/reproduced before claiming a fair baseline.

Source: https://www.nature.com/articles/s41551-025-01357-0

### VirTues — direct marker reconstruction and downstream evaluation

Wenckstern et al., *The Virtual Tissues foundation model resolves spatial proteomics across scales*, Nature (published 5 August 2026), DOI 10.1038/s41586-026-10884-y. The paper reports whole-channel marker masking and niche masking; evaluates reconstruction on hidden pixels/markers with Pearson correlation and MSE; compares to mean-intensity and most-correlated-marker baselines; and demonstrates further downstream cell phenotyping and biomarker tasks. The released pipeline includes dataset-specific clipping, shifted log transformation, tissue-aware statistics and Gaussian smoothing.

**Implication:** neither virtual staining, foundation-model reconstruction, downstream evaluation nor a better reconstruction score is novel alone. The candidate must ask about a more specific output decision: whether the signed intervention set chosen by a separate counterfactual optimizer changes under whole-channel reconstruction.

Source: https://www.nature.com/articles/s41586-026-10884-y

### Spatium — missing protein measurement reconstruction

*Spatium: A Protein Language Foundation Model for Spatial Proteomics* (preprint version published 26 July 2026), DOI 10.64898/2026.07.23.740264, describes pretraining on over 51 million cells across 70 spatial-proteomics studies and includes reconstruction of missing protein measurements.

**Implication:** broad missing-protein reconstruction and cross-panel representation learning are active and crowded. Spatium is an optional comparator only if code, data terms, marker panel and computational feasibility justify inclusion; it is not required for the first pilot.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC13419744/

### SPAD-CFR — spatial generative counterfactuals

Ding, Luo and Xiong, *Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments*, Biology (2026), DOI 10.3390/biology15141097. The method represents tissue as spatial point clouds and generates counterfactual tissue states where molecular profiles and spatial coordinates can change together, including immune-focused examples.

**Implication:** broad spatial counterfactual tissue reprogramming for cancer immunotherapy is not a new framing. The proposed question must be explicitly about fidelity of a recommendation made downstream of reconstructed missing protein channels, not about generating spatial counterfactuals generally.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC13406000/

### Celcomen — spatial causal perturbation modeling

The 2026 Celcomen article describes a generative graph neural network using a mathematical causality framework to model intra- and inter-cellular gene regulation and generate spatial counterfactual transcriptomic states.

**Implication:** “spatial causal AI for tissue perturbations” is not novel. The modality and recommendation endpoint differ, but the paper is a conceptual neighbor that should stay in the methods matrix.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC13149852/

### TISSUE — uncertainty-aware downstream analysis

Sun et al., *TISSUE: uncertainty-calibrated prediction of single-cell spatial transcriptomics improves downstream analyses*, Nature Methods (2024), DOI 10.1038/s41592-024-02184-y. It uses conformal inference to calibrate spatial expression predictions and evaluate effects on hypothesis testing, clustering and supervised learning.

**Implication:** adding uncertainty estimates or an abstention rule is not novelty alone. It could only support a contribution if a prespecified recommendation-reliability rule improves signed-target fidelity or model-reference regret at a reported coverage cost, over simple baselines and on untouched patients.

Source: https://www.nature.com/articles/s41592-024-02184-y

## Revised candidate and falsifiable contribution

Keep only this candidate for a small feasibility test:

> Under patient-held-out evaluation, does whole-channel reconstruction change the signed marker-intervention set chosen by the same counterfactual discovery pipeline, and can a prespecified reliability/abstention rule predict when that decision diverges from the fully measured model reference?

The comparison must:
1. use the same held-out patients and a fixed target budget in both conditions;
2. hide whole marker channels, not only random cells/pixels;
3. compare a measured-channel model reference, a masked-panel condition, at least one simple imputation baseline, and foundation-model reconstruction;
4. report reconstruction error separately from signed target-set fidelity, direction flips, patient-level model-predicted uplift agreement, and model-reference regret;
5. choose every threshold on training/validation patients, then evaluate only on untouched patients;
6. describe all uplift as *model-predicted*, not causal treatment effect or biological ground truth.

The reference condition is a model output, not a biological oracle. A difference from that reference demonstrates decision instability, not that the reconstructed strategy is clinically wrong. A causal or therapeutic claim needs independent biological/experimental evidence.

## Go/no-go

**Current status: conditional feasibility candidate; not a confirmed gap.**

Proceed only if:
- permitted input data, correct marker-plane mapping and patient/ROI metadata are available;
- the exact pretrained checkpoint exposure is verified;
- the preprocessing path is valid;
- a simple pilot exhibits measurable differences between the full-channel and reconstructed-channel recommendation conditions; and
- a more complete review of the closest methods/supplements finds no equivalent evaluation.

Stop or pivot if the whole-channel comparison adds no interpretable value beyond existing baselines, if no valid outcome/marker set exists, or if the exact decision-fidelity analysis is already covered in prior work.

## Sources reviewed

- Morpheus (Nature Biomedical Engineering, 2025): https://doi.org/10.1038/s41551-025-01357-0
- VirTues (Nature, 2026): https://doi.org/10.1038/s41586-026-10884-y
- Spatium (2026 preprint): https://doi.org/10.64898/2026.07.23.740264
- SPAD-CFR (Biology, 2026): https://doi.org/10.3390/biology15141097
- Celcomen (2026): https://pmc.ncbi.nlm.nih.gov/articles/PMC13149852/
- TISSUE (Nature Methods, 2024): https://doi.org/10.1038/s41592-024-02184-y
