#!/usr/bin/env python3
"""
ClickUp Dropdown Fields Setup - Korrektes Format
"""

import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
CREATIVE_PIPELINE = "901521337307"

def create_dropdown_field(name, options):
    """Erstellt ein Dropdown Field mit korrektem Format"""
    url = f"https://api.clickup.com/api/v2/list/{CREATIVE_PIPELINE}/field"
    
    # Format: options als Array von Objekten mit 'label' statt 'name'
    data = {
        "name": name,
        "type": "drop_down",
        "type_config": {
            "options": [{"name": opt, "color": None} for opt in options]
        }
    }
    
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

def create_label_field(name, options):
    """Erstellt ein Labels Field"""
    url = f"https://api.clickup.com/api/v2/list/{CREATIVE_PIPELINE}/field"
    
    data = {
        "name": name,
        "type": "labels",
        "type_config": {
            "options": [{"name": opt, "color": None} for opt in options]
        }
    }
    
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

print("🔄 Erstelle Dropdown & Label Fields...\n")

# Dropdown Fields
dropdowns = [
    ("Creative Type", ["Static Image", "Video (UGC)", "Video (Motion)", "Carousel", "Collection", "Story"]),
    ("Hook Type", ["Problem-Agitate", "Social Proof", "Question", "Bold Claim", "Before/After", "Unboxing", "POV", "Testimonial", "How-To", "Trend"]),
    ("Testing Phase", ["Konzept", "Produktion", "Review", "Live Test", "Analyse", "Winner", "Loser"]),
    ("Format", ["1:1", "9:16", "16:9", "4:5", "1.91:1"]),
    ("Funnel Position", ["TOF", "MOF", "BOF"]),
    ("CTA", ["Shop Now", "Learn More", "Sign Up", "Get Offer", "Book Now"]),
]

for name, options in dropdowns:
    print(f"📋 Dropdown: {name}...")
    result = create_dropdown_field(name, options)
    if "err" in result:
        print(f"   ❌ {result['err']}")
    else:
        print(f"   ✅ {result.get('name', name)}")
    time.sleep(0.5)

# Label Fields
print("\n📋 Labels: Ad Platform...")
result = create_label_field("Ad Platform", ["Meta", "TikTok", "Google", "LinkedIn", "Pinterest"])
if "err" in result:
    print(f"   ❌ {result['err']}")
else:
    print(f"   ✅ {result.get('name', 'Ad Platform')}")

print("\n✅ Dropdown-Setup abgeschlossen!")
