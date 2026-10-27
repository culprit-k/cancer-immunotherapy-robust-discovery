# Patient-level biology analysis: first executable layer

**Status:** implementation with synthetic tests; no HCC biological result has been computed.

## Rationale

The current HCC imaging cohorts contain repeated regions of interest (ROIs) per patient. Treating ROIs as independent outcomes would inflate the effective sample size. This module reduces ROI features to one patient-level row by a predeclared median/mean rule, validates that each patient has one outcome, and estimates associations with uncertainty.

## What it does

- Aggregates ROI-derived feature values within patients (median by default).
- Reports mean/median differences, rank-biserial effect size, patient-label permutation p-value, stratified patient-bootstrap confidence interval, leave-one-patient-out sign stability and Benjamini-Hochberg q-value.
- Writes private output tables and a manifest describing group counts, exclusions, feature set and random seed.

## What it does not do

- It does not extract biological features from raw TIFFs.
- It does not infer channel/marker ordering, mask semantics, cell identities or clinical endpoints.
- It does not implement a high-dimensional response predictor.
- It does not prove a causal mechanism or clinical utility.
- It cannot establish novelty by ranking the smallest p-value.

Only run it after marker mapping, mask codebook, ROI-to-patient crosswalk, preprocessing and outcome dictionary pass the existing gates. Keep feature tables and outputs private; do not commit patient-level data.

## Run after valid feature extraction

    python scripts/run_hcc_biology_first_analysis.py \
      --input /path/to/private_roi_feature_table.csv \
      --output-dir /path/to/private_hcc_biology_results \
      --patient-col patient_id --outcome-col outcome \
      --features immune_density,activation_score,interface_score \
      --positive PR --negative PD

Feature names and outcome labels above are placeholders, not claims about verified channels or the primary endpoint. Freeze the feature dictionary and endpoint before use. With only five PR patients in the current extraction, a PR contrast is exploratory and has limited precision; SD/PD/PR must not be combined without clinical justification.

## Interpretation rule

A candidate association proceeds only if its effect size is meaningful, uncertainty is compatible with the claim, missingness is acceptable, its sign does not depend on one patient, multiplicity is addressed, biological meaning follows from verified annotations, and independent evidence corroborates it. Even then, it is an association/hypothesis—not causal proof.

## Current status

Unit tests exercise aggregation, outcome-conflict rejection, multiplicity correction and stability output on synthetic data only. They validate software behavior, not the existence of a biological signal in HCC.
