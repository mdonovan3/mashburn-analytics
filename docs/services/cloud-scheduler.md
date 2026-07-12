# Cloud Scheduler

**What it is:** Google Cloud's fully managed cron service. It doesn't run
any code itself — it just fires on a schedule (standard cron syntax) and
hits one of three target types: HTTP/S, Pub/Sub, or App Engine.

**How it triggers a Cloud Run Job (the pattern used here):** Cloud Run Jobs
don't expose a plain HTTP endpoint the way a Cloud Run *Service* does —
they're started via the **Cloud Run Admin API**'s `jobs:run` method. So the
Scheduler target is an HTTP call to
`https://{region}-run.googleapis.com/.../jobs/{job}:run`, authenticated
with an **OAuth** token (not OIDC — OIDC is for calling your own HTTP
endpoints; Google's own `*.googleapis.com` APIs expect OAuth). That call
just tells the Admin API to start a new Execution; Scheduler's job is done
once the API acknowledges the request.

```bash
gcloud scheduler jobs create http shopify-dlt-daily \
  --schedule="0 6 * * *" \
  --uri="https://us-central1-run.googleapis.com/apps/v1/namespaces/PROJECT/jobs/shopify-dlt:run" \
  --http-method=POST \
  --oauth-service-account-email=INVOKER_SA
```

**Identity:** a dedicated "invoker" service account with only
`roles/run.developer` — enough to start a Job, nothing else. Kept separate
from the Job's own runtime service account (which has BigQuery + secret
access) — Scheduler can start work, it can't do the work itself.

**Status:** :jigsaw: designed (`ingestion/dlt/DEPLOY.md` has the full
command), no Scheduler job actually created yet.
