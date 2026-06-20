{{ config(materialized='ephemeral') }}

-- TODO: Combine Loop return requests + line items + Shopify order line items
-- Output: one row per returned item with
--   original order date, return date, days_to_return
--   return_resolution (refund/exchange/credit)
--   reason, outcome, product_type, vendor
SELECT * FROM {{ ref('stg_loop__return_requests') }}
