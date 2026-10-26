# HCC–VirTues audit and decision summary
**Audit date:** 2026-10-26  
**Status:** metadata and clinical-table audit complete; model inference remains blocked.

## Research question
Do VirTues-derived spatial-proteomics representations provide reproducible patient-level information beyond established spatial immune features for understanding outcomes after immune checkpoint inhibitor treatment in hepatocellular carcinoma (HCC)?

This is a testable research question, not a confirmed novelty claim. Salié et al. already described HCC spatial immunotypes and their association with ICI outcomes, so simply rediscovering depleted/compartmentalized/enriched groups is not novel.

## Completed local audit
- Re-parsed the source supplementary PDF using text coordinates and corrected 26 field-level extraction discrepancies: 13 etiology cells and 13 immunotype cells.
- Corrected table: 42 unique patients and 21 columns.
- Missingness: etiology 8; immunotype 2; AFP 5.
- Etiology counts: HCV 15, ALD 12, SLD 4, HBV 3, missing 8.
- Immunotype counts: depleted 17, compartmentalized 13, enriched 10, missing 2.
- Best RECIST response: PR 5, SD 27, PD 10.
- The extracted binary response field has five positive cases and coincides with PR in this table. This is a coding cross-check, not a model result.
- Clinical table reports 84 ROIs while image inventory contains 86 normalized TIFFs, 86 cell masks and 86 stromal masks. Filename triplets are complete for all 86 inventory names. Patient-level discrepancies: ICI_24 (clinical 2, filenames 3) and ICI_39 (clinical 1, filenames 2).
- Preserve AFP source unit as recorded until verified. Do not interpret the source censoring field as a PFS event indicator without clarification.

## Checkpoint/preprocessing decision
The released HCC TIFFs are described as PENGUIN-normalized to [0,1]. VirTues' published input path uses tissue-mask-aware 99th-percentile clipping, shifted log1p, dataset-wise channel standardization and Gaussian smoothing. These representations are not demonstrably equivalent. **Direct official VirTues inference on the released normalized TIFFs is NO-GO.** Do not invert the normalization or invent statistics.

The virtues-imc14 checkpoint remains a candidate only after exact immutable revision, weight checksum and training-exposure documentation are reverified. virtues-sp32 includes the Salié HCC cohort and is not appropriate for a held-out HCC evaluation. Do not use virtues-sp31 for held-out claims until its omitted-cohort list is confirmed. No VirTues inference or outcome model has been run.

## Cohort summary
The local inventory reports 42 patients, 36 biopsies and 6 resectates. The cohort has only five PR/binary-response-positive cases, so complex supervised prediction would be highly overfit-prone. Prioritize low-dimensional prespecified analyses, patient-level validation, effect sizes and uncertainty.

## Required next gates
1. Obtain/verify original-scale intensity values or define a separately named normalized-domain adaptation; never present adaptation as official VirTues preprocessing reproduction.
2. Resolve the 84-versus-86 ROI mapping for ICI_24 and ICI_39 from source records.
3. Confirm checkpoint revision/hash and exposure evidence; preserve licence terms.
4. Establish pixel/channel/mask compatibility and patient-held-out reconstruction QC before outcome analyses.
5. Freeze endpoints, eligible markers, baseline spatial features, split strategy and analysis before accessing the external evaluation cohort.
6. Compare against established spatial immune features; report uncertainty and avoid causal/clinical-utility claims.

## Data governance
This repository is public. Do not commit raw images/masks, model weights, or patient-level clinical rows as part of this audit update. The local corrected CSVs and detailed QC artifacts remain in the private research workspace unless redistribution rights and disclosure are reviewed.

## Key references
- Salié et al., Gut 2025;74:451–466. DOI: 10.1136/gutjnl-2024-332837.
- VirTues, Nature 2026. DOI: 10.1038/s41586-026-10884-y.
- HCC ICI cohort: https://zenodo.org/records/10794904
- VirTues code: https://github.com/bunnelab/virtues
