# Data Modeling — Overview

The dbt project has three layers (see
[Warehouse & Modeling](../architecture/warehouse-modeling.md) for the
diagram). Status differs sharply by layer — worth being precise about,
since "the model exists" and "the model does what it's supposed to" are
different claims here.

## Status, honestly

| Layer | Structure (folders, naming, `schema.yml` docs, source tests) | SQL logic |
|---|---|---|
| Sources (`sources.yml`) | :white_check_mark: Implemented — all 25 raw tables across 5 sources documented, with `unique`/`not_null` tests on primary keys | N/A — this is the raw layer |
| Staging | :white_check_mark: Folder structure + `schema.yml` per source :material-arrow-right: :clipboard: **SQL is `SELECT 1 AS stub`** in every model | Planned — detailed `-- TODO` comments specify the exact rename/cast/derive logic per model, not written yet |
| Intermediate | :white_check_mark: Folder structure, `ephemeral` materialization configured :material-arrow-right: :clipboard: **SQL is a bare passthrough** (`SELECT * FROM {{ ref(...) }}`) | Planned — TODO comments specify the joins |
| Marts | :white_check_mark: Folder structure, domain schemas configured (`customer`/`product`/`channel`/`returns`) :material-arrow-right: :clipboard: **SQL is `SELECT 1 AS stub`** | Planned — TODO comments specify every output column and the business question each mart answers |

**Why call the folders "implemented" if the SQL is stubbed?** Because the
scaffolding — naming conventions, materialization strategy, `ref()` graph,
column-level documentation, and tests on the raw sources — is real
decision-making that's already made and dbt-compiles/runs successfully
today (confirmed: `dbt run` + `dbt test` both pass against the mock data).
What's missing is the transformation logic itself, and that's tracked
explicitly rather than glossed over — see the per-layer pages for exactly
what's stubbed where.

## Layer pages

- [Staging](staging.md) — one view per source table, all 15 models stubbed
- [Intermediate](intermediate.md) — 5 ephemeral join models, all stubbed
- [Marts](marts.md) — 7 mart tables across 4 business domains, all stubbed

## What's genuinely done vs. what's next

Done: source declarations, tests, naming conventions, the full dbt DAG
shape (every `ref()` and materialization already wired correctly), and a
working connection from BigQuery through to a `dbt run`.

Next: writing the actual `SELECT` logic in dependency order — staging
first (it's what everything else `ref()`s), then intermediate, then marts.
Each stub's TODO comment is close to a spec, not a placeholder — see any
model file directly for the intended column list and transform.
