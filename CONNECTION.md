# BigQuery Connection Info

**Project:** mashburn-analytics-dev  
**Account:** martindonovan3@gmail.com  
**Auth:** Application Default Credentials (ADC) via gcloud  

Datasets:
- `raw_shopify`
- `raw_shiphero`
- `raw_swym`
- `raw_loop`
- `raw_klaviyo`

---

## R (bigrquery)

```r
install.packages("bigrquery")
library(bigrquery)

# Auth — opens browser on first run, then caches credentials
bq_auth(email = "martindonovan3@gmail.com")

project <- "mashburn-analytics-dev"

# Example query
con <- dbConnect(
  bigrquery::bigquery(),
  project = project,
  dataset = "raw_shopify",
  billing = project
)

# Or run ad hoc SQL
results <- bq_project_query(
  project,
  "SELECT * FROM `mashburn-analytics-dev.raw_shopify.orders` LIMIT 10"
) |> bq_table_download()
```

---

## DataGrip

1. **New Data Source → Google BigQuery**
2. **Project ID:** `mashburn-analytics-dev`
3. **Authentication:** Google OAuth (recommended)  
   - Click "Sign in with Google" → authenticate with `martindonovan3@gmail.com`
   - DataGrip stores the OAuth token — no service account needed
4. **Default dataset:** leave blank or set to `raw_shopify`
5. Test connection → should show all 5 raw datasets

---

## Notes

- ADC credentials are stored at `~/.config/gcloud/application_default_credentials.json`
- To refresh: `gcloud auth application-default login`
- To refresh R auth: `bq_auth(email = "martindonovan3@gmail.com")`
- All datasets are in region **US**
