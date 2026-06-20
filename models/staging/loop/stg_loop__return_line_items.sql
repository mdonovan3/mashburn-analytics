{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_loop.return_line_items
--   id → return_line_item_id (STRING)
--   return_request_id → return_id (STRING)
--   line_item_id, product_id, variant_id → STRING
--   sku, title, variant_title, reason, parent_reason, outcome
--   price → NUMERIC
--   returned_at → TIMESTAMP

SELECT 1 AS stub
