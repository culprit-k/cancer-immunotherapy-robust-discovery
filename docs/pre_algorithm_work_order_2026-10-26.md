# Work order before designing the full algorithm
**Date:** 2026-10-26. This is the sequence to complete before committing to the high-complexity AI architecture.

## Gate A — Research definition
- [x] State a focused HCC–ICI question.
- [x] Audit prior extraction and document patient/ROI discrepancies.
- [x] Record obvious overlap with HCC immunotype and VirTues literature.
- [ ] Complete a targeted, reproducible literature search and comparison matrix.
- [ ] Read VirTues supplement, code and checkpoint training-data manifests in full.
- [ ] Decide whether the primary claim is technical transfer, incremental prediction, or target prioritization. Do not merge all three into one endpoint.

## Gate B — Data and model eligibility
- [x] Write a fail-closed gate scaffold.
- [ ] Deliver actual image/mask arrays or source archive to a private execution workspace.
- [ ] Produce full QC JSON and validate all 86 triplets at tensor level.
- [ ] Resolve ICI_24 / ICI_39 ROI crosswalk.
- [ ] Verify exact ordered marker map and mapping evidence.
- [ ] Obtain original-scale input or explicitly preregister the normalized-domain adaptation.
- [ ] Pin checkpoint revision, weight hash, licence and dataset exposure evidence.
- [ ] Decide whether the 42-patient ICI cohort is development, feasibility-only, or held-out external evaluation.

## Gate C — Protocol and benchmark
- [x] Draft a patient-level split and leakage-control framework.
- [x] Define simple reconstruction comparator and downstream comparator ladder.
- [x] Define negative controls, ablations and stop conditions.
- [ ] Freeze the exact primary metric and failure threshold using method-independent rationale.
- [ ] Prepare synthetic spatial datasets and unit tests.
- [ ] Freeze endpoint and source variable definitions after source verification.
- [ ] Register/version the protocol before outcome-guided analysis where feasible.

## Gate D — Mathematical novelty selection
Do not freeze a large architecture until Gates A–C are sufficiently resolved. Then:
1. Write at least three mathematically distinct candidate designs in shared notation.
2. For each design, state the unique contribution, assumptions, objective, computational cost, failure modes and falsifiable tests.
3. Benchmark each candidate on synthetic data first and then eligible development data.
4. Select the smallest design that passes robustness tests and adds value over the strongest baseline.
5. Only then implement the full algorithm and run an independent evaluation.

## Current hard blockers
- The current local assistant workspace did not contain image/mask arrays or verified checkpoint weights at last audit.
- Preprocessing compatibility is unresolved for faithful VirTues reproduction.
- Marker/channel mapping and the two ROI discrepancies remain unresolved.
- Checkpoint exposure needs a final, immutable verification.
- The outcome cohort is small (42 patients; five PR/binary-positive cases in the corrected extraction) for large supervised outcome modelling.
- No VirTues inference, outcome model, or biological discovery has been reported.

## Completion criterion for pre-algorithm preparation
This phase is complete only when the literature comparison matrix, data provenance/QC bundle, valid checkpoint record, preregistered evaluation plan and synthetic test suite are reviewable. The full algorithm must then have a declared novelty claim tied to measurable evidence; model size alone is not a contribution.
