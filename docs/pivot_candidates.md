# Pivot candidates after the October 2026 prior-art update

**Purpose:** choose the next research question by novelty, evidence and feasibility rather than committing to an algorithm prematurely.

Scores are expert planning judgments from the current targeted audit, not measured performance. "Novelty potential" is not a novelty finding.

| Candidate | Scientific question | Novelty potential (provisional) | Feasibility with current resources | Main risk | Decision |
|---|---|---:|---:|---|---|
| A. Cross-method intervention decision utility | Does a prespecified consensus across compatible spatial counterfactual methods identify interventions with better held-out-patient model-predicted immune uplift than the best single method, at equal target budget? | Medium, potentially stronger than a single-method stability score | Low–medium; intervention outputs/endpoints must be made comparable | Morpheus and SPAD-CFR do not natively generate identical intervention objects. A comparison can be invalid if forced onto a common scale after looking at results. | **Investigate first if common data/endpoint exists** |
| B. Cross-cohort/platform transfer of signed target direction | Do target directions discovered in one patient cohort or spatial platform transfer to an independent cohort with shared markers and a compatible endpoint? | Medium–high if truly independent, prespecified and biologically interpretable | Low–medium; marker intersection, access and endpoint compatibility are unknown | Cross-cohort prediction is already established; small independent patient counts and differing assays can make this underpowered or incoherent. | **High value but first check data compatibility** |
| C. Mechanistic admissibility / target plausibility | Do intervention sets that satisfy prespecified pathway, sign, druggability and molecular constraints outperform unconstrained suggestions on independent plausibility checks? | Low–medium without a new formal principle or strong empirical result | Medium for computational implementation, low for independent ground truth | Morpheus itself discusses interaction-graph constraints; SPAD-CFR is biologically informed and PHAROS contains admissibility checks. A graph regularizer alone is not novel. | **Do not lead with this without a sharper gap** |
| D. Original robustness-only benchmark | Re-run Morpheus with grouped patient resamples and seeds, calculate selection frequency/Jaccard and held-out uplift | Low as a standalone novelty-led paper; useful for reproducibility | Medium after data and compute gates; repeated optimization may be expensive | Very close to established bootstrap/stability practices; likely incremental unless it changes scientific decisions. | **No-go as the primary novelty claim; acceptable as an exploratory baseline** |

## Minimum decision tree

1. **Dataset/endpoint map first:** list every candidate dataset, platform, patient count, shared markers, target direction, label/end point, code/data access and license.
2. **Common-support test:** verify that at least two methods can generate comparable intervention hypotheses and can be evaluated on an identical untouched-patient endpoint. If not, Candidate A is invalid.
3. **Independent-transfer test:** verify whether an independent cohort has shared markers and the same or defensibly harmonizable endpoint. If not, Candidate B is invalid.
4. **Prior-art test:** search exact phrases and methods for intervention consensus, counterfactual transfer, target-direction stability, and clinically grounded intervention validation before selecting a gap.
5. **Choose exactly one primary question** only after these checks. Do not turn all options into one large project; that would make interpretation and MBBS-level execution harder.

## Recommended next move

Build a compact dataset/method compatibility table and conduct a targeted prior-art search for Candidates A and B. If no compatible dataset exists, pivot to an entirely different cancer-immunotherapy question rather than presenting generic robustness as invention. Do not claim patentability.
