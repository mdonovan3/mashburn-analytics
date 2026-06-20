{{ config(materialized='view') }}

SELECT
    CAST(id AS STRING)          AS event_id,
    customer_email,
    CAST(campaign_id AS STRING) AS campaign_id,
    CAST(flow_id AS STRING)     AS flow_id,
    event_type,
    subject,
    CAST(created_at AS TIMESTAMP) AS created_at
FROM {{ source('klaviyo', 'email_events') }}
