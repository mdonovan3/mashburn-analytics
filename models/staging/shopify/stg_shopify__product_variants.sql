{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_shopify.product_variants
--   id → variant_id (STRING), product_id → STRING
--   sku, inventory_quantity
--   price, compare_at_price → NUMERIC
--   option1 → size, option2 → color, option3
--   created_at → TIMESTAMP

SELECT 1 AS stub
