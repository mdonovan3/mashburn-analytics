# dlt Pipelines (production-style scaffold)

Scaffolds the "real" ingestion path described in
[`docs/production-ingestion/NOTES.md`](../../docs/production-ingestion/NOTES.md):
dlt extracts from each source's API and loads straight to BigQuery, with
incremental state and schema evolution handled by dlt instead of the
hand-rolled batch loader in `ingestion/load_to_bigquery.py`.

This is additive — the mock ingestion scripts one level up are unaffected
and remain the way to populate `raw_*` datasets for local dbt development
without live source connections.

Each source is its own subfolder, its own image, and (per `DEPLOY.md`) its
own Cloud Run Job — kept independent so one source's API outage or schema
change doesn't block the others.

| Source | Folder | Status |
|---|---|---|
| Shopify | [`shopify/`](shopify/README.md) | Scaffolded, not yet run end-to-end |
| ShipHero | [`shiphero/`](shiphero/README.md) | Scaffolded, not yet run end-to-end |
| Loop Returns | not started | — |
| Swym | not started | — |

## Running as a container

See [`DEPLOY.md`](DEPLOY.md) for the shared `Dockerfile` + `Cloud Scheduler
-> Cloud Run Job -> BigQuery` deployment recipe — same steps for every
source, just swap the folder/image/secret name.
