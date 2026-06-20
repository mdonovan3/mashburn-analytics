{{ config(materialized='table') }}

-- TODO: Return rate mart at SKU level
-- Columns: variant_id, sku, product_title, size, color
--   units_sold, units_returned, return_rate
--   top_return_reason, pct_exchange, pct_refund
-- Key question: which SKUs have highest return rates and why? (size/fit issues?)
SELECT 1 AS stub
