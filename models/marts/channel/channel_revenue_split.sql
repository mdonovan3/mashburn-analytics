{{ config(materialized='table') }}

-- TODO: Channel revenue mart
-- Columns: channel (ecommerce/pos), month, orders, revenue, avg_order_value, pct_of_total
-- Key question: what % of revenue is eCommerce vs in-store? Trending?
SELECT 1 AS stub
