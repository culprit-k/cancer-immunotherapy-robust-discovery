# Next QC run: ROI pairing and mask-label audit

**Date:** 2026-10-27  
**Branch:** `hcc-virtues-audit-next-step`  
**Purpose:** produce reproducible, metadata-only structural QC from the HCC ICI cohort in the user's Colab runtime.

## Current evidence from the supplied Colab output

- 86/86 images, 86/86 cell masks, and 86/86 stromal masks were found.
- The displayed ROI-key table reports successful filename pairing for the shown rows.
- Cell masks are 2D `uint16` arrays with thousands of unique values in the sampled ROIs.
- The script deliberately labels mask semantics as unverified. A high number of unique values is consistent with instance labels but is not proof of their biological meaning.
- This is not a VirTues inference result and does not resolve the 84-clinical-ROI versus 86-image discrepancy.

## Run in Colab

Clone or pull the research branch, then install the lightweight dependencies:

```python
!git clone --branch hcc-virtues-audit-next-step https://github.com/culprit-k/cancer-immunotherapy-robust-discovery.git
%cd cancer-immunotherapy-robust-discovery
!pip -q install tifffile pandas numpy
```

Set the three folder paths to the extracted archive's actual locations. Do not guess folder names; list the extracted directory first:

```python
from pathlib import Path
root = Path("/content")  # change if the archive was extracted elsewhere
for p in root.rglob("ICI_img_normalized"):
    print("images:", p)
for p in root.rglob("ICI_cellmasks"):
    print("cell masks:", p)
for p in root.rglob("ICI_stromamasks"):
    print("stromal masks:", p)
```

Then run (replace the three placeholders with the paths printed above):

```python
!python scripts/hcc_roi_mask_validation.py \
  --images "/PATH/TO/ICI_img_normalized" \
  --cell-masks "/PATH/TO/ICI_cellmasks" \
  --stromal-masks "/PATH/TO/ICI_stromamasks" \
  --out "/content/hcc_virtues_audit/roi_mask_qc"
```

## Expected outputs

- `roi_pairing_qc.csv`: filename presence, shapes, shape agreement, and file hashes.
- `mask_label_summary.csv`: shape, dtype, zero fraction, unique-value count, sample of nonzero values, and hashes. It does not export pixel arrays.
- `qc_summary.json`: compact aggregate counts and mismatched keys.

Keep these outputs in the private Colab workspace initially. Do not commit raw images, masks, patient-level data, or identifying clinical rows to the public repository.

## How to interpret the report

1. Every ROI should be `PAIRED_SHAPES_MATCH` before proceeding to visual review.
2. A matching filename and shape are necessary but not sufficient for clinical mapping.
3. Verify cell-mask label semantics and stromal-mask value conventions against the dataset's source documentation and inspect overlays for a few representative ROIs.
4. Build the clinical ROI crosswalk from authoritative source records. Keep `ICI_24` and `ICI_39` quarantined until the 86-vs-84 discrepancy is resolved; do not infer the mapping from filenames.
5. Confirm the 45-channel-to-marker mapping against the exact panel file.
6. Do not run official VirTues inference on the normalized 0–1 TIFFs unless official preprocessing compatibility is established. If the only viable path is a normalized-domain adaptation, label and evaluate it separately.

## Gate decision

This utility only advances structural QC. It cannot establish mask biology, clinical ROI identity, checkpoint exposure, preprocessing equivalence, or scientific novelty. The next gate remains blocked until these are independently verified.
