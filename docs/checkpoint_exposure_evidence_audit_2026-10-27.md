# Checkpoint exposure audit: what public evidence does and does not establish

**Date:** 2026-10-27  
**Scope:** Candidate `virtues-imc14` checkpoint for evaluation on the Salié et al. HCC ICI cohort.

## Decision

**Exposure clearance remains BLOCKED.** The public VirTues paper and README establish the broad training-corpus description, but the evidence reviewed here does not yet provide a checkpoint-specific, immutable list of all 14 IMC datasets and accession-level inclusion/exclusion records sufficient to certify that the candidate weights never saw this HCC cohort.

Do not call the cohort an independent held-out validation set until this is resolved.

## Evidence reviewed

1. The official VirTues README says `virtues-imc14` was trained on 14 IMC datasets and is licensed CC BY-NC 4.0. It separately describes `virtues-sp32` as trained on 32 spatial-proteomics datasets.  
   Source: https://github.com/bunnelab/virtues
2. The Nature paper says the IMC-only corpus comprises 14 public datasets and reports additional model variants trained while excluding selected cited studies for specific zero-shot evaluations. That description does not, by itself, identify the exact immutable data manifest for the downloaded `virtues-imc14/model.safetensors` file.  
   Source: https://www.nature.com/articles/s41586-026-10884-y
3. The HCC ICI cohort is Salié et al., *Gut*, DOI 10.1136/gutjnl-2024-332837. The fact that this paper is an HCC spatial-proteomics study is not proof that it was or was not included in a particular checkpoint's training data.  
   Source: https://gut.bmj.com/content/74/3/451

## Required evidence to clear the gate

- An author-maintained or release-pinned dataset manifest for the exact `virtues-imc14` weights, with source study citations and accession/record identifiers where available.
- Crosswalk the manifest against Salié et al. and the HCC ICI release at Zenodo DOI 10.5281/zenodo.10794904.
- Record the exact model repository revision, weight file revision, SHA-256, and licence beside the manifest.
- If the exact manifest is unavailable, seek written clarification from the VirTues authors. Keep exposure status **unknown**, not “no overlap.”
- If overlap is found, do not use this checkpoint for an independent HCC validation claim. Consider a documented leave-one-cohort-out checkpoint only if the authors' published weights and provenance explicitly support it.

## Research consequences

- The current candidate checkpoint is not exposure-cleared.
- This is independent of the separate preprocessing blocker: even an exposure-cleared checkpoint cannot be applied as an official reproduction until image scaling, channel order, marker/UniProt mapping, mask semantics, and preprocessing are verified.
- A successful synthetic checkpoint load or CPU attention test establishes software compatibility only; it does not establish training-data independence or biological validity.
- Do not report target combinations, clinical utility, causal immune-evasion mechanisms, or patentability from this audit.

## Current status

**NO-GO for an independent held-out HCC claim.** Continue source-data and provenance checks without modifying original data or running outcome-driven analyses.
