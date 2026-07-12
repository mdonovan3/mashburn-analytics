"""Entrypoint for the Shopify dlt pipeline -> BigQuery.

Run:
    cd ingestion/dlt
    python shopify_pipeline.py

Requires .dlt/config.toml (shop_url) and .dlt/secrets.toml (access_token) —
copy .dlt/secrets.toml.example and fill it in. See README.md.

BigQuery auth reuses this project's existing Application Default Credentials
(same as ingestion/load_to_bigquery.py, see ../../CONNECTION.md) — no service
account key needed as long as `gcloud auth application-default login` has
already been run.
"""

import dlt
from shopify_source import shopify_source


def run() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="shopify",
        destination="bigquery",
        dataset_name="raw_shopify",
    )
    load_info = pipeline.run(shopify_source())
    print(load_info)


if __name__ == "__main__":
    run()
