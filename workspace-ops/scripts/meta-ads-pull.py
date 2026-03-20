#!/usr/bin/env python3
"""
Meta Ads Reporting Tool
Pulls campaign data from Meta Ads API and writes to Google Sheets
"""

import urllib.request
import urllib.parse
import json
import sys
import os
from datetime import datetime, timedelta

META_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")
BASE_URL = "https://graph.facebook.com/v18.0"

def api_call(path, params=None):
    """Make Meta API call"""
    url = f"{BASE_URL}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {META_TOKEN}")
    
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ API Error {e.code}: {error_body[:300]}", file=sys.stderr)
        return None

def get_account_info(account_id):
    """Get basic account info"""
    return api_call(f"act_{account_id}", {"fields": "name,account_status,amount_spent,currency"})

def get_campaigns(account_id, since, until):
    """Get campaigns for date range"""
    params = {
        "fields": "id,name,status,objective,daily_budget,lifetime_budget,start_time,stop_time",
        "effective_status": "['ACTIVE','PAUSED','COMPLETED']",
        "limit": 100
    }
    return api_call(f"act_{account_id}/campaigns", params)

def get_adsets(account_id, since, until):
    """Get adsets for date range"""
    params = {
        "fields": "id,name,campaign_id,targeting,budget_type,budget_amount,daily_budget,lifetime_budget",
        "limit": 100
    }
    return api_call(f"act_{account_id}/adsets", params)

def get_ads(account_id, since, until):
    """Get ads for date range"""
    params = {
        "fields": "id,name,adset_id,creative,status",
        "limit": 100
    }
    return api_call(f"act_{account_id}/ads", params)

def get_insights(account_id, since, until, breakdown=""):
    """Get performance insights"""
    params = {
        "fields": "campaign_id,adset_id,ad_id,impressions,clicks,ctr,cpc,cpm,spend,purchases,purchase_roas,actions",
        "time_range": json.dumps({"since": since, "until": until}),
        "time_increment": 1,
        "limit": 500
    }
    if breakdown:
        params["breakdown"] = breakdown
    
    return api_call(f"act_{account_id}/insights", params)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True, help="Meta Ad Account ID (without act_)")
    parser.add_argument("--since", help="Start date YYYY-MM-DD")
    parser.add_argument("--until", help="End date YYYY-MM-DD")
    parser.add_argument("--output", choices=["json", "pretty"], default="pretty")
    
    args = parser.parse_args()
    
    if not META_TOKEN:
        print("❌ META_ACCESS_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    
    # Default to last 30 days
    if not args.until:
        args.until = datetime.now().strftime("%Y-%m-%d")
    if not args.since:
        since_date = datetime.now() - timedelta(days=30)
        args.since = since_date.strftime("%Y-%m-%d")
    
    print(f"📊 Pulling data for account {args.account_id}", file=sys.stderr)
    print(f"📅 Date range: {args.since} to {args.until}", file=sys.stderr)
    
    # Get account info
    account = get_account_info(args.account_id)
    if not account:
        print("❌ Failed to get account info", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ Account: {account.get('name')}", file=sys.stderr)
    
    # Get campaigns
    campaigns = get_campaigns(args.account_id, args.since, args.until)
    print(f"📋 Found {len(campaigns.get('data', []))} campaigns", file=sys.stderr)
    
    # Get adsets
    adsets = get_adsets(args.account_id, args.since, args.until)
    print(f"🎯 Found {len(adsets.get('data', []))} adsets", file=sys.stderr)
    
    # Get ads
    ads = get_ads(args.account_id, args.since, args.until)
    print(f"📝 Found {len(ads.get('data', []))} ads", file=sys.stderr)
    
    # Get insights
    insights = get_insights(args.account_id, args.since, args.until)
    print(f"📈 Found {len(insights.get('data', []))} insight records", file=sys.stderr)
    
    # Output
    result = {
        "account": account,
        "date_range": {"since": args.since, "until": args.until},
        "campaigns": campaigns.get("data", []),
        "adsets": adsets.get("data", []),
        "ads": ads.get("data", []),
        "insights": insights.get("data", [])
    }
    
    if args.output == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        # Pretty summary
        total_spend = sum(float(i.get("spend", 0)) for i in insights.get("data", []))
        total_impressions = sum(int(i.get("impressions", 0)) for i in insights.get("data", []))
        total_clicks = sum(int(i.get("clicks", 0)) for i in insights.get("data", []))
        
        print(f"\n{'='*50}")
        print(f"SUMMARY")
        print(f"{'='*50}")
        print(f"Total Spend: €{total_spend:,.2f}")
        print(f"Total Impressions: {total_impressions:,}")
        print(f"Total Clicks: {total_clicks:,}")
        if total_impressions > 0:
            print(f"CTR: {(total_clicks/total_impressions)*100:.2f}%")
        print(f"{'='*50}")
        
        # Campaign breakdown
        print(f"\n📊 Campaign Performance:")
        for campaign in campaigns.get("data", [])[:5]:
            cid = campaign.get("id")
            campaign_insights = [i for i in insights.get("data", []) if i.get("campaign_id") == cid]
            if campaign_insights:
                c_spend = sum(float(i.get("spend", 0)) for i in campaign_insights)
                c_imp = sum(int(i.get("impressions", 0)) for i in campaign_insights)
                c_clk = sum(int(i.get("clicks", 0)) for i in campaign_insights)
                print(f"  • {campaign.get('name')[:40]:<40} | €{c_spend:>8.2f} | {c_imp:>8,} imp | {c_clk:>5,} clk")

if __name__ == "__main__":
    main()
