{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_shopify.locations
--   id → location_id (STRING)
--   name, city, country, zip, active
--   province → state

SELECT 1 AS stub
