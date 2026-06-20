{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)   AS campaign_id,
    name,
    subject,
    status,
    list_id,
    open_rate,
    click_rate,
    CAST(sent_at AS TIMESTAMP) AS sent_at
FROM {{ source('klaviyo', 'campaigns') }}
