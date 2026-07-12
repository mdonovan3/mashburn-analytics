"""dlt source for the ShipHero GraphQL API.

Scaffolds the production-style ShipHero ingestion path described in
docs/production-ingestion/NOTES.md. Separate from ingestion/load_to_bigquery.py,
which loads *mock* data for local dbt development and is unaffected by this.

ShipHero's public API (developer.shiphero.com) is GraphQL, not REST, so this
does NOT use dlt's rest_api_source helper (that's REST-specific) — it's a
plain @dlt.resource generator that POSTs a GraphQL query with `requests` and
walks the cursor-based edges/pageInfo pagination pattern by hand. This is
the standard way to use dlt against a GraphQL API: a dlt resource is just a
Python generator, so any HTTP client works inside it.

IMPORTANT — field coverage caveat: the query below only requests fields
confirmed from ShipHero's public docs/examples (developer.shiphero.com).
The mock schema in ingestion/schemas.py (SHIPHERO_SHIPMENTS) also has
`delivered`, `completed`, `picked_up`, `needs_refund`, `refunded`, and
`shipping_labels.tracking_url` / `.status` — those were NOT confirmed to
exist on the real API from available docs. Check the interactive schema
browser at https://developer.shiphero.com/schema/ and add/adjust fields
before running this for real; an unrecognized field name is a hard GraphQL
error, not a silent skip.

Not yet run end-to-end — no live ShipHero account connected to this
portfolio project.
"""

import dlt
import requests

GRAPHQL_URL = "https://public-api.shiphero.com/graphql"
AUTH_REFRESH_URL = "https://public-api.shiphero.com/auth/refresh"
PAGE_SIZE = 50

# Confirmed structure: shipments(...) -> data -> edges -> node, with
# pageInfo{hasNextPage,endCursor} on `data` (see developer.shiphero.com/examples).
SHIPMENTS_QUERY = """
query Shipments($dateFrom: String, $dateTo: String, $after: String) {
  shipments(date_from: $dateFrom, date_to: $dateTo, first: %d, after: $after) {
    request_id
    complexity
    data {
      pageInfo {
        hasNextPage
        endCursor
      }
      edges {
        node {
          id
          order_id
          warehouse_id
          created_date
          shipped_off_shiphero
          dropshipment
          address {
            name
            address1
            city
            state
            country
            zip
            phone
          }
          shipping_labels {
            id
            carrier
            shipping_name
            shipping_method
            tracking_number
            cost
            created_date
          }
        }
      }
    }
  }
}
""" % PAGE_SIZE


def _get_access_token(refresh_token: str) -> str:
    """Exchanges the long-lived refresh token for a short-lived access token.

    ShipHero access tokens expire every 28 days (per developer.shiphero.com/
    getting-started); refreshing on every pipeline run avoids ever needing
    manual re-auth for a scheduled job.
    """
    resp = requests.post(
        AUTH_REFRESH_URL,
        json={"refresh_token": refresh_token},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@dlt.resource(name="shipments", primary_key="id", write_disposition="merge")
def shipments(
    refresh_token: str = dlt.secrets.value,
    updated_at=dlt.sources.incremental("created_date", initial_value="2024-01-01"),
):
    access_token = _get_access_token(refresh_token)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    after = None
    while True:
        variables = {
            "dateFrom": updated_at.last_value,
            "dateTo": None,
            "after": after,
        }
        resp = requests.post(
            GRAPHQL_URL,
            json={"query": SHIPMENTS_QUERY, "variables": variables},
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        if "errors" in payload:
            raise RuntimeError(f"ShipHero GraphQL error: {payload['errors']}")

        connection = payload["data"]["shipments"]["data"]
        nodes = [edge["node"] for edge in connection["edges"]]
        if nodes:
            yield nodes

        page_info = connection["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]


@dlt.source(name="shiphero")
def shiphero_source(refresh_token: str = dlt.secrets.value):
    yield shipments(refresh_token=refresh_token)
