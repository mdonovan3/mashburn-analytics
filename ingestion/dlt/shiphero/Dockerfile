FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shiphero_source.py shiphero_pipeline.py ./
COPY .dlt/config.toml .dlt/config.toml
# secrets.toml is never copied in — the refresh token is injected at deploy
# time as SOURCES__SHIPHERO__REFRESH_TOKEN via Secret Manager (see ../DEPLOY.md)

CMD ["python", "shiphero_pipeline.py"]
