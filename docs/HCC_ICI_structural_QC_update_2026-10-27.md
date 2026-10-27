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
The commit containing this report has two completed successful GitHub Actions runs:
- **HCC pre-algorithm metadata-gate tests** (run 40485611174): compile/QC-script syntax step and metadata-validator unit tests passed.
- **Analysis helper tests** (run 40485611185): synthetic unit tests passed.
These are software/metadata checks only. They do not mean the private dataset was downloaded in this execution environment, that tensor-level QC was independently reproduced here, or that VirTues inference ran.

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
