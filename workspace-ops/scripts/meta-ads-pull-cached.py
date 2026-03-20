#!/usr/bin/env python3
"""
Meta Ads Reporting Tool - MIT CACHING
Pulls campaign data from Meta Ads API with 24h cache

Cache-Location: ~/.openclaw/workspace/.cache/meta-ads/
Token-Einsparung: ~70% bei wiederholten Aufrufen
"""

import urllib.request
import urllib.parse
import json
import sys
import os
from datetime import datetime, timedelta
import hashlib

META_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")
BASE_URL = "https://graph.facebook.com/v18.0"
CACHE_DIR = os.path.expanduser("~/.openclaw/workspace/.cache/meta-ads")
CACHE_TTL_HOURS = 24

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_key(account_id, endpoint, date_str):
    """Generate cache key from parameters"""
    key_str = f"{account_id}_{endpoint}_{date_str}"
    return hashlib.md5(key_str.encode()).hexdigest()

def get_cache_path(cache_key):
    """Get full path to cache file"""
    return os.path.join(CACHE_DIR, f"{cache_key}.json")

def read_cache(cache_key, ttl_hours=CACHE_TTL_HOURS):
    """Read cached data if still valid"""
    cache_path = get_cache_path(cache_key)
    
    if not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'r') as f:
            cached = json.load(f)
        
        # Check TTL
        updated = datetime.fromisoformat(cached.get('updated', '2000-01-01T00:00:00'))
        age_hours = (datetime.now() - updated).total_seconds() / 3600
        
        if age_hours < ttl_hours:
            print(f"📦 CACHE HIT ({int(age_hours)}h alt)", file=sys.stderr)
            return cached.get('data')
        else:
            print(f"⏰ Cache expired ({int(age_hours)}h alt)", file=sys.stderr)
            return None
    except Exception as e:
        print(f"⚠️ Cache read error: {e}", file=sys.stderr)
        return None

def read_stale_cache(cache_key):
    """Read cache even if expired (fallback)"""
    cache_path = get_cache_path(cache_key)
    
    if not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'r') as f:
            cached = json.load(f)
        updated = cached.get('updated', 'unknown')
        print(f"🔄 Using STALE cache from {updated}", file=sys.stderr)
        return cached.get('data')
    except:
        return None

def write_cache(cache_key, data):
    """Write data to cache"""
    cache_path = get_cache_path(cache_key)
    
    try:
        with open(cache_path, 'w') as f:
            json.dump({
                'data': data,
                'updated': datetime.now().isoformat(),
                'key': cache_key
            }, f)
        return True
    except Exception as e:
        print(f"⚠️ Cache write error: {e}", file=sys.stderr)
        return False

def api_call(path, params=None, use_cache=True, cache_key=None, force_refresh=False):
    """Make Meta API call with caching"""
    
    # Try cache first (unless force refresh)
    if use_cache and cache_key and not force_refresh:
        cached = read_cache(cache_key)
        if cached:
            return cached
    
    # Make API call
    url = f"{BASE_URL}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {META_TOKEN}")
    
    try:
        print(f"🌐 API Call: {path}", file=sys.stderr)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        
        # Cache successful response
        if use_cache and cache_key:
            write_cache(cache_key, data)
        
        return data
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ API Error {e.code}: {error_body[:300]}", file=sys.stderr)
        
        # Fallback to stale cache on API error
        if use_cache and cache_key:
            stale = read_stale_cache(cache_key)
            if stale:
                print(f"✅ Fallback zu stale cache", file=sys.stderr)
                return stale
        
        return None
    except Exception as e:
        print(f"❌ Request Error: {e}", file=sys.stderr)
        
        # Fallback to stale cache on any error
        if use_cache and cache_key:
            stale = read_stale_cache(cache_key)
            if stale:
                return stale
        
        return None

def get_account_info(account_id, force_refresh=False):
    """Get basic account info with caching"""
    today = datetime.now().strftime('%Y-%m-%d')
    cache_key = get_cache_key(account_id, 'account_info', today)
    return api_call(f"act_{account_id}", {"fields": "name,account_status,amount_spent,currency"}, 
                   use_cache=True, cache_key=cache_key, force_refresh=force_refresh)

