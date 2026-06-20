{{ config(materialized='view') }}

-- TODO: Implement this model
-- Source: raw_shopify.orders
-- Key transforms:
--   - id → order_id (STRING), customer_id, location_id (STRING)
--   - total_price, subtotal_price, total_discounts, total_tax → NUMERIC
--   - created_at, updated_at → TIMESTAMP
--   - Derive channel: CASE WHEN location_id IS NULL THEN 'ecommerce' ELSE 'pos' END
--   - Parse discount_codes JSON string (stored as string) for discount code name
--   - line_items stays nested — use stg_shopify__order_line_items to UNNEST

SELECT * FROM {{ source('shopify', 'orders') }}
