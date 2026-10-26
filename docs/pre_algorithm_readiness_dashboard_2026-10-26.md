# Pre-algorithm readiness dashboard
**As of:** 2026-10-26. **Purpose:** separate completed preparation from blocked empirical work.

## What is ready
- Corrected and source-checked clinical-table extraction with aggregate audit summaries.
- Research question and boundary against rediscovering known HCC immunotypes.
- Targeted novelty assessment updated for VirTues and recent HCC spatial niche / multi-omics / biomarker work.
- Data contract and private/public storage boundary.
- Draft patient-level analysis plan, leakage rules, baseline ladder and stop criteria.
- Candidate screen for three possible mathematical directions; no architecture falsely declared novel.
- Fail-closed pilot gate plus ROI manifest validator.
- Six synthetic unit tests for manifest validation pass locally; CI is configured to rerun them on this branch/PR.

## What is not ready
- Raw TIFF/mask arrays are not present in this execution workspace.
- The file inventory does not prove actual tensor dimensions, axes, value ranges or image–mask spatial alignment.
- Marker ordering and exact marker-to-UniProt mapping are not yet verified.
- Clinical table reports 84 ROIs while the source inventory has 86 triplets; ICI_24 and ICI_39 remain unresolved.
- PENGUIN-normalized [0,1] input is not proven equivalent to the VirTues preprocessing route.
- Exact eligible checkpoint revision, weight checksum, licence and HCC training exposure require final confirmation.
- Endpoint semantics (particularly the censoring field) are not sufficient for survival modelling without source-level verification.
- No reconstruction, representation, outcome-model or target-discovery experiment has run.

## Decision
**Continue preparation; do not start the full algorithm or report biological claims yet.** The available material supports a disciplined research plan, not a validated model. The next empirical gate is a private/local input bundle containing the full images and masks, channel map, tensor-QC JSON, resolution/quarantine note for the two ROI discrepancies, and an immutable checkpoint record. Run the metadata tests first, then the separate tensor/image preflight; a metadata PASS is not a model-compatibility PASS.

## Research links
- HCC source cohort: https://zenodo.org/records/10794904
- HCC discovery cohort: https://zenodo.org/records/10793609
- VirTues code: https://github.com/bunnelab/virtues
- HCC source paper: https://doi.org/10.1136/gutjnl-2024-332837
- VirTues paper: https://doi.org/10.1038/s41586-026-10884-y
