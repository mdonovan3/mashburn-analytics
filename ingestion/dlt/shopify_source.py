"""dlt source for the Shopify Admin REST API.

Scaffolds the production-style Shopify ingestion path described in
docs/production-ingestion/NOTES.md: dlt owns extraction, incremental
state, and schema evolution. This is separate from ingestion/load_to_bigquery.py,
which loads *mock* data for local dbt development and is unaffected by this.

Resources match the raw_shopify tables already modeled in ingestion/schemas.py:
orders, customers, products, product_variants, locations, inventory_levels.

Requires a real Shopify store + Admin API access token to run — see README.md.
Not yet run end-to-end (no live store connected to this portfolio project).
"""

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources

SHOPIFY_API_VERSION = "2024-01"


@dlt.transformer(primary_key="id", write_disposition="merge")
def product_variants(product: dict):
    """Child resource: flattens each product's nested `variants` array.

    Shopify's Admin API has no standalone /variants.json endpoint — variants
    only come back nested inside /products.json, so this runs once per
    product yielded by the `products` resource (piped via `|` below).
    """
    for variant in product.get("variants", []):
        yield {**variant, "product_id": product["id"]}


@dlt.source(name="shopify")
def shopify_source(
    shop_url: str = dlt.config.value,
    access_token: str = dlt.secrets.value,
    start_date: str = "2024-01-01T00:00:00Z",
):
    """Yields orders, customers, products, product_variants, locations, and
    inventory_levels from a Shopify store's Admin REST API."""

    config: RESTAPIConfig = {
        "client": {
            "base_url": f"{shop_url.rstrip('/')}/admin/api/{SHOPIFY_API_VERSION}/",
            "auth": {
                "type": "api_key",
                "name": "X-Shopify-Access-Token",
                "location": "header",
                "api_key": access_token,
            },
            # Shopify paginates via a standard RFC 5988 Link header; dlt's
            # rest_api source auto-detects this (HeaderLinkPaginator) —
            # no explicit paginator config needed.
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
            "endpoint": {
                "params": {"limit": 250},
            },
        },
        "resources": [
            {
                "name": "orders",
                "endpoint": {
                    "path": "orders.json",
                    "data_selector": "orders",
                    "params": {
                        "status": "any",
                        "updated_at_min": {
                            "type": "incremental",
                            "cursor_path": "updated_at",
                            "initial_value": start_date,
                        },
                    },
                },
            },
            {
                "name": "customers",
                "endpoint": {
                    "path": "customers.json",
                    "data_selector": "customers",
                    "params": {
                        "updated_at_min": {
                            "type": "incremental",
                            "cursor_path": "updated_at",
                            "initial_value": start_date,
                        },
                    },
                },
            },
            {
                "name": "products",
                "endpoint": {
                    "path": "products.json",
                    "data_selector": "products",
                    "params": {
                        "updated_at_min": {
                            "type": "incremental",
                            "cursor_path": "updated_at",
                            "initial_value": start_date,
                        },
                    },
                },
            },
            {
                "name": "locations",
                "write_disposition": "replace",
                "endpoint": {
                    "path": "locations.json",
                    "data_selector": "locations",
                },
            },
            {
                # One inventory_levels.json call per location, using dlt's
                # parent/child "resolve" param binding against `locations`
                # (same pattern as the posts -> comments example in dlt docs).
                "name": "inventory_levels",
                "primary_key": ["inventory_item_id", "location_id"],
                "endpoint": {
                    "path": "inventory_levels.json",
                    "data_selector": "inventory_levels",
                    "params": {
                        "location_ids": {
                            "type": "resolve",
                            "resource": "locations",
                            "field": "id",
                        },
                        "updated_at_min": {
                            "type": "incremental",
                            "cursor_path": "updated_at",
                            "initial_value": start_date,
                        },
                    },
                },
            },
        ],
    }

    resources = {r.name: r for r in rest_api_resources(config)}
    yield from resources.values()
    yield resources["products"] | product_variants
