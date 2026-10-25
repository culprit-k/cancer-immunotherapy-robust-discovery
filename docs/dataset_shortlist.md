# Dataset shortlist for the virtual-marker / counterfactual fidelity pilot

**Last checked:** 25 October 2026  
**Status:** paper and catalogue metadata review only. No dataset has been downloaded, checksummed, inspected locally or permission-cleared for this project.

## Decision summary

**Best biological-development candidate:** hoch2022multiplexed (melanoma, imaging mass cytometry, 35 patients / 50 images, chemokine and immune landscape, immunotherapy context). It is highly relevant to an immune-infiltration counterfactual baseline, but VirTues uses this cohort for a cell-type evaluation and its Methods indicates that for some phenotype tasks the train/test split aligns with pretraining. It must therefore be treated as a development cohort unless a checkpoint trained without this cohort is used.

**Best convenient pipeline smoke-test candidate:** allam2022spatially (lung cancer IMC, 26 patients / 26 images, approximately 500 MB according to the spora project landing page). It is a useful data-load/marker-mask debugging route, but its marker panel and endpoint must be checked before treating it as the main target-discovery dataset.

**Best candidates to audit for independent evaluation:** moldoveanu2022spatially (melanoma, 90 patients / 90 images) and xiao2022multiplexed (melanoma, 26 patients / 158 images). Their exact panel overlap, patient response labels, data-use terms, and overlap with VirTues/other foundation-model training cohorts remain unverified here. Do not label either one independent before confirming that.

## Candidate details

| Priority | spora cohort ID | Public catalogue information | Strength for this question | Critical unresolved checks |
|---|---|---|---|---|
| 1 — development | hoch2022multiplexed | 35 patients, 50 images, melanoma, IMC; published chemokine-milieu study of immunotherapy response. Original raw-data record: https://zenodo.org/records/6004986 | Most direct link between measured chemokines and immune infiltration; candidate interventions have biological interpretability. | Panel names/units, exact outcome labels, license, availability of patient-level IDs, VirTues pretraining exposure, and the exact mapping between raw and harmonized spora versions. |
| 2 — smoke test | allam2022spatially | 26 patients, 26 images, lung cancer, IMC; spora describes a downloadable cohort around 500 MB. | Smaller first dataset to validate spora-io, channel masking, metadata parsing and patient splits before a large run. | Does its measured panel contain enough candidate target markers? Is CD8/T-cell labeling included in the standardized annotations? Exact rights and checkpoint exposure. |
| 3 — potential external test | moldoveanu2022spatially | 90 patients, 90 images, melanoma, IMC; Spatially mapping the immune landscape of melanoma using imaging mass cytometry. | Larger melanoma cohort; potentially useful to test marker-mask fidelity on independent tissue. | Need full panel and label mapping; check whether it is in the VirTues and any baseline model's training data; response/outcome fields and permissions. |
| 4 — potential external test | xiao2022multiplexed | 26 patients, 158 images, melanoma, IMC; Multiplexed imaging mass cytometry reveals distinct tumor-immune microenvironments linked to immunotherapy responses in melanoma. | Direct anti-PD-1 response context and cell-level immune annotations. | Marker/channel overlap, patient IDs, whether response labels are included in spora download, model pretraining overlap, and data-use terms. |
| 5 — secondary/alternative | schurch2020coordinated | 35 patients, 251 images, colorectal cancer, CODEX/H&E. | Useful alternative tissue architecture and immune-neighbourhood context. | Not the same marker panel/technology as IMC; target identities and endpoint must be mapped before comparison. |

Catalogue source: https://spora.bioimagearchive.org/projects/spora/dataset. The catalog currently lists 35 cohorts, 5,477 patients and five spatial imaging technologies. It says the standardized collection includes multiplex images and, where available, H&E, cell/tissue masks, cell types, patient metadata and other metadata. Dataset terms vary by cohort; the spora software license is not the same as the dataset license.

## Specific VirTues exposure warning

The VirTues paper explicitly uses Hoch et al. for cell typing and describes a marker-reconstruction stability experiment for other cohorts (Danenberg B-cell markers and Cords T-cell markers). It also describes zero-shot evaluation using models trained with an evaluation dataset withheld from pretraining. This is direct evidence that the candidate question must be more specific than generic cell phenotyping under marker masking. For a valid held-out cohort claim, use the official leave-one-dataset-out procedure or a model checkpoint whose training cohort list demonstrates that the selected evaluation cohort was excluded.

Sources:
- VirTues paper: https://www.nature.com/articles/s41586-026-10884-y
- VirTues code/weights: https://github.com/bunnelab/virtues
- spora dataset collection: https://spora.bioimagearchive.org/
- Hoch et al. raw data: https://zenodo.org/records/6004986
- Moldoveanu et al.: https://doi.org/10.1126/sciimmunol.eabi5072
- Xiao et al.: https://pmc.ncbi.nlm.nih.gov/articles/PMC9587266/

## Metadata checklist before committing to one dataset

- Dataset ID/version and per-dataset license in the BioImage Archive/spora interface.
- Source paper and original-data license.
- Number of independent patients, image cores, tiles, and cells after QC.
- Exact channel/marker names, UniProt IDs, transformations, and available target directions.
- Patient IDs and all aliases linking cores/tiles to a patient.
- Definition and completeness of CD8/T-cell phenotype labels.
- Availability and reliability of immunotherapy response/outcome labels.
- Whether the foundation-model checkpoint saw any cells/images/patients from that cohort during pretraining or fine-tuning.
- Whether the counterfactual model's output can be evaluated on fully measured, untouched patients.
- Storage, compute, and per-run inference/training time.

## Immediate gate

Start by downloading only allam2022spatially or an equally small permitted cohort to validate data loading, while separately auditing Hoch's channels and rights for the biological study. Do not use a smoke-test cohort as the primary endpoint unless it passes the biological and marker criteria. Do not commit raw data to GitHub.
