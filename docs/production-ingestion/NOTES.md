# Production Ingestion Architecture — Research Notes

Context: this repo's `ingestion/` scripts load *mock* data for local dbt practice.
These notes are about how the real pipeline would work if Mashburn brought
ingestion in-house from an outsourced vendor, landing in BigQuery. Useful
reference for interview discussion of "how would you actually build this."

## Sources and real connector coverage

| Source | Fivetran | Airbyte | Portable | Hevo |
|---|---|---|---|---|
| Shopify | native | native | native | native |
| ShipHero | native | no real connector (marketing pages only, not in their catalog/repo) | native | not confirmed |
| Loop Returns | native | not found | native | not confirmed |
| Swym | not found | not found | buildable on request (custom, ~days) | not confirmed |

Note: Portable and some other vendors run auto-generated SEO pages of the form
"Does Airbyte offer a ShipHero connector? Portable does!" for nearly every
tool x tool combination, regardless of whether the claim is true. Always
verify against the vendor's own docs domain (e.g. `fivetran.com/docs/...`),
not comparison/marketing pages.

## Managed options considered (cheaper than Fivetran)

1. **Portable.io** — flat-rate pricing (not volume/MAR-based), already has
   real Shopify/ShipHero/Loop Returns connectors, builds niche ones (Swym)
   on request. Best fit if no dedicated data-eng headcount yet — probably
   the fastest way to actually replace an outsourced vendor.
2. **Airbyte Cloud / self-hosted** — cheapest at real scale (~$16K/yr median
   contract vs. Fivetran's ~$44K/yr per public reporting). Native Shopify
   connector; ShipHero/Loop/Swym would need custom low-code CDK connectors
   built and maintained in-house.
3. **dlt (open source) + serverless orchestration** — free library, no
   platform fee. Chosen direction for this project (see below).

## Chosen direction: dlt + Cloud Run Jobs + Cloud Scheduler

- **dlt** (Python) handles extraction/loading/schema evolution. Shopify has
  a well-trodden REST API path; ShipHero, Loop Returns, and Swym each need a
  custom dlt REST source (no verified/pre-built dlt source exists for them).
- **Cloud Run Jobs** runs the container. Any language works (just a Linux
  container that exits 0/non-zero), but dlt is Python-only, so the pipeline
  stays Python. Official base images cover Go/Java/Node/PHP/Python/Ruby/.NET;
  R also works via a custom `rocker`-based image if ever needed, but dlt has
  no R client, so R would mean hand-rolling API calls + `bigrquery` loads —
  not worth it here since dlt already does this in Python.
- **Cloud Scheduler** is just the cron trigger (HTTP/Pub/Sub/App Engine
  targets) — it doesn't run code itself. For Cloud Run Jobs specifically it
  calls the Cloud Run Admin API's `jobs:run` method (an OAuth-authenticated
  call to a `*.googleapis.com` endpoint, not OIDC — OIDC is for triggering
  your own HTTP endpoints, e.g. a Cloud Run *Service*). That API call starts
  a fresh Execution: a new container pulled from the image, run once,
  destroyed on exit — no warm/idle instance between runs.
- Flow: `Cloud Scheduler (cron) → OAuth → Cloud Run Admin API (jobs:run) → new container Execution (Python/dlt) → BigQuery`
- Why not a full orchestrator (Airflow/Dagster/Composer): overkill for 4
  independent, non-interdependent source pulls. That machinery earns its
  cost at dozens+ of interdependent jobs. Tradeoff: no managed
  retry/alerting UI — cover failures with a Slack webhook / Sentry call in
  the pipeline's `except` block instead.

## Open items / not yet built

- Shopify dlt source scaffolded at `ingestion/dlt/shopify/` — orders,
  customers, products, product_variants, locations, inventory_levels, all
  incremental on `updated_at`. Not yet run end-to-end; no live store
  connected to this portfolio project.
- ShipHero dlt source scaffolded at `ingestion/dlt/shiphero/` —
  `shipments` resource against ShipHero's GraphQL API (not REST — uses a
  hand-rolled `requests`-based resource since dlt's REST API helper doesn't
  fit GraphQL, plus a refresh-token exchange since ShipHero access tokens
  expire every 28 days). Only the fields confirmed from ShipHero's public
  docs/examples are queried; the extra boolean flags in the mock schema
  (`delivered`/`completed`/`picked_up`/`needs_refund`/`refunded`) and
  `shipping_labels.tracking_url`/`.status` are NOT confirmed to exist on the
  real API — check the schema browser at developer.shiphero.com/schema
  before trusting those. Not yet run end-to-end.
- Container + deploy recipe scaffolded and generalized across sources:
  `ingestion/dlt/DEPLOY.md` (Artifact Registry build, Secret Manager per
  source, separate runtime service accounts + one shared invoker account,
  `gcloud scheduler jobs create http` targeting the Cloud Run Jobs Admin API
  with OAuth). Also not yet run — needs real credentials to actually execute.
- No dlt sources written yet for Loop Returns or Swym (APIs are documented,
  just not scaffolded). Each would get its own image/Job/secret per the
  "repeating this" section of DEPLOY.md.
- Portable sales conversation would be needed to get real pricing before
  committing to option 1 vs. self-built option 3.
