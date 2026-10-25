# Reproducibility run log

**Last updated:** 25 October 2026  
**Status:** Main-article/public-code audit and synthetic helper-function tests completed; current robustness-only novelty proposal rejected as a standalone novelty claim; data/model reproduction still pending.

## Source audit completed

### Morpheus paper and public implementation
- Inspected the main published article/Methods PDF, Morpheus README, tutorial notebook, main.py, counterfactual-generation code, analysis helper, and TrustScore implementation.
- Confirmed the public tutorial path uses crc_tutorial.zip from Caltech Data Portal record ID pr14s-wgk05, a pretrained unet.ckpt, and patient_split.json.
- Confirmed the runnable example sets seed_everything(42); this is a fixed seeded starting setup, not robustness across seeds.
- Confirmed code tracks PatientID, ImageNumber and patch_id and maps perturbation outputs back to patient/image metadata.
- Confirmed TrustScore is a nearest-neighbour distance-based classifier-input trust score, not the stability of complete intervention sets across patient resamples/retrained models.
- Confirmed the generation helper chooses a decision threshold using the validation split before generating counterfactuals.
- The main article establishes patient-level splits, within-patient and across-patient median aggregation, in-silico held-out-patient evaluation, sensitivity to sparsity and marked sample variability.

### New nearby literature identified
- PHAROS (bioRxiv preprint, September 2026): single-cell perturbation-model search for target-directed combinations with controls, sampled batches, independent combinatorial data evaluation and robustness-aware reranking.
- Anzum et al., MICCAI 2026: counterfactual directional cell-cell influence in spatial transcriptomics, with held-out cores, permutation/spatial-shuffle controls and core-level bootstrap uncertainty.
- Ding et al., SPAD-CFR, Biology 2026: spatial point-cloud/diffusion counterfactual tissue reprogramming with molecular profiles and coordinates changed together, including melanoma immune-focused intervention hypotheses.
- Consequence: a generic paper that bootstraps/retrains Morpheus and reports selection frequency/Jaccard alone is now considered too incremental for a high-novelty contribution. See docs/related_work_addendum_2026.md and docs/pivot_candidates.md.

## Data and access trail
- The paper cites a melanoma dataset, original melanoma data-for-analysis, Morpheus-preprocessed data/model outputs, and a small CRC tutorial bundle. These are distinct resources.
- The original melanoma data-for-analysis record lists data_for_analysis.zip at approximately 7.1 GB and a code archive around 41 MB. The license field is not clear in the record; check terms before reuse/re-distribution.
- Morpheus reports 159 melanoma cores from 69 patients; CRC liver-metastasis cohort 209 cores from 30 patients; breast cohort 749 cores from 693 patients, with a marker panel described as unsuitable for the same therapeutic perturbation task.
- The separate supplementary PDF is available as a listed artifact from CaltechAUTHORS, but retrieval through its signed download redirect failed. The supplement has not been read and must not be reported as audited.

## What did not run
- No data archive was downloaded into this runtime.
- No Morpheus dependency environment was installed.
- No original checkpoint was loaded.
- No model training, counterfactual generation, full notebook reproduction or biological validation was performed.
- Direct network retrieval from this execution environment failed with name-resolution/network errors; this does not show the public data host is unavailable.

## Code added to this research repo
- analysis/target_stability.py: target selection frequency, pairwise/full-set Jaccard, signed-direction consistency, patient-equal-weight predicted uplift summary and patient-level bootstrap confidence intervals.
- tests/test_target_stability.py: six synthetic unit tests covering metric conventions, equal patient weighting, deterministic bootstrap and invalid inputs.
- Local unit-test command: python -m pytest -q
- Result: **6 passed** on synthetic inputs.
- These tests validate generic helper code only; they do not reproduce Morpheus or establish a scientific result.

## Updated next steps
1. Retrieve and read the complete Morpheus supplementary PDF.
2. Resolve license/terms for the exact data and code artifacts.
3. Build a dataset/method compatibility matrix for cross-method intervention decision utility and cross-cohort/platform transfer.
4. Run a small permitted baseline reproduction in a network-enabled environment, recording versions, checksums, hardware, runtime and deviations.
5. Choose one primary research question only after the prior-art and compatibility gates pass.


