# dbt

**What it is:** a SQL-first transformation framework. You write `SELECT`
statements as version-controlled `.sql` files; dbt handles dependency
ordering (via `{{ ref() }}`), materialization (view/table/ephemeral/
incremental), testing, and documentation generation. It doesn't move data
in — that's [dlt](dlt.md)'s job — it only transforms data already sitting
in the warehouse.

**In this project:** `dbt-bigquery` adapter, `dbt_utils` package. Project
structure: `staging` (views) → `intermediate` (ephemeral) →
`marts` (tables), one schema per business domain. See
[Data Modeling](../data-modeling/overview.md) for current status — the
project structure, source declarations, and tests are real; the model SQL
itself is stubbed.

**Two flavors:**

- **dbt Core** — free, open source, runs anywhere you can run Python
  (`pip install dbt-bigquery`, `dbt run`). What this project uses locally.
- **dbt Cloud** — managed: hosted IDE, hosted docs, built-in cron
  scheduling, CI/CD. Free single-seat tier, then $100/seat/month.

See [Managed vs. Self-Hosted](../architecture/managed-vs-self-hosted.md)
for the recommendation on running dbt in production (self-hosted, on the
same Cloud Run Jobs pattern as ingestion, rather than dbt Cloud).

**Local commands used in this project:**

```bash
dbt deps    # install packages (dbt_utils)
dbt seed    # load seed CSVs (none currently used — mock data loads via ingestion/load_to_bigquery.py instead)
dbt run     # build staging/intermediate/marts
dbt test    # run schema tests (unique, not_null, etc.)
```
