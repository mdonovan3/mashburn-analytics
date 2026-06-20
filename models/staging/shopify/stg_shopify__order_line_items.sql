{{ config(materialized='view') }}

-- TODO: Implement this model
-- UNNEST line_items from raw_shopify.orders
-- BigQuery pattern:
--   FROM {{ source('shopify', 'orders') }} o, UNNEST(o.line_items) AS li
-- Key transforms:
--   - li.id → line_item_id (STRING), o.id → order_id (STRING)
--   - li.product_id, variant_id, sku, title, variant_title
--   - li.quantity (INT), li.price (NUMERIC), li.total_discount (NUMERIC)
--   - li.fulfillment_status
--   - o.created_at → order_created_at

SELECT
    CAST(li.id AS STRING) AS line_item_id,
    CAST(o.id AS STRING) AS order_id,
    li.product_id,
    li.variant_id,
    li.sku,
    li.title,
    li.variant_title,
    li.quantity,
    li.price,
    li.total_discount,
    li.fulfillment_status,
    o.created_at AS order_created_at
FROM {{ source('shopify', 'orders') }} o,
UNNEST(o.line_items) AS li
