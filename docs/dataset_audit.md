# Dataset feasibility audit

**Status (25 October 2026): likely research candidate identified; data/model feasibility and reuse permissions not fully verified. No data downloaded or locally validated.**

## Candidate starting point: Morpheus melanoma IMC

- Paper: https://doi.org/10.1038/s41551-025-01357-0
- Melanoma dataset cited by paper: https://doi.org/10.5281/zenodo.5994135
- Original melanoma IMC data-for-analysis record: https://doi.org/10.5281/zenodo.5994136
- Morpheus preprocessed data and model outputs: https://doi.org/10.22002/pr14s-wgk05
- Public code/tutorial: https://github.com/cellethology/morpheus-spatial
- CRC tutorial notebook downloads crc_tutorial.zip from Caltech Data Portal record pr14s-wgk05.

The Morpheus paper describes 159 tumour cores from 69 melanoma patients across 39 channels, including chemokines. This is the preferred candidate because it has relevant spatial molecular markers and multiple cores for some patients. The independent unit is the patient (69), not the core or image patch.

The paper describes a CRC liver-metastasis cohort with 209 sections from 30 patients and reports the source data are available from the authors on request. The public CRC tutorial bundle is a reproduction/example path and should not be confused with the full source dataset. The paper reports a breast cohort of 749 cores from 693 patients, but states its marker panel is not suitable for the same therapeutic-perturbation task.

## Public data archive and licensing caution

The original melanoma data-for-analysis Zenodo record lists:
- data_for_analysis.zip: approximately 7.1 GB; listed MD5 d59d8bda091da8bb053fa0df464595ee.
- MelanomaIMC-Zenodo.zip: approximately 41.1 MB; listed MD5 79c606231e3d93bec7bd05b7afb1dedb.

That record describes processed single-cell objects, clinical tables, labels, and code used for the original analysis. It is distinct from the Morpheus-preprocessed artifact/model outputs and the CRC tutorial bundle.

The Rights/License field on the original data-for-analysis record appears blank in the audit. The Morpheus paper is licensed CC BY-NC-ND 4.0, but the paper's license does not automatically license separate datasets or source code. Check the individual accession, files, repository and any applicable data-use terms before substantive reuse or redistribution. A missing license field is not evidence of unrestricted use.

## Required checks before analysis

- Exact data artifact/version, source, publication and retrieval date.
- Rights/license and whether academic reuse or derived-data publication has conditions.
- Patient identifiers and ability to group all cores, samples and patches from each patient.
- Channel list, marker semantics, units, normalization and intervention direction.
- Endpoint definition and availability of true labels for validation.
- Missingness, batch effects and clinical covariates.
- Predefined train/validation/test patient split and any data overlap.
- Reproduction of published outputs and checksums.
- RAM/disk, GPU/CPU feasibility, dependency versions and runtime.

## Access/reproduction observations

The public Morpheus tutorial uses a trained unet.ckpt, a saved patient_split.json, and an example CRC dataset. main.py starts from seed 42. Package documentation specifies Python >=3.9 and <3.12; the workflow uses PyTorch/Lightning, and counterfactual generation can be expensive. A CPU-only small smoke test may work, but it has not been tried here.

The execution environment for this project could not retrieve the public archives because direct network access failed with name-resolution errors. No file was downloaded, no checksum was verified, no model was loaded, and no smoke test was run. This is an execution-environment limitation, not evidence that the public data host is down.

## Leakage prevention and evaluation design

- Keep every core/patch from a patient in one partition.
- Fit normalization, imputation, feature selection and thresholds only within the training/inner-validation data.
- Do not use held-out patients to choose or rank target sets.
- Evaluate model-predicted counterfactual uplift by aggregating within patient, then weighting patients equally.
- Keep cached-output resampling distinct from retraining/full-pipeline robustness.
- Do not pool spatial protein measurements with bulk RNA-seq unless marker/outcome equivalence is justified.

## Initial recommendation

Use the tutorial/preprocessed artifacts first if their terms allow it. Test parsing, saved model loading and a published baseline on a small subset before downloading the 7.1 GB archive or retraining. If the license remains unclear, seek permission or select a dataset with explicit reuse terms. Do not commit raw or restricted data to GitHub.
