{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_swym.wishlist_events
--   _pkey → event_id, empi → product_id (STRING), epi → variant_id (STRING)
--   dt → product_title, du → product_url, iu → image_url
--   pr → price (NUMERIC), sku, lid → list_id, di → device_id
--   bt → source_domain, _t → wishlist_action
--   cts → created_at (TIMESTAMP_MILLIS), uts → updated_at (TIMESTAMP_MILLIS)

SELECT 1 AS stub
