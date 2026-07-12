# Shopify

Primary commerce source — orders, customers, products, inventory.

| | |
|---|---|
| **Mock data** | :white_check_mark: Implemented — `raw_shopify` populated in BigQuery |
| **dlt source** | :jigsaw: Scaffolded — `ingestion/dlt/shopify/`, not yet run against a live store |
| **API style** | REST (Admin API) |
| **Managed connector coverage** | Native on Fivetran, Airbyte, Portable, Hevo — the one source with no coverage gaps anywhere |

## Tables

| Table | Grain | Key fields |
|---|---|---|
| `orders` | one row per order | `id`, `customer_id`, `location_id`, `financial_status`, `fulfillment_status`, `total_price`, `line_items` (nested array) |
| `customers` | one row per customer | `id`, `email`, `orders_count`, `total_spent`, `default_address` (nested) |
| `products` | one row per product | `id`, `title`, `product_type`, `vendor`, `tags`, `status` |
| `product_variants` | one row per SKU | `id`, `product_id`, `sku`, `price`, `inventory_quantity`, `option1/2/3` |
| `inventory_levels` | one row per item × location | `inventory_item_id`, `location_id`, `available` |
| `locations` | one row per store | `id`, `name`, `city`, `province`, `active` |

`location_id IS NULL` on an order is how staging derives `channel = 'ecommerce'` vs `'pos'` (see [Staging](../data-modeling/staging.md)).

## dlt pipeline notes

- Uses dlt's declarative `rest_api_source` — no custom HTTP code needed, since Shopify's Admin API is straightforward REST.
- All of `orders`/`customers`/`products` are incremental on `updated_at`.
- `product_variants` has no standalone Shopify endpoint — it's nested inside `products.json`, so it's implemented as a `@dlt.transformer` piped from the `products` resource.
- `inventory_levels` requires a `location_ids` query param — implemented as a child resource resolved per-location from the `locations` resource (dlt's `resolve` binding).
- Pagination is Shopify's standard RFC 5988 `Link` header — dlt auto-detects this, no explicit paginator config needed.

Full setup/run instructions: [`ingestion/dlt/shopify/README.md`](https://github.com/mdonovan3/mashburn-analytics/blob/main/ingestion/dlt/shopify/README.md).

## Getting API access

Requires a custom app on the target store (Settings → Apps and sales
channels → Develop apps) with scopes: `read_orders`, `read_customers`,
`read_products`, `read_locations`, `read_inventory`.
