# Novelty assessment

**Current status: UNVERIFIED — do not claim novelty yet.**

## Proposed contribution to assess

A leakage-safe evaluation framework for the stability of complete computationally predicted cancer immunotherapy target combinations under patient-level resampling and prespecified modelling changes, with separate reporting of external generalization and uncertainty.

## What would not be novel on its own

- Predicting immunotherapy response.
- Applying AI to cancer datasets.
- Generating counterfactual perturbations.
- Predicting increased T-cell infiltration.
- Testing performance on a held-out cohort.
- Measuring feature stability in general.
- Reporting a generic robustness score without showing why it is needed or what it adds.

Morpheus and COMPASS already cover important adjacent areas, so these components must be compared directly with the literature.

## Evidence required to support a contribution

1. A targeted, documented literature search including related terminology and methods.
2. A comparison table mapping existing methods to the proposed capabilities.
3. A clear distinction between individual-target stability and whole-combination stability, if that distinction is genuinely under-addressed.
4. A reproducible baseline and suitable benchmark.
5. Prespecified metrics and evaluation splits.
6. An empirical result showing what the method adds beyond the baseline, including negative findings.
7. A limitations statement that distinguishes computational robustness from biological and clinical validity.

## Proposed decision rules

- **Proceed:** A specific gap remains after the audit, data support a fair test, and a measurable contribution can be evaluated.
- **Refine:** The general problem matters, but the proposed metric or algorithm overlaps existing work.
- **Stop or pivot:** The gap is already addressed, the data cannot support the claimed evaluation, or the baseline cannot be reproduced.

## Intellectual-property caution

This repository is public. Public disclosure may affect patent options depending on jurisdiction and circumstances. If a potentially patentable invention emerges, seek appropriate institutional or patent-professional advice before publicly disclosing enabling technical details. No claim about patentability is made here.
