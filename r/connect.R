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

orders           <- dbGetQuery(con_shopify,  "SELECT * FROM orders LIMIT 10")
customers        <- dbGetQuery(con_shopify,  "SELECT * FROM customers LIMIT 10")
products         <- dbGetQuery(con_shopify,  "SELECT * FROM products LIMIT 10")
product_variants <- dbGetQuery(con_shopify,  "SELECT * FROM product_variants LIMIT 10")
inventory_levels <- dbGetQuery(con_shopify,  "SELECT * FROM inventory_levels LIMIT 10")
locations        <- dbGetQuery(con_shopify,  "SELECT * FROM locations LIMIT 10")

shipments        <- dbGetQuery(con_shiphero, "SELECT * FROM shipments LIMIT 10")

return_requests  <- dbGetQuery(con_loop,     "SELECT * FROM return_requests LIMIT 10")
return_line_items <- dbGetQuery(con_loop,    "SELECT * FROM return_line_items LIMIT 10")

wishlist_events  <- dbGetQuery(con_swym,     "SELECT * FROM wishlist_events LIMIT 10")
waitlist_signups <- dbGetQuery(con_swym,     "SELECT * FROM waitlist_signups LIMIT 10")

campaigns        <- dbGetQuery(con_klaviyo,  "SELECT * FROM campaigns LIMIT 10")
email_events     <- dbGetQuery(con_klaviyo,  "SELECT * FROM email_events LIMIT 10")

# ── Staging views ─────────────────────────────────────────────────────────────

stg_orders           <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__orders LIMIT 10")
stg_customers        <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__customers LIMIT 10")
stg_products         <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__products LIMIT 10")
stg_product_variants <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__product_variants LIMIT 10")
stg_order_line_items <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__order_line_items LIMIT 10")
stg_inventory_levels <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__inventory_levels LIMIT 10")
stg_locations        <- dbGetQuery(con_staging, "SELECT * FROM stg_shopify__locations LIMIT 10")
stg_shipments        <- dbGetQuery(con_staging, "SELECT * FROM stg_shiphero__shipments LIMIT 10")
stg_shipping_labels  <- dbGetQuery(con_staging, "SELECT * FROM stg_shiphero__shipping_labels LIMIT 10")
stg_return_requests  <- dbGetQuery(con_staging, "SELECT * FROM stg_loop__return_requests LIMIT 10")
stg_return_line_items <- dbGetQuery(con_staging, "SELECT * FROM stg_loop__return_line_items LIMIT 10")
stg_wishlist_events  <- dbGetQuery(con_staging, "SELECT * FROM stg_swym__wishlist_events LIMIT 10")
stg_waitlist_signups <- dbGetQuery(con_staging, "SELECT * FROM stg_swym__waitlist_signups LIMIT 10")
stg_campaigns        <- dbGetQuery(con_staging, "SELECT * FROM stg_klaviyo__campaigns LIMIT 10")
stg_email_events     <- dbGetQuery(con_staging, "SELECT * FROM stg_klaviyo__email_events LIMIT 10")

# ── Mart tables ───────────────────────────────────────────────────────────────

customer_ltv             <- dbGetQuery(con_marts, "SELECT * FROM customer_ltv LIMIT 10")
customer_retention       <- dbGetQuery(con_marts, "SELECT * FROM customer_retention_cohorts LIMIT 10")
product_performance      <- dbGetQuery(con_marts, "SELECT * FROM product_performance LIMIT 10")
return_rates_by_sku      <- dbGetQuery(con_marts, "SELECT * FROM return_rates_by_sku LIMIT 10")
return_analysis          <- dbGetQuery(con_marts, "SELECT * FROM return_analysis LIMIT 10")
channel_revenue_split    <- dbGetQuery(con_marts, "SELECT * FROM channel_revenue_split LIMIT 10")
store_performance        <- dbGetQuery(con_marts, "SELECT * FROM store_performance LIMIT 10")
