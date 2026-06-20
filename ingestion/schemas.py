from google.cloud.bigquery import SchemaField

# ─── Shopify ──────────────────────────────────────────────────────────────────

SHOPIFY_ORDERS = [
    SchemaField("id", "INTEGER", mode="REQUIRED"),
    SchemaField("customer_id", "INTEGER"),
    SchemaField("location_id", "INTEGER"),
    SchemaField("order_number", "INTEGER"),
    SchemaField("email", "STRING"),
    SchemaField("source_name", "STRING"),
    SchemaField("financial_status", "STRING"),
    SchemaField("fulfillment_status", "STRING"),
    SchemaField("total_price", "FLOAT"),
    SchemaField("subtotal_price", "FLOAT"),
    SchemaField("total_discounts", "FLOAT"),
    SchemaField("total_tax", "FLOAT"),
    SchemaField("currency", "STRING"),
    SchemaField("tags", "STRING"),
    SchemaField("discount_codes", "STRING"),  # JSON array as string
    SchemaField("created_at", "TIMESTAMP"),
    SchemaField("updated_at", "TIMESTAMP"),
    SchemaField("line_items", "RECORD", mode="REPEATED", fields=[
        SchemaField("id", "INTEGER"),
        SchemaField("product_id", "INTEGER"),
        SchemaField("variant_id", "INTEGER"),
        SchemaField("sku", "STRING"),
        SchemaField("title", "STRING"),
        SchemaField("variant_title", "STRING"),
        SchemaField("quantity", "INTEGER"),
        SchemaField("price", "FLOAT"),
        SchemaField("total_discount", "FLOAT"),
        SchemaField("fulfillment_status", "STRING"),
    ]),
]

SHOPIFY_CUSTOMERS = [
    SchemaField("id", "INTEGER", mode="REQUIRED"),
    SchemaField("email", "STRING"),
    SchemaField("first_name", "STRING"),
    SchemaField("last_name", "STRING"),
    SchemaField("phone", "STRING"),
    SchemaField("orders_count", "INTEGER"),
    SchemaField("total_spent", "FLOAT"),
    SchemaField("tags", "STRING"),
    SchemaField("accepts_marketing", "BOOLEAN"),
    SchemaField("created_at", "TIMESTAMP"),
    SchemaField("updated_at", "TIMESTAMP"),
    SchemaField("default_address", "RECORD", fields=[
        SchemaField("address1", "STRING"),
        SchemaField("city", "STRING"),
        SchemaField("province", "STRING"),
        SchemaField("country", "STRING"),
        SchemaField("zip", "STRING"),
    ]),
]

SHOPIFY_PRODUCTS = [
    SchemaField("id", "INTEGER", mode="REQUIRED"),
    SchemaField("title", "STRING"),
    SchemaField("product_type", "STRING"),
    SchemaField("vendor", "STRING"),
    SchemaField("tags", "STRING"),
    SchemaField("status", "STRING"),
    SchemaField("created_at", "TIMESTAMP"),
    SchemaField("updated_at", "TIMESTAMP"),
]

SHOPIFY_PRODUCT_VARIANTS = [
    SchemaField("id", "INTEGER", mode="REQUIRED"),
    SchemaField("product_id", "INTEGER"),
    SchemaField("sku", "STRING"),
    SchemaField("price", "FLOAT"),
    SchemaField("compare_at_price", "FLOAT"),
    SchemaField("inventory_quantity", "INTEGER"),
    SchemaField("option1", "STRING"),
    SchemaField("option2", "STRING"),
    SchemaField("option3", "STRING"),
    SchemaField("created_at", "TIMESTAMP"),
]

SHOPIFY_INVENTORY_LEVELS = [
    SchemaField("inventory_item_id", "INTEGER"),
    SchemaField("location_id", "INTEGER"),
    SchemaField("available", "INTEGER"),
    SchemaField("updated_at", "TIMESTAMP"),
]

SHOPIFY_LOCATIONS = [
    SchemaField("id", "INTEGER", mode="REQUIRED"),
    SchemaField("name", "STRING"),
    SchemaField("city", "STRING"),
    SchemaField("province", "STRING"),
    SchemaField("country", "STRING"),
    SchemaField("zip", "STRING"),
    SchemaField("active", "BOOLEAN"),
]

# ─── ShipHero ─────────────────────────────────────────────────────────────────

SHIPHERO_SHIPMENTS = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("order_id", "STRING"),
    SchemaField("warehouse_id", "STRING"),
    SchemaField("created_date", "TIMESTAMP"),
    SchemaField("delivered", "BOOLEAN"),
    SchemaField("completed", "BOOLEAN"),
    SchemaField("picked_up", "BOOLEAN"),
    SchemaField("needs_refund", "BOOLEAN"),
    SchemaField("refunded", "BOOLEAN"),
    SchemaField("address", "RECORD", fields=[
        SchemaField("name", "STRING"),
        SchemaField("address1", "STRING"),
        SchemaField("city", "STRING"),
        SchemaField("state", "STRING"),
        SchemaField("country", "STRING"),
        SchemaField("zip", "STRING"),
        SchemaField("phone", "STRING"),
    ]),
    SchemaField("shipping_labels", "RECORD", mode="REPEATED", fields=[
        SchemaField("id", "STRING"),
        SchemaField("carrier", "STRING"),
        SchemaField("shipping_name", "STRING"),
        SchemaField("shipping_method", "STRING"),
        SchemaField("tracking_number", "STRING"),
        SchemaField("tracking_url", "STRING"),
        SchemaField("cost", "STRING"),
        SchemaField("status", "STRING"),
        SchemaField("created_date", "TIMESTAMP"),
    ]),
]

