#!/usr/bin/env python3
"""
Generates mock_data/seed/ JSON files for mashburn-analytics.
Reads existing shopify/{customers,products,product_variants,locations}.json
so IDs stay consistent. Writes everything else.

Run from repo root: python ingestion/generate_seed.py
"""
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).parent.parent
SEED = REPO / "mock_data" / "seed"


def load(rel):
    return json.loads((SEED / rel).read_text())


def save(rel, data):
    path = SEED / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))
    n = len(next(iter(data.values())) if isinstance(data, dict) else data)
    print(f"  wrote {path.relative_to(REPO)} ({n} records)")


def ts(date_str, hour=12, minute=0, tz_offset="-05:00"):
    return f"{date_str}T{hour:02d}:{minute:02d}:00{tz_offset}"


def tsz(date_str, hour=12, minute=0):
    return f"{date_str}T{hour:02d}:{minute:02d}:00Z"


# ─── Load existing reference data ─────────────────────────────────────────────
customers = load("shopify/customers.json")["customers"]
products_raw = load("shopify/products.json")["products"]
variants = load("shopify/product_variants.json")["product_variants"]
locations = load("shopify/locations.json")["locations"]

cust_by_id = {c["id"]: c for c in customers}
var_by_id = {v["id"]: v for v in variants}
prod_by_id = {p["id"]: p for p in products_raw}
var_by_product = {}
for v in variants:
    var_by_product.setdefault(v["product_id"], []).append(v)


# ─── Shopify orders ───────────────────────────────────────────────────────────
# Each tuple: (order_id, date, customer_id, location_id or None, [(variant_id, qty)], discount_code, tags)
# Orders 5001-5025: fulfilled; 5026-5030: unfulfilled (recent)
ORDER_SPECS = [
    (5001, "2026-05-01", 1001, None, [(2011, 1), (2024, 1)], None, ""),
    (5002, "2026-05-02", 1003, 101,  [(2003, 1)], None, ""),
    (5003, "2026-05-03", 1005, None, [(2007, 1), (2017, 1)], None, ""),
    (5004, "2026-05-04", 1007, None, [(2031, 1)], None, ""),
    (5005, "2026-05-05", 1002, 108,  [(2056, 1)], None, "ann-loves-lately"),
    (5006, "2026-05-06", 1010, None, [(2013, 1), (2040, 1)], None, ""),
    (5007, "2026-05-07", 1013, 103,  [(2002, 1), (2012, 1), (2047, 1)], None, ""),
    (5008, "2026-05-08", 1008, None, [(2044, 1)], None, "ann-loves-lately"),
    (5009, "2026-05-09", 1015, None, [(2025, 1), (2032, 1)], None, ""),
    (5010, "2026-05-10", 1018, 101,  [(2028, 1)], None, ""),
    (5011, "2026-05-11", 1001, None, [(2050, 1)], None, ""),
    (5012, "2026-05-12", 1006, None, [(2011, 1)], None, ""),
    (5013, "2026-05-13", 1017, 105,  [(2016, 1), (2014, 1)], None, ""),
    (5014, "2026-05-14", 1003, None, [(2008, 1), (2052, 1)], None, ""),
    (5015, "2026-05-15", 1004, 102,  [(2057, 1)], None, "ann-loves-lately"),
    (5016, "2026-05-16", 1009, None, [(2020, 1)], "WELCOME10", ""),
    (5017, "2026-05-17", 1011, None, [(2016, 1)], None, ""),
    (5018, "2026-05-18", 1016, 104,  [(2032, 1)], None, ""),
    (5019, "2026-05-19", 1013, None, [(2011, 1), (2037, 1), (2041, 1)], None, ""),
    (5020, "2026-05-20", 1005, None, [(2025, 1)], None, ""),
    (5021, "2026-05-21", 1003, 107,  [(2004, 1)], None, ""),
    (5022, "2026-05-22", 1012, None, [(2045, 1), (2055, 1)], None, "ann-loves-lately"),
    (5023, "2026-05-23", 1007, None, [(2006, 1), (2048, 1)], None, ""),
    (5024, "2026-05-24", 1014, 106,  [(2043, 1)], None, "ann-loves-lately"),
    (5025, "2026-05-25", 1008, None, [(2021, 1)], "SPRING20", ""),
    (5026, "2026-05-26", 1013, None, [(2017, 1), (2012, 1)], None, ""),
    (5027, "2026-05-27", 1015, 101,  [(2029, 1)], None, ""),
    (5028, "2026-05-28", 1018, None, [(2026, 1), (2040, 1)], None, ""),
    (5029, "2026-05-29", 1001, None, [(2013, 1), (2049, 1)], None, ""),
    (5030, "2026-05-30", 1005, 103,  [(2008, 1)], None, ""),
]

