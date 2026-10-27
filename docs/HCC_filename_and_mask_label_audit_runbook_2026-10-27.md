# HCC ICI filename crosswalk and mask-label audit — next gate

## Purpose
The initial Colab run established that 86 image files, 86 cell masks and 86 stromal masks are readable and that their spatial shapes match. It did not settle the 86-file versus 84-clinical-ROI discrepancy, establish authoritative image-to-mask pairing, or decode mask labels. This script is the next *local/private* audit step.

## Run in the same private Colab runtime
After the existing notebook has downloaded and extracted the archive, run:

```python
import sys
from pathlib import Path
repo = Path("/content/cancer-immunotherapy-robust-discovery")
root = Path("/content/hcc_virtues_private/extracted")
out = Path("/content/hcc_virtues_private/filename_mask_audit")
!{sys.executable} {repo / "scripts/hcc_filename_and_mask_label_audit.py"} --root {root} --outdir {out} --mask-samples 12
```

If the archive was extracted into a different directory, change `root` to the actual extraction directory. The script reads local files and writes three outputs locally:
- `private_filename_inventory.csv`
- `private_roi_filename_summary.csv`
- `private_mask_label_diagnostics.json`

These outputs intentionally contain local filenames/paths and can expose patient/ROI information. **Do not commit or upload them to GitHub.** Share only manually reviewed, de-identified aggregate findings.

## How to interpret the output
1. Use the filename inventory to compare image, cell-mask and stromal-mask names. It reports ROI-like tokens but deliberately labels all matches as review-required.
2. For ICI_24 and ICI_39, do not select a filename based on ordering, file size, or the token alone. Resolve the extra file(s) against the paper/supplement, source metadata, or a documented author-provided crosswalk. If no authoritative mapping is available, quarantine those ROI records.
3. Inspect mask unique values and counts. This only reveals encoding candidates. It does not prove whether a value means cell, stroma, parenchyma, background, or another class. Verify meanings from source metadata/code before any mask-dependent preprocessing.
4. Compare the reported paths to the existing QC output. Do not assume the filename-token heuristic is correct if naming conventions differ.

## Hard stop conditions
- Any unresolved ROI identity or image-mask pairing: no inference for that ROI.
- Any uncertain marker/channel identity or ordering: no marker-conditioned VirTues inference.
- Any unverified mask semantics: do not use that mask as a tissue mask for official preprocessing.
- Any inability to reproduce the official preprocessing: report a separate normalized-domain adaptation, not an exact VirTues reproduction.
- Do not load the candidate checkpoint or claim reconstruction performance until the checkpoint/code revision, licensing, training-cohort exposure and required preprocessing are documented.

## What this step does not do
It does not inspect the clinical outcome table, resolve the crosswalk automatically, alter the data, run VirTues, train a model, or produce biological/clinical conclusions. The next decision depends on the local audit outputs and an authoritative source for disputed mappings.
