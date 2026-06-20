{{ config(materialized='view') }}

SELECT
    CAST(lbl.id AS STRING)              AS label_id,
    CAST(s.id AS STRING)                AS shipment_id,
    CAST(s.order_id AS STRING)          AS order_id,
    lbl.carrier,
    lbl.shipping_name,
    lbl.shipping_method,
    lbl.tracking_number,
    lbl.tracking_url,
    lbl.cost                            AS shipping_cost_raw,
    lbl.status                          AS label_status,
    CAST(lbl.created_date AS TIMESTAMP) AS created_at
FROM {{ source('shiphero', 'shipments') }} s,
UNNEST(s.shipping_labels) AS lbl
