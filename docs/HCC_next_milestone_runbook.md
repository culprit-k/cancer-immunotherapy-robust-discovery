# Next milestone runbook (private local/Colab)

## Why the assistant cannot finish the tensor QC directly here
The HCC ICI archive is 882 MB. The public Zenodo record identifies the archive and provides its MD5, but the current assistant execution workspace does not contain the image/mask arrays. The archive download endpoint also rejects oversized downloads in the browsing layer. Do not interpret prior filename counts as tensor QC.

## Run the bootstrap in Colab or a private local environment
1. Open the project branch and copy `scripts/bootstrap_hcc_public_data.sh` into the private runtime (or run its equivalent commands below).
2. Download and verify the archive:
   ```bash
   bash scripts/bootstrap_hcc_public_data.sh "$HOME/hcc_virtues_private"
   ```
   Expected MD5 from the official Zenodo record: `d0b3242740b70c1355f67bc7bd176c6a`.
3. Locate the extracted image, cell-mask, stromal-mask directories and `ICICohort_panel.csv`. Do not rename files or silently alter axes.
4. Create a local copy of `templates/hcc_channel_map_template.csv`. Populate the channel order exactly as the TIFF array order and the panel file. Leave uncertain protein identifiers explicitly unresolved; do not guess. The panel annotation is reported by Zenodo to contain metal tag and marker.
5. Run the local tensor QC:
   ```bash
   python -m pip install numpy tifffile imageio
   python scripts/hcc_tensor_qc.py --images PATH_TO_IMAGES --cell-masks PATH_TO_CELL_MASKS --stromal-masks PATH_TO_STROMAL_MASKS --channel-map PATH_TO_FILLED_CHANNEL_MAP --outdir "$HOME/hcc_virtues_private/qc"
   ```
6. Inspect representative TIFF axes and mask labels, then rerun with `--channel-axis N` only when the correct channel axis is established from metadata/code. A shape or count match alone does not prove pixelwise alignment.
7. Resolve ICI_24 and ICI_39 against the clinical ROI table and actual filenames. If there is no authoritative crosswalk, quarantine those ROI records; do not force a match.
8. Keep all source images, masks, filled manifests and weights private. Share only the aggregate QC JSON/CSV after checking they contain no paths or patient-level information. The report may include local file paths; sanitize those before sharing.

## Gates before reconstruction
- Every ROI has a complete triplet; missing or discrepant ROIs are quarantined.
- Channel count and order are verified against the panel and model marker embedding requirements.
- Image and mask axes/dimensions, integer mask labels, finite intensity values, and image–mask alignment are verified.
- Checkpoint hash, code/config revision, licence and training exposure are frozen.
- Official VirTues preprocessing is reproduced only if the required tissue masks and dataset-level statistics are available. Otherwise call it normalized-domain adaptation.
- Only then run the predeclared masked-pixel reconstruction pilot versus the tissue-area channel-mean baseline.
