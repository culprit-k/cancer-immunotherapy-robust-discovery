# Cancer Immunotherapy AI: Robust Target Discovery

**Project status (25 October 2026): the generic robustness-only paper is NO-GO as a novelty-led study. Conditional GO for a narrow feasibility pilot on counterfactual recommendation fidelity under virtual marker reconstruction. Novelty is not established.**

## Current research candidate

**What Happens When a Marker Is Missing? Counterfactual Target Discovery Under Virtual Staining in Spatial Immuno-oncology**

Primary question: when one or more complete spatial-proteomics marker channels are missing and reconstructed by a foundation model, do the signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes remain faithful to results from fully measured channels?

This is a candidate research question—not a confirmed gap or a claim of a new algorithm. The proposed contribution is downstream **intervention-decision fidelity**, not generic virtual staining, spatial counterfactual generation, cross-panel transfer or Jaccard stability.

## Why the project changed

Morpheus already discovers spatial-proteomic counterfactual target combinations and evaluates them on held-out patients. SPAD-CFR and Celcomen cover spatial counterfactual/generative perturbation modeling. VirTues and Spatium cover foundation-model representations and virtual reconstruction of spatial protein markers; spora has standardized virtual-staining and cross-cohort benchmarks. Therefore, broad combinations, virtual staining, spatial counterfactuals or cross-platform transfer are not enough as novelty claims.

The candidate question is whether good marker reconstruction scores can still mask changes in the *selected signed target set* or in its downstream model-predicted objective. Spatium and CONCERT are material adjacent prior art; the exact gap remains unverified. A validation-calibrated selective/abstention rule is only a possible contribution if it beats simple baselines at a fixed coverage/target budget.

## Work completed in the repository

- Updated literature audit with VirTues, Spatium, Celcomen, spora, the 2026 anti-PD-1 melanoma spatial-mIF dataset and the GSE300793/GSE300445 melanoma cohort.
- Updated novelty assessment and research question.
- Candidate study protocol with hypotheses, leakage-safe design, outcomes and go/no-go criteria.
- Dataset shortlist ranking a melanoma chemokine cohort for development, a smaller lung IMC cohort for smoke testing, and two melanoma cohorts for possible external evaluation, with model-exposure and license caveats.
- Method/dataset compatibility matrix and decision-gate protocol.
- Generic target-stability metric code from the previous phase.
- New panel-shift metrics for marker reconstruction error, signed intervention-set fidelity/direction changes, patient-level predicted-uplift fidelity, and paired patient-level model-based reference regret.
- A post-hoc report CLI that reads prepared reconstruction/prediction CSVs and signed target-set JSON to generate a strict JSON report; it does not run the underlying models.
- Unit tests for both helper modules. A local synthetic suite run on copies of the current source/test files passed **19 tests** (6 target-stability + 9 panel-shift metric + 4 report-builder tests). No completed GitHub Actions run has been verified.
- A GitHub Actions test workflow. No raw data have been committed.

## Next steps, in order

1. Finish full supplementary/prior-art review for Morpheus and the newer virtual-tissue methods.
2. Audit SPORA/spora candidate datasets for patient IDs, CD8/T-cell labels, measured candidate target markers, foundation-model training exposure, and precise data-use terms.
3. Pick one permitted cohort and run a small masked-channel reconstruction smoke test.
4. Reproduce the target-discovery baseline or explicitly define a surrogate if the published implementation is not compatible.
5. Compare measured-channel reference, no-imputation, simple imputation and foundation-model reconstruction on the same held-out patients, using signed target-set fidelity and model-predicted uplift fidelity.
6. Proceed to a full paper only if the exact gap survives prior art and the pilot confirms that the analysis changes a meaningful decision beyond marker-level reconstruction metrics.

## Repository map

