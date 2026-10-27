# HCC ICI archive structural QC — verified run (2026-10-27)

## Result

**Structural preflight: PASS_STRUCTURAL_ONLY.** The public Zenodo archive was downloaded and checked inside GitHub Actions. The analysis read every listed image, cell-mask, and stromal-mask TIFF in the archive. This was outcome-blind structural QC and did not call VirTues or read clinical outcomes.

- Workflow run: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504894939
- Aggregate-only report artifact: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504894939/artifacts/12734062500
- Data record: https://doi.org/10.5281/zenodo.10794904
- Archive size: 882,022,729 bytes
- Expected and observed MD5: `d0b3242740b70c1355f67bc7bd176c6a` (match)
- Run's research commit: `1d98c9d804e465e4511d3624131d584742ce7147`

## Verified structural results

| Check | Result |
|---|---:|
| ZIP members | 259 |
| Image stacks | 86 |
| Cell-mask TIFFs | 86 |
| Stromal-mask TIFFs | 86 |
| Complete, uniquely paired triplets | 86 / 86 |
| Duplicate canonical image/mask keys | 0 |
| Missing or orphan masks | 0 |
| Image arrays | 86 / 86 readable, 3-D, `float32` |
| Image channel count | 45 planes in every stack |
| Finite images | 86 / 86 |
| Images with values all in [0,1] | 86 / 86 |
| Image read errors | 0 |
| Cell masks | 86 / 86, 2-D integer arrays |
| Stromal masks | 86 / 86, 2-D integer arrays |
| Cell-mask spatial shape matches image | 86 / 86 |
| Stromal-mask spatial shape matches image | 86 / 86 |
| Mask read errors or non-2-D arrays | 0 |
| Panel entries | 45, channels 1–45, unique and complete |
| Unique spatial image shape count | 64 |

The image stacks vary in spatial size across 64 shapes; downstream code must not assume all ROIs share a single height and width. The observed union of cell-mask labels spans 0 through 413. The observed stromal-mask label union is `{3,4,5,6,7,8,9}`, and the median zero-pixel fraction is 0. This describes the numerical encoding only; no biological meaning is assigned to the numeric labels.

## ROI count reconciliation still blocked

The archive filenames contain:
- ICI_24: 3 image ROIs, versus 2 ROIs reported in Supplementary Table 3.
- ICI_39: 2 image ROIs, versus 1 ROI reported in Supplementary Table 3.

The supplementary table provides counts/clinical metadata but does not name which archive filename is extra. **No ROI is auto-deleted or reassigned.** Keep these two patients out of outcome-linked analyses until an authoritative image-level crosswalk is available.

## What this does and does not clear

It clears the basic archive-integrity, stack readability, complete-pairing, channel-count, finite-range and image/mask shape gates for the ICI archive. It does **not** prove:
- that stack plane order semantically matches panel row order;
- that each marker target is correctly linked to an authoritative UniProt accession and the exact ESM embedding used by VirTues;
- what labels 3–9 represent in the stromal mask or what region each code denotes;
- that PENGUIN-normalized [0,1] inputs match the VirTues training input representation;
- that ROI filenames map without ambiguity to the clinical table;
- any model reconstruction accuracy, counterfactual target stability, immune-evasion mechanism, or response prediction.

## Immediate next steps

1. Export the authoritative `ICICohort_panel.xlsx` rows as a public metadata-only table, then build a source-backed channel → marker target → UniProt accession → ESM embedding map. Do not guess complex/ambiguous targets.
2. Resolve whether `ICI_24` and `ICI_39` excess filenames reflect additional regions, duplicate exports, or a separate sampling discrepancy using an authoritative source.
3. Obtain or document the stromal-mask codebook / processing outputs before translating label IDs to biology.
4. Retain the official VirTues synthetic preflight result, but keep the no-go on HCC model inference until channel identity and preprocessing compatibility are demonstrated.

**Important:** The archive audit was successfully completed under the earlier script revision. A newer workflow exports the marker panel rows separately for convenient mapping, but its result must be inspected separately before claiming the public panel mapping artifact was generated.
