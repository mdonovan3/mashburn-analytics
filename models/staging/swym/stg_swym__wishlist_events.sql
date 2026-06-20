{{ config(materialized='view') }}

SELECT
    _pkey                                AS event_id,
    CAST(empi AS STRING)                 AS product_id,
    CAST(epi AS STRING)                  AS variant_id,
    dt                                   AS product_title,
    du                                   AS product_url,
    iu                                   AS image_url,
    CAST(pr AS NUMERIC)                  AS price,
    sku,
    lid                                  AS list_id,
    di                                   AS device_id,
    bt                                   AS source_domain,
    _t                                   AS wishlist_action,
    TIMESTAMP_MILLIS(cts)                AS created_at,
    TIMESTAMP_MILLIS(uts)                AS updated_at
FROM {{ source('swym', 'wishlist_events') }}