## 25 October 2026 — virtual-marker / recommendation-fidelity pivot

### Prior-art refinement
- VirTues (Nature, 2026) is not just a marker-reconstruction model: its Methods also tests whether downstream cell phenotyping remains stable under virtual-marker replacement. It removes/reconstructs CD20 and CD20+CD38 for B-cell phenotyping on Danenberg data and progressively masks T-cell markers for phenotyping on Cords data.
- Therefore, the candidate novelty boundary is narrower than "imputation affects downstream analyses": test whether virtual marker reconstruction changes **signed counterfactual intervention sets and their held-out-patient model-predicted objective**. This is still unverified and needs targeted prior-art review.
- VirTues uses the Hoch et al. melanoma cohort for cell-typing evaluation and notes that some phenotype evaluations align patient-level train/test splits with pretraining. Do not label Hoch as unseen-cohort validation with the standard published full VirTues model.

### Dataset shortlist
- hoch2022multiplexed: melanoma IMC, 35 patients / 50 images in the spora catalogue; most biologically relevant development candidate for chemokines and immune infiltration, subject to panel/license and VirTues exposure checks.
- allam2022spatially: lung IMC, 26 patients / 26 images and about 500 MB in the spora quick-download workflow; best small smoke-test candidate if markers and rights pass.
- moldoveanu2022spatially: melanoma IMC, 90 patients / 90 images; potential independent evaluation candidate, but target markers, outcome labels and model training exposure still need verification.
- xiao2022multiplexed: melanoma IMC, 26 patients / 158 images, anti-PD-1 context; potential external cohort subject to same checks.
- Exact cohort licenses vary. The catalogue was reviewed, but no dataset file was downloaded or inspected locally.

### Synthetic code tests
- Helper source and test files were copied from the current GitHub contents into an isolated local test directory because a direct GitHub clone failed in the execution environment due DNS/name-resolution errors.
- Ran pytest -q tests: **13 passed** (6 target-stability tests + 7 panel-shift metric tests) on synthetic data.
- Test coverage includes reconstruction MAE/RMSE/correlation, signed target-set overlap/direction flips, patient-level uplift fidelity, equal weighting through the patient-level inputs, deterministic bootstrap and invalid-input checks.
- This verifies the utility functions against synthetic cases only. It is not a test of VirTues, Morpheus, SPORA data, or a biological hypothesis. GitHub Actions status was not independently confirmed.

### Still not run
- No spatial data archive downloaded or checksummed.
- No VirTues weights or Morpheus checkpoint loaded.
- No masked-channel reconstruction on actual images/cells.
- No counterfactual target discovery or held-out-patient objective evaluated.
- No full Morpheus supplementary PDF audit; its downloadable artifact could not be retrieved in this runtime.


### Updated metric implementation and tests
- Added a paired patient-level reference-regret helper: compares the candidate and reference target strategies with the same evaluator on the same fully measured held-out patients; positive candidate-minus-reference values mean higher model-predicted uplift.
- Added two more unit tests for patient-level reference regret and mismatched patient IDs.
- Local test run of materialized copies of the committed helper/test source: **15 passed** (6 target-stability + 9 panel-shift tests) using synthetic data.
- The GitHub Actions workflow was corrected to install pandas as well as NumPy/pytest. Its actual hosted run status remains unverified.


### Reporting harness
- Added analysis/panel_shift_report.py, a CLI that accepts prepared marker-reconstruction values, held-out per-core/patch predictions for both strategies, and a JSON of signed target sets; it emits a strict JSON report for reconstruction metrics, target-set fidelity, patient-level uplift fidelity and paired model-based reference regret.
- Added three synthetic tests for the report builder, including matched-patient validation and required-column checks.
- Updated local synthetic test run after adding the report harness: **18 passed** (6 target-stability + 9 panel-shift metric + 3 report-builder tests).
- This harness only evaluates prepared outputs. It does not download data, run VirTues/Morpheus, reconstruct channels or generate counterfactual target sets.


