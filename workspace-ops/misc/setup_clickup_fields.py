#!/usr/bin/env python3
"""
ClickUp Custom Fields Setup Script (using urllib)
"""

import urllib.request
import urllib.error
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
CREATIVE_PIPELINE = "901521337307"

def make_request(url, data=None):
    """HTTP Request mit Bearer Token"""
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=headers, method="POST" if data else "GET")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

def create_field(list_id, name, field_type, options=None, config=None):
    """Erstellt ein Custom Field"""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/field"
    
    data = {
        "name": name,
        "type": field_type
    }
    
    if options:
        data["options"] = [{"name": opt} for opt in options]
    
    if config:
        data["type_config"] = config
    
    return make_request(url, data)

print("🚀 Starte ClickUp Custom Fields Setup...\n")

fields_to_create = [
    ("Creative Type", "drop_down", ["Static Image", "Video (UGC)", "Video (Motion)", "Carousel", "Collection", "Story"]),
    ("Hook Type", "drop_down", ["Problem-Agitate", "Social Proof", "Question", "Bold Claim", "Before/After", "Unboxing", "POV", "Testimonial", "How-To", "Trend"]),
    ("Testing Phase", "drop_down", ["Konzept", "Produktion", "Review", "Live Test", "Analyse", "Winner", "Loser"]),
    ("Format", "drop_down", ["1:1", "9:16", "16:9", "4:5", "1.91:1"]),
    ("Funnel Position", "drop_down", ["TOF", "MOF", "BOF"]),
    ("CTA", "drop_down", ["Shop Now", "Learn More", "Sign Up", "Get Offer", "Book Now"]),
    ("Ad Platform", "labels", ["Meta", "TikTok", "Google", "LinkedIn", "Pinterest"]),
    ("Figma/Canva Link", "url", None),
    ("Raw File Link", "url", None),
    ("Final Asset Link", "url", None),
    ("CTR (%)", "number", None),
    ("Hook Rate (%)", "number", None),
    ("Hold Rate (%)", "number", None),
    ("ROAS", "number", None),
    ("CPA", "number", None),
]

success_count = 0
error_count = 0

for name, field_type, options in fields_to_create:
    print(f"📋 Erstelle: {name}...")
    result = create_field(CREATIVE_PIPELINE, name, field_type, options)
    
    if "err" in result:
        print(f"   ❌ Fehler: {result['err']}")
        error_count += 1
    else:
        print(f"   ✅ Erstellt: {result.get('name', name)}")
        success_count += 1
    
    time.sleep(0.5)  # Rate limiting

print(f"\n{'='*50}")
print(f"✅ Erfolgreich: {success_count}")
print(f"❌ Fehler: {error_count}")
print(f"{'='*50}")
