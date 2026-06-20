{{ config(materialized='view') }}

-- TODO: UNNEST shipping_labels array from raw_shiphero.shipments
--   FROM shipments s, UNNEST(s.shipping_labels) AS lbl
--   lbl.id → label_id (STRING), s.id → shipment_id (STRING), s.order_id → order_id (STRING)
--   lbl.carrier, shipping_name, shipping_method, tracking_number, tracking_url
--   lbl.cost → shipping_cost_raw, lbl.status → label_status
--   lbl.created_date → created_at (TIMESTAMP)

SELECT 1 AS stub
