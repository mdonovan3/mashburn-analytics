{{ config(materialized='view') }}

-- TODO: Implement this model
-- Source: raw_shopify.customers
-- Key transforms:
--   - id → customer_id (STRING)
--   - total_spent → NUMERIC
--   - created_at, updated_at → TIMESTAMP
--   - default_address is a RECORD — flatten city/province/country/zip or keep nested
--   - tags stays as comma-separated string (split in marts if needed)
--   - accepts_marketing is BOOLEAN, no cast needed

SELECT * FROM {{ source('shopify', 'customers') }}
