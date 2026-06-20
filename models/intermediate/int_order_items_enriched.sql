{{ config(materialized='ephemeral') }}

-- TODO: Join order line items + products + variants
-- stg_shopify__order_line_items li
--   LEFT JOIN stg_shopify__products p ON li.product_id = p.product_id
--   LEFT JOIN stg_shopify__product_variants v ON li.variant_id = v.variant_id
-- Output one row per line item with product_type, vendor, size, color
SELECT * FROM {{ ref('stg_shopify__order_line_items') }}
