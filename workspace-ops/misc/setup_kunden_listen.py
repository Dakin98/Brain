#!/usr/bin/env python3
"""
ClickUp: Pro Kunde eigene Creative Testing Listen erstellen
"""
import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"

# Kunden-Folder IDs
KUNDEN = {
    "ATB Bau": "901514522366",
    "Green Cola Germany": "901514522387",
    "schnelleinfachgesund": "901514522393",
    "Ferro Berlin": "901514522399",
    "RAZECO": "901514522405"
}

# Listen pro Kunde
LISTEN = [
    ("💡 Creative Ideas", "Sammlung aller Kreativ-Ideen, Hooks und Angles"),
    ("📝 Creative Pipeline", "Aktive Produktion: Von Briefing bis Live Test"),
    ("📦 Creative Archive", "Abgeschlossene Creatives: Winner & Loser"),
    ("📚 Creative Learnings", "Was hat funktioniert? Insights und Erkenntnisse"),
    ("👤 Creator Pool", "UGC Creators, Models, Voiceover für diesen Kunden")
]

def create_list(folder_id, name, content=""):
    """Erstellt eine Liste im Folder"""
    url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
    
    data = {
        "name": name,
        "content": content
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

print("🚀 Erstelle Creative Testing Listen pro Kunde...\n")

total_created = 0
errors = []

for kunde_name, folder_id in KUNDEN.items():
    print(f"📁 {kunde_name}:")
    
    for list_name, content in LISTEN:
        print(f"   📋 {list_name}...", end=" ")
        result = create_list(folder_id, list_name, content)
        
        if "id" in result:
            print(f"✅")
            total_created += 1
        else:
            error_msg = result.get('err', 'Unbekannter Fehler')
            print(f"❌ {error_msg}")
            errors.append(f"{kunde_name} - {list_name}: {error_msg}")
        
        time.sleep(0.5)  # Rate limiting
    
    print()

print(f"{'='*60}")
print(f"🎉 Ergebnis: {total_created}/{len(KUNDEN) * len(LISTEN)} Listen erstellt!")

if errors:
    print(f"\n❌ Fehler ({len(errors)}):")
    for error in errors:
        print(f"   - {error}")
else:
    print("\n✅ Keine Fehler!")

print(f"{'='*60}")
