{{ config(materialized='table') }}

-- TODO: Return analysis mart
-- Columns: month, total_returns, return_rate, pct_exchange, pct_refund, pct_credit
--   top_return_reason, avg_days_to_return
--   return_revenue_impact (refunds issued vs exchanges retained)
-- Key question: what % of returns become exchanges? (exchanges keep revenue)
SELECT 1 AS stub
