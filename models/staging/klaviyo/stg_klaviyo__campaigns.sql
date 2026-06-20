{{ config(materialized='view') }}

-- TODO: Rename and cast from raw_klaviyo.campaigns
--   id → campaign_id (STRING)
--   name, subject, status, list_id, open_rate, click_rate
--   sent_at → TIMESTAMP

SELECT 1 AS stub
