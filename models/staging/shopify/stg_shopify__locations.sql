{{ config(materialized='view') }}

-- TODO: Implement this model
-- Source: raw_shopify.locations
-- Key transforms:
--   - id → location_id (STRING)
--   - province → state
--   - Filter active = true, or keep all and flag in marts

SELECT * FROM {{ source('shopify', 'locations') }}
