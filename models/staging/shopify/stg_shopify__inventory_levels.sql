{{ config(materialized='view') }}

SELECT
    CAST(inventory_item_id AS STRING) AS inventory_item_id,
    CAST(location_id AS STRING)       AS location_id,
    available,
    CAST(updated_at AS TIMESTAMP)     AS updated_at
FROM {{ source('shopify', 'inventory_levels') }}
