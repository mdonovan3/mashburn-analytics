# Shopify dlt Pipeline

dlt extracts from the Shopify Admin REST API and loads into `raw_shopify`
on BigQuery. See [`../README.md`](../README.md) for how this fits into the
overall ingestion layout, and [`../DEPLOY.md`](../DEPLOY.md) for running it
as a container.

**Status: scaffolded, not yet run end-to-end.** This portfolio project has
no live Shopify store connected, so this hasn't been executed against real
data. The REST API config follows dlt's documented `rest_api_source`
patterns (declarative resources, incremental cursor params, parent/child
`resolve` binding, Link-header pagination) — validate against a real store
+ token before relying on it, since dlt's API surface does shift between
versions.

## Resources

Matches the tables already modeled in `ingestion/schemas.py`:

| Resource | Shopify endpoint | Incremental on |
|---|---|---|
| `orders` | `orders.json` | `updated_at` |
| `customers` | `customers.json` | `updated_at` |
| `products` | `products.json` | `updated_at` |
| `product_variants` | nested in `products.json` (no standalone endpoint) | via parent `products` |
| `locations` | `locations.json` | full refresh (small table) |
| `inventory_levels` | `inventory_levels.json`, one call per location | `updated_at` |

## Setup

```bash
cd ingestion/dlt/shopify
pip install -r requirements.txt

cp .dlt/secrets.toml.example .dlt/secrets.toml
# edit .dlt/secrets.toml — add a real Shopify Admin API access token

# edit .dlt/config.toml — set shop_url to the real store domain
```

BigQuery auth reuses this project's Application Default Credentials (same
as `../../../CONNECTION.md`) — no service account file needed if
`gcloud auth application-default login` has already been run.

## Run

```bash
python shopify_pipeline.py
```

Then inspect the run:

```bash
dlt pipeline shopify show
```

## Getting a Shopify Admin API access token

Requires a custom app on the target store (Settings → Apps and sales
channels → Develop apps), with Admin API scopes: `read_orders`,
`read_customers`, `read_products`, `read_locations`, `read_inventory`.
