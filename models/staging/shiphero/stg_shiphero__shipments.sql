{{ config(materialized='view') }}

-- TODO: Flatten and cast from raw_shiphero.shipments
--   id → shipment_id (STRING), order_id → STRING
--   warehouse_id, delivered, completed, picked_up, needs_refund, refunded
--   Flatten address RECORD: address.city → ship_city, address.state → ship_state,
--     address.country → ship_country, address.zip → ship_zip
--   created_date → created_at (TIMESTAMP)

SELECT 1 AS stub
