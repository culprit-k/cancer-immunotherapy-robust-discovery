# Review of uploaded HCC structural audit CSV

**Date:** 2026-10-27  
**Source:** user-uploaded `structural_audit_stage2.csv` (86 rows, 21 columns). This review was computed from the uploaded CSV; the original image and mask arrays were not re-opened in this review.

## Confirmed from the CSV

- 86 records; no duplicate filenames.
- `read_status=OK` for all 86 records.
- Cell mask and stromal mask files were present for all 86 records.
- `channels_45_first=True` for all 86 images; image shapes are `(45, H, W)`.
- `image_finite_fraction=1.0`, `image_min=0.0`, `image_max=1.0`, and `image_negative_fraction=0.0` for all records.
- Cell-mask and stromal-mask spatial dimensions match the image dimensions for all 86 records.
- 64 distinct image shapes were reported, so downstream crop selection must be explicit and deterministic.
- Cell-mask label-count summary: minimum 1,270, median 5,856, maximum 14,019 (as reported by the QC script).
- Every record reports `stroma_label_count=7`, `stroma_labels=[3, 4, 5, 6, 7, 8, 9]`, and `stroma_zero_fraction=0.0`.

## Follow-up issue: stromal-mask semantics need validation

The combination of exactly seven stromal labels (3–9) and a zero fraction of 0.0 in every ROI means the exported stromal mask has no zero-valued pixels according to the current audit. This is not automatically an error: the masks may use a non-binary labeling convention or have been encoded in a way that assigns every pixel a label. However, it is unusual enough that the meaning of the mask and the definition of `stroma_zero_fraction` must be checked against the source's mask-generation code/documentation before treating these arrays as a tissue/background mask.

**Required action:** inspect the source mask-generation convention and create private visual overlays for representative ROIs. Confirm whether values 3–9 are class labels, region IDs, or another encoding; determine whether any background class should exist; and document whether the QC script's zero-fraction statistic is meaningful for this mask type. Do not modify or recode masks by guesswork.

## Remaining blockers

1. Reconcile the 86 image/mask triplets with the previously audited 84 clinical ROIs using authoritative metadata. The CSV filename list shows multiple ROIs for many ICI IDs; specifically verify the known clinical multiplicity discrepancy for ICI_24 and ICI_39. Multiple ROIs per patient are not themselves a problem, but the correct mapping and analysis unit must be established.
2. Verify the exact channel-to-marker mapping from the panel and official checkpoint input contract.
3. Validate mask semantics with documentation and overlays.
4. Pin model weights, code commit, configuration, and dependencies.
5. Demonstrate preprocessing compatibility; 0–1 normalization alone does not prove equivalence to official VirTues preprocessing.
6. Only after these checks, run an outcome-blind, deterministic reconstruction smoke test with a predeclared baseline.

## Decision

**Structural file checks: PASS. Model-input compatibility: NOT YET ESTABLISHED. Inference: HOLD.** No biological result, clinical prediction, or reconstruction metric is claimed from this audit.