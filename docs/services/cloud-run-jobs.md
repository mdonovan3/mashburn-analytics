# Cloud Run Jobs

**What it is:** the batch-execution sibling of Cloud Run's more familiar
Service type. A Job runs a container **to completion** — no server, no
listening port, no idle instance kept warm. You're billed only for the
seconds the container actually runs.

**Execution model:** each trigger (manual, `gcloud run jobs execute`, or a
Cloud Scheduler call) starts a new **Execution**, which spins up one or
more **Tasks** (independent container instances). The container is pulled
fresh from [Artifact Registry](artifact-registry.md), runs your `CMD`
start-to-finish, and its exit code decides the outcome: `0` = success,
non-zero = failure (retried up to `--max-retries` times). Either way the
container is destroyed afterward.

**Why this over Cloud Run Services or a VM** for this project's ingestion
containers: nothing here needs to be "always on" — it's 4-5 independent
scheduled pulls, a few minutes each, a handful of times a day. A Service
would sit idle (and potentially billed) between runs; a VM needs patching
and babysitting. A Job is the shape that matches the actual workload.

**Language support:** any Linux container — Google publishes official base
images for Go/Java/Node/PHP/Python/Ruby/.NET, but since the only contract
is "exit 0 on success," anything works, including R via a custom `rocker`
image. This project stays Python since [dlt](dlt.md) is Python-only.

**Used for, in this project:** one Job per ingestion source (`shopify-dlt`,
`shiphero-dlt`, ...), and proposed for the dbt run step too — see
[Managed vs. Self-Hosted](../architecture/managed-vs-self-hosted.md).

**Status:** :jigsaw: designed (`ingestion/dlt/*/Dockerfile`,
`ingestion/dlt/DEPLOY.md`), no Job actually deployed yet.
