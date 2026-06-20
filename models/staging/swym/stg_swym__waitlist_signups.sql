{{ config(materialized='view') }}

-- TODO: Implement — empi → product_id, epi → variant_id (STRING)
-- Derive: converted = purchased_at IS NOT NULL, notified = notified_at IS NOT NULL
SELECT * FROM {{ source('swym', 'waitlist_signups') }}
