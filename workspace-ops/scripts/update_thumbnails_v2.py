#!/usr/bin/env python3
"""Update Creatives tab with thumbnail URLs - batch version"""
import subprocess, json, os

SHEET_ID = "1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA"
ACCOUNT_ID = "act_1538907656986107"
META_TOKEN = [l.strip().split("=",1)[1] for l in open(os.path.expanduser("~/.openclaw/workspace/.env")) if l.startswith("META_ACCESS_TOKEN=")][0]

# 1. Get all ad thumbnails from Meta
print("Fetching thumbnails from Meta API...")
thumbnails = {}
page = 0
result = subprocess.run(["curl", "-s", "-G",
    f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/ads",
    "--data-urlencode", "fields=id,creative{thumbnail_url,object_type}",
    "--data-urlencode", "limit=500",
    "--data-urlencode", f"access_token={META_TOKEN}"],
    capture_output=True, text=True)
data = json.loads(result.stdout)
for ad in data.get("data", []):
    c = ad.get("creative", {})
    thumbnails[ad["id"]] = {"thumb": c.get("thumbnail_url",""), "type": c.get("object_type","")}

next_url = data.get("paging",{}).get("next")
while next_url:
    page += 1
    print(f"  Page {page+1}...")
    r = subprocess.run(["curl", "-s", next_url], capture_output=True, text=True)
    data = json.loads(r.stdout)
    for ad in data.get("data", []):
        c = ad.get("creative", {})
        thumbnails[ad["id"]] = {"thumb": c.get("thumbnail_url",""), "type": c.get("object_type","")}
    next_url = data.get("paging",{}).get("next")

print(f"Found {len(thumbnails)} ads")

# 2. Read current Creatives sheet
print("Reading Creatives tab...")
result = subprocess.run(["gog", "sheets", "get", SHEET_ID, "Creatives!E:I", "--json"], capture_output=True, text=True)
rows = json.loads(result.stdout).get("values", [])

# 3. Build batch updates
updates = []  # (row_num, type, thumb)
for i, row in enumerate(rows):
    if i == 0: continue  # header
    row_num = i + 1
    ad_id = row[0] if row else ""
    current_thumb = row[4] if len(row) > 4 else ""
    if ad_id in thumbnails and not current_thumb:
        info = thumbnails[ad_id]
        updates.append((row_num, info["type"], info["thumb"]))

print(f"Need to update {len(updates)} rows")

# 4. Batch update in chunks via gog (one call per chunk)
CHUNK = 100
for i in range(0, len(updates), CHUNK):
    chunk = updates[i:i+CHUNK]
    # Build range for this chunk - use individual updates but faster
    for row_num, obj_type, thumb in chunk:
        subprocess.run(["gog", "sheets", "update", SHEET_ID,
            f"Creatives!H{row_num}:I{row_num}",
            "--values-json", json.dumps([[obj_type, thumb]]),
            "--input", "USER_ENTERED"],
            capture_output=True, text=True)
    done = min(i + CHUNK, len(updates))
    print(f"  Updated {done}/{len(updates)}")

print("✅ Done!")
