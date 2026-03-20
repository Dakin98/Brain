#!/usr/bin/env python3
"""
Check platform access for a client.
Input: JSON via stdin with platform IDs
Output: JSON with access status per platform
"""

import urllib.request, json, sys, os, subprocess

input_data = json.load(sys.stdin)
results = {}

# === META ADS CHECK ===
meta_ad_account = input_data.get("meta_ad_account_id", "")
if meta_ad_account:
    # Try to access the ad account via Meta API
    meta_token = os.environ.get("META_ACCESS_TOKEN", "")
    if meta_token:
        try:
            aid = meta_ad_account if meta_ad_account.startswith("act_") else f"act_{meta_ad_account}"
            req = urllib.request.Request(f"https://graph.facebook.com/v21.0/{aid}?fields=name,account_status&access_token={meta_token}")
            resp = json.load(urllib.request.urlopen(req))
            results["meta"] = {"ok": True, "name": resp.get("name"), "status": resp.get("account_status")}
            print(f"  ✅ Meta Ads: {resp.get('name')} (Status: {resp.get('account_status')})", file=sys.stderr)
        except Exception as e:
            results["meta"] = {"ok": False, "error": str(e)[:200]}
            print(f"  ❌ Meta Ads: {e}", file=sys.stderr)
    else:
        results["meta"] = {"ok": False, "error": "No META_ACCESS_TOKEN"}
        print(f"  ⏭️ Meta Ads: No access token configured", file=sys.stderr)

# === GOOGLE ADS CHECK ===
google_ads_cid = input_data.get("google_ads_cid", "")
if google_ads_cid:
    # Google Ads API requires OAuth — simplified check via gog CLI
    results["google_ads"] = {"ok": False, "error": "Manual check required", "cid": google_ads_cid}
    print(f"  ℹ️ Google Ads: CID {google_ads_cid} — manueller Check nötig", file=sys.stderr)

# === GA4 CHECK ===
ga4_property = input_data.get("ga4_property_id", "")
if ga4_property:
    try:
        # Use Google Analytics skill via Maton gateway
        maton_key = os.environ.get("MATON_API_KEY", "")
        if maton_key:
            req = urllib.request.Request(
                f"https://gateway.maton.ai/google-analytics/v1beta/properties/{ga4_property}",
            )
            req.add_header("Authorization", f"Bearer {maton_key}")
            resp = json.load(urllib.request.urlopen(req))
            results["ga4"] = {"ok": True, "name": resp.get("displayName"), "property": ga4_property}
            print(f"  ✅ GA4: {resp.get('displayName')} ({ga4_property})", file=sys.stderr)
        else:
            results["ga4"] = {"ok": False, "error": "No MATON_API_KEY"}
    except Exception as e:
        results["ga4"] = {"ok": False, "error": str(e)[:200], "property": ga4_property}
        print(f"  ❌ GA4: {e}", file=sys.stderr)

# === GTM CHECK ===
gtm_container = input_data.get("gtm_container_id", "")
if gtm_container:
    results["gtm"] = {"ok": False, "error": "Manual check required", "container": gtm_container}
    print(f"  ℹ️ GTM: {gtm_container} — manueller Check nötig", file=sys.stderr)

# === SHOPIFY CHECK ===
shopify_url = input_data.get("shopify_shop_url", "")
shopify_token = input_data.get("shopify_access_token", "")
if shopify_url and shopify_token:
    try:
        shop = shopify_url.replace("https://", "").replace("http://", "").rstrip("/")
        req = urllib.request.Request(f"https://{shop}/admin/api/2024-01/shop.json")
        req.add_header("X-Shopify-Access-Token", shopify_token)
        resp = json.load(urllib.request.urlopen(req))
        shop_name = resp.get("shop", {}).get("name", "?")
        results["shopify"] = {"ok": True, "name": shop_name, "shop": shop}
        print(f"  ✅ Shopify: {shop_name} ({shop})", file=sys.stderr)
    except Exception as e:
        results["shopify"] = {"ok": False, "error": str(e)[:200]}
        print(f"  ❌ Shopify: {e}", file=sys.stderr)

# === KLAVIYO CHECK ===
klaviyo_key = input_data.get("klaviyo_api_key", "")
if klaviyo_key:
    try:
        req = urllib.request.Request("https://a.klaviyo.com/api/accounts")
        req.add_header("Authorization", f"Klaviyo-API-Key {klaviyo_key}")
        req.add_header("revision", "2024-10-15")
        resp = json.load(urllib.request.urlopen(req))
        acct = resp.get("data", [{}])[0].get("attributes", {})
        results["klaviyo"] = {"ok": True, "name": acct.get("contact_information", {}).get("organization_name", "?")}
        print(f"  ✅ Klaviyo: {results['klaviyo']['name']}", file=sys.stderr)
    except Exception as e:
        results["klaviyo"] = {"ok": False, "error": str(e)[:200]}
        print(f"  ❌ Klaviyo: {e}", file=sys.stderr)

print(json.dumps(results))
