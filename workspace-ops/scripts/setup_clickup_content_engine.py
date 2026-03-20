#!/usr/bin/env python3
"""
ClickUp Content Engine Setup - Erstellt alle Custom Fields und Status
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl

CLICKUP_BASE = "https://api.clickup.com/api/v2"
LIST_CONTENT_IDEAS = "901521521000"

def get_api_token():
    config_path = os.path.expanduser("~/.config/clickup/api_token")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return f.read().strip()
    return os.environ.get("CLICKUP_API_TOKEN")

def clickup_request(method, endpoint, data=None):
    headers = {
        "Authorization": get_api_token(),
        "Content-Type": "application/json"
    }
    url = f"{CLICKUP_BASE}{endpoint}"
    req = urllib.request.Request(url, headers=headers, method=method)
    if data and method in ["POST", "PUT"]:
        req.data = json.dumps(data).encode()
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  ⚠️  Error {e.code}: {error_body[:200]}")
        return None

def get_existing_fields():
    """Get existing custom fields"""
    result = clickup_request("GET", f"/list/{LIST_CONTENT_IDEAS}/field")
    if result:
        return {f["name"]: f for f in result.get("fields", [])}
    return {}

def get_existing_statuses():
    """Get existing statuses"""
    result = clickup_request("GET", f"/list/{LIST_CONTENT_IDEAS}")
    if result:
        return [s["status"] for s in result.get("statuses", [])]
    return []

def create_dropdown_field(name, options, required=False):
    """Create dropdown field with options"""
    # Format options for ClickUp API
    formatted_options = []
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500", "#800080"]
    for i, opt in enumerate(options):
        formatted_options.append({
            "name": opt,
            "color": colors[i % len(colors)]
        })
    
    data = {
        "name": name,
        "type": "drop_down",
        "required": required,
        "type_config": {
            "options": formatted_options
        }
    }
    return clickup_request("POST", f"/list/{LIST_CONTENT_IDEAS}/field", data)

def create_text_field(name, required=False):
    """Create text field"""
    data = {
        "name": name,
        "type": "text",
        "required": required
    }
    return clickup_request("POST", f"/list/{LIST_CONTENT_IDEAS}/field", data)

def create_number_field(name, required=False):
    """Create number field"""
    data = {
        "name": name,
        "type": "number",
        "required": required
    }
    return clickup_request("POST", f"/list/{LIST_CONTENT_IDEAS}/field", data)

def add_status(status_name, color="#6F2DA8", status_type="custom"):
    """Add a new status to the list"""
    data = {
        "status": status_name,
        "color": color,
        "type": status_type
    }
    return clickup_request("POST", f"/list/{LIST_CONTENT_IDEAS}/status", data)

def setup_all():
    print("=" * 60)
    print("🎬 Content Engine Setup")
    print("=" * 60)
    
    # Check existing fields
    print("\n📋 Checking existing custom fields...")
    existing_fields = get_existing_fields()
    print(f"   Found {len(existing_fields)} existing fields")
    for name in existing_fields:
        print(f"   • {name}")
    
    # Check existing statuses
    print("\n📊 Checking existing statuses...")
    existing_statuses = get_existing_statuses()
    print(f"   Found: {', '.join(existing_statuses)}")
    
    # Setup Custom Fields
    print("\n" + "=" * 60)
    print("🔧 Setting up Custom Fields")
    print("=" * 60)
    
    # 1. Content Pillar
    if "Content Pillar" not in existing_fields:
        print("\n1️⃣ Creating 'Content Pillar' field...")
        result = create_dropdown_field(
            "Content Pillar",
            ["Meta Ads Tutorials", "Case Study", "Agency Life", "Industry Commentary"],
            required=True
        )
        if result:
            print("   ✅ Content Pillar created")
    else:
        print("\n1️⃣ Content Pillar already exists ✓")
    
    # 2. Target Audience
    if "Target Audience" not in existing_fields:
        print("\n2️⃣ Creating 'Target Audience' field...")
        result = create_dropdown_field(
            "Target Audience",
            ["E-Com Brands", "SaaS", "Agencies", "Beginners"],
            required=False
        )
        if result:
            print("   ✅ Target Audience created")
    else:
        print("\n2️⃣ Target Audience already exists ✓")
    
    # 3. Keywords
    if "Keywords" not in existing_fields:
        print("\n3️⃣ Creating 'Keywords' field...")
        result = create_text_field("Keywords", required=False)
        if result:
            print("   ✅ Keywords created")
    else:
        print("\n3️⃣ Keywords already exists ✓")
    
    # 4. Priority Score
    if "Priority Score" not in existing_fields:
        print("\n4️⃣ Creating 'Priority Score' field...")
        result = create_number_field("Priority Score", required=False)
        if result:
            print("   ✅ Priority Score created")
    else:
        print("\n4️⃣ Priority Score already exists ✓")
    
    # 5. Estimated Views
    if "Estimated Views" not in existing_fields:
        print("\n5️⃣ Creating 'Estimated Views' field...")
        result = create_number_field("Estimated Views", required=False)
        if result:
            print("   ✅ Estimated Views created")
    else:
        print("\n5️⃣ Estimated Views already exists ✓")
    
    # Setup Statuses
    print("\n" + "=" * 60)
    print("📊 Setting up Statuses")
    print("=" * 60)
    
    # 1. Claude Generate
    if "Claude Generate" not in existing_statuses:
        print("\n1️⃣ Adding 'Claude Generate' status...")
        result = add_status("Claude Generate", color="#6F2DA8", status_type="custom")
        if result:
            print("   ✅ Claude Generate status added")
        else:
            print("   ⚠️  Could not add status (may need to be done manually in ClickUp UI)")
    else:
        print("\n1️⃣ Claude Generate status already exists ✓")
    
    # 2. Content Generated
    if "Content Generated" not in existing_statuses:
        print("\n2️⃣ Adding 'Content Generated' status...")
        result = add_status("Content Generated", color="#00AA00", status_type="custom")
        if result:
            print("   ✅ Content Generated status added")
        else:
            print("   ⚠️  Could not add status (may need to be done manually in ClickUp UI)")
    else:
        print("\n2️⃣ Content Generated status already exists ✓")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("   1. Verify fields in ClickUp UI")
    print("   2. Create a test task")
    print("   3. Set status to 'Claude Generate'")
    print("   4. Wait for content generation")
    print("\n🔄 The cron job runs every 5 minutes to check for new tasks")

if __name__ == "__main__":
    try:
        setup_all()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
