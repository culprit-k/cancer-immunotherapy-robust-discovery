# Outcome-blind spatial cell-marker feature layer

**Status:** implementation and synthetic tests only. No HCC image was processed by this code in this commit.

## Why this is a biological analysis layer

The proposed hypothesis is that the spatial association between a cytotoxic-associated marker state and a neighbouring myeloid-associated marker state may contain information beyond total marker abundance. This is not a new biological finding and is not yet a demonstrated literature gap. It must be compared with established HCC spatial immunotypes, published T-cell/myeloid neighbourhood results, and recent stromal FAP-alpha findings before claiming novelty.

## Feature construction

Given a source-verified image stack with shape `(channels, height, width)`, a verified cell-instance label mask and a row-by-row verified channel map, the module:

1. Computes the mean value for each requested marker within every segmented object.
2. Converts each requested marker to within-ROI percentile ranks to reduce sensitivity to channel-scale differences.
3. Calculates a continuous focal marker-state score and a mean score among the `k` nearest cell centroids.
4. Computes Spearman association between the scores and compares it to a spatial-shuffle reference formed by randomly assigning neighbouring-state scores to fixed cell coordinates.
5. Writes an ROI-level statistic. The shuffle p-value is only a spatial diagnostic, not patient-level inferential evidence.

No cell type is inferred by this module. Marker names such as CD8a, GranzymeB, CD163 or CD68 do not by themselves prove a particular cell identity, and the user must supply the marker sets only after confirming image-plane mapping and annotation semantics.

## Required gates

- Channel map has zero-based image-plane indices and unique markers; every used row is explicitly marked verified and has source evidence.
- Cell mask semantics and background label are verified from source documentation and overlays.
- Intensities and coordinates are checked for finite values and matching dimensions.
- For the HCC ICI cohort, the ICI_24 / ICI_39 ROI discrepancy is resolved or affected rows are quarantined using an outcome-independent rule.
- Keep patient IDs, derived features and all analysis outputs private.

## Analysis plan after extraction

The ROI scores must be aggregated to one score per patient under a frozen rule. Outcome association should use the patient-level module in `analysis/patient_level_discovery.py`, with effect size, confidence interval, permutation analysis, multiplicity correction and leave-one-patient-out influence checks. Compare against overall marker abundance, single-marker features, simple additive models and published immunotype. Use independent cohort or orthogonal evidence before a strong biological claim.

The current HCC ICI cohort has only five partial-response patients in the derived clinical table, so no high-dimensional PR classifier should be fitted. This score must not be selected for best performance on the ICI cohort and then described as independently validated.

## Reproducibility

The unit tests use synthetic arrays only. CI passing will mean code behavior was tested; it will not mean a biological effect was observed. Do not commit raw images, masks, patient tables or generated per-cell outputs.
