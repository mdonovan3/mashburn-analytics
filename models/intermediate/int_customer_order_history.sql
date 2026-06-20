{{ config(materialized='ephemeral') }}

-- TODO: Aggregate per-customer purchase history
-- GROUP BY customer_id:
--   COUNT(DISTINCT order_id) AS lifetime_orders
--   SUM(total_price) AS lifetime_revenue
--   MIN(created_at) AS first_order_at, MAX(created_at) AS last_order_at
--   DATE_DIFF(last_order_at, first_order_at, DAY) AS customer_age_days
SELECT * FROM {{ ref('stg_shopify__orders') }}
