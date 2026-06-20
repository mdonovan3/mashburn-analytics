{{ config(materialized='table') }}

-- TODO: Customer lifetime value mart
-- One row per customer
-- Columns: customer_id, email, first_name, last_name, tags, city, state
--   lifetime_orders, lifetime_revenue, avg_order_value
--   first_order_at, last_order_at, days_since_last_order
--   customer_tier (derived from tags or spending threshold)
--   acquisition_channel (first order source_name)
-- Key question: which acquisition channel produces highest LTV?
SELECT 1 AS stub
