{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING) AS location_id,
    name,
    city,
    province           AS state,
    country,
    zip,
    active
FROM {{ source('shopify', 'locations') }}
