# Decision-gate protocol: virtual-marker reconstruction and counterfactual target recommendations

**Status (25 October 2026): conditional GO for a small feasibility pilot only. The generic robustness-only paper remains NO-GO as the main novelty claim.**

## Current candidate

**Question:** When one or more complete spatial-proteomics marker channels are absent and reconstructed by a foundation model, do the resulting signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes remain faithful to those obtained from fully measured channels?

The candidate is motivated by the intersection of:
- Morpheus and other spatial counterfactual target-discovery approaches.
- VirTues/Spatium and other virtual-staining or marker-reconstruction methods.
- Existing work on imputation uncertainty and downstream spatial inference.

This is not a verified research gap or a claim to invent virtual staining/counterfactual modeling.

## Why alternatives A/B are insufficient as originally framed

### Cross-method intervention decision utility
Morpheus, SPAD-CFR and Celcomen have different input/output representations and endpoints; a direct comparison cannot be assumed valid without a common measurement and evaluation design. VirTues and SPORA already benchmark cross-cohort/technology spatial representations and biomarker tasks.

### Broad cross-cohort/platform transfer
This is already well established by VirTues and related foundation models. Transfer might still be important, but it is not sufficient novelty alone.

### Replacement candidate: decision fidelity under marker missingness
The narrower question is whether virtual marker reconstruction changes the *intervention recommendation* even when marker reconstruction scores look good. This is more specific, but still requires a targeted prior-art audit.

## Gate 0 — targeted novelty audit

1. Read the complete Morpheus supplementary material.
2. Inspect VirTues/Spora, Spatium, Celcomen, SPAD-CFR, TISSUE and related spatial-proteomics imputation/counterfactual literature.
3. Search specifically for recommendation-level or intervention-set fidelity after whole-channel masking, virtual staining, imputation uncertainty and marker-panel shift.
4. Record overlap in input modality, missingness mechanism, target output and outcome.
5. Do not claim novelty unless the exact downstream decision-fidelity test is meaningfully absent.

**Pass:** no equivalent study appears after this targeted audit and dataset feasibility is established.  
**Fail/pivot:** prior work already tests the same recommendation-level consequence, or only generic reconstruction accuracy is new.

## Gate 1 — dataset, marker and license eligibility

Select candidate data only if they provide:
- measured spatial protein channels that can be hidden to create an evaluation reference;
- a measured CD8/T-cell endpoint or appropriate held-out cell-state label;
- candidate perturbation markers with clear marker identities and directions;
- patient/core/section identifiers;
- data-use terms that permit analysis and publication of derived results;
- a foundation-model checkpoint whose exposure to this cohort can be accounted for.

The current spora docs report 35 cohorts and 5,477 patients across five imaging technologies, whereas the VirTues paper describes its own 32-cohort pretraining corpus. These counts have different scope. The Morpheus/Wang data were obtained by access request for VirTues and cannot be redistributed in the harmonized corpus; do not assume their availability or permission.

**Pass:** at least one eligible cohort has sufficient markers, patient metadata and explicit reuse terms.  
**Fail/pivot:** no comparable data, missing patient IDs, unclear terms, or unavoidable foundation-model training leakage.

## Gate 2 — compute and baseline reproducibility

1. Obtain one permitted dataset subset.
2. Reproduce a small marker reconstruction example with VirTues or another approved model.
3. Calculate marker reconstruction error against true measured values hidden from the model.
4. Run the same counterfactual target-discovery pipeline under fully measured and reconstructed conditions.
5. If Morpheus cannot be fairly adapted, define a clearly named surrogate and do not claim reproduction of Morpheus.
6. Record hardware, model/data versions, checksums, runtime, failures and deviations.

**Current status:** no spatial dataset has been downloaded; no VirTues, SPAD-CFR, Celcomen or Morpheus checkpoint has been run in this project.

## Gate 3 — leakage-safe evaluation

- Split by patient and keep every core, section, tile and cell from one patient in one partition.
- Fit all normalization, imputation, target selection, thresholds and hyperparameters only on training/inner-validation patients.
- Reserve untouched outer patients for evaluation.
- Mask whole channels to mimic real panel missingness; cell-wise random masking is a diagnostic, not the primary scenario.
- Exclude CD8 label leakage from predictor inputs.
- Use exactly matched target budgets across conditions.
- Aggregate predicted uplift within patient before calculating patient-level statistics.
- Do not select targets based on outer test results.

## Gate 4 — outputs and interpretation

Measure:
1. Marker reconstruction error (MAE/RMSE/correlation).
2. Signed target-set fidelity (Jaccard, precision/recall, direction flips, target-set size).
3. Patient-level model-predicted uplift agreement and model-based reference regret on fully measured held-out patients.
4. Optional coverage/error trade-off for a confidence-aware abstention rule, with threshold chosen on validation data.

The full-measurement reference is itself a model output, not biological truth. "Reference regret" is disagreement in predicted objective, not clinical regret or a measured treatment effect. Do not claim a causal mechanism or therapeutic efficacy.

## Go/no-go decision

**Proceed to a full study** only if the exact gap survives prior-art review, the data/rights gate passes, the model is not leaking the evaluation cohort, and the pilot shows that marker imputation can change a target decision in a measurable way beyond standard reconstruction errors.

**Stop or pivot** if the task is already benchmarked, no compatible cohort exists, the baseline does not run, or only generic marker reconstruction results can be reported.

## Intellectual property and transparency

The repository is public. No patentability or novelty claim is made. If a genuinely distinct invention emerges, consult institutional technology-transfer or qualified patent advice before disclosing enabling details.
