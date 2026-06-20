{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)            AS product_id,
    title,
    product_type,
    vendor,
    tags,
    status,
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM {{ source('shopify', 'products') }}
