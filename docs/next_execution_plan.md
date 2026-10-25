# Next execution plan — decision gates and reproducible milestones

**Status date:** 25 October 2026  
**Current stage:** Discovery archive/panel audit complete; official-source-format VirTues reproduction is blocked because only PENGUIN-normalized HCC TIFFs are public. A separate normalized-domain adaptation pilot is now specified but not yet run.  
**Do not start full counterfactual inference until input adaptation, endpoint and marker mapping are validated.**

## Stage 0 — Preserve verified state

- Development archive: Zenodo 10793609; checksum `a842fa253ac2f0eda3cbf4d41e1b0ec1` verified.
- Actual panel file: `DiscoveryCohort_panel.csv`; 42 rows parsed.
- Latest enhanced metadata-only audit: [run 40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382), artifact [12607480794](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382/artifacts/12607480794). Sampled TIFF-storage QC is complete: image dtype/ranges, 42-page panel match and mask-grid alignment passed on checked samples. Do not commit the archive, images or masks.
- Checkpoint: `bunnelab/virtues/virtues-imc14/model.safetensors`, immutable model revision and SHA-256 recorded in `configs/panel_shift_pilot.example.yaml`.
- HCC/VirTues inference is blocked until compatible inputs are established; the existence of a pinned checkpoint does not make a dataset compatible.

## Stage 1 — Resolve data and model contract

1. Send the draft in `docs/data_clarification_request_salie_hcc.md` to the corresponding author or data curator, after adding the student's name/institution and obtaining supervisor approval if required.
2. Ask for raw/compensated intensity data, normalization provenance, channel order, per-ROI statistics and cell phenotype labels.
3. **Completed at storage-audit level:** sample TIFF series/page axes, channel count, pixel dtype/range and mask-grid alignment. Twelve image stacks were readable; sampled values were float32 and within [0,1]; sampled stack page counts matched the 42-row panel; paired mask shapes matched in three representative ROIs. This is representative sampling, not an exhaustive full-pixel scan, and it does not establish pretrained-model compatibility.
4. In parallel, inspect the exact VirTues inference notebook and pin the *code* commit separately from the weight revision.
5. Build a canonical channel table: image channel index, metal tag, panel target, canonical protein name, UniProt ID, embedding availability, transformation history, and any unresolved alias.
6. Do not infer raw intensity by inverting already-normalized TIFF values. If the source cannot provide compatible data, take Stage 1B instead.

### Stage 1A — If compatible original-scale data are available

- Create a minimal conversion for a single ROI, preserving the original channel order and all metadata.
- Verify conversion against a known-compatible official VirTues example.
- Run one masked-marker reconstruction; check output dimensions, finite values, spatial alignment, marker identity, and MAE/RMSE/correlation against the measured channel.
- Only proceed if the smoke test passes without hidden preprocessing assumptions.

### Stage 1B — If original-scale data are not available: normalized-domain feasibility pilot

- Do not claim direct reproduction of the official VirTues input pipeline. Use `docs/hcc_normalized_input_adaptation_protocol.md` to compare two explicitly labeled input transforms on PENGUIN-normalized discovery images.
- First verify the TIFF numeric storage encoding, stack axes/page count, panel/channel order and mask compatibility. Do not infer the pixel scaling factor from observed maxima alone.
- Use patient-grouped validation and entire-channel masking. Compare each transform with constant/mean-channel and best-correlated-marker baselines; use patient-macro metrics and patient-level uncertainty.
- Keep the 42-patient ICI cohort untouched until the transform, marker list, output-scale calibration and evaluation script are frozen. Do not tune on ICI results.
- If no transform beats baselines robustly, stop the HCC/VirTues pathway and select a permitted compatible spora cohort or a model trained/validated for PENGUIN-normalized data.
- If a cohort-specific model is trained, use patient-level splits and compare against simple baselines. Do not call it a foundation model or imply external generalization without evidence.
- Re-audit training exposure and licence terms for any replacement dataset/model before inference.

## Stage 2 — Lock the clinical/statistical estimand before model comparison

- Unit of splitting and inference: patient; all ROIs, cells, crops and tiles from a patient stay in the same fold.
- Primary reconstruction metric: patient-macro-averaged marker MAE/RMSE; correlation metrics are secondary and must handle constant channels explicitly.
- Primary downstream endpoint: only a documented or validated CD8 phenotype/infiltration definition. Cell/stroma masks alone are not CD8 labels.
- Counterfactual baseline: reproduce a published method or write and version a fully specified alternative before looking at test outputs.
- Eligible target markers and directions: pre-register a biologically justified list from the actual panel; do not equate every measured protein with a manipulable therapeutic target.
- Conditions: full measured reference, missing marker/no imputation, simple imputation, learned reconstruction. Compare on identical held-out patients.
- Primary decision-fidelity outcomes: signed target-set Jaccard/precision/recall, direction-flip rate, and patient-level model-predicted uplift fidelity. Clearly label these as agreement with a model reference, not causal effects.
- Uncertainty: patient-level paired bootstrap; report patient count, exclusions, confidence intervals and missingness pattern. Never bootstrap cells as if they were independent patients.

## Stage 3 — Novelty and reporting gate

Before drafting claims, update the prior-art table with the exact implemented estimand and all baselines. A possible contribution is whether virtual marker reconstruction preserves *signed counterfactual intervention recommendations* and *model-predicted objectives* under whole-channel missingness. Do not claim that this gap is novel, clinically useful, patentable or causal until the literature audit and experiments support those statements.

## Go/no-go criteria

**GO to normalized-domain pilot only when:** TIFF encoding/axes and channel order are verified; marker-to-UniProt/embedding mapping is complete for the candidate channels; the pinned checkpoint and licence are recorded; and the pilot uses patient-grouped splits and prespecified baselines.

**GO to the counterfactual pilot only when:** a normalized-domain reconstruction transform beats simple baselines on held-out patients, target output scale is calibrated without test-patient leakage, a defensible CD8 endpoint and eligible target set are locked, and a reproducible counterfactual baseline is implemented.

**GO to held-out evaluation only when:** the pilot passes, patient split is frozen, all comparison conditions are run on the same held-out patients, and no target/threshold/model selection uses test patients.

**NO-GO / redesign when:** the only available intensities cannot be reconciled with model preprocessing, canonical marker embeddings are missing, patient grouping cannot be reconstructed, cell labels do not support the endpoint, or the intervention baseline cannot be defined without circularity.
