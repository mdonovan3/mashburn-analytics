# Marts

Physical tables (`materialized='table'`), one schema per business domain,
each built to answer a specific question rather than to be a generic
"clean copy" of a source. This is the layer analysts/BI tools should
actually query.

**Status: :clipboard: structurally scaffolded, SQL not written.** Every
model currently compiles to `SELECT 1 AS stub`. Depends on
[Intermediate](intermediate.md) being written first.

## customer {: #customer }

| Model | Intended output | Business question |
|---|---|---|
| `customer_ltv` | One row per customer: lifetime_orders, lifetime_revenue, avg_order_value, first/last order date, days_since_last_order, customer_tier, acquisition_channel | Which acquisition channel produces the highest-LTV customers? |
| `customer_retention_cohorts` | Monthly cohort table: cohort_month × months_since_first_purchase → customers_retained, retention_rate, plus repeat_purchase_rate at 90/180/365 days | What % of customers come back within 90/180/365 days? |

## product {: #product }

| Model | Intended output | Business question |
|---|---|---|
| `product_performance` | One row per product: units_sold, gross_revenue, units_returned, return_rate, wishlist_adds, wishlist_conversion_rate, `in_ann_loves_lately` tag flag | Sell-through by collection tag; which products have high wishlist interest but low actual purchase (a reorder demand signal)? |
| `return_rates_by_sku` | One row per variant/SKU: units_sold, units_returned, return_rate, top_return_reason, pct_exchange vs. pct_refund | Which SKUs have the highest return rates, and is it a size/fit pattern? |

## channel {: #channel }

| Model | Intended output | Business question |
|---|---|---|
| `channel_revenue_split` | channel (ecommerce/pos) × month: orders, revenue, avg_order_value, pct_of_total | What share of revenue is e-commerce vs. in-store, and how is that trending? |
| `store_performance` | One row per location × month: orders, revenue, avg_order_value, top_product_type | Which of the ~15 physical stores punch above their weight? |

## returns {: #returns }

| Model | Intended output | Business question |
|---|---|---|
| `return_analysis` | One row per month: total_returns, return_rate, pct_exchange/pct_refund/pct_credit, top_return_reason, avg_days_to_return | What % of returns become exchanges (which keep revenue) vs. straight refunds? |

## Why these seven, specifically

Each mart maps directly to one of the 10 business questions the project
set out to answer (see the original project README) — there isn't a mart
that exists just because a source table existed. `wishlist-to-purchase`
and `back-in-stock performance`, for instance, don't get their own mart;
they're columns *within* `product_performance`, because they're properties
of a product, not a new grain worth a whole table.

## What "done" looks like for this layer

Each stub's TODO comment already specifies the full column list and the
question it answers — genuinely closer to a lightweight spec than a
placeholder. The real work left is writing the aggregation SQL against
[Intermediate](intermediate.md) models (once those are real), plus the
`schema.yml` tests each mart should get (at minimum: `unique`+`not_null` on
the grain columns, `accepted_values` on categorical outputs like
`customer_tier` or `outcome`).