DISCOUNT_RATES = {"WELCOME10": 0.10, "SPRING20": 0.20}


def build_orders():
    orders = []
    for (oid, date, cid, loc_id, items, disc_code, tags) in ORDER_SPECS:
        fulfilled = oid <= 5025
        cust = cust_by_id[cid]
        hour = 10 + (oid % 8)  # spread order times across the day

        line_items = []
        subtotal = 0.0
        li_id = oid * 100
        for vid, qty in items:
            v = var_by_id[vid]
            price = v["price"]
            prod = prod_by_id[v["product_id"]]
            line_items.append({
                "id": li_id,
                "product_id": v["product_id"],
                "variant_id": vid,
                "sku": v["sku"],
                "title": prod["title"],
                "variant_title": v.get("option1", "") + (" / " + v["option2"] if v.get("option2") else ""),
                "quantity": qty,
                "price": price,
                "total_discount": 0.0,
                "fulfillment_status": "fulfilled" if fulfilled else None,
            })
            subtotal += price * qty
            li_id += 1

        disc_amount = round(subtotal * DISCOUNT_RATES.get(disc_code, 0), 2)
        for li in line_items:
            if disc_amount > 0:
                li["total_discount"] = round(li["price"] * DISCOUNT_RATES.get(disc_code, 0), 2)

        total_price = round(subtotal - disc_amount, 2)
        tax = round(total_price * 0.08, 2)

        orders.append({
            "id": oid,
            "customer_id": cid,
            "location_id": loc_id,
            "order_number": oid - 4000,
            "email": cust["email"],
            "source_name": "pos" if loc_id else "web",
            "financial_status": "paid",
            "fulfillment_status": "fulfilled" if fulfilled else None,
            "total_price": round(total_price + tax, 2),
            "subtotal_price": subtotal,
            "total_discounts": disc_amount,
            "total_tax": tax,
            "currency": "USD",
            "tags": tags,
            "discount_codes": json.dumps([{"code": disc_code, "amount": str(disc_amount), "type": "percentage"}]) if disc_code else "[]",
            "created_at": ts(date, hour=hour),
            "updated_at": ts(date, hour=hour + 1),
            "line_items": line_items,
        })
    return orders


# ─── Shopify inventory levels ─────────────────────────────────────────────────
def build_inventory_levels():
    levels = []
    loc_ids = [loc["id"] for loc in locations]
    inv_item_id = 3001  # inventory_item_id != variant_id in Shopify; we assign sequentially
    for v in variants:
        # eCommerce gets all inventory; stores get a subset
        for loc_id in loc_ids:
            qty = max(0, v["inventory_quantity"] - (3 if loc_id > 101 else 0))
            levels.append({
                "inventory_item_id": inv_item_id,
                "location_id": loc_id,
                "available": qty,
                "updated_at": tsz("2026-05-01"),
            })
        inv_item_id += 1
    return levels


# ─── ShipHero shipments ───────────────────────────────────────────────────────
CARRIERS = ["UPS", "FedEx", "USPS"]
METHODS = {
    "UPS": ("UPS Ground", "GROUND", "1Z9{n:08d}"),
    "FedEx": ("FedEx Home Delivery", "GROUND", "7489{n:012d}"),
    "USPS": ("USPS Priority Mail", "PRIORITY", "9400{n:016d}"),
}


