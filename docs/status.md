# Status & Roadmap

Single rollup of every piece of the ecosystem. See [index.md](index.md) for
the status legend (:white_check_mark: Implemented / :jigsaw: Scaffolded /
:clipboard: Planned).

## Ingestion

| Piece | Status | Detail |
|---|---|---|
| Mock data generators | :white_check_mark: Implemented | [Ingestion Layer](architecture/ingestion.md#mock-path) |
| BigQuery loader (mock → raw_*) | :white_check_mark: Implemented | same |
| dlt — Shopify | :jigsaw: Scaffolded, not run live | [Shopify](data-sources/shopify.md) |
| dlt — ShipHero | :jigsaw: Scaffolded, not run live | [ShipHero](data-sources/shiphero.md) |
| dlt — Loop Returns | :clipboard: Planned | [Loop Returns](data-sources/loop-returns.md) |
| dlt — Swym | :clipboard: Planned | [Swym](data-sources/swym.md) |
| dlt — Klaviyo | :clipboard: Planned, not researched | [Klaviyo](data-sources/klaviyo.md) |

## Data modeling (dbt)

| Piece | Status | Detail |
|---|---|---|
| Project scaffolding, `sources.yml`, source tests | :white_check_mark: Implemented | [Data Modeling](data-modeling/overview.md) |
| Staging SQL (15 models) | :clipboard: Planned — stubbed | [Staging](data-modeling/staging.md) |
| Intermediate SQL (5 models) | :clipboard: Planned — stubbed | [Intermediate](data-modeling/intermediate.md) |
| Marts SQL (7 models) | :clipboard: Planned — stubbed | [Marts](data-modeling/marts.md) |
| dbt-on-Cloud-Run-Jobs (proposed prod runner) | :clipboard: Planned — proposal only | [Managed vs. Self-Hosted](architecture/managed-vs-self-hosted.md) |

## Orchestration & deployment

| Piece | Status | Detail |
|---|---|---|
| Container recipe (Dockerfiles) | :jigsaw: Scaffolded | [Orchestration & Deployment](architecture/orchestration-deployment.md) |
| Deploy command sequence (`DEPLOY.md`) | :jigsaw: Scaffolded (documented, untested) | same |
| Artifact Registry repo | :clipboard: Planned — not created | [Artifact Registry](services/artifact-registry.md) |
| Secret Manager secrets | :clipboard: Planned — not created | [Secret Manager](services/secret-manager.md) |
| Cloud Run Jobs | :clipboard: Planned — not deployed | [Cloud Run Jobs](services/cloud-run-jobs.md) |
| Cloud Scheduler jobs | :clipboard: Planned — not created | [Cloud Scheduler](services/cloud-scheduler.md) |

## Research / decisions

| Piece | Status |
|---|---|
| Managed ELT platform evaluation (Fivetran/Airbyte/Portable/Hevo) | :white_check_mark: Done | 
| dlt chosen over managed platform | :white_check_mark: Decided |
| Self-hosted vs. dbt Cloud for modeling | :white_check_mark: Decided (self-hosted proposed) |
| Loop Returns platform identity confirmed (vs. a competitor) | :clipboard: Not done — only the subdomain pattern is confirmed |
| Klaviyo actually in use, confirmed | :clipboard: Not done |
| Company sizing (store count, catalog size, revenue-derived order volume) | :white_check_mark: Done, from public sources — see [Managed vs. Self-Hosted](architecture/managed-vs-self-hosted.md#estimated-data-volumes) |
| Customer identity resolution across sources checked against real API docs | :white_check_mark: Done — see [Customer Identity & Conversion Tracking](architecture/customer-identity.md) |
| `SWYM_WISHLIST_EVENTS` mock schema missing email field | :white_check_mark: Fixed — `customer_email` added to `schemas.py`, both mock generators, and `sources.yml` |
| `int_customer_identity` dbt model | :clipboard: Planned — same page |

## Documentation

| Piece | Status |
|---|---|
| This site (MkDocs + Material) | :white_check_mark: Implemented, local |
| GitHub Pages hosting | :clipboard: Proposed — pending a go-ahead (repo is already public, so this is low-risk) |

## What "done" would look like next, in order

1. Write real staging SQL (unblocks everything downstream in dbt)
2. Run the Shopify and ShipHero dlt pipelines against real credentials —
   validates the scaffolded code actually works, not just compiles
3. Deploy one source (Shopify, simplest) end-to-end through
   [Orchestration & Deployment](architecture/orchestration-deployment.md) as
   a proof of the whole pattern before repeating it 3 more times
4. Confirm Loop Returns' actual platform identity and Klaviyo's actual
   presence before scaffolding either
5. Write intermediate + marts SQL
6. Stand up the dbt-on-Cloud-Run-Jobs runner
