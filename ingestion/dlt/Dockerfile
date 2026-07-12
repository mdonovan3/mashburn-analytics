FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shopify_source.py shopify_pipeline.py ./
COPY .dlt/config.toml .dlt/config.toml
# secrets.toml is never copied in — the access token is injected at deploy
# time as SOURCES__SHOPIFY__ACCESS_TOKEN via Secret Manager (see DEPLOY.md)

# Cloud Run Jobs just need the container to exit 0 on success / non-zero on
# failure — no server, no exposed port.
CMD ["python", "shopify_pipeline.py"]
