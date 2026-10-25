# HCC normalized-input adaptation protocol

**Status:** Proposed validation protocol only. The storage-level TIFF audit (Step 0) has passed on representative samples; the adaptation is not implemented end-to-end, and no VirTues inference result exists.

## Decision in one sentence

The published HCC TIFFs are not compatible with a claim of *reproducing VirTues' official raw/source-format preprocessing*. However, the HCC study can still be retained as a **separate, explicitly labeled normalized-domain transfer experiment** if its stored pixel encoding is verified and the adapted input path passes a patient-held-out reconstruction benchmark before any counterfactual analysis.

Do not invert PENGUIN-normalized values into raw intensities, and do not describe adapted inputs as the official VirTues preprocessing.

## Evidence

The Salié paper Methods say PENGUIN normalization scales channel intensities to 0–1, removes unspecific background signal and applies percentile-based denoising per marker. Percentiles and thresholds were selected separately by manual inspection per marker, then applied to every ROI. The Zenodo archive contains normalized TIFF stacks, cell masks, stromal/parenchymal masks and a marker panel; the archive does not include original MCD acquisitions or a VirTues preprocessing-statistics file.

The VirTues paper says its official preprocessing clips each image/channel at the tissue-area 99th percentile, applies a shifted logarithm (`log1p`), standardizes channels using means and standard deviations computed over tissue pixels, and applies a 3×3 Gaussian blur with unit variance. The official loader also maps channel protein IDs to available marker embeddings. These steps do not undo PENGUIN normalization.

