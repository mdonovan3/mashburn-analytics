{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)               AS order_id,
    CAST(customer_id AS STRING)      AS customer_id,
    CAST(location_id AS STRING)      AS location_id,
    order_number,
    email,
    source_name,
    financial_status,
    fulfillment_status,
    CAST(total_price AS NUMERIC)     AS total_price,
    CAST(subtotal_price AS NUMERIC)  AS subtotal_price,
    CAST(total_discounts AS NUMERIC) AS total_discounts,
    CAST(total_tax AS NUMERIC)       AS total_tax,
    currency,
    tags,
    discount_codes,
    CASE WHEN location_id IS NULL THEN 'ecommerce' ELSE 'pos' END AS channel,
    CAST(created_at AS TIMESTAMP)    AS created_at,
    CAST(updated_at AS TIMESTAMP)    AS updated_at
FROM {{ source('shopify', 'orders') }}
