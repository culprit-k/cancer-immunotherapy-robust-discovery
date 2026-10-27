# Execution work order: HCC robust target discovery
**Updated:** 2026-10-27  
**Branch:** `hcc-virtues-audit-next-step`  
**Purpose:** A single fail-closed sequence for moving from current audits to a scientifically defensible first model run.

## Executive decision
**Current stage: pre-inference compatibility validation.** Do not run outcome-driven model selection or claim target discovery until the data, panel, preprocessing, checkpoint exposure, and patient-level analysis gates are documented.

This work order intentionally separates three types of evidence:
1. **Repository/CI evidence:** tests run in GitHub Actions.
2. **Runtime evidence:** commands executed against the user's actual Colab files and checkpoint.
3. **Scientific evidence:** outcomes from a prespecified experiment on eligible patient-level data.

Passing one category does not imply the others passed.

## Gate A — Preserve and identify source data
- [ ] Preserve original archives, extracted files, and checkpoint; do not overwrite or redownload existing copies.
- [ ] Record source DOI/URL, download date if known, archive size, MD5/SHA-256, licence, and exact extracted-file inventory.
- [ ] Keep patient-level clinical data, raw images, and model weights out of the public repository.
- [ ] Confirm all 86 image/cell-mask/stromal-mask triplets are structurally valid (existing audit reports this passed).
- [ ] Maintain the source-derived patient table separately from the ROI manifest.

**Evidence status:** structural QC reported passed within scope. Do not reinterpret it as clinical validity.

## Gate B — Patient/ROI reconciliation
- [ ] Patient-prefix linkage: 42 image patient prefixes map to the 42 clinical patient rows.
- [ ] Explicitly record unresolved source-count conflicts: ICI_24 table=2/archive=3; ICI_39 table=1/archive=2.
- [ ] Request source-authoritative filename-to-ROI mapping or written author clarification.
- [ ] Until resolved, exclude both affected patients from the primary outcome analysis; document this exclusion before viewing model performance. Preserve the full archive and manifest.
- [ ] Do not invent a clinical record ID or infer ROI eligibility solely from ROI number order.
- [ ] Unit of analysis is patient. Aggregate ROI-level features per patient and split all train/validation/test sets by patient.

**Gate state:** partial pass for patient-prefix mapping; blocked for authoritative resolution of two ROI-count conflicts.

## Gate C — Panel and masks
- [ ] Verify exact order of all 45 planes in the released image arrays; a 45-row panel workbook alone does not prove plane order.
- [ ] Map each marker to its official target name, UniProt accession, and the exact VirTues marker embedding. Record ambiguous synonyms and unresolved targets.
- [ ] Determine the semantic codebook for cell and stromal masks from source documentation; do not assume mask labels are binary or interchangeable.
- [ ] For every eligible ROI, verify image/mask dimensions, dtype, label values, empty regions, finite-value range, and visual overlays. Keep overlays in private runtime unless permitted for publication.
- [ ] Record each check in a machine-readable QC report.

**Gate state:** channel count and structural alignment reported passed; exact channel order and mask semantics require confirmation.

## Gate D — Preprocessing compatibility
- [ ] Read the exact official VirTues preprocessing implementation and pinned dataset configuration.
- [ ] Identify expected input axis order, channel scaling, clipping, transformations, standardization statistics, smoothing, cropping, and mask handling.
- [ ] Determine whether released HCC TIFFs are original-scale data or already normalized/preprocessed. Values in [0,1] alone cannot answer this.
- [ ] Prefer documented original-scale inputs plus official processing metadata.
- [ ] If only normalized TIFFs are available, design a separately named normalized-domain adaptation with explicit assumptions and sensitivity analyses. Never call it official reproduction.
- [ ] Add an input contract test that checks all dimensions, channel IDs/order, units/range, mask semantics, and transformation provenance.

