{{ config(materialized='view') }}

-- TODO: Implement — cast total/refund/exchange/gift_card to NUMERIC
-- Derive return_resolution: CASE WHEN refund > 0 THEN 'refund' WHEN exchange > 0 THEN 'exchange' ...
-- provider_order_id = Shopify order_id (STRING, already matches)
SELECT * FROM {{ source('loop_returns', 'return_requests') }}