### Patient-level reconstruction error correction
- Hardened the report harness to require patient_id in the reconstruction table, calculate marker reconstruction metrics within each patient, and report patient-macro-averaged error as the primary metric. Pooled-cell metrics are retained only as a secondary diagnostic.
- Added a synthetic test showing how a patient with many more cells would otherwise dominate the pooled error.
- Updated local synthetic suite: **19 passed** (6 target stability + 9 panel-shift metric + 4 panel-shift report tests). The locally materialized copies reflect the updated source and tests from GitHub.


### Patient-macro reconstruction error safeguard
- Updated the report schema to require `patient_id` for every reconstruction row.
- Per-marker MAE/RMSE/bias/correlation are now computed within each patient first and then macro-averaged across patients; pooled-cell metrics are explicitly secondary. This prevents patients with many more cells from dominating the primary reconstruction summary.
- Added a synthetic test that adds many rows to one patient and checks equal patient weighting.
- The previous local test run was **18 passed** before this latest test was added. The current committed suite should contain 19 tests, but a completed hosted CI run for the latest commit has not been verified; do not state 19 passed until CI or a local run confirms it.


## 25 October 2026 — targeted prior-art and local test verification

- Added `docs/targeted_prior_art_and_feasibility_audit_2026-10-25.md` with the decision boundary, licensing/exposure gates and stop conditions.
- Added Spatium (spatial-protein imputation), CONCERT (spatial-transcriptomics imputation plus counterfactual perturbation simulation), and the 2026 spatial-metabolomics imputation benchmark to the nearby-prior-art risk list. These do not prove exact equivalence, but make a broad imputation-plus-counterfactual claim unsafe without a full methods/supplement comparison.
- Inspected the official VirTues repository's published weight table: `virtues-sp32` is trained on 32 datasets and uses CC BY-NC 4.0 weights; `virtues-sp31` is trained on 31 datasets with MIT weights; `virtues-imc14` is trained on 14 IMC datasets with CC BY-NC 4.0 weights. Exact training exposure of the checkpoint selected for Rigamonti is still unverified.
- Ran `python -m pytest -q` in the available isolated test-copy directory `/mnt/data/research-helper-tests`: **19 passed** in 1.20 seconds. This verifies the current local source/test copies only; it does not prove the repository's current checkout or hosted GitHub Actions passed.
- No dataset downloaded, checksum recorded, licence cleared, model loaded, counterfactual generated or biological experiment performed.


## 25 October 2026 — cohort panel re-ranking

- Inspected the official spora-bench Rigamonti dataset and cell-annotation configs. They confirm a CD8 T-cell annotation but do not establish a Morpheus-compatible perturbation marker panel. The original Rigamonti paper describes a 24-marker NSCLC panel focused on tumour, architecture and immune-lineage markers; demote it to pipeline smoke testing unless a narrower target question is justified before analysis.
- Inspected the published Xiao et al. 2022 41-channel panel: CD8a, PD-1 and PD-L1 are present, but the VirTues extended corpus lists Xiao et al. 2022 among its 32 cohorts. Standard `virtues-sp32` therefore cannot be treated as an independent imputer for Xiao.
- Inspected the panel CSV in the Godbole et al. melanoma IMC dataset posted 17 September 2026 (Zenodo 15124735). It lists CD8a, PD-1, PD-L1, CTLA-4, TIM-3, LAG-3, TIGIT, CCL2 and CCL4. This is a promising external exploratory candidate because it postdates the VirTues release, but has only six patients, no displayed dataset licence, and unverified exact checkpoint exposure. Do not use until terms are clarified; not suitable as definitive external validation.
- Dataset shortlist and README have been corrected. No cohort is yet rights-cleared or approved for the primary experiment.

- Ran an end-to-end **synthetic CLI smoke test** on the isolated local helper copies: generated a strict JSON report from tiny synthetic CSV/JSON inputs and asserted patient count, a signed direction flip and negative model-based reference regret. Result: passed. This remains synthetic software validation, not a real-data experiment.

- Follow-up validation: added the latest 100-extra-cells patient-macro stress scenario to the isolated local report tests and reran the suite: **20 passed** in 1.19 seconds. The local `panel_shift_metrics.py` and metric tests match the repository blob hashes, but the local `panel_shift_report.py` and report-test copies do not match the latest repository blobs byte-for-byte; therefore this is not a claim that the exact current remote checkout was tested. A hosted GitHub Actions pass is still unverified.

