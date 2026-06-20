{{ config(materialized='table') }}

-- TODO: Monthly cohort retention table
-- Cohort = month of first purchase
-- Columns: cohort_month, months_since_first_purchase, customers_retained, retention_rate
-- Also: repeat_purchase_rate_90d, repeat_purchase_rate_180d
-- Key question: what % of customers come back within 90 / 180 / 365 days?
SELECT 1 AS stub
