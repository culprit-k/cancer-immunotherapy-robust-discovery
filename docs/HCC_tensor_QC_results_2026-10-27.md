# HCC ICI cohort: structural tensor QC results

**Date recorded:** 2026-10-27  
**Evidence source:** user-provided output from the Colab structural-audit notebook. This is a transcription/interpretation of those outputs, not a claim that the author independently reran the archive in this environment.

## Summary

The structural audit reported 86 image files, 86 cell masks, and 86 stromal masks. All 86 image records had read status `OK`; the inventory reported no non-OK records and no potentially problematic ROIs under the checks implemented in the notebook.

The marker panel contained 45 rows and 45 unique channel numbers, with channel numbers exactly 1–45. All 86 images were reported in channels-first format, with array shapes of the form `(45, height, width)`. Spatial dimensions matched for image/cell-mask pairs and image/stromal-mask pairs for all 86 records.

Across images, the reported intensity minimum was 0, maximum was 1, finite fraction was 1, and negative fraction was 0. This is consistent with a normalized 0–1 image domain, but does not establish equivalence to the official VirTues preprocessing pipeline.

## Observed shape variation

The output reported 64 distinct image shapes. Examples of repeated shapes included `(45, 1200, 1200)` for 15 images and `(45, 1000, 1000)` for 8 images. Other images had different spatial dimensions. Any reconstruction pilot must therefore use an explicit, deterministic crop/ROI policy and must not assume a single global image size.

## What this establishes

- Files were readable by the notebook's chosen TIFF reader.
- The expected 45-channel-first structure was observed for all 86 images.
- The panel file had 45 unique channel numbers, exactly 1–45.
- Image and mask spatial dimensions matched for all 86 records under the implemented checks.
- No non-finite or negative image values were reported.
- The notebook's implemented structural checks flagged no problematic ROI records.

## What this does not establish

- It does not verify the semantic identity/order of image channels against the panel's marker names and metal tags.
- It does not prove that cell/stromal masks are biologically correct or use the expected label semantics.
- It does not reconcile the 86 image triplets with the previously audited 84 clinically represented ROIs.
- It does not establish that ROIs are independent, that each file corresponds to a unique patient, or that filenames map correctly to clinical outcomes.
- It does not establish compatibility with VirTues model inputs, official preprocessing, checkpoint provenance, or inference.
- It does not constitute a biological finding, a biomarker result, or clinical prediction performance.

## Required gates before inference

1. **ROI reconciliation:** build a filename-to-ROI-to-patient crosswalk from authoritative source metadata. Specifically resolve the previously flagged ICI_24 and ICI_39 multiplicities. Quarantine unresolved records; do not infer mappings from filename order.
2. **Channel mapping:** export the full 45-row panel (channel, metal tag, target, comment), inspect duplicate/missing targets and confirm the exact mapping expected by the selected checkpoint and official code.
3. **Mask semantics:** inspect unique values/label counts and representative overlays for image, cell mask, and stromal mask; verify mask conventions from source documentation.
4. **Checkpoint provenance:** pin exact model file, hash, code commit, configuration, dependency versions, and documented training cohort. Do not use `virtues-sp32` for an independent held-out HCC evaluation because the expanded training corpus includes the HCC cohort.
5. **Preprocessing parity:** establish the official preprocessing path. Do not assume the source images' 0–1 normalization is equivalent to VirTues clipping, dataset-wise standardization, and Gaussian smoothing.
6. **Pilot:** only after gates 1–5 pass, run a deterministic, outcome-blind reconstruction smoke test on one eligible ROI and compare masked-pixel error against a predeclared tissue-area-mean baseline.

## Data governance

Keep image arrays, masks, patient-level tables, completed crosswalks, and model weights out of GitHub. Commit only aggregate QC summaries, code, and non-identifying documentation. The source archive should remain in the private runtime or approved storage.

## Current gate status

| Gate | Status |
|---|---|
| Basic file readability | PASS (reported by notebook) |
| 45-channel array shape | PASS (reported by notebook) |
| Image/mask spatial shape agreement | PASS (reported by notebook) |
| Finite and non-negative image values | PASS (reported by notebook) |
| Exact channel-to-marker mapping | OPEN |
| Mask label semantics/visual overlays | OPEN |
| 86-file vs 84-clinical-ROI reconciliation | OPEN |
| Checkpoint/code/config provenance | OPEN |
| Official preprocessing compatibility | OPEN |
| VirTues inference | NOT RUN |

**Decision:** structural QC is encouraging, but the project remains **NO-GO for inference** until the open gates above are resolved.