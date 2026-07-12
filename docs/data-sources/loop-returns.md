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
| **API style** | Not yet researched for this project |
| **Managed connector coverage** | Native on Fivetran, Portable (for Loop specifically — moot if the real platform turns out to be a competitor) |

## Tables

| Table | Grain | Key fields |
|---|---|---|
| `return_requests` | one row per return | `id`, `order_name`, `provider_order_id` (Shopify order id), `state`, `type`, `total`, `refund`, `exchange`, `gift_card` |
| `return_line_items` | one row per returned item | `id`, `return_request_id`, `product_id`, `variant_id`, `reason`, `parent_reason`, `outcome` (reject/donate/review/keep/default), `returned_at` |

`exchange` vs. `refund` vs. `gift_card` on `return_requests` is the basis
for the "what % of returns become exchanges vs. cash refunds" business
question — exchanges keep revenue, refunds don't.

## What's next before building the dlt source

1. **Confirm the actual returns platform** — visit `returns.shopmashburn.com`
   and check its page source/footer branding to verify it's Loop and not a
   competitor (Return Prime, AfterShip Returns, Narvar all use the same
   subdomain-portal pattern).
2. Then research that platform's API style (REST vs. GraphQL), auth model,
   and rate limits — don't assume it's REST just because Shopify was;
   ShipHero's GraphQL surprise is the reason to check first rather than
   guess.
3. Only then scaffold `ingestion/dlt/loop-returns/`.
