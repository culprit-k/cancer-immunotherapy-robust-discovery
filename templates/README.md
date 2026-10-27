# Private input templates

These header-only templates define the minimum metadata contract for local validation.

- Fill the ROI manifest only in a private/local workspace. Use a study-specific pseudonymous patient key and one row per ROI. Do not commit filled manifests to public GitHub.
- Use paths that exist from the local machine running the validator. Keep all ROIs from the same patient tied to the same patient key.
- Populate channel indexes in the exact array order, not alphabetical order. Map markers using the source panel annotation and authoritative protein identifier; never guess unresolved IDs. Record the evidence.
- Set qc_status to pending until image/mask tensor checks are completed. A metadata-only pass is not evidence of spatial alignment or model compatibility.
- The templates do not contain any patient data and are not completed manifests.
