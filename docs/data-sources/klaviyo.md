# Klaviyo

Email/SMS marketing — campaigns and message-level events. **Assumed** to be
in use (near-universal for Shopify-native email at this size of retailer),
not independently confirmed, and not yet part of the connector research
done for the other four sources.

| | |
|---|---|
| **Mock data** | :white_check_mark: Implemented — `raw_klaviyo` populated in BigQuery |
| **dlt source** | :clipboard: Planned — not started, not yet researched |
| **API style** | Not yet researched for this project |
| **Managed connector coverage** | Not independently verified for this project (Klaviyo is a common connector on most platforms generally, but that claim hasn't been checked against each vendor's actual docs the way Shopify/ShipHero/Loop/Swym were) |

## Tables

| Table | Grain | Key fields |
|---|---|---|
| `email_events` | one row per message event | `id`, `customer_email`, `campaign_id`, `flow_id`, `event_type` (sent/opened/clicked/bounced/unsubscribed), `created_at` |
| `campaigns` | one row per campaign | `id`, `name`, `subject`, `status`, `sent_at`, `open_rate`, `click_rate` |

Feeds the "what revenue is attributable to email campaigns vs. flows"
business question, joined against Shopify order data.

## Status note

Klaviyo is the least-developed source in this project — it exists in the
mock data and dbt source declarations because it was assumed to round out
a realistic picture of the marketing stack, but unlike the other four
sources it hasn't gone through the same verification pass. A page-source
check of shopmashburn.com (the same pass that confirmed Swym and turned up
the `returns.shopmashburn.com` portal) didn't surface a Klaviyo tracking
pixel or script — but that's a weak negative signal, not real evidence of
absence: marketing pixels load via JavaScript and generally don't show up
in a static HTML/markdown read the way a footer link does. Before
scaffolding a dlt source for this one, confirm it's actually in use
(checking network requests in a real browser, or asking someone at the
company) and check its real API shape — don't assume the same
platform/pattern choices that worked for Shopify apply here.
