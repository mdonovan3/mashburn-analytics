#!/bin/bash
# mashburn-analytics project setup
# Ubuntu 24.04 — run once on a new machine
# After this script completes, follow the manual steps printed at the end.

set -e

echo "=== 1. Install Google Cloud CLI ==="
sudo apt-get install -y apt-transport-https ca-certificates gnupg curl

curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
  | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
  | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list

sudo apt-get update && sudo apt-get install -y google-cloud-cli

echo ""
echo "=== 2. Install Python dependencies ==="
pip install google-cloud-bigquery --break-system-packages

echo ""
echo "=== 3. Verify installs ==="
gcloud --version
python3 -c "from google.cloud import bigquery; print('google-cloud-bigquery OK')"

echo ""
echo "================================================================"
echo "  Setup complete. Now run these steps MANUALLY in order:"
echo "================================================================"
echo ""
echo "  1. Authenticate your Google account:"
echo "     gcloud auth login"
echo ""
echo "  2. Set your GCP project:"
echo "     gcloud config set project mashburn-analytics-dev"
echo ""
echo "  3. Set up application default credentials (used by Python):"
echo "     gcloud auth application-default login"
echo ""
echo "  4. Test the BigQuery connection:"
echo "     python3 ingestion/load_to_bigquery.py \\"
echo "       --batch mock_data/seed \\"
echo "       --project mashburn-analytics-dev"
echo "================================================================"
