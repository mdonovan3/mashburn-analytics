#!/usr/bin/env python3
"""
Generate an incremental daily batch of mock data.

Usage:
    python ingestion/generate_daily.py --date 2026-06-20 --output mock_data/incremental/2026-06-20

IDs are seeded to continue from the seed data (orders 5001-5035, etc.)
"""

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ─── Reference data (must match seed) ────────────────────────────────────────

CUSTOMERS = [
    {"id": 1001, "email": "james.whitfield@gmail.com", "first_name": "James", "last_name": "Whitfield"},
    {"id": 1002, "email": "sarah.brennan@hotmail.com", "first_name": "Sarah", "last_name": "Brennan"},
    {"id": 1003, "email": "michael.torrence@gmail.com", "first_name": "Michael", "last_name": "Torrence"},
    {"id": 1004, "email": "caroline.hayes@gmail.com", "first_name": "Caroline", "last_name": "Hayes"},
    {"id": 1005, "email": "robert.lindsey@outlook.com", "first_name": "Robert", "last_name": "Lindsey"},
    {"id": 1006, "email": "anne.sterling@gmail.com", "first_name": "Anne", "last_name": "Sterling"},
    {"id": 1007, "email": "david.park@gmail.com", "first_name": "David", "last_name": "Park"},
    {"id": 1008, "email": "elizabeth.moore@gmail.com", "first_name": "Elizabeth", "last_name": "Moore"},
    {"id": 1009, "email": "thomas.greer@yahoo.com", "first_name": "Thomas", "last_name": "Greer"},
    {"id": 1010, "email": "patricia.wu@gmail.com", "first_name": "Patricia", "last_name": "Wu"},
    {"id": 1011, "email": "william.foster@gmail.com", "first_name": "William", "last_name": "Foster"},
    {"id": 1012, "email": "jennifer.cross@gmail.com", "first_name": "Jennifer", "last_name": "Cross"},
    {"id": 1013, "email": "charles.ingram@gmail.com", "first_name": "Charles", "last_name": "Ingram"},
    {"id": 1014, "email": "margaret.cole@outlook.com", "first_name": "Margaret", "last_name": "Cole"},
    {"id": 1015, "email": "henry.shaw@gmail.com", "first_name": "Henry", "last_name": "Shaw"},
    {"id": 1016, "email": "dorothy.james@gmail.com", "first_name": "Dorothy", "last_name": "James"},
    {"id": 1017, "email": "george.butler@gmail.com", "first_name": "George", "last_name": "Butler"},
    {"id": 1018, "email": "helen.price@gmail.com", "first_name": "Helen", "last_name": "Price"},
    {"id": 1019, "email": "frank.morgan@gmail.com", "first_name": "Frank", "last_name": "Morgan"},
    {"id": 1020, "email": "ruth.turner@gmail.com", "first_name": "Ruth", "last_name": "Turner"},
]

