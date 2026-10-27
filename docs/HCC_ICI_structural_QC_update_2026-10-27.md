# HCC ICI cohort: full structural QC update (2026-10-27)

## Scope and evidence
This update summarizes the private Colab audit output shared on 2026-10-27. The private dataset and patient-level records are not included here. The audit output lists:
- archive: `HCC_ICICohort.zip`, 882,022,729 bytes;
- panel: `ICICohort_panel.xlsx`, Sheet1 with 45 rows and columns `Channel`, `MetalTag`, `Target`, `Comment`;
- 86 image TIFFs, 86 cell-mask TIFFs, and 86 stromal-mask TIFFs with matching filename triplets.

## Confirmed structural results
- Panel channel numbers are 1–45 with no missing or duplicate channel numbers.
- Across the 86 image/mask triplets, the structural audit reports status `OK`; the image stack is channels-first with shape `(45, H, W)`, dtype `float32`, finite fraction 1.0, and observed range [0,1].
- Cell masks are `uint16`; spatial dimensions match image dimensions. Nonzero values behave as instance labels in the inspected summary, but this does not itself certify the segmentation algorithm or biological meaning of each cell.
- Stromal masks are `uint16`; spatial dimensions match image dimensions. The inspected audit reports labels 3–9 in all 86 ROIs. Do not assign semantics to individual codes without an authoritative source.
- Representative mask-review PNGs and aggregate label-count CSVs were produced in the user's private Colab workspace.

## Important interpretation limits
1. Structural shape/range checks do not verify that TIFF plane order corresponds exactly to the Excel panel order. Confirm channel-to-marker mapping using source documentation or a known reference ROI before model input.
2. The dataset landing page describes cell masks and masks for stromal/parenchymal regions, but the available description does not define the meanings of individual numeric stromal-mask labels 3–9. No mapping should be guessed.
3. The clinical table has 84 ROI entries while the image/mask inventory has 86 filenames. Prior audit identified discrepancies for ICI_24 (clinical 2, image filenames 3) and ICI_39 (clinical 1, image filenames 2). These remain unresolved without the authoritative crosswalk.
4. Public image values [0,1] are consistent with a normalized export but are not interchangeable with VirTues' documented clipping/log/blur/standardization input representation. Do not invert normalization or fabricate missing statistics.
5. Do not use `virtues-sp32` for held-out HCC evaluation because its training corpus includes the Salié HCC cohort. `virtues-imc14` remains a candidate subject to the existing revision/hash/provenance caveats; `virtues-sp31` remains unapproved until its omitted cohort is confirmed.

## Decision
**GO:** continue metadata/source crosswalk work and outcome-blind compatibility checks.
**NO-GO:** official VirTues inference on the released normalized HCC TIFFs until preprocessing and channel mapping are verified; clinical outcome analysis for ambiguous ROIs; biological or novelty claims from these structural QC outputs.

## Next actions
- Retrieve supplementary Table 3 and the original ROI/patient crosswalk; quarantine ambiguous ROIs rather than infer a match.
- Ask the dataset contact for the stromal-mask label-code definition, channel-order confirmation, and original-scale inputs/preprocessing statistics.
- Pin and independently verify the selected checkpoint revision and weight hash, plus training-exposure evidence.
- If original-compatible inputs cannot be obtained, preregister a separate normalized-domain adaptation pilot with patient-held-out splits, per-marker metrics, simple baselines, and predeclared failure thresholds. Label it as adaptation, not reproduction of official preprocessing.

## Public dataset documentation
The Zenodo description for record 10794904 says the archive contains normalized multistack TIFFs, a panel table, cell masks, stromal/parenchymal masks, and points to supplementary table 3 for patient metadata. It does not, in the description itself, document the meanings of numeric stromal-mask codes.
