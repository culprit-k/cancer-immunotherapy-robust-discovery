# Public source-data check and immediate next experiment

**Checked:** 2026-10-26

## What the public records establish

The Zenodo record for the 42-patient ICI-treated HCC cohort describes the available image data as preprocessed and normalized multistack TIFF images, with separate cell and stromal masks and a channel annotation table. The source record lists an 882 MB archive but does not display a populated licence in its visible Rights field. The associated Gut article states that the discovery and ICI-cohort imaging data and masks are publicly downloadable from Zenodo and that the article is CC BY 4.0. Preserve both facts; do not silently treat an absent dataset-level licence display as a separate explicit licence grant.

Source record: https://zenodo.org/records/10794904
Associated article/data availability: https://gut.bmj.com/content/early/2024/09/30/gutjnl-2024-332837?versioned=true

The public description does not identify original-scale instrument intensities or provide enough evidence to reconstruct the exact VirTues preprocessing statistics. PENGUIN-normalized [0,1] TIFFs must not be treated as original intensity values. The project has already sent the authors a clarification request for original-scale intensities and preprocessing details.

## Immediate next step

Use the available normalized cohort only for **data-structure and explicitly labeled normalized-domain adaptation feasibility**, not for a claim of official VirTues preprocessing reproduction. Do not start outcome analysis until the input pipeline and checkpoint exposure gates pass.

1. Run the new `scripts/hcc_preinference_preflight.py` against the controlled local data copy and inspect every image/mask filename triplet.
2. Reconcile ICI_24 and ICI_39 against the supplementary table and source file mapping.
3. Inspect per-file TIFF dimensions, dtype, channel order, finite values and mask labels. A complete filename triplet alone is insufficient.
4. Keep the 42-patient ICI cohort out of development/tuning if it is to be used as external evaluation.
5. If original-scale inputs are not provided, define a separate adaptation protocol and train/validate on patient-held-out development patients; compare against a simple baseline. Report this as adaptation, not as a reproduction of the published VirTues input pipeline.

## Current status

The public-source check supports that the cohort images are preprocessed/normalized. It does not resolve original-scale availability, precise preprocessing equivalence, patient-level ROI mapping, or checkpoint eligibility. No inference or outcome model has been run and no biological result is established.