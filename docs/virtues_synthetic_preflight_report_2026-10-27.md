# VirTues checkpoint + synthetic CPU preflight report (2026-10-27)

## Result

**PASS_SYNTHETIC_PREFLIGHT_ONLY.** This report records a real run in GitHub Actions against the official VirTues source and pinned public IMC14 model checkpoint. It is not an HCC inference result.

- Workflow run: [VirTues checkpoint and synthetic model preflight #1](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504248041)
- Report artifact: [Download the JSON report from the workflow run](https://github.com/culprit-k/cancer-immunotherapy-robust-discovery/actions/runs/40504248041/artifacts/12734062500)
- Research revision used by the run: `4ff69f09a321043cdf19e86c5c220fc09ae8a1a7`
- Official VirTues source commit: `2c9c6cba1ee796c4d8dff9329175c47e4a72f409`
- Model weights source: Hugging Face `bunnelab/virtues`, revision `43fd00fce052c46f9e0cc1a87f42806620632319`
- Runtime: Python 3.12.15, PyTorch 2.14.1+cu130, CUDA unavailable; model executed on CPU.

## Verified checks

| Check | Observed result |
|---|---|
| Official source tree and configuration present | PASS |
| Reversible CPU SDPA patch | PASS; original source backed up in the ephemeral CI runner |
| Checkpoint size | 173,543,728 bytes; exact expected size |
| Checkpoint SHA-256 | `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`; exact expected hash |
| Checkpoint tensor count | 356; exact expected count |
| Packed CPU attention smoke test | PASS; input/output shape `(1, 7, 16)`, finite output, packed segments 3 and 4 |
| Strict checkpoint load | PASS; `strict=True`, zero missing keys, zero unexpected keys |
| Official example marker embeddings | `(40, 640)`; compatible with checkpoint projection width 640 |
| Synthetic model forward | PASS; input `(2, 16, 16)`, output `(2, 16, 16)`, finite output |

The 640-dimensional example embeddings are consistent with the checkpoint tensor `encoder.prior_embedding_encoder.weight` of shape `(512, 640)`. The earlier fixed 768-dimensional check was incorrect and has been replaced by a check derived from the pinned checkpoint.

## Interpretation and boundaries

This resolves the current *software/checkpoint execution* blocker in the accessible CI environment. It demonstrates that the official pinned architecture can strict-load the pinned checkpoint and complete a tiny synthetic CPU forward pass under the reversible SDPA fallback.

It does **not** demonstrate that:
- normalized HCC TIFFs match the VirTues preprocessing used during training;
- TIFF channel order has been authoritatively mapped to the panel/UniProt embeddings;
- stromal-mask codes have known biological definitions;
- the HCC discovery/ICI crosswalk is fully resolved;
- reconstruction, counterfactual optimization, target ranking or any clinical model has run;
- any immune-evasion mechanism, biomarker, therapeutic effect, novelty or patentability has been demonstrated.

No HCC image, mask, or patient outcome was loaded by this workflow. The model weights were downloaded only into ephemeral CI storage and were not committed to this repository. The experimental CPU patch is also not evidence of numerical equivalence to FlashAttention in general; the result is a shape/runtime smoke test.

## Next scientific gate

Proceed with outcome-blind HCC data compatibility audits only: actual image/mask tensor shapes, channel ordering and marker identities, stromal-mask definitions, expected ROI counts from the authoritative supplementary table, and the preprocessing-source mismatch. Do not run the outcome analysis or make biological claims until those gates are resolved.

## References

- VirTues official source: https://github.com/bunnelab/virtues
- VirTues paper: https://doi.org/10.1038/s41586-026-10884-y
- ICI cohort data and documentation: https://doi.org/10.5281/zenodo.10794904
- HCC discovery cohort data and documentation: https://doi.org/10.5281/zenodo.10793609
