# Robust HCC target-discovery analysis plan (v1; pre-results)

**Status:** protocol/analysis plan only. No HCC VirTues inference, counterfactual result, or clinical-outcome model is reported by this document.

**Purpose:** establish a locked, leakage-resistant plan for evaluating whether model-derived spatial-proteomic perturbation hypotheses are reproducible across patients, marker panels, and cohorts, before making any claim about immune-evasion targets.

## 1. Research question

Among HCC spatial-proteomics samples, do AI-derived candidate molecular perturbations associated with a more T-cell-infiltrated spatial phenotype remain stable under patient-level resampling, marker-panel restriction, reasonable preprocessing perturbations, and evaluation in a separate patient cohort?

### Intended contribution

The planned contribution is a *robustness and transportability evaluation* of computational counterfactual candidates, not a claim that a model identifies causal therapeutic targets. Morpheus already uses counterfactual optimization of spatial-proteomic profiles to propose changes associated with increased predicted CD8+ T-cell presence; a broad “AI counterfactual target discovery” claim would therefore not establish novelty by itself. The candidate contribution must be the predeclared patient/cohort-level stability analysis and explicit failure characterization, provided the data and inputs support it.

## 2. Public data and eligibility

- **HCC discovery cohort:** Zenodo record [10.5281/zenodo.10793609](https://doi.org/10.5281/zenodo.10793609); the record describes 54 HCC patients and normalized multichannel TIFF images, cell masks, stromal/parenchymal masks, and panel metadata.
- **ICI-treated HCC cohort:** Zenodo record [10.5281/zenodo.10794904](https://doi.org/10.5281/zenodo.10794904); the record describes 42 HCC patients treated with immune checkpoint inhibitors and normalized multichannel TIFF images, cell masks, stromal/parenchymal masks, and panel metadata.
- **Checkpoint candidate:** `virtues-imc14`, pinned in the audit records by immutable weight identity. Do not use `virtues-sp32` for held-out HCC evaluation because the published VirTues training corpus includes the Salié HCC cohort. The `virtues-imc14` exposure assessment remains a publication-level audit, not a signed accession-by-accession training certificate.
- **Licence:** the discovery cohort is listed CC BY 4.0. Review the specific ICI dataset's repository terms before redistribution or derivative-data release. The `virtues-imc14` weights are CC BY-NC 4.0; do not commit them to the public repository. Cite and comply with the original VirTues code and dataset terms.

### Mandatory exclusions / hold points

1. The ICI inventory has 86 image/mask ROI triplets but 84 clinical ROI entries. The known discrepancies in ICI_24 and ICI_39 must be reconciled using the authoritative supplementary table/crosswalk. Until resolved, those ambiguous ROIs are excluded from clinical-outcome analyses; they must not be assigned by guesswork.
2. Confirm the ordered image-plane-to-panel mapping and UniProt marker identity for every eligible stack. Matching channel counts are not proof of ordering.
3. Obtain an authoritative definition for numeric stromal-mask labels 3–9 and verify mask/image alignment. Do not infer code meaning from label numbers.
4. Published VirTues preprocessing and the released [0,1]-normalized TIFF representation are not yet demonstrated to be equivalent. Official-reproduction claims are a no-go until the original input scale/statistics and pipeline are documented. If that cannot be obtained, any normalized-domain experiment must be separately labelled **exploratory adaptation**, not official VirTues reproduction.
5. Complete tensor-level QC on the actual arrays, not only filenames or representative images: dimensions, axis order, dtype, finite fraction, value distribution, channel order and mask alignment.

## 3. Technical entry gate

Before any HCC inference:
- Verify the source revision, config, checkpoint SHA-256, size, tensor inventory, and licence.
- Strictly load the checkpoint into the matching official architecture; no missing/unexpected keys permitted.
- Pass packed-attention execution and a synthetic forward test using the official marker embeddings. The pinned `virtues-imc14` checkpoint's `encoder.prior_embedding_encoder.weight` shape is (512, 640); the marker embeddings must have width 640, and must not be padded/resized to satisfy an assumed dimension.
- Preserve the original attention source and record the patch diff. The CPU SDPA fallback is an experimental code-path compatibility aid; it is not presumed numerically identical to FlashAttention until equivalence tests support that statement.
- Save the full environment, command, seeds, logs, and machine-readable report.

A passing software preflight is necessary but not sufficient for scientific inference.

## 4. Primary analysis: reconstruction and model diagnostic

Once input compatibility is proven, start with one ROI chosen by a deterministic outcome-blind rule (lexicographically first eligible ROI). Use the official reconstruction interface where valid. Use a fixed seed and a fixed mask pattern; score predictions only on withheld pixels/channels.

Compare against at least:
1. a tissue-area/channel mean baseline;
2. a spatially local mean/smoothing baseline;
3. the VirTues reconstruction output, if the model/input gates pass.

Report per-marker and pooled MAE, MSE/RMSE, scored-pixel count, and patient-level variability. Never split ROIs from the same patient across training and evaluation. After the single-ROI smoke test passes, use a prespecified set of eligible ROIs without outcome-driven selection.

## 5. Robust candidate generation and stability evaluation

Only if the reconstruction/feature pipeline and phenotype labels are valid:

1. Define the target phenotype before fitting. Prefer an explicit, validated T-cell infiltration/spatial immune-state endpoint; mask the target cells/marker information from predictor inputs to limit label leakage.
2. Generate bounded, biologically constrained perturbation candidates under a locked model and objective. Save the unperturbed profile, perturbation vector, objective terms, bounds, stopping rule and all random seeds.
3. Use patient-level bootstrap resampling in the development cohort. Recompute candidate rankings in each resample.
4. Repeat under predeclared panel-intersection and preprocessing sensitivity settings. Report changes in candidate ranks and performance instead of selecting the most favourable configuration.
5. Treat the ICI cohort as external evaluation only. Do not use its outcomes to choose markers, tune hyperparameters, select thresholds, or revise counterfactual objectives.
6. Quantify candidate stability using top-k selection frequency, pairwise rank correlation and Jaccard overlap of top-k sets across resamples/settings; give patient-level uncertainty intervals. Compare against shuffled-marker and simple baseline controls where appropriate.
7. Report unstable candidates and null/negative results with the same prominence as stable candidates.

**Interpretation rule:** a counterfactual is a model-generated hypothesis, not an intervention observation. An increase in predicted CD8+ T-cell presence is not evidence of a causal immune-evasion mechanism, a therapeutic effect, druggability, or patient benefit.

## 6. Clinical outcome analysis: strictly secondary and low-dimensional

The ICI cohort has 42 patients and the current extraction summary reports only five partial responses (PR). This is too small to support a high-dimensional supervised response model reliably. Do not train a large predictor on these outcomes.

After the crosswalk and endpoint definitions are resolved, use only low-dimensional, predeclared descriptive or exploratory analyses. Report effect sizes, patient-level confidence intervals, missingness, and multiplicity handling. Survival endpoints must use an authoritative patient-level clinical table and prespecified censoring/event definitions. No patient-level predictions or claims of clinical utility are permitted from this exploratory dataset alone.

## 7. Reproducibility and reporting

Release, subject to licences:
- source and versioned configuration;
- audit scripts/tests and aggregate QC summaries;
- immutable source/checkpoint identifiers and hashes (not model weights);
- patient-level split manifest using pseudonymous IDs only when permitted;
- per-ROI and per-marker metrics with patient identifiers removed or suitably aggregated;
- negative results, failures, sensitivity analyses, and full model limitations.

Do not publish patient-level clinical rows, potentially identifiable pathology images, access-restricted model weights, or data-derived files unless their licence/governance explicitly allows it. Follow the original dataset citation instructions and local institutional policy for secondary analysis of public, de-identified data.

## 8. Go/no-go decision rules

**GO to an exploratory reconstruction pilot** only after Gates 1–3 and the technical entry gate pass.

**GO to the cross-cohort robustness analysis** only after the pilot beats preregistered simple baselines on held-out patients and the marker/panel map is authoritative.

**NO-GO for target claims** if candidates are unstable under patient bootstrap, depend on one preprocessing choice, fail external evaluation, or cannot be separated from published HCC immunotypes.

**NO-GO for a results manuscript** until real-data results exist, code and data provenance are reproducible, and the novelty claim has been checked against prior work. If the model or data compatibility cannot be resolved, report the compatibility audit as a technical limitation rather than manufacture a biological result.

## 9. References and source records

1. Wenckstern J, Jain E, von Querfurth B, et al. *The Virtual Tissues foundation model resolves spatial proteomics across scales.* Nature (2026). DOI: [10.1038/s41586-026-10884-y](https://doi.org/10.1038/s41586-026-10884-y). Official code: [bunnelab/virtues](https://github.com/bunnelab/virtues).
2. Salié H, et al. *Spatial single-cell profiling and neighbourhood analysis reveal the determinants of immune architecture connected to checkpoint inhibitor therapy outcome in hepatocellular carcinoma.* Gut (2024). DOI: [10.1136/gutjnl-2024-332837](https://doi.org/10.1136/gutjnl-2024-332837).
3. Wang ZJ, Farooq AS, Chen YJ, et al. *Identifying perturbations that boost T-cell infiltration into tumours via counterfactual learning of their spatial proteomic profiles.* Nature Biomedical Engineering 9, 390–404 (2025). DOI: [10.1038/s41551-025-01357-0](https://doi.org/10.1038/s41551-025-01357-0).
4. Discovery cohort data: [10.5281/zenodo.10793609](https://doi.org/10.5281/zenodo.10793609).
5. ICI cohort data: [10.5281/zenodo.10794904](https://doi.org/10.5281/zenodo.10794904).

---
**Version note:** This plan is written before HCC model inference and before outcomes are used for model selection. Changes to eligibility, primary metric, splits, perturbation objective or thresholds must be versioned and explained; changes made after viewing outcomes are exploratory.
