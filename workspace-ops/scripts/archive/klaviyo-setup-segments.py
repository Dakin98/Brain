#!/usr/bin/env python3
"""
Klaviyo Segment Setup — Creates all standard segments for a client.
Input: JSON via stdin with fields: klaviyo_api_key, firmenname
Output: JSON with created segment IDs
"""

import urllib.request, urllib.parse, json, sys, time

input_data = json.load(sys.stdin)
API_KEY = input_data.get("klaviyo_api_key", "")
FIRMA = input_data.get("firmenname", "")
REVISION = "2024-10-15"
BASE = "https://a.klaviyo.com/api"

if not API_KEY:
    print(json.dumps({"error": "Missing klaviyo_api_key"}))
    sys.exit(1)

def klav(method, path, data=None):
    url = f"{BASE}/{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Klaviyo-API-Key {API_KEY}")
    req.add_header("revision", REVISION)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read()
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ❌ API Error {e.code}: {body[:200]}", file=sys.stderr)
        return None

# Step 1: Get all metrics
print("🔍 Fetching metrics...", file=sys.stderr)
metrics_resp = klav("GET", "metrics")
all_metrics = metrics_resp.get("data", []) if metrics_resp else []

placed_order_id = None
opened_email_id = None
clicked_email_id = None
active_site_id = None
refund_id = None

for m in all_metrics:
    name = m["attributes"]["name"].lower()
    mid = m["id"]
    if "placed order" in name and not placed_order_id:
        placed_order_id = mid
    elif "opened email" in name and not opened_email_id:
        opened_email_id = mid
    elif "clicked email" in name and not clicked_email_id:
        clicked_email_id = mid
    elif ("active on site" in name or "viewed product" in name) and not active_site_id:
        active_site_id = mid
    elif "refund" in name and not refund_id:
        refund_id = mid

print(f"  Metrics: order={placed_order_id} open={opened_email_id} click={clicked_email_id} refund={refund_id}", file=sys.stderr)

has_orders = placed_order_id is not None
has_email = opened_email_id is not None
print(f"  Orders: {'✅' if has_orders else '❌ (Shopify not connected yet)'}", file=sys.stderr)
print(f"  Email: {'✅' if has_email else '❌'}", file=sys.stderr)

# Segment definitions
segments = []

def metric_cond(metric_id, op, val, timeframe_op, **tf_kwargs):
    """Helper to create a metric condition."""
    tf = {"type": "date", "operator": timeframe_op}
    if "unit" in tf_kwargs:
        tf["unit"] = tf_kwargs["unit"]
    if "quantity" in tf_kwargs:
        tf["quantity"] = tf_kwargs["quantity"]
    return {
        "type": "profile-metric",
        "metric_id": metric_id,
        "measurement": "count",
        "measurement_filter": {"type": "numeric", "operator": op, "value": val},
        "timeframe_filter": tf,
        "metric_filters": None
    }

# ==================== ESSENTIAL ====================

if opened_email_id:
    for days in [30, 60, 90, 120]:
        segments.append({
            "name": f"Engaged {days} Days",
            "conditions": [metric_cond(opened_email_id, "greater-than", 0, "in-the-last", unit="day", quantity=days)]
        })

if placed_order_id:
    segments.append({
        "name": "Buyers - All",
        "conditions": [metric_cond(placed_order_id, "greater-than", 0, "alltime")]
    })
    segments.append({
        "name": "Repeat Buyers",
        "conditions": [metric_cond(placed_order_id, "greater-than", 1, "alltime")]
    })
    segments.append({
        "name": "First-time Buyers",
        "conditions": [metric_cond(placed_order_id, "equals", 1, "alltime")]
    })

if opened_email_id and placed_order_id:
    segments.append({
        "name": "Active, No Purchase",
        "conditions": [
            metric_cond(opened_email_id, "greater-than", 0, "in-the-last", unit="day", quantity=30),
            metric_cond(placed_order_id, "equals", 0, "alltime")
        ]
    })

if placed_order_id:
    for days in [60, 90, 120]:
        segments.append({
            "name": f"Win-Back {days} Days",
            "conditions": [
                metric_cond(placed_order_id, "greater-than", 0, "alltime"),
                metric_cond(placed_order_id, "equals", 0, "in-the-last", unit="day", quantity=days)
            ]
        })
    segments.append({
        "name": "VIP Customers",
        "conditions": [metric_cond(placed_order_id, "greater-or-equal", 4, "alltime")]
    })

# ==================== EXCLUSION ====================

if placed_order_id:
    segments.append({
        "name": "⛔ Recent Buyers (7 Days)",
        "conditions": [metric_cond(placed_order_id, "greater-than", 0, "in-the-last", unit="day", quantity=7)]
    })

if placed_order_id and refund_id:
    segments.append({
        "name": "⛔ Refunds",
        "conditions": [
            metric_cond(placed_order_id, "equals", 1, "alltime"),
            metric_cond(refund_id, "greater-than", 0, "alltime")
        ]
    })

