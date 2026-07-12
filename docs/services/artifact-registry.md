# Artifact Registry

**What it is:** Google Cloud's managed container/package registry
(Docker Registry's successor on GCP). Holds the built images that
[Cloud Run Jobs](cloud-run-jobs.md) pulls from.

**In this project:** one Docker repository (`mashburn-ingestion`), with one
image per source (`shopify-dlt`, `shiphero-dlt`, ...) — matching the
one-container-per-source design (see
[Orchestration & Deployment](../architecture/orchestration-deployment.md)).

```bash
gcloud artifacts repositories create mashburn-ingestion \
  --repository-format=docker \
  --location=us-central1

# Build + push in one step — no local Docker daemon needed
gcloud builds submit --tag us-central1-docker.pkg.dev/PROJECT/mashburn-ingestion/shopify-dlt
```

**Status:** :jigsaw: designed, no repository actually created and no image
actually built/pushed yet.
