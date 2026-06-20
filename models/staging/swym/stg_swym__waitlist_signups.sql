{{ config(materialized='view') }}

SELECT
    CAST(empi AS STRING)          AS product_id,
    CAST(epi AS STRING)           AS variant_id,
    sku,
    customer_email,
    CAST(signed_up_at AS TIMESTAMP)  AS signed_up_at,
    CAST(notified_at AS TIMESTAMP)   AS notified_at,
    CAST(purchased_at AS TIMESTAMP)  AS purchased_at,
    notified_at IS NOT NULL          AS notified,
    purchased_at IS NOT NULL         AS converted
FROM {{ source('swym', 'waitlist_signups') }}
