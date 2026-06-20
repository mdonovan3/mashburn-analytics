{{ config(materialized='table') }}

-- TODO: Product performance mart
-- One row per product (or product x month for trending)
-- Columns: product_id, title, product_type, vendor
--   units_sold, gross_revenue, avg_unit_price
--   units_returned, return_rate
--   wishlist_adds, wishlist_converts, wishlist_conversion_rate
--   in_ann_loves_lately (tag flag)
-- Key question: sell-through by collection tag, return rate by SKU
SELECT 1 AS stub
