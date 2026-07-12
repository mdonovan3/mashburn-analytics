# Secret Manager

**What it is:** Google Cloud's managed secret storage — versioned,
IAM-controlled, encrypted at rest. Secrets are referenced by name (and
version, e.g. `:latest`) rather than embedded anywhere in code or images.

**In this project:** one secret per ingestion source (`shopify-access-token`,
`shiphero-access-token`, ...), holding the credential each dlt pipeline
needs (a static access token for Shopify, a refresh token for ShipHero).
Never baked into a Docker image — injected as an environment variable at
Cloud Run Job deploy time via `--set-secrets`, using dlt's
`SOURCES__<source>__<field>` env var convention so no code change is needed
between local development (`.dlt/secrets.toml`) and production (Secret
Manager-backed env var).

**Access control:** each source's runtime service account gets
`roles/secretmanager.secretAccessor` scoped to *only that one secret* — the
Shopify container can't read the ShipHero secret and vice versa, even
though they run in the same GCP project.

```bash
printf '%s' 'REPLACE_WITH_REAL_TOKEN' | \
  gcloud secrets create shiphero-access-token --data-file=-

gcloud secrets add-iam-policy-binding shiphero-access-token \
  --member="serviceAccount:shiphero-dlt-runner@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

**Status:** :jigsaw: designed, no secret actually created yet.
