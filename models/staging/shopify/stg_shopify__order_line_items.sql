{{ config(materialized='view') }}

-- TODO: UNNEST line_items from raw_shopify.orders
--   FROM orders o, UNNEST(o.line_items) AS li
--   li.id → line_item_id (STRING), o.id → order_id (STRING)
--   li.product_id, variant_id → STRING, sku, title, variant_title
--   li.quantity (INT), li.price → NUMERIC, li.total_discount → NUMERIC
--   li.fulfillment_status
--   o.created_at → order_created_at (TIMESTAMP)

SELECT 1 AS stub
