{{ config(materialized='view') }}

-- TODO: Implement — flatten ShipHero shipments (address RECORD, nested shipping_labels)
-- Source: raw_shiphero.shipments
-- address.city → ship_city, .state → ship_state, .country, .zip
-- shipping_labels: use stg_shiphero__shipping_labels to UNNEST
SELECT * FROM {{ source('shiphero', 'shipments') }}
