# Method and dataset compatibility matrix

**Status (25 October 2026): scoping only. This table is not evidence that cohorts can be pooled or models compared directly.**

| Study/resource | Modality and cohort information | Model output / endpoint | Access and rights status | Directly comparable to Morpheus CD8-infiltration intervention evaluation? |
|---|---|---|---|---|
| **Morpheus (2025)** | Imaging mass cytometry / spatial proteomics. Melanoma: 159 cores from 69 patients, 39 channels. CRC liver metastases: 209 sections from 30 patients. | Counterfactual per-patch molecular intensity changes; median aggregation into whole-tumour strategy; model-predicted CD8+ T-cell infiltration on held-out patient samples. Selected hypotheses tested in vitro. | Public code and tutorial bundle. Several data artifacts are separate. The original melanoma data-for-analysis archive is about 7.1 GB, and its Zenodo Rights/license field appeared blank in this audit; confirm specific terms. | **Reference baseline.** Published task, model output and endpoint are available in the article/code, but local reproduction is pending. |
| **SPAD-CFR (Biology, 2026)** | Spatial point-cloud tissue representation with molecular profiles and coordinates; paper describes multiple tissue settings and melanoma immune-focused intervention hypotheses. Exact marker overlap and patient-level data correspondence require detailed audit. | Generative counterfactual tissue states that may change both molecular profiles and spatial coordinates; includes predicted immune-focused behavior. | Article is open access under CC BY, but its article license does not automatically resolve terms for every underlying dataset or code artifact. Exact reproducibility/data availability is not confirmed here. | **Not yet.** Output is a tissue-state simulation, not necessarily a Morpheus-compatible signed marker-intensity strategy or same CD8 endpoint. A comparison requires a prespecified common endpoint and careful validation. |
| **Anzum et al. (MICCAI 2026)** | Spatial transcriptomics (Xenium); 38 cholangiocarcinoma tissue-microarray cores. The paper page states the primary cores are not publicly available; code demonstrates on a public breast cancer dataset. | Counterfactual neighbor replacement and directional cell-cell influence score; held-out cores and core-level bootstrap uncertainty. | Code linked; primary evaluation data not publicly available according to the proceedings page. | **No direct comparison.** Endpoint is directional cell-cell influence, not complete therapeutic intervention sets or CD8 infiltration uplift. Highly relevant prior art on spatial counterfactuals and core-level uncertainty. |
| **PHAROS (bioRxiv preprint, September 2026)** | Single-cell perturbation models and combinatorial drug perturbation datasets. | Searches and ranks drug combinations that move cells from a starting state toward a target state; includes matched controls, sampled batches and robustness-aware reranking. | Public code repository, described as MIT-licensed. Data/model requirements and compute can be substantial; check each data artifact license. | **Not directly.** The intervention object is drug treatment in single-cell state space, and endpoint is state-conversion score, not spatial-protein CD8+ infiltration. Strong prior art against a broad combination-search or robustness-reranking claim. |
| **COMPASS (Nature Medicine, 2026)** | Bulk tumour transcriptomes and clinical immunotherapy cohorts; article reports training on 10,184 tumours and evaluation across 16 cohorts/1,133 patients. | Prediction of immunotherapy response from transcriptomic/immune concepts; cross-cohort generalization. | Public article/reported cohorts; exact data-level reuse terms must be checked per source. | **No direct comparison.** Its output is treatment-response prediction, not an intervention set. It can inform external-validation practice but cannot be pooled with spatial protein values without a sound mapping. |
| **Original melanoma IMC data-for-analysis (Zenodo 5994136)** | Processed single-cell objects, clinical tables, labels and analysis files from the original melanoma IMC study. This is related to Morpheus' melanoma domain but is not the same as the Morpheus preprocessed artifact/model output. | Input/metadata for the original published analysis, not a ready-made common endpoint or an interchangeable Morpheus model input bundle. | Archive lists a 7.1 GB data zip and 41.1 MB code zip; license field not clearly displayed. Verify exact terms before reuse. | **Potential source only.** First verify preprocessing, channels, patient IDs and a compatible label/outcome; do not infer direct comparability from disease name alone. |

## Decision consequences

### Cross-method intervention decision utility
Current obstacle: Morpheus outputs perturbations to molecular channels and predicted CD8+ infiltration; SPAD-CFR generates spatial tissue counterfactuals; the MICCAI method estimates directional cell-cell influence; PHAROS ranks drug combinations in single-cell state space. Those output objects are not interchangeable.

Candidate A should proceed only if two methods can be evaluated on the same patient-level data or both can be mapped to a well-justified common endpoint *before* inspecting results. If not, a head-to-head comparison would be scientifically invalid.

### Cross-cohort/platform transfer
Current obstacle: matching cancer labels or target names does not establish comparability. We need shared measured markers, a consistent signed intervention interpretation, compatible patient-level endpoint, and genuinely independent samples. Same-patient or same-study reuse can create leakage if provenance is not checked.

Candidate B should proceed only after a channel/marker crosswalk and endpoint-compatibility check.

## Immediate deliverable from this matrix

The next step should be a small data dictionary/crosswalk for candidate resources and exact access terms. No model training or transfer result should be claimed until the files are available, checksummed, inspected and a baseline evaluated on the chosen endpoint.


## October 2026 update: virtual-marker candidate and newly relevant datasets

