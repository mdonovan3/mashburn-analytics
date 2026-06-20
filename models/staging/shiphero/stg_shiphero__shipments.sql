{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)              AS shipment_id,
    CAST(order_id AS STRING)        AS order_id,
    warehouse_id,
    delivered,
    completed,
    picked_up,
    needs_refund,
    refunded,
    address.city                    AS ship_city,
    address.state                   AS ship_state,
    address.country                 AS ship_country,
    address.zip                     AS ship_zip,
    CAST(created_date AS TIMESTAMP) AS created_at
FROM {{ source('shiphero', 'shipments') }}