def build_shipments(orders):
    fulfilled_orders = [o for o in orders if o["fulfillment_status"] == "fulfilled"]
    shipments = []
    for i, order in enumerate(fulfilled_orders):
        carrier = CARRIERS[i % len(CARRIERS)]
        sname, smethod, tracking_fmt = METHODS[carrier]
        tracking = tracking_fmt.format(n=5000000 + i)
        ship_date = order["created_at"][:10]
        # Ship next business day
        ship_dt = datetime.strptime(ship_date, "%Y-%m-%d") + timedelta(days=1)
        ship_date_str = ship_dt.strftime("%Y-%m-%d")
        deliver_dt = ship_dt + timedelta(days=3 if carrier != "USPS" else 2)

        cust = cust_by_id[order["customer_id"]]
        addr = cust.get("default_address", {})

        shipments.append({
            "id": f"sh_{order['id']}",
            "order_id": str(order["id"]),
            "warehouse_id": "wh_atlanta_01",
            "created_date": tsz(ship_date_str, hour=9),
            "delivered": True,
            "completed": True,
            "picked_up": False,
            "needs_refund": False,
            "refunded": False,
            "address": {
                "name": f"{cust['first_name']} {cust['last_name']}",
                "address1": addr.get("address1", ""),
                "city": addr.get("city", ""),
                "state": addr.get("province", ""),
                "country": addr.get("country", "US"),
                "zip": addr.get("zip", ""),
                "phone": cust.get("phone", ""),
            },
            "shipping_labels": [{
                "id": f"lbl_{order['id']}_01",
                "carrier": carrier,
                "shipping_name": sname,
                "shipping_method": smethod,
                "tracking_number": tracking,
                "tracking_url": f"https://www.ups.com/track?tracknum={tracking}" if carrier == "UPS"
                               else f"https://www.fedex.com/fedextrack/?tracknumbers={tracking}" if carrier == "FedEx"
                               else f"https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking}",
                "cost": f"{6.50 + (i % 5) * 1.25:.2f}",
                "status": "delivered",
                "created_date": tsz(ship_date_str, hour=9),
            }],
        })
    return shipments


# ─── Swym wishlist events ─────────────────────────────────────────────────────
# Customers who use wishlists (mix of marketing subscribers and not)
WISHLIST_CUSTOMERS = [
    (1001, "james.whitfield@gmail.com"),
    (1003, "michael.torrence@gmail.com"),
    (1004, "caroline.hayes@gmail.com"),
    (1007, "david.park@gmail.com"),
    (1008, "elizabeth.moore@gmail.com"),
    (1010, "patricia.wu@gmail.com"),
    (1012, "jennifer.cross@gmail.com"),
    (1013, "charles.ingram@gmail.com"),
    (1015, "henry.shaw@gmail.com"),
    (1018, "helen.price@gmail.com"),
]

SWYM_LIST_ID = "lst_default_wishlist"
SWYM_BASE_URL = "https://shopmashburn.com/products"

