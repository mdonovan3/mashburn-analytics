"""Entrypoint for the ShipHero dlt pipeline -> BigQuery.

Run:
    cd ingestion/dlt/shiphero
    python shiphero_pipeline.py

Requires .dlt/secrets.toml with a real ShipHero refresh token — copy
.dlt/secrets.toml.example and fill it in. See README.md.

BigQuery auth reuses this project's existing Application Default Credentials
(same as ingestion/load_to_bigquery.py, see ../../../CONNECTION.md) — no
service account key needed as long as `gcloud auth application-default
login` has already been run.
"""

import dlt
from shiphero_source import shiphero_source


def run() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="shiphero",
        destination="bigquery",
        dataset_name="raw_shiphero",
    )
    load_info = pipeline.run(shiphero_source())
    print(load_info)


if __name__ == "__main__":
    run()
