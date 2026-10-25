# Analysis plan: intervention decision fidelity under virtual marker reconstruction

**Status (25 October 2026): pilot plan only. The old generic robustness-only novelty claim is rejected. The new candidate gap remains unverified.**

## Objective

Test whether reconstruction of missing spatial protein-marker channels preserves (a) the signed target combinations chosen by a counterfactual discovery pipeline and (b) its held-out-patient **model-predicted** CD8+ infiltration change, relative to a fully measured-channel reference.

## Stage 0 — prior art and dataset eligibility
- Read the complete Morpheus supplement and inspect relevant VirTues, Spora, Spatium, Celcomen, SPAD-CFR, TISSUE and downstream virtual-staining/imputation papers.
- Search specifically for counterfactual target-set fidelity under whole-channel masking, virtual staining and imputation uncertainty.
- Inspect and verify the selected Salié HCC panel CSVs, patient/core IDs, CD8/T-cell endpoint and exact data-use terms; see the cohort/checkpoint decision record.
- Check whether the foundation-model weights saw the candidate cohort; use a leave-one-cohort-out checkpoint or other leakage-safe design if needed.
- Do not redistribute raw or restricted data.

## Stage 1 — small smoke test
- Get one permitted public cohort and one pretrained reconstruction model.
- Verify table schema, marker aliases, patient/core grouping, and exact mapping from measured to reconstructed channels.
- Mask one entire measured channel in a small held-out subset, reconstruct it, and calculate marker error against its true measured value.
- Run the downstream baseline on a tiny subset if the data are compatible.
- Record environment, model/data version, license, checksums, hardware, run time and all deviations.
- Do not claim full baseline reproduction until a known published result is recovered.

## Stage 2 — panel scenarios
Prespecify the exact scenarios after inspecting panel metadata but before examining model outcomes:
1. Whole-channel masking, one channel at a time.
2. A cross-panel-like missing set constructed from real panel overlaps.
3. Optional higher-dropout scenario only if it represents a real assay difference.
4. Cell-wise/random masking is a diagnostic only, not the principal scenario.

The CD8/T-cell outcome must retain a true measured label for evaluation even when the associated input signal is masked. All input channels that directly leak the output label must be excluded or masked.

## Stage 3 — competing conditions
Using the same patient-grouped outer folds and identical target budget:
- **Reference:** full measured channels.
- **Reduced-panel baseline:** only observed channels, with no imputation.
- **Simple imputer:** choose a reproducible baseline after checking data structure.
- **Foundation-model reconstruction:** e.g., VirTues reconstructed channels.
- **Optional second imputer:** include only if licensing, method compatibility and compute allow.

Apply the same counterfactual target-discovery algorithm across conditions. Prefer Morpheus if the selected data can be converted fairly to its input/output format; otherwise label any alternative implementation as a surrogate, not as Morpheus reproduction.

## Stage 4 — leakage-safe target discovery
- Split by patient at the outer level. All cores, sections, tiles and cells from a patient remain in one partition.
- Fit normalizers, model, imputation transforms, thresholds and feature selection only on training/inner-validation patients.
- Generate target sets from training patients only.
- Fix the candidate target marker list and target budget before outer test evaluation.
- Encode each target with its marker identity and signed direction (+1 increase, -1 decrease).
- Evaluate every strategy on the same held-out patients using the measured-channel values for independent downstream reference.
- Aggregate nested patches/cores within patient and give each patient equal weight.

## Stage 5 — outcomes
### Marker-level reconstruction
- MAE, RMSE, bias, Pearson and Spearman correlation on held-out cells/locations.
- Marker-stratified results; do not report only a pooled score.

### Recommendation fidelity (primary)
- Signed target-set Jaccard similarity vs. fully measured reference.
- Signed precision/recall.
- Direction-flip count/rate among shared markers.
- Set size and empty-recommendation frequency.

### Predicted-uplift fidelity (key secondary)
- Patient-level MAE/RMSE and rank correlation between predicted uplift from reconstructed-panel and reference target sets.
- Direction/sign concordance by patient.
- Model-based reference regret: reconstructed-selected strategy's predicted uplift minus full-measurement-reference strategy's predicted uplift, evaluated on the same fully measured held-out patients.
- Label every uplift estimate as **model-predicted**, not observed treatment effect.

### Optional reliability/abstention analysis
Only include if the pilot demonstrates meaningful decision changes. Calibrate target-set agreement or imputation uncertainty thresholds on inner validation, then report coverage vs. set disagreement and model-based regret in outer test patients. Compare with single imputation and simple selection-frequency baselines.

## Stage 6 — uncertainty and inference
- Use paired condition comparisons on the same held-out patients.
- Bootstrap patients, not cells or patches.
- Report confidence intervals for marker and target-level metrics; account for multiple target comparisons where relevant.
- Report each cohort separately; pool only if endpoint and measurement scales are compatible.
- Report null results and all failed/empty recommendations.
- Do not infer causality from a stable counterfactual prediction or marker association.

## Decision criteria
**Proceed to full study** only if:
- the exact downstream fidelity question survives the expanded prior-art search;
- at least one eligible, clearly licensed cohort has sufficient markers and patient IDs;
- model training exposure can be controlled;
- the baseline and masked-channel reconstruction run end-to-end;
- the result tests recommendation fidelity rather than just reconstruction accuracy.

**Pivot/stop** if no dataset supports the comparison, data reuse terms are unclear, the model has unavoidable evaluation leakage, the baseline cannot run, or prior work already evaluates this same downstream decision.

## Cohort and checkpoint decision (25 October 2026)

Use the selected Salié HCC IMC cohort pair:
- **Development/calibration:** 54-patient discovery cohort, Zenodo 10793609, with CC BY 4.0 reported by the NLM Dataset Catalog.
- **External evaluation:** 42-patient ICI-treated cohort, Zenodo 10794904, where OpenAIRE/Datacite metadata reports CC BY but the Zenodo rights field appears blank. Preserve the metadata evidence and resolve the discrepancy before redistribution if required.
- **Reconstruction checkpoint candidate:** official VirTues `virtues-imc14/model.safetensors` (14 IMC training datasets; CC BY-NC 4.0 weights). Do not use `virtues-sp32`/`virtues-sp31` for a held-out Salié claim. Pin the precise immutable revision and SHA-256 at download, and confirm exact cohort exposure.

The exact marker panel and patient metadata still require local inspection. The source cohort archives provide per-channel TIFF stacks; convert them and the masks to VirTues/spora's expected layout and audit preprocessing before inference. VirTues applies clipping/log transformation, tissue-aware normalization and Gaussian smoothing during its published preprocessing, so avoid double-transforming source-normalized images. No channel-specific target set is final until both panel CSVs have been checked. Use development patients to freeze the endpoint, preprocessing, target budget, threshold and abstention rule. Open the 42-patient cohort only for the final external evaluation. VirTues reconstruction and the counterfactual target model are separate components; a Morpheus-style target generator has not yet been validated on this HCC data.

Decision record: [docs/cohort_checkpoint_decision.md](cohort_checkpoint_decision.md).
