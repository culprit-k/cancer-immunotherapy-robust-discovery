# Dataset shortlist for the virtual-marker / counterfactual fidelity pilot

**Last checked:** 25 October 2026  
**Status:** paper and catalogue metadata review only. No dataset has been downloaded, checksummed, inspected locally or permission-cleared for this project.

## Decision summary

**Best first candidate for a held-out recommendation-fidelity pilot:** rigamonti2024integrating (lung cancer, IMC + H&E, 108 patients / 158 images). The spora benchmark metadata includes CD4 T-cell and CD8 T-cell labels, and VirTues reports a leave-one-dataset-out zero-shot marker-reconstruction evaluation on Rigamonti et al. This makes it a promising test setting, provided we verify the exact checkpoint training composition, candidate marker panel, data-use terms and whether the released model is the leave-one-out checkpoint rather than a model that included this cohort.

**Best biological-development candidate:** hoch2022multiplexed (melanoma, IMC, 35 patients / 50 images, chemokine and immune landscape, immunotherapy context). It has the clearest biological link to chemokines and immune infiltration, but VirTues directly evaluates cell typing on this cohort and some relevant tasks align their patient split with pretraining. Use for development only unless the reconstruction model is trained without this cohort.

**Best convenient pipeline smoke-test candidate:** allam2022spatially (lung cancer IMC, 26 patients / 26 images, approximately 500 MB according to the spora project landing page). Use only to check data-loading and masking code; panel suitability must still be verified.

**Other potential cohorts:** moldoveanu2022spatially (melanoma, 90 patients / 90 images) and xiao2022multiplexed (melanoma, 26 patients / 158 images). Their exact panel overlap, patient outcome labels, data-use terms, and overlap with VirTues/other foundation-model training cohorts remain unverified; do not call either independent before the audit.

## Candidate details

| Priority | spora cohort ID | Public catalogue information | Strength for this question | Critical unresolved checks |
|---|---|---|---|---|
| 1 — potential held-out fidelity test | rigamonti2024integrating | 108 patients, 158 images, lung cancer, IMC + H&E. The spora benchmark has cell annotation classes including CD4 T cell and CD8 T cell. | VirTues reports a leave-one-dataset-out zero-shot reconstruction test on this cohort; useful for testing whether reconstruction affects counterfactual target recommendations in a cohort excluded from that specific model's pretraining. | Exact checkpoint/weight variant, marker panel, model training exposure, permissions, and whether the measured markers support a meaningful target set. |
| 2 — biological development | hoch2022multiplexed | 35 patients, 50 images, melanoma, IMC; published chemokine-milieu study of immunotherapy response. Original raw-data record: https://zenodo.org/records/6004986 | Most direct connection between chemokines and immune infiltration. | VirTues exposure and cell-typing use; panel names/units, outcome labels, rights and raw-to-spora mapping. |
| 3 — smoke test | allam2022spatially | 26 patients, 26 images, lung cancer, IMC; spora describes a downloadable cohort around 500 MB. | Smaller route to validate spora-io, channel masking, metadata parsing and patient splits. | Does its panel contain suitable perturbation markers? Are CD8/T-cell labels and terms available? |
| 4 — potential external test | moldoveanu2022spatially | 90 patients, 90 images, melanoma, IMC; Spatially mapping the immune landscape of melanoma using imaging mass cytometry. | Larger melanoma cohort; possible marker-mask fidelity test. | Panel, labels, access and model-training overlap must be verified. |
| 5 — potential external test | xiao2022multiplexed | 26 patients, 158 images, melanoma, IMC; anti-PD-1 response context. | Clinical response context with cell-level annotations. | Marker/channel overlap, patient IDs, response label availability, pretraining overlap and terms. |
| 6 — secondary/alternative | schurch2020coordinated | 35 patients, 251 images, colorectal cancer, CODEX/H&E. | Useful alternative tissue architecture and immune-neighbourhood context. | Not a direct substitute for an IMC panel without mapping and endpoint justification. |

Catalogue source: https://spora.bioimagearchive.org/projects/spora/dataset. The catalog currently lists 35 cohorts, 5,477 patients and five spatial imaging technologies. It says the standardized collection includes multiplex images and, where available, H&E, cell/tissue masks, cell types, patient metadata and other metadata. Dataset terms vary by cohort; the spora software license is not the same as the dataset license.

## Specific VirTues exposure warning

The VirTues paper explicitly uses Hoch et al. for cell typing and describes a marker-reconstruction stability experiment for other cohorts (Danenberg B-cell markers and Cords T-cell markers). It also describes zero-shot evaluation using models trained with an evaluation dataset withheld from pretraining. This is direct evidence that the candidate question must be more specific than generic cell phenotyping under marker masking. For a valid held-out cohort claim, use the official leave-one-dataset-out procedure or a model checkpoint whose training cohort list demonstrates that the selected evaluation cohort was excluded.

Sources:
- VirTues paper: https://www.nature.com/articles/s41586-026-10884-y
- VirTues/Spora benchmark configuration for Rigamonti cell annotation (includes CD8 T-cell labels): https://github.com/bunnelab/spora-bench/blob/master/configs/benchmarks/cell_annotation/rigamonti2024integrating.yaml
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