WISHLIST_SPECS = [
    # (customer_id, variant_id, date_str, action) action: a=add, r=remove
    (1001, 2007, "2026-05-01", "a"),  # James wishlists Aldrich 38R sport coat
    (1003, 2003, "2026-05-01", "a"),  # Michael: Walton 40R suit
    (1008, 2044, "2026-05-02", "a"),  # Elizabeth: Madras M
    (1007, 2006, "2026-05-02", "a"),  # David: Aldrich 36R
    (1013, 2002, "2026-05-03", "a"),  # Charles: Walton 38R
    (1004, 2057, "2026-05-03", "a"),  # Caroline: Cashmere S
    (1015, 2029, "2026-05-04", "a"),  # Henry: Linen L
    (1010, 2013, "2026-05-04", "a"),  # Patricia: TM Shirt M blue
    (1012, 2055, "2026-05-05", "a"),  # Jennifer: Cashmere XS
    (1018, 2028, "2026-05-05", "a"),  # Helen: Linen M
    (1001, 2050, "2026-05-06", "a"),  # James: Atlantic Brief
    (1008, 2021, "2026-05-07", "a"),  # Elizabeth: Denim 34
    (1003, 2008, "2026-05-08", "a"),  # Michael: Aldrich 40R sport coat
    (1013, 2017, "2026-05-08", "a"),  # Charles: Kennedy 34x32
    (1015, 2025, "2026-05-09", "a"),  # Henry: Chino 32 olive
    (1007, 2048, "2026-05-10", "a"),  # David: Tie burgundy
    (1001, 2007, "2026-05-11", "r"),  # James removes (bought it -- wait, he bought 2011 not 2007)
    (1010, 2052, "2026-05-11", "a"),  # Patricia: V-neck M
    (1012, 2045, "2026-05-12", "a"),  # Jennifer: Madras S
    (1018, 2026, "2026-05-12", "a"),  # Helen: Chino navy 34
    (1004, 2043, "2026-05-13", "a"),  # Caroline: Madras L
    (1003, 2052, "2026-05-14", "a"),  # Michael: V-neck (bought it)
    (1003, 2052, "2026-05-14", "r"),  # Michael removes after purchase
    (1008, 2044, "2026-05-15", "r"),  # Elizabeth removes Madras (bought it)
    (1008, 2021, "2026-05-26", "r"),  # Elizabeth removes denim (bought it)
    (1007, 2006, "2026-05-16", "r"),  # David removes Aldrich (bought 2006 on 5/23)
    (1013, 2002, "2026-05-17", "a"),  # Charles re-adds Walton 38R
    (1015, 2053, "2026-05-18", "a"),  # Henry: V-neck L
    (1010, 2037, "2026-05-19", "a"),  # Patricia: Canclini oxford L
    (1012, 2055, "2026-05-22", "r"),  # Jennifer removes (bought 2055 on 5/22)
    (1012, 2045, "2026-05-22", "r"),  # Jennifer removes (bought 2045 on 5/22)
    (1001, 2013, "2026-05-24", "a"),  # James: TM Shirt M blue
    (1018, 2028, "2026-05-25", "r"),  # Helen removes Linen (bought 2028 on 5/10)
    (1004, 2043, "2026-05-25", "r"),  # Caroline removes Madras (bought 2043 on 5/24)
    (1015, 2029, "2026-05-27", "r"),  # Henry removes Linen (bought 2029 on 5/27)
    (1013, 2017, "2026-05-28", "a"),  # Charles: Kennedy 34x32 (re-adds)
    (1018, 2040, "2026-05-28", "a"),  # Helen: Tee M
    (1010, 2052, "2026-05-29", "a"),  # Patricia: V-neck M (duplicate -- different device)
    (1001, 2049, "2026-05-29", "r"),  # James removes tie (bought 2049 on 5/29)
    (1007, 2048, "2026-05-30", "r"),  # David removes tie (bought 2048 on 5/23)
]


def _swym_ts(date_str, offset_hours=0):
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=14, tzinfo=timezone.utc)
    dt = dt + timedelta(hours=offset_hours)
    return int(dt.timestamp() * 1000)


def build_wishlist_events():
    events = []
    for i, (cid, vid, date, action) in enumerate(WISHLIST_SPECS):
        v = var_by_id[vid]
        prod = prod_by_id[v["product_id"]]
        cust = cust_by_id[cid]
        slug = prod["title"].lower().replace(" ", "-").replace("'", "")
        cts = _swym_ts(date, offset_hours=i % 8)
        events.append({
            "_pkey": f"swym_{cid}_{vid}_{cts}",
            "empi": v["product_id"],
            "epi": vid,
            "dt": prod["title"],
            "du": f"{SWYM_BASE_URL}/{slug}",
            "iu": f"https://cdn.shopify.com/s/files/1/0001/mashburn/{v['product_id']}_main.jpg",
            "pr": v["price"],
            "sku": v["sku"],
            "lid": SWYM_LIST_ID,
            "di": f"device_{cid}_{i % 3}",
            "bt": "shopmashburn.com",
            "customer_email": cust["email"],
            "cts": cts,
            "uts": cts + 1000,
            "_t": action,
        })
    return events


