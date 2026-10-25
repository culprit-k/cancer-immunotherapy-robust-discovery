# Data clarification request — Salié HCC IMC cohort

**Purpose:** Resolve whether the HCC discovery cohort can be processed reproducibly with a spatial-proteomics reconstruction model. This is a draft for the research team to send; it has not been sent.

## Questions to the corresponding author / dataset curator

1. Are the original spillover-compensated IMC acquisition files (for example, MCD or equivalent raw channel intensities) available for the 54-patient discovery cohort, under the same or an additional data-use agreement?
2. If only the normalized TIFFs are distributable, what exact operations generated `DC_img_normalized` (including any arcsinh/log transform, cofactor, clipping, normalization unit, background correction, scaling and handling of negative values)?
3. Are per-ROI/per-channel transformation parameters or the unnormalized image stacks available? If normalized values cannot be inverted, can the original-scale values be shared for non-commercial academic research?
4. Can you confirm the exact TIFF channel ordering and whether the published panel table is authoritative for every ROI? The ZIP currently contains `DiscoveryCohort_panel.csv`, while the Zenodo description mentions `DCCohort_panel.csv`.
5. Are cell-level phenotype labels, gates, cluster assignments or the original analysis objects available for the image ROIs? The public archive description identifies cell/stroma masks but does not explicitly promise cell-type labels.
6. Are patient identifiers and ROI metadata sufficient to reconstruct the patient-to-ROI mapping without exposing direct identifiers? Are the supplementary clinical tables permitted to be linked to image-derived summaries for this research question?
7. The paper's Methods describe PENGUIN channel normalization to 0–1, background removal and percentile denoising, with channel-specific thresholds selected by manual inspection and applied consistently to every ROI. Can you confirm whether this is the complete export recipe for `DC_img_normalized`, or whether any additional transformation or integer encoding is applied when writing the TIFF files?
8. Are the PENGUIN thresholds / background settings retained anywhere for the discovery cohort? If the normalization is not invertible, is the original compensated intensity data available under suitable academic terms?
9. Is the proposed use—benchmarking missing-marker reconstruction and evaluating stability of *model-predicted* immune-target recommendations—covered by the current CC BY 4.0 dataset terms and article citation requirements? We will not redistribute raw images or make clinical treatment claims.

## Draft email

Subject: Clarification request on raw/normalized IMC data and cell annotations for the Salié HCC cohort

Dear Professor Salié / dataset team,

I am an MBBS student developing a reproducible academic study on how missing-marker reconstruction affects downstream computational analyses of spatial immuno-oncology data. I have verified the checksum and marker-panel metadata of the public 54-patient HCC discovery archive and am checking data compatibility before running any model.

The public archive appears to contain PENGUIN-normalized TIFF stacks and cell/stroma masks, but not the original MCD acquisitions or the quantile/mean/standard-deviation metadata expected by the VirTues input pipeline. I do not want to treat a conversion of normalized TIFFs as though it recreated original intensities, nor infer cell phenotypes from masks alone.

Could you please confirm the exact TIFF storage encoding and complete PENGUIN normalization recipe, and whether original-scale/spillover-compensated images plus channel/ROI metadata can be made available for academic research? I would also appreciate cell-type labels or the analysis objects used for the published immune-phenotyping results, the authoritative panel filename/channel order, and any terms relevant to this proposed use.

I will cite the dataset and paper, respect the applicable license and any additional conditions, and will not redistribute raw data. No model inference or biological conclusions have been produced yet; I am trying to establish a valid and reproducible input contract first.

Thank you for your time and for making the dataset available.

Kind regards,  
[Your name]  
[Institution / research supervisor, if applicable]

## Decision rule

- If original-scale inputs and metadata are provided under suitable terms, build and validate a VirTues-compatible conversion and compare it with the published example pipeline before evaluating the HCC cohort.
- If not, do not attempt to reverse normalized TIFFs into raw values. Use a model explicitly validated for the released representation or switch to a compatible independent cohort.
- If cell labels are unavailable, define a prespecified marker-based endpoint only if it can be justified from the paper and validated without using the held-out patients to tune thresholds. Otherwise change the endpoint.
