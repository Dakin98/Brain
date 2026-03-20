#!/usr/bin/env python3
"""Update Creatives tab with thumbnail URLs from Meta API"""
import subprocess, json, os

SHEET_ID = "1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA"
ACCOUNT_ID = "act_1538907656986107"
ENV_PATH = os.path.expanduser("~/.openclaw/workspace/.env")

def get_meta_token():
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("META_ACCESS_TOKEN="):
                return line.strip().split("=", 1)[1]

META_TOKEN = get_meta_token()

def curl_meta(url):
    result = subprocess.run(["curl", "-s", "-G", url,
        "--data-urlencode", f"access_token={META_TOKEN}"],
        capture_output=True, text=True)
    return json.loads(result.stdout)

def get_all_ad_thumbnails():
    thumbnails = {}
    base = f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/ads?fields=id,creative{{thumbnail_url,object_type}}&limit=500"
    url = base
    page = 0
    while url:
        page += 1
        print(f"  Page {page}...")
        if page == 1:
            result = subprocess.run(["curl", "-s", "-G",
                f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/ads",
                "--data-urlencode", "fields=id,creative{thumbnail_url,object_type}",
                "--data-urlencode", "limit=500",
                "--data-urlencode", f"access_token={META_TOKEN}"],
                capture_output=True, text=True)
            result = json.loads(result.stdout)
        else:
            r = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
            result = json.loads(r.stdout)
        
        for ad in result.get("data", []):
            creative = ad.get("creative", {})
            thumb = creative.get("thumbnail_url", "")
            obj_type = creative.get("object_type", "")
            thumbnails[ad["id"]] = {"thumbnail": thumb, "type": obj_type}
        
        url = result.get("paging", {}).get("next")
    return thumbnails

def gog_sheets_get(range_str):
    result = subprocess.run(
        ["gog", "sheets", "get", SHEET_ID, range_str, "--json"],
        capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return json.loads(result.stdout).get("values", [])

def gog_sheets_update(range_str, values):
    subprocess.run(
        ["gog", "sheets", "update", SHEET_ID, range_str,
         "--values-json", json.dumps(values), "--input", "USER_ENTERED"],
        capture_output=True, text=True)

print("Fetching ad thumbnails from Meta API...")
thumbnails = get_all_ad_thumbnails()
print(f"Found {len(thumbnails)} ads with thumbnails")

print("Reading Creatives tab...")
data = gog_sheets_get("Creatives!E:I")

batch_h = []
batch_i = []
rows_to_update = []
row_num = 1

for row in data:
    row_num += 1
    if not row or row[0] == "Ad ID":
        continue
    ad_id = row[0] if row else ""
    current_thumb = row[4] if len(row) > 4 else ""
    
    if ad_id in thumbnails and not current_thumb:
        info = thumbnails[ad_id]
        rows_to_update.append((row_num, info))

print(f"Updating {len(rows_to_update)} rows...")

# Batch update in chunks of 50
for i in range(0, len(rows_to_update), 50):
    chunk = rows_to_update[i:i+50]
    for row_num, info in chunk:
        gog_sheets_update(f"Creatives!H{row_num}:I{row_num}",
                         [[info["type"], info["thumbnail"]]])
    print(f"  Updated {min(i+50, len(rows_to_update))}/{len(rows_to_update)}")

print(f"✅ Done!")