| Resource / study | What is available or covered | Value for current candidate | Limitations / gate |
|---|---|---|---|
| **VirTues (Nature 2026)** | Pretrained spatial-proteomics foundation model; masked-channel reconstruction, virtual staining, cell/tissue representation and cross-panel/cross-technology tasks. Its paper reports 32 cohorts and more than 5,100 patients across four technologies; the model weights and code are public. | Best candidate reconstruction model for testing whether missing marker channels preserve counterfactual target recommendations. | The dataset corpus has exact license restrictions; the Morpheus/Wang data cannot be redistributed. Need to establish whether the evaluation cohort was included in pretraining. VirTues already covers reconstruction and biomarkers, so the novelty question must be downstream intervention-decision fidelity. |
| **spora [data] / spora [bench]** | The current data documentation lists 35 cohorts, 5,477 patients and five imaging technologies. Benchmarks include multiplex-to-multiplex virtual staining, cell annotation and tissue-level tasks. | Strongest place to search for a permitted dataset with measured channels that can be masked and then compared with reconstruction. | Actual candidate channels, CD8 outcome, patient IDs and data terms have not yet been audited. Counts on the current platform are not identical to the VirTues paper's training corpus. |
| **Spatium (2026)** | Protein-language foundation approach for reconstructing missing spatial protein maps and preserving tissue architecture. | Important adjacent imputation baseline if code/data access and compute make it feasible. | Need to check whether its inputs/output representation are compatible; additional model is optional, not required for the first pilot. |
| **Celcomen (Nature Communications, March 2026)** | Causal spatial transcriptomics model that disentangles intra-/inter-cellular gene programs and generates spatial counterfactual responses. | Important prior art on causal spatial perturbation models. | RNA-expression output is not a direct substitute for spatial protein counterfactual target sets; do not pool modalities without a mapping. |
| **Pybus et al. anti-PD-1 spatial mIF cohort** | 12 stage-IV melanoma patients, 14 proteins across two 8-marker panels, >8 million cells; 4 responders and 8 non-responders; processed dataset DOI 10.5281/zenodo.16898362. | Potential secondary check if the target marker overlap is sufficient. | Small number of independent patients and limited overlap with Morpheus's four melanoma target chemokines. It is not the primary dataset for a high-dimensional clinical model. |
| **GSE300793 / GSE300445 melanoma study** | 57 pretreatment bulk RNA-seq samples from stage-III primary melanoma, plus spatial transcriptomic analysis on four primary tumours in the associated study. | May support a pre-specified exploratory gene-expression/relapse association for a fixed target signature. | Bulk RNA is not spatial protein measurement; it cannot validate an intervention effect. Four spatial tumors are inadequate for independent spatial inference by themselves. |
| **Morpheus melanoma / Wang et al.** | Closest spatial-proteomic target-discovery baseline, but data access and redistribution rights differ by archive. | Baseline method and prior target definitions. | VirTues paper states this data could not be redistributed in its harmonized corpus due to licensing restrictions. The exact access/license terms must be verified before use. |

## Current recommendation from the compatibility audit

Do not pursue broad cross-method comparisons or generic cross-platform transfer as the headline. The new candidate is a masked-marker **counterfactual recommendation-fidelity** study. Select the actual cohort only after checking channels and rights. A good initial cohort must have a measured CD8/T-cell label, enough immune-related measured markers to define a target budget, patient-level IDs, and whole-channel holdout ground truth. If the public spora corpus has no cohort satisfying these rules, stop rather than force an invalid comparison.


## Dataset-level candidate shortlist

The public spora browser currently lists these most relevant entries. Counts are catalog metadata, not local QC counts.

| Cohort ID | Catalog summary | Current use recommendation |
|---|---|---|
| hoch2022multiplexed | Melanoma IMC; 35 patients / 50 images; chemokine-milieu and immunotherapy-response study | Best biological development cohort. Must be treated as exposed to VirTues unless using a checkpoint trained without it; not a clean unseen-cohort test by default. |
| allam2022spatially | Lung cancer IMC; 26 patients / 26 images; roughly 500 MB quick-download cohort | Small data-pipeline / masking smoke test if its panel has required immune labels and rights. Not yet a main biological dataset. |
| moldoveanu2022spatially | Melanoma IMC; 90 patients / 90 images | Potential external cohort, but marker overlap, endpoint labels, licensing and VirTues training exposure remain unchecked. |
| xiao2022multiplexed | Melanoma IMC; 26 patients / 158 images; anti-PD-1 response context | Potential secondary external cohort, with panel and training exposure checks outstanding. |
| schurch2020coordinated | Colorectal cancer CODEX/H&E; 35 patients / 251 images | Potential secondary architecture context, not a direct substitute for IMC target channels without a mapping plan. |

Public browser: https://spora.bioimagearchive.org/projects/spora/dataset. Detailed checklist: docs/dataset_shortlist.md.

## Updated novelty boundary after inspecting VirTues Methods

VirTues already evaluates downstream cell-phenotyping stability after reconstructing masked markers: it removes CD20/CD38 for B-cell classification and progressively removes CD3E/CD4/CD45RA/CD8 for T-cell phenotyping, then reruns the phenotyping task. Therefore, "virtual-marker reconstruction preserves downstream analysis" is too broad to claim as new. The candidate is specifically about **counterfactual target-set and predicted-objective fidelity**, which is a different downstream decision from phenotype classification. The complete supplement and a broader prior-art search still need review before calling this an established gap.
