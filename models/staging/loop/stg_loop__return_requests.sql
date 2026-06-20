{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_loop.return_requests
--   id → return_id (STRING), provider_order_id → order_id (STRING)
--   customer_email, customer_first_name, customer_last_name
--   state, type → return_type, carrier, tracking_number, label_status, order_name
--   total, refund, exchange, gift_card → NUMERIC, currency
--   Derive: return_resolution CASE WHEN refund > 0 THEN 'refund'
--           WHEN exchange > 0 THEN 'exchange' WHEN gift_card > 0 THEN 'gift_card' ELSE 'other'

SELECT 1 AS stub
