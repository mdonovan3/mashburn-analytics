{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_shopify.customers
--   id → customer_id (STRING)
--   email, first_name, last_name, phone, orders_count, tags, accepts_marketing
--   total_spent → NUMERIC
--   Flatten default_address RECORD: city, province → state, country, zip
--   created_at, updated_at → TIMESTAMP

SELECT 1 AS stub
