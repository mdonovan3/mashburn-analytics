{{ config(materialized='ephemeral') }}

-- TODO: Join Swym wishlist 'add' events to Shopify order line items
-- Match on variant_id (epi = variant_id) AND customer email
-- Flag converted = order line item found AFTER wishlist add date
-- Key metric: wishlist-to-purchase conversion rate by product
SELECT * FROM {{ ref('stg_swym__wishlist_events') }}
