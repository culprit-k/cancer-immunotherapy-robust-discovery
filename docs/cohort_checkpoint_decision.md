# Cohort and checkpoint decision record — 25 October 2026

## Decision

**Selected biological study system:** Salié et al. hepatocellular carcinoma (HCC) imaging-mass-cytometry (IMC) dataset pair. The completed Zenodo API audit reports `cc-by-4.0` for both records, though the landing-page Rights display is blank. The 54-patient cohort is the development candidate; the 42-patient ICI cohort is a conditional external test. Data-format compatibility remains a blocker for pretrained VirTues inference.

- **Development cohort:** 54-patient HCC discovery cohort, Zenodo record [10793609](https://zenodo.org/records/10793609). The NLM Dataset Catalog reports CC BY 4.0 for this record. It includes preprocessed multichannel images and cell/stroma masks; channel annotations are in `DCCohort_panel.csv`.
- **Proposed external clinical-context test cohort (different patient cohort; model-exposure assessed at publication level):** 42-patient HCC ICI-treatment cohort, Zenodo record [10794904](https://zenodo.org/records/10794904). The archive contains normalized TIFFs and masks; patient metadata are in Supplementary Table 3. The completed Zenodo API audit [run 40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382) returned `cc-by-4.0` for this record. Its image archive was not downloaded. Preserve the metadata-only evidence and confirm with the data contact/institutional office if local policy requires an explicit landing-page licence display.
- **Published cohort paper:** Salié et al., *Gut* (2024/2025 issue), DOI [10.1136/gutjnl-2024-332837](https://doi.org/10.1136/gutjnl-2024-332837). It describes a 41-plex IMC panel and 54-person discovery plus 42-person ICI validation cohort; key immune phenotypes include CD8 T cells, PD-1-positive/exhausted CD8 T cells, TIM-3/LAG-3, PD-L1-positive myeloid/APC states, CD204 macrophages and HLA-DR-positive cells.

**Pinned foundation-model variant:** `bunnelab/virtues` — **`virtues-imc14/model.safetensors`**, the core-14 IMC checkpoint from the official [VirTues Hugging Face repository](https://huggingface.co/bunnelab/virtues), with matching official code at [bunnelab/virtues](https://github.com/bunnelab/virtues). Identity was frozen by [manifest run 40196348184](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40196348184).

Why this variant:
- The official model table identifies `virtues-imc14` as pretrained on 14 IMC datasets and assigns the **CC BY-NC 4.0 model-weight licence**.
- The VirTues paper distinguishes this core 14-IMC model from the extended 32-cohort corpus, which adds seven extra IMC cohorts (refs. 90–96) alongside non-IMC cohorts.
- The Salié HCC study is cited as ref. 95 among IMC datasets added to the extended corpus. Therefore `virtues-imc14` is the appropriate published variant for HCC exposure separation. `virtues-sp32` includes the extended corpus and is **not** an independent checkpoint for HCC. `virtues-sp31` is listed as a 31-cohort variant, but the exact omitted cohort was not verified here; do not use it for an HCC-held-out claim until its training inventory confirms Salié HCC is excluded.
- Publication-level training-corpus comparison supports no direct Salié-study inclusion in the pinned core-14 checkpoint: the HCC study is reference 95 in the seven extra IMC cohorts added only to the extended 32-cohort corpus. The checkpoint revision, file SHA-256 and size are now pinned. No signed author statement or machine-readable accession-to-training-run certificate was located, so describe this as exclusion supported by the published corpus inventory rather than an independently certified training-log audit.

## Compatibility rationale

| Requirement | Evidence / status | Decision |
|---|---|---|
| Cancer and immune-oncology relevance | HCC, spatial immune architecture and ICI-treatment outcomes in the linked 42-patient cohort. | Strong fit. |
| Spatial protein channels | IMC panel; released TIFFs are PENGUIN-normalized to 0–1 per ROI/channel. | **Direct pretrained VirTues inference is NO-GO.** Its documented clip/log/blur/tissue-statistic standardization pipeline does not match the published released TIFF representation. Do not invert or invent statistics. |
| Cell/tissue geometry | Cell masks and stroma masks are included in the released archives. | Potentially useful, but masks alone do not validate cell phenotypes. Conversion to spora layout would not solve the normalized-intensity mismatch; original-scale inputs or a separately validated model adaptation is required. |
| CD8 objective | The article analyzes CD8 T-cell infiltration and CD8/checkpoint-positive immune states. | Potential endpoint. Need a reproducible cell-label / threshold definition before analysis. |
| Candidate intervention targets | Article reports PD-1, TIM-3/LAG-3, PD-L1-positive APC/myeloid states, CD204 macrophages and other immune markers. | Provisional biological shortlist only; final allowed target markers must be read from the actual panel CSV and fixed before test evaluation. Never manipulate the CD8 endpoint marker to predict CD8 density. |
| Dataset rights | The CI audit queried Zenodo API metadata for both records and received `cc-by-4.0`; landing pages do not visibly display the licence. | Record-level metadata supports attribution-based reuse; retain the API audit and confirm with the study team/institutional office if policy requires the landing-page display. |
| Foundation-model weights | `virtues-imc14` CC BY-NC 4.0. | Suitable for non-commercial academic research with attribution and compliance; **not suitable for commercial use without separate permission/licensing**. Do not assume the MIT code licence applies to the weights. |
| Exact model exposure | Exact `virtues-imc14` revision and SHA-256 are pinned; paper places Salié et al. (ref. 95) among extra IMC cohorts in the extended corpus, outside core 14. | Publication-level evidence supports no direct Salié-study exposure for `virtues-imc14`; retain the reference-level caveat. `virtues-sp32` is exposed; `virtues-sp31` requires exact omitted-cohort verification. |
| Exact counterfactual baseline compatibility | Morpheus was developed for other tumour cohorts and its original target-prediction pipeline has not been reproduced on HCC. | Not yet established. Validate panel and endpoint first; reproduce/adapt with pre-specified rules, and label any adapted method as an adaptation rather than a direct reproduction. |

## Locked analysis roles

1. **Development / method calibration:** 54-patient discovery cohort (Zenodo 10793609), patient-level splits only. Use this cohort to settle image preprocessing, panel-to-marker mapping, endpoint definition, masking cases and validation-calibrated thresholds.
2. **External evaluation:** 42-patient ICI cohort (Zenodo 10794904), untouched until the pipeline, target budget, marker shortlist, threshold and reliability/abstention rule are frozen. Do not tune on this test cohort.
3. **Reconstruction checkpoint:** freeze `virtues-imc14` at revision `43fd00fce052c46f9e0cc1a87f42806620632319`, SHA-256 `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`, file size 173543728 bytes, retrieval time 2026-10-25T13:10:07.676504+00:00; do not substitute later weights. Published training-corpus evidence supports no direct Salié-study inclusion. The remaining caveat is that no separate accession-to-training-run certificate was located; cite the paper's core-versus-extended corpus distinction rather than implying access to internal training logs.
4. **Evaluation unit:** patient. All ROIs/images from a patient must remain in one split. Never treat cells, tiles or ROIs as independent patients.
5. **Primary output:** signed intervention recommendation fidelity (marker identity plus increase/decrease direction) and patient-level change in the model-predicted CD8 objective between full-panel and reconstructed-panel runs. Full-panel output is a model reference, not biological ground truth. Predicted change is not a demonstrated treatment effect.

## Go/no-go checklist before actual inference

- [ ] Download the 54-patient and 42-patient archives from their official records; store outside the public GitHub repository.
- [ ] Verify archive integrity against source checksums and record new SHA-256 values locally.
- [ ] Inspect the actual `DiscoveryCohort_panel.csv` from the audited discovery ZIP and `ICICohort_panel.csv` in the not-yet-downloaded ICI archive; compare marker names, metal channels, image dimensions, masks and patient metadata.
- [ ] Obtain or recover an input representation and the required per-tissue preprocessing statistics compatible with VirTues; directory/layout conversion alone is insufficient. If those inputs cannot be obtained, select a compatible cohort/model or pre-specify a separate HCC-specific adaptation. Preserve channel order and ROI/patient identities.
- [x] Audit stored intensity ranges and published normalization. Sampled float32 pixels are within [0,1] as expected for PENGUIN-normalized images. These values do not reverse the transformation; direct VirTues inference remains NO-GO.
- [x] Save the metadata-only Zenodo API audit evidence for both HCC accessions; it reports `cc-by-4.0` for each. The ICI image archive remains undownloaded; confirm landing-page display with the data contact/institution if needed.
- [x] Pin the official `virtues-imc14` weight artefact, revision, SHA-256, size and licence (provenance manifest generated and verified).
- [x] Compare the published core-versus-extended training inventory; Salié ref. 95 appears in added IMC cohorts beyond the core-14 model.
- [x] Complete sparse TIFF structure and pixel-range audit: 12 evenly spaced image stacks readable, sample image pages float32 and within [0,1], 42 pages match the panel, and image/mask spatial shapes matched in the three checked ROIs. This is representative sampling, not a full pixel-by-pixel scan.
- [ ] Request original-scale HCC data and preprocessing metadata; draft request is prepared but not sent.
- [ ] If original-scale data are unavailable, execute the normalized-domain adaptation pilot and compare transforms on patient-held-out measured-marker reconstruction. Do not call this official VirTues preprocessing reproduction.
- [ ] `virtues-sp32` is unsuitable for held-out HCC; `virtues-sp31` requires verification of its omitted cohort.
- [x] Compare the exact pinned checkpoint's published training-corpus description with the source paper: Salié et al. (ref. 95) is among extended-corpus IMC additions, outside core-14 `virtues-imc14`. This is publication-level evidence, not an accession-to-training-job certificate.
- [ ] Define an endpoint from cell labels/marker thresholds without using the withheld test data; pre-register eligible intervention markers from the panel CSV.
- [ ] Reproduce or justify the counterfactual baseline before interpreting output as target discovery.

## Scope and honest status

This establishes a scientifically relevant cohort pair, a completed discovery archive audit, a pinned model file, and a documented preprocessing NO-GO. It does not mean the public HCC TIFFs can be run directly through pretrained VirTues, that formal legal clearance has been issued, or that biological results exist. The next milestone is either (A) author-supplied original-scale input plus an official-pipeline smoke test, or (B) a separately labeled PENGUIN-normalized-domain pilot under `docs/hcc_normalized_input_adaptation_protocol.md`. Route B is not claimed to reproduce official VirTues preprocessing; it must pass patient-held-out reconstruction tests against simple baselines before counterfactual analysis.


## Checkpoint pinning implementation

A small script, `scripts/resolve_virtues_imc14_checkpoint.py`, now defaults to the audited immutable revision `43fd00fce052c46f9e0cc1a87f42806620632319`, downloads only `virtues-imc14/model.safetensors` to a temporary runner cache, computes file SHA-256/size and emits a JSON provenance manifest. The workflow `.github/workflows/resolve_virtues_imc14_checkpoint.yml` uploads only that manifest (not the model weights). The checkpoint manifest is published at [run 40212033753](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40212033753). This ensures file reproducibility; cohort exposure assessment relies separately on the published core-versus-extended corpus description.


## Retrieved checkpoint provenance — verified 25 October 2026

The official checkpoint was downloaded on an ephemeral GitHub Actions runner from the official Hugging Face repository at the immutable revision returned by the Hugging Face API. The script calculated the SHA-256 of the actual downloaded weight file. **The 173,543,728-byte model file itself was not committed to the public GitHub repository; only the JSON provenance manifest was uploaded as an Actions artifact.**

- Repository/file: `bunnelab/virtues` / `virtues-imc14/model.safetensors`
- Immutable repository revision: `43fd00fce052c46f9e0cc1a87f42806620632319`
- Weight-file SHA-256: `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`
- File size: `173543728` bytes
- Retrieved timestamp: `2026-10-25T13:10:07.676504+00:00`
- Successful resolver workflow: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40196348184
- Manifest artifact: `virtues-imc14-checkpoint-manifest` (artifact ID `12600630655`; expires 24 November 2026 UTC)
- Hashing procedure: `scripts/resolve_virtues_imc14_checkpoint.py`

This resolves version pinning and file integrity for the retrieved copy. It does not replace the published training-corpus review, establish an accession-to-training-job certificate, and does not mean inference has been run. The Zenodo API metadata audit found `cc-by-4.0` on both records; no images from the ICI cohort were downloaded.


## Actual discovery archive/panel audit — 25 October 2026

Historical note: the first archive-inspection run [40198072585](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198072585) identified the correct archive and panel but had an artifact upload issue. This was subsequently fixed and superseded by the successful structural audit [run 40211055869](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40211055869), whose metadata-only artifact is published and whose panel structural QC passed.

The 42-patient ICI cohort's current Zenodo API metadata reports `cc-by-4.0` and a present license field, though the previously observed blank landing-page display should be reconciled in the rights log before redistribution or external evaluation.

The development panel includes CD8a, PD1, PD-L1, TIGIT, Tim3 and Lag3. This is relevant immune/checkpoint coverage, but not yet proof that the Morpheus intervention targets and objective are available or compatible. The cohort remains **pre-inference**, pending a marker crosswalk, input/preprocessing contract, cell-label/endpoint audit, and exposure/rights documentation.


## Intervention-marker compatibility crosswalk — checked 25 October 2026

A direct comparison against the published Morpheus target sets shows that the HCC discovery panel is **not a drop-in replication cohort for the original Morpheus target-discovery experiment**:

| Published Morpheus cancer setting | Reported intervention targets | Present in HCC discovery panel? |
|---|---|---|
| Melanoma | CXCL9, CXCL10, CCL22, CCL18 | None of these four is listed in the 42-row HCC panel |
| Colorectal cancer liver metastases | CXCR4, PD-1, PD-L1, CYR61 | PD-1 and PD-L1 are present; CXCR4 and CYR61 are absent |

The HCC panel does contain CD8a and multiple checkpoint/immune-state markers, including PD1, PD-L1, TIGIT, Tim3, Lag3, CD4, CD3 and GranzymeB. That supports a **restricted, pre-specified checkpoint-marker exploratory question**, but does not justify claiming the original Morpheus target set can be reproduced or validated on this cohort. Do not substitute other markers post hoc and call them the same intervention.

**Decision gate:** before model inference, choose and justify one of two routes:
1. Narrow the study to a clearly labeled *checkpoint-marker decision-fidelity adaptation* (e.g. a fixed eligible subset of measured markers), with the endpoint and perturbation semantics explicitly redefined and all limits reported; or
2. Select a different licensed spatial-proteomics cohort that measures the relevant Morpheus target channels, and separately verify that the frozen imputer did not train on it.

Whichever route is chosen, keep CD8a out of predictor inputs where required to prevent label leakage, define a cell-/patch-level CD8 endpoint using documented masks/annotations, and distinguish marker reconstruction from a biologically actionable intervention. A virtual change in measured intensity is not equivalent to a drug perturbation or causal therapeutic effect.

This crosswalk is based on the published Morpheus reported target sets and the parsed `DiscoveryCohort_panel.csv`; it is a compatibility screen, not model validation.


## End-to-end audit outcome — 25 October 2026

The corrected audit workflow passed end-to-end in [run 40198884781](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198884781). Its metadata-only artifact (ID `12601036644`) was downloaded and inspected. It confirms a matching archive MD5, the actual panel filename `DiscoveryCohort_panel.csv`, 42 parsed marker rows and `cc-by-4.0` in the direct Zenodo API metadata for both the development and proposed ICI records. The external ICI images were not downloaded. This resolves the archive/panel discovery and artifact-upload blockers, not model/data compatibility or legal review.

**Updated gate status:** discovery archive integrity/panel QC and checkpoint file identity are complete. Direct pretrained inference on released HCC TIFFs is NO-GO because preprocessing domains differ. Published-corpus evidence supports using `virtues-imc14` as outside direct Salié-study exposure, with the reference-level provenance caveat. Remaining gates are original-scale compatible inputs (or a compatible alternative cohort), canonical marker mapping, validated cell labels/CD8 endpoint, and counterfactual baseline compatibility. No biological result or actual independent external validation has been produced.


## Additional blocking finding: image preprocessing contract

A source-code audit of the official VirTues dataset loader found that its documented path applies per-tissue 99th-percentile clipping, `log1p`, Gaussian blur and per-tissue log-standardization using quantile/mean/std tables; it also filters channels using canonical protein IDs with available marker embeddings. The Salié Zenodo HCC archive provides preprocessed/normalized TIFFs and panel labels only, and the source paper describes arcsinh transformation of raw channels for downstream analysis. Those transformations are not interchangeable. The archive does not advertise original MCD acquisitions or VirTues' per-tissue statistics.

Accordingly, the decision for the specific **HCC-normalized-TIFF + VirTues IMC14** pairing is now **NO-GO for inference** until raw/source data and required metadata are located and cleared, or a compatible dataset/model is selected. Do not reverse-engineer normalized values into raw intensities or apply the VirTues pipeline blindly. The HCC panel audit itself remains valid; only the assumed model/data compatibility has been rejected. See `docs/method_dataset_compatibility.md` for the exact gates and sources.
