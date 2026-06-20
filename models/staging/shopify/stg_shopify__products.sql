{{ config(materialized='view') }}

-- TODO: Implement this model
-- Source: raw_shopify.products
-- Key transforms:
--   - id → product_id (STRING)
--   - created_at, updated_at → TIMESTAMP
--   - tags stays as string (parse in marts)
--   - status: 'active' | 'draft' | 'archived'

SELECT * FROM {{ source('shopify', 'products') }}
