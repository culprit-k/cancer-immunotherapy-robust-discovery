# HCC–VirTues data contract and provenance
**Status:** required-input specification. Does not assert that the required artifacts are present or validated.

## Required private/local inputs
1. Immutable source archive with URL/accession, download date, archive hash (SHA-256), expected file count, rights/usage record, and source citation.
2. One manifest row per ROI with a pseudonymous patient key, ROI key, image path, cell-mask path, stromal-mask path, marker-map version, acquisition/source cohort, and QC status.
3. Ordered channel map: channel index, exact marker label, official protein identifier (e.g. UniProt where applicable), source nomenclature, intensity units/normalization description, and mapping evidence.
4. QC report: array shape and axes, dtype, finite fraction, min/max/quantiles, unique mask labels, empty-mask flags, image–mask dimension match, spatial alignment, duplicate files, corrupted files, and missing triplets.
5. Cohort crosswalk resolving the clinical table's 84 ROI count versus the 86 image/mask triplets, especially ICI_24 and ICI_39. Preserve unresolved status rather than guessing.
6. Checkpoint record: official repository, immutable commit/revision, model config/architecture, weight file hash, licence, training-set inventory, and evidence that the HCC evaluation cohort was not included in pretraining.
7. Preprocessing record: exact input semantics, order of transforms, clipping/log parameters, normalization statistics, smoothing, tissue mask, software versions, and any deviations.
8. Endpoint data dictionary from the source, with each field's definition, units, missingness semantics, time origin, censoring/event coding, and response criteria.
9. Software environment lockfile, random seeds, run command, logs, and exact code commits.

## Data protection and repository boundaries
- Raw image arrays/masks, model weights, clinical rows and patient-level crosswalks stay in private/local storage unless rights and privacy review explicitly permit release.
- Public repository may store aggregate reports, schemas, scripts, manifests without patient identity, hashes, and source citations.
- Never push tokens, credentials, private author correspondence, or protected data.
- Use stable pseudonymous IDs locally and do not upload re-identification keys.
- Cite the source and respect both dataset and checkpoint licences; do not assume that a paper's open-access licence automatically defines every attached model-weight licence.

## Key known unresolved items
- TIFF images are described in the previous audit as PENGUIN-normalized to [0,1]; official VirTues preprocessing is not established as equivalent.
- Exact ordered marker/channel map and UniProt mapping remain unverified.
- Tensor compatibility and mask semantics are not established by filenames alone.
- ICI_24 and ICI_39 ROI counts remain discrepant.
- `virtues-imc14` is the leading checkpoint candidate after paper-level cohort screening; the exact checkpoint-release-to-supplement cohort mapping and pinned code/config still need final confirmation. Its model-file SHA-256 and CC BY-NC 4.0 terms are recorded in `docs/virtues_checkpoint_provenance_2026-10-26.md`.
- The virtues-sp32 checkpoint is ineligible for held-out evaluation because the Salié HCC cohort is included in its training corpus; virtues-sp31 requires omitted-cohort confirmation.

## Definition of ready
No input is considered ready merely because a filename exists. Ready requires schema validation, hash match, mapping verification, tensor QC, documented preprocessing and checkpoint provenance, plus resolution or explicit quarantine of every discrepancy.
