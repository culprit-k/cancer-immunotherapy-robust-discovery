# Novelty assessment

**Status (25 October 2026): the old robustness-only paper is NO-GO as the primary novelty claim. A more specific virtual-marker / counterfactual recommendation-fidelity question is CONDITIONALLY worth a feasibility pilot; novelty remains unverified.**

## Rejected primary candidate

Repeating Morpheus across patient resamples and seeds, then reporting generic selection frequency and Jaccard scores, is useful for reproducibility but too incremental on its own. Morpheus already performs patient-level splits, whole-tumour aggregation and held-out-patient evaluation. PHAROS, SPAD-CFR and Celcomen further demonstrate that combination search and spatial counterfactual modeling are active and crowded areas.

## New candidate

**Working title:** *What Happens When a Marker Is Missing? Counterfactual Target Discovery Under Virtual Staining in Spatial Immuno-oncology.*

**Question:** When one or more complete protein-marker channels are absent and reconstructed by a spatial-proteomics foundation model, do the resulting signed counterfactual target recommendations and held-out-patient model-predicted CD8+ infiltration changes remain faithful to those obtained from fully measured channels?

Possible secondary question: can a prespecified, validation-calibrated reliability/abstention rule flag recommendations that change under plausible marker reconstruction?

This candidate connects two mature areas:
- Spatial counterfactual target discovery (Morpheus; SPAD-CFR) and spatial causal perturbation modeling (Celcomen).
- Virtual marker reconstruction, cross-panel transfer and spatial-proteomics foundation models (VirTues; Spatium; spora benchmarks), plus uncertainty-aware imputation (TISSUE and related methods).

The potential gap is narrower: **downstream intervention-decision fidelity under whole-channel reconstruction**, rather than another method for spatial counterfactual generation, marker imputation or generic stability scoring.

## Why this may be more specific—but is not yet confirmed

VirTues supports marker reconstruction and virtual staining and has already been evaluated on cross-panel/cross-technology settings and clinical biomarker tasks. Spora also has explicit virtual-staining and tissue-level benchmark pipelines. Spatial imputation research already evaluates reconstruction quality and downstream tasks. The new work can only be distinguished if it shows that marker-level reconstruction metrics miss or misestimate changes in the *signed target set* or its held-out model-predicted objective, and if a reliability evaluation/abstention rule adds value over established baselines.

A focused web/literature search did not identify a direct paper explicitly benchmarking spatial-proteomic counterfactual intervention-set fidelity under virtual-marker reconstruction. This is **not proof of absence**; the search is not systematic and broader terms, supplementary materials and newer preprints may reveal overlap.

## What would not be novel on its own

- Virtual staining or marker reconstruction.
- Spatial counterfactual generation.
- Cross-panel/cross-technology transfer.
- Counterfactual robustness or feature stability in general.
- Marker-level MAE/RMSE or correlation alone.
- A new named score without showing that it changes a decision or improves reliability.
- Claiming causal truth or therapeutic efficacy from a model-predicted CD8+ infiltration change.

## Testable experimental contribution

A strong paper would compare, at equal target budgets and on the same untouched patients:
1. Fully measured-channel reference.
2. Observed-marker-only model without imputation.
3. Simple reconstruction baseline.
4. Foundation-model reconstruction (e.g., VirTues) with whole-channel masking.
5. Optional additional imputer only if feasible.

It would measure both marker reconstruction and decision-level outcomes: signed target-set Jaccard, direction flips, target-set size/empty recommendation rate, patient-level predicted-uplift fidelity and model-based reference regret. It would evaluate an abstention/reliability rule only if the pilot demonstrates meaningful recommendation errors and the rule can be calibrated on training/validation data. "Regret" here means disagreement with the full-measurement model reference—not observed therapeutic regret or clinical treatment effect.

## Data and feasibility risk

