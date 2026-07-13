# Loop Returns

Self-serve returns portal — the dominant returns platform in the Shopify
ecosystem for fashion/DTC brands.

**Partially confirmed:** the footer of shopmashburn.com has a "Start A
Return" link pointing to `returns.shopmashburn.com` — a merchant-branded
subdomain returns portal, which is the standard hosting pattern Loop (and
similar platforms — Return Prime, AfterShip Returns, Narvar) use. That
confirms *a* returns platform is live; it does **not** confirm it's
specifically Loop rather than a competitor — that would need actually
loading the portal or checking its page source for the provider's own
branding/API calls, which hasn't been done yet.

| | |
|---|---|
| **Mock data** | :white_check_mark: Implemented — `raw_loop` populated in BigQuery |
| **dlt source** | :clipboard: Planned — not started |
| **API style** | :white_check_mark: Researched — REST, JSON, standard HTTP (confirmed via [docs.loopreturns.com](https://docs.loopreturns.com/api-reference/authentication)) — assuming the platform actually is Loop, see caveat above |
| **Auth** | API key via `X-Authorization` header, scoped per key (Cart/Return/Order/Report/Developer Tools/Destinations). OAuth 2.0 only required for the separate Label API and Webhooks API |
| **Managed connector coverage** | Native on Fivetran, Portable (for Loop specifically — moot if the real platform turns out to be a competitor) |

## Tables

| Table | Grain | Key fields |
|---|---|---|
| `return_requests` | one row per return | `id`, `order_name`, `provider_order_id` (Shopify order id), `state`, `type`, `total`, `refund`, `exchange`, `gift_card` |
| `return_line_items` | one row per returned item | `id`, `return_request_id`, `product_id`, `variant_id`, `reason`, `parent_reason`, `outcome` (reject/donate/review/keep/default), `returned_at` |

`exchange` vs. `refund` vs. `gift_card` on `return_requests` is the basis
for the "what % of returns become exchanges vs. cash refunds" business
question — exchanges keep revenue, refunds don't.

## API shape, if the platform is confirmed to be Loop

Good news for the dlt build: Loop's real API is REST with a simple static
API-key header — the same shape as Shopify, not the GraphQL/refresh-token
pattern ShipHero required. A declarative `rest_api_source` config (like
`shopify_source.py`) should fit cleanly, no custom `requests`-based
resource needed. Webhooks are also available (Loop supports a
webhooks-management API), which is worth a second look later as an
alternative to polling — a scheduled Cloud Run Job pulling on a cron is
still the simpler starting point and consistent with every other source
in this project, but Loop specifically has the option if latency ever
matters.

## What's next before building the dlt source

1. **Confirm the actual returns platform** — visit `returns.shopmashburn.com`
   and check its page source/footer branding to verify it's Loop and not a
   competitor (Return Prime, AfterShip Returns, Narvar all use the same
   subdomain-portal pattern). This is the one thing genuinely still
   unverified — the API research above assumes it checks out as Loop.
2. Generate a scoped API key (Return + Order read scopes should cover the
   two tables modeled here) and confirm the exact endpoint paths/response
   shapes against `docs.loopreturns.com` before writing the dlt config.
3. Then scaffold `ingestion/dlt/loop-returns/`.