## 25 October 2026 — cohort/checkpoint selection

- Selected the Salié et al. HCC IMC cohort pair: **54-patient discovery** cohort (Zenodo 10793609; CC BY 4.0 per the NLM Dataset Catalog) for development/calibration, and **42-patient ICI-treated** cohort (Zenodo 10794904) as a proposed untouched external evaluation.
- The 54-patient dataset is listed by the NLM Dataset Catalog as CC BY 4.0. For the 42-patient accession, the Zenodo landing page has a blank rights field, while OpenAIRE/Datacite-linked metadata for the exact DOI reports CC BY. The discrepancy is now a formal rights gate; preserve metadata evidence and confirm terms with the data contact/institutional office before redistribution if required.
- Selected official VirTues `virtues-imc14/model.safetensors` as the best *candidate* checkpoint. The official model table states it was trained on 14 IMC datasets and labels the weights CC BY-NC 4.0. VirTues' extended 32-cohort corpus adds seven extra IMC datasets, and the Salié study is reference 95 in that added group, so use `virtues-imc14` instead of `virtues-sp32`/`virtues-sp31` for the held-out design.
- Exposure confidence is **strong but not final**: model variant and published cohort grouping support exclusion, but the downloaded file's immutable revision/hash and accession-level exposure have not been checked. Pin the exact model revision, SHA-256, size, date and licence when downloaded; contact authors if exposure cannot be resolved from model metadata.
- The selected cohort has the right modality and relevant CD8/checkpoint immune architecture, but final intervention-marker list must be read from the actual panel CSVs. Morpheus target discovery has not been reproduced on HCC; this remains a separate compatibility gate.
- No cohort archives or model weights were downloaded. No checksum was computed and no inference was run.
- Created `docs/cohort_checkpoint_decision.md` with the locked development/test roles, checkpoint rationale, rights caveats and pre-inference checklist.

## 25 October 2026 — hosted CI dependency fix

- Inspected the GitHub Actions failure at commit `612acf98c486423be2df1bd3f4a72beb5da728b7`. The tests did not reveal a logic failure; four tests errored because the workflow's “minimal test dependencies” omitted **SciPy**, which pandas' Spearman correlation implementation imports at runtime (`ModuleNotFoundError: No module named 'scipy'`).
- Fixed `.github/workflows/tests.yml` to install `scipy` explicitly (commit `a04fcc072386f5fc7cd1ffda78238e1ed1a482a7`). The subsequent hosted GitHub Actions run **passed: 19 passed in 1.13 seconds**: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40196134743.
- Later commits in this decision pass changed documentation, CSV/YAML templates and audit notes, not Python analysis/test source. Follow-up Actions runs are triggered for the latest documentation commits; check the current run before treating the latest HEAD as CI-green.


## 25 October 2026 — checkpoint pinning workflow added

- Added `scripts/resolve_virtues_imc14_checkpoint.py` and `.github/workflows/resolve_virtues_imc14_checkpoint.yml`. The workflow downloads the official `virtues-imc14/model.safetensors` at the resolved immutable Hugging Face repository revision, computes SHA-256 and file size, and uploads only a JSON provenance manifest; the weights are not committed to GitHub.
- Workflow run was triggered on commit `d926c2d354ded6f95ba9b14d2b2115cf41115953`; final run outcome and actual hash are pending at the time of this note. Do not replace the revision/hash placeholder until the manifest is retrieved and checked.


## 25 October 2026 — checkpoint hash resolved

The checkpoint resolver workflow completed successfully: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40196348184. The hosted runner downloaded the official weight file and printed the following manifest values:

- File: `bunnelab/virtues/virtues-imc14/model.safetensors`
- Immutable repository revision: `43fd00fce052c46f9e0cc1a87f42806620632319`
- SHA-256: `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`
- Size: `173543728` bytes
- Retrieved at: `2026-10-25T13:10:07.676504+00:00` UTC
- Uploaded output: JSON provenance manifest only, artifact ID `12600630655`; no weight file committed to GitHub.

This pins the file for reproducible future loading. It does not verify exact cohort exposure from every training/fine-tuning source, does not resolve the 42-patient Zenodo licence display, and is not an inference run. The 54-patient development archive remains the only cohort with a directly supported CC BY 4.0 metadata record at this stage.


