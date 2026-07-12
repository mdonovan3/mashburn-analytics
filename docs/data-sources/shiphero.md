# ShipHero

Warehouse management / fulfillment — shipments and shipping labels.

| | |
|---|---|
| **Mock data** | :white_check_mark: Implemented — `raw_shiphero` populated in BigQuery |
| **dlt source** | :jigsaw: Scaffolded — `ingestion/dlt/shiphero/`, not yet run against a live account |
| **API style** | **GraphQL** (single `/graphql` endpoint) — not REST |
| **Managed connector coverage** | Native on Fivetran, Portable. **Not on Airbyte** — despite marketing pages implying otherwise, there's no real ShipHero connector in Airbyte's actual catalog/repo |

## Table

| Table | Grain | Key fields |
|---|---|---|
| `shipments` | one row per shipment | `id`, `order_id`, `warehouse_id`, `created_date`, `address` (nested), `shipping_labels` (nested array) |

## dlt pipeline notes — why this one looks different from Shopify

ShipHero's public API is GraphQL, not REST, so `shiphero_source.py` doesn't
use dlt's `rest_api_source` helper (that's REST-specific). Instead it's a
plain `@dlt.resource` generator that POSTs GraphQL queries with `requests`
directly and walks the `edges` / `pageInfo.hasNextPage` / `endCursor`
cursor-pagination pattern by hand — a dlt resource is just a Python
generator, so any HTTP client works inside it.

**Auth is a refresh-token exchange, not a static key.** ShipHero access
tokens expire every 28 days. Rather than manage that as an operational
chore, the pipeline stores a long-lived refresh token as the secret and
calls `POST /auth/refresh` for a fresh access token on every run.

## :warning: Field coverage — verify before trusting

The GraphQL query only requests fields confirmed from ShipHero's public
docs/examples: `id`, `order_id`, `warehouse_id`, `created_date`,
`shipped_off_shiphero`, `dropshipment`, `address{...}`,
`shipping_labels{id, carrier, shipping_name, shipping_method,
tracking_number, cost, created_date}`.

The mock schema already in this repo also includes `delivered`,
`completed`, `picked_up`, `needs_refund`, `refunded`, and
`shipping_labels.tracking_url` / `.status` — **these were not confirmed to
exist on the real API** from available docs. GraphQL hard-errors on an
unrecognized field rather than silently skipping it, so check the
interactive schema browser at
[developer.shiphero.com/schema](https://developer.shiphero.com/schema/)
and adjust the query before running this for real.

Full setup/run instructions: [`ingestion/dlt/shiphero/README.md`](https://github.com/mdonovan3/mashburn-analytics/blob/main/ingestion/dlt/shiphero/README.md).

## Getting API access

Create a Third-Party Developer user in the ShipHero account (Settings →
API) — the access + refresh token pair is shown once at creation.
