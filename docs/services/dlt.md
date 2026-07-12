# dlt (data load tool)

**What it is:** an open-source Python library — not a hosted platform —
for the "EL" in ELT. You write plain Python generator functions
(`@dlt.resource`) that yield records from a source; dlt handles schema
inference/evolution, batching, retries, incremental state tracking (via
`dlt.sources.incremental`), and loading into 20+ destinations. For REST
APIs specifically, `dlt.sources.rest_api` adds a declarative config layer
so most REST sources need no custom HTTP code at all.

**Why it's the ingestion choice here:** no platform fee, runs as a plain
container (fits the Cloud Scheduler → Cloud Run Job pattern), and full
control in-house — see [Evaluated, not chosen](evaluated-not-chosen.md)
for the managed-platform alternatives that were considered first.

**Core concepts, mapped to this project:**

| Concept | What it is | Example here |
|---|---|---|
| Resource | one logical stream of records | `orders`, `shipments` |
| Source | a bundle of resources | `shopify_source()`, `shiphero_source()` |
| Pipeline | the run object — source + destination + dataset | `shopify_pipeline.py` |
| Incremental | tracks the last-seen cursor value between runs | `updated_at` (Shopify), `created_date` (ShipHero) |

**Two API styles handled two different ways** in this project — see
[Ingestion Layer](../architecture/ingestion.md#why-shopify-and-shiphero-look-different):
declarative `rest_api_source` for Shopify's REST API, a hand-rolled
`@dlt.resource` generator with `requests` for ShipHero's GraphQL API (dlt's
REST helper doesn't fit GraphQL).

**Config/secrets:** `.dlt/config.toml` (non-secret) and `.dlt/secrets.toml`
(gitignored). Both can be overridden by environment variables using the
`SOURCES__<source>__<field>` naming convention (uppercased, `.` → `__`) —
env vars always win, which is how secrets get injected in the container
deployment without rebuilding the image.

**Install:** `pip install "dlt[bigquery]"` — the `[bigquery]` extra pulls
in `google-cloud-bigquery` and destination-specific dependencies.
