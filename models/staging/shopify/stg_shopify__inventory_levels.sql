{{ config(materialized='view') }}

-- TODO: Cast from raw_shopify.inventory_levels
--   inventory_item_id, location_id → STRING
--   available
--   updated_at → TIMESTAMP

SELECT 1 AS stub