# ─── Swym waitlist signups (back-in-stock) ───────────────────────────────────
WAITLIST_SPECS = [
    # (customer_email, variant_id, signed_up, notified, purchased)
    # Out-of-stock items that customers signed up to be notified about
    ("michael.torrence@gmail.com",  2005, "2026-05-01", "2026-05-10", None),  # Walton 44R
    ("caroline.hayes@gmail.com",    2055, "2026-05-02", "2026-05-09", "2026-05-15"),  # Cashmere XS → bought
    ("helen.price@gmail.com",       2005, "2026-05-03", "2026-05-10", None),
    ("patricia.wu@gmail.com",       2033, "2026-05-04", None,         None),  # Polo L green - not yet notified
    ("henry.shaw@gmail.com",        2005, "2026-05-05", "2026-05-10", None),
    ("james.whitfield@gmail.com",   2034, "2026-05-06", None,         None),  # Polo XL navy
    ("jennifer.cross@gmail.com",    2058, "2026-05-08", "2026-05-15", None),  # Cashmere L
    ("george.butler@gmail.com",     2033, "2026-05-10", None,         None),
    ("anne.sterling@gmail.com",     2034, "2026-05-12", None,         None),
    ("elizabeth.moore@gmail.com",   2046, "2026-05-20", None,         None),  # Madras XL
]


def build_waitlist():
    rows = []
    for (email, vid, signed, notified, purchased) in WAITLIST_SPECS:
        v = var_by_id[vid]
        rows.append({
            "empi": v["product_id"],
            "epi": vid,
            "sku": v["sku"],
            "customer_email": email,
            "signed_up_at": tsz(signed),
            "notified_at": tsz(notified) if notified else None,
            "purchased_at": tsz(purchased) if purchased else None,
        })
    return rows


# ─── Loop Returns ─────────────────────────────────────────────────────────────
RETURN_SPECS = [
    # order_id, return reasons: (line_item_id_in_order, reason, parent_reason, outcome, return_outcome_type)
    # return_outcome_type: refund | exchange | credit
    {
        "return_id": "ret_001",
        "order_id": 5003,
        "reason_type": "exchange",
        "items": [(500300, 2007, "Size too large", "Fit", "default")],  # Aldrich 38R → exchange for 36R
    },
    {
        "return_id": "ret_002",
        "order_id": 5006,
        "reason_type": "refund",
        "items": [(500600, 2013, "Wrong size ordered", "Fit", "default")],  # TM Shirt M blue
    },
    {
        "return_id": "ret_003",
        "order_id": 5008,
        "reason_type": "exchange",
        "items": [(500800, 2044, "Too small", "Fit", "default")],  # Madras M → exchange L
    },
    {
        "return_id": "ret_004",
        "order_id": 5014,
        "reason_type": "exchange",
        "items": [(501400, 2008, "Size too large", "Fit", "default")],  # Aldrich 40R → exchange 38R
    },
    {
        "return_id": "ret_005",
        "order_id": 5016,
        "reason_type": "refund",
        "items": [(501600, 2020, "Fit not as expected", "Fit", "default")],  # Levi's 32
    },
    {
        "return_id": "ret_006",
        "order_id": 5019,
        "reason_type": "refund",
        "items": [(501901, 2037, "Changed mind", "Style", "default")],  # Canclini oxford
    },
]


