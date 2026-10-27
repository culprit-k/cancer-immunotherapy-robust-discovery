# Immediate Colab step: inspect one real HCC image/mask pair

This is the next executable gate before feature extraction. It does not use outcomes, alter the source files, or require re-downloading the dataset/checkpoint.

## 1. Locate extracted ICI files in the existing runtime

In a Colab cell, run:

```bash
find /content -type f \( -iname '*.tif' -o -iname '*.tiff' \) 2>/dev/null | grep -Ei 'ICI.*(img|cellmask)|img_normalized|cellmasks' | head -40
```

Use one known matching image and cell-mask pair from the existing extracted ICI archive. Do not select an image and mask merely because their filenames look similar; confirm their pair from the archive's source manifest. Keep outputs in a private temporary directory.

## 2. Fetch the current branch and install only lightweight dependencies if needed

If the repo clone already exists, preserve it and fetch the branch rather than deleting or recloning:

```bash
cd /content/cancer-immunotherapy-robust-discovery
git fetch origin
git checkout hcc-virtues-audit-next-step
git pull --ff-only origin hcc-virtues-audit-next-step
python -c "import tifffile, PIL, numpy; print('QC dependencies available')"
```

If the repository directory is elsewhere, change only the `cd` path. Do not remove checkpoints, downloaded data, or existing work.

## 3. Generate private QC previews

Replace the two example paths with the verified matching files you found:

```bash
python scripts/preview_hcc_image_mask_qc.py \
  --image "/path/to/one_verified_image.tiff" \
  --cell-mask "/path/to/its_verified_cell_mask.tiff" \
  --output-dir "/content/hcc_private_qc/roi1"
```

Open the generated `plane_montage.png` and `cell_mask_labels.png` in Colab. The JSON manifest reports shape, dtype, finite values, intensity percentiles and label frequencies. The montage labels candidate plane numbers only; it does not prove channel order or biological identity.

## 4. What must be confirmed from source records

- Image TIFF axis order is really channel-first `(C,H,W)`; if not, stop and inspect TIFF metadata before transposing.
- The mask is a per-cell instance-label map, not a class map or a binary mask.
- The documented background label is known; zero is not assumed to mean background without source evidence.
- The image-to-mask pairing and spatial registration are correct.
- Plane order is supported by the acquisition/export manifest, not only by the panel spreadsheet row order.

## 5. Return only non-sensitive diagnostics

Share the printed JSON summary and, if allowed, the two QC previews. Do not upload clinical tables, patient identifiers, raw images, masks or per-cell measurements to GitHub. These diagnostics are enough to decide the next technical gate without exposing patient-level data.

**Stop condition:** if the source documentation does not establish the channel order or mask semantics, do not proceed to biological feature extraction. Ask the dataset authors or find the authoritative export codebook first.
