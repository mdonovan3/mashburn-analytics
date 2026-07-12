# Evaluated, not chosen

Four managed ELT platforms were researched before deciding to build the
ingestion layer on [dlt](dlt.md) directly. Summarized on
[Managed vs. Self-Hosted](../architecture/managed-vs-self-hosted.md); full
detail and sourcing here.

## Connector coverage for these 4 specific sources

| Source | Fivetran | Airbyte | Portable | Hevo |
|---|---|---|---|---|
| Shopify | native | native | native | native |
| ShipHero | native | **no real connector** | native | not confirmed |
| Loop Returns | native | not found | native | not confirmed |
| Swym | not found | not found | buildable on request (custom, ~days) | not confirmed |

## Fivetran

Best raw connector coverage of anything evaluated — genuinely has native
Shopify, ShipHero, *and* Loop Returns connectors (confirmed via Fivetran's
own docs and a real support-forum announcement thread, not a marketing
page). The blocker is cost at this scale: **$500 per million Monthly
Active Rows, with a $12,000/year minimum** — the floor alone is a lot to
pay for 4 low-volume sources at a company this size (see
[sizing context](../architecture/managed-vs-self-hosted.md#sizing-context-how-big-is-this-actually)).
A 2025 shift to per-connector billing also reportedly spiked many
customers' bills 50-60%+.

## Airbyte

Open source, cheapest at real scale (median contract ~$16K/yr vs.
Fivetran's ~$44K/yr per public reporting), self-hostable at flat compute
cost regardless of row volume. The catch for this project specifically:
**no real ShipHero connector** — `airbyte.com/connections/ShipHero-to-*`
pages exist, but they're auto-generated SEO/marketing pages, not backed by
an actual maintained connector in Airbyte's catalog or GitHub repo. Would
need the same custom low-code connector work as dlt, for a source that's
arguably the trickiest of the four (GraphQL API, refresh-token auth — see
[ShipHero](../data-sources/shiphero.md)).

## Portable.io

Flat-rate pricing (not volume/MAR-based), real connectors for Shopify,
ShipHero, and Loop Returns, and their whole pitch is building niche
connectors like Swym on request, typically within days. Genuinely the
strongest "just replace the outsourced vendor with minimal engineering
lift" option of the four. Not chosen mainly because: (a) pricing isn't
public — needs a sales conversation to know the real number — and (b) it's
still a vendor relationship, which cuts somewhat against the role's actual
mandate of *reducing* outsourced dependency rather than trading one vendor
for another.

## Hevo

Native Shopify connector, Starter plan from ~$299/month. ShipHero/Loop
Returns/Swym coverage was not confirmed in either direction during
research — Hevo's own docs and searches didn't surface those connectors,
but that's weaker evidence than the explicit "not in the catalog" finding
for Airbyte/ShipHero. Not pursued further once Portable and dlt covered
the more clearly-evaluated options.

## A methodological note worth keeping

Several of these platforms (Portable especially) run
`does-<vendor>-have-a-<connector>` pages for nearly every tool×tool
combination as auto-generated SEO content — they exist regardless of
whether the underlying claim is actually true, which makes them
unreliable in *either* direction. This research hit both cases with the
same page pattern, for the same source: a `does-airbyte-have-a-shiphero-connector`-style
page turned out to be correct (Airbyte genuinely has no real ShipHero
connector, confirmed against Airbyte's own docs/catalog), while a
`does-fivetran-have-a-shiphero-connector`-style page turned out to be
**wrong** (Fivetran does have one, confirmed against Fivetran's own docs
and a real support-forum announcement). Since the same style of page was
right once and wrong once, the pattern itself carries no signal — only
cross-checking the actual vendor's own docs domain
(`fivetran.com/docs/...`, `docs.airbyte.com/...`) settles it. Worth
remembering for any future vendor research.
