{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)            AS customer_id,
    email,
    first_name,
    last_name,
    phone,
    orders_count,
    CAST(total_spent AS NUMERIC)  AS total_spent,
    tags,
    accepts_marketing,
    default_address.city          AS city,
    default_address.province      AS state,
    default_address.country       AS country,
    default_address.zip           AS zip,
    CAST(created_at AS TIMESTAMP) AS created_at,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM {{ source('shopify', 'customers') }}
