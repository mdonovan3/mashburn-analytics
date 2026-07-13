# Customer Identity & Conversion Tracking

Cross-cutting question that touches [Data Sources](../data-sources/overview.md)
and [Data Modeling](../data-modeling/overview.md) alike: **can a customer
be reliably identified across all 5 systems, well enough to answer "did
this wishlist add / email click ever turn into a purchase?"**

Short answer: yes, using data these platforms already provide — no new
identity/CDP tool needed. Below is what was actually checked (not assumed)
and what's still an open business-logic decision rather than a data gap.

## Shopify is the identity anchor

`customers.email` and `orders.email` are both already modeled fields (see
`ingestion/schemas.py`) — every other source's identity signal gets
resolved back to a Shopify `customer.id` via one of these.

## Per-source findings

| Source | Identity field(s) | Status |
|---|---|---|
| Shopify | `customers.email`, `customers.id`, `orders.email` | :white_check_mark: Confirmed — the anchor everything else joins to |
| Loop Returns | `customer_email` + `provider_order_id` (Shopify order id) | :white_check_mark: Present in the modeled schema |
| Klaviyo | `customer_email` on `email_events` | :white_check_mark: **Confirmed by design** — Klaviyo's real [Events API](https://developers.klaviyo.com/en/reference/events_api_overview) requires every event to carry a profile identifier (`id`/`email`/`phone_number`). Not just "the field happens to exist," it's structurally required |
| Swym `waitlist_signups` | `customer_email` | :white_check_mark: Present in the modeled schema |
| Swym `wishlist_events` | — | :warning: **Gap found, then resolved** — see below |
| ShipHero `shipments` | `order_id` only (no direct customer field) | :white_check_mark: Fine — resolves transitively through the Shopify order, no identity work needed at this layer |

## The one real gap: Swym `wishlist_events`

The mock schema this project modeled
([`SWYM_WISHLIST_EVENTS`](https://github.com/mdonovan3/mashburn-analytics/blob/main/ingestion/schemas.py))
has no email or customer_id field — only `di` (a device identifier). That
looked like a real problem: `int_wishlist_to_purchase`'s own TODO comment
calls for matching on "variant_id **and customer email**," a field that
doesn't exist on this table as modeled.

**Checked against Swym's actual developer docs** — not assumed —
[developers.getswym.com/docs/wishlist-add](https://developers.getswym.com/docs/wishlist-add):
every real wishlist webhook (`AddToWishlist`, `RemoveWishlist`,
`ShareWishlist`, `AuthEmail`, etc.) includes a `User` object with `UserId`,
`Medium` (set to `"email"`), and `MediumValue` (the actual email address).

**Conclusion: the real API has what's needed. The mock schema was just
incomplete.** Fix is mechanical — add an email field to
`SWYM_WISHLIST_EVENTS` in `ingestion/schemas.py` (and to the real dlt
source once that's built) — not a design problem. Not yet applied to the
mock schema; tracked in [Status & Roadmap](../status.md).

## What's a genuine decision, not a data problem

A clean join doesn't automatically mean correct *attribution*. Specifically
for Klaviyo email-to-purchase conversion tracking (not yet a scaffolded
model):

- A guest-checkout order can use a different email than the one Klaviyo
  has on file for that shopper — silently undercounts conversions.
- Shared/family emails can overcount.
- "Conversion" itself needs an explicit definition: a time window (e.g.
  order within 7 days of a click) and a single-touch vs. multi-touch rule,
  chosen deliberately and documented in the mart's `schema.yml` — not left
  implicit in a `JOIN`. Last-touch, within a short window, is the simplest
  defensible starting definition.

## Recommended implementation

A canonical identity-resolution model in dbt — e.g. `int_customer_identity`
— anchored on Shopify `customer.id`, resolving `email` (and `device_id`
where relevant) from every other source back to one row per customer. A
`LEFT JOIN` + `COALESCE` pattern, not a new model architecture. This
belongs in the [intermediate](../data-modeling/intermediate.md) layer —
either folded into `int_wishlist_to_purchase` or split out so other marts
(Klaviyo conversion, once built) can reuse it instead of re-deriving the
same joins.

## Deliberately not pursuing: a dedicated CDP

Tools like Segment or mParticle solve a different problem — real-time
cross-channel identity activation at large scale. That's inconsistent with
the self-hosted, minimal-new-vendor approach argued for throughout this
project (see [Managed vs. Self-Hosted](managed-vs-self-hosted.md)) and
isn't needed here — plain `email` joins in dbt cover what's actually
required.

## Out of scope, worth naming: on-site browsing activity

Product page views, cart adds, and checkout starts short of a completed
order are a *different* thing from the wishlist/email/purchase events
covered above, and **none of this project's 5 modeled sources capture
them**. Shopify exposes this via its Web Pixels API / Customer Events,
which would need its own evaluation (ingestion approach, data volume,
whether Mashburn already has GA4 or similar covering this) before it's
part of the identity picture — not assumed to already be covered by
anything discussed on this page.

## Status

:white_check_mark: Research done — identity resolution across all 5
sources is confirmed feasible with data these platforms already provide.
:clipboard: Not yet built — the `SWYM_WISHLIST_EVENTS` mock-schema fix,
the `int_customer_identity` model, and the Klaviyo conversion mart (with
its attribution rule) are all still open work. Tracked in
[Status & Roadmap](../status.md).
