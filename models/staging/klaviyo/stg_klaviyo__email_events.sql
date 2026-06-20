{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_klaviyo.email_events
--   id → event_id (STRING)
--   campaign_id, flow_id → STRING
--   customer_email, event_type, subject
--   created_at → TIMESTAMP

SELECT 1 AS stub
