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

## Follow-up checks (2026-10-27)

### CI status
At commit `39912eba8116c59b1a9e3005511dc637c458c7be`, two GitHub Actions runs completed successfully:
- **HCC pre-algorithm metadata-gate tests** (run `40486154373`): script compilation and existing metadata-validator unit tests passed.
- **Analysis helper tests** (run `40486154257`): synthetic unit tests passed.
These are software/metadata checks only. They do not mean the private dataset was downloaded in this execution environment, that tensor-level QC was independently reproduced here, or that VirTues inference ran.

### Panel validator regression tests added
After the above successful runs, the workflow was strengthened to install `pandas`/`openpyxl`, compile `scripts/validate_hcc_panel.py`, and run new integration tests covering a valid sorted export, duplicate channel rejection, blank-field rejection, and missing-column rejection. The test file is `tests/test_validate_hcc_panel.py`. The workflow/test changes are committed after `39912eba8116c59b1a9e3005511dc637c458c7be`; their CI result must be checked separately and is not represented by the earlier successful run IDs.

### Source clarification
The official Zenodo record confirms that the ICI archive contains normalized multistack TIFFs, a marker panel, cell masks, and masks identifying stromal and parenchymal regions; it directs users to supplementary table 3 for patient metadata. It does not provide an explicit numeric-code dictionary for stromal-mask labels 3–9. The article describes spatial immunotypes (depleted, compartmentalized, enriched) associated with different ICI outcomes. Therefore, simply re-describing these spatial phenotypes or reporting a broad association with outcome would not, by itself, establish novelty. A defensible contribution would need a clearly differentiated, predeclared AI/methodological claim and independent validation.

### Research novelty gate
Before any outcome analysis, compare the proposed contribution directly against the published HCC spatial-immunotype analysis and other recent work on spatial immune architecture/ICI response. Keep the claim narrow: e.g., robustness and transportability of a specified model-derived pattern across patient-level held-out data, only if a permitted independent cohort and compatible measurements can actually support that test. Do not describe this as causal target discovery unless the design supports causal inference. If no independent compatible cohort is available, frame results as exploratory within-cohort method evaluation and state that limitation.

### Remaining hard blockers (unchanged)
- Obtain an authoritative mapping between the 86 image ROIs and the 84 clinical ROI entries; exclude ICI_24 and ICI_39 from clinical analysis until resolved.
- Verify TIFF plane-to-panel ordering from a source of record or a known reference ROI.
- Obtain the numeric stromal-mask label dictionary and confirm cell-mask semantics.
- Pin checkpoint revision and weight hash and substantiate training exposure. Do not use `virtues-sp32` for held-out HCC evaluation; `virtues-imc14` is only a candidate until provenance is confirmed.
- Demonstrate official preprocessing compatibility, or separately predeclare and label a normalized-domain adaptation experiment.
- Only then run a deterministic outcome-blind pilot with simple baselines and predefined failure thresholds. No biological result is established by the current audit.

## Panel-validator tooling added (2026-10-27)
A fail-closed script, `scripts/validate_hcc_panel.py`, now checks that the panel workbook has the required `Channel`, `MetalTag`, and `Target` columns; validates integer channel IDs, uniqueness, the expected 1–45 channel set, and nonblank marker/tag fields; and exports a channel-sorted CSV plus a JSON report. The HCC pre-algorithm workflow now syntax-checks this script.

Run in the existing Colab runtime after confirming the workbook path:
```bash
python scripts/validate_hcc_panel.py \
  --panel /content/hcc_virtues_audit/dataset/ICICohort_panel.xlsx \
  --sheet Sheet1 --expected-channels 45 \
  --out-csv /content/hcc_virtues_audit/next_gate/channel_map_panel_order.csv \
  --out-json /content/hcc_virtues_audit/next_gate/panel_validation.json
```
This validates the spreadsheet table only. It does **not** prove TIFF plane ordering, nor does it map marker names to the exact protein identifiers/embedding vocabulary required by VirTues. Those remain separate gates.


## Fail-closed ROI crosswalk tooling added (2026-10-27)

Added `scripts/validate_hcc_roi_crosswalk.py` and unit tests in `tests/test_validate_hcc_roi_crosswalk.py`. The validator requires a source-backed CSV with columns `image_stem,patient_id,clinical_roi_id,source_reference,resolution_status`. It rejects unresolved rows, duplicate image stems, duplicate patient/clinical-ROI keys, blank source evidence, missing image stems, and unknown image stems. It never tries to infer the two disputed matches.

Example after creating a CSV from an authoritative source document (do not fill it by guessing):

```bash
python scripts/validate_hcc_roi_crosswalk.py \
  --crosswalk /content/hcc_virtues_audit/next_gate/authoritative_roi_crosswalk.csv \
  --images-dir /content/hcc_virtues_audit/dataset/images \
  --out-json /content/hcc_virtues_audit/next_gate/roi_crosswalk_validation.json
```

Adjust `--images-dir` to the actual image folder in the existing workspace. The script's pass means only that the supplied crosswalk is internally complete and marked resolved with source references; it cannot independently authenticate those source references. No crosswalk has been populated or validated in this environment because the private workbook, clinical table, and image inventory are not mounted here.

The HCC CI workflow was extended to compile this script and run its unit tests. The workflow run for the latest commit must be checked before claiming these new tests passed.


## Reconciled patient-level ROI inventory from available audit files (2026-10-27)

I compared the extracted Supplementary Table 3 patient rows with the 86-row structural TIFF inventory already available in the project. The analysis found 42 clinical patient rows and 42 unique patient prefixes represented among 86 image files. Every image prefix matches a patient row; no clinical patient is absent from the image inventory. The sum of Table 3's `No. of ROIs` entries is 84, compared with 86 image files.

The only count conflicts are:
- `ICI_24`: Table 3 reports 2 ROIs; the structural inventory contains `ICI_24_ROI1`, `ICI_24_ROI2`, and `ICI_24_ROI3`.
- `ICI_39`: Table 3 reports 1 ROI; the inventory contains `ICI_39_ROI1` and `ICI_39_ROI2`.

The publication's description of the ICI cohort reports 86 ROIs, and the filename prefixes explicitly identify their patient. Therefore, the **patient mapping is resolved for inventory purposes**, but the supplementary ROI-count discrepancy remains an audit caveat. The derived crosswalk is stored at `data/derived/hcc_roi_patient_crosswalk_2026-10-27.csv`; the quantitative reconciliation is stored at `data/derived/hcc_roi_count_reconciliation_2026-10-27.json`.

Important analysis constraint: Supplementary Table 3 outcomes are patient-level. Do not interpret per-ROI images as independent patient outcomes; aggregate ROI-level imaging features to the patient level before outcome modelling, and split/evaluate at patient level. The crosswalk's `clinical_roi_id` is the ROI ordinal parsed from the released filename, not a separate source-provided ROI clinical record.

Sources: [Zenodo ICI cohort record](https://zenodo.org/records/10794904) describes the 42-patient dataset, channel-per-stack images, and panel file; [Salié et al., Gut](https://gut.bmj.com/content/74/3/451) provides the published cohort context.
