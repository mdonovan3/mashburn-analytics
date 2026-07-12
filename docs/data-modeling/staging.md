# Staging

One view per raw source table. Job: rename to snake_case, cast types,
derive nothing else — no filtering, no joins, no business logic. That
discipline is what keeps everything downstream trustworthy: if a number
looks wrong in a mart, staging is never the place bad logic could be
hiding.

**Status: :clipboard: structurally scaffolded, SQL not written.** Every
model below currently compiles to `SELECT 1 AS stub`. The TODO comment in
each file specifies the intended rename/cast/derive logic in enough detail
that writing the real query is closer to transcription than design work —
that design work is already done.

## Convention

- Naming: `stg_<source>__<table>` (e.g. `stg_shopify__orders`)
- Materialization: `view` (cheap, always current — no need for a physical
  table at this layer)
- All timestamps cast to `TIMESTAMP`
- Source freshness tests on `created_at`/`updated_at` columns (not yet
  configured — freshness checks are a `dbt source freshness` feature, added
  once the loop is closed on the production dlt sources actually running on
  a schedule)

## Models (15 total, all 5 sources)

| Source | Models |
|---|---|
| Shopify | `stg_shopify__orders`, `__customers`, `__products`, `__product_variants`, `__inventory_levels`, `__locations`, `__order_line_items` |
| ShipHero | `stg_shiphero__shipments`, `__shipping_labels` |
| Loop | `stg_loop__return_requests`, `__return_line_items` |
| Swym | `stg_swym__wishlist_events`, `__waitlist_signups` |
| Klaviyo | `stg_klaviyo__email_events`, `__campaigns` |

## Representative example — what's specified vs. what's written

`stg_shopify__orders.sql` today:

```sql
{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_shopify.orders
--   id → order_id (STRING), customer_id, location_id → STRING
--   order_number, email, source_name, financial_status, fulfillment_status
--   total_price, subtotal_price, total_discounts, total_tax → NUMERIC, currency
--   tags, discount_codes
--   Derive: channel = CASE WHEN location_id IS NULL THEN 'ecommerce' ELSE 'pos' END
--   created_at, updated_at → TIMESTAMP

SELECT 1 AS stub
```

The `channel` derivation is the one piece of light logic staging allows —
it's a direct 1:1 recode of a single column, not a join or aggregation, so
it stays in scope for this layer under most staging conventions (including
this one).

`stg_swym__wishlist_events.sql` is a good example of why staging exists at
all: Swym's raw field names (`empi`, `epi`, `cts`, `bt`, ...) are opaque
API shorthand — staging is where those become `product_id`, `variant_id`,
`created_at`, `source_domain`, so nothing downstream has to remember what
`empi` means.

## Source declarations (the part that IS done)

`models/staging/sources.yml` documents all 25 raw tables across the 5
sources — full column lists, descriptions for non-obvious fields (like
Swym's), and `unique`/`not_null` tests on every primary key. This is real,
tested, and passing today — it's the contract staging will be built
against, just written before the staging SQL itself.
