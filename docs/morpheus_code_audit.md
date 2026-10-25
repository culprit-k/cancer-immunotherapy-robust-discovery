# Morpheus code and evaluation audit

**Status:** First-pass public-paper and repository inspection. This is not yet a successful local reproduction.

## Sources inspected

- Paper: https://doi.org/10.1038/s41551-025-01357-0
- Published code/reproduction repository: https://github.com/cellethology/morpheus-spatial
- Model package repository named by the paper: https://github.com/neonine2/morpheus-spatial
- Preprocessed data and model outputs cited by the paper: https://doi.org/10.22002/pr14s-wgk05
- Melanoma dataset record cited by the paper: https://doi.org/10.5281/zenodo.5994135
- Data-for-analysis deposit for the original melanoma IMC study: https://doi.org/10.5281/zenodo.5994136

## What Morpheus already does

1. Trains a U-Net classifier to predict CD8+ T-cell presence from spatial multiplexed tumour images, masking CD8+ cells to reduce direct label leakage.
2. Splits patients into training, validation, and test groups (the article describes an approximate 65/15/20 ratio with class-balance constraints).
3. Generates counterfactual perturbations per image patch using prediction, distance, and prototype-related objectives.
4. Aggregates and clusters patient-level perturbation patterns and reports cohort-dependent target combinations.
5. Takes median perturbations across samples to define whole-tumour strategies, then evaluates predicted T-cell distribution after applying those strategies in silico to a test patient cohort.
6. Reports in-vitro validation of selected predicted combinations.
7. Discusses variation between tissue samples, including samples from the same patient, and proposes future testing where perturbations derived from some samples are assessed on remaining samples.

These points rule out claiming novelty for patient-level splitting, per-patch counterfactual discovery, patient-specific variation, or experimental testing of selected combinations.

## What we checked in the public implementation

The repository contains a reproduction notebook, helper code for retrieving counterfactual perturbations and merging patch identifiers with patient/image metadata, and a counterfactual generation implementation. The inspected analysis helper calculates classifier prediction error aggregated by image and retrieves per-patch perturbations; it also supports analyses of perturbation patterns and patient metadata.

The package includes a TrustScore implementation for assessing whether classifier inputs resemble examples from predicted classes. This is not equivalent to measuring whether a complete therapeutic recommendation remains stable across patient resampling or model retraining.

In the main article and inspected public helper code, we found a fixed patient-level train/validation/test design, aggregation of per-patch perturbations into cohort strategies, and in-silico evaluation on test patients. We did not identify a dedicated benchmark that systematically repeats the *entire discovery pipeline* across many patient-level resamples and retrained models, then quantifies complete-combination stability alongside independent predictive/biological evaluation. This is a **provisional observation**: the full supplementary material and all notebook cells have not yet been exhaustively audited, and related literature remains to be searched.

## Key methodological distinction

Morpheus has an independent patient test split for the T-cell classifier and reports therapeutic perturbation results across patients. This is not the same as repeatedly re-running the entire target-discovery procedure under alternative patient samples and measuring how the resulting *sets of targets* change.

Our possible gap, if confirmed, is therefore not “patient-level validation.” It is a carefully defined audit of the *reliability of the recommendation-generating process itself*.

## Constraints and feasibility

- The melanoma cohort contains 159 image cores from 69 patients. Multiple cores per patient are not independent observations.
- The CRC liver-metastasis cohort contains 209 cores from 30 patients; it is reported as available from the authors on request.
- The breast tumour dataset is useful for validating classifier performance but the paper says its marker panel is not suitable for the same therapeutic-perturbation analysis.
- The source dataset deposit for the original melanoma IMC analysis is about 7.1 GB, while the Morpheus paper also cites separate preprocessed data/model outputs. Verify exactly which files are needed before downloading.
- The package documentation recommends Python 3.9–3.11 and lists PyTorch Lightning, PyTorch and other dependencies; CUDA is recommended for acceleration. A CPU-only feasibility run may be possible but must be tested.
- No data have yet been downloaded and no reproduction has been run in this project.

## Next reproducibility gate

1. Inspect the full supplementary material and notebook for any existing robustness or resampling analyses.
2. Verify the preprocessed data DOI resolves and list the available files and licence.
3. Inspect the notebook's exact data paths, model checkpoints, and expected outputs.
4. Determine whether the saved patient split and target perturbations are sufficient for an initial analysis.
5. Download a manageable permitted subset or preprocessed artifact and attempt a smoke test; do not begin a full reproduction before this succeeds.
6. Record missing files, environment conflicts, runtime, and any deviation from the paper.

## Preliminary conclusion

Morpheus is a suitable methodological baseline to inspect because it directly addresses spatial tumour perturbations and already provides patient-level splits and some sample-level analysis. The candidate robustness question remains plausible but unverified. A narrow audit of repeated discovery stability may be worth testing only after the supplementary methods, notebook, and related robust-counterfactual literature are checked more thoroughly.
