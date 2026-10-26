# HCC–VirTues input compatibility: decision and first experiment gate (2026-10-26)

## Decision

**HCC inference is not yet scientifically cleared to run.** The prior inventory result (86 TIFF images, 86 cell masks, 86 stromal masks; 86 complete filename triplets) is a filename-level pass only. It does not establish tensor compatibility or valid channel identity. The current assistant execution workspace contains audit tables, notebooks and screenshots, but no HCC TIFF image/mask arrays or model weights, so I cannot truthfully report an HCC reconstruction result from this workspace.

## Compatibility findings

1. **Input scale / preprocessing — unresolved.** The HCC cohort TIFFs have been described in the project audit as PENGUIN-normalized to 0–1. The VirTues paper describes a different pipeline: tissue-mask-aware channel-wise 99th-percentile clipping, shifted log1p, dataset-wise channel standardization using tissue-area statistics, and Gaussian smoothing (kernel 3, sigma 1). Do not apply that sequence to the already-normalized TIFFs blindly, invert the normalization, or invent missing dataset statistics. Obtain the authors' exact preprocessing/source-scale export if available. If it cannot be obtained, a separately named *normalized-domain adaptation* can be tested, but it must not be presented as faithful reproduction of official VirTues preprocessing.

2. **Checkpoint exposure — choose the conservative candidate.** `virtues-sp32` is not suitable for held-out HCC evaluation because the HCC/Salié cohort is included in its training corpus. `virtues-sp31` is not approved until its omitted dataset and exact checkpoint revision are verified. `virtues-imc14` is the candidate to evaluate for this HCC cohort, subject to verifying the exact checkpoint/hash and training-data list. Its published model-weight terms are CC BY-NC 4.0; this is a non-commercial research use context, but record the terms and citation.

3. **Channel semantics — unresolved.** Need the exact ordered marker/channel map and mapping to UniProt IDs for every image. Channel count alone is insufficient because VirTues uses marker embeddings. Missing/ambiguous markers must be resolved explicitly, not guessed.

4. **Image/mask semantics — unresolved.** Need shape, axis order, dtype, finite-value fraction, min/max, cell-mask labels, stromal-mask labels and spatial alignment. Filename triplets do not prove alignment. Two ROI-count discrepancies remain in the clinical crosswalk: ICI_24 and ICI_39.

5. **Pilot design — pre-specified.** Start with one ROI chosen by a deterministic rule (lexicographically first eligible ROI, not outcome-selected). After all gates pass, run a 128×128 crop with official VirTues inference code, using a fixed random seed and a fixed independent masking pattern (mask ratio sampled once per channel within the official 0.6–1.0 range). Compare predictions only on masked pixels/channels against a transparent baseline that predicts each held-out channel's tissue-area mean. Report per-channel and pooled masked-pixel MSE, MAE and the number of scored pixels. Repeat across a small, predeclared set of ROIs only after the single-ROI smoke test passes. Do not inspect patient outcomes to select ROIs or tune preprocessing.

6. **Interpretation.** This is a technical reconstruction smoke test, not an outcome prediction, biomarker validation, or clinical result. The 42-patient cohort must not be used to tune the model if it is later designated as external evaluation. Any result from normalized-domain adaptation must be labeled as such.

## Exact unblock artifacts

The next run requires a private/local folder (do not commit patient-level data or weights publicly) containing:
- HCC normalized TIFFs and both masks, or a source-scale export;
- a machine-readable ordered channel/marker-to-UniProt map;
- image/mask QC JSON from `scripts/hcc_preinference_preflight.py --inspect-tiffs`;
- the exact `virtues-imc14` model revision and SHA-256 of the downloaded weight file;
- the dataset-specific standardization statistics and tissue mask, if the intended run claims official preprocessing reproduction;
- a note resolving ICI_24/ICI_39 ROI counts or identifying the discrepancy as unresolved.

## Current status

- Filename triplet inventory: previously reported pass (86/86), pending re-run against the actual arrays in the execution environment.
- Full image tensor QC: not verified in this workspace.
- Channel/marker mapping: not verified.
- Preprocessing compatibility: **fail / unresolved for faithful reproduction**.
- Eligible checkpoint: **candidate only; not yet pinned and verified**.
- HCC reconstruction metrics: **not run**. No model performance claim is supported yet.