PRODUCTS = [
    {"id": 1001, "title": "The Walton Suit", "type": "Suits", "price": 1695.0, "variants": [
        {"id": 2001, "sku": "WLT-36R", "option1": "36R", "price": 1695.0},
        {"id": 2002, "sku": "WLT-38R", "option1": "38R", "price": 1695.0},
        {"id": 2003, "sku": "WLT-40R", "option1": "40R", "price": 1695.0},
        {"id": 2004, "sku": "WLT-42R", "option1": "42R", "price": 1695.0},
        {"id": 2005, "sku": "WLT-44R", "option1": "44R", "price": 1695.0},
    ]},
    {"id": 1002, "title": "The Aldrich Sport Coat", "type": "Sport Coats", "price": 1295.0, "variants": [
        {"id": 2006, "sku": "ALD-36R", "option1": "36R", "price": 1295.0},
        {"id": 2007, "sku": "ALD-38R", "option1": "38R", "price": 1295.0},
        {"id": 2008, "sku": "ALD-40R", "option1": "40R", "price": 1295.0},
        {"id": 2009, "sku": "ALD-42R", "option1": "42R", "price": 1295.0},
    ]},
    {"id": 1003, "title": "Thomas Mason Dress Shirt", "type": "Dress Shirts", "price": 195.0, "variants": [
        {"id": 2010, "sku": "TMS-S-WHT", "option1": "S", "option2": "white", "price": 195.0},
        {"id": 2011, "sku": "TMS-M-WHT", "option1": "M", "option2": "white", "price": 195.0},
        {"id": 2012, "sku": "TMS-L-WHT", "option1": "L", "option2": "white", "price": 195.0},
        {"id": 2013, "sku": "TMS-M-BLU", "option1": "M", "option2": "blue", "price": 195.0},
        {"id": 2014, "sku": "TMS-L-BLU", "option1": "L", "option2": "blue", "price": 195.0},
    ]},
    {"id": 1004, "title": "The Kennedy Trouser", "type": "Trousers", "price": 285.0, "variants": [
        {"id": 2015, "sku": "KND-30x32", "option1": "30x32", "price": 285.0},
        {"id": 2016, "sku": "KND-32x32", "option1": "32x32", "price": 285.0},
        {"id": 2017, "sku": "KND-34x32", "option1": "34x32", "price": 285.0},
        {"id": 2018, "sku": "KND-36x32", "option1": "36x32", "price": 285.0},
    ]},
    {"id": 1005, "title": "Custom Levi's 501", "type": "Denim", "price": 95.0, "variants": [
        {"id": 2019, "sku": "LEV-30", "option1": "30", "price": 95.0},
        {"id": 2020, "sku": "LEV-32", "option1": "32", "price": 95.0},
        {"id": 2021, "sku": "LEV-34", "option1": "34", "price": 95.0},
        {"id": 2022, "sku": "LEV-36", "option1": "36", "price": 95.0},
    ]},
    {"id": 1006, "title": "The Aldrich Chino", "type": "Trousers", "price": 165.0, "variants": [
        {"id": 2023, "sku": "CHN-30-KHK", "option1": "30", "option2": "khaki", "price": 165.0},
        {"id": 2024, "sku": "CHN-32-KHK", "option1": "32", "option2": "khaki", "price": 165.0},
        {"id": 2025, "sku": "CHN-32-OLV", "option1": "32", "option2": "olive", "price": 165.0},
        {"id": 2026, "sku": "CHN-34-NVY", "option1": "34", "option2": "navy", "price": 165.0},
    ]},
    {"id": 1007, "title": "Inis Meain Linen Crewneck", "type": "Knitwear", "price": 295.0, "variants": [
        {"id": 2027, "sku": "INS-S", "option1": "S", "price": 295.0},
        {"id": 2028, "sku": "INS-M", "option1": "M", "price": 295.0},
        {"id": 2029, "sku": "INS-L", "option1": "L", "price": 295.0},
        {"id": 2030, "sku": "INS-XL", "option1": "XL", "price": 295.0},
    ]},
    {"id": 1008, "title": "The Standard Polo", "type": "Polos", "price": 145.0, "variants": [
        {"id": 2031, "sku": "PLO-S-WHT", "option1": "S", "option2": "white", "price": 145.0},
        {"id": 2032, "sku": "PLO-M-NVY", "option1": "M", "option2": "navy", "price": 145.0},
        {"id": 2033, "sku": "PLO-L-GRN", "option1": "L", "option2": "green", "price": 145.0},
        {"id": 2034, "sku": "PLO-XL-NVY", "option1": "XL", "option2": "navy", "price": 145.0},
    ]},
    {"id": 1009, "title": "Canclini Oxford Shirt", "type": "Casual Shirts", "price": 165.0, "variants": [
        {"id": 2035, "sku": "CAN-S", "option1": "S", "price": 165.0},
        {"id": 2036, "sku": "CAN-M", "option1": "M", "price": 165.0},
        {"id": 2037, "sku": "CAN-L", "option1": "L", "price": 165.0},
        {"id": 2038, "sku": "CAN-XL", "option1": "XL", "price": 165.0},
    ]},
    {"id": 1010, "title": "The Standard Tee", "type": "T-Shirts", "price": 55.0, "variants": [
        {"id": 2039, "sku": "TEE-S", "option1": "S", "price": 55.0},
        {"id": 2040, "sku": "TEE-M", "option1": "M", "price": 55.0},
        {"id": 2041, "sku": "TEE-L", "option1": "L", "price": 55.0},
        {"id": 2042, "sku": "TEE-XL", "option1": "XL", "price": 55.0},
    ]},
    {"id": 1011, "title": "Madras Camp Collar Shirt", "type": "Casual Shirts", "price": 145.0, "variants": [
        {"id": 2043, "sku": "MDR-S", "option1": "S", "price": 145.0},
        {"id": 2044, "sku": "MDR-M", "option1": "M", "price": 145.0},
        {"id": 2045, "sku": "MDR-L", "option1": "L", "price": 145.0},
        {"id": 2046, "sku": "MDR-XL", "option1": "XL", "price": 145.0},
    ]},
    {"id": 1012, "title": "Sid Mashburn Silk Tie", "type": "Accessories", "price": 125.0, "variants": [
        {"id": 2047, "sku": "TIE-NVY", "option1": "navy stripe", "price": 125.0},
        {"id": 2048, "sku": "TIE-BRG", "option1": "burgundy", "price": 125.0},
        {"id": 2049, "sku": "TIE-OLV", "option1": "olive", "price": 125.0},
    ]},
    {"id": 1013, "title": "The Atlantic Brief", "type": "Accessories", "price": 395.0, "variants": [
        {"id": 2050, "sku": "ATL-OS", "option1": "one size", "price": 395.0},
    ]},
    {"id": 1014, "title": "Merino V-Neck", "type": "Knitwear", "price": 185.0, "variants": [
        {"id": 2051, "sku": "MVN-S", "option1": "S", "price": 185.0},
        {"id": 2052, "sku": "MVN-M", "option1": "M", "price": 185.0},
        {"id": 2053, "sku": "MVN-L", "option1": "L", "price": 185.0},
        {"id": 2054, "sku": "MVN-XL", "option1": "XL", "price": 185.0},
    ]},
    {"id": 1015, "title": "Ann Mashburn Cashmere Turtleneck", "type": "Knitwear", "price": 395.0, "variants": [
        {"id": 2055, "sku": "CSH-XS", "option1": "XS", "price": 395.0},
        {"id": 2056, "sku": "CSH-S", "option1": "S", "price": 395.0},
        {"id": 2057, "sku": "CSH-M", "option1": "M", "price": 395.0},
        {"id": 2058, "sku": "CSH-L", "option1": "L", "price": 395.0},
    ]},
]

