# Managed vs. Self-Hosted

Both halves of the in-house build-out — **ingestion** and **the dbt run
process** — have a managed-platform option and a self-hosted option. This
page lays out both decisions side by side with cost, pros, and cons, and
gives a sizing-informed recommendation.

## Sizing context: how big is this, actually?

Mashburn operates **~8 markets with separate Sid Mashburn (menswear) and
Ann Mashburn (womenswear) stores in each** (roughly 15 physical locations),
plus e-commerce, plus a seasonal "On the Road" pop-up program — a
specialty/boutique multi-brand retailer, not a national chain. (Source:
company site + Wikipedia; exact revenue/order volume not public.)

**Catalog size, roughly:** shopmashburn.com's public Shopify sitemap is
split across 3 `sitemap_products_*.xml` files; spot-checking one file
showed on the order of several hundred `<url>` entries. That points to a
catalog in the **low thousands of products** (menswear + womenswear + kids
combined) — not the tens-of-thousands-plus range a mass-market retailer
would have. Treat this as a rough order-of-magnitude estimate from public
sitemap inspection, not a confirmed number.

That matters for this decision: at this scale, order/customer/inventory
row counts are almost certainly in the thousands-to-tens-of-thousands per
day range, not millions, and the product catalog itself is small enough
that `products`/`product_variants` syncs will always be quick regardless of
tooling. The headline value proposition of the expensive managed platforms
— reliably handling massive scale, or supporting large multi-team
collaboration — isn't really the constraint here. **Cost per seat/row and
operational simplicity for a small team matter more than raw throughput
ceiling.** That biases this whole page toward self-hosted options, and
that bias is stated up front rather than hidden in the "recommendation"
section.

## Estimated data volumes

!!! warning "Illustrative planning model, not real numbers"
    Mashburn hasn't shared actual order/traffic data with this project.
    The order-volume estimate below is grounded in two public data points —
    third-party revenue estimates and actual observed price points from
    shopmashburn.com — rather than a pure guess, but it's still a
    back-of-envelope model, not a confirmed number. Stated explicitly so
    it's easy to throw out and replace with real numbers on day one. Treat
    the "why it matters" conclusions as more durable than the specific row
    counts.

**Order volume, derived from revenue ÷ average order value:**

- **Revenue:** third-party estimates (Growjo, RocketReach — algorithmic
  estimates for a private company, not filed financials) put combined
  Sid + Ann Mashburn revenue at **$28M–$44M/year**.
- **Average order value (AOV):** built from actual prices pulled off the
  site — silk ties $155, dress socks $15, ready-to-wear sport coats
  $950–$1,695, made-to-measure suits from $2,295. A single-item accessory
  order sits well under $200; a jacket or suit order alone clears
  $1,000+. Blended across a catalog with that spread (and skewed toward
  the more frequently-bought lower end — shirts, ties, accessories —
  rather than suits), **$250–$400** is a reasonable estimated AOV for a
  specialty menswear/womenswear retailer at this price tier.
- **Orders/year = revenue ÷ AOV:** $28M / $400 ≈ **70,000** at the low end,
  $44M / $250 ≈ **175,000** at the high end → **~192–480 orders/day**,
  call it **~300/day mid-case**.

This mid-case (~300 orders/day) happens to land close to an independent
foot-traffic-based guess (~15 stores × modest daily transactions +
e-commerce) made earlier in this project's research — two different
methods landing in the same neighborhood is a reasonable sanity check,
though both ultimately rest on third-party/estimated inputs rather than
confirmed figures.

| Table | Source | Est. rows/day (mid, low–high) | Est. rows/month | Basis |
|---|---|---|---|---|
| `orders` | Shopify | ~300 (192–480) | ~9K (6K–14K) | revenue ÷ AOV, derived above |
| `order_line_items` | Shopify | ~750 (480–1,200) | ~22K (14K–36K) | ~2.5 items/order |
| `customers` (new+updated) | Shopify | ~150 (100–240) | ~4.5K (3K–7K) | ~0.5x order volume — new signups + repeat-customer profile/order-count updates |
| `locations` | Shopify | ~0 | negligible | ~15–16 total rows; store openings/closings are rare events, not a daily-volume source |
| `products` (changed) | Shopify | ~50 | ~1.5K | driven by catalog refresh cadence (new arrivals, discontinued items), roughly independent of order volume |
| `product_variants` (changed) | Shopify | ~150 | ~4.5K | ~3 variants/product on average; same low-churn logic as `products` |
| `inventory_levels` (changed) | Shopify | ~1,000–2,000 | ~35K | variants × ~16 locations is a large cross-product; every sale/restock touches a row — likely the largest Shopify contributor |
| `shipments` | ShipHero | ~330 (210–530) | ~10K (6K–16K) | ~1.1x order volume, not 1:1 — accounts for split shipments: buy-online-ship-from-store across multiple physical locations, and made-to-measure pieces (a meaningful part of this catalog — MTM suits/jackets/topcoats) which typically ship separately from any in-stock items on the same order |
| `shipping_labels` | ShipHero | ~350 (220–560) | ~10.5K (7K–17K) | ~1.05x `shipments` — most shipments are single-box/single-label, small allowance for multi-box packages |
| `return_requests` | Loop | ~50–75 | ~2K | apparel return rates typically run 15–25% of orders |
| `return_line_items` | Loop | ~90 | ~2.5K | ~1.5x `return_requests` — some returns include multiple items |
| `wishlist_events` | Swym | ~600–1,200 | ~27K | wishlist adds outpace purchases — a higher-funnel, lower-commitment action, roughly 2–3x order volume |
| `waitlist_signups` | Swym | ~30 | ~1K | back-in-stock signups — smaller subset of wishlist activity |
| `email_events` | Klaviyo | ~5,000–20,000 | **~350K** | sends+opens+clicks across a subscriber list — reliably the largest volume source in any retail data stack, usually by 5–10x over the next-largest table |
| `campaigns` | Klaviyo | <5 | negligible | — |

