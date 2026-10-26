#!/usr/bin/env bash
# Download and verify the public HCC ICI cohort into a PRIVATE local/Colab folder.
# This script never uploads data to GitHub. Review Zenodo/article terms before use.
set -euo pipefail
ROOT="${1:-$HOME/hcc_virtues_private}"
ZIP="$ROOT/HCC_ICICohort.zip"
mkdir -p "$ROOT"
URL="https://zenodo.org/records/10794904/files/HCC_ICICohort.zip?download=1"
EXPECTED_MD5="d0b3242740b70c1355f67bc7bd176c6a"
if [[ ! -f "$ZIP" ]]; then
  echo "Downloading 882 MB public HCC ICI cohort to $ZIP"
  curl -L --fail --retry 3 "$URL" -o "$ZIP"
fi
ACTUAL_MD5="$(md5sum "$ZIP" | awk '{print $1}')"
if [[ "$ACTUAL_MD5" != "$EXPECTED_MD5" ]]; then
  echo "ERROR: MD5 mismatch. expected=$EXPECTED_MD5 actual=$ACTUAL_MD5" >&2
  exit 2
fi
echo "Archive MD5 verified: $ACTUAL_MD5"
mkdir -p "$ROOT/extracted"
if [[ ! -f "$ROOT/.extracted_ok" ]]; then
  unzip -o "$ZIP" -d "$ROOT/extracted"
  touch "$ROOT/.extracted_ok"
fi
echo
echo "Extraction inventory (first 100 paths):"
find "$ROOT/extracted" -maxdepth 4 -type f | sort | head -100
echo
echo "Find image/mask/panel folders, then run hcc_tensor_qc.py with their actual paths."
echo "Do not infer the channel axis from this script; inspect TIFF axes and document the chosen axis."
echo "PRIVATE DATA ROOT: $ROOT"
