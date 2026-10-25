# Next execution plan — decision gates and reproducible milestones

**Status date:** 25 October 2026  
**Current stage:** Archive/panel audit complete; selected HCC + VirTues pairing blocked by preprocessing contract.  
**Do not start full inference until the input contract and endpoint are defensible.**

## Stage 0 — Preserve verified state

- Development archive: Zenodo 10793609; checksum `a842fa253ac2f0eda3cbf4d41e1b0ec1` verified.
- Actual panel file: `DiscoveryCohort_panel.csv`; 42 rows parsed.
- Metadata-only audit artifact: run 40198884781, artifact 12601036644. Do not commit the archive, images or masks.
- Checkpoint: `bunnelab/virtues/virtues-imc14/model.safetensors`, immutable model revision and SHA-256 recorded in `configs/panel_shift_pilot.example.yaml`.
- HCC/VirTues inference is blocked until compatible inputs are established; the existence of a pinned checkpoint does not make a dataset compatible.

## Stage 1 — Resolve data and model contract

1. Send the draft in `docs/data_clarification_request_salie_hcc.md` to the corresponding author or data curator, after adding the student's name/institution and obtaining supervisor approval if required.
2. Ask for raw/compensated intensity data, normalization provenance, channel order, per-ROI statistics and cell phenotype labels.
3. In parallel, inspect the exact VirTues inference notebook and pin the *code* commit separately from the weight revision.
4. Build a canonical channel table: image channel index, metal tag, panel target, canonical protein name, UniProt ID, embedding availability, transformation history, and any unresolved alias.
5. Do not infer raw intensity by inverting already-normalized TIFF values. If the source cannot provide compatible data, take Stage 1B instead.

### Stage 1A — If compatible original-scale data are available

- Create a minimal conversion for a single ROI, preserving the original channel order and all metadata.
- Verify conversion against a known-compatible official VirTues example.
- Run one masked-marker reconstruction; check output dimensions, finite values, spatial alignment, marker identity, and MAE/RMSE/correlation against the measured channel.
- Only proceed if the smoke test passes without hidden preprocessing assumptions.

### Stage 1B — If compatible original-scale data are not available

- Stop the VirTues/HCC pairing.
- Select a reconstruction model that explicitly accepts the released normalized representation, or select a permitted independent dataset with raw/original-scale images and complete channel metadata.
- If a cohort-specific model is trained, use patient-level splits and compare against simple baselines. Do not call it a foundation model or imply external generalization without evidence.
- Re-audit training exposure and license terms for any replacement dataset/model before download or inference.

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

**GO to pilot only when:** input contract is documented; panel-to-UniProt mapping is complete; checkpoint code/weights are pinned; exposure is screened; endpoint and baseline are locked; and one-channel reconstruction passes a sanity check.

**GO to held-out evaluation only when:** the pilot passes, patient split is frozen, all comparison conditions are run on the same held-out patients, and no target/threshold/model selection uses test patients.

**NO-GO / redesign when:** the only available intensities cannot be reconciled with model preprocessing, canonical marker embeddings are missing, patient grouping cannot be reconstructed, cell labels do not support the endpoint, or the intervention baseline cannot be defined without circularity.