## 25 October 2026 — HCC archive audit diagnostic correction

- The first HCC archive audit failed after downloading and checksum-verifying the archive because it assumed a member named `DCCohort_panel.csv`; the actual ZIP did not contain that exact basename. This was an audit-script assumption, not evidence that the cohort itself is invalid.
- Updated `scripts/audit_salie_hcc_discovery_archive.py` to inventory every CSV member with its size, select the exact panel filename only when present or a unique small CSV filename containing `panel`, and emit a diagnostic report even when the panel is ambiguous or absent. It will not silently choose a non-unique candidate.
- The rerun is GitHub Actions run https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198072585. Do not call the cohort panel-compatible until that report identifies and parses the correct marker panel and the channel list is checked against the VirTues IMC14 input contract.


## 25 October 2026 — archive audit succeeded; artifact upload path defect isolated

- Hosted run [40198072585](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198072585) completed the download/integrity/panel inspection step successfully. Archive size: 1,541,132,381 bytes; actual MD5 matched expected `a842fa253ac2f0eda3cbf4d41e1b0ec1`; ZIP entries: 325; CSV inventory: one file, `DiscoveryCohort_panel.csv`; panel parsed successfully with 42 rows and columns `Channel`, `MetalTag`, `Target`.
- The workflow failed only at artifact upload: the configured path contained an escaped GitHub expression (`\\${{ runner.temp }}`) and became an invalid path beginning with a backslash. Corrected it to `${{ runner.temp }}/salie-hcc-discovery-audit.json`, matching the script's `$RUNNER_TEMP` output destination. A fresh run is required to confirm artifact publication.
- The audit's current Zenodo API response for record 10794904 reports `cc-by-4.0` with the license field present. Keep a note of the landing-page display discrepancy; do not describe legal review as complete based only on the API field.
- Panel-level caution: the panel contains CD8a, PD1, PD-L1, TIGIT, Tim3 and Lag3, but this does not automatically make the cohort compatible with Morpheus's counterfactual intervention set or prove the model's target-discovery objective transfers to HCC. Map target markers and cell-label/end-point definitions before inference.


## 25 October 2026 — corrected HCC audit workflow verified end-to-end

- Corrected workflow run [40198884781](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198884781) completed successfully, including the metadata-only artifact upload. Artifact: `salie-hcc-discovery-metadata-audit`, ID `12601036644`, expires 24 November 2026 UTC; artifact digest `sha256:91b9b9fc0dd3fe1fda5d488822e2f782ba156dd34710e2c8e5144a1a9e0e115d`.
- Downloaded and inspected the artifact JSON independently. It confirms archive integrity (`1541132381` bytes; MD5 `a842fa253ac2f0eda3cbf4d41e1b0ec1`), panel `DiscoveryCohort_panel.csv`, 42 parsed rows and columns `Channel`, `MetalTag`, `Target`. No raw images or masks are in the artifact.
- The current Zenodo API metadata for both records reports `cc-by-4.0` and a present license field. The 42-patient cohort remains metadata-only and was not downloaded. Keep the landing-page/API display discrepancy documented and re-check source terms before redistribution.
- The latest analysis-helper test check on commit `cd8bc5c524d21814979fdf3bff54a766b2b865f5` passed: [GitHub Actions test job](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40199745223/job/121188188741).
- Status is now **archive integrity + panel parsing + audit artifact publication verified**. Model preprocessing compatibility, model exposure, endpoint validity, baseline compatibility, inference and biological interpretation remain pending.


## 25 October 2026 — preprocessing contract blocks the selected model/data pairing

