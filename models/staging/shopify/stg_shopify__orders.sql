{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_shopify.orders
--   id → order_id (STRING), customer_id, location_id → STRING
--   order_number, email, source_name, financial_status, fulfillment_status
--   total_price, subtotal_price, total_discounts, total_tax → NUMERIC, currency
--   tags, discount_codes
--   Derive: channel = CASE WHEN location_id IS NULL THEN 'ecommerce' ELSE 'pos' END
--   created_at, updated_at → TIMESTAMP

SELECT 1 AS stub
