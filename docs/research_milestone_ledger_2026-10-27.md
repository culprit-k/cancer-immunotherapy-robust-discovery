# Research milestone ledger — robust HCC immune-evasion discovery

Updated: 2026-10-27. This ledger distinguishes engineering readiness from scientific evidence. Do not describe the work as a validated discovery or publish a biological claim until the required gates pass.

## Milestone 1 — Public archive integrity (PASS, structural only)
- ICI archive checksum matched the recorded checksum.
- 86/86 image stacks, cell masks, and stromal masks were readable and paired by filename.
- All stacks had 45 channels; arrays were finite float32 in [0,1].
- All mask/image spatial shapes matched.
- Panel contains channels 1–45 without duplicates or gaps.
- Reproducible audit run: https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504894939
- This is file integrity, not evidence that the model understands the channels or that the masks mean what their labels suggest.

## Milestone 2 — Panel and mask semantics (IN PROGRESS)
- Preserve the extracted 45-channel panel CSV as a reference artifact.
- Verify the HCC discovery panel independently; never assume channel order matches the ICI cohort.
- Trace cell/stromal mask creation and label definitions to source metadata or methods. Until sourced, treat labels 3–9 as opaque IDs, not named cell classes.
- Resolve the 86 ROI images versus 84 clinical records using the original sample/ROI-to-patient crosswalk. No row-order matching and no outcome-driven exclusions.
- Output required: channel-to-marker crosswalk with source, mask-codebook evidence, and ROI→patient linkage audit.

## Milestone 3 — VirTues CPU synthetic preflight (BLOCKED)
- The pinned checkpoint identity is verified: SHA-256 714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f; 173,543,728 bytes; 356 tensors.
- The reversible CPU SDPA patch and packed-attention micro-smoke passed once.
- A later run failed because its preflight expected embedding width 768; official embedding files are (40,640) and the checkpoint projection is (512,640). The repository preflight has been updated to derive embedding width from the checkpoint tensor. Re-run the latest branch version and record exact commit and report.
- Required before next gate: import/attention smoke PASS, strict checkpoint load PASS, synthetic forward PASS. This is a software test only.

## Milestone 4 — Official preprocessing compatibility (NO-GO until proven)
- Compare raw archive generation, normalization, channel order, segmentation, tiling, masks, and inference input contracts with the official VirTues pipeline and publication.
- Do not treat [0,1] normalization as proof of compatibility. Do not silently reorder channels, invert intensities, or invent missing marker embeddings.
- Required output: executable preprocessing parity tests and a written go/no-go decision.

## Milestone 5 — Checkpoint exposure / licensing (CONDITIONAL)
- Current published-corpus audit does not support direct pretraining exposure, but no accession-by-accession author certification has been located.
- Keep checkpoint and source licence conditions documented. Do not commit weights or redistribute them.
- Clearly disclose the pretrained model, licence, possible exposure uncertainty, and the limitations of any exclusion claim.

## Milestone 6 — Cohort/endpoint lock and leakage prevention (NOT STARTED)
- Identify patient-level endpoint, time origin, treatment and follow-up definitions from source tables.
- Lock patient-level split before feature/target exploration; all ROIs from a patient stay in one split.
- Resolve missingness and inclusion/exclusion rules blind to outcome where possible.
- External ICI cohort is validation only; no tuning on it. Report patient counts, not just ROI counts.

## Milestone 7 — Baseline reproduction (NOT STARTED)
- Run a small, deterministic, pre-registered baseline only after Milestones 2–6 pass.
- Report all intended metrics, calibration/probability quality, uncertainty intervals, and exact software/data versions.
- Reconcile previous metric discrepancies before any model comparison; do not select metrics after seeing outcomes.

## Milestone 8 — Robust counterfactual candidate discovery (NOT STARTED)
- Define the estimand and counterfactual intervention constraints before analysis.
- Compare against non-counterfactual baselines and ablations; quantify patient/cohort stability and sensitivity to preprocessing.
- Candidate combinations are hypotheses, not causal mechanisms. Require independent validation and biological literature/context before interpretation.

## Milestone 9 — Manuscript and public release (NOT READY)
- Publish methods, cohort flow, licences, code, configs, seeds, environment, audit reports, negative results, limitations, and a reproducibility checklist.
- Never claim clinical utility, causality, novelty, patentability, or an immune-evasion mechanism without evidence.
- Current status: archive QC is reproducible; model preflight, preprocessing parity, cohort linkage, and biological validation remain unresolved.