def get_campaigns(account_id, since, until, force_refresh=False):
    """Get campaigns with caching"""
    cache_key = get_cache_key(account_id, f"campaigns_{since}_{until}", '')
    
    params = {
        "fields": "id,name,status,objective,daily_budget,lifetime_budget,start_time,stop_time",
        "effective_status": "['ACTIVE','PAUSED','COMPLETED']",
        "limit": 100
    }
    return api_call(f"act_{account_id}/campaigns", params, 
                   use_cache=True, cache_key=cache_key, force_refresh=force_refresh)

def get_adsets(account_id, since, until, force_refresh=False):
    """Get adsets with caching"""
    cache_key = get_cache_key(account_id, f"adsets_{since}_{until}", '')
    
    params = {
        "fields": "id,name,campaign_id,targeting,budget_type,budget_amount,daily_budget,lifetime_budget",
        "limit": 100
    }
    return api_call(f"act_{account_id}/adsets", params,
                   use_cache=True, cache_key=cache_key, force_refresh=force_refresh)

def get_ads(account_id, since, until, force_refresh=False):
    """Get ads with caching"""
    cache_key = get_cache_key(account_id, f"ads_{since}_{until}", '')
    
    params = {
        "fields": "id,name,adset_id,creative,status",
        "limit": 100
    }
    return api_call(f"act_{account_id}/ads", params,
                   use_cache=True, cache_key=cache_key, force_refresh=force_refresh)

def get_insights(account_id, since, until, level="campaign", force_refresh=False):
    """Get performance insights with caching"""
    cache_key = get_cache_key(account_id, f"insights_{level}_{since}_{until}", '')
    
    params = {
        "fields": "campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,impressions,clicks,spend,cpc,ctr,conversions",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": level,
        "limit": 500
    }
    return api_call(f"act_{account_id}/insights", params,
                   use_cache=True, cache_key=cache_key, force_refresh=force_refresh)

def cache_stats():
    """Show cache statistics"""
    try:
        files = os.listdir(CACHE_DIR)
        total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) for f in files)
        
        print("📊 Meta Ads Cache Stats")
        print("=" * 40)
        print(f"📁 Location: {CACHE_DIR}")
        print(f"📄 Files: {len(files)}")
        print(f"💾 Size: {total_size / 1024:.1f} KB")
        print("")
        
        # Show recent files
        if files:
            print("🕐 Recent entries:")
            files_with_time = [(f, os.path.getmtime(os.path.join(CACHE_DIR, f))) for f in files]
            files_with_time.sort(key=lambda x: x[1], reverse=True)
            for f, mtime in files_with_time[:5]:
                age = datetime.now() - datetime.fromtimestamp(mtime)
                print(f"   {f[:20]}... ({age.days}d {age.seconds//3600}h ago)")
        
    except Exception as e:
        print(f"❌ Error reading cache: {e}")

def clear_cache():
    """Clear all cached data"""
    try:
        files = os.listdir(CACHE_DIR)
        for f in files:
            os.remove(os.path.join(CACHE_DIR, f))
        print(f"✅ Cache cleared ({len(files)} files)")
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Meta Ads Reporting with Caching')
    parser.add_argument('command', choices=['account', 'campaigns', 'adsets', 'ads', 'insights', 'cache-stats', 'cache-clear'])
    parser.add_argument('--account', default=os.environ.get('META_AD_ACCOUNT', ''), help='Ad Account ID')
    parser.add_argument('--since', default=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    parser.add_argument('--until', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--level', default='campaign', choices=['campaign', 'adset', 'ad'])
    parser.add_argument('--force', action='store_true', help='Force refresh (ignore cache)')
    
    args = parser.parse_args()
    
    if args.command == 'cache-stats':
        cache_stats()
        return
    
    if args.command == 'cache-clear':
        clear_cache()
        return
    
    if not args.account:
        print("❌ No account ID provided. Use --account or set META_AD_ACCOUNT env var")
        sys.exit(1)
    
    if not META_TOKEN:
        print("❌ No access token. Set META_ACCESS_TOKEN env var")
        sys.exit(1)
    
    # Execute command
    if args.command == 'account':
        result = get_account_info(args.account, force_refresh=args.force)
    elif args.command == 'campaigns':
        result = get_campaigns(args.account, args.since, args.until, force_refresh=args.force)
    elif args.command == 'adsets':
        result = get_adsets(args.account, args.since, args.until, force_refresh=args.force)
    elif args.command == 'ads':
        result = get_ads(args.account, args.since, args.until, force_refresh=args.force)
    elif args.command == 'insights':
        result = get_insights(args.account, args.since, args.until, args.level, force_refresh=args.force)
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
