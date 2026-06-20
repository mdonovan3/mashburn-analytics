{{ config(materialized='view') }}

-- TODO: Implement this model
-- Source: raw_shopify.product_variants
-- Key transforms:
--   - id → variant_id (STRING), product_id (STRING)
--   - price, compare_at_price → NUMERIC
--   - created_at → TIMESTAMP
--   - option1 = size, option2 = color (for most products)

SELECT * FROM {{ source('shopify', 'product_variants') }}