def build_loop_returns(orders):
    order_by_id = {o["id"]: o for o in orders}
    returns = []
    for spec in RETURN_SPECS:
        order = order_by_id[spec["order_id"]]
        cust = cust_by_id[order["customer_id"]]
        otype = spec["reason_type"]
        total_val = sum(var_by_id[vid]["price"] for (_, vid, _, _, _) in spec["items"])
        returned_date = (datetime.strptime(order["created_at"][:10], "%Y-%m-%d") + timedelta(days=8)).strftime("%Y-%m-%d")

        ret = {
            "id": spec["return_id"],
            "order_name": f"#{order['order_number'] + 4000}",
            "provider_order_id": str(order["id"]),
            "customer_email": cust["email"],
            "customer_first_name": cust["first_name"],
            "customer_last_name": cust["last_name"],
            "state": "closed",
            "type": "return",
            "carrier": "UPS",
            "tracking_number": f"1ZRET{spec['return_id'][-3:].upper()}000000001",
            "total": total_val,
            "refund": total_val if otype == "refund" else 0.0,
            "exchange": total_val if otype == "exchange" else 0.0,
            "gift_card": 0.0,
            "currency": "USD",
            "label_status": "scanned",
            "line_items": [
                {
                    "id": f"{spec['return_id']}_li_{j}",
                    "return_request_id": spec["return_id"],
                    "line_item_id": str(li_id),
                    "product_id": var_by_id[vid]["product_id"],
                    "variant_id": vid,
                    "sku": var_by_id[vid]["sku"],
                    "title": prod_by_id[var_by_id[vid]["product_id"]]["title"],
                    "variant_title": var_by_id[vid].get("option1", ""),
                    "price": var_by_id[vid]["price"],
                    "reason": reason,
                    "parent_reason": parent,
                    "outcome": outcome,
                    "returned_at": tsz(returned_date),
                }
                for j, (li_id, vid, reason, parent, outcome) in enumerate(spec["items"])
            ],
        }
        returns.append(ret)
    return returns


# ─── Klaviyo campaigns ────────────────────────────────────────────────────────
CAMPAIGNS_DATA = [
    {
        "id": "camp_001",
        "name": "Spring Collection 2026",
        "subject": "Spring is here — shop the new arrivals",
        "status": "sent",
        "sent_at": tsz("2026-05-01", hour=10),
        "list_id": "list_all_subscribers",
        "open_rate": 0.28,
        "click_rate": 0.04,
    },
    {
        "id": "camp_002",
        "name": "Custom Denim Launch",
        "subject": "Custom Levi's are back — get yours before they're gone",
        "status": "sent",
        "sent_at": tsz("2026-05-08", hour=10),
        "list_id": "list_all_subscribers",
        "open_rate": 0.31,
        "click_rate": 0.06,
    },
    {
        "id": "camp_003",
        "name": "Ann Loves Lately — May Edit",
        "subject": "What Ann's been wearing this month",
        "status": "sent",
        "sent_at": tsz("2026-05-14", hour=10),
        "list_id": "list_all_subscribers",
        "open_rate": 0.33,
        "click_rate": 0.05,
    },
    {
        "id": "camp_004",
        "name": "Mother's Day Gift Guide",
        "subject": "Still looking? We've got you covered.",
        "status": "sent",
        "sent_at": tsz("2026-05-09", hour=10),
        "list_id": "list_all_subscribers",
        "open_rate": 0.25,
        "click_rate": 0.03,
    },
    {
        "id": "camp_005",
        "name": "VIP Early Access — Summer",
        "subject": "You're getting it first — summer preview inside",
        "status": "sent",
        "sent_at": tsz("2026-05-22", hour=10),
        "list_id": "list_vip",
        "open_rate": 0.45,
        "click_rate": 0.12,
    },
]

# VIP list customers
VIP_EMAILS = {
    "james.whitfield@gmail.com",
    "michael.torrence@gmail.com",
    "robert.lindsey@outlook.com",
    "elizabeth.moore@gmail.com",
    "william.foster@gmail.com",
    "charles.ingram@gmail.com",
    "david.park@gmail.com",
    "patricia.wu@gmail.com",
    "henry.shaw@gmail.com",
    "helen.price@gmail.com",
}

