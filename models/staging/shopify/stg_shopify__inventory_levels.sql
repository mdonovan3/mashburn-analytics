{{ config(materialized='view') }}

-- TODO: Implement this model
-- Source: raw_shopify.inventory_levels
-- Key transforms:
--   - inventory_item_id, location_id → STRING
--   - updated_at → TIMESTAMP
-- Note: In real Shopify, inventory_item_id ≠ variant_id
--   Join to product_variants on inventory_item_id to get variant_id + sku
--   (In this mock data inventory_item_id maps sequentially to variants)

SELECT * FROM {{ source('shopify', 'inventory_levels') }}
