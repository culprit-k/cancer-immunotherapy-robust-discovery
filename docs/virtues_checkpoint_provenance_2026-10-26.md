# VirTues checkpoint provenance decision log
**Audit date:** 2026-10-26  
**Status:** strong paper-based exposure distinction recorded; final checkpoint eligibility still requires matching the exact inference implementation/config and reviewing the released training manifest.

## Immutable model-weight identity
- Hugging Face repository: https://huggingface.co/bunnelab/virtues
- Candidate weight: `virtues-imc14/model.safetensors`
- File SHA-256 shown on the model file page: `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`
- File-specific commit: `9d1250295536cc8c72360677e3db86a7b849e5cd`
- File page: https://huggingface.co/bunnelab/virtues/blob/main/virtues-imc14/model.safetensors
- File-specific commit: https://huggingface.co/bunnelab/virtues/commit/9d1250295536cc8c72360677e3db86a7b849e5cd
- Licence for the IMC-only model weights: CC BY-NC 4.0. Record attribution and the non-commercial restriction; do not assume this licence permits commercial use.

The weight hash and file revision identify the weights but do not alone freeze code, configuration, dependencies or inference preprocessing. Pin those separately in an eventual run record.

## Training-exposure evidence in the Nature paper
The main text describes the IMC-only pretraining corpus as 14 datasets spanning lung, breast, colon, kidney, head/neck, melanoma, tonsil, endometrium and pancreas. It then describes seven additional IMC datasets added to create the expanded 32-cohort multi-technology corpus. The additional-cohort reference list includes Salié et al.'s 2025 HCC study (Gut 74:451–466, cited as reference 95).

Sources:
- Nature 2026 main text, “Datasets for VirTues development,” especially dataset curation and released model instances: https://www.nature.com/articles/s41586-026-10884-y
- Nature supplementary Tables 1–2, referenced by the article as the cohort-level inventory of the 14 IMC and expanded 32-cohort datasets.
- Salié et al. HCC study: https://gut.bmj.com/content/74/3/451

## Current checkpoint decision
- **`virtues-sp32`: NO-GO for held-out evaluation on the Salié HCC cohort.** The HCC study is among the expanded corpus's additional IMC datasets, so this checkpoint has cohort exposure.
- **`virtues-imc14`: leading candidate; conditionally eligible for HCC-excluded transfer evaluation.** The main-text composition of the 14-dataset corpus does not list HCC, and the Salié study appears in the later added-cohort references. Before a final claim, cross-check the exact supplementary dataset table/model release configuration to ensure the downloaded checkpoint is the intended IMC-only instance and no HCC derivative has entered via another dataset.
- **`virtues-sp31`: not approved** until its omitted-cohort identity and exact revision are verified.

## Still unresolved even if checkpoint exposure is acceptable
1. HCC images/masks and full tensor QC are not present in the current execution workspace.
2. HCC marker/channel ordering and protein-ID mapping are not verified.
3. Clinical ROI count (84) does not match image/mask triplet count (86); ICI_24 and ICI_39 need crosswalk resolution or quarantine.
4. Released HCC TIFF normalization (PENGUIN-normalized to [0,1]) is not proven equivalent to VirTues' tissue-mask-aware 99th-percentile clipping, shifted log1p, dataset-wise channel standardization and Gaussian blur.
5. If official input processing cannot be reproduced, a separately labelled normalized-domain adaptation may be tested; it must not be reported as official preprocessing reproduction.
6. No reconstruction metrics, outcome modelling or biological result has been produced.

## Claim boundary
Checkpoint exposure control reduces a leakage threat; it does not establish model validity, novelty, performance, outcome prediction or target discovery. The current decision only supports advancing the IMC-only checkpoint to the next compatibility gate.