# ─── Swym ─────────────────────────────────────────────────────────────────────

SWYM_WISHLIST_EVENTS = [
    SchemaField("_pkey", "STRING", mode="REQUIRED"),
    SchemaField("empi", "INTEGER"),      # Shopify product_id
    SchemaField("epi", "INTEGER"),       # Shopify variant_id
    SchemaField("dt", "STRING"),         # product title
    SchemaField("du", "STRING"),         # product URL
    SchemaField("iu", "STRING"),         # image URL
    SchemaField("pr", "FLOAT"),          # price
    SchemaField("sku", "STRING"),
    SchemaField("lid", "STRING"),        # list id
    SchemaField("di", "STRING"),         # device identifier
    SchemaField("bt", "STRING"),         # brand/source
    SchemaField("cts", "INTEGER"),       # created timestamp millis
    SchemaField("uts", "INTEGER"),       # updated timestamp millis
    SchemaField("_t", "STRING"),         # action type (e.g. "a" = add)
]

SWYM_WAITLIST_SIGNUPS = [
    SchemaField("empi", "INTEGER"),
    SchemaField("epi", "INTEGER"),
    SchemaField("sku", "STRING"),
    SchemaField("customer_email", "STRING"),
    SchemaField("signed_up_at", "TIMESTAMP"),
    SchemaField("notified_at", "TIMESTAMP"),
    SchemaField("purchased_at", "TIMESTAMP"),
]

# ─── Loop Returns ─────────────────────────────────────────────────────────────

LOOP_RETURN_REQUESTS = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("order_name", "STRING"),
    SchemaField("provider_order_id", "STRING"),  # Shopify order id
    SchemaField("customer_email", "STRING"),
    SchemaField("customer_first_name", "STRING"),
    SchemaField("customer_last_name", "STRING"),
    SchemaField("state", "STRING"),
    SchemaField("type", "STRING"),
    SchemaField("carrier", "STRING"),
    SchemaField("tracking_number", "STRING"),
    SchemaField("total", "FLOAT"),
    SchemaField("refund", "FLOAT"),
    SchemaField("exchange", "FLOAT"),
    SchemaField("gift_card", "FLOAT"),
    SchemaField("currency", "STRING"),
    SchemaField("label_status", "STRING"),
]

LOOP_RETURN_LINE_ITEMS = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("return_request_id", "STRING"),
    SchemaField("line_item_id", "STRING"),
    SchemaField("product_id", "INTEGER"),
    SchemaField("variant_id", "INTEGER"),
    SchemaField("sku", "STRING"),
    SchemaField("title", "STRING"),
    SchemaField("variant_title", "STRING"),
    SchemaField("price", "FLOAT"),
    SchemaField("reason", "STRING"),
    SchemaField("parent_reason", "STRING"),
    SchemaField("outcome", "STRING"),
    SchemaField("returned_at", "TIMESTAMP"),
]

# ─── Klaviyo ──────────────────────────────────────────────────────────────────

KLAVIYO_EMAIL_EVENTS = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("customer_email", "STRING"),
    SchemaField("campaign_id", "STRING"),
    SchemaField("flow_id", "STRING"),
    SchemaField("event_type", "STRING"),
    SchemaField("subject", "STRING"),
    SchemaField("created_at", "TIMESTAMP"),
]

KLAVIYO_CAMPAIGNS = [
    SchemaField("id", "STRING", mode="REQUIRED"),
    SchemaField("name", "STRING"),
    SchemaField("subject", "STRING"),
    SchemaField("status", "STRING"),
    SchemaField("sent_at", "TIMESTAMP"),
    SchemaField("list_id", "STRING"),
    SchemaField("open_rate", "FLOAT"),
    SchemaField("click_rate", "FLOAT"),
]

# ─── Schema registry ──────────────────────────────────────────────────────────

SCHEMAS = {
    "raw_shopify": {
        "orders": SHOPIFY_ORDERS,
        "customers": SHOPIFY_CUSTOMERS,
        "products": SHOPIFY_PRODUCTS,
        "product_variants": SHOPIFY_PRODUCT_VARIANTS,
        "inventory_levels": SHOPIFY_INVENTORY_LEVELS,
        "locations": SHOPIFY_LOCATIONS,
    },
    "raw_shiphero": {
        "shipments": SHIPHERO_SHIPMENTS,
    },
    "raw_swym": {
        "wishlist_events": SWYM_WISHLIST_EVENTS,
        "waitlist_signups": SWYM_WAITLIST_SIGNUPS,
    },
    "raw_loop": {
        "return_requests": LOOP_RETURN_REQUESTS,
        "return_line_items": LOOP_RETURN_LINE_ITEMS,
    },
    "raw_klaviyo": {
        "email_events": KLAVIYO_EMAIL_EVENTS,
        "campaigns": KLAVIYO_CAMPAIGNS,
    },
}
