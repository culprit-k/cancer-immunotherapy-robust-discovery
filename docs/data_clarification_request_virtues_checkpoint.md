# Data clarification request — VirTues checkpoint exposure

**Purpose:** Obtain an author-confirmed provenance record for the pretrained VirTues checkpoint selected for the HCC study. This draft has **not** been sent.

## Public evidence already reviewed

- Official VirTues paper (Nature, 2026): https://www.nature.com/articles/s41586-026-10884-y
- Official model/code repository: https://github.com/bunnelab/virtues
- Pinned checkpoint: `bunnelab/virtues/virtues-imc14/model.safetensors`
- Immutable revision: `43fd00fce052c46f9e0cc1a87f42806620632319`
- SHA-256: `714efed862f4a4b5cfd13f91e1ab8a7589f1295bd1735f827b4f8d4806cde28f`
- HCC discovery accession: https://zenodo.org/records/10793609
- HCC ICI accession: https://zenodo.org/records/10794904

The paper states that the IMC-only core model uses 14 IMC datasets and that the extended multi-technology corpus adds seven additional IMC datasets corresponding to references 90–96. Salié et al. is reference 95. This is strong publication-level evidence that the HCC study is not directly included in the core-14 `virtues-imc14` training inventory; it is not a separate signed accession-to-checkpoint training certificate.

## Questions for the authors/model maintainers

1. Can you confirm that neither Zenodo accession 10.5281/zenodo.10793609 (54-patient discovery) nor 10.5281/zenodo.10794904 (42-patient ICI cohort), nor derived images/ROIs from Salié et al., were used in pretraining, fine-tuning or any other training step for the exact `virtues-imc14/model.safetensors` file at revision `43fd00fce052c46f9e0cc1a87f42806620632319`?
2. Is there a checkpoint-specific dataset manifest or training record that identifies the exact core-14 datasets and can be cited or archived for reproducible evaluation?
3. Which dataset is omitted from `virtues-sp31` relative to `virtues-sp32`? This matters because the public README lists 31 versus 32 training cohorts but does not identify the omitted cohort.
4. Are there any dataset-specific fine-tuning or downstream-adaptation steps that would change the pretraining exposure assessment for the published `virtues-imc14` weights?

## Draft email

**Subject:** Request for training-corpus provenance of VirTues IMC14 checkpoint

Dear VirTues team,

I am preparing a reproducible academic evaluation of virtual-marker reconstruction on the Salié et al. HCC imaging-mass-cytometry cohorts (Zenodo records 10793609 and 10794904). I have pinned the official `virtues-imc14/model.safetensors` checkpoint at revision `43fd00fce052c46f9e0cc1a87f42806620632319` and verified its SHA-256.

The Nature paper appears to place the Salié study (reference 95) among the seven additional IMC cohorts used in the extended corpus rather than the core-14 IMC model. To document the evaluation correctly, could you confirm whether both HCC accessions and any derived images were excluded from all training stages for this exact checkpoint? If available, a checkpoint-specific dataset manifest would be very helpful. Could you also clarify which cohort is omitted from the `virtues-sp31` variant compared with `virtues-sp32`?

I will respect the model-weight licence and will not redistribute the weights or source data. The confirmation would be used only to document model exposure accurately in the study.

Thank you for your time and for releasing the framework.

Kind regards,  
[Your name]  
[Institution / supervisor, if applicable]

## Decision rule

- If the authors confirm exclusion for the pinned `virtues-imc14` checkpoint, record their response and use it as an accession-level provenance certificate.
- If they cannot confirm, retain the published-corpus conclusion only and describe exposure as “excluded according to the published core-versus-extended corpus inventory,” not as author-certified.
- Do not use `virtues-sp31` as an HCC-held-out checkpoint until the omitted dataset is identified and checked.
- The model's non-commercial weight licence remains independent of training-exposure status.