- [Research question](docs/research_question.md)
- [Full candidate study protocol](docs/virtual_marker_counterfactual_study.md)
- [Manuscript outline](docs/manuscript_outline.md)
- [Literature review](docs/literature_review.md)
- [Novelty assessment](docs/novelty_assessment.md)
- [Targeted prior-art and feasibility audit (25 Oct 2026)](docs/targeted_prior_art_and_feasibility_audit_2026-10-25.md)
- [Cohort and checkpoint decision record](docs/cohort_checkpoint_decision.md)
- [Related-work addendum](docs/related_work_addendum_2026.md)
- [Method/dataset compatibility matrix](docs/method_dataset_compatibility.md)
- [Dataset shortlist and eligibility checklist](docs/dataset_shortlist.md)
- [Cohort screening template](data/cohort_screening_template.csv)
- [Pilot configuration template](configs/panel_shift_pilot.example.yaml)
- [Pivot candidates](docs/pivot_candidates.md)
- [Morpheus code audit](docs/morpheus_code_audit.md)
- [Dataset feasibility audit](docs/dataset_audit.md)
- [Analysis plan](docs/analysis_plan.md)
- [Decision-gate protocol](docs/decision_gate_protocol.md)
- [Reproducibility run log](docs/reproducibility_run_log.md)
- [Target stability metrics](analysis/target_stability.py)
- [Panel-shift fidelity metrics](analysis/panel_shift_metrics.py)
- [Panel-shift report generator](analysis/panel_shift_report.py)
- [Target stability tests](tests/test_target_stability.py)
- [Panel-shift metric tests](tests/test_panel_shift_metrics.py)
- [Panel-shift report tests](tests/test_panel_shift_report.py)

## Current cohort and checkpoint decision

**Best current choice:** the Salié et al. HCC IMC cohort pair.

- Development/calibration: 54-patient HCC discovery cohort, [Zenodo 10793609](https://zenodo.org/records/10793609). The NLM Dataset Catalog reports CC BY 4.0.
- Untouched external evaluation: 42-patient ICI-treatment HCC cohort, [Zenodo 10794904](https://zenodo.org/records/10794904). OpenAIRE metadata reports CC BY, but the Zenodo Rights/License field is blank, so record this discrepancy and confirm with the data contact or institution where needed.
- Reconstruction checkpoint candidate: official VirTues `virtues-imc14/model.safetensors` from [Hugging Face](https://huggingface.co/bunnelab/virtues), with source code at [bunnelab/virtues](https://github.com/bunnelab/virtues). The variant is trained on 14 IMC cohorts and its weights are CC BY-NC 4.0. It is the best candidate based on the published training-inventory grouping; exact exposure and file hash still need final pinning. Do not use `virtues-sp32` or `virtues-sp31` for a clean held-out claim.

The 54-patient cohort is for development only; keep the 42-patient cohort untouched until target markers, preprocessing, thresholds and the analysis pipeline are frozen. The HCC marker panels must be inspected before locking the intervention set. Morpheus is not yet directly reproduced on HCC.

Full decision record: [Cohort and checkpoint decision](docs/cohort_checkpoint_decision.md).

The project is now at **candidate selection, not data-ready execution**. No dataset archive or model weights have been downloaded, checksummed or run yet.

## Important data and interpretation limits

- The VirTues paper reports that the Morpheus/Wang dataset cannot be redistributed in the harmonized corpus because of licensing restrictions. Do not assume the original Morpheus data are freely reusable just because article or code links are public.
- The current spora website describes 35 cohorts, 5,477 patients and five imaging technologies; the VirTues paper reports its own 32-cohort model corpus. Those inventories have different scopes.
- A full-measurement reference is still a model output, not a biological ground truth.
- Model-predicted CD8+ infiltration uplift is not observed therapeutic effect, causal evidence, clinical utility or patient-specific advice.
- No spatial data archive has been downloaded, and no Morpheus/VirTues/SPAD-CFR/Celcomen model run has been executed in this project.
- This repository is public. No claim about novelty or patentability is made. Consult qualified institutional/IP advice before disclosing enabling details of any genuinely distinct invention.

## Key sources

1. Morpheus (2025): https://doi.org/10.1038/s41551-025-01357-0
2. VirTues (Nature, 2026): https://doi.org/10.1038/s41586-026-10884-y
3. Spatium preprint (2026): https://doi.org/10.64898/2026.07.23.740264
4. CONCERT preprint (2025): https://doi.org/10.1101/2025.11.08.686890
5. Godbole et al. 2026 melanoma IMC cohort: https://zenodo.org/records/15124735
6. Xiao et al. 2022 melanoma IMC panel: https://zenodo.org/records/6836992
4. Celcomen (Nature Communications, 2026): https://doi.org/10.1038/s41467-026-69856-5
5. SPAD-CFR (Biology, 2026): https://doi.org/10.3390/biology15141097
6. spora data documentation: https://spora.epfl.ch/docs/index.html
7. Anti-PD-1 melanoma spatial-mIF data: https://doi.org/10.5281/zenodo.16898362
