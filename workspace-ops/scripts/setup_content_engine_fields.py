#!/usr/bin/env python3
"""
Setup ClickUp Custom Fields for Content Engine

Usage:
    python3 setup_content_engine_fields.py
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
        print(f"Error {e.code}: {e.read().decode()}")
        return None

def create_dropdown_field(list_id, name, options, required=False):
    """Create dropdown custom field"""
    data = {
        "name": name,
        "type": "drop_down",
        "required": required,
        "type_config": {
            "options": [{"name": opt, "color": "#000000"} for opt in options]
        }
    }
    return clickup_request("POST", f"/list/{list_id}/field", data)

def create_text_field(list_id, name, required=False):
    """Create text custom field"""
    data = {
        "name": name,
        "type": "text",
        "required": required
    }
    return clickup_request("POST", f"/list/{list_id}/field", data)

def create_number_field(list_id, name, required=False):
    """Create number custom field"""
    data = {
        "name": name,
        "type": "number",
        "required": required
    }
    return clickup_request("POST", f"/list/{list_id}/field", data)

def setup_content_ideas_fields():
    """Setup custom fields for Content Ideas list"""
    
    print("Setting up Content Ideas custom fields...")
    
    # Content Pillar
    result = create_dropdown_field(
        LIST_CONTENT_IDEAS,
        "Content Pillar",
        ["Meta Ads Tutorials", "Case Study", "Agency Life", "Industry Commentary"],
        required=True
    )
    if result:
        print("✅ Content Pillar field created")
    
    # Target Audience
    result = create_dropdown_field(
        LIST_CONTENT_IDEAS,
        "Target Audience",
        ["E-Com Brands", "SaaS", "Agencies", "Beginners"],
        required=False
    )
    if result:
        print("✅ Target Audience field created")
    
    # Keywords
    result = create_text_field(
        LIST_CONTENT_IDEAS,
        "Keywords",
        required=False
    )
    if result:
        print("✅ Keywords field created")
    
    # Priority Score
    result = create_number_field(
        LIST_CONTENT_IDEAS,
        "Priority Score",
        required=False
    )
    if result:
        print("✅ Priority Score field created")
    
    # Estimated Views
    result = create_number_field(
        LIST_CONTENT_IDEAS,
        "Estimated Views",
        required=False
    )
    if result:
        print("✅ Estimated Views field created")
    
    print("\n✅ Content Ideas fields setup complete!")

def get_existing_fields():
    """Get existing custom fields"""
    return clickup_request("GET", f"/list/{LIST_CONTENT_IDEAS}/field")

if __name__ == "__main__":
    print("Content Engine Field Setup")
    print("=" * 40)
    
    # Check existing fields
    existing = get_existing_fields()
    if existing:
        print(f"\nExisting fields: {len(existing.get('fields', []))}")
        for field in existing.get('fields', []):
            print(f"  - {field['name']} ({field['type']})")
    
    print("\nCreating new fields...")
    setup_content_ideas_fields()
    
    print("\n" + "=" * 40)
    print("Next steps:")
    print("1. Add 'Claude Generate' status to Content Ideas list")
    print("2. Set up n8n webhook automation")
    print("3. Test with a sample task")
