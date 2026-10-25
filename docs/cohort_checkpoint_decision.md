# Cohort and checkpoint decision record — 25 October 2026

## Decision

**Selected study system:** Salié et al. hepatocellular carcinoma (HCC) imaging-mass-cytometry (IMC) dataset pair. The 54-patient discovery cohort is the rights-cleared development candidate; the 42-patient ICI cohort is a conditional external test because the direct Zenodo licence field is blank.

- **Development cohort:** 54-patient HCC discovery cohort, Zenodo record [10793609](https://zenodo.org/records/10793609). The NLM Dataset Catalog reports CC BY 4.0 for this record. It includes preprocessed multichannel images and cell/stroma masks; channel annotations are in `DCCohort_panel.csv`.
- **Independent clinical-context test cohort:** 42-patient HCC ICI-treatment cohort, Zenodo record [10794904](https://zenodo.org/records/10794904), DOI 10.5281/zenodo.10794904. The Zenodo landing page describes normalized channel-wise multi-stack TIFF images, cell masks, stromal masks and `ICICohort_panel.csv`; patient metadata are in Supplementary Table 3 of the associated paper. OpenAIRE/Datacite-linked metadata for this exact record reports **CC BY**, although the direct Zenodo “Rights / License” field is visually blank. This is a license-metadata discrepancy, so retain the OpenAIRE evidence and request clarification from the dataset contact before any redistribution or if institutional policy requires source-record confirmation.
- **Published cohort paper:** Salié et al., *Gut* (2024/2025 issue), DOI [10.1136/gutjnl-2024-332837](https://doi.org/10.1136/gutjnl-2024-332837). It describes a 41-plex IMC panel and 54-person discovery plus 42-person ICI validation cohort; key immune phenotypes include CD8 T cells, PD-1-positive/exhausted CD8 T cells, TIM-3/LAG-3, PD-L1-positive myeloid/APC states, CD204 macrophages and HLA-DR-positive cells.

**Selected foundation-model variant (to be frozen by immutable revision at download):** `bunnelab/virtues` — **`virtues-imc14/model.safetensors`** from the official [VirTues Hugging Face repository](https://huggingface.co/bunnelab/virtues), using the matching official code at [bunnelab/virtues](https://github.com/bunnelab/virtues).

Why this variant:
- The official model table identifies `virtues-imc14` as pretrained on 14 IMC datasets and assigns the **CC BY-NC 4.0 model-weight licence**.
- The VirTues paper distinguishes this core 14-IMC model from the extended 32-cohort corpus, which adds seven extra IMC cohorts (refs. 90–96) alongside non-IMC cohorts.
- The Salié HCC study is cited as ref. 95 in the VirTues paper, within the extended-corpus additions. Therefore the IMC-only 14-cohort checkpoint is the appropriate published variant to investigate for HCC evaluation; `virtues-sp32` and `virtues-sp31` are **not** acceptable independent checkpoints for this cohort because they use the extended multi-technology corpus that includes the Salié study.
- This conclusion is based on the published cohort grouping, not yet on a checksum or direct confirmation from the model authors that both Zenodo accessions (54-patient discovery and 42-patient ICI validation) were excluded from the precise `virtues-imc14` weights. Treat cohort exposure as **likely excluded but not finally verified** until the downloaded artifact revision and model-training manifest are recorded.

## Compatibility rationale

| Requirement | Evidence / status | Decision |
|---|---|---|
| Cancer and immune-oncology relevance | HCC, spatial immune architecture and ICI-treatment outcomes in the linked 42-patient cohort. | Strong fit. |
| Spatial protein channels | IMC, 41-plex panel; channel-wise normalized TIFF stacks. | Compatible modality for VirTues IMC reconstruction. |
| Cell/tissue geometry | Cell masks and stroma masks included in the 42-patient upload; analogous masks in the 54-patient cohort. | Suitable starting inputs; inspect actual file structure and quality after download. |
| CD8 objective | The article analyzes CD8 T-cell infiltration and CD8/checkpoint-positive immune states. | Potential endpoint. Need a reproducible cell-label / threshold definition before analysis. |
| Candidate intervention targets | Article reports PD-1, TIM-3/LAG-3, PD-L1-positive APC/myeloid states, CD204 macrophages and other immune markers. | Provisional biological shortlist only; final allowed target markers must be read from the actual panel CSV and fixed before test evaluation. Never manipulate the CD8 endpoint marker to predict CD8 density. |
| Dataset rights | 54-cohort: NLM catalogue reports CC BY 4.0. 42-cohort: OpenAIRE/Datacite metadata reports CC BY; direct Zenodo rights field appears blank. | 54-cohort provisionally cleared for attribution-based reuse; retain evidence. 42-cohort provisionally CC BY but resolve discrepancy with data contact/institutional policy before redistribution. |
| Foundation-model weights | `virtues-imc14` CC BY-NC 4.0. | Suitable for non-commercial academic research with attribution and compliance; **not suitable for commercial use without separate permission/licensing**. Do not assume the MIT code licence applies to the weights. |
| Exact model exposure | Published pretraining inventory suggests the Salié dataset is in the seven extra IMC additions to the extended corpus, not the core 14-IMC model. | Strongest available checkpoint candidate; still require immutable model revision/hash and exposure confirmation before calling it rigorously held out. |
| Exact counterfactual baseline compatibility | Morpheus was developed for other tumour cohorts and its original target-prediction pipeline has not been reproduced on HCC. | Not yet established. Validate panel and endpoint first; reproduce/adapt with pre-specified rules, and label any adapted method as an adaptation rather than a direct reproduction. |

## Locked analysis roles

1. **Development / method calibration:** 54-patient discovery cohort (Zenodo 10793609), patient-level splits only. Use this cohort to settle image preprocessing, panel-to-marker mapping, endpoint definition, masking cases and validation-calibrated thresholds.
2. **External evaluation:** 42-patient ICI cohort (Zenodo 10794904), untouched until the pipeline, target budget, marker shortlist, threshold and reliability/abstention rule are frozen. Do not tune on this test cohort.
3. **Reconstruction checkpoint:** freeze `virtues-imc14`, pin the downloaded snapshot to an immutable Hugging Face commit and store SHA-256, file size, download date and model licence text in the run log. If the exact model-training exclusion cannot be confirmed, report it as a *candidate external checkpoint with uncertain exposure*, not as strictly independent.
4. **Evaluation unit:** patient. All ROIs/images from a patient must remain in one split. Never treat cells, tiles or ROIs as independent patients.
5. **Primary output:** signed intervention recommendation fidelity (marker identity plus increase/decrease direction) and patient-level change in the model-predicted CD8 objective between full-panel and reconstructed-panel runs. Full-panel output is a model reference, not biological ground truth. Predicted change is not a demonstrated treatment effect.

## Go/no-go checklist before actual inference

- [ ] Download the 54-patient and 42-patient archives from their official records; store outside the public GitHub repository.
- [ ] Verify archive integrity against source checksums and record new SHA-256 values locally.
- [ ] Inspect `DCCohort_panel.csv` and `ICICohort_panel.csv`; compare marker names, metal channels, image dimensions, masks and patient metadata.
- [ ] Save an evidence copy of the CC BY metadata for the 54-patient cohort; resolve the 42-patient cohort's blank Zenodo license field with the data contact or institutional research office.
- [ ] Download only the official `virtues-imc14` weight artefact, read its licence, pin the exact immutable revision and record SHA-256. Do not use `virtues-sp32` or `virtues-sp31` for the primary held-out claim.
- [ ] Confirm model-training cohort inclusion/exclusion against the exact checkpoint version. Ask the authors if the public supplement/model card does not resolve accession-level exposure.
- [ ] Define an endpoint from cell labels/marker thresholds without using the withheld test data; pre-register eligible intervention markers from the panel CSV.
- [ ] Reproduce or justify the counterfactual baseline before interpreting output as target discovery.

## Scope and honest status

This establishes a **specific, scientifically compatible cohort pair and the most appropriate public checkpoint variant** based on available paper, repository and catalogue evidence. It does not mean data or weights have been downloaded, checksummed, model outputs generated, legal clearance formally issued, or zero exposure proven. No biological result exists yet. The first true-data milestone is a panel/metadata audit and one-channel reconstruction smoke test.
