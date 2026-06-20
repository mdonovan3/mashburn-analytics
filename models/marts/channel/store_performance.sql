{{ config(materialized='table') }}

-- TODO: Store-level performance mart
-- One row per location x month
-- Columns: location_id, location_name, city, state, month
--   orders, revenue, avg_order_value, units_sold
--   top_product_type (by revenue)
-- Key question: which stores punch above their weight?
SELECT 1 AS stub
