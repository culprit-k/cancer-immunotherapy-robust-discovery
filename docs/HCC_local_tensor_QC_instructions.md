# Local HCC tensor QC

Keep the 882 MB source archive, extracted images/masks, channel map, QC JSON and checkpoint weights in a private local/Colab workspace. Do not upload filled manifests, images, masks, model weights or patient-level rows to this repository.

## Inputs
- `--images`: directory of normalized multichannel TIFF images
- `--cell-masks`: cell-label masks
- `--stromal-masks`: stroma/parenchyma masks
- `--channel-map`: filled copy of `templates/hcc_channel_map_template.csv`
- `--outdir`: private QC output folder
- Optional `--channel-axis`: specify only after checking the source TIFF axes. No channel axis is silently assumed.

## Install and run
```bash
python -m pip install numpy tifffile imageio
python scripts/hcc_tensor_qc.py --images /private/ICI_img_normalized --cell-masks /private/ICI_cellmasks --stromal-masks /private/ICI_stromamasks --channel-map /private/ICICohort_panel_mapped.csv --outdir /private/hcc_qc
```

If the TIFF layout is documented and channel axis verified, rerun with `--channel-axis N` (e.g. `-1` only if the last axis is confirmed to be channels). Outputs `hcc_tensor_qc.json` and `hcc_tensor_qc_summary.csv`.

A PASS is only preliminary tensor QC. It does not prove mask spatial alignment, marker-to-UniProt mapping correctness, exact VirTues preprocessing equivalence, checkpoint exposure, or model validity. Review flagged dimensions manually before model inference.
