# Immediate next step: data request and compatible-cohort screen (2026-10-25)

## Decision
Do not run pretrained VirTues on the current normalized HCC discovery TIFFs. The published cohort is already preprocessed, and the required VirTues-compatible intensity representation/statistics are not available in the downloaded archive. Keep inference blocked until the input representation is validated.

## Route A — request data/preprocessing clarification from the HCC study team

Publicly listed contact: Prof. Bertram Bengsch, University Medical Center Freiburg, bertram.bengsch@uniklinik-freiburg.de (institutional contact page: https://www.bioss.uni-freiburg.de/person/prof-dr-dr-bertram-bengsch/).

### Draft email — not sent
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
| HCC spatial multi-omics study, Zenodo 15392699 | Processed CODEX multiplex immunofluorescence cell-level protein expression and annotations across 48 fields of view, plus Visium data across 22 samples, according to the paper | Potential alternative for a cell-level marker-masking benchmark and spatial/clinical association analyses | Different assay and data representation; not a drop-in VirTues input. Verify license, sample-level labels, marker panel, access files and independence from model training before use | **Promising alternative; verify before selection** |
| VirTues harmonized training corpus | Harmonized spatial proteomics corpus and model-specific preprocessing pipeline documented by authors | Reference for implementing the model's own pipeline and for checking training exposure | A cohort used in pretraining cannot serve as a clean held-out external validation cohort for that same checkpoint | **Use for compatibility/provenance research only** |

Sources:
- HCC discovery: https://zenodo.org/records/10793609
- HCC ICI: https://zenodo.org/records/10794904
- HCC multi-omics paper and dataset DOI 10.5281/zenodo.15392699: https://pmc.ncbi.nlm.nih.gov/articles/PMC12259099/
- VirTues paper/repository: https://www.nature.com/articles/s41586-026-10884-y and https://github.com/bunnelab/virtues

## Selection rule
Do not choose a dataset solely because it is available. It must have:
- a documented and reproducible input representation;
- a marker panel that supports the planned masked-marker experiment;
- appropriate spatial or cell-level structure;
- a defensible independent evaluation split;
- a relevant downstream endpoint or a clearly stated, non-clinical surrogate endpoint;
- reuse terms that permit the intended analysis.

## Next go/no-go gate
Within the next research iteration:
1. Send the email above (manual action; no email has been sent by this workflow).
2. Audit the ICI archive structure and panel, without committing raw images.
3. Inspect Zenodo 15392699 files, license and metadata; compare markers, sample labels and data format.
4. Inspect the VirTues cohort inventory to rule out training overlap for any candidate validation cohort.
5. Select one route and document the rationale before inference.

## Scientific guardrail
The immediate experiment should first test reconstruction fidelity and downstream ranking stability under controlled marker masking. Do not call model-generated rankings validated immunotherapy targets, clinical recommendations, or novel discoveries without independent biological evidence.