Sources:
- [Salié HCC discovery archive](https://zenodo.org/records/10793609)
- [Salié et al. Methods, image normalisation](https://gut.bmj.com/content/early/2024/09/30/gutjnl-2024-332837?versioned=true)
- [VirTues paper, dataset preprocessing and model instances](https://www.nature.com/articles/s41586-026-10884-y)
- [Official VirTues loader](https://github.com/bunnelab/virtues/blob/main/virtues/data/multiplex_dataset.py)

## Step 0 — storage-level TIFF audit: PASS

Enhanced audit workflow: [run 40214428382](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382); metadata-only artifact [12607480794](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40214428382/artifacts/12607480794). Audit result:
- ZIP inventory: 108 TIFFs each in `DC_img_normalized`, `DC_cellmasks`, and `DC_stromamasks` (324 TIFFs total), plus the panel CSV.
- Twelve evenly spaced image stacks sampled by the enhanced TIFF audit were readable. Sampled image stacks were `float32`, had 42 pages/channels, and page count agreed with the 42-row panel.
- Sampled stack shapes included `(42, 1300, 1300)` and `(42, 1500, 1500)`; preserve ROI-specific spatial dimensions rather than forcing one common shape.
- Sparse pixel summaries were taken from first/middle/last pages of 12 sampled stacks; in addition, all 42 planes were read for the first, middle and last representative ROIs (126 planes total). All sampled pixels were finite and within `[0,1]` (min `0.0`, max `1.0`; no sampled out-of-range values).
- Corresponding cell and stroma masks were present and spatial dimensions matched for all three checked ROIs (3/3 per mask directory); sampled mask storage was `uint16`.

**Scope limitation:** this is a sparse TIFF storage audit, not a complete pixel-by-pixel scan of all 108 normalized stacks. It verifies the stored float32 [0,1] representation in sampled planes, not original raw acquisition values. Do not invert normalized values or assume that matching spatial shapes establishes cell labels or model compatibility. This audit makes direct HCC-TIFF → pretrained VirTues inference more clearly **NO-GO**, not GO.

## Step 1 — make the panel and spatial axes auditable

Create one crosswalk row per measured channel with:
- actual TIFF channel/page index and exact panel row;
- metal tag, published target string, canonical protein and UniProt accession;
- VirTues marker embedding availability at the pinned code/model version;
- any alias, duplicate protein mapping or unresolved ambiguity;
- pixel shape/resolution, ROI identifier, patient identifier and source mask.

Fail closed on unexplained channel-order differences, unsupported axes, missing embeddings or unresolved ROI-to-patient mapping. Do not silently map `PD1`, `Tim3`, `Lag3` or `CD8a` aliases.

Generate a tissue mask from a documented source if the current masks are not tissue masks. The VirTues paper describes an Otsu-thresholded pixel-wise max projection followed by binary morphology as one such method. The cell and stroma masks are not interchangeable with a verified tissue mask or cell-type labels.

## Step 2 — compare two explicit input transforms

Both branches use discovery-cohort training patients only to set any dataset-level calibration parameters. For an artificially masked marker, the hidden channel's true values may be used only as evaluation ground truth, not to compute input features or parameters available to the model at inference.

**Variant A: HCC-native normalized domain**
1. Decode stored TIFF values only according to verified encoding/source metadata.
2. Preserve the PENGUIN background removal and percentile denoising; do not apply another undocumented PENGUIN step.
3. Standardize available channels using tissue pixels and a documented mask, with any means/standard deviations computed from permitted inputs only.
4. Do not apply additional `log1p` or blur by default; this branch tests whether the existing normalized/denoised images can serve as a model input domain after channel standardization.

**Variant B: PENGUIN-to-VirTues-like domain**
1. Start from the same verified decoded PENGUIN-normalized values.
2. Apply tissue-area 99th-percentile clipping, `log1p`, 3×3 Gaussian blur (unit variance), then tissue-area channel standardization.
3. Label this a *modified preprocessing adaptation*, not a reproduction of VirTues source preprocessing.

The two branches are hypotheses, not interchangeable certified pipelines. Any target-channel scale calibration must be learned only on training/validation patients. Report reconstruction scores in the documented normalized domain and/or standardized evaluation space so scale inversion is not silently assumed.

## Step 3 — run only a small patient-held-out reconstruction pilot

Use patient-grouped folds; all ROIs and cells from one patient must stay within one fold. For each pre-specified marker, mask the entire measured channel and reconstruct it using each transform. Compare the same held-out patients against:
1. a constant/mean-channel baseline;
2. a best-correlated observed-marker baseline;
3. VirTues under Variant A;
4. VirTues under Variant B.

Report patient-macro MAE/RMSE and correlation (with constant-channel handling), per-marker performance, uncertainty from patient-level bootstrap, and any output scale/range failures. Choose no transformation using the external ICI cohort. Set stopping rules and candidate channels before examining held-out outputs.

**Pilot GO only if** at least one transform gives reproducible held-out improvements over simple baselines without marker-specific collapse, leakage, or unvalidated output-scale calibration. Otherwise pivot to a model explicitly trained/validated for PENGUIN-normalized images.

## Step 4 — only then decide whether counterfactual fidelity is estimable

The HCC panel contains CD8a and checkpoint/state markers but does not contain the full Morpheus marker set for its melanoma or colorectal experiments. Any HCC experiment must be labeled a *checkpoint-marker decision-fidelity adaptation*, not direct reproduction of Morpheus' original target-discovery results.

Before counterfactual analysis, independently lock:
- a defensible cell-/patch-level CD8 objective supported by labels or a validated marker-based rule;
- the eligible target-marker set and increase/decrease semantics;
- the counterfactual method, target budget, thresholds and calibration procedure;
- the patient-level split and the full-measured model-reference definition.

Cell and stroma masks by themselves are not CD8 cell labels. Predicted CD8 infiltration is not an observed treatment effect. Do not perturb CD8a when using a CD8a-derived endpoint if that creates target/label leakage.

## Stop conditions

Stop the VirTues/HCC path if the TIFF storage encoding or axes cannot be resolved; channel-to-protein embedding mapping is incomplete; patient/ROI links are not reliable; no defensible CD8 endpoint exists; or no normalized-domain transform beats simple baselines on held-out patients. In that case use the unsent Salié data request or pivot to a verified spora-compatible cohort/model.
