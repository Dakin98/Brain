#!/usr/bin/env python3
"""
Klaviyo Flow Setup Automation
Erstellt Standard-Flows für neue E-Mail Marketing Kunden
"""

import json
import sys
import urllib.request
import urllib.error
import ssl

def klaviyo_api_call(api_key, endpoint, method="GET", data=None):
    """Make Klaviyo API call"""
    url = f"https://a.klaviyo.com/api/{endpoint}"
    
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": "2024-10-15",
        "Content-Type": "application/json"
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url, headers=headers, method=method)
    
    if data and method in ["POST", "PATCH", "PUT"]:
        req.data = json.dumps(data).encode()
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_data = json.loads(error_body)
            return {"error": error_data}
        except:
            return {"error": error_body}
    except Exception as e:
        return {"error": str(e)}

def get_list_id(api_key):
    """Get main newsletter list ID"""
    result = klaviyo_api_call(api_key, "lists")
    if "error" in result:
        return None
    
    lists = result.get("data", [])
    
    # Prefer "newsletter" or "Newsletter" list
    for lst in lists:
        name = lst.get("attributes", {}).get("name", "").lower()
        if "newsletter" in name:
            return lst.get("id")
    
    # Fallback to first list
    if lists:
        return lists[0].get("id")
    
    return None

def create_flow(api_key, flow_name, trigger_type="list", list_id=None):
    """Create a new flow"""
    data = {
        "data": {
            "type": "flow",
            "attributes": {
                "name": flow_name,
                "status": "draft"
            }
        }
    }
    
    result = klaviyo_api_call(api_key, "flows", "POST", data)
    return result

def setup_welcome_flow(api_key, list_id):
    """Setup Welcome Series Flow"""
    print("  🎯 Erstelle Welcome Series Flow...")
    
    flow = create_flow(api_key, "🎉 Welcome Series", "list", list_id)
    
    if "error" in flow:
        print(f"    ❌ Fehler: {flow['error']}")
        return None
    
    flow_id = flow.get("data", {}).get("id")
    print(f"    ✅ Flow erstellt: {flow_id}")
    
    return flow_id

def setup_abandoned_cart_flow(api_key):
    """Setup Abandoned Cart Flow"""
    print("  🛒 Erstelle Abandoned Cart Flow...")
    
    flow = create_flow(api_key, "🛒 Abandoned Cart")
    
    if "error" in flow:
        print(f"    ❌ Fehler: {flow['error']}")
        return None
    
    flow_id = flow.get("data", {}).get("id")
    print(f"    ✅ Flow erstellt: {flow_id}")
    
    return flow_id

def setup_browse_abandonment_flow(api_key):
    """Setup Browse Abandonment Flow"""
    print("  👁️ Erstelle Browse Abandonment Flow...")
    
    flow = create_flow(api_key, "👁️ Browse Abandonment")
    
    if "error" in flow:
        print(f"    ❌ Fehler: {flow['error']}")
        return None
    
    flow_id = flow.get("data", {}).get("id")
    print(f"    ✅ Flow erstellt: {flow_id}")
    
    return flow_id

def setup_post_purchase_flow(api_key):
    """Setup Post-Purchase Flow"""
    print("  📦 Erstelle Post-Purchase Flow...")
    
    flow = create_flow(api_key, "📦 Post-Purchase")
    
    if "error" in flow:
        print(f"    ❌ Fehler: {flow['error']}")
        return None
    
    flow_id = flow.get("data", {}).get("id")
    print(f"    ✅ Flow erstellt: {flow_id}")
    
    return flow_id

def setup_winback_flow(api_key):
    """Setup Win-Back Flow"""
    print("  🏆 Erstelle Win-Back Flow...")
    
    flow = create_flow(api_key, "🏆 Win-Back")
    
    if "error" in flow:
        print(f"    ❌ Fehler: {flow['error']}")
        return None
    
    flow_id = flow.get("data", {}).get("id")
    print(f"    ✅ Flow erstellt: {flow_id}")
    
    return flow_id

def main():
    """Main function"""
    if len(sys.argv) < 2:
        # Read from stdin
        try:
            input_data = json.load(sys.stdin)
        except:
            print(json.dumps({"error": "Invalid JSON input"}))
            sys.exit(1)
    else:
        # Read from file
        try:
            with open(sys.argv[1]) as f:
                input_data = json.load(f)
        except:
            print(json.dumps({"error": "Invalid JSON file"}))
            sys.exit(1)
    
    api_key = input_data.get("klaviyo_api_key")
    firmenname = input_data.get("firmenname", "Kunde")
    
    if not api_key:
        print(json.dumps({"error": "Missing klaviyo_api_key"}))
        sys.exit(1)
    
    print(f"\n🚀 Klaviyo Flow Setup für {firmenname}")
    print("=" * 50)
    
    # Get list ID
    print("\n📋 Schritt 1: Liste ermitteln...")
    list_id = get_list_id(api_key)
    if list_id:
        print(f"  ✅ Liste gefunden: {list_id}")
    else:
        print("  ⚠️ Keine Liste gefunden, erstelle Flows ohne List-Trigger")
    
    # Create flows
    print("\n📧 Schritt 2: Standard-Flows erstellen...")
    
    flows = {}
    
    # Welcome Flow (highest priority)
    welcome_id = setup_welcome_flow(api_key, list_id)
    if welcome_id:
        flows["welcome"] = welcome_id
    
    # Abandoned Cart
    cart_id = setup_abandoned_cart_flow(api_key)
    if cart_id:
        flows["abandoned_cart"] = cart_id
    
    # Browse Abandonment
    browse_id = setup_browse_abandonment_flow(api_key)
    if browse_id:
        flows["browse_abandonment"] = browse_id
    
    # Post-Purchase
    post_id = setup_post_purchase_flow(api_key)
    if post_id:
        flows["post_purchase"] = post_id
    
    # Win-Back
    winback_id = setup_winback_flow(api_key)
    if winback_id:
        flows["winback"] = winback_id
    
    print("\n" + "=" * 50)
    print(f"✅ Flow Setup abgeschlossen!")
    print(f"\nErstellte Flows:")
    for flow_type, flow_id in flows.items():
        print(f"  • {flow_type}: {flow_id}")
    
    # Output JSON result
    result = {
        "success": True,
        "firmenname": firmenname,
        "flows_created": len(flows),
        "flows": flows,
        "list_id": list_id
    }
    
    print(f"\n{json.dumps(result)}")
    return result

if __name__ == "__main__":
    main()
