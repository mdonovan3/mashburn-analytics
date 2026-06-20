{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_shopify.products
--   id → product_id (STRING)
--   title, product_type, vendor, tags, status
--   created_at, updated_at → TIMESTAMP

SELECT 1 AS stub
