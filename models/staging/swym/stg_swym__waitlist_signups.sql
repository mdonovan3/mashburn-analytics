{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_swym.waitlist_signups
--   empi → product_id (STRING), epi → variant_id (STRING)
--   sku, customer_email
--   signed_up_at, notified_at, purchased_at → TIMESTAMP
--   Derive: notified = notified_at IS NOT NULL, converted = purchased_at IS NOT NULL

SELECT 1 AS stub
