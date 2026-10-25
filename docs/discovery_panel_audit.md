# Salié HCC discovery panel audit

**Audit date:** 25 October 2026  
**Source:** [Zenodo record 10793609](https://zenodo.org/records/10793609)  
**Latest verified audit:** GitHub Actions run [40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382)  
**Status:** Archive integrity and panel structural QC verified PASS; direct VirTues inference on these normalized TIFFs is NO-GO. Checkpoint exposure is assessed in [the HCC preprocessing/exposure decision](hcc_preprocessing_and_checkpoint_exposure_decision_2026-10-25.md).

## Integrity and panel parsing

- Archive: `HCC_DiscoveryCohort.zip`
- Downloaded size: 1,541,132,381 bytes
- Expected and observed MD5: `a842fa253ac2f0eda3cbf4d41e1b0ec1` (match)
- ZIP entries: 325 (324 TIFFs and one CSV)
- Top-level image/mask directories: `DC_img_normalized`, `DC_cellmasks`, `DC_stromamasks`; no raw-MCD/raw-intensity directory or per-tissue quantile/mean/std tables were present in this archive.
- Actual panel member: `DiscoveryCohort_panel.csv` (not the `DCCohort_panel.csv` filename described in the record text)
- Parsed panel: 42 rows; columns `Channel`, `MetalTag`, `Target`
- Raw images and masks were not committed or uploaded. The completed enhanced audit is [GitHub Actions run 40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382); metadata-only artifact ID `12607480794`, digest `sha256:40cbe02a0e40939354bd1acacba177303321cee934b146f23de23fbc6502d282`, expires 24 November 2026 UTC.
- SHA-256 of the downloaded archive: `8d09d946659164bb2275468ca4ad3239819b2036af83e63ab7b586ddbfc47f72`.

## Sampled TIFF storage audit

The workflow counted 108 TIFFs in each of `DC_img_normalized`, `DC_cellmasks`, and `DC_stromamasks`. It sampled 12 evenly spaced image stacks, all readable, and read first/middle/last pages for their scalar pixel summaries. It also read all 42 pages/channels from three representative ROIs (126 planes).

- Sampled image stack dtype: `float32`; sampled stack shape examples: `(42, 1300, 1300)` and `(42, 1500, 1500)`. The differing ROI dimensions must be preserved in the spatial crosswalk.
- Sampled pages have observed minimum `0.0` and maximum `1.0`; all sampled values were finite and within `[0,1]`.
- The corresponding cell-mask and stroma-mask TIFFs were present for the three representative ROIs; spatial dimensions matched in all checks (3/3 per mask directory), with mask storage observed as `uint16`.
- Scope limitation: this is sparse TIFF QC, not an exhaustive pixel-by-pixel scan of all 108 stacks. No pixel arrays were saved to the audit JSON/artifact.

These stored values are consistent with the publication's PENGUIN-normalized image representation. They do not restore raw intensities or make the images compatible with pretrained VirTues preprocessing.

## Marker panel inventory

| Channel | Metal tag | Target |
|---:|---|---|
| 1 | Y89 | CD45 |
| 2 | In113 | CD68 |
| 3 | In115 | HLADR |
| 4 | Pr141 | SMA |
| 5 | Nd142 | CD15 |
| 6 | Nd143 | LYVE1 |
| 7 | Nd144 | CD69 |
| 8 | Nd145 | CD3 |
| 9 | Nd146 | Ki67 |
| 10 | Sm147 | CD163 |
| 11 | Nd148 | TIGIT |
| 12 | Sm149 | CXCR5 |
| 13 | Nd150 | PD-L1 |
| 14 | Eu151 | CXCR6 |
| 15 | Sm152 | TCF1 |
| 16 | Eu153 | TOX |
| 17 | Sm154 | Tim3 |
| 18 | Gd155 | FoxP3 |
| 19 | Gd156 | CD4 |
| 20 | Gd157 | Lag3 |
| 21 | Gd158 | Ecadherin |
| 22 | Tb159 | bCatenin |
| 23 | Gd160 | Tbet |
| 24 | Dy161 | CD20 |
| 25 | Dy162 | CD8a |
| 26 | Dy163 | Eomes |
| 27 | Dy164 | RpS6 |
| 28 | Ho165 | PD1 |
| 29 | Er166 | CD204 |
| 30 | Er167 | GranzymeB |
| 31 | Er168 | CD39 |
| 32 | Tm169 | Collagen |
| 33 | Er170 | CD103 |
| 34 | Yb171 | pERK12 |
| 35 | Yb172 | CD38 |
| 36 | Yb173 | CD45RO |
| 37 | Yb174 | CD33 |
| 38 | Lu175 | CD34 |
| 39 | Yb176 | CK7 |
| 40 | Ir191 | DNA1 |
| 41 | Ir193 | DNA2 |
| 42 | Pt194 | HistoneH3 |

## Relevance to the proposed study

The panel has a plausible set of immune-state and checkpoint-associated markers, including CD8a, PD1, PD-L1, TIGIT, Tim3, Lag3, TCF1, TOX, GranzymeB, CD3, CD4 and FoxP3. This makes the cohort a promising *candidate* for studying immune-marker reconstruction.

That does **not** establish compatibility with the selected foundation model or with a counterfactual intervention algorithm. In particular:

1. The VirTues input-channel and marker-embedding contract must be read from the exact pinned code/checkpoint implementation. Marker spelling and aliases (for example, `PD1` versus `PD-1`, `Tim3` versus `TIM-3`, `Lag3` versus `LAG-3`, `CD8a` versus `CD8`) must be resolved explicitly, never silently guessed.
2. The panel does not by itself define cell phenotypes or a validated CD8 infiltration endpoint. The existing masks are cell/stroma masks, not automatically immune-cell labels. The audit inventory confirms the archive contains normalized image stacks plus cell/stroma masks, with no raw-MCD directory or VirTues per-tissue preprocessing-statistics tables.
3. A marker's presence does not mean that marker is a valid intervention target. Target eligibility, intervention direction and the counterfactual baseline must be pre-specified and biologically justified.
4. A reconstructed-marker model's predictions are not observed treatment effects. A high-fidelity recommendation is not evidence that intervening on the recommended target will benefit a patient.
5. The published VirTues corpus inventory places Salié et al. (ref. 95) among seven extra IMC cohorts in the extended multi-technology corpus, not the core-14 `virtues-imc14` corpus. See the checkpoint provenance caveat in the linked decision memo.

## Decision gates before inference

- [x] Archive MD5 verified.
- [x] Actual panel CSV located and parsed.
- [x] Marker inventory recorded.
- [x] Run the corrected workflow and verify the metadata-only artifact uploads successfully.
- [x] Validate required columns, blank values, duplicate channels/tags/targets and channel numbering automatically; structural QC passes.
- [x] Read the pinned VirTues preprocessing contract and compare it with the HCC publication: released PENGUIN-normalized 0–1 images are not compatible with the pretrained pipeline.
- [x] Assess checkpoint exposure against the published training corpus: Salié et al. (ref. 95) is in the extended additions, outside the core-14 `virtues-imc14` training set at the published-reference level. `virtues-sp32` includes Salié HCC; `virtues-sp31` is unapproved for a held-out HCC claim until its omitted cohort is verified.
- [x] Complete sparse TIFF metadata/pixel-range, sampled channel-count, and mask-grid checks in the enhanced audit (sampled, not exhaustive). 
- [ ] Define and lock patient-level split, endpoint/cell labels, eligible intervention targets and counterfactual baseline before evaluating held-out patients.
- [ ] Run a one-image/one-channel reconstruction smoke test with quantitative sanity checks only after compatible input data or a separately specified normalized-domain adaptation passes held-out reconstruction evaluation.
- [ ] Only after the smoke test passes, run patient-level held-out reconstruction and signed recommendation-fidelity experiments.

**Current decision:** Archive integrity and panel structural QC **PASS**. Direct inference on the public HCC normalized TIFFs using pretrained VirTues is **NO-GO**. Use original-scale inputs if supplied by the study team, or pivot to a verified VirTues/spora-compatible cohort. Cell labels, CD8 endpoint, counterfactual baseline, real-data inference and biological conclusions remain open.
