#!/usr/bin/env python3
"""
ClickUp Custom Fields für Creative Ideas & Creator Pool Listen
"""

import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
CREATIVE_IDEAS = "901521337371"
CREATOR_POOL = "901521337373"

def create_field(list_id, name, field_type, config=None):
    """Erstellt ein Custom Field"""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/field"
    
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

print("🎨 Erstelle Custom Fields für Creative Ideas...\n")

# Creative Ideas Fields
ideas_fields = [
    ("Hook Type", "drop_down", {
        "options": [
            {"name": "Problem-Agitate", "color": None},
            {"name": "Social Proof", "color": None},
            {"name": "Question", "color": None},
            {"name": "Bold Claim", "color": None},
            {"name": "Before/After", "color": None},
            {"name": "Unboxing", "color": None},
            {"name": "POV", "color": None},
            {"name": "Testimonial", "color": None},
            {"name": "How-To", "color": None},
            {"name": "Trend", "color": None}
        ]
    }),
    ("Zielgruppe", "drop_down", {
        "options": [
            {"name": "Cold", "color": None},
            {"name": "Warm", "color": None},
            {"name": "Hot", "color": None},
            {"name": "Broad", "color": None}
        ]
    }),
    ("Geschätzte Produktionszeit", "drop_down", {
        "options": [
            {"name": "< 1h", "color": None},
            {"name": "1-3h", "color": None},
            {"name": "3-8h", "color": None},
            {"name": "1-2 Tage", "color": None},
            {"name": "3+ Tage", "color": None}
        ]
    }),
    ("Priorität", "number", {"min": 1, "max": 5}),
    ("Inspiration Link", "url", None),
    ("Für Kunde", "drop_down", {
        "options": [
            {"name": "Alle Kunden", "color": None},
            {"name": "ATB Bau", "color": None},
            {"name": "Green Cola Germany", "color": None},
            {"name": "schnelleinfachgesund", "color": None},
            {"name": "Ferro Berlin", "color": None},
            {"name": "RAZECO", "color": None}
        ]
    }),
]

for name, field_type, config in ideas_fields:
    print(f"📋 Creative Ideas: {name}...")
    result = create_field(CREATIVE_IDEAS, name, field_type, config)
    print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
    time.sleep(0.5)

print("\n👤 Erstelle Custom Fields für Creator Pool...\n")

# Creator Pool Fields
creator_fields = [
    ("Typ", "drop_down", {
        "options": [
            {"name": "UGC Creator", "color": None},
            {"name": "Model", "color": None},
            {"name": "Voiceover", "color": None},
            {"name": "Motion Designer", "color": None},
            {"name": "Fotograf", "color": None}
        ]
    }),
    ("Tagessatz", "number", None),
    ("Pro Video", "number", None),
    ("Sprachen", "labels", {
        "options": [
            {"label": "Deutsch", "color": "#000000"},
            {"label": "Englisch", "color": "#000000"},
            {"label": "Französisch", "color": "#000000"},
            {"label": "Spanisch", "color": "#000000"}
        ]
    }),
    ("Nischen", "labels", {
        "options": [
            {"label": "Beauty", "color": "#000000"},
            {"label": "Fashion", "color": "#000000"},
            {"label": "Food", "color": "#000000"},
            {"label": "Tech", "color": "#000000"},
            {"label": "Fitness", "color": "#000000"},
            {"label": "Home", "color": "#000000"},
            {"label": "Finance", "color": "#000000"}
        ]
    }),
    ("Bewertung", "number", {"min": 1, "max": 5}),
    ("Verfügbarkeit", "drop_down", {
        "options": [
            {"name": "Verfügbar", "color": None},
            {"name": "Gebucht", "color": None},
            {"name": "Nicht verfügbar", "color": None},
            {"name": "Blacklisted", "color": None}
        ]
    }),
    ("Instagram", "url", None),
    ("TikTok", "url", None),
    ("Portfolio", "url", None),
    ("Kontakt E-Mail", "email", None),
    ("Letzte Zusammenarbeit", "date", None),
]

for name, field_type, config in creator_fields:
    print(f"📋 Creator Pool: {name}...")
    result = create_field(CREATOR_POOL, name, field_type, config)
    print(f"   {'✅' if 'err' not in result else '❌'} {result.get('name', result.get('err', 'Unknown'))}")
    time.sleep(0.5)

print("\n🎉 Alle Custom Fields erstellt!")
