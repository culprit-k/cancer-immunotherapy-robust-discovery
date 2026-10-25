# HCC preprocessing and VirTues checkpoint-exposure decision

**Decision date:** 25 October 2026  
**Scope:** Public Salié HCC discovery and ICI IMC archives versus the pinned official VirTues IMC-only checkpoint.  
**Outcome:** HCC archive/panel audit **PASS**; direct inference on the released normalized HCC TIFFs **NO-GO**; direct pretraining exposure of the pinned IMC-only checkpoint is **not supported by the published training-corpus inventory** (strong publication-level exclusion; no separate accession-by-accession author certificate located).

## 1. Completed archive audit

The successful enhanced archive/TIFF audit is GitHub Actions run [40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382), on commit `a13476ac1d7ddf4d663d8ce9d3afcdaf55049bbc`. The follow-up run [40215732626](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40215732626) re-runs the same audit with more precise sample-scope wording.

- Discovery archive: `HCC_DiscoveryCohort.zip`, Zenodo DOI [10.5281/zenodo.10793609](https://zenodo.org/records/10793609).
- Downloaded size: **1,541,132,381 bytes**, matching the size advertised by Zenodo.
- MD5: **a842fa253ac2f0eda3cbf4d41e1b0ec1**, matching the published archive checksum.
- SHA-256: **8d09d946659164bb2275468ca4ad3239819b2036af83e63ab7b586ddbfc47f72**.
- ZIP inventory: **325 entries**, comprising 324 TIFFs and one CSV. The relevant top-level directories are `DC_img_normalized`, `DC_cellmasks`, and `DC_stromamasks`.
- Panel CSV actually contained in the archive: `DiscoveryCohort_panel.csv`; the Zenodo descriptive text names `DCCohort_panel.csv`.
- Parsed panel: 42 rows, with `Channel`, `MetalTag`, and `Target` columns.
- Structural QC: required columns present; no blank required cells; no duplicate channel numbers, metal tags, or target names; channels are numeric and contiguous from 1 to 42. **`structural_qc_pass = true`.**
- The workflow published metadata-only artifact [12607480794](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382/artifacts/12607480794), digest `sha256:40cbe02a0e40939354bd1acacba177303321cee934b146f23de23fbc6502d282`, expiring 24 November 2026 UTC. No pixel arrays or full image data are in this artifact.
- Raw images and masks were not committed or uploaded as artifacts.
- The direct Zenodo API metadata retrieved during the same run reported `cc-by-4.0` for both Zenodo records 10793609 and 10794904. The ICI image archive was **not** downloaded in this audit; the API check was metadata-only.

This is a completed archive-integrity, panel-structure, and sampled TIFF-storage audit. It establishes actual stored pixel ranges and sampled image/mask grid compatibility, but does not recover raw acquisition intensities, prove VirTues input compatibility, validate cell labels/biology, or certify checkpoint exposure from internal training logs.

## 2. Sampled TIFF storage QC: PASS

The enhanced workflow inventories 108 TIFFs in each of `DC_img_normalized`, `DC_cellmasks`, and `DC_stromamasks` (324 total). It audits panel structure and uses deterministic sparse samples for image/mask inspection:

- Twelve evenly spaced normalized image stacks were readable; the sampled image series use `float32` storage and 42 pages/channels, matching the 42-row marker panel.
- Sampled image-stack dimensions included `(42, 1300, 1300)` and `(42, 1500, 1500)`. The varying ROI sizes should be preserved in the ROI crosswalk; it is not evidence of a mismatch by itself.
- Pixel statistics were collected from first/middle/last pages across the sampled image stacks, and all 42 pages were read for three representative ROIs (126 planes total). Across these sampled planes, all stored pixel values were finite and within `[0, 1]` (observed minimum `0.0`, maximum `1.0`; no out-of-range pixels in those samples).
- For the first/middle/last representative ROIs, corresponding cell-mask and stroma-mask files were present and spatial dimensions matched the normalized image grid (3/3 each, no mismatch or read error). Sampled mask stacks were stored as `uint16`.

**Scope limitation:** inventory counts cover all TIFF members, but detailed series/page metadata and numeric pixel summaries are sampled, not a full pixel-by-pixel scan of all 108 image stacks. These results confirm that the sampled TIFFs are stored as normalized float images, consistent with the published PENGUIN normalization; they do not reveal or permit inversion to the original intensity scale.

## 3. Preprocessing contract: incompatible as released

### What the HCC public files are

The Zenodo records describe the image stacks as already preprocessed and normalized. The Salié paper's Methods specify PENGUIN channel normalization to values between **0 and 1**, background removal, and percentile-based noise reduction. Channel parameters were selected separately by manual inspection and applied to every ROI. The public archive contains normalized TIFFs and masks, not original MCD acquisitions or an accompanying per-image/per-channel VirTues quantile/mean/standard-deviation table.

Sources:

- [Salié HCC discovery data record](https://zenodo.org/records/10793609)
- [Salié et al., Gut Methods / full text](https://gut.bmj.com/content/early/2024/09/30/gutjnl-2024-332837?versioned=true)
- [Salié HCC ICI data record](https://zenodo.org/records/10794904)

The article also mentions arcsinh cofactor 0.5 for certain downstream analysis of raw channels. That statement must not be misread as the transformation that produced the public normalized TIFFs: the Methods separately specify PENGUIN normalization for the image channels. We must not apply arcsinh, invert PENGUIN normalization, or infer raw intensities from these released TIFFs.

### What VirTues expects

The official VirTues loader `virtues/data/multiplex_dataset.py` expects numeric image arrays plus:
- a channel table with `protein_id` values mapped to available marker embeddings;
- per-tissue/per-channel 99th-percentile quantiles for clipping;
- per-tissue/per-channel mean and standard deviation values for standardization;
- tissue segmentation masks defining the area for these statistics.

Its preprocessing, in order, is: clamp each channel at its tissue-specific 99th percentile; apply `log1p`; Gaussian blur with kernel 3 and unit sigma; standardize using the stored tissue-specific mean and standard deviation. The paper describes the percentiles and the means/standard deviations as computed from the training-format images using tissue masks.

Sources:

- [Official VirTues repository and data-format instructions](https://github.com/bunnelab/virtues)
- [VirTues Nature paper, Methods—dataset preprocessing](https://www.nature.com/articles/s41586-026-10884-y), especially the dataset/preprocessing/model-instance discussion.

### Decision

**NO-GO: do not run the pretrained VirTues checkpoint directly on the public HCC normalized TIFF stacks.** Recomputing statistics from the normalized pixels and feeding those outputs to the existing checkpoint is not equivalent to the published training pipeline. Reapplying the original pipeline without the original representation also does not reverse or restore it. An image-level smoke test would merely prove that tensors can pass through code, not that the input distribution is valid.

There are only two scientifically defensible routes:
1. Obtain original compensated intensity data and sufficient channel/tissue metadata from the study team, then implement the official data contract and verify a one-image smoke test.
2. Switch to a cohort already distributed in the official VirTues/spora format, and independently verify its source licence, patient identifiers, labels, and checkpoint training exposure.

A new model trained explicitly on normalized HCC images is a different study design, not a fix that makes the published pretrained VirTues checkpoint compatible.

## 4. Checkpoint identity and cohort-exposure finding

Pinned artifact:
- Repository: `bunnelab/virtues`
- File: `virtues-imc14/model.safetensors`
- Immutable Hugging Face revision: `43fd00fce052c46f9e0cc1a87f42806620632319`
- SHA-256: `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`
- Size: `173543728` bytes
- Weight licence published by VirTues: **CC BY-NC 4.0** (non-commercial research only, unless separate permission is obtained).
- Reproducibility manifest run: [40196348184](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40196348184), artifact ID `12600630655`.

### What the published training inventory supports

The VirTues paper states that:
- the IMC-only core corpus contains **14 datasets**;
- the extended 32-cohort corpus adds seven more IMC datasets, citing references 90–96, plus CODEX, Orion and MIBI cohorts;
- the Salié HCC study is reference **95**;
- the `virtues-imc14` model is the IMC-only core-14 model; `virtues-sp32` uses the extended 32-cohort multi-technology corpus, which includes Salié et al. (ref. 95). `virtues-sp31` is described as a 31-cohort model, but its exact omitted cohort was not verified in this audit.

Therefore, the published corpus grouping supports **no direct inclusion of the Salié HCC study in the standard core-14 `virtues-imc14` training set**. The study appears in the seven extra IMC cohorts used for the extended corpus, so `virtues-sp32` must not be used for a held-out HCC claim. Do not use `virtues-sp31` for a held-out HCC claim unless its exact training inventory confirms that Salié HCC is absent.

This is substantially stronger than the prior “exposure unknown” status and resolves the practical model selection: **`virtues-imc14` is the one public variant whose published core-14 training inventory supports assessment of HCC outside its training corpus.** The multi-technology `virtues-sp32` is exposed to Salié HCC; `virtues-sp31` remains unapproved for HCC-held-out use until its omitted dataset is confirmed. The official paper describes leave-one-dataset-out variants for selected core-14 cohorts (references 2, 6, 8, 42 and 48), not a special HCC-excluded variant; such a special HCC variant is unnecessary if the published core/extended corpus distinction applies to the pinned weights.

Caveat: the public paper/model card provides corpus-level, reference-level provenance rather than a machine-readable certificate mapping each Zenodo accession to every training job. We did not find a separate signed author statement confirming both accessions were excluded from the exact weight hash. In a manuscript, describe this as “the pinned core-14 checkpoint was selected because the published training inventory places Salié et al. in the extended corpus, not the core-14 corpus,” and retain the citation/hash. Do not claim independently audited row-level provenance beyond that evidence.

Source: [VirTues Nature paper, datasets and model instances](https://www.nature.com/articles/s41586-026-10884-y), Methods sections “Dataset curation” and “VirTues model instances”; [official source repository](https://github.com/bunnelab/virtues).

## 5. Final gate table

| Gate | Result | Meaning |
|---|---|---|
| Discovery archive integrity | **PASS** | Published MD5 and size match; SHA-256 recorded. |
| Panel table structure | **PASS** | 42 channel rows; no required-field blanks or duplicates; channel sequence is valid. |
| Public TIFF intensity representation | **PENGUIN-normalized, 0–1** | Preprocessed values, not the original model-input scale. |
| Direct HCC TIFF → pretrained VirTues inference | **NO-GO** | Input contract/distribution mismatch; do not invert or invent statistics. |
| `virtues-imc14` direct HCC training exposure | **Excluded by published corpus grouping** | Good published evidence for no direct Salié-study exposure; keep the provenance caveat above. |
| `virtues-sp32` exposure | **NO-GO for held-out HCC testing** | Its full extended corpus includes Salié ref. 95. |
| `virtues-sp31` exposure | **Unresolved; not approved for held-out HCC testing** | The release states 31 cohorts, but this audit did not verify which one is omitted. |
| Cell labels / CD8 endpoint | **OPEN** | Cell/stroma masks do not by themselves establish cell-type labels or a validated endpoint. |
| Real model inference / biological conclusions | **NOT RUN** | No reconstruction or counterfactual results can be reported. |

## 6. Next action

Use the unsent draft in `docs/data_clarification_request_salie_hcc.md` to request original compensated intensities, the exact PENGUIN parameters, authoritative panel/channel ordering and cell phenotype labels. If original inputs cannot be obtained, pivot to a verified spora-compatible cohort while keeping the study question and decision-level evaluation metrics. No external email has been sent.
