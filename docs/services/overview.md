# Services & Tools — Overview

Short reference docs for every tool/service involved in this project,
including the ones evaluated and *not* chosen — the reasoning behind a
rejection is often as useful to have written down as the reasoning behind
a choice.

## In use

| Service | Role | Status |
|---|---|---|
| [dbt](dbt.md) | SQL transformation / modeling framework | :white_check_mark: project scaffolded and running; model SQL itself is stubbed — see [Data Modeling](../data-modeling/overview.md) |
| [dlt](dlt.md) | Python data-loading library — extraction + incremental state + schema | :jigsaw: 2 of 5 sources scaffolded |
| [BigQuery](bigquery.md) | Data warehouse | :white_check_mark: in use, mock data loaded |
| [Cloud Run Jobs](cloud-run-jobs.md) | Runs the ingestion (and proposed dbt) containers | :jigsaw: designed, not deployed |
| [Cloud Scheduler](cloud-scheduler.md) | Cron trigger for Cloud Run Jobs | :jigsaw: designed, not deployed |
| [Secret Manager](secret-manager.md) | Holds per-source API credentials | :jigsaw: designed, not deployed |
| [Artifact Registry](artifact-registry.md) | Hosts container images | :jigsaw: designed, not deployed |
| MkDocs + Material | This documentation site | :white_check_mark: built, `mkdocs serve` locally |

## Evaluated, not chosen

Fivetran, Airbyte, Portable, Hevo (managed ELT platforms) — see
[Evaluated, not chosen](evaluated-not-chosen.md) for the full comparison
and why dlt won instead.

## See also

[Managed vs. Self-Hosted](../architecture/managed-vs-self-hosted.md) — the
cost/pros/cons comparison that ties these services together into an actual
recommendation, sized to Mashburn's scale.
