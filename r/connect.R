library(bigrquery)
library(DBI)

# Authenticate — opens browser on first run, then caches
bq_auth(email = "martindonovan3@gmail.com")

project <- "mashburn-analytics-dev"

# ── Connections ───────────────────────────────────────────────────────────────

con_staging  <- dbConnect(bigrquery::bigquery(), project = project, dataset = "dbt_dev_staging", billing = project)
con_marts    <- dbConnect(bigrquery::bigquery(), project = project, dataset = "dbt_dev_marts",   billing = project)
con_shopify  <- dbConnect(bigrquery::bigquery(), project = project, dataset = "raw_shopify",      billing = project)
con_shiphero <- dbConnect(bigrquery::bigquery(), project = project, dataset = "raw_shiphero",     billing = project)
con_loop     <- dbConnect(bigrquery::bigquery(), project = project, dataset = "raw_loop",         billing = project)
con_swym     <- dbConnect(bigrquery::bigquery(), project = project, dataset = "raw_swym",         billing = project)
con_klaviyo  <- dbConnect(bigrquery::bigquery(), project = project, dataset = "raw_klaviyo",      billing = project)

# ── Raw tables ────────────────────────────────────────────────────────────────

dbGetQuery(con_shopify,  "SELECT * FROM orders LIMIT 10")
dbGetQuery(con_shopify,  "SELECT * FROM customers LIMIT 10")
dbGetQuery(con_shopify,  "SELECT * FROM products LIMIT 10")
dbGetQuery(con_shopify,  "SELECT * FROM product_variants LIMIT 10")
dbGetQuery(con_shopify,  "SELECT * FROM inventory_levels LIMIT 10")
dbGetQuery(con_shopify,  "SELECT * FROM locations LIMIT 10")

dbGetQuery(con_shiphero, "SELECT * FROM shipments LIMIT 10")

dbGetQuery(con_loop,     "SELECT * FROM return_requests LIMIT 10")
dbGetQuery(con_loop,     "SELECT * FROM return_line_items LIMIT 10")

dbGetQuery(con_swym,     "SELECT * FROM wishlist_events LIMIT 10")
dbGetQuery(con_swym,     "SELECT * FROM waitlist_signups LIMIT 10")

dbGetQuery(con_klaviyo,  "SELECT * FROM campaigns LIMIT 10")
dbGetQuery(con_klaviyo,  "SELECT * FROM email_events LIMIT 10")

# ── Staging views ─────────────────────────────────────────────────────────────

dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__orders LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__customers LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__products LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__product_variants LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__order_line_items LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__inventory_levels LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shopify__locations LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shiphero__shipments LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_shiphero__shipping_labels LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_loop__return_requests LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_loop__return_line_items LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_swym__wishlist_events LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_swym__waitlist_signups LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_klaviyo__campaigns LIMIT 10")
dbGetQuery(con_staging,  "SELECT * FROM stg_klaviyo__email_events LIMIT 10")

# ── Mart tables ───────────────────────────────────────────────────────────────

dbGetQuery(con_marts,    "SELECT * FROM customer_ltv LIMIT 10")
dbGetQuery(con_marts,    "SELECT * FROM customer_retention_cohorts LIMIT 10")
dbGetQuery(con_marts,    "SELECT * FROM product_performance LIMIT 10")
dbGetQuery(con_marts,    "SELECT * FROM return_rates_by_sku LIMIT 10")
dbGetQuery(con_marts,    "SELECT * FROM return_analysis LIMIT 10")
dbGetQuery(con_marts,    "SELECT * FROM channel_revenue_split LIMIT 10")
dbGetQuery(con_marts,    "SELECT * FROM store_performance LIMIT 10")
