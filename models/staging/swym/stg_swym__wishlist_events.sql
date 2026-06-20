{{ config(materialized='view') }}

-- TODO: Implement — rename Swym abbreviated fields
-- empi → product_id, epi → variant_id, dt → product_title, du → product_url
-- iu → image_url, pr → price, lid → list_id, di → device_id, bt → source_domain
-- TIMESTAMP_MILLIS(cts) → created_at,  TIMESTAMP_MILLIS(uts) → updated_at
-- _t → wishlist_action ('a'=add, 'r'=remove)
SELECT * FROM {{ source('swym', 'wishlist_events') }}
