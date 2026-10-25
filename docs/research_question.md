# Research question and scope

## Project direction

Cancer immunotherapy target discovery using computational models is the broad research area. The initially proposed robustness-only study now appears too incremental to carry a strong novelty claim, given Morpheus (2025), PHAROS (2026 preprint), spatial counterfactual core-bootstrap work at MICCAI 2026, and SPAD-CFR (Biology, 2026).

## Current recommendation

**Do not proceed with the original study as a novelty-led paper yet.** Investigate a more specific decision-level question instead:

> When spatial counterfactual methods propose molecular interventions for cancer immune activity, does a prespecified, target-budget-matched consensus across methods/cohorts identify intervention directions that replicate better in untouched patients and retain model-predicted immune uplift than the strongest single-method baseline?

This candidate may need to be narrowed further after checking compatible datasets, endpoints and intervention definitions. It is not a confirmed literature gap or an algorithm claim.

## Candidate alternatives

1. **Cross-method intervention decision utility.** Compare two or more methods only when they can be evaluated on a common data representation and same held-out patient endpoint. Test whether consensus changes decisions compared with best single method at equal target budget. Main risks: methods may predict different objects, and adapting them could itself introduce bias.
2. **Cross-cohort/platform transfer of signed target directions.** Test whether target directions discovered in one patient cohort/platform transfer to another using only preregistered shared markers and compatible outcomes. Main risks: small patient counts, incomplete overlap of channels, and cross-cohort prediction already being a mature field.
3. **Mechanistic admissibility of counterfactual interventions.** Test whether predicted target sets are consistent with prespecified molecular/signalling constraints and whether such constraints improve independent plausibility. Main risk: existing work already proposes biologically informed spatial counterfactuals and knowledge-graph constraints; adding a graph term is not enough.

## What was already established in the first audit

Morpheus applies counterfactual optimization to spatial proteomic tissue images, creates perturbations per patch, aggregates these into whole-tumour strategies, evaluates them in silico on held-out patients, and validates selected predictions in vitro. PHAROS searches target-directed combinations in single-cell perturbation space and uses controls/sample-based reranking. A MICCAI 2026 spatial transcriptomics method uses counterfactual neighbour replacement and core-level bootstrap evaluation. SPAD-CFR (Biology, 2026) generates spatial counterfactual tissue states and includes melanoma immune-focused interventions.

These methods make broad “AI for cancer immunotherapy”, generic combinations, spatial counterfactual generation, core-level bootstrap, or generic stability scoring insufficient as novelty claims.

## Required next gate

- Complete the Morpheus supplement audit.
- Compare the three alternatives against recent papers and preprints.
- Verify data licenses/terms and whether an endpoint is shared across methods.
- Create a feasibility matrix before choosing a new primary question.
- Reproduce a baseline only after rights and data access are clear.

## Definitions and guardrails

- Model-predicted uplift is a model output, not an observed treatment effect.
- Biological validity requires independent experiments or a well-justified orthogonal benchmark.
- Patient is the inferential unit; all cores/patches from one patient must remain together.
- Do not claim novelty, causal efficacy, clinical utility, or patentability before supporting evidence is available.
