{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)                  AS variant_id,
    CAST(product_id AS STRING)          AS product_id,
    sku,
    CAST(price AS NUMERIC)              AS price,
    CAST(compare_at_price AS NUMERIC)   AS compare_at_price,
    inventory_quantity,
    option1                             AS size,
    option2                             AS color,
    option3,
    CAST(created_at AS TIMESTAMP)       AS created_at
FROM {{ source('shopify', 'product_variants') }}
