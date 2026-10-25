# Dataset feasibility audit

## Candidate starting point

The Morpheus melanoma spatial-proteomics dataset is the first candidate because the original study uses it for counterfactual perturbation discovery and provides associated code and preprocessed resources.

- Morpheus paper: https://doi.org/10.1038/s41551-025-01357-0
- Dataset DOI cited by the paper: https://doi.org/10.5281/zenodo.5994135
- Original melanoma IMC data-for-analysis record: https://doi.org/10.5281/zenodo.5994136
- Morpheus reproduction repository: https://github.com/cellethology/morpheus-spatial
- Morpheus package/model code: https://github.com/neonine2/morpheus-spatial
- Preprocessed data and model outputs cited by the paper: https://doi.org/10.22002/pr14s-wgk05

The original melanoma cohort comprises 159 images/cores from 69 patients, with samples from sites including skin and lymph nodes. This gives repeated tissue samples for some patients, but the independent patient count remains 69. The CRC liver-metastasis cohort has 209 cores from 30 patients and is reported as available from the authors on request. The breast tumour cohort contains 693 patients, but the Morpheus paper states that its marker panel is not suitable for the same therapeutic perturbation analysis.

## Initial access findings

The original melanoma data-for-analysis Zenodo record describes a source archive of approximately 7.1 GB containing processed single-cell objects, clinical tables, classifier labels, and analysis code for the original melanoma IMC study. The Morpheus article separately cites preprocessed data and model outputs at the Dataverse DOI above. These are related but should not be assumed to be identical. Verify the exact files needed for reproducing Morpheus before downloading.

## Required checks before choosing data

For every dataset, record:
- Exact accession, version, source, publication, and retrieval date.
- Licence and permitted reuse.
- Number of patients, samples, tissue sections, and image patches.
- Patient identifiers and whether samples/patches can be grouped by patient.
- Available molecular markers and their units/normalization.
- Availability and definition of immune-infiltration outcome.
- Missingness, batch effects, and relevant covariates.
- Train/test splits used in the original paper.
- Whether the original code reproduces reported results.
- Storage, compute, and dependency requirements.

## Leakage prevention

- Split at the patient level wherever possible.
- Keep all samples, cores, sections, or patches from one patient within a single partition.
- Fit normalization, feature selection, imputation, and hyperparameter selection only on the training portion of each split.
- Use an untouched evaluation set or nested validation for model selection.
- Document any overlap between datasets and cohorts.

## Cross-cohort compatibility

Do not assume that spatial proteomics and bulk RNA-seq can be pooled directly. Before attempting cross-cohort analysis, establish compatible biological endpoints, target definitions, measurement platforms, and patient-level metadata. If they are incompatible, evaluate within-cohort robustness first and state that limitation.

## Data governance

Do not commit large raw data, restricted clinical data, identifiable information, credentials, or data whose licence prohibits redistribution. Store download instructions and checksums where useful; keep raw data outside version control.

## Current status

Dataset feasibility is **partially assessed from published metadata only**. No files have yet been downloaded, inspected locally, or validated in this project.
