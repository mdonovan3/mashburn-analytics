# ShipHero dlt Pipeline

dlt extracts from ShipHero's **GraphQL** API and loads into `raw_shiphero`
on BigQuery. See [`../README.md`](../README.md) for how this fits into the
overall ingestion layout, and [`../DEPLOY.md`](../DEPLOY.md) for running it
as a container (`SOURCE=shiphero`).

**Status: scaffolded, not yet run end-to-end.** No live ShipHero account is
connected to this portfolio project.

## Why this looks different from the Shopify pipeline

ShipHero's public API (`developer.shiphero.com`) is GraphQL — a single
`/graphql` endpoint you POST queries to — not REST like Shopify's Admin
API. dlt's `rest_api_source` declarative helper is REST-specific, so
`shiphero_source.py` instead uses a plain `@dlt.resource` generator that
POSTs the query with `requests` and walks the pagination itself. This is
the standard dlt pattern for GraphQL APIs: a dlt resource is just a Python
generator, so any HTTP client works inside it.

## Auth: refresh token, not a static key

ShipHero access tokens expire every **28 days**. Rather than manage that
expiry as an operational chore, the resource takes a long-lived
**refresh token** as the secret and exchanges it for a fresh access token
via `POST /auth/refresh` on every pipeline run. One secret, no manual
rotation.

## Field coverage — verify before trusting

The GraphQL query only requests fields confirmed from ShipHero's public
docs/examples: `id`, `order_id`, `warehouse_id`, `created_date`,
`shipped_off_shiphero`, `dropshipment`, `address{...}`,
`shipping_labels{id, carrier, shipping_name, shipping_method,
tracking_number, cost, created_date}`.

The mock schema this project already models in `ingestion/schemas.py`
(`SHIPHERO_SHIPMENTS`) also has `delivered`, `completed`, `picked_up`,
`needs_refund`, `refunded`, and `shipping_labels.tracking_url` /
`.status` — those were **not** confirmed against ShipHero's real schema
from available docs. GraphQL treats an unrecognized field as a hard error,
not a silent skip, so check the interactive schema browser at
https://developer.shiphero.com/schema/ and adjust `SHIPMENTS_QUERY` before
running this for real.

## Resources

| Resource | ShipHero query | Incremental on |
|---|---|---|
| `shipments` | `shipments(date_from, date_to, first, after)` | `created_date` |

## Setup

```bash
cd ingestion/dlt/shiphero
pip install -r requirements.txt

cp .dlt/secrets.toml.example .dlt/secrets.toml
# edit .dlt/secrets.toml — add a real ShipHero refresh token
```

Get a refresh token by creating a Third-Party Developer user in the
ShipHero account (Settings → API) — the access + refresh token pair is
shown once at creation.

BigQuery auth reuses this project's Application Default Credentials (same
as `../../../CONNECTION.md`) — no service account file needed if
`gcloud auth application-default login` has already been run.

## Run

```bash
python shiphero_pipeline.py
```

Then inspect the run:

```bash
dlt pipeline shiphero show
```
