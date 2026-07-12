# Intermediate

Business-logic joins across staging models. Materialized `ephemeral` —
compiled inline into whatever references them, no physical table — because
nothing outside the dbt project should ever query these directly; they
exist purely to keep mart SQL from repeating the same joins five times.

**Status: :clipboard: structurally scaffolded, SQL not written.** Every
model currently compiles to a bare passthrough
(`SELECT * FROM {{ ref('some_staging_model') }}`), which only works at all
because staging is *also* stubbed right now — once staging has real logic,
these passthroughs need real joins or the whole chain breaks. Depends on
[Staging](staging.md) being written first.

## Models (5 total)

| Model | Intended join | Feeds |
|---|---|---|
| `int_orders_enriched` | `stg_shopify__orders` + `stg_shopify__customers` + `stg_shopify__locations` — one row per order with customer name, city, location name, channel | [customer](marts.md#customer), [channel](marts.md#channel) marts |
| `int_order_items_enriched` | `stg_shopify__order_line_items` + `stg_shopify__products` + `stg_shopify__product_variants` — one row per line item with product_type, vendor, size, color | [product](marts.md#product) marts |
| `int_customer_order_history` | Aggregates `stg_shopify__orders` by `customer_id` — lifetime_orders, lifetime_revenue, first/last order date | `customer_ltv` mart |
| `int_return_metrics` | `stg_loop__return_requests` + `stg_loop__return_line_items` + Shopify order line items — one row per returned item with days_to_return, resolution type, reason | [returns](marts.md#returns) mart |
| `int_wishlist_to_purchase` | `stg_swym__wishlist_events` joined to Shopify order line items on `variant_id` (`epi`) + customer email, flagged `converted` if a matching order line item exists *after* the wishlist-add date | `product_performance` mart (wishlist conversion columns) |

## Why ephemeral, not a view or table

- **Not a table**: no value in materializing an intermediate join
  physically — it's not queried on its own, and a table adds storage cost
  and a refresh step for no benefit.
- **Not a view**: a view still shows up as a queryable object in BigQuery,
  inviting someone to query it directly and bypass the mart layer's
  business logic/naming. Ephemeral models don't exist as objects at all —
  dbt inlines their SQL as a CTE wherever they're `ref()`'d.

## The one non-trivial piece of logic in this layer

`int_wishlist_to_purchase` is the most interesting model here — it's a
time-ordered join (wishlist add must happen *before* the matching
purchase, not just "ever purchased") on top of a fuzzy match (variant_id +
email, since Swym doesn't carry a Shopify order id to join on directly).
That's real analytical design, not a mechanical rename — worth flagging as
the piece most likely to need iteration once written against real data
rather than mock data with clean, unambiguous timestamps.
