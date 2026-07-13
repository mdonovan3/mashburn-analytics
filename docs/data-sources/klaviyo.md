# Klaviyo

Email/SMS marketing — campaigns and message-level events. **Assumed** to be
in use (near-universal for Shopify-native email at this size of retailer),
not independently confirmed, and not yet part of the connector research
done for the other four sources.

| | |
|---|---|
| **Mock data** | :white_check_mark: Implemented — `raw_klaviyo` populated in BigQuery |
| **dlt source** | :clipboard: Planned — not started |
| **API style** | :white_check_mark: Researched — REST, cursor-based pagination (confirmed via [developers.klaviyo.com](https://developers.klaviyo.com/en/reference/api_overview)) |
| **Auth** | Private API key via `Authorization: Klaviyo-API-Key <key>` header (OAuth also available for server-side apps) |
| **Rate limits** | Fixed-window (burst + short-window, plus a longer steady-state window), enforced per account — private-key integrations **share one quota across the whole account**, so this and any other Klaviyo integration in use would compete for the same limit; HTTP 429 on exceeding |
| **Managed connector coverage** | Not independently verified for this project (Klaviyo is a common connector on most platforms generally, but that claim hasn't been checked against each vendor's actual docs the way Shopify/ShipHero/Loop/Swym were) |

## Tables

| Table | Grain | Key fields |
|---|---|---|
| `email_events` | one row per message event | `id`, `customer_email`, `campaign_id`, `flow_id`, `event_type` (sent/opened/clicked/bounced/unsubscribed), `created_at` |
| `campaigns` | one row per campaign | `id`, `name`, `subject`, `status`, `sent_at`, `open_rate`, `click_rate` |

Feeds the "what revenue is attributable to email campaigns vs. flows"
business question, joined against Shopify order data.

## API shape

Klaviyo's real Events API is confirmed to require a profile identifier
(`id`/`email`/`phone_number`) on every event — already established in
[Customer Identity & Conversion Tracking](../architecture/customer-identity.md),
which is what makes the `customer_email` join to Shopify orders sound. On
top of that, the REST/API-key/cursor-pagination shape means the dlt source
here can follow the same declarative `rest_api_source` pattern as Shopify
— no GraphQL, no refresh-token dance like ShipHero. The one design point
worth resolving before scaffolding is the shared per-account rate limit:
if Mashburn runs other Klaviyo-connected tools alongside this pipeline,
they'd all draw from the same quota, so the sync schedule/page size may
need tuning to avoid 429s rather than just maxing out request concurrency.

## Status note

Klaviyo is the least-developed source in this project in one specific way
that the API research above doesn't resolve — it exists in the mock data
and dbt source declarations because it was assumed to round out a
realistic picture of the marketing stack, but unlike the other four
sources it hasn't gone through the same *usage* verification pass. A
page-source check of shopmashburn.com (the same pass that confirmed Swym
and turned up the `returns.shopmashburn.com` portal) didn't surface a
Klaviyo tracking pixel or script — but that's a weak negative signal, not
real evidence of absence: marketing pixels load via JavaScript and
generally don't show up in a static HTML/markdown read the way a footer
link does. Before scaffolding a dlt source for this one, confirm it's
actually in use (checking network requests in a real browser, or asking
someone at the company) — the API shape is now known, but *is Klaviyo
actually the tool in use* is still open.
