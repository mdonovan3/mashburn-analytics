{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)                AS return_line_item_id,
    CAST(return_request_id AS STRING) AS return_id,
    CAST(line_item_id AS STRING)      AS line_item_id,
    CAST(product_id AS STRING)        AS product_id,
    CAST(variant_id AS STRING)        AS variant_id,
    sku,
    title,
    variant_title,
    CAST(price AS NUMERIC)            AS price,
    reason,
    parent_reason,
    outcome,
    CAST(returned_at AS TIMESTAMP)    AS returned_at
FROM {{ source('loop_returns', 'return_line_items') }}
