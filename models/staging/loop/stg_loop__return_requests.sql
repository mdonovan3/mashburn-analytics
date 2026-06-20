{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)               AS return_id,
    order_name,
    CAST(provider_order_id AS STRING) AS order_id,
    customer_email,
    customer_first_name,
    customer_last_name,
    state,
    type                             AS return_type,
    carrier,
    tracking_number,
    CAST(total AS NUMERIC)           AS total,
    CAST(refund AS NUMERIC)          AS refund,
    CAST(exchange AS NUMERIC)        AS exchange,
    CAST(gift_card AS NUMERIC)       AS gift_card,
    currency,
    label_status,
    CASE
        WHEN refund  > 0 THEN 'refund'
        WHEN exchange > 0 THEN 'exchange'
        WHEN gift_card > 0 THEN 'gift_card'
        ELSE 'other'
    END AS return_resolution
FROM {{ source('loop_returns', 'return_requests') }}
