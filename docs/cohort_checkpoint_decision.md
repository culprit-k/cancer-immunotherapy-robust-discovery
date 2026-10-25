# Cohort and checkpoint decision record — 25 October 2026

## Decision

**Selected biological study system:** Salié et al. hepatocellular carcinoma (HCC) imaging-mass-cytometry (IMC) dataset pair. The completed Zenodo API audit reports `cc-by-4.0` for both records, though the landing-page Rights display is blank. The 54-patient cohort is the development candidate; the 42-patient ICI cohort is a conditional external test. Data-format compatibility remains a blocker for pretrained VirTues inference.

- **Development cohort:** 54-patient HCC discovery cohort, Zenodo record [10793609](https://zenodo.org/records/10793609). The NLM Dataset Catalog reports CC BY 4.0 for this record. It includes preprocessed multichannel images and cell/stroma masks; channel annotations are in `DCCohort_panel.csv`.
- **Proposed external clinical-context test cohort (distinct clinical cohort; model-exposure gate still pending):** 42-patient HCC ICI-treatment cohort, Zenodo record [10794904](https://zenodo.org/records/10794904), DOI 10.5281/zenodo.10794904. The Zenodo landing page describes normalized channel-wise multi-stack TIFF images, cell masks, stromal masks and `ICICohort_panel.csv`; patient metadata are in Supplementary Table 3 of the associated paper. OpenAIRE/Datacite-linked metadata for this exact record reports **CC BY**, although the direct Zenodo “Rights / License” field is visually blank. The completed metadata-only API audit in [run 40210741291](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40210741291) also returned `cc-by-4.0` for this ICI record. Preserve that audit evidence; confirm with the data contact/institutional office if policy requires a license explicitly displayed on the landing page.
- **Published cohort paper:** Salié et al., *Gut* (2024/2025 issue), DOI [10.1136/gutjnl-2024-332837](https://doi.org/10.1136/gutjnl-2024-332837). It describes a 41-plex IMC panel and 54-person discovery plus 42-person ICI validation cohort; key immune phenotypes include CD8 T cells, PD-1-positive/exhausted CD8 T cells, TIM-3/LAG-3, PD-L1-positive myeloid/APC states, CD204 macrophages and HLA-DR-positive cells.

**Pinned foundation-model variant:** `bunnelab/virtues` — **`virtues-imc14/model.safetensors`**, the core-14 IMC checkpoint from the official [VirTues Hugging Face repository](https://huggingface.co/bunnelab/virtues), with matching official code at [bunnelab/virtues](https://github.com/bunnelab/virtues). Identity was frozen by [manifest run 40196348184](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40196348184).

Why this variant:
- The official model table identifies `virtues-imc14` as pretrained on 14 IMC datasets and assigns the **CC BY-NC 4.0 model-weight licence**.
- The VirTues paper distinguishes this core 14-IMC model from the extended 32-cohort corpus, which adds seven extra IMC cohorts (refs. 90–96) alongside non-IMC cohorts.
- The Salié HCC study is cited as ref. 95 in the VirTues paper, within the extended-corpus additions. Therefore the IMC-only 14-cohort checkpoint is the appropriate published variant to investigate for HCC evaluation; `virtues-sp32` and `virtues-sp31` are **not** acceptable independent checkpoints for this cohort because they use the extended multi-technology corpus that includes the Salié study.
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
| Exact model exposure | Exact `virtues-imc14` revision and SHA-256 are pinned; paper places Salié et al. (ref. 95) among extra IMC cohorts in the extended corpus, outside core 14. | Use `virtues-imc14` only for HCC held-out questions among the public variants; this is supported by the published inventory with a reference-level provenance caveat. Exclude `virtues-sp32`/`virtues-sp31`. |
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
- [ ] Inspect `DCCohort_panel.csv` and `ICICohort_panel.csv`; compare marker names, metal channels, image dimensions, masks and patient metadata.
- [ ] Convert channel-wise TIFFs and masks to the input structure required by official VirTues/spora code; preserve a reversible channel map and ROI/patient identity.
- [ ] Audit intensity ranges and existing normalization first. VirTues' published preprocessing includes clipping/log transform, tissue-aware channel normalization and Gaussian smoothing; do not double-transform data already normalized by the source study.
- [ ] Save an evidence copy of the CC BY metadata for the 54-patient cohort; resolve the 42-patient cohort's blank Zenodo license field with the data contact or institutional research office.
- [ ] Download only the official `virtues-imc14` weight artefact, read its licence, pin the exact immutable revision and record SHA-256. Do not use `virtues-sp32` or `virtues-sp31` for the primary held-out claim.
- [ ] Confirm model-training cohort inclusion/exclusion against the exact checkpoint version. Ask the authors if the public supplement/model card does not resolve accession-level exposure.
- [ ] Define an endpoint from cell labels/marker thresholds without using the withheld test data; pre-register eligible intervention markers from the panel CSV.
- [ ] Reproduce or justify the counterfactual baseline before interpreting output as target discovery.

## Scope and honest status

This establishes a **specific, scientifically compatible cohort pair and the most appropriate public checkpoint variant** based on available paper, repository and catalogue evidence. It does not mean data or weights have been downloaded, checksummed, model outputs generated, legal clearance formally issued, or zero exposure proven. No biological result exists yet. The first true-data milestone is a panel/metadata audit and one-channel reconstruction smoke test.


## Checkpoint pinning implementation

A small script, `scripts/resolve_virtues_imc14_checkpoint.py`, resolves the official Hugging Face repository's current immutable revision, downloads only `virtues-imc14/model.safetensors` to a temporary runner cache, computes file SHA-256/size and emits a JSON provenance manifest. The workflow `.github/workflows/resolve_virtues_imc14_checkpoint.yml` uploads only that manifest (not the model weights). Once the first run finishes, copy the exact revision and checksum into the study configuration and run log. This does not independently certify training exposure; it only makes the fetched artifact reproducible.


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

This resolves version pinning and file integrity for that retrieved copy. It does **not** by itself prove that the HCC accessions were absent from all pretraining/fine-tuning, does not clear the 42-patient dataset's source-level licence discrepancy, and does not mean inference has been run. Preserve the checksum/revision in all future runs; if the file is re-downloaded from a different revision, treat it as a different model.


## Actual discovery archive/panel audit — 25 October 2026

The first complete archive-inspection step has now run on a hosted GitHub Actions runner. Run [40198072585](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198072585) reports the archive's actual MD5 matching the expected value and identifies `DiscoveryCohort_panel.csv` (42 rows; columns `Channel`, `MetalTag`, `Target`). The raw archive remained in an ephemeral runner directory; only JSON diagnostics were printed to the job log. Artifact upload failed because the workflow path accidentally escaped the `${{ runner.temp }}` expression; the workflow has been corrected, and the rerun must verify successful artifact publication.

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

**Updated gate status:** archive integrity, panel parsing and metadata artifact publication are complete. Remaining gates are exact checkpoint exposure, VirTues input/normalization contract, endpoint and cell-label validity, pre-specified intervention/baseline compatibility, and a one-channel reconstruction smoke test. Do not claim a biological result or independent external validation yet.


## Additional blocking finding: image preprocessing contract

A source-code audit of the official VirTues dataset loader found that its documented path applies per-tissue 99th-percentile clipping, `log1p`, Gaussian blur and per-tissue log-standardization using quantile/mean/std tables; it also filters channels using canonical protein IDs with available marker embeddings. The Salié Zenodo HCC archive provides preprocessed/normalized TIFFs and panel labels only, and the source paper describes arcsinh transformation of raw channels for downstream analysis. Those transformations are not interchangeable. The archive does not advertise original MCD acquisitions or VirTues' per-tissue statistics.

Accordingly, the decision for the specific **HCC-normalized-TIFF + VirTues IMC14** pairing is now **NO-GO for inference** until raw/source data and required metadata are located and cleared, or a compatible dataset/model is selected. Do not reverse-engineer normalized values into raw intensities or apply the VirTues pipeline blindly. The HCC panel audit itself remains valid; only the assumed model/data compatibility has been rejected. See `docs/method_dataset_compatibility.md` for the exact gates and sources.
