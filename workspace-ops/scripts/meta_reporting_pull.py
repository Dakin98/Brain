#!/usr/bin/env python3
"""
Meta Ads Reporting → Google Sheets (Razeco UG)
Pulls only missing months. Appends to existing data.
"""

import subprocess, json, sys, os
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# Config
SHEET_ID = "1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA"
ACCOUNT_ID = "act_1538907656986107"
ACCOUNT_NAME = "Razeco UG"
ENV_PATH = os.path.expanduser("~/.openclaw/workspace/.env")

def get_meta_token():
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("META_ACCESS_TOKEN="):
                return line.strip().split("=", 1)[1]
    raise ValueError("META_ACCESS_TOKEN not found in .env")

META_TOKEN = get_meta_token()

def gog_sheets_get(range_str):
    """Get data from Google Sheet via gog CLI"""
    result = subprocess.run(
        ["gog", "sheets", "get", SHEET_ID, range_str, "--json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout)
        return data.get("values", [])
    except:
        return []

def gog_sheets_append(tab, values):
    """Append rows to Google Sheet via gog CLI"""
    if not values:
        return
    result = subprocess.run(
        ["gog", "sheets", "append", SHEET_ID, f"{tab}!A:Z",
         "--values-json", json.dumps(values),
         "--insert", "INSERT_ROWS",
         "--input", "USER_ENTERED"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR appending to {tab}: {result.stderr}")
    else:
        print(f"  ✅ Appended {len(values)} rows to {tab}")

def get_existing_months(tab):
    """Get set of months already in the sheet"""
    data = gog_sheets_get(f"{tab}!A:A")
    months = set()
    for row in data:
        if row and row[0] and row[0] != "Monat":
            months.add(row[0])
    return months

def meta_api_get(level, fields, since, until):
    """Pull insights from Meta API with pagination"""
    all_data = []
    params = urlencode({
        "level": level,
        "fields": fields,
        "time_range": json.dumps({"since": since, "until": until}),
        "limit": "500",
        "filtering": json.dumps([{"field": "spend", "operator": "GREATER_THAN", "value": "0"}]),
        "access_token": META_TOKEN
    })
    url = f"https://graph.facebook.com/v21.0/{ACCOUNT_ID}/insights?{params}"
    
    while url:
        req = Request(url)
        resp = urlopen(req)
        result = json.loads(resp.read())
        all_data.extend(result.get("data", []))
        url = result.get("paging", {}).get("next")
    
    return all_data

def extract_action(actions, action_types):
    """Extract value from Meta actions array"""
    if not actions:
        return 0
    for at in action_types:
        for a in actions:
            if a.get("action_type") == at:
                return a.get("value", 0)
    return 0

def get_months_to_pull():
    """Determine which months need pulling"""
    # Get existing months from all 3 tabs
    existing_campaigns = get_existing_months("Campaigns")
    existing_adsets = get_existing_months("Ad Sets")
    existing_creatives = get_existing_months("Creatives")
    
    # Use campaigns tab as reference (if it has data, we assume all tabs have it)
    existing = existing_campaigns
    
    # Generate all months from 2024-01 to last complete month
    now = datetime.now()
    if now.day < 5:
        # If we're in first 5 days, last complete month is 2 months ago
        end = now.replace(day=1) - timedelta(days=1)
    else:
        end = now.replace(day=1) - timedelta(days=1)
    
    months = []
    current = datetime(2024, 1, 1)
    while current <= end:
        month_str = current.strftime("%Y-%m")
        if month_str not in existing:
            last_day = (current.replace(month=current.month % 12 + 1, day=1) - timedelta(days=1)).day if current.month < 12 else 31
            months.append({
                "label": month_str,
                "since": current.strftime("%Y-%m-01"),
                "until": current.strftime(f"%Y-%m-{last_day:02d}")
            })
        current = (current.replace(day=28) + timedelta(days=5)).replace(day=1)
    
    return months

def transform_campaigns(data, month_label):
    rows = []
    for r in data:
        spend = float(r.get("spend", 0))
        conversions = extract_action(r.get("actions"), ["offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"])
        cost_per_conv = extract_action(r.get("cost_per_action_type"), ["offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"])
        revenue = extract_action(r.get("action_values"), ["offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"])
        revenue = float(revenue) if revenue else 0
        roas = round(revenue / spend, 2) if spend > 0 else 0
        
        rows.append([
            month_label,
            ACCOUNT_NAME,
            r.get("campaign_id", ""),
            r.get("campaign_name", ""),
            r.get("objective", ""),
            spend,
            int(r.get("impressions", 0)),
            int(r.get("reach", 0)),
            round(float(r.get("frequency", 0)), 2),
            int(r.get("clicks", 0)),
            round(float(r.get("ctr", 0)), 2),
            round(float(r.get("cpm", 0)), 2),
            int(conversions) if conversions else 0,
            round(float(cost_per_conv), 2) if cost_per_conv else 0,
            roas
        ])
    return rows

def transform_adsets(data, month_label):
    rows = []
    for r in data:
        conversions = extract_action(r.get("actions"), ["offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"])
        cost_per_conv = extract_action(r.get("cost_per_action_type"), ["offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"])
        
        rows.append([
            month_label,
            ACCOUNT_NAME,
            r.get("campaign_id", ""),
            r.get("campaign_name", ""),
            r.get("adset_id", ""),
            r.get("adset_name", ""),
            r.get("objective", ""),
            "",  # Targeting (API doesn't return this in insights)
            "",  # Budget
            float(r.get("spend", 0)),
            int(r.get("impressions", 0)),
            int(r.get("reach", 0)),
            round(float(r.get("frequency", 0)), 2),
            int(r.get("clicks", 0)),
            round(float(r.get("ctr", 0)), 2),
            round(float(r.get("cpm", 0)), 2),
            int(conversions) if conversions else 0,
            round(float(cost_per_conv), 2) if cost_per_conv else 0
        ])
    return rows

def transform_ads(data, month_label):
    rows = []
    for r in data:
        impressions = int(r.get("impressions", 0))
        video_plays = extract_action(r.get("video_play_actions"), ["video_view"])
        video_plays = int(video_plays) if video_plays else 0
        thruplay = extract_action(r.get("video_p100_watched_actions"), ["video_view"])
        thruplay = int(thruplay) if thruplay else 0
        
        hook_rate = round((video_plays / impressions) * 100, 1) if impressions > 0 and video_plays > 0 else ""
        hold_rate = round((thruplay / video_plays) * 100, 1) if video_plays > 0 and thruplay > 0 else ""
        
        rows.append([
            month_label,
            ACCOUNT_NAME,
            r.get("campaign_name", ""),
            r.get("adset_name", ""),
            r.get("ad_id", ""),
            r.get("ad_name", ""),
            r.get("objective", ""),
            "",  # Creative Type
            "",  # Thumbnail URL
            "",  # Landing Page URL
            float(r.get("spend", 0)),
            impressions,
            int(r.get("clicks", 0)),
            round(float(r.get("ctr", 0)), 2),
            round(float(r.get("cpc", 0)), 2) if r.get("cpc") else 0,
            round(float(r.get("cpm", 0)), 2),
            video_plays,
            thruplay,
            hook_rate,
            hold_rate
        ])
    return rows

def main():
    print("🧠 Meta Ads Reporting Pull")
    print(f"Account: {ACCOUNT_NAME} ({ACCOUNT_ID})")
    print("")
    
    months = get_months_to_pull()
    
    if not months:
        print("✅ Alles aktuell — keine fehlenden Monate!")
        return
    
    print(f"📅 {len(months)} Monate zu ziehen: {', '.join(m['label'] for m in months)}")
    print("")
    
    for m in months:
        print(f"--- {m['label']} ---")
        
        # Campaign level
        print(f"  Pulling campaigns...")
        camp_data = meta_api_get("campaign", 
            "campaign_id,campaign_name,objective,spend,impressions,reach,frequency,clicks,ctr,cpm,actions,action_values,cost_per_action_type",
            m["since"], m["until"])
        camp_rows = transform_campaigns(camp_data, m["label"])
        gog_sheets_append("Campaigns", camp_rows)
        
        # Ad Set level
        print(f"  Pulling ad sets...")
        adset_data = meta_api_get("adset",
            "campaign_id,campaign_name,adset_id,adset_name,objective,spend,impressions,reach,frequency,clicks,ctr,cpm,actions,cost_per_action_type",
            m["since"], m["until"])
        adset_rows = transform_adsets(adset_data, m["label"])
        gog_sheets_append("Ad Sets", adset_rows)
        
        # Ad/Creative level
        print(f"  Pulling creatives...")
        ad_data = meta_api_get("ad",
            "campaign_name,adset_name,ad_id,ad_name,objective,spend,impressions,clicks,ctr,cpc,cpm,actions,cost_per_action_type,video_30_sec_watched_actions,video_p75_watched_actions,video_p100_watched_actions,video_play_actions",
            m["since"], m["until"])
        ad_rows = transform_ads(ad_data, m["label"])
        gog_sheets_append("Creatives", ad_rows)
        
        print("")
    
    print("🎉 Fertig!")

if __name__ == "__main__":
    main()
