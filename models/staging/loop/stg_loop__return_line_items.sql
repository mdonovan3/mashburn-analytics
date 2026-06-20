{{ config(materialized='view') }}

-- TODO: Implement — cast product_id, variant_id to STRING; price to NUMERIC
-- returned_at → TIMESTAMP
-- outcome: reject | donate | review | keep | default
SELECT * FROM {{ source('loop_returns', 'return_line_items') }}
