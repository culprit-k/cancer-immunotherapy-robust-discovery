**Project status (27 October 2026):** HCC archive integrity and structural image/mask QC have passed the checks documented in the audit, including an 86-image/mask inventory and explicit unresolved patient/ROI multiplicity conflicts (ICI_24 and ICI_39). The released HCC images are normalized to [0,1], and official VirTues input compatibility remains **UNPROVEN**; do not run official pretrained inference on them or invent inverse preprocessing. The candidate `virtues-imc14` checkpoint is hash-pinned but remains conditional on exact training-manifest/exposure verification; `virtues-sp32` is not eligible for held-out HCC evaluation. An experimental, reversible CPU SDPA attention helper and synthetic tests have now been added to the open audit branch, but it has **not** been executed in the user's Colab or on real data. No real-data inference, validated biological target, clinical prediction, or novelty claim has been established. See the [HCC preprocessing/exposure decision](docs/hcc_preprocessing_and_checkpoint_exposure_decision_2026-10-25.md), [latest compatibility review](docs/HCC_virtues_compatibility_review_2026-10-27.md), and [CPU SDPA helper scope and instructions](docs/virtues_cpu_sdpa_compatibility_patch_2026-10-27.md).

## Current research candidate

**What Happens When a Marker Is Missing? Counterfactual Target Discovery Under Virtual Staining in Spatial Immuno-oncology**

Primary question: when one or more complete spatial-proteomics marker channels are missing and reconstructed by a foundation model, do the signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes remain faithful to results from fully measured channels?

This is a candidate research question—not a confirmed gap or a claim of a new algorithm. The proposed contribution is downstream **intervention-decision fidelity**, not generic virtual staining, spatial counterfactual generation, cross-panel transfer or Jaccard stability.

## Why the project changed

Morpheus already discovers spatial-proteomic counterfactual target combinations and evaluates them on held-out patients. SPAD-CFR and Celcomen cover spatial counterfactual/generative perturbation modeling. VirTues and Spatium cover foundation-model representations and virtual reconstruction of spatial protein markers; spora has standardized virtual-staining and cross-cohort benchmarks. Therefore, broad combinations, virtual staining, spatial counterfactuals or cross-platform transfer are not enough as novelty claims.

The candidate question is whether good marker reconstruction scores can still mask changes in the *selected signed target set* or in its downstream model-predicted objective. Spatium and CONCERT are material adjacent prior art; the exact gap remains unverified. A validation-calibrated selective/abstention rule is only a possible contribution if it beats simple baselines at a fixed coverage/target budget.

## Work completed in the repository

- Completed the HCC archive, panel and sampled TIFF audit: checksum and size match, the 42-row panel passes structural QC, 12 evenly spaced image stacks were readable, sampled pixel values were float32 and within [0,1], and sampled cell/stroma masks matched image spatial grids. Latest completed audit: [run 40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382), metadata-only artifact [12607480794](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382/artifacts/12607480794). This is sparse sampling, not an exhaustive pixel scan.
- Resolved current HCC inference decision: public TIFFs are PENGUIN-normalized to 0–1 and are not interchangeable with VirTues' documented clipping/log/blur/standardization input path. Do not invert or guess preprocessing statistics.
- Exposure decision: the pinned `virtues-imc14` checkpoint aligns with the core 14-IMC set; Salié HCC is ref. 95 among additional IMC cohorts in the extended corpus. `virtues-sp32` includes Salié HCC; `virtues-sp31` needs an exact omitted-cohort check before any held-out claim. See the evidence and caveat in the decision memo.

