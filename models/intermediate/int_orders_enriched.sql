{{ config(materialized='ephemeral') }}

-- TODO: Join orders + customers + locations
-- stg_shopify__orders o
--   LEFT JOIN stg_shopify__customers c ON o.customer_id = c.customer_id
--   LEFT JOIN stg_shopify__locations loc ON o.location_id = loc.location_id
-- Output one row per order with customer name, city, location name, channel
SELECT * FROM {{ ref('stg_shopify__orders') }}
