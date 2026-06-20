#!/usr/bin/env python3
"""
Load mock data JSON files into BigQuery raw tables.

Usage:
    python ingestion/load_to_bigquery.py --batch mock_data/seed --project mashburn-analytics-dev
    python ingestion/load_to_bigquery.py --batch mock_data/incremental/2026-06-20 --project mashburn-analytics-dev --mode append
"""

import argparse
import json
import os
import sys
from pathlib import Path

from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig, WriteDisposition

from schemas import SCHEMAS


SOURCE_MAP = {
    "shopify": "raw_shopify",
    "shiphero": "raw_shiphero",
    "swym": "raw_swym",
    "loop": "raw_loop",
    "klaviyo": "raw_klaviyo",
}

# JSON envelope keys — outer key to unwrap
ENVELOPE_MAP = {
    "shopify/orders": "orders",
    "shopify/locations": "locations",
    "shopify/products": "products",
    "shopify/customers": "customers",
    "shopify/inventory_levels": "inventory_levels",
    "shiphero/shipments": "shipments",
    "swym/wishlist_events": "events",
    "swym/waitlist_signups": "waitlist",
    "loop/returns": "returns",
    "klaviyo/campaigns": "campaigns",
    "klaviyo/email_events": "events",
}


def get_client(project: str) -> bigquery.Client:
    return bigquery.Client(project=project)


def ensure_dataset(client: bigquery.Client, dataset_id: str) -> None:
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(f"{client.project}.{dataset_id}")
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)
        print(f"  Created dataset: {dataset_id}")


def load_table(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str,
    rows: list,
    schema,
    mode: str,
) -> None:
    table_ref = f"{client.project}.{dataset_id}.{table_id}"
    write_disp = (
        WriteDisposition.WRITE_TRUNCATE if mode == "full"
        else WriteDisposition.WRITE_APPEND
    )
    job_config = LoadJobConfig(
        schema=schema,
        write_disposition=write_disp,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
    job = client.load_table_from_json(
        json_rows=rows,
        destination=table_ref,
        job_config=job_config,
    )
    job.result()
    print(f"  Loaded {len(rows)} rows → {table_ref} [{mode}]")


def extract_order_line_items(orders: list) -> list:
    """Extract line_items from orders into a flat list."""
    line_items = []
    for order in orders:
        for li in order.get("line_items", []):
            row = {**li, "order_id": order["id"]}
            line_items.append(row)
    return line_items


def extract_shipping_labels(shipments: list) -> list:
    """Extract shipping_labels from shipments — unused for BQ nested schema but available."""
    labels = []
    for shipment in shipments:
        for lbl in shipment.get("shipping_labels", []):
            row = {**lbl, "shipment_id": shipment["id"], "order_id": shipment["order_id"]}
            labels.append(row)
    return labels


def process_batch(client: bigquery.Client, batch_path: Path, mode: str) -> None:
    for source_dir in sorted(batch_path.iterdir()):
        if not source_dir.is_dir():
            continue
        source_name = source_dir.name
        dataset_id = SOURCE_MAP.get(source_name)
        if dataset_id is None:
            print(f"  Warning: unknown source directory '{source_name}', skipping")
            continue

        ensure_dataset(client, dataset_id)
        dataset_schemas = SCHEMAS.get(dataset_id, {})

        for json_file in sorted(source_dir.glob("*.json")):
            table_name = json_file.stem  # e.g. "orders"
            envelope_key = f"{source_name}/{table_name}"
            envelope = ENVELOPE_MAP.get(envelope_key)

            with open(json_file) as f:
                raw = json.load(f)

            rows = raw[envelope] if envelope and isinstance(raw, dict) else raw

            # Special handling: Loop returns.json → return_requests + return_line_items
            if source_name == "loop" and table_name == "returns":
                # Load return_requests
                req_rows = []
                li_rows = []
                for ret in rows:
                    line_items = ret.pop("line_items", [])
                    req_rows.append(ret)
                    for li in line_items:
                        li_rows.append({**li, "return_request_id": ret["id"]})

                if "return_requests" in dataset_schemas:
                    load_table(client, dataset_id, "return_requests", req_rows, dataset_schemas["return_requests"], mode)
                if "return_line_items" in dataset_schemas:
                    load_table(client, dataset_id, "return_line_items", li_rows, dataset_schemas["return_line_items"], mode)
                continue

            # For orders: keep line_items as nested RECORD (BigQuery handles it)
            bq_table_name = table_name
            schema = dataset_schemas.get(bq_table_name)
            if schema is None:
                print(f"  Warning: no schema for {dataset_id}.{bq_table_name}, skipping")
                continue

            load_table(client, dataset_id, bq_table_name, rows, schema, mode)


def main():
    parser = argparse.ArgumentParser(description="Load mock data into BigQuery")
    parser.add_argument("--batch", required=True, help="Path to batch directory (e.g. mock_data/seed)")
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--mode", choices=["full", "append"], default="full",
                        help="full = WRITE_TRUNCATE, append = WRITE_APPEND")
    args = parser.parse_args()

    batch_path = Path(args.batch)
    if not batch_path.exists():
        print(f"Error: batch path '{batch_path}' does not exist")
        sys.exit(1)

    client = get_client(args.project)
    print(f"Loading batch: {batch_path} → project: {args.project} [{args.mode}]")
    process_batch(client, batch_path, args.mode)
    print("Done.")


if __name__ == "__main__":
    main()
