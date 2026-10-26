# HCC–VirTues artifact inventory (26 October 2026)

This index distinguishes repository-safe artifacts from files retained only in the local research workspace.

## Repository-safe outputs
- `docs/HCC_VirTues_audit_2026-10-26.md` — corrected audit summary and scientific decision.
- `docs/HCC_VirTues_corrected_extraction_summary.csv` — aggregate-only counts; no patient rows.
- `docs/HCC_VirTues_next_step_gate_plan.md` — ordered compatibility and analysis gates.
- `scripts/hcc_preinference_preflight.py` — reproducible inventory and optional TIFF scan utility. It does not run VirTues.

## Local outputs not copied into this public repository
The local workspace contains detailed patient-level clinical CSVs/crosswalks, source supplementary PDF, audit outputs, rendered figures, notebooks, logs and ZIP packages. Patient-level rows and clinical crosswalks are intentionally not committed to a public repository. Raw images/masks, checkpoint weights and any restricted source files must also remain out of GitHub unless rights and governance have been reviewed. The private package remains the local record of those artifacts.

## Key audit facts
- Corrected clinical table: 42 unique patients, 21 columns.
- 26 field-level extraction corrections: 13 etiology and 13 immunotype cells.
- Missing etiology 8, missing immunotype 2, missing AFP 5.
- RECIST best response: PR 5, SD 27, PD 10.
- Clinical ROI count 84 versus 86 image/mask filename triplets.
- Two unresolved patient-level count discrepancies: ICI_24 and ICI_39.
- Direct official VirTues inference on released PENGUIN-normalized [0,1] TIFFs remains NO-GO until compatible input preprocessing is documented.
- No VirTues inference, outcome model, or biological discovery has been established.

## Running the preflight utility
Install optional dependencies if TIFF pixel inspection is desired:
`pip install numpy tifffile`

Example:
`python scripts/hcc_preinference_preflight.py --images /path/to/images --cell-masks /path/to/cell_masks --stromal-masks /path/to/stromal_masks --outdir qc --inspect-tiffs`

Run only against a controlled local copy of the source data. A passing filename inventory is not evidence of biological validity or full model compatibility.