LOCATIONS = [101, 102, 103, 104, 105, 106, 107, 108]
CAMPAIGNS = ["camp_1", "camp_2", "camp_3", "camp_4", "camp_5", "camp_6", "camp_7", "camp_8"]

# Seed data ends at these IDs — increment from here
SEED_ORDER_COUNT = 35
SEED_ORDER_ID_START = 5001
SEED_SHIPMENT_COUNT = 30
SEED_WISHLIST_EVENT_COUNT = 50
SEED_KLAVIYO_EVENT_COUNT = 120


def ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def rand_variant(product: dict) -> dict:
    return random.choice(product["variants"])


def generate_orders(date: datetime, batch_num: int, count: int) -> list:
    orders = []
    base_id = SEED_ORDER_ID_START + SEED_ORDER_COUNT + (batch_num * 10)
    for i in range(count):
        order_id = base_id + i
        customer = random.choice(CUSTOMERS)
        is_web = random.random() < 0.6
        location_id = None if is_web else random.choice(LOCATIONS)
        num_items = random.randint(1, 3)
        line_items = []
        subtotal = 0.0
        li_id_base = order_id * 100
        for j in range(num_items):
            product = random.choice(PRODUCTS)
            variant = rand_variant(product)
            qty = 1
            price = variant["price"]
            subtotal += price * qty
            line_items.append({
                "id": li_id_base + j,
                "product_id": product["id"],
                "variant_id": variant["id"],
                "sku": variant["sku"],
                "title": product["title"],
                "variant_title": variant.get("option1", ""),
                "quantity": qty,
                "price": str(price),
                "total_discount": "0.00",
                "fulfillment_status": "fulfilled",
            })
        tax = round(subtotal * 0.08, 2)
        order_ts = date.replace(
            hour=random.randint(9, 21),
            minute=random.randint(0, 59),
            tzinfo=timezone.utc
        )
        orders.append({
            "id": order_id,
            "customer_id": customer["id"],
            "location_id": location_id,
            "order_number": 1000 + order_id - SEED_ORDER_ID_START,
            "email": customer["email"],
            "source_name": "web" if is_web else "pos",
            "financial_status": "paid",
            "fulfillment_status": "fulfilled",
            "total_price": str(round(subtotal + tax, 2)),
            "subtotal_price": str(round(subtotal, 2)),
            "total_discounts": "0.00",
            "total_tax": str(tax),
            "currency": "USD",
            "tags": "",
            "discount_codes": "[]",
            "created_at": ts(order_ts),
            "updated_at": ts(order_ts),
            "line_items": line_items,
        })
    return orders


def generate_shipments(orders: list, date: datetime, batch_num: int) -> list:
    shipments = []
    base_id = SEED_SHIPMENT_COUNT + (batch_num * 10)
    carriers = ["UPS", "FedEx", "USPS"]
    methods = {"UPS": "GROUND", "FedEx": "GROUND", "USPS": "PRIORITY"}
    for i, order in enumerate(orders):
        carrier = random.choice(carriers)
        sh_id = f"sh_{base_id + i:03d}"
        lbl_id = f"lbl_{base_id + i:03d}"
        tracking = f"1Z{random.randint(100000000, 999999999)}"
        ship_ts = date.replace(hour=9, minute=0, tzinfo=timezone.utc) + timedelta(hours=random.randint(1, 8))
        shipments.append({
            "id": sh_id,
            "order_id": str(order["id"]),
            "warehouse_id": "wh_001",
            "created_date": ts(ship_ts),
            "delivered": True,
            "completed": True,
            "picked_up": False,
            "needs_refund": False,
            "refunded": False,
            "address": {
                "name": order["email"].split("@")[0].replace(".", " ").title(),
                "address1": "123 Main St",
                "city": "Atlanta",
                "state": "GA",
                "country": "US",
                "zip": "30301",
                "phone": "",
            },
            "shipping_labels": [{
                "id": lbl_id,
                "carrier": carrier,
                "shipping_name": f"{carrier} Ground",
                "shipping_method": methods.get(carrier, "GROUND"),
                "tracking_number": tracking,
                "tracking_url": f"https://www.ups.com/track?tracknum={tracking}",
                "cost": str(round(random.uniform(7.0, 14.0), 2)),
                "status": "delivered",
                "created_date": ts(ship_ts),
            }],
        })
    return shipments


