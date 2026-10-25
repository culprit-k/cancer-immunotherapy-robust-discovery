# Decision memo: next compatible cohort/model path

**Date:** 25 October 2026  
**Decision:** Preserve the scientific question; reject the current HCC-normalized-TIFF + VirTues-IMC14 execution pairing until its input contract is resolved.

## Why this decision is necessary

The 54-patient Salié HCC archive passed checksum validation and its 42-channel panel was parsed. However, the released images are already preprocessed/normalized and the archive inventory does not include original MCD acquisitions or the per-tissue quantile/mean/standard-deviation tables described in the VirTues preprocessing contract. Applying the VirTues pipeline again or attempting to invert the released images would be scientifically unjustified.

The 42-patient HCC ICI cohort is not a shortcut around this issue: its published files are also normalized images, and it shares the same general source cohort/program. It is not independent validation until both model exposure and data processing are resolved.

## Preferred path A — resolve original-scale HCC inputs

Use the draft request in `docs/data_clarification_request_salie_hcc.md` to ask the authors/data curator whether the original compensated MCD acquisitions, normalization recipe, channel order and per-image/per-channel statistics can be made available under appropriate terms.

**Go only if** the input scale and all required metadata can be documented, the official VirTues data contract can be implemented without guessed values, and a one-image reconstruction smoke test succeeds. If only normalized TIFFs can be shared, do not try to invert them.

## Preferred path B — use a compatible, documented harmonized spatial-proteomics cohort

If original HCC inputs are unavailable, use a dataset already distributed in the official VirTues/spora harmonized format, with the marker embeddings and tissue masks required by the loader. Then:

1. Select a cohort with a defensible immune endpoint and sufficient patient-level sample size.
2. Verify the dataset's licence and patient/ROI identifiers before downloading or processing.
3. Determine whether an exact checkpoint variant excluding that cohort is actually released. Pin both model revision and weights SHA-256. Do not call the evaluation zero-shot if this cannot be demonstrated.
4. Reproduce the official reconstruction demo first, then mask one measured marker at a time and compare the reconstructed values with the truly observed held-out marker.
5. Use patient-level splits, never image/crop-level splits that can leak ROIs from the same patient across partitions.
6. Only after reconstruction checks pass, run the pre-specified downstream recommendation-fidelity analysis. The endpoint must be supported by existing cell annotations or a validated label rule.

Official starting points: [VirTues repository and data-format instructions](https://github.com/bunnelab/virtues), [VirTues paper and dataset/training description](https://www.nature.com/articles/s41586-026-10884-y). The existence of a harmonized corpus does not itself establish that a compatible held-out checkpoint is available for any particular cohort; verify exact files and exposure before selecting one.

## Do not do these things

- Do not apply VirTues clipping/log1p/standardization to already-normalized HCC images without proving that this is the expected representation.
- Do not infer raw intensity from normalized images.
- Do not claim the HCC ICI cohort is external validation merely because it has a separate accession.
- Do not infer CD8 cell labels from cell/stroma masks alone.
- Do not call model-predicted changes treatment effects or clinical recommendations.
- Do not claim novelty, independent validation, or publication readiness before a targeted prior-art review and complete experiment.

## Current status

- **Completed:** HCC discovery archive MD5, panel extraction, metadata-only audit artifact; checkpoint weight identity pin; analysis-metric unit tests.
- **Blocked:** HCC/VirTues preprocessing compatibility; canonical marker-embedding map; exact checkpoint exposure at accession level; defensible cell-level endpoint; counterfactual intervention/baseline compatibility.
- **Next decision:** Wait for author clarification, or nominate a specific harmonized cohort and verify its exact leave-one-cohort-out checkpoint before committing the primary analysis.
