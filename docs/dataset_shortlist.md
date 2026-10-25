# Dataset shortlist for the virtual-marker / counterfactual fidelity pilot

**Last checked:** 25 October 2026  
**Status:** paper and catalogue metadata review only. No dataset has been downloaded, checksummed, inspected locally or permission-cleared for this project.

## Decision summary

**Important correction:** rigamonti2024integrating is useful for a reconstruction/cell-annotation pipeline smoke test, but its published 24-marker panel does not appear to include the chemokine/target channels needed for a Morpheus-style signed intervention-set test. It should not be the primary target-discovery cohort unless the target set is narrowed and justified in advance. The original study reports CD8+ T-cell labels and prognostic spatial analysis, not a Morpheus-compatible intervention endpoint.

**Best biological-development candidate:** hoch2022multiplexed (melanoma, IMC, 35 patients / 50 images, chemokine and immune landscape, immunotherapy context). It has the clearest biological link to chemokines and immune infiltration, but VirTues directly evaluates cell typing on this cohort and some relevant tasks align their patient split with pretraining. Use for development only unless the reconstruction model is trained without this cohort.

**Best convenient pipeline smoke-test candidate:** allam2022spatially (lung cancer IMC, 26 patients / 26 images, approximately 500 MB according to the spora project landing page). Use only to check data-loading and masking code; panel suitability must still be verified.

**Other potential cohorts:** moldoveanu2022spatially (melanoma, 90 patients / 90 images) and xiao2022multiplexed (melanoma, 26 patients / 158 images). The VirTues paper's extended 32-cohort corpus includes Xiao et al. (2022), so the standard `virtues-sp32` checkpoint must not be treated as an independent imputer for Xiao. The Xiao panel includes CD8a, PD-1 and PD-L1 but not all Morpheus melanoma targets. Moldoveanu is also listed in the VirTues corpus. Both require an alternative independent imputer or leave-one-cohort-out retraining.

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


## Updated checkpoint and rights gate (25 October 2026)

The official VirTues repository lists `virtues-sp32` trained on 32 datasets with CC BY-NC 4.0 model weights, `virtues-sp31` trained on 31 datasets with MIT-licensed weights, and `virtues-imc14` trained on 14 IMC datasets with CC BY-NC 4.0 weights. These weight licences are distinct from both the code licence and the underlying cohort's terms. Before describing any cohort as held out, record the exact checkpoint name/version and its full training cohort list. The default `virtues-sp32` model cannot be treated as independent on any cohort included in its 32-dataset training mixture.

For `rigamonti2024integrating`, the published leave-one-dataset-out result is a reason to investigate—not evidence that the specific public checkpoint currently available to us excludes Rigamonti. Confirm the exact model artifact and training composition, candidate channel overlap, patient split, and dataset reuse terms before approval. Do not download or redistribute restricted artifacts, and do not commit raw patient-level data to GitHub.

See [targeted prior-art and feasibility audit](targeted_prior_art_and_feasibility_audit_2026-10-25.md) for the complete gate checklist.


## New post-VirTues-release exploratory cohort candidate

**Godbole et al. 2026 melanoma IMC cohort** — Zenodo record 15124735, posted 17 September 2026; six patients with multiple regions of interest. The downloadable panel table lists CD8a, PD-1, PD-L1, CTLA-4, TIM-3, LAG-3, TIGIT, CCL2, CCL4, VEGF and macrophage markers. The panel is biologically relevant to immunotherapy resistance and has a CD8 endpoint. Because the record postdates the VirTues article/model release, it is a promising *candidate external exploratory test* for a frozen pre-existing checkpoint, but exact training exposure still needs documentation and the Zenodo page's licence field is blank. Contact the data custodian or verify applicable terms before use. Six patients are far too few to claim a definitive external validation; treat it as a feasibility/exploratory cohort only.

**Panel-level findings from source metadata:** the Rigamonti 2024 panel is a 24-marker NSCLC panel focused on tumour, tissue architecture and immune lineages; it supports CD8 annotation but not an obvious Morpheus-style chemokine target set. Xiao 2022's 41-channel melanoma panel includes CD8a, PD-1 and PD-L1, but the VirTues 32-cohort training corpus includes Xiao. The recent Godbole 2026 panel includes multiple checkpoint and chemokine markers but only six patients and no displayed dataset licence.

Source records: Godbole et al. dataset https://zenodo.org/records/15124735; Xiao panel https://zenodo.org/records/6836992; Rigamonti article DOI 10.1158/0008-5472.CAN-23-1698; VirTues article https://www.nature.com/articles/s41586-026-10884-y.
