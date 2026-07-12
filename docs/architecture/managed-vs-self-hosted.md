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