def generate_wishlist_events(date: datetime, batch_num: int, count: int = 5) -> list:
    events = []
    base_id = SEED_WISHLIST_EVENT_COUNT + (batch_num * 10)
    for i in range(count):
        customer = random.choice(CUSTOMERS)
        product = random.choice(PRODUCTS)
        variant = rand_variant(product)
        event_ts = date.replace(
            hour=random.randint(8, 22), minute=random.randint(0, 59),
            tzinfo=timezone.utc
        )
        cts = int(event_ts.timestamp() * 1000)
        events.append({
            "_pkey": f"wl_{base_id + i:04d}",
            "empi": product["id"],
            "epi": variant["id"],
            "dt": product["title"],
            "du": f"https://sidmashburn.com/products/{product['title'].lower().replace(' ', '-')}",
            "iu": f"https://cdn.shopify.com/s/files/products/{product['id']}.jpg",
            "pr": variant["price"],
            "sku": variant["sku"],
            "lid": f"list_{customer['id']}",
            "di": f"device_{random.randint(1000, 9999)}",
            "bt": "web",
            "cts": cts,
            "uts": cts,
        })
    return events


def generate_klaviyo_events(date: datetime, batch_num: int, count: int = 10) -> list:
    events = []
    base_id = SEED_KLAVIYO_EVENT_COUNT + (batch_num * 10)
    event_types = ["sent", "opened", "clicked"]
    weights = [0.5, 0.3, 0.2]
    campaign = random.choice(CAMPAIGNS)
    for i in range(count):
        customer = random.choice(CUSTOMERS)
        event_type = random.choices(event_types, weights=weights)[0]
        event_ts = date.replace(
            hour=random.randint(8, 20), minute=random.randint(0, 59),
            tzinfo=timezone.utc
        )
        events.append({
            "id": f"kl_{base_id + i:04d}",
            "customer_email": customer["email"],
            "campaign_id": campaign,
            "flow_id": None,
            "event_type": event_type,
            "subject": "New arrivals and seasonal picks from Sid Mashburn",
            "created_at": ts(event_ts),
        })
    return events


def main():
    parser = argparse.ArgumentParser(description="Generate incremental daily mock data")
    parser.add_argument("--date", required=True, help="Date to generate data for (YYYY-MM-DD)")
    parser.add_argument("--output", required=True, help="Output directory path")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    random.seed(args.seed)
    date = datetime.strptime(args.date, "%Y-%m-%d")
    # batch_num used to avoid ID collisions across multiple incremental runs
    batch_num = (date - datetime(2026, 6, 11)).days

    output = Path(args.output)

    # Generate orders
    order_count = random.randint(2, 5)
    orders = generate_orders(date, batch_num, order_count)

    # Generate shipments for those orders
    shipments = generate_shipments(orders, date, batch_num)

    # Generate wishlist events
    wishlist_events = generate_wishlist_events(date, batch_num)

    # Generate Klaviyo events
    klaviyo_events = generate_klaviyo_events(date, batch_num)

    # Write output
    sources = {
        "shopify": {"orders": {"orders": orders}},
        "shiphero": {"shipments": {"shipments": shipments}},
        "swym": {"wishlist_events": {"events": wishlist_events}},
        "klaviyo": {"email_events": {"events": klaviyo_events}},
    }

    for source_name, tables in sources.items():
        source_dir = output / source_name
        source_dir.mkdir(parents=True, exist_ok=True)
        for table_name, data in tables.items():
            out_file = source_dir / f"{table_name}.json"
            with open(out_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  Wrote {out_file} ({len(list(data.values())[0])} records)")

    print(f"\nBatch generated: {output}")
    print(f"  {len(orders)} orders, {len(shipments)} shipments, "
          f"{len(wishlist_events)} wishlist events, {len(klaviyo_events)} klaviyo events")


if __name__ == "__main__":
    main()