- Inspected the official VirTues dataset loader and model README. Its pipeline clips at per-tissue 99th percentiles, applies `log1p`, Gaussian blur, then per-tissue log-standardization using quantile/mean/std tables; channels are retained only when a canonical `protein_id` has a matching marker embedding.
- The verified HCC archive contains 324 TIFFs plus one CSV, with only `DC_img_normalized`, `DC_cellmasks` and `DC_stromamasks` directories. No raw-MCD/raw-intensity directory or VirTues per-tissue preprocessing-statistics tables were present. The Salié paper describes arcsinh transformation of raw channels with cofactor 0.5 for downstream analysis. This is not equivalent to VirTues' preprocessing.
- Decision changed from conditional pilot to **NO-GO for HCC-normalized-TIFF + VirTues inference** until compatible original-scale data/metadata are obtained or a different compatible model/dataset is chosen. Do not invert normalized TIFF values or apply the VirTues pipeline blindly.
- Added `docs/data_clarification_request_salie_hcc.md` with a draft author inquiry for original intensities, normalization provenance, channel mapping and cell phenotype labels; it has not been sent.
- Added `docs/next_execution_plan.md` with staged gates, an explicit alternative if raw data are unavailable, patient-level evaluation rules and go/no-go criteria.
- The research hypothesis remains plausible but unproven; no inference or biological result has been generated. The next meaningful action is resolving the input contract, not forcing a model run.

## 25 October 2026 — HCC archive audit and preprocessing/exposure decisions

### Completed archive and panel audit

- Successful final structural audit: [GitHub Actions run 40211055869](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40211055869), commit `15b3516f67b815b8f17a2d1d0ddc90d6e912f7e6`.
- Archive size 1,541,132,381 bytes equals Zenodo metadata; published MD5 `a842fa253ac2f0eda3cbf4d41e1b0ec1` matched; downloaded SHA-256 `8d09d946659164bb2275468ca4ad3239819b2036af83e63ab7b586ddbfc47f72`.
- ZIP inventory: 325 entries (324 TIFFs and one CSV). The actual panel is `DiscoveryCohort_panel.csv`, 42 rows, columns `Channel`, `MetalTag`, `Target`.
- Structural QC passed: required columns present, no blank required cells, no duplicated channel/metal-tag/target values, and channel numbers 1–42 are numeric and contiguous.
- Metadata-only artifact ID `12606106783`, SHA-256 digest `302d7a0bc55bbb32748185f97fa6e6b2110964dd56e7ec901371fc839bc452a3`; raw TIFFs/masks were not published as workflow artifacts or committed.
- Direct Zenodo API metadata reported `cc-by-4.0` for both records. The 42-patient ICI image archive was not downloaded.

### Preprocessing decision — resolved as a NO-GO for direct inference

The public HCC image stacks are PENGUIN-normalized to 0–1 with background removal and marker-specific percentile denoising per ROI. VirTues' official loader expects source-format intensity images and uses tissue-specific 99th-percentile clipping, `log1p`, Gaussian blur, and tissue-specific mean/SD standardization. No original acquisition files or matching VirTues quantile/mean/SD tables are in the discovery archive. Recomputing statistics from normalized TIFFs would produce a different representation; inversion is not justified. Do not send these TIFFs through the pretrained VirTues input path.

### Checkpoint exposure decision

The selected official checkpoint is `virtues-imc14/model.safetensors`, pinned at revision `43fd00fce052c46f9e0cc1a87f42806620632319`, SHA-256 `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`, 173,543,728 bytes. The VirTues Methods list the Salié HCC study as ref. 95 among seven IMC cohorts added to the extended corpus, while the checkpoint is the published core 14-IMC model. Therefore direct Salié-study exposure is not indicated for the core-14 checkpoint by the published corpus inventory; this remains reference-level evidence rather than a separate accession-to-training-job certificate. Do not use `virtues-sp32` for held-out HCC testing because it includes the HCC study. The precise cohort omitted from `virtues-sp31` was not verified, so do not use it for held-out HCC testing unless the released training inventory confirms Salié HCC is excluded.

### Scientific status and next gate

- HCC archive/panel structure: PASS.
- HCC public TIFFs + pretrained VirTues preprocessing: NO-GO.
- Core-14 checkpoint as outside direct Salié-study training corpus: supported by published corpus inventory, with provenance caveat.
- Cell labels, CD8 endpoint, marker embedding IDs, valid counterfactual baseline: unresolved.
- No real-data inference, target recommendations, clinical claims or biological validation have been produced.

Next actions: request the original compensated data, full image-normalization metadata, canonical panel/embedding mapping and cell phenotype annotations from the authors (draft only; not sent); otherwise select a verified compatible spora cohort with a checkpoint proven to exclude it.
