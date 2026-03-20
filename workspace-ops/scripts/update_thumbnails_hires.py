#!/usr/bin/env python3
"""Update Creatives thumbnails with higher resolution"""
import subprocess, json, os, re

SHEET_ID = "1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA"
ACCOUNT_ID = "act_1538907656986107"
META_TOKEN = [l.strip().split("=",1)[1] for l in open(os.path.expanduser("~/.openclaw/workspace/.env")) if l.startswith("META_ACCESS_TOKEN=")][0]

# 1. Get hi-res thumbnails
print("Fetching hi-res thumbnails...")
thumbnails = {}

def fetch_page(url_or_none=None):
    if url_or_none:
        r = subprocess.run(["curl", "-s", url_or_none], capture_output=True, text=True)
    else:
        r = subprocess.run(["curl", "-s", "-G",
            f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/ads",
            "--data-urlencode", "fields=id,creative{thumbnail_url,image_url,object_story_spec}",
            "--data-urlencode", "limit=500",
            "--data-urlencode", f"access_token={META_TOKEN}"],
            capture_output=True, text=True)
    return json.loads(r.stdout)

data = fetch_page()
page = 1
while True:
    print(f"  Page {page} ({len(data.get('data',[]))} ads)...")
    for ad in data.get("data", []):
        c = ad.get("creative", {})
        # Priority: image_url from object_story_spec > thumbnail with higher res > thumbnail
        thumb = c.get("thumbnail_url", "")
        # Upgrade thumbnail resolution: replace p64x64 with p480x480
        if thumb and "p64x64" in thumb:
            thumb = thumb.replace("p64x64", "p480x480")
        
        spec = c.get("object_story_spec", {})
        # Try to get image_url from video_data or link_data
        for key in ["video_data", "link_data", "photo_data"]:
            if key in spec and "image_url" in spec[key]:
                hi_res = spec[key]["image_url"]
                if hi_res and not hi_res.startswith("https://www.facebook.com/ads/image"):
                    thumb = hi_res
                break
        
        thumbnails[ad["id"]] = thumb
    
    next_url = data.get("paging", {}).get("next")
    if not next_url:
        break
    data = fetch_page(next_url)
    page += 1

print(f"Found {len(thumbnails)} ads")

# 2. Read current sheet
print("Reading Creatives tab...")
result = subprocess.run(["gog", "sheets", "get", SHEET_ID, "Creatives!E:I", "--json"], capture_output=True, text=True)
rows = json.loads(result.stdout).get("values", [])

# 3. Update all rows (overwrite low-res with hi-res)
updates = []
for i, row in enumerate(rows):
    if i == 0: continue
    ad_id = row[0] if row else ""
    if ad_id in thumbnails and thumbnails[ad_id]:
        updates.append((i + 1, thumbnails[ad_id]))

print(f"Updating {len(updates)} rows with hi-res thumbnails...")
for idx, (row_num, thumb) in enumerate(updates):
    subprocess.run(["gog", "sheets", "update", SHEET_ID,
        f"Creatives!I{row_num}",
        "--values-json", json.dumps([[thumb]]),
        "--input", "USER_ENTERED"],
        capture_output=True, text=True)
    if (idx + 1) % 50 == 0:
        print(f"  {idx+1}/{len(updates)}")

print(f"✅ Done! Updated {len(updates)} thumbnails to hi-res")