- Updated literature audit with VirTues, Spatium, Celcomen, spora, the 2026 anti-PD-1 melanoma spatial-mIF dataset and the GSE300793/GSE300445 melanoma cohort.
- Updated novelty assessment and research question.
- Candidate study protocol with hypotheses, leakage-safe design, outcomes and go/no-go criteria.
- Selected the 54-patient Salié HCC discovery IMC cohort (CC BY 4.0 per the NLM Dataset Catalog) for development/calibration and the 42-patient ICI-treated HCC cohort as conditional external evaluation (OpenAIRE metadata says CC BY, while Zenodo's direct rights field appears blank).
- Method/dataset compatibility matrix and decision-gate protocol.
- Generic target-stability metric code from the previous phase.
- New panel-shift metrics for marker reconstruction error, signed intervention-set fidelity/direction changes, patient-level predicted-uplift fidelity, and paired patient-level model-based reference regret.
- A post-hoc report CLI that reads prepared reconstruction/prediction CSVs and signed target-set JSON to generate a strict JSON report; it does not run the underlying models.
- Unit tests for both helper modules. A local synthetic run on isolated copies reached **20 passing tests**, but report-generator/test copies differed byte-for-byte from the latest remote blobs. The hosted GitHub Actions suite passed **19 tests** after adding the missing SciPy dependency (commit `a04fcc0`); a follow-up run is triggered for the latest documentation/template commits. Latest workflow status: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions.
- A GitHub Actions test workflow. No raw data have been committed.

## Next steps, in order

1. Download the 54-patient HCC discovery archive and 42-patient HCC ICI validation archive outside public GitHub; checksum them and inspect their panel CSVs and patient metadata.
2. Resolve the 42-patient cohort's blank Zenodo licence display (OpenAIRE reports CC BY) and preserve the rights evidence for both cohorts.
3. Download the official VirTues `virtues-imc14/model.safetensors` weights under the CC BY-NC 4.0 terms; pin the immutable revision and SHA-256, then verify exact training exposure.
4. Run one-channel masked reconstruction on development data, compare against held-out measured values, and check panel-to-marker mapping.
5. Reproduce or clearly adapt the counterfactual target baseline for HCC; freeze the CD8 endpoint, eligible target markers, thresholds and target budget before evaluating the 42-patient cohort.
6. Continue to a full paper only if the novelty gate and pilot outcome support a meaningful recommendation-level contribution.

## Repository map

- [Research question](docs/research_question.md)
- [Project execution status and remaining gates (27 Oct 2026)](docs/project_execution_status_2026-10-27.md)
- [Full candidate study protocol](docs/virtual_marker_counterfactual_study.md)
- [Manuscript outline](docs/manuscript_outline.md)
- [Literature review](docs/literature_review.md)
- [Novelty assessment](docs/novelty_assessment.md)
- [Targeted prior-art and feasibility audit (25 Oct 2026)](docs/targeted_prior_art_and_feasibility_audit_2026-10-25.md)
- [Cohort and checkpoint decision record](docs/cohort_checkpoint_decision.md)
- [Checkpoint revision/hash resolver](scripts/resolve_virtues_imc14_checkpoint.py)
- [Checkpoint resolver workflow](.github/workflows/resolve_virtues_imc14_checkpoint.yml)
- [Experimental VirTues CPU SDPA compatibility helper and limits](docs/virtues_cpu_sdpa_compatibility_patch_2026-10-27.md)
- [Reversible CPU SDPA patch utility](scripts/patch_virtues_cpu_sdpa.py)
- [CPU SDPA patch tests](tests/test_patch_virtues_cpu_sdpa.py)
- [One-command Colab preflight runner](scripts/run_virtues_cpu_preflight_colab.py)
- [Colab preflight CLI test](tests/test_virtues_cpu_preflight_cli.py)
- [Related-work addendum](docs/related_work_addendum_2026.md)
- [Method/dataset compatibility matrix](docs/method_dataset_compatibility.md)
- [Verified HCC discovery marker-panel audit and inference gates](docs/discovery_panel_audit.md)
- [Draft data clarification request for original intensities and cell labels](docs/data_clarification_request_salie_hcc.md)
- [Compatible cohort decision memo and fallback path](docs/compatible_cohort_decision_memo.md)
- [Next execution plan and go/no-go gates](docs/next_execution_plan.md)
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

- Discovery cohort: 54-patient HCC cohort, [Zenodo 10793609](https://zenodo.org/records/10793609). The completed CI audit's Zenodo API query reports `cc-by-4.0`; archive checksum and panel structural QC passed. Direct use with pretrained VirTues is blocked by image preprocessing incompatibility.
- Potential external evaluation: 42-patient ICI-treatment HCC cohort, [Zenodo 10794904](https://zenodo.org/records/10794904). The completed CI audit's Zenodo API query also reports `cc-by-4.0`; its image archive was not downloaded. Preserve the audit evidence and confirm with the data contact/institution if a landing-page licence display is institutionally required.
- Reconstruction checkpoint: official `virtues-imc14/model.safetensors`, weight licence CC BY-NC 4.0. Its immutable revision and file SHA-256/size are pinned below. Published corpus inventory places Salié et al. (ref. 95) among added IMC cohorts in the extended corpus, not the core-14 model. This supports no direct study exposure for `virtues-imc14` at reference level; `virtues-sp32` includes Salié HCC and is unsuitable for held-out evaluation. The exact cohort omitted from `virtues-sp31` has not been verified, so do not use that checkpoint for held-out HCC unless its omission list confirms exclusion.

The checkpoint file is hash-pinned: revision `43fd00fce052c46f9e0cc1a87f42806620632319`, SHA-256 `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`, size 173543728 bytes. Only its provenance manifest was retained; the weights were not committed to GitHub. The published corpus inventory supports core-14 exposure separation for the Salié study, with no signed accession-level certificate located. Zenodo API metadata returned `cc-by-4.0` for both HCC records; the ICI image archive was not downloaded.

The 54-patient cohort can support HCC-specific adaptation research only after a separate valid input pipeline is specified; the public normalized TIFFs are not suitable for direct VirTues pretrained inference. Keep the 42-patient cohort untouched until a validated pipeline, endpoint, eligible markers, thresholds and analysis are frozen. Morpheus has not been directly reproduced on HCC.

Full decision records: [Cohort and checkpoint decision](docs/cohort_checkpoint_decision.md), [HCC preprocessing/exposure decision](docs/hcc_preprocessing_and_checkpoint_exposure_decision_2026-10-25.md), and [normalized-input adaptation protocol](docs/hcc_normalized_input_adaptation_protocol.md).

The project remains in **pre-inference compatibility validation**. The completed archive/panel/TIFF storage audit [run 40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382) verified the checksum, panel and sampled image/mask storage metadata; its metadata-only artifact [12607480794](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382/artifacts/12607480794) is published. No raw images/masks were committed. The pinned checkpoint has not been loaded for HCC inference. Direct claims of official VirTues preprocessing reproduction are NO-GO; the separately labeled normalized-domain adaptation pilot is unrun and must pass patient-held-out reconstruction tests before downstream counterfactual analysis.

## Important data and interpretation limits

- The VirTues paper reports that the Morpheus/Wang dataset cannot be redistributed in the harmonized corpus because of licensing restrictions. Do not assume the original Morpheus data are freely reusable just because article or code links are public.
- The current spora website describes 35 cohorts, 5,477 patients and five imaging technologies; the VirTues paper reports its own 32-cohort model corpus. Those inventories have different scopes.
- A full-measurement reference is still a model output, not a biological ground truth.
- Model-predicted CD8+ infiltration uplift is not observed therapeutic effect, causal evidence, clinical utility or patient-specific advice.
- The 54-patient discovery archive has been integrity-checked and its panel metadata inspected; no raw images/masks were retained in the repository. No Morpheus/VirTues/SPAD-CFR/Celcomen inference run has been executed in this project.
- This repository is public. No claim about novelty or patentability is made. Consult qualified institutional/IP advice before disclosing enabling details of any genuinely distinct invention.

## Key sources

1. Morpheus (2025): https://doi.org/10.1038/s41551-025-01357-0
2. VirTues (Nature, 2026): https://doi.org/10.1038/s41586-026-10884-y
3. VirTues model repository and weight licences: https://github.com/bunnelab/virtues and https://huggingface.co/bunnelab/virtues
4. Salié et al. HCC paper: https://doi.org/10.1136/gutjnl-2024-332837
5. HCC discovery cohort (54 patients; NLM catalogue reports CC BY 4.0): https://zenodo.org/records/10793609
6. HCC ICI cohort (42 patients; OpenAIRE reports CC BY, source-page licence display to reconcile): https://zenodo.org/records/10794904
7. Spatium preprint (2026): https://doi.org/10.64898/2026.07.23.740264
8. CONCERT preprint (2025): https://doi.org/10.1101/2025.11.08.686890
9. SPAD-CFR (Biology, 2026): https://doi.org/10.3390/biology15141097
10. spora data documentation: https://spora.epfl.ch/docs/index.html


## Latest operational audit (25 October 2026)

- GitHub Actions run [40198072585](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198072585) downloaded the 1,541,132,381-byte discovery archive and matched the expected MD5 `a842fa253ac2f0eda3cbf4d41e1b0ec1`.
- The actual panel filename is `DiscoveryCohort_panel.csv` (42 rows; columns `Channel`, `MetalTag`, `Target`). The original audit's exact-name assumption was wrong, and the subsequent artifact-upload step also had an escaped GitHub expression that produced an invalid path. The latter is being fixed in the workflow.
- The 42-patient ICI cohort's current Zenodo API metadata returned `cc-by-4.0`; the landing-page display discrepancy should still be recorded and terms rechecked before any redistribution or external evaluation.
- This is a metadata and panel audit, not a successful artifact publication, model inference, biological result, or proof of intervention compatibility. The HCC panel contains CD8a, PD1, PD-L1, TIGIT, Tim3 and Lag3, but a Morpheus-style target set and its objective must be mapped explicitly before claiming compatibility.
