# Novelty assessment

**Current status: UNVERIFIED — do not claim novelty yet.**

## Proposed contribution to assess

A leakage-safe evaluation framework for the joint reliability of complete computationally predicted cancer immunotherapy target combinations under patient-level resampling and prespecified modelling changes, with separate reporting of combination stability, uncertainty, and independent evaluation.

## Important prior-work overlap

- **Morpheus (2025):** counterfactual perturbation discovery from spatial tumour-protein data and selected experimental validation.
- **COMPASS (2026):** immunotherapy-response prediction and cross-cohort generalization.
- **Jiang et al. (IJCAI 2024):** survey of robust counterfactual explanations across several robustness definitions.
- **Takefuji (Cancer Letters, 2026 issue):** feature-attribution/selection stability in oncology.

These papers make a generic robustness framework or generic feature-stability score insufficient as a novelty claim.

## What would not be novel on its own

- Predicting immunotherapy response.
- Applying AI to cancer datasets.
- Generating counterfactual perturbations.
- Predicting increased T-cell infiltration.
- Testing performance on a held-out cohort.
- Measuring feature stability in general.
- Applying generic counterfactual robustness methods without a distinct scientific or methodological advance.
- Reporting a generic robustness score without showing what it adds.

## Evidence required to support a contribution

1. A targeted, documented literature search including terminology for robust counterfactuals, intervention-set stability, stability selection, and spatial immuno-oncology.
2. A comparison table mapping existing methods to the proposed capabilities.
3. Evidence that the whole-combination reliability question is not already adequately addressed.
4. A reproducible baseline and suitable benchmark.
5. Prespecified metrics and leakage-safe patient-level evaluation.
6. Empirical evidence of added value beyond baselines, including negative findings.
7. A clear distinction between computational robustness, causal validity, biological validation, and clinical utility.

## Decision rules

- **Proceed:** A specific gap remains after the audit, data support a fair test, and a measurable contribution can be evaluated.
- **Refine:** The problem matters but the proposed metric or algorithm overlaps existing work.
- **Pivot:** Existing methods already address the core contribution, or data cannot support the proposed claim.

## Intellectual-property caution

This repository is public. Public disclosure may affect patent options depending on jurisdiction and circumstances. If a potentially patentable invention emerges, seek appropriate institutional or patent-professional advice before publicly disclosing enabling technical details. No claim about patentability is made here.