**Rough total: ~0.3–0.6M rows/month across all 5 sources combined**
(mid-case sums to ≈480K), overwhelmingly dominated by Klaviyo email events
(~70-75% of the total). Everything else — including both ShipHero tables
combined (~20K/month mid-case) — is a small fraction of that. Note that
`SHIPHERO_SHIPMENTS` is the only ShipHero table actually implemented in
this project's schema (`ingestion/schemas.py`); the original project
README also mentions `inventory_movements` and `returns` as conceptually
part of ShipHero's WMS data, but neither is modeled here, so there's no
volume estimate for them.

**Why this number matters:** Fivetran's $500/million-MAR pricing with a
$12,000/year minimum effectively pre-pays for **2M rows/month**. Even the
high end of this estimate (~0.6M/month) is well under a third of what
that floor already covers — a concrete version of the "the floor alone
likely exceeds what's needed" claim made throughout this page, not just an
assertion.

## Ingestion: managed platform vs. self-hosted (dlt)

| Option | Type | Approx. cost at this scale | Pros | Cons |
|---|---|---|---|---|
| **dlt + Cloud Run Jobs** :white_check_mark: chosen | Self-hosted | GCP compute only — a few dollars/month for daily runs of this size (Cloud Run Jobs bill per second, no idle cost) | No platform fee; full control of every field/transform; same GCP project/billing/IAM as BigQuery; scales down to near-zero cost at low volume | You own connector maintenance for niche sources (ShipHero, Loop, Swym); no vendor support line; more upfront build time |
| Fivetran | Managed | $500/million Monthly Active Rows, **$12K/yr minimum** — the floor alone likely exceeds what 4 low-volume sources need | Best connector coverage of anything evaluated (has Shopify, ShipHero, *and* Loop Returns natively) | Priciest by a wide margin at this scale; per-connector billing change in 2025 spiked many customers' bills 50-60%+ |
| Airbyte Cloud / self-hosted OSS | Managed or self-hosted | Cloud: ~$10/mo + usage credits. Self-hosted: compute only, flat regardless of row volume | Cheapest at real scale (~$16K/yr median contract vs. Fivetran's ~$44K/yr per public reporting); open source | **No real ShipHero connector** (only auto-generated marketing pages, not in their actual catalog) — would need a custom low-code connector anyway, same work as dlt |
| Portable.io | Managed | Flat-rate, undisclosed publicly — sales quote needed | Real Shopify/ShipHero/Loop Returns connectors; builds niche ones (Swym) on request in days; not volume-priced | Pricing opacity; still a vendor dependency for a role whose mandate is reducing vendor dependency |
| Hevo | Managed | Starter ~$299/mo+ | Native Shopify | ShipHero/Loop/Swym coverage unconfirmed — likely needs custom work too |

Full writeup with sourcing: [Evaluated, not chosen](../services/evaluated-not-chosen.md).

**Why dlt won:** 2 of 4 sources (ShipHero, and definitely Swym) need a
custom connector on *any* platform, including the expensive ones — so the
custom-build cost is fixed regardless of vendor choice. Given that, paying
a platform fee on top buys relatively little at this data volume. dlt gets
the same outcome (data in BigQuery, on schedule, incrementally) for
infrastructure cost only.

### What volume range justifies each option

| Option | Volume where it's actually justified | Why |
|---|---|---|
| **dlt + Cloud Run Jobs** | No meaningful lower bound — works fine even smaller than this. Scales up to tens of millions of rows/month on a single container before you'd need to think about parallelization | Compute-priced, not row-priced. The eventual ceiling is Cloud Run's per-task timeout (up to 7 days) and single-container throughput, not cost — a ceiling this project is nowhere near |
| **Fivetran** | Starts making economic sense once real usage approaches/exceeds ~2M rows/month (what the $12K/yr floor already covers), *or* regardless of volume once there's truly zero in-house engineering bandwidth for connector upkeep | Mashburn's estimated ~0.3–0.6M rows/month is a fraction of the floor — paying mostly for coverage/reliability/support, not for capacity actually used |
| **Airbyte Cloud** | Cost-competitive against Fivetran roughly in the tens-of-millions-of-rows/month range, per the public contract-value comparison cited above | Below that range, usage-based credits don't obviously beat self-hosted OSS or dlt on cost — the free lunch is at the high end, not the low end |
| **Airbyte self-hosted OSS** | Same "works at any volume" profile as dlt, since it's also compute-priced | The real gap for this project isn't volume, it's the missing native ShipHero connector |
| **Portable.io** | Flat-rate pricing makes it specifically attractive at **low volume with several niche connectors needed** — exactly this project's shape | Could look relatively worse at very high volume, where a per-row platform's marginal cost might undercut a flat fee — not a problem at Mashburn's scale |
| **Hevo** | Similar reasoning to Fivetran, but a lower cost floor (~$239–299/mo) — better fit than Fivetran at small scale, still pricier than self-hosted here | Event-based tiers still mean paying for headroom this project's volume doesn't use |

## dbt run process: dbt Cloud vs. self-hosted dbt Core

| Option | Type | Approx. cost | Pros | Cons |
|---|---|---|---|---|
| **dbt Core + Cloud Run Jobs** :jigsaw: proposed | Self-hosted | GCP compute only — same near-zero marginal cost as the ingestion jobs, since it's the identical Cloud Scheduler → Cloud Run Job pattern already built | Reuses infrastructure/patterns already in place for ingestion — one more container + one more Scheduler entry, not a new system; zero seat cost; full control over CI checks | No hosted docs site, no browser IDE, no built-in job UI — have to build/accept less tooling around it (or self-host `dbt docs generate` output, e.g. onto this same docs site) |
| dbt Cloud — Developer (free) | Managed | $0, 1 seat, 3,000 model builds/mo included | Hosted IDE, hosted docs, manual/API job runs, zero infra to run | **Single seat only** — doesn't scale to a second analyst/engineer; still limited scheduling |
| dbt Cloud — Team | Managed | $100/seat/month | Cron-based scheduling, CI/CD, hosted docs, unlimited projects | At even 2 seats that's $2,400/yr — real money for a small team, for capability (scheduling, docs hosting) the self-hosted route gets for free by reusing existing GCP infra |
| dbt Core + Airflow/Dagster | Self-hosted | Cluster/compute cost + real operational overhead | Best choice **if** the team ends up needing a full orchestrator anyway (e.g. once Loop/Swym/Klaviyo pipelines create real cross-source dependencies) | Overkill today — same "why not a full orchestrator" reasoning as the ingestion side (see [Orchestration & Deployment](orchestration-deployment.md)) |
| dbt Core + GitHub Actions | Self-hosted | Free on a public repo's included minutes | Zero infra to run or maintain; cron trigger, secrets, logs all built into GitHub already | Data leaves GCP's network for the run (GitHub-hosted runner) unless using a self-hosted runner; less natural fit than staying inside the same GCP project as BigQuery + the ingestion Jobs |

## Recommendation

**Self-host both, on the same pattern.** The ingestion architecture already
being built (Cloud Scheduler → Cloud Run Jobs → BigQuery, see
[Orchestration & Deployment](orchestration-deployment.md)) extends directly
to running `dbt build` — add one more Cloud Run Job (a small image with
`dbt-bigquery` installed) and one more Scheduler entry, timed to fire after
the ingestion jobs finish (or triggered by a Pub/Sub message from the last
ingestion job's completion, if sequencing needs to be exact rather than
just time-offset). No new system, no per-seat cost, no new vendor
relationship — which lines up with the actual mandate of the role: reduce
outsourced/vendor dependency, not add a new one.

**Reassess if:** the team grows past ~2-3 people needing simultaneous dbt
development access (dbt Cloud's IDE/collaboration features start earning
their cost), or Loop Returns/Swym/Klaviyo pipelines create real
cross-source sequencing dependencies that outgrow "run dbt after ingestion,
offset by N minutes" (that's the trigger to revisit a full orchestrator —
see the same threshold discussed for ingestion).

## Status of this page

:jigsaw: This is a proposal — no dbt-on-Cloud-Run-Jobs container has been
built yet (only the ingestion containers exist so far, see
[Ingestion Layer](ingestion.md)). Tracked in
[Status & Roadmap](../status.md).
