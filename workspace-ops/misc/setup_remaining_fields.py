#!/usr/bin/env python3
"""
ClickUp Custom Fields - Restliche Felder für Creative Pipeline
"""

import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
CREATIVE_PIPELINE = "901521337307"

def create_field(name, field_type, config=None):
    """Erstellt ein Custom Field"""
    url = f"https://api.clickup.com/api/v2/list/{CREATIVE_PIPELINE}/field"
    
    data = {
        "name": name,
        "type": field_type
    }
    
    if config:
        data["type_config"] = config
    
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

print("🔄 Erstelle restliche Creative Pipeline Felder...\n")

# 1. Ad Platform Labels (mit korrektem Format)
print("📋 Labels: Ad Platform...")
result = create_field("Ad Platform", "labels", {
    "options": [
        {"label": "Meta", "color": "#000000"},
        {"label": "TikTok", "color": "#000000"},
        {"label": "Google", "color": "#000000"},
        {"label": "LinkedIn", "color": "#000000"},
        {"label": "Pinterest", "color": "#000000"}
    ]
})
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 2. Test Start (Date)
print("📋 Date: Test Start...")
result = create_field("Test Start", "date")
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 3. Spend im Test (Currency)
print("📋 Currency: Spend im Test...")
result = create_field("Spend im Test", "money", {
    "currency_type": "EUR"
})
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 4. Notizen / Learnings (Long Text)
print("📋 Text: Notizen / Learnings...")
result = create_field("Notizen / Learnings", "text", {
    "is_multiline": True
})
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 5. Angle / Message (Short Text)
print("📋 Text: Angle / Message...")
result = create_field("Angle / Message", "text")
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 6. Iterations (Number)
print("📋 Number: Iterations...")
result = create_field("Iterations", "number")
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 7. Language (Dropdown)
print("📋 Dropdown: Language...")
result = create_field("Language", "drop_down", {
    "options": [
        {"name": "Deutsch", "color": None},
        {"name": "Englisch", "color": None},
        {"name": "Multilingual", "color": None}
    ]
})
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
time.sleep(0.5)

# 8. Performance Score (Rating 1-5)
print("📋 Rating: Performance Score...")
result = create_field("Performance Score", "emoji", {
    "code_point": "⭐",
    "count": 5
})
print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")

print("\n✅ Alle restlichen Felder erstellt!")
