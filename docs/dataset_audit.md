# Dataset feasibility audit

## Candidate starting point

Morpheus's published melanoma spatial-proteomics dataset is a candidate because the original study uses it for counterfactual perturbation discovery and provides associated code and preprocessed resources.

- Article: https://doi.org/10.1038/s41551-025-01357-0
- Dataset DOI: https://doi.org/10.5281/zenodo.5994135
- Code: https://github.com/neonine2/morpheus-spatial
- Additional preprocessed data/model outputs: https://doi.org/10.22002/pr14s-wgk05

These links identify candidate resources, not confirmation that we have downloaded, inspected, or reproduced them.

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
