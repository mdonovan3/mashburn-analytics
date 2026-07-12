# BigQuery

**What it is:** Google Cloud's serverless, columnar data warehouse.
Pay-per-query (or flat-rate/capacity pricing at larger scale) — no cluster
to size or manage, which is a large part of why it fits a small team well.

**In this project:** project `mashburn-analytics-dev`, region `US`
(multi-region). Datasets: `raw_shopify`, `raw_shiphero`, `raw_swym`,
`raw_loop`, `raw_klaviyo` (loaded by both the mock generators and, once
run, the dlt pipelines), plus `staging`/`marts` datasets dbt builds into.
Full connection details (R/`bigrquery`, DataGrip, ADC setup) in
[`CONNECTION.md`](https://github.com/mdonovan3/mashburn-analytics/blob/main/CONNECTION.md).

**Auth pattern used throughout this project:** Application Default
Credentials (ADC) — `gcloud auth application-default login` locally, or the
attached service account's identity automatically when running in Cloud
Run. No service account key file anywhere in this project, by design (keys
are a standing credential-leak risk; ADC/attached-identity auth has nothing
to leak).

**BigQuery-specific modeling notes** (see
[Warehouse & Modeling](../architecture/warehouse-modeling.md) for more):

- Partitioning/clustering defined in dbt `config()`, not raw DDL
- Always filter on the partition column directly (`WHERE DATE(created_at) >= ...`),
  never a derived expression (`WHERE EXTRACT(YEAR FROM created_at) = ...`) —
  the latter defeats partition pruning
- Nested/repeated fields (Shopify `line_items`, ShipHero `shipping_labels`)
  stay as `ARRAY<STRUCT>` through staging; `UNNEST` where a flat grain is
  needed
- Useful BQ-specific functions: `SAFE_DIVIDE`, `COUNTIF`, `ARRAY_AGG(x ORDER BY y LIMIT 1)`
  (first-touch attribution pattern)
