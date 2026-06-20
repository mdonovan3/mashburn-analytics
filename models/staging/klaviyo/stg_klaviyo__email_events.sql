{{ config(materialized='view') }}

-- TODO: Implement — created_at → TIMESTAMP; event_type: sent/opened/clicked/bounced
-- campaign_id IS NOT NULL vs flow_id IS NOT NULL (mutually exclusive)
SELECT * FROM {{ source('klaviyo', 'email_events') }}
