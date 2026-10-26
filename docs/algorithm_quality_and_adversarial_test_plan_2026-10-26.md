# Algorithm quality and adversarial test plan
**Status:** required test plan for future implementation; no full AI algorithm is implemented by this document.

## Required unit / integration tests
- Manifest schema: missing required fields, duplicate ROI IDs, duplicate patient/ROI pair, path traversal, invalid hashes and unknown preprocessing modes must fail closed.
- Image/mask integrity: mismatched shapes, unknown axes, NaN/Inf, empty tissue masks, unknown label IDs, missing channels, duplicate markers and wrong mask alignment must be detected.
- Channel semantics: reordered channels must change the manifest fingerprint; the pipeline must never silently infer channel order from filenames.
- Checkpoint identity: missing revision/hash/licence/training inventory must block eligible-checkpoint status; hash mismatch must fail.
- Leakage: patient IDs must not occur across training, calibration and evaluation partitions; all ROIs from a patient remain together.
- Outcome leakage: changing outcome labels must not alter preprocessing, ROI selection, reconstruction-mask seed or feature extraction.
- Reproducibility: identical configuration, data hashes, code revision and seed should reproduce the same result within a declared numerical tolerance.
- Negative controls: shuffled outcomes should not retain convincing predictive performance beyond chance; synthetic data with no signal should not generate stable high-confidence targets.
- Robustness: test marker dropout, marker reordering, ROI omission, mask perturbation, plausible normalization shift, rare markers and domain shift.
- Ablation: remove each claimed new component and verify its incremental contribution; if removing a component does not change preregistered behavior, do not claim that component as the innovation.
- Fail-safe outputs: unsupported markers, low evidence, out-of-domain input or poor calibration should trigger explicit uncertainty/abstention rather than forced rankings.

## Synthetic benchmark before clinical outcome use
Create synthetic tissues where the ground truth is controllable: (1) no response-related spatial signal; (2) signal only in cell abundance; (3) signal only in neighbourhood/compartment relationships; (4) signal confounded by cohort/acquisition; (5) missing-not-at-random marker panel; (6) duplicated patient ROIs; (7) one known interaction perturbation; and (8) no true causal effect despite a strong observational association.

Measure whether the algorithm recovers only the planted signal, resists confounding, returns uncertainty when signal is absent, and avoids interpreting correlation as intervention effects.

## Statistical robustness tests
- Patient-level bootstrap / grouped cross-validation only where event counts permit.
- Repeat random-dependent steps under recorded seeds; summarize ranking stability and performance spread.
- Evaluate calibration and uncertainty, not only discrimination.
- Report failures, empty regions, missing markers and exclusions in the denominator.
- Any external cohort used for evaluation must remain unavailable to fitting, feature selection and hyperparameter tuning.

## Complexity guardrail
No component is accepted merely because it makes the model larger. Each must have (a) a stated failure mode in a simpler baseline, (b) a formal role in the objective, (c) a test, (d) an ablation, and (e) a measurable benefit or justified safety benefit. Prefer the smallest model that passes the scientific objective.
