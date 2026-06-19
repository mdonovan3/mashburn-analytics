# mashburn-analytics

Mock dbt + BigQuery project modeled after the Sid Mashburn data ecosystem.
Built as a portfolio project and interview prep for the Data Engineer role.

## Purpose

- Practice dbt on BigQuery (closing the platform gap before round 2)
- Model the exact data sources Mashburn uses in production
- Demonstrate analytical thinking about specialty retail / DTC / eCommerce data problems
- Build something real to reference in technical interviews

## Data Sources

| Source | What it is | Key tables |
|--------|-----------|------------|
| **Shopify** | Orders, customers, products, inventory | orders, order_line_items, customers, products, product_variants, inventory_levels, locations |
| **ShipHero** | WMS / fulfillment | shipments, inventory_movements, returns |
| **Swym** | Wishlist + back-in-stock waitlist | wishlist_events, waitlist_signups |
| **Loop Returns** | Self-serve returns portal | return_requests, return_line_items |
| **Klaviyo** | Email/SMS marketing | email_events, campaigns |

> **Note:** Swym is confirmed on shopmashburn.com (wishlist heart icon on PDPs).
> Loop Returns is the dominant returns platform in the Shopify ecosystem for fashion/DTC.
> Klaviyo is nearly universal for Shopify-native email — assumed until confirmed otherwise.

## dbt Project Structure

```
models/
  staging/          # One model per source table. Rename columns, cast types, no logic.
    shopify/
    shiphero/
    swym/
    loop/
    klaviyo/
  intermediate/     # Business logic joins. Ephemeral (no physical tables).
  marts/
    customer/       # LTV, retention, cohort, repeat purchase rate
    product/        # Sell-through, collection performance, return rates by SKU
    channel/        # Store vs. eCommerce, by location, by acquisition source
    returns/        # Return rate, reason analysis, resolution type breakdown

seeds/              # Mock CSVs for local development (no live data needed)
analyses/           # Ad-hoc SQL — sample business questions
macros/             # Shared logic (fiscal calendar, tier classification, etc.)
```

## Key Business Questions This Project Answers

1. **Collection performance** — How did the "Ann Loves Lately" editorial collection sell through vs. standard inventory? Sell-through rate by tag.
2. **Customer LTV & retention** — What is the repeat purchase rate at 90/180/365 days? Which acquisition channel produces the highest LTV customers?
3. **Channel split** — What share of revenue is eCommerce vs. in-store, by location? Which stores punch above their weight?
4. **Wishlist-to-purchase conversion** (Swym) — What % of wishlisted items convert? Which products have high wishlist + low purchase (demand signal for reorder)?
5. **Back-in-stock performance** (Swym waitlist) — What % of waitlist signups convert after notification?
6. **Return rate by product** — Which SKUs/categories have the highest return rates and why?
7. **Exchange vs. refund rate** (Loop) — What % of returns become exchanges vs. cash refunds? (exchanges keep revenue)
8. **Email attribution** (Klaviyo) — What revenue is attributable to email campaigns vs. flows?
9. **Discount impact** — Are customers who use discount codes worse LTV than full-price buyers? Are we training people to wait for promotions?
10. **Inventory health** — Weeks of supply by SKU and location. Flag aged inventory before it needs markdown.

## Setup

### Prerequisites
- Python 3.9+
- dbt-bigquery: `pip install dbt-bigquery`
- Google Cloud SDK: `gcloud auth application-default login`
- Free BigQuery project (10GB storage + 1TB queries/month free)

### First-time setup
```bash
# 1. Install dbt
pip install dbt-bigquery

# 2. Create a GCP project at console.cloud.google.com
#    Enable the BigQuery API

# 3. Authenticate
gcloud auth application-default login

# 4. Copy profiles template
cp profiles.yml.template ~/.dbt/profiles.yml
# Edit ~/.dbt/profiles.yml — set your GCP project ID

# 5. Install dbt packages
dbt deps

# 6. Load seeds (mock data)
dbt seed

# 7. Run models
dbt run

# 8. Test
dbt test
```

### BigQuery dataset layout
```
mashburn-analytics-dev/
  raw_shopify/          # seed data lands here
  raw_shiphero/
  raw_swym/
  raw_loop/
  raw_klaviyo/
  staging/              # dbt staging views
  marts/                # dbt mart tables
```

## Staging conventions

- Prefix: `stg_<source>__<table>` (e.g. `stg_shopify__orders`)
- Cast all timestamps to `TIMESTAMP`
- Rename to snake_case
- No filtering or business logic in staging — that goes in intermediate/marts
- Source freshness tests on `created_at` columns

## BigQuery vs. PostgreSQL notes

Key differences to internalize:

```sql
-- Partitioning (define in dbt config, not DDL)
{{ config(partition_by={"field": "order_date", "data_type": "date"}) }}

-- Clustering
{{ config(cluster_by=["channel", "location_id"]) }}

-- Always filter on partition column (cost + performance)
WHERE DATE(created_at) >= '2024-01-01'   -- good: prunes partitions
WHERE EXTRACT(YEAR FROM created_at) = 2024 -- bad: full scan

-- Nested fields (Shopify line_items come as ARRAY<STRUCT>)
SELECT o.id, li.sku, li.quantity
FROM raw_shopify.orders o, UNNEST(o.line_items) AS li

-- BQ-specific functions
SAFE_DIVIDE(a, b)           -- null instead of divide-by-zero
COUNTIF(condition)          -- cleaner than COUNT(CASE WHEN ...)
DATE_TRUNC(col, MONTH)      -- same as PG
ARRAY_AGG(x ORDER BY y LIMIT 1)  -- useful for first-touch attribution
```

## Status

- [x] Repo created, directory structure scaffolded
- [x] Sources documented (sources.yml)
- [x] README with business questions and setup instructions
- [ ] Mock seed CSVs (Shopify orders, customers, products)
- [ ] Staging models
- [ ] Intermediate joins
- [ ] Mart models
- [ ] Analyses (sample business questions as SQL)
- [ ] BigQuery project created and connected