**Gate state:** no-go for direct official VirTues inference on current normalized TIFFs until equivalence is demonstrated.

## Gate E — Checkpoint provenance and licence
- [ ] Pin repository revision, immutable file revision, file size and SHA-256.
- [ ] Keep the checkpoint private/local; never commit model weights.
- [ ] Verify checkpoint-specific training dataset manifest, not only the paper's general cohort list.
- [ ] Exclude `virtues-sp32` from held-out HCC evaluation because it includes the target HCC study.
- [ ] Treat `virtues-imc14` as a candidate only until its exact training manifest has been checked for HCC overlap.
- [ ] Respect the checkpoint's CC BY-NC 4.0 noncommercial restriction.

**Gate state:** checkpoint identity recorded; exposure clearance incomplete.

## Gate F — First pilot, only after A–E
1. Freeze one eligible ROI using a rule independent of clinical outcome.
2. Run the official pipeline on a synthetic input and then one real ROI.
3. Save command, git commit, Python/package versions, device, seed, config hash, input file hashes, checkpoint hash, stdout/stderr, and output shapes/ranges.
4. Confirm outputs are finite, shape-compatible, and consistent with expected semantics.
5. Compare the reconstruction to input using prespecified metrics; do not use this single ROI as biological evidence.
6. If any contract check fails, stop and report the exact failed gate rather than silently coercing data.

## Gate G — Patient-level analysis preregistration
- [ ] Verify the primary endpoint and response definitions from the source publication/table before choosing metrics.
- [ ] Keep clinical outcomes at patient level; ROIs/cells/pixels are nested measurements, not independent observations.
- [ ] Prespecify cohort eligibility and exclusions before model scoring.
- [ ] Compare clinical-only, single-marker, regularized additive, pairwise/small-combination, and proposed AI ranking baselines where sample size supports them.
- [ ] Fit preprocessing, feature selection, calibration and thresholds only inside patient-level training folds.
- [ ] Report uncertainty and stability, not just best AUROC or a selected combination.
- [ ] Use an independent cohort as external validation only if endpoint, panel and preprocessing compatibility are documented.
- [ ] Describe counterfactual changes as model-generated hypotheses, not proven causal immune-evasion mechanisms or treatment recommendations.

## Gate H — Decision rules
**GO to pilot:** Gates A–E documented, no unresolved fatal contract mismatch, ROI eligibility frozen, checkpoint exposure and licence recorded.

**GO to outcome analysis:** pilot passes; endpoint dictionary and patient-level split plan frozen; eligible patient set documented; leakage tests pass.

**NO-GO:** unknown channel order; unverified preprocessing; unresolved model/data schema; checkpoint exposure unclear for a held-out claim; patient/ROI linkage guessed; or outcome leakage.

## Current verified status (as of 2026-10-27)
- Public discovery cohort archive and 42-channel panel: structural identity checks reported passed.
- ICI archive: 86 image stacks, 86 cell masks, 86 stromal masks; 86 complete triplets; structural checks reported passed.
- Clinical table: 42 patients; response counts documented as SD=27, PD=10, PR=5. Only five PR cases; a complex response classifier cannot credibly be called validated from this cohort alone.
- ICI_24 and ICI_39 ROI-count discrepancies remain unresolved at image level.
- VirTues CPU compatibility and metadata helper tests passed in GitHub Actions; these do not prove actual Colab inference.
- Current normalized HCC TIFFs are not yet proven compatible with official VirTues preprocessing.
- Exact `virtues-imc14` training manifest remains unverified for HCC exposure.
- No real HCC VirTues inference, validated robust combinations, causal mechanism, clinical utility, or patentability has been established.

## Immediate next action
Use the user's existing Colab runtime to execute the documented preflight **without deleting or replacing existing data** and collect its full JSON/stdout report. In parallel, seek an authoritative image-level ROI mapping and the checkpoint-specific training manifest. Do not bypass a failed gate to produce an apparent model result.
