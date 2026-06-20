{{ config(materialized='view') }}

-- TODO: Implement — sent_at → TIMESTAMP; open_rate/click_rate already FLOAT
SELECT * FROM {{ source('klaviyo', 'campaigns') }}
