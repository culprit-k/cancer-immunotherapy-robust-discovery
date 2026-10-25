# Decision memo: next compatible cohort/model path

**Date:** 25 October 2026  
**Decision:** Preserve the scientific question; reject direct inference on the HCC normalized TIFFs using VirTues-IMC14. The preprocessing mismatch has been resolved as a definitive NO-GO for the released images. The pinned IMC-only checkpoint is supported as outside direct Salié-study pretraining by the paper's core-versus-extended corpus inventory.

## Why this decision is necessary

The 54-patient Salié HCC archive passed checksum and structural panel QC. The completed audit recorded MD5 `a842fa253ac2f0eda3cbf4d41e1b0ec1`, SHA-256 `8d09d946659164bb2275468ca4ad3239819b2036af83e63ab7b586ddbfc47f72`, exact advertised size, 325 archive entries, 42 panel rows, and `structural_qc_pass=true`; see [audit run 40211055869](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40211055869). The public images are PENGUIN-normalized to 0–1 per channel/ROI. There are no original MCD acquisitions or matching VirTues per-tissue quantile/mean/standard-deviation tables in this archive. Applying VirTues' clip/log/blur/standardization pipeline to these normalized values would not recreate the training representation; inversion is not justified.

The 42-patient HCC ICI cohort does not solve the representation mismatch: its public files are also normalized TIFFs. The completed metadata-only audit retrieved the Zenodo API `cc-by-4.0` field for both records but did not download the ICI image archive. Its distinct patient cohort can remain an external evaluation candidate only after an appropriate image input route and outcome/label definition are locked.

## Preferred path A — resolve original-scale HCC inputs

Use the draft request in `docs/data_clarification_request_salie_hcc.md` to ask the authors/data curator whether the original compensated MCD acquisitions, normalization recipe, channel order and per-image/per-channel statistics can be made available under appropriate terms.

**Go only if** original compensated intensities (or an explicitly validated, model-compatible representation) and the required channel/tissue metadata are available, the official VirTues data contract can be implemented without guessed values, and a one-image reconstruction smoke test succeeds. If only PENGUIN-normalized TIFFs can be shared, do not try to invert them or treat recomputed statistics as equivalent.

## Preferred path B — use a compatible, documented harmonized spatial-proteomics cohort

If original HCC inputs are unavailable, use a dataset already distributed in the official VirTues/spora harmonized format, with the marker embeddings and tissue masks required by the loader. Then:

1. Select a cohort with a defensible immune endpoint and sufficient patient-level sample size.
2. Verify the dataset's licence and patient/ROI identifiers before downloading or processing.
3. Determine whether an exact checkpoint variant excluding that cohort is actually released. Pin both model revision and weights SHA-256. Do not call the evaluation zero-shot if this cannot be demonstrated.
4. Reproduce the official reconstruction demo first, then mask one measured marker at a time and compare the reconstructed values with the truly observed held-out marker.
5. Use patient-level splits, never image/crop-level splits that can leak ROIs from the same patient across partitions.
6. Only after reconstruction checks pass, run the pre-specified downstream recommendation-fidelity analysis. The endpoint must be supported by existing cell annotations or a validated label rule.

Official starting points: [VirTues repository and data-format instructions](https://github.com/bunnelab/virtues), [VirTues paper and dataset/training description](https://www.nature.com/articles/s41586-026-10884-y). The existence of a harmonized corpus does not itself establish that a compatible held-out checkpoint is available for any particular cohort; verify exact files, reuse rights, patient/ROI identifiers, immune labels, and training exposure before selecting one.

## Do not do these things

- Do not apply VirTues clipping/log1p/standardization to already-normalized HCC images without proving that this is the expected representation.
- Do not infer raw intensity from normalized images.
- Do not claim the HCC ICI cohort is external validation merely because it has a separate accession.
- Do not infer CD8 cell labels from cell/stroma masks alone.
- Do not call model-predicted changes treatment effects or clinical recommendations.
- Do not claim novelty, independent validation, or publication readiness before a targeted prior-art review and complete experiment.

## Current status

- **Completed:** HCC discovery archive MD5, panel extraction, metadata-only audit artifact; checkpoint weight identity pin; analysis-metric unit tests.
- **Blocked:** HCC/VirTues preprocessing compatibility; canonical marker-embedding map; defensible cell-level endpoint; counterfactual intervention/baseline compatibility. An accession-to-training-run certificate was not located, but the pinned core-14 model is supported as outside direct Salié-study exposure by the published cohort inventory.
- **Next decision:** The scientific block is now explicit: use the unsent author-request draft to obtain original-scale HCC inputs and cell labels, or pivot to a spora-compatible cohort. The pinned `virtues-imc14` checkpoint (`43fd00fce052c46f9e0cc1a87f42806620632319`, SHA-256 `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`) is the defensible public model variant for HCC exposure because Salié et al. is ref. 95 among seven extra IMC cohorts added to the extended corpus, not the core 14. This is publication-level corpus evidence; no separate accession-to-training-run certificate was found.
