{{ config(materialized='view') }}

-- TODO: Implement — UNNEST shipping_labels from raw_shiphero.shipments
-- FROM {{ source('shiphero', 'shipments') }} s, UNNEST(s.shipping_labels) AS lbl
-- CAST(lbl.cost AS NUMERIC) → shipping_cost
SELECT
    lbl.id AS label_id,
    s.id AS shipment_id,
    s.order_id,
    lbl.carrier,
    lbl.shipping_name,
    lbl.shipping_method,
    lbl.tracking_number,
    lbl.tracking_url,
    lbl.cost AS shipping_cost_raw,
    lbl.status AS label_status,
    lbl.created_date AS created_at
FROM {{ source('shiphero', 'shipments') }} s,
UNNEST(s.shipping_labels) AS lbl
