# Immediate next step: data request and compatible-cohort screen (2026-10-25)

## Decision
Do not run pretrained VirTues on the current normalized HCC discovery TIFFs. The public discovery cohort is already preprocessed, and the required VirTues-compatible intensity representation/statistics are not available in the downloaded archive. Keep inference blocked until the input representation is validated.

## Route A — request data/preprocessing clarification from the HCC study team

Publicly listed contact: Prof. Bertram Bengsch, University Medical Center Freiburg, bertram.bengsch@uniklinik-freiburg.de (institutional contact page: https://www.bioss.uni-freiburg.de/person/prof-dr-dr-bertram-bengsch/).

### Email status — sent by the researcher on 2026-10-25
The email draft below was sent by the researcher, who confirmed sending it in chat. Awaiting a response; no response has been received or verified here.
**Subject:** Request for original-scale IMC data and preprocessing details for HCC cohort (Zenodo 10793609 / 10794904)

Dear Professor Bengsch and colleagues,

I am an MBBS student developing a reproducible research project on how missing-marker reconstruction in spatial proteomics can affect downstream immune-target discovery.

I am reviewing the HCC discovery cohort (Zenodo 10793609) and, subject to suitability, the ICI-treated cohort (Zenodo 10794904). The public discovery archive provides normalized multichannel TIFF images, masks and a marker panel. Before choosing a reconstruction model, I want to ensure that the input representation is scientifically compatible with the method.

Would it be possible to clarify or share, if available and permissible:
1. Original-scale IMC/MCD data or an export before the current image normalization;
2. The exact preprocessing steps and parameters used to create the public normalized TIFFs, including clipping/thresholding, noise removal, transformations, and per-channel/per-tissue normalization;
3. Any channel-wise statistics or reference values required to reproduce the published image representation;
4. Whether the discovery and ICI cohorts share the same preprocessing pipeline and whether there are known restrictions on derived-data redistribution or reuse;
5. The recommended citation and any additional conditions for reuse.

I do not need identifiable patient information. I would only use data under the applicable access terms and would document the preprocessing provenance. If the original-scale data cannot be shared, a methods note or parameter file would still be very helpful.

Thank you for your time and for making the cohort available.

Kind regards,  
[Your full name]  
MBBS student  
[Institution, optional]  
[Project repository, optional]

## Route B — alternatives to screen in parallel

| Candidate | What is available | Potential role | Main caveat / next check | Initial status |
|---|---|---|---|---|
| HCC discovery cohort, Zenodo 10793609 | 54-patient IMC cohort; normalized TIFF stacks, masks, panel | Primary biological cohort if compatible input can be obtained or a validated model is selected | Public TIFFs are not known to be compatible with VirTues preprocessing; do not invert normalization | **Hold for direct VirTues inference** |
| HCC ICI cohort, Zenodo 10794904 | Public HCC cohort related to immune-checkpoint inhibitor therapy; normalized TIFF stacks, masks, panel | Potential clinical/biological validation cohort after full audit | Images and panel have not yet been structurally audited in this project; check preprocessing and whether cohort was used in any selected model's training | **Audit next; not yet approved** |
| HCC spatial multi-omics study, latest Zenodo record 19123188 (v2; earlier record 15392699) | Processed CODEX MIF cell-level normalized protein expression and cell-type annotations across 48 fields of view; Visium data across 22 samples; metadata includes patient ID, pre/post-treatment, immunotherapy response and treatment type | Promising alternative for a cell-level marker-masking benchmark and downstream response-association analysis | Different assay and data representation; not a drop-in VirTues input. Zenodo page lists the record as open but does not visibly specify a license. Confirm license/reuse terms, marker panel, patient-level split, and model-training independence before selection | **Best alternative to investigate first; not yet approved** |
| VirTues harmonized training corpus | Harmonized spatial proteomics corpus and model-specific preprocessing pipeline documented by authors | Reference for implementing the model's own pipeline and for checking training exposure | A cohort used in pretraining cannot serve as clean held-out external validation for that checkpoint | **Use for compatibility/provenance research only** |

Sources:
- HCC discovery: https://zenodo.org/records/10793609
- HCC ICI: https://zenodo.org/records/10794904
- HCC multi-omics latest version: https://zenodo.org/records/19123188 (previous record/version: https://zenodo.org/records/15392699)
- HCC multi-omics paper/preprint DOI: 10.1101/2025.06.11.656869
- VirTues paper/repository: https://www.nature.com/articles/s41586-026-10884-y and https://github.com/bunnelab/virtues

## Preliminary alternative-cohort assessment
The CODEX/Visium HCC dataset is attractive because it provides normalized per-cell protein features, cell labels, spatial coordinates and treatment-response metadata. This permits a controlled **cell-level** missing-marker benchmark without pretending the data are compatible with VirTues image preprocessing. The benchmark would need a separate, appropriately validated tabular/cell-graph model and must account for patient-level grouping to prevent leakage across regions from the same patient. It is not yet selected: license/reuse terms and the actual metadata/panel contents still need checking.

The newer Zenodo record (19123188) is listed as open and includes CODEX-MIF, metadata, Visium data and co-registered H&E images. Its landing page does not visibly identify a license; do not assume that “Open” alone resolves reuse rights. Confirm the file-level license and permitted research use with the authors/Zenodo metadata before substantive analysis or redistribution.

### Public metadata audit completed 2026-10-25
- **CODEX/Visium HCC alternative (Zenodo 19123188):** downloaded/read the small public `metadata.csv` preview only; no large archives were downloaded. It has 48 region rows and 7 columns: `region_id`, `region_label`, `patient_id`, `state`, `response`, `species`, `treatment`. The rows identify 13 distinct patient IDs, with both pre- and post-treatment regions and responder/non-responder labels. This is repeated-region metadata, not 48 independent patients. A patient-level split is mandatory to prevent leakage. The records are split across treatment labels “List A” and “List B”; the exact clinical meaning of those labels must be checked against the paper/supplement before analysis.
- **CODEX feature format:** the archive preview lists per-region cell-data, cell-type, cell-feature and expression CSV files. The expression tables are documented as normalized protein biomarker levels, so the dataset is suitable in principle for a cell-level masking benchmark if marker columns and preprocessing are verified. It is not a VirTues image input.
- **Scientific-overlap caution:** the accompanying HCC study already analyzes spatial multi-omics and deep-learning fingerprints of immunotherapy response/resistance. Our contribution must therefore be tightly framed around marker-missingness, reconstruction error, and the effect on downstream marker/target ranking; generic prediction of immunotherapy response is not a novel claim.
- **HCC ICI cohort (Zenodo 10794904):** the public record describes 42 ICI-treated HCC patients and an 882 MB archive containing normalized multichannel TIFFs, cell masks, stromal/parenchymal masks and `ICICohort_panel.csv`. Its image representation is likewise preprocessed/normalized, so it is not automatically compatible with VirTues. The archive itself is too large for the web preview, and the full archive/panel have **not** been downloaded or structurally audited here. The landing page's license field is not visibly populated; confirm rights and cite the source study before reuse.
- **License status:** the Zenodo record pages show an empty visible “License” field for both the CODEX/Visium HCC alternative and the HCC ICI record. The discovery cohort has a separate CC BY 4.0 catalog listing, but do not transfer that license assumption to another record. Treat reuse as **pending clarification** until authoritative metadata or the depositor confirms terms.

## Selection rule
Do not choose a dataset solely because it is available. It must have:
- a documented and reproducible input representation;
- a marker panel that supports the planned masked-marker experiment;
- appropriate spatial or cell-level structure;
- a defensible patient-level independent evaluation split;
- a relevant downstream endpoint or a clearly stated, non-clinical surrogate endpoint;
- reuse terms that permit the intended analysis.

## Next go/no-go gate
1. Await the author response to the email sent by the researcher on 2026-10-25; follow up if appropriate.
2. Download and structurally audit the HCC ICI archive/panel only after verifying reuse terms; keep raw images out of GitHub.
3. Obtain authoritative reuse terms for the CODEX/Visium record; then audit the expression-table marker columns and missingness.
4. Inspect the VirTues cohort inventory to rule out training overlap for any candidate validation cohort.
5. Select one route and document the rationale before inference.

## Scientific guardrail
The first experiment should test reconstruction fidelity and downstream ranking stability under controlled marker masking. Do not call model-generated rankings validated immunotherapy targets, clinical recommendations, or novel discoveries without independent biological evidence.
