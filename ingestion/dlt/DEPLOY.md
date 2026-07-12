# Deploying as a container (Cloud Scheduler -> Cloud Run Job -> BigQuery)

Implements the architecture from
[`docs/production-ingestion/NOTES.md`](../../docs/production-ingestion/NOTES.md):
`Cloud Scheduler (cron) -> HTTP+OAuth -> Cloud Run Job (this container) -> BigQuery`.

Not yet run — this is the deployment recipe to follow once a real store /
API token is available for the source being deployed. Placeholders below
assume the existing `mashburn-analytics-dev` GCP project (see
`../../CONNECTION.md`) and `us-central1` as the Cloud Run region (Cloud Run
needs a specific region; BigQuery data itself stays in the `US`
multi-region already in use).

Written for Shopify below; substitute `SOURCE=shiphero` (etc.) to deploy
another source — steps 1 and 6 (project setup, invoker account) are one-time
and shared across sources.

```bash
export PROJECT_ID=mashburn-analytics-dev
export REGION=us-central1
export REPO=mashburn-ingestion
export SOURCE=shopify
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${SOURCE}-dlt"
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
cd ingestion/dlt/${SOURCE}
gcloud builds submit --tag "$IMAGE" --project="$PROJECT_ID"
```

## 3. Store the source's API credential in Secret Manager

Never bake this into the image or the Dockerfile — it's injected as an env
var at deploy time. Shopify uses a single access token; ShipHero uses a
refresh token (see `shiphero/README.md`) — either way, one secret per
source.

```bash
printf '%s' 'REPLACE_WITH_REAL_TOKEN' | \
  gcloud secrets create "${SOURCE}-access-token" \
    --data-file=- \
    --project="$PROJECT_ID"
```

## 4. Runtime service account (least privilege)

A dedicated identity for the job itself — separate from whatever account
triggers it.

```bash
gcloud iam service-accounts create "${SOURCE}-dlt-runner" \
  --display-name="${SOURCE} dlt pipeline runtime" \
  --project="$PROJECT_ID"

RUNNER_SA="${SOURCE}-dlt-runner@${PROJECT_ID}.iam.gserviceaccount.com"

# Write access to BigQuery + ability to run query/load jobs
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${RUNNER_SA}" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${RUNNER_SA}" \
  --role="roles/bigquery.jobUser"

# Read access to the one secret it needs
gcloud secrets add-iam-policy-binding "${SOURCE}-access-token" \
  --member="serviceAccount:${RUNNER_SA}" \
  --role="roles/secretmanager.secretAccessor" \
  --project="$PROJECT_ID"
```

No BigQuery credentials file needed — `google-cloud-bigquery` (and dlt's
BigQuery destination) auto-detects the attached service account via the
Cloud Run metadata server, the same ADC mechanism used locally.

## 5. Deploy the Cloud Run Job

```bash
# Shopify example — env var names follow dlt's SOURCES__<source>__<field>
# convention (uppercased, "." -> "__"). ShipHero's secret is a refresh
# token so its env var is SOURCES__SHIPHERO__REFRESH_TOKEN instead.
gcloud run jobs deploy "${SOURCE}-dlt" \
  --image="$IMAGE" \
  --region="$REGION" \
  --project="$PROJECT_ID" \
  --service-account="$RUNNER_SA" \
  --set-secrets="SOURCES__SHOPIFY__ACCESS_TOKEN=${SOURCE}-access-token:latest" \
  --set-env-vars="SOURCES__SHOPIFY__SHOP_URL=https://your-store.myshopify.com" \
  --max-retries=1 \
  --task-timeout=15m
```

Env vars always win over `.dlt/secrets.toml` / `config.toml`, so nothing
else needs to change in the pipeline code.

Test it manually before scheduling:

```bash
gcloud run jobs execute "${SOURCE}-dlt" --region="$REGION" --project="$PROJECT_ID"
```

## 6. Invoker service account for Cloud Scheduler

A second, separate identity — Scheduler needs permission to *start* jobs,
not to do anything the jobs themselves do. **One-time, shared across all
sources** — `roles/run.developer` at the project level covers every Cloud
Run Job, so don't recreate this per source.

```bash
gcloud iam service-accounts create dlt-scheduler-invoker \
  --display-name="Cloud Scheduler invoker for dlt Cloud Run Jobs" \
  --project="$PROJECT_ID"

INVOKER_SA="dlt-scheduler-invoker@${PROJECT_ID}.iam.gserviceaccount.com"

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
gcloud scheduler jobs create http "${SOURCE}-dlt-daily" \
  --location="$REGION" \
  --schedule="0 6 * * *" \
  --uri="https://${REGION}-run.googleapis.com/apps/v1/namespaces/${PROJECT_ID}/jobs/${SOURCE}-dlt:run" \
  --http-method=POST \
  --oauth-service-account-email="$INVOKER_SA" \
  --project="$PROJECT_ID"
```

Runs daily at 06:00 in the scheduler location's timezone (defaults to UTC
unless `--time-zone` is set). Stagger source schedules (e.g. ShipHero at
`15 6 * * *`) so they're not all hitting BigQuery at once.

## Repeating this for other sources

Set `SOURCE=shiphero` (or `loop`, `swym`) and re-run steps 2-5 and 7 — each
source gets its own image, secret, runtime service account, and Scheduler
job. They don't share a container; keeping them independent means one
source's API outage doesn't block the others.
