# Morpheus code and evaluation audit

**Status (25 October 2026): main article Methods and relevant public code inspected; separate supplementary PDF not yet read; no local data/model reproduction.**

## Sources inspected

- Main article/PDF: https://doi.org/10.1038/s41551-025-01357-0
- Public code/reproduction repository: https://github.com/cellethology/morpheus-spatial
- Model package repository named by the article: https://github.com/neonine2/morpheus-spatial
- Public tutorial notebook: https://github.com/cellethology/morpheus-spatial/blob/master/examples/tutorial.ipynb
- Preprocessed data/model outputs cited by the article: https://doi.org/10.22002/pr14s-wgk05
- Original melanoma IMC data-for-analysis: https://doi.org/10.5281/zenodo.5994136
- Melanoma dataset DOI cited by the article: https://doi.org/10.5281/zenodo.5994135
- Supplementary material landing page: https://authors.library.caltech.edu/records/6jd2w-a0388

The main Methods PDF and selected source files were inspected directly. The supplementary PDF is listed at the landing page, but a signed download redirect was not retrievable in this execution environment. Do not treat the supplement as audited.

## What Morpheus already does

1. Trains a U-Net classifier to predict CD8+ T-cell presence from spatial multiplexed tumour images, masking CD8+ signals to reduce direct label leakage.
2. Uses patient-level training, validation, and test splits.
3. Generates per-patch counterfactual perturbations with prediction, distance/sparsity, and prototype-related objectives.
4. Constrains each molecule's relative perturbation to apply uniformly across cells within an image.
5. Aggregates patch-level perturbations by the median to make whole-tumour strategies; the paper also reports within-patient and across-patient aggregation.
6. Evaluates predicted strategies in silico on test-patient samples.
7. Reports in-vitro validation for selected combinations.
8. Examines sensitivity to perturbation sparsity settings and discusses variation across tissue samples, including samples from the same patient.

These facts rule out novelty claims for counterfactual discovery itself, patient-level splitting, aggregation into whole-tumour strategies, held-out-patient model evaluation, within-patient variation, or selected in-vitro validation.

## Code-level findings

- The entry script main.py begins with seed_everything(42). This is a fixed seeded run setup, not evidence of a multi-seed robustness study.
- The tutorial notebook also sets seed 42, downloads crc_tutorial.zip from the Caltech Data Portal record ID pr14s-wgk05, and uses a saved unet.ckpt and patient_split.json.
- The public code carries PatientID, ImageNumber, and patch_id metadata. The analysis helper maps counterfactual outputs back to patient/image information and aggregates perturbations.
- The generation function chooses a decision threshold using the validation split before generating counterfactuals.
- TrustScore estimates whether a classifier input resembles samples from the predicted class versus other classes using nearest-neighbour distances. It is not a stability score for complete molecular intervention sets across retrained models or patient resamples.
- The inspected repository code has a reproduction notebook, counterfactual-generation machinery, patient/image metadata helpers, and analysis code for perturbation patterns. Repository searches did not find a dedicated bootstrap or repeated full-discovery benchmark. A search result is not proof that no such analysis exists in supplementary files or other literature.

## The candidate distinction—and its limits

The main paper already forms strategies by taking medians of patch-level and patient-level perturbations and evaluates them in silico on held-out patients. The candidate question is narrower: if the entire discovery process is repeated with different patient-grouped training samples and independently retrained model seeds, do the same signed target sets reappear, and does a consensus chosen without accessing outer test patients perform better at a matched target budget?

This candidate is still high-risk and unverified. PHAROS (a 2026 preprint) already searches target-directed drug combinations and uses multiple sampled batches and robustness-aware re-ranking, albeit in a different single-cell perturbation setting. A generic resampling/Jaccard analysis or generic combination-ranking method is not enough.

## Data and compute constraints

- Morpheus melanoma cohort: 159 tumour cores from 69 patients, 39 molecular channels including chemokines. Independent unit for resampling/inference is the patient, not the core/patch.
- Morpheus CRC liver-metastasis cohort: 209 sections from 30 patients. The paper reports the source data as available from the authors on request; the public tutorial bundle is a separate example/reproduction route.
- Morpheus breast cohort: 749 cores from 693 patients; the article states its panel is not suitable for the same therapeutic perturbation analysis.
- The original melanoma data-for-analysis archive is about 7.1 GB, with an approximately 41 MB code archive. It is not the same as the preprocessed Morpheus data/model-output record or the CRC tutorial.
- The public package specifies Python >=3.9 and <3.12 and uses PyTorch, Lightning, NumPy and other dependencies. Its README/tutorial warns that counterfactual generation can be expensive and may require GPU/parallel compute.
- The original melanoma Zenodo record has no clear license value displayed in its Rights section. The article's CC BY-NC-ND license applies to the article and does not automatically grant license rights over separately deposited data. Confirm the exact data and code terms before redistribution or use that requires permission.
- No full archive has been downloaded, no model checkpoint has been loaded, and no model training/counterfactual generation has been executed in this project. Direct network retrieval from this runtime failed due a network/name-resolution error; this does not show the dataset is unavailable online.

## Reproduction gate

1. Retrieve and read the complete supplementary PDF.
2. Resolve licence and access terms for the exact code/data artifacts.
3. Run the small tutorial path or use authorized cached outputs and record checksums/version details.
4. Reproduce one baseline result before changing the method.
5. Measure compute requirements on a small subset.
6. Distinguish any inexpensive cached-output resampling from full pipeline resampling plus retraining.

## Preliminary conclusion

Morpheus remains the closest relevant spatial counterfactual baseline. The most defensible candidate study is a patient/core-hierarchical reproducibility benchmark, separating patient-sampling variability from model-seed variability and evaluating only on held-out patients. Proceed only to the feasibility pilot until the supplement, prior art and baseline reproduction gates pass.
