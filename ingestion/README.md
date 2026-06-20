# Ingestion Scripts

Python scripts for loading mock data into BigQuery and simulating incremental data.

## Setup

```bash
pip install google-cloud-bigquery
gcloud auth application-default login
```

## Load seed data (full refresh)

```bash
python ingestion/load_to_bigquery.py \
  --batch mock_data/seed \
  --project mashburn-analytics-dev
```

## Load incremental data (append)

```bash
# Generate a new daily batch
python ingestion/generate_daily.py \
  --date 2026-06-20 \
  --output mock_data/incremental/2026-06-20

# Load it
python ingestion/load_to_bigquery.py \
  --batch mock_data/incremental/2026-06-20 \
  --project mashburn-analytics-dev \
  --mode append
```

## File format

Each batch directory has subdirectories per source:
```
{batch}/
  shopify/
    orders.json         {"orders": [...]}
    customers.json      {"customers": [...]}
    products.json       {"products": [...]}
    inventory_levels.json
    locations.json
  shiphero/
    shipments.json      {"shipments": [...]}
  swym/
    wishlist_events.json   {"events": [...]}
    waitlist_signups.json  {"waitlist": [...]}
  loop/
    returns.json        {"returns": [...]}   # split into return_requests + return_line_items
  klaviyo/
    campaigns.json      {"campaigns": [...]}
    email_events.json   {"events": [...]}
```

## Schemas

See `ingestion/schemas.py` for BigQuery `SchemaField` definitions for all tables.

The loader creates datasets automatically if they don't exist:
- `raw_shopify`
- `raw_shiphero`
- `raw_swym`
- `raw_loop`
- `raw_klaviyo`
