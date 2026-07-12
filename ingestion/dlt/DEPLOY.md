# Deploying as a container (Cloud Scheduler -> Cloud Run Job -> BigQuery)

Implements the architecture from
[`docs/production-ingestion/NOTES.md`](../../docs/production-ingestion/NOTES.md):
`Cloud Scheduler (cron) -> HTTP+OAuth -> Cloud Run Job (this container) -> BigQuery`.

Not yet run — this is the deployment recipe to follow once a real Shopify
store + access token are available. Placeholders below assume the existing
`mashburn-analytics-dev` GCP project (see `../../CONNECTION.md`) and
`us-central1` as the Cloud Run region (Cloud Run needs a specific region;
BigQuery data itself stays in the `US` multi-region already in use).

```bash
export PROJECT_ID=mashburn-analytics-dev
export REGION=us-central1
export REPO=mashburn-ingestion
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/shopify-dlt"
```

## 1. One-time project setup

```bash
gcloud services enable \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  --project="$PROJECT_ID"

gcloud artifacts repositories create "$REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --project="$PROJECT_ID"
```

## 2. Build and push the image

```bash
cd ingestion/dlt
gcloud builds submit --tag "$IMAGE" --project="$PROJECT_ID"
```

## 3. Store the Shopify access token in Secret Manager

Never bake this into the image or the Dockerfile — it's injected as an env
var at deploy time.

```bash
printf '%s' 'shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxx' | \
  gcloud secrets create shopify-access-token \
    --data-file=- \
    --project="$PROJECT_ID"
```

## 4. Runtime service account (least privilege)

A dedicated identity for the job itself — separate from whatever account
triggers it.

```bash
gcloud iam service-accounts create shopify-dlt-runner \
  --display-name="Shopify dlt pipeline runtime" \
  --project="$PROJECT_ID"

RUNNER_SA="shopify-dlt-runner@${PROJECT_ID}.iam.gserviceaccount.com"

# Write access to BigQuery + ability to run query/load jobs
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${RUNNER_SA}" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${RUNNER_SA}" \
  --role="roles/bigquery.jobUser"

# Read access to the one secret it needs
gcloud secrets add-iam-policy-binding shopify-access-token \
  --member="serviceAccount:${RUNNER_SA}" \
  --role="roles/secretmanager.secretAccessor" \
  --project="$PROJECT_ID"
```

No BigQuery credentials file needed — `google-cloud-bigquery` (and dlt's
BigQuery destination) auto-detects the attached service account via the
Cloud Run metadata server, the same ADC mechanism used locally.

## 5. Deploy the Cloud Run Job

```bash
gcloud run jobs deploy shopify-dlt \
  --image="$IMAGE" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --service-account="$RUNNER_SA" \
  --set-secrets="SOURCES__SHOPIFY__ACCESS_TOKEN=shopify-access-token:latest" \
  --set-env-vars="SOURCES__SHOPIFY__SHOP_URL=https://your-store.myshopify.com" \
  --max-retries=1 \
  --task-timeout=15m
```

`SOURCES__SHOPIFY__ACCESS_TOKEN` / `SOURCES__SHOPIFY__SHOP_URL` follow dlt's
env var convention — `SOURCES__<source name>__<field>`, uppercased, `.`
replaced with `__`. Env vars always win over `.dlt/secrets.toml` /
`config.toml`, so nothing else needs to change in the pipeline code.

Test it manually before scheduling:

```bash
gcloud run jobs execute shopify-dlt --region="$REGION" --project="$PROJECT_ID"
```

## 6. Invoker service account for Cloud Scheduler

A second, separate identity — Scheduler needs permission to *start* the
job, not to do anything the job itself does.

```bash
gcloud iam service-accounts create shopify-dlt-invoker \
  --display-name="Cloud Scheduler invoker for shopify-dlt" \
  --project="$PROJECT_ID"

INVOKER_SA="shopify-dlt-invoker@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${INVOKER_SA}" \
  --role="roles/run.developer"
```

## 7. Cloud Scheduler job

Cloud Run Jobs are started via the Cloud Run Admin API (`jobs:run`), not a
plain HTTP endpoint on the job itself — so the Scheduler target is the
`run.googleapis.com` API, authenticated with an **OAuth** token (not OIDC;
OIDC is for your own HTTP endpoints, Google APIs on `*.googleapis.com`
expect OAuth).

```bash
gcloud scheduler jobs create http shopify-dlt-daily \
  --location="$REGION" \
  --schedule="0 6 * * *" \
  --uri="https://${REGION}-run.googleapis.com/apps/v1/namespaces/${PROJECT_ID}/jobs/shopify-dlt:run" \
  --http-method=POST \
  --oauth-service-account-email="$INVOKER_SA" \
  --project="$PROJECT_ID"
```

Runs daily at 06:00 in the scheduler location's timezone (defaults to UTC
unless `--time-zone` is set).

## Repeating this for ShipHero / Loop Returns / Swym

Once those dlt sources exist, each gets its own Artifact Registry image,
Cloud Run Job, runtime service account (or a shared one with the same
BigQuery roles), and Scheduler job — same recipe, different secret name and
image tag. They don't need to share a container; keeping them independent
means one source's API outage doesn't block the others.