# (email, campaign_ids_they_open, campaign_ids_they_click)
# Built deterministically from customer patterns
EMAIL_EVENT_SPECS = [
    # subscribers with high engagement
    ("james.whitfield@gmail.com",    ["camp_001", "camp_002", "camp_003", "camp_004", "camp_005"], ["camp_002", "camp_005"]),
    ("michael.torrence@gmail.com",   ["camp_001", "camp_002", "camp_003", "camp_005"], ["camp_001", "camp_005"]),
    ("caroline.hayes@gmail.com",     ["camp_001", "camp_003", "camp_004"], ["camp_003"]),
    ("anne.sterling@gmail.com",      ["camp_001", "camp_004"], []),
    ("david.park@gmail.com",         ["camp_001", "camp_002", "camp_005"], ["camp_002", "camp_005"]),
    ("elizabeth.moore@gmail.com",    ["camp_001", "camp_003", "camp_004", "camp_005"], ["camp_003", "camp_005"]),
    ("patricia.wu@gmail.com",        ["camp_001", "camp_002", "camp_003"], ["camp_002"]),
    ("william.foster@gmail.com",     ["camp_001", "camp_005"], ["camp_005"]),
    ("jennifer.cross@gmail.com",     ["camp_003", "camp_004"], []),
    ("margaret.cole@outlook.com",    ["camp_001", "camp_003"], ["camp_003"]),
    ("henry.shaw@gmail.com",         ["camp_001", "camp_002", "camp_005"], ["camp_001"]),
    ("dorothy.james@gmail.com",      ["camp_004"], []),
    ("helen.price@gmail.com",        ["camp_001", "camp_002", "camp_003", "camp_005"], ["camp_002", "camp_005"]),
    ("frank.morgan@gmail.com",       ["camp_001"], []),
    ("ruth.turner@gmail.com",        ["camp_003", "camp_004"], ["camp_004"]),
]

# Camp subjects for reference in events
CAMP_SUBJECTS = {c["id"]: c["subject"] for c in CAMPAIGNS_DATA}
CAMP_SENT_AT = {c["id"]: c["sent_at"] for c in CAMPAIGNS_DATA}


def build_email_events():
    events = []
    ev_id = 9001
    for (email, opened_camps, clicked_camps) in EMAIL_EVENT_SPECS:
        is_vip = email in VIP_EMAILS
        camps_to_send = [c for c in CAMPAIGNS_DATA
                         if c["list_id"] == "list_all_subscribers" or (c["list_id"] == "list_vip" and is_vip)]
        for camp in camps_to_send:
            cid = camp["id"]
            sent_ts = camp["sent_at"]
            # Sent event (always)
            events.append({
                "id": f"ev_{ev_id}",
                "customer_email": email,
                "campaign_id": cid,
                "flow_id": None,
                "event_type": "sent",
                "subject": camp["subject"],
                "created_at": sent_ts,
            })
            ev_id += 1
            # Opened event
            if cid in opened_camps:
                open_ts = sent_ts[:10] + "T" + "11:30:00Z"  # ~90 min after send
                events.append({
                    "id": f"ev_{ev_id}",
                    "customer_email": email,
                    "campaign_id": cid,
                    "flow_id": None,
                    "event_type": "opened",
                    "subject": camp["subject"],
                    "created_at": open_ts,
                })
                ev_id += 1
            # Clicked event
            if cid in clicked_camps:
                click_ts = sent_ts[:10] + "T" + "11:45:00Z"
                events.append({
                    "id": f"ev_{ev_id}",
                    "customer_email": email,
                    "campaign_id": cid,
                    "flow_id": None,
                    "event_type": "clicked",
                    "subject": camp["subject"],
                    "created_at": click_ts,
                })
                ev_id += 1
    return events


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("Generating seed data...")

    orders = build_orders()
    save("shopify/orders.json", {"orders": orders})
    save("shopify/inventory_levels.json", {"inventory_levels": build_inventory_levels()})

    (SEED / "shiphero").mkdir(parents=True, exist_ok=True)
    shipments = build_shipments(orders)
    save("shiphero/shipments.json", {"shipments": shipments})

    (SEED / "swym").mkdir(parents=True, exist_ok=True)
    save("swym/wishlist_events.json", {"events": build_wishlist_events()})
    save("swym/waitlist_signups.json", {"waitlist": build_waitlist()})

    (SEED / "loop").mkdir(parents=True, exist_ok=True)
    save("loop/returns.json", {"returns": build_loop_returns(orders)})

    (SEED / "klaviyo").mkdir(parents=True, exist_ok=True)
    save("klaviyo/campaigns.json", {"campaigns": CAMPAIGNS_DATA})
    save("klaviyo/email_events.json", {"events": build_email_events()})

    print("Done.")


if __name__ == "__main__":
    main()
