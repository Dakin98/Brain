#!/bin/bash
# Klaviyo Segment Setup — Creates all standard segments for a client
# Input: JSON via stdin with fields: klaviyo_api_key, firmenname
# Output: JSON with created segment IDs

set -e

INPUT=$(cat)
API_KEY=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('klaviyo_api_key',''))")
FIRMA=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")

if [ -z "$API_KEY" ]; then
  echo '{"error": "Missing klaviyo_api_key"}' >&2
  exit 1
fi

export _KLAV_KEY="$API_KEY"
export _KLAV_FIRMA="$FIRMA"

python3 << 'PYEOF'
import urllib.request, json, sys, os

API_KEY = os.environ.get("_KLAV_KEY", "")
FIRMA = os.environ.get("_KLAV_FIRMA", "")
REVISION = "2025-01-15"
BASE = "https://a.klaviyo.com/api"

def klav(method, path, data=None):
    from urllib.parse import quote, urlsplit, urlunsplit
    raw_url = f"{BASE}/{path}"
    # URL-encode query params (spaces etc.) while keeping structure intact
    parts = urlsplit(raw_url)
    safe_url = urlunsplit((parts.scheme, parts.netloc, quote(parts.path, safe="/@:"), quote(parts.query, safe="=&',()"), parts.fragment))
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(safe_url, data=body, method=method)
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

# Step 1: Fetch ALL metrics and find IDs locally (avoids URL encoding issues with filter params)
print("🔍 Fetching all metrics...", file=sys.stderr)
metrics_resp = klav("GET", "metrics")
all_metrics = metrics_resp.get("data", []) if metrics_resp else []

# Paginate if needed
while metrics_resp and metrics_resp.get("links", {}).get("next"):
    next_url = metrics_resp["links"]["next"]
    # Extract path from full URL
    next_path = next_url.replace(BASE + "/", "") if next_url.startswith(BASE) else next_url
    metrics_resp = klav("GET", next_path)
    if metrics_resp and metrics_resp.get("data"):
        all_metrics.extend(metrics_resp["data"])

print(f"  📊 Found {len(all_metrics)} metrics total", file=sys.stderr)

placed_order_id = None
for m in all_metrics:
    name = m["attributes"]["name"].lower()
    if "placed order" in name or "ordered product" in name:
        placed_order_id = m["id"]
        print(f"  ✅ Placed Order metric: '{m['attributes']['name']}' → {placed_order_id}", file=sys.stderr)
        break
if not placed_order_id:
    print("  ⚠️ No 'Placed Order' metric found — order-based segments will be skipped", file=sys.stderr)

# Step 2: Find other metric IDs from already-fetched list
opened_email_id = None
clicked_email_id = None
active_site_id = None
refund_id = None

for m in all_metrics:
    name = m["attributes"]["name"].lower()
    if "opened email" in name and not opened_email_id:
        opened_email_id = m["id"]
    if "clicked email" in name and not clicked_email_id:
        clicked_email_id = m["id"]
    if ("active on site" in name or "viewed product" in name) and not active_site_id:
        active_site_id = m["id"]
    if "refund" in name and not refund_id:
        refund_id = m["id"]

print(f"  Metrics: order={placed_order_id} open={opened_email_id} click={clicked_email_id} site={active_site_id} refund={refund_id}", file=sys.stderr)

# ============================================================
# SEGMENT DEFINITIONS
# ============================================================

segments = []

# --- ESSENTIAL SEGMENTS ---

# Engaged 30 Days
segments.append({
    "name": "Engaged 30 Days",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 30},
         "metric_filters": None}
    ]}]} if opened_email_id else None
})

# Engaged 60 Days
segments.append({
    "name": "Engaged 60 Days",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 60},
         "metric_filters": None}
    ]}]} if opened_email_id else None
})

# Engaged 90 Days
segments.append({
    "name": "Engaged 90 Days",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 90},
         "metric_filters": None}
    ]}]} if opened_email_id else None
})

# Engaged 120 Days
segments.append({
    "name": "Engaged 120 Days",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 120},
         "metric_filters": None}
    ]}]} if opened_email_id else None
})

