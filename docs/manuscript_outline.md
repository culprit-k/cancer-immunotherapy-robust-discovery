# Manuscript outline: Counterfactual Target Recommendation Fidelity Under Virtual Marker Reconstruction

**Status:** Protocol/analysis outline only. No empirical results are available yet. The title, claims and intended journal should be revisited after data eligibility, full prior-art review and the feasibility pilot.

## Proposed title

**Counterfactual Target Recommendation Fidelity Under Virtual Reconstruction of Missing Spatial Protein Markers**

Alternative title: *What Happens When a Marker Is Missing? Testing the stability of spatial immuno-oncology intervention recommendations under virtual staining.*

## Proposed central claim to test

Virtual marker reconstruction can be accurate at the marker level yet may—or may not—preserve the signed target set selected by a downstream spatial counterfactual discovery method. The study will test whether standard marker-reconstruction metrics predict intervention-recommendation fidelity and whether a validation-calibrated reliability/abstention rule adds value.

This is not yet a claim that the effect exists or that the question is novel. VirTues already studies marker reconstruction, cross-panel transfer, and downstream cell phenotyping under marker masking. The intended distinction is specifically the target recommendation/decision resulting from a counterfactual optimization pipeline.

## Abstract template (leave Results unfilled until real analysis)

**Background:** Spatial-proteomics cohorts use heterogeneous antibody panels; missing channels are increasingly reconstructed by foundation models. The extent to which reconstruction preserves downstream counterfactual intervention recommendations is not established by marker-level reconstruction metrics alone.

**Objective:** Evaluate whether virtual reconstruction of wholly missing marker channels preserves signed counterfactual target sets and held-out-patient model-predicted immune-infiltration changes relative to fully measured marker data.

**Methods:** Use eligible, permission-cleared spatial-proteomics cohorts with patient IDs, fully measured channels and a CD8/T-cell outcome. Split by patient before preprocessing or target discovery. Compare a fully measured reference, an observed-only panel baseline, simple imputation and a foundation-model reconstruction under prespecified whole-channel masks. Keep the downstream evaluation model and target budget fixed within each comparison. Evaluate marker reconstruction within patient, target-set fidelity, direction flips and model-predicted uplift on the same fully measured held-out patients. Treat all patient-level outcomes using equal patient weights and prespecified paired uncertainty estimates.

**Results:** To be written only after the dataset is inspected and the analysis is completed. Report all prespecified endpoints, confidence intervals, negative results and failed/empty recommendations.

**Conclusions:** To be written from actual findings only. Distinguish reconstruction quality, recommendation fidelity, biological validity and clinical utility.

## Introduction logic

1. Explain how limited spatial-protein panels create missing-channel and cross-panel analysis challenges.
2. Summarize foundation models/virtual staining (VirTues, Spatium) and note that reconstruction quality and broad downstream tasks already have substantial prior work.
3. Summarize spatial counterfactual target discovery (Morpheus, SPAD-CFR, Celcomen) and establish that target-set generation itself is not new.
4. Point out the narrower empirical question to investigate: whether replacing measured markers with reconstructed values changes the signed intervention set or its held-out predicted objective.
5. State the prespecified research question, hypotheses, and boundaries: model-predicted outcomes are not evidence of causal therapeutic effects.

## Methods structure

### 1. Cohort selection and data governance
List source cohort IDs, publication, sample counts after QC, data licensing, channel names, patient identifiers, endpoint definitions and foundation-model training exposure. Include a flow diagram of datasets considered versus excluded, with reason.

### 2. Leakage and split policy
Use patient-level outer folds; keep all image cores, tiles and cells from a patient together. Fit any imputer fine-tuning, normalization, thresholds or target selection only on training/inner-validation data. Check whether the pretrained reconstruction model saw the evaluation cohort; use leave-one-cohort-out weights or exclude the cohort if leakage cannot be addressed.

### 3. Virtual marker scenarios
Prespecify whole-channel masks based on real panel differences. Include measured-channel reference, reduced panel without imputation, simple imputation, and foundation-model reconstruction. Use cell-wise masking only as a diagnostic. Exclude outcome-label leakage from predictor channels.

### 4. Counterfactual target-discovery baseline
Use the published baseline if the selected cohort is compatible and it can be reproduced. Otherwise document a surrogate and do not call it a Morpheus reproduction. Freeze target budget, optimizer budget and target sign conventions before evaluating outer patients.

### 5. Held-out evaluation
Select intervention sets only using training patients. Apply the reference and reconstructed-selected strategies to the same untouched, fully measured patients using the same evaluation model. Summarize all nested patches/cores within patient before any inferential comparison.

### 6. Outcomes
- Marker-level reconstruction metrics, macro-averaged over patients.
- Signed target-set Jaccard, precision/recall, direction flips, target-set size and empty-set frequency.
- Per-patient predicted uplift fidelity and model-based reference regret.
- Optional reliability/abstention coverage-versus-error curve only if justified by pilot evidence and calibrated on validation data.

### 7. Statistical analysis
Specify the primary endpoint and target budget before final evaluation. Use paired patient-level comparisons within each outer fold. Bootstrap patients, not cells. Correct target-level multiple comparisons as appropriate. Report each cohort separately unless a common estimand supports pooling.

## Planned Results sections (empty until analysis)

1. Cohort and marker-panel eligibility.
2. Baseline and foundation-model reconstruction feasibility.
3. Marker-level reconstruction accuracy by missingness scenario and patient.
4. Recommendation fidelity and direction flips under whole-channel masking.
5. Held-out-patient predicted objective and model-based reference regret.
6. Sensitivity to imputation method, target budget and reconstruction uncertainty.
7. Reliability/abstention trade-off, if prespecified and feasible.
8. Negative findings, failed runs and deviation analysis.

## Figure plan

- **Figure 1:** study design showing fully measured reference versus masked-channel reconstruction, target discovery and held-out evaluation.
- **Figure 2:** marker reconstruction error by marker and patient, comparing baseline and foundation model.
- **Figure 3:** signed target-set fidelity and direction changes across masking scenarios.
- **Figure 4:** paired patient-level model-predicted uplift comparison and reference-regret distribution.
- **Figure 5 (optional):** coverage versus recommendation discrepancy/regret for the validation-calibrated reliability rule.
- **Supplementary:** channel crosswalk, data licenses/access, full target sets, preprocessing/model settings, failed runs and per-cohort results.

## Required limitations statement

The fully measured reference is a model-generated recommendation, not a known biological ground truth. An agreement metric measures recommendation fidelity to that reference, not causal validity. Model-predicted CD8+ infiltration uplift is not an observed treatment effect. In-vitro or external orthogonal validation would be necessary to make stronger biological claims. Any small clinical cohort must be described as exploratory and patient-level sample size must be reported.

## Stop conditions

Do not submit a novelty-led manuscript if the full prior-art audit finds an equivalent intervention-fidelity study, no eligible cohort has the required channel and patient metadata, the foundation model has unavoidable training overlap, or the effect cannot be evaluated on independent patients. A null finding may still support a carefully framed benchmark/reproducibility paper, but no new method should be claimed without evidence.
