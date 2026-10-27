# HCC VirTues compatibility review after structural QC

**Date:** 2026-10-27  
**Scope:** public source documentation plus the user's structural-audit summary. This is a documentation review, not a fresh execution against the original TIFF arrays.

## New source-confirmed facts

The HCC ICI Zenodo record describes the 42-patient dataset as preprocessed and normalized multistack TIFF images, with channel annotations in `ICICohort_panel.csv`. It says cell masks identify individual cells and stromal masks identify stromal and parenchymal regions. This means the stromal mask should not automatically be treated as a binary foreground/background mask.

VirTues' official reconstruction demo does not pass arbitrary TIFF arrays straight to the model. It uses `MultiplexImagingDataset` from `spora_io`, a per-dataset configuration, the panel-to-UniProt mapping, marker embeddings, dataset standardization statistics, Gaussian blur filtering, and a 128 × 128 crop. The demo's example standardizer is `QuantileClippingLog1PStandardizer` with global statistics, and the code explicitly uses the standardized Spora data format. Therefore, the HCC images' 0–1 range alone does **not** establish compatibility with official model inputs.

Official references:
- HCC ICI cohort record: https://zenodo.org/records/10794904
- VirTues repository and model documentation: https://github.com/bunnelab/virtues
- Official reconstruction demo: https://github.com/bunnelab/virtues/blob/main/notebooks/1_demo_reconstruction.ipynb
- HCC discovery cohort record: https://zenodo.org/records/10793609

## Interpretation of the user's structural QC

- 86 image/mask triplets read successfully.
- All images are reported as `(45, H, W)`, finite and within [0, 1].
- Cell and stromal mask dimensions match image dimensions in all 86 records.
- Stromal masks report labels 3–9 and zero fraction 0.0. Given the source description, this is a semantic/encoding check—not evidence by itself of corrupted masks. Inspect actual label frequencies, source convention, and visual overlays before deciding whether any background class is expected.
- The clinical table and image inventory still have a multiplicity discrepancy (84 clinical ROI entries versus 86 image triplets). Do not drop or merge ROIs without authoritative mapping.

## Updated gates — fail closed

1. **ROI crosswalk:** join filenames to the published patient/ROI metadata; explicitly resolve ICI_24 and ICI_39; preserve multiple ROIs per patient where supported.
2. **Channel contract:** parse `ICICohort_panel.csv` in channel order and match every channel to the official VirTues marker/UniProt embedding contract. Do not assume the channel index alone is enough.
3. **Mask convention:** inspect unique values and frequencies, overlay representative cell/stromal masks on marker images, and document the mask meaning. Do not recode masks by guesswork.
4. **Preprocessing:** reproduce the official `spora_io`/dataset standardization path where possible, including marker QC, channel filtering, dataset standardization statistics and Gaussian blur. If required stats or mappings are unavailable, classify the experiment as a separately labelled normalized-domain adaptation—not official-pipeline reproduction.
5. **Model provenance:** pin the chosen checkpoint, exact file hash, repository commit, config, dependencies, marker embeddings and licences. The `virtues-imc14` candidate remains conditional until the exact released checkpoint and preprocessing configuration are frozen.
6. **Smoke test:** only after gates 1–5, run a deterministic outcome-blind 128 × 128 reconstruction test. Score masked pixels/channels only and compare with the predeclared tissue-area/channel-mean baseline. Record failures and per-channel metrics.
7. **No clinical model yet:** the cohort is small, with only five PR/binary-positive patients in the current extraction; reconstruction is not clinical response validation. Keep patient-level outcome analysis out of this first smoke test.

## Current decision

**Structural QC: PASS based on the user's CSV output. Official model-input compatibility: UNPROVEN. Reconstruction inference: HOLD.** No biological discovery, clinical prediction, or reconstruction score is claimed.