# Buyers - All
segments.append({
    "name": "Buyers - All",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# Repeat Buyers
segments.append({
    "name": "Repeat Buyers",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 1},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# First-time Buyers
segments.append({
    "name": "First-time Buyers",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 1},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# Active, No Purchase
segments.append({
    "name": "Active, No Purchase",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 30},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if opened_email_id and placed_order_id else None
})

# Win-Back 60 Days
segments.append({
    "name": "Win-Back 60 Days",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 60},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# Win-Back 90 Days
segments.append({
    "name": "Win-Back 90 Days",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 90},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# VIP (4+ orders alltime)
segments.append({
    "name": "VIP Customers",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-or-equal", "value": 4},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# --- EXCLUSION SEGMENTS ---

# Recent Buyers (last 7 days)
segments.append({
    "name": "⛔ Recent Buyers (7 Days)",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 7},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# Refunds
if refund_id:
    segments.append({
        "name": "⛔ Refunds",
        "condition": {"condition_groups": [{"conditions": [
            {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
             "measurement_filter": {"type": "numeric", "operator": "equals", "value": 1},
             "timeframe_filter": {"type": "date", "operator": "alltime"},
             "metric_filters": None},
            {"type": "profile-metric", "metric_id": refund_id, "measurement": "count",
             "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
             "timeframe_filter": {"type": "date", "operator": "alltime"},
             "metric_filters": None}
        ]}]}
    })

# Unengaged (received 10+ emails, opened 0 in last 90 days)
segments.append({
    "name": "⛔ Unengaged",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 90},
         "metric_filters": None}
    ]}]} if opened_email_id else None
})

# Sunset (180+ days no interaction)
segments.append({
    "name": "⛔ Sunset (180+ Days Inactive)",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 180},
         "metric_filters": None}
    ]}]} if opened_email_id else None
})

# --- ADVANCED SEGMENTS ---

# Potential VIPs
segments.append({
    "name": "🦋 Potential VIPs",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-than", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 90},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "less-than", "value": 4},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# Nearly There (engaged but no purchase)
segments.append({
    "name": "🦋 Nearly There",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-or-equal", "value": 2},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 30},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if opened_email_id and placed_order_id else None
})

# Lapsed VIPs
segments.append({
    "name": "🦋 Lapsed VIPs",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "greater-or-equal", "value": 3},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 180},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# One Hit Wonders
segments.append({
    "name": "🦋 One Hit Wonders",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 1},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 180},
         "metric_filters": None}
    ]}]} if placed_order_id else None
})

# False Starts (engaged before, not anymore, never bought)
segments.append({
    "name": "🦋 False Starts",
    "condition": {"condition_groups": [{"conditions": [
        {"type": "profile-metric", "metric_id": opened_email_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "in-the-last", "unit": "day", "quantity": 90},
         "metric_filters": None},
        {"type": "profile-metric", "metric_id": placed_order_id, "measurement": "count",
         "measurement_filter": {"type": "numeric", "operator": "equals", "value": 0},
         "timeframe_filter": {"type": "date", "operator": "alltime"},
         "metric_filters": None}
    ]}]} if opened_email_id and placed_order_id else None
})

# ============================================================
# FETCH EXISTING SEGMENTS (for idempotency)
# ============================================================
print("🔍 Fetching existing segments...", file=sys.stderr)
existing_segments = set()
seg_resp = klav("GET", "segments")
if seg_resp:
    for s in seg_resp.get("data", []):
        existing_segments.add(s["attributes"]["name"])
    # Paginate
    while seg_resp and seg_resp.get("links", {}).get("next"):
        next_url = seg_resp["links"]["next"]
        next_path = next_url.replace(BASE + "/", "") if next_url.startswith(BASE) else next_url
        seg_resp = klav("GET", next_path)
        if seg_resp:
            for s in seg_resp.get("data", []):
                existing_segments.add(s["attributes"]["name"])
print(f"  📋 {len(existing_segments)} existing segments found", file=sys.stderr)

# ============================================================
# CREATE SEGMENTS
# ============================================================

created = []
skipped = []

for seg in segments:
    if seg.get("condition") is None:
        skipped.append(seg["name"])
        continue
    
    if seg["name"] in existing_segments:
        skipped.append(seg["name"] + " (exists)")
        print(f"  ⏭️ {seg['name']} — already exists", file=sys.stderr)
        continue
    
    payload = {
        "data": {
            "type": "segment",
            "attributes": {
                "name": seg["name"],
                "definition": seg["condition"]
            }
        }
    }
    
    result = klav("POST", "segments", payload)
    if result and result.get("data"):
        sid = result["data"]["id"]
        created.append({"name": seg["name"], "id": sid})
        print(f"  ✅ {seg['name']} → {sid}", file=sys.stderr)
    else:
        skipped.append(seg["name"])
        print(f"  ❌ {seg['name']} — failed", file=sys.stderr)

print(json.dumps({
    "firma": FIRMA,
    "created": len(created),
    "skipped": len(skipped),
    "segments": created,
    "skipped_names": skipped
}))

print(f"\n🎉 {len(created)} Segmente erstellt, {len(skipped)} übersprungen für {FIRMA}", file=sys.stderr)
PYEOF