if opened_email_id:
    segments.append({
        "name": "⛔ Unengaged (90 Days)",
        "conditions": [metric_cond(opened_email_id, "equals", 0, "in-the-last", unit="day", quantity=90)]
    })
    segments.append({
        "name": "⛔ Sunset (180+ Days)",
        "conditions": [metric_cond(opened_email_id, "equals", 0, "in-the-last", unit="day", quantity=180)]
    })

# ==================== ADVANCED ====================

if placed_order_id:
    segments.append({
        "name": "🦋 Potential VIPs",
        "conditions": [
            metric_cond(placed_order_id, "greater-than", 0, "in-the-last", unit="day", quantity=90),
            metric_cond(placed_order_id, "less-than", 4, "alltime")
        ]
    })

if opened_email_id and placed_order_id:
    segments.append({
        "name": "🦋 Nearly There",
        "conditions": [
            metric_cond(opened_email_id, "greater-or-equal", 2, "in-the-last", unit="day", quantity=30),
            metric_cond(placed_order_id, "equals", 0, "alltime")
        ]
    })

if placed_order_id:
    segments.append({
        "name": "🦋 Lapsed VIPs",
        "conditions": [
            metric_cond(placed_order_id, "greater-or-equal", 3, "alltime"),
            metric_cond(placed_order_id, "equals", 0, "in-the-last", unit="day", quantity=180)
        ]
    })
    segments.append({
        "name": "🦋 One Hit Wonders",
        "conditions": [
            metric_cond(placed_order_id, "equals", 1, "alltime"),
            metric_cond(placed_order_id, "equals", 0, "in-the-last", unit="day", quantity=180)
        ]
    })

if opened_email_id and placed_order_id:
    segments.append({
        "name": "🦋 False Starts",
        "conditions": [
            metric_cond(opened_email_id, "equals", 0, "in-the-last", unit="day", quantity=90),
            metric_cond(placed_order_id, "equals", 0, "alltime")
        ]
    })

# ==================== CHECK EXISTING ====================

print("🔍 Checking existing segments...", file=sys.stderr)
time.sleep(1.5)
existing_resp = klav("GET", "segments?fields[segment]=name")
existing_names = set()
if existing_resp and existing_resp.get("data"):
    for s in existing_resp["data"]:
        existing_names.add(s["attributes"]["name"])
    # Handle pagination
    while existing_resp.get("links", {}).get("next"):
        time.sleep(1.5)
        next_url = existing_resp["links"]["next"].replace("https://a.klaviyo.com/api/", "")
        existing_resp = klav("GET", next_url)
        if existing_resp and existing_resp.get("data"):
            for s in existing_resp["data"]:
                existing_names.add(s["attributes"]["name"])

print(f"  {len(existing_names)} existing segments found", file=sys.stderr)

# ==================== CREATE ====================

created = []
skipped_existing = []
failed = []

for seg in segments:
    if seg["name"] in existing_names:
        skipped_existing.append(seg["name"])
        print(f"  ⏭️ {seg['name']} (exists)", file=sys.stderr)
        continue
    payload = {
        "data": {
            "type": "segment",
            "attributes": {
                "name": seg["name"],
                "definition": {
                    "condition_groups": [{
                        "conditions": seg["conditions"]
                    }]
                }
            }
        }
    }

    time.sleep(1.5)  # Klaviyo rate limit: ~1 req/sec
    result = klav("POST", "segments", payload)
    if result and result.get("data"):
        sid = result["data"]["id"]
        created.append({"name": seg["name"], "id": sid})
        print(f"  ✅ {seg['name']} → {sid}", file=sys.stderr)
    else:
        # Retry once after rate limit
        time.sleep(3)
        result = klav("POST", "segments", payload)
        if result and result.get("data"):
            sid = result["data"]["id"]
            created.append({"name": seg["name"], "id": sid})
            print(f"  ✅ {seg['name']} → {sid} (retry)", file=sys.stderr)
        else:
            failed.append(seg["name"])
            print(f"  ❌ {seg['name']}", file=sys.stderr)

needs_orders = not has_orders
total_possible = len(segments) + (14 if needs_orders else 0)  # 14 order-based segments missing

print(f"\n🎉 {FIRMA}: {len(created)} erstellt, {len(skipped_existing)} existierten schon, {len(failed)} fehlgeschlagen", file=sys.stderr)
if needs_orders:
    print(f"  ⏳ 14 weitere Segmente warten auf Shopify/Order-Integration", file=sys.stderr)

all_done = not needs_orders and len(failed) == 0

print(json.dumps({
    "firma": FIRMA,
    "created": len(created),
    "skipped_existing": len(skipped_existing),
    "failed": len(failed),
    "segments": created,
    "failed_names": failed,
    "all_done": all_done,
    "needs_orders": needs_orders
}))
