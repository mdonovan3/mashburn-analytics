# Data Sources — Overview

Five systems, matching what's confirmed or assumed to be live on
shopmashburn.com and used operationally.

| Source | What it is | Mock data | dlt source | Managed connector coverage |
|---|---|---|---|---|
| [Shopify](shopify.md) | Orders, customers, products, inventory | :white_check_mark: | :jigsaw: Scaffolded | Native on Fivetran/Airbyte/Portable/Hevo |
| [ShipHero](shiphero.md) | WMS / fulfillment | :white_check_mark: | :jigsaw: Scaffolded | Native on Fivetran, Portable — **not** Airbyte (marketing pages only) |
| [Loop Returns](loop-returns.md) | Self-serve returns portal | :white_check_mark: | :clipboard: Planned | Native on Fivetran, Portable |
| [Swym](swym.md) | Wishlist + back-in-stock waitlist | :white_check_mark: | :clipboard: Planned | Not found on any evaluated platform — custom build only |
| [Klaviyo](klaviyo.md) | Email/SMS marketing | :white_check_mark: | :clipboard: Planned | Native on most platforms (not independently verified for this project) |

## Confidence on each source being real

> **Note copied from the original project README:** Swym is confirmed on
> shopmashburn.com (wishlist heart icon on PDPs). Loop Returns is the
> dominant returns platform in the Shopify ecosystem for fashion/DTC —
> assumed, not confirmed. Klaviyo is nearly universal for Shopify-native
> email — assumed until confirmed otherwise.

## Connector research: why dlt over a managed platform

Four platforms were evaluated for the production ingestion path before
deciding to build on [dlt](../services/dlt.md) directly — see
[Evaluated, not chosen](../services/evaluated-not-chosen.md) for the full
writeup. Short version: coverage of these specific sources is uneven across
vendors (ShipHero is missing from Airbyte entirely; Swym isn't a native
connector anywhere), so at least 2 of 4 sources needed a custom build
regardless of platform choice. That tipped the decision toward dlt — no
platform fee, full control, and the custom-connector work is the same
either way.

One live finding worth flagging: several vendor comparison pages
(`portable.io/learn/does-X-have-a-Y-connector`) exist for nearly every
tool×tool combination as auto-generated SEO content, regardless of whether
the claim is true. The ShipHero-on-Airbyte and ShipHero-on-Fivetran
questions were both initially answered wrong by trusting those pages —
always cross-checked against the vendor's own docs domain
(`fivetran.com/docs/...`, `docs.airbyte.com/...`) before relying on a
coverage claim.

## Per-source detail pages

Each page below covers: what the source is, the tables/fields modeled,
current ingestion status (mock + dlt), and — where researched — real
connector coverage across managed platforms.

- [Shopify](shopify.md)
- [ShipHero](shiphero.md)
- [Loop Returns](loop-returns.md)
- [Swym](swym.md)
- [Klaviyo](klaviyo.md)
