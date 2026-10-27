# HCC cohort readiness and VirTues checkpoint decision — 2026-10-27

## 1. Patient-to-ROI mapping: resolved at the patient level

I parsed the extracted Supplementary Table 3 text and reconciled it against the structural inventory. Results: 42 clinical patient rows, 86 image files, 42 unique image patient prefixes, no image patient prefix absent from the clinical table, and no clinical patient without images. The table's `No. of ROIs` fields sum to 84, whereas the paper's HCC ICI dataset contains 86 images/ROIs.

Only two patient-specific count conflicts remain: ICI_24 is reported as 2 but has ROI1–ROI3 images; ICI_39 is reported as 1 but has ROI1–ROI2 images. These are explicitly recorded in `data/derived/hcc_patient_roi_reconciliation_2026-10-27.json`. The image-to-patient mapping is resolved from the `ICI_XX` filename prefix; the mismatched counts are not silently corrected. The crosswalk is `data/derived/hcc_roi_patient_crosswalk_2026-10-27.csv`.

**Outcome unit:** clinical outcomes in Supplementary Table 3 are patient-level. The combined manifest repeats each patient's outcome on their image rows for convenience; these are not 86 independent labels. Aggregate ROI features to one record per patient and split only by patient. The cohort has 42 patients and only five PR cases; do not fit or describe a complex response classifier as validated on this dataset.

Sources: [Zenodo HCC ICI cohort, record 10794904](https://zenodo.org/records/10794904); [Salié et al., Gut](https://gut.bmj.com/content/74/3/451).

## 2. Candidate model and cohort-exposure decision

**Use `virtues-imc14` as the candidate checkpoint; exclude `virtues-sp32` from a held-out HCC evaluation.** The published VirTues methods describe the HCC ICI study by Salié et al. as one of seven additional IMC cohorts added to the expanded 32-cohort multi-technology corpus, whereas the released `virtues-imc14` is described as an IMC-only checkpoint trained on 14 IMC datasets. The expanded `virtues-sp32` corpus includes these additional cohorts, so it is not appropriate for claiming held-out HCC transfer.

Checkpoint pin recorded from the specific Hugging Face file page:
- Repository: `bunnelab/virtues`
- Model path: `virtues-imc14/model.safetensors`
- Immutable file commit: `9d1250295536cc8c72360677e3db86a7b849e5cd`
- SHA-256: `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`
- Xet hash: `4ce9adfb786c209633ad356d9a92537ab08b22f166f225b44cb272470bec07bc`
- Published weight licence: CC BY-NC 4.0; use is non-commercial and requires compliance with that licence.

This is a **publication-level no-direct-cohort-overlap decision**, not a substitute for recording the actual local file SHA-256 and the exact source commit when downloading. Verify that the local checkpoint matches the values above before inference. Do not use the SHA reported for the root `model.safetensors` as an identity for another file unless they match exactly.

Sources: [VirTues paper, Nature (2026)](https://www.nature.com/articles/s41586-026-10884-y); [official model repository](https://huggingface.co/bunnelab/virtues); [pinned imc14 file](https://huggingface.co/bunnelab/virtues/blob/9d1250295536cc8c72360677e3db86a7b849e5cd/virtues-imc14/model.safetensors).

## 3. Preprocessing compatibility: official reproduction blocked; adaptation pilot is permissible

VirTues describes channel-wise 99th-percentile clipping, shifted-log transformation (size factor 1), per-dataset/channel standardisation using tissue-region statistics, and Gaussian smoothing (kernel size 3, unit variance). The released HCC images in the available QC inventory are `float32` and span [0,1], documented as preprocessed/normalised by the data release. The original intensity scale and exact operations leading to those [0,1] values have not been established here; normalisation is not generally invertible.

Decision:
- **Do not label an inference run on the released normalized TIFFs as a reproduction of the official VirTues preprocessing.**
- A separate, explicitly named **normalized-domain reconstruction pilot** may proceed only after the panel-to-channel index is verified and the exact checkpoint hash matches. It should be outcome-blind, use a predeclared seed and fixed 128×128 crops, score only intentionally masked pixels, report per-channel and pooled MSE/MAE, and compare against a simple visible-pixel channel-mean baseline. Label it a domain-adaptation/feasibility experiment, not clinical prediction or biological target discovery.
- Do not use ambiguous stromal-mask IDs for tissue-only normalisation until their values are mapped to classes from an authoritative source. The published paper describes a parenchyma/stroma pixel classification, but the available numeric audit shows IDs 3–9; the numeric encoding itself has not been authoritatively mapped.

## 4. Remaining hard gates before a biological claim

1. Run the panel validator on the actual `ICICohort_panel.xlsx` in the existing Colab and retain the JSON/CSV result. The structural audit confirms 45 channels first in every inspected image; that does not by itself independently prove marker names are ordered identically to image planes.
2. Obtain an authoritative encoding for values 3–9 in `ICI_stromamasks`, or keep stromal compartment analyses disabled.
3. Run the outcome-blind normalized-domain pilot, if the panel and checkpoint gates pass.
4. Any later outcome analysis is exploratory with only five PR cases, patient-level aggregation and patient-grouped uncertainty. No robust target or clinical performance claim is established until independently evaluated.

## Status vocabulary

- `RESOLVED`: image-to-patient linkage from filename prefixes and complete structural inventory.
- `DISCLOSED SOURCE DISCREPANCY`: Table 3 ROI count fields for ICI_24 and ICI_39.
- `PINNED CANDIDATE`: `virtues-imc14` model file revision and SHA as above.
- `BLOCKED`: official preprocessing reproduction on normalised inputs and numeric stromal-mask class mapping.
- `NOT YET RUN`: panel validation against the actual workbook in Colab, and any VirTues inference on the HCC images.