The public spora collection documents multiple spatial-proteomics cohorts/technologies; VirTues provides public code and pretrained weights. However:
- We have not audited all dataset-level licenses or panel/channel mappings.
- The Morpheus/Wang dataset was obtained by access request for VirTues and is not redistributable in the harmonized VirTues corpus because of licensing restrictions.
- We have not downloaded a dataset or run VirTues, Morpheus, SPAD-CFR or Celcomen locally.
- An independent anti-PD-1 melanoma spatial mIF dataset is available (12 patients, 14 markers, data DOI 10.5281/zenodo.16898362) but has only four responders and limited marker overlap; use only for exploratory secondary analyses if justified.
- A separate public melanoma dataset has 57 pretreatment stage-III bulk RNA-seq samples and four Visium tumors; bulk RNA cannot validate spatial protein intervention effects directly.


## Material new prior-art risks (25 October 2026)

The targeted audit now includes **Spatium** and **CONCERT**, which make the original gap more crowded:

- **Spatium (2026)** already addresses spatial-protein imputation with held-out tissue sections. Generic protein reconstruction and section-level generalization are therefore not differentiators.
- **CONCERT** combines spatial-transcriptomics imputation with counterfactual perturbation-response simulation. It is a different modality, but it is a close conceptual neighbor and must be examined before claiming that imputation-aware counterfactuals are new.
- The 2026 spatial-metabolomics benchmark explicitly assesses both imputation error and preservation of downstream spatial clustering. Merely adding a downstream metric is not a novelty claim.

Official/public sources: VirTues paper and model repo (https://www.nature.com/articles/s41586-026-10884-y; https://github.com/bunnelab/virtues), Spatium (https://pmc.ncbi.nlm.nih.gov/articles/PMC13419744/), CONCERT (https://pmc.ncbi.nlm.nih.gov/articles/PMC12642540/), spatial-metabolomics benchmark (https://doi.org/10.1016/j.isci.2026.115203), and spora docs (https://spora.epfl.ch/docs/).

### Sharpened candidate—not a proven gap

If the candidate survives full methods/supplement review, the potentially useful question is whether complete-channel virtual staining changes **signed intervention decisions** and their patient-level model-predicted CD8 objective, and whether a **validation-calibrated selective/abstention rule** can reduce decision error at a stated coverage/target budget. This must beat simple observed-marker-only and simple-imputation baselines. A new score alone is insufficient.

### Model licence and exposure gate

The official VirTues repository lists `virtues-sp32` (32 datasets, CC BY-NC 4.0 weights), `virtues-sp31` (31 datasets, MIT weights) and `virtues-imc14` (14 IMC datasets, CC BY-NC 4.0 weights). Code, model weights and each dataset have separate terms. A held-out cohort claim requires the exact checkpoint and training cohort list; a standard all-dataset checkpoint is not independent on a cohort included in its training data. Review non-commercial restrictions before any commercial or patent-oriented use.

Full targeted audit: [targeted prior-art and feasibility audit](targeted_prior_art_and_feasibility_audit_2026-10-25.md).

## Decision

**Conditional GO for the feasibility pilot only.** Proceed to a full protocol only if:
1. The complete prior-art review leaves a specific gap.
2. An eligible cohort has measured marker channels, patient IDs, a usable CD8/T-cell endpoint and clear reuse terms.
3. The foundation-model training exposure to that cohort is known and leakage is prevented.
4. A published/surrogate counterfactual baseline is reproducible.
5. The study measures decision-level fidelity beyond ordinary marker reconstruction metrics.

If any of these fail, pivot rather than claim novelty. No patentability, clinical utility or biological efficacy claim is made.


## Important additional narrowing after inspecting VirTues Methods

VirTues explicitly tests downstream phenotyping after virtual marker reconstruction: it reconstructs CD20/CD20+CD38 for B-cell phenotyping and progressively masked T-cell markers (CD3E and combinations with CD4/CD45RA/CD8) for T-cell phenotyping, then reruns classification (Nature 2026 Methods, Supplementary Fig. 16; https://www.nature.com/articles/s41586-026-10884-y).

Therefore, the candidate must **not** claim novelty for "imputation affects downstream analysis" in general, or for virtual-marker preservation of cell phenotypes. The only remaining candidate distinction is the narrower downstream decision: whether reconstruction changes complete signed *counterfactual target recommendations* and their objective when evaluated on untouched, fully measured patients. This still requires a more systematic search for imputation-aware intervention/causal recommendation studies before being treated as a gap.
