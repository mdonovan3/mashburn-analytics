# Swym

Wishlist + back-in-stock waitlist. **Confirmed** live on shopmashburn.com —
"My Wishlist" links in the header/footer point to `/pages/swym-wishlist`
(Swym's own branding in the URL), plus heart icons on product cards. The
one source in this list that's directly verified rather than assumed.

| | |
|---|---|
| **Mock data** | :white_check_mark: Implemented — `raw_swym` populated in BigQuery |
| **dlt source** | :clipboard: Planned — not started |
| **API style** | Not yet researched for this project |
| **Managed connector coverage** | **None found** on any platform evaluated (Fivetran, Airbyte, Portable, Hevo) — this one is a custom build no matter which ingestion platform gets used |

## Tables

Field names below are Swym's actual (somewhat cryptic) API field names —
kept as-is in `raw_swym` on purpose, with human-readable meaning documented
in `sources.yml`; renaming happens in [staging](../data-modeling/staging.md).

| Table | Grain | Key fields (raw name → meaning) |
|---|---|---|
| `wishlist_events` | one row per add/remove event | `_pkey` (event id), `empi` (= Shopify `product_id`), `epi` (= Shopify `variant_id`), `pr` (price), `cts`/`uts` (created/updated, epoch millis) |
| `waitlist_signups` | one row per back-in-stock signup | `empi`, `epi`, `sku`, `customer_email`, `signed_up_at`, `notified_at`, `purchased_at` |

`empi`/`epi` are the join keys back to Shopify products/variants — this is
what makes the "wishlist-to-purchase conversion" and "back-in-stock
performance" business questions answerable at all (see
[`int_wishlist_to_purchase`](../data-modeling/intermediate.md)).

## Why this is the hardest source to bring in-house

Swym has no connector on any evaluated managed platform — confirmed via
direct search, not just absence from one vendor. Whatever ingestion
platform Mashburn ultimately standardizes on, Swym gets a hand-built
connector regardless. That was one of the deciding factors for choosing
dlt over a managed platform in the first place: paying a platform fee
doesn't remove this particular piece of custom work. See
[Evaluated, not chosen](../services/evaluated-not-chosen.md).
