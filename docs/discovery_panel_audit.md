# Salié HCC discovery panel audit

**Audit date:** 25 October 2026  
**Source:** [Zenodo record 10793609](https://zenodo.org/records/10793609)  
**Metadata source:** GitHub Actions run [40198072585](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40198072585)  
**Status:** Archive integrity and panel parsing verified; model compatibility and inference remain pending.

## Integrity and panel parsing

- Archive: `HCC_DiscoveryCohort.zip`
- Downloaded size: 1,541,132,381 bytes
- Expected and observed MD5: `a842fa253ac2f0eda3cbf4d41e1b0ec1` (match)
- ZIP entries: 325
- Actual panel member: `DiscoveryCohort_panel.csv` (not the `DCCohort_panel.csv` filename described in the record text)
- Parsed panel: 42 rows; columns `Channel`, `MetalTag`, `Target`
- Raw images and masks were not committed to the repository. The original run's artifact upload failed due to a workflow path expression defect; the workflow path has since been corrected, but successful publication must be confirmed by a new run.

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
2. The panel does not by itself define cell phenotypes or a validated CD8 infiltration endpoint. The existing masks are cell/stroma masks, not automatically immune-cell labels.
3. A marker's presence does not mean that marker is a valid intervention target. Target eligibility, intervention direction and the counterfactual baseline must be pre-specified and biologically justified.
4. A reconstructed-marker model's predictions are not observed treatment effects. A high-fidelity recommendation is not evidence that intervening on the recommended target will benefit a patient.
5. Exact training/fine-tuning exposure of the HCC accession to the selected checkpoint remains a separate gate.

## Decision gates before inference

- [x] Archive MD5 verified.
- [x] Actual panel CSV located and parsed.
- [x] Marker inventory recorded.
- [ ] Run the corrected workflow and verify the metadata-only artifact uploads successfully.
- [ ] Validate required columns, blank values, duplicate channels/tags/targets and channel numbering automatically.
- [ ] Read the pinned VirTues preprocessing and marker embedding contract; check that pre-normalized HCC inputs will not be transformed twice.
- [ ] Verify model training/fine-tuning exposure at accession/cohort level.
- [ ] Define and lock patient-level split, endpoint/cell labels, eligible intervention targets and counterfactual baseline before evaluating held-out patients.
- [ ] Run a one-image/one-channel reconstruction smoke test with quantitative sanity checks.
- [ ] Only after the smoke test passes, run patient-level held-out reconstruction and signed recommendation-fidelity experiments.

**Current decision: CONDITIONAL GO for compatibility work; NO-GO for biological claims or full counterfactual experiments until the gates above are resolved.**
