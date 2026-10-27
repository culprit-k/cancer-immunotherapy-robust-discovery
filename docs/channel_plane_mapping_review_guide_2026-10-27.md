# Channel-plane map review template

The CSV lists the published panel targets and a *candidate* zero-based plane sequence based on panel row order. Every row is intentionally marked `pending_review`. Do not set it to `verified` merely to make the script run.

Review the actual TIFF stack axes and the source acquisition/preprocessing documentation. Add traceable evidence to each row (for example, a source file and page/section or a documented reproducible export statement) and change `verification_status` to `verified` only when you can defend the exact plane-to-marker correspondence. If channel order is not established by available records, request clarification from the data authors rather than assuming the panel row order.

After review, save a private copy outside GitHub and pass it as `--reviewed-channel-map` to `scripts/run_hcc_spatial_marker_coupling.py`. The runner fails closed while any row is pending. Do not commit the reviewed copy or patient-level output CSVs.

Source panel metadata: `data/reference/ICI_ICICohort_panel_verified_2026-10-27.csv`. The candidate sequence is not itself verification.
