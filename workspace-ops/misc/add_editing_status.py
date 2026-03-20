#!/usr/bin/env python3
"""
ClickUp: Editing Status zu allen Creative Pipelines hinzufügen
"""
import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"

# Kunden und ihre Folder IDs
KUNDEN = {
    "ATB Bau": "901514522366",
    "Green Cola Germany": "901514522387",
    "schnelleinfachgesund": "901514522393",
    "Ferro Berlin": "901514522399",
    "RAZECO": "901514522405"
}

def get_lists_in_folder(folder_id):
    """Holt alle Listen im Folder"""
    url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
    req = urllib.request.Request(url)
    req.add_header("Authorization", API_TOKEN)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('lists', [])
    except:
        return []

def add_status(list_id, status_name, color, status_type="custom"):
    """Fügt einen Status zur Liste hinzu"""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/status"
    
    data = {
        "status_name": status_name,
        "color": color,
        "type": status_type
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

print("✂️  Füge Editing Status zu allen Creative Pipelines hinzu...\n")

total_added = 0
errors = []

for kunde_name, folder_id in KUNDEN.items():
    print(f"📁 {kunde_name}:")
    
    # Listen holen
    lists = get_lists_in_folder(folder_id)
    
    # Creative Pipeline finden
    for lst in lists:
        if "Creative Pipeline" in lst['name']:
            print(f"   📝 {lst['name']}...", end=" ")
            
            result = add_status(lst['id'], "✂️ Editing", "#FF6B35")
            
            if "id" in result or "status" in result:
                print("✅ Editing hinzugefügt")
                total_added += 1
            else:
                error_msg = result.get('err', 'Unbekannter Fehler')
                print(f"❌ {error_msg}")
                errors.append(f"{kunde_name}: {error_msg}")
            
            time.sleep(0.3)
    
    print()

print(f"{'='*60}")
print(f"🎉 Ergebnis: {total_added}/{len(KUNDEN)} Editing-Status hinzugefügt!")

if errors:
    print(f"\n❌ Fehler ({len(errors)}):")
    for error in errors:
        print(f"   - {error}")

print(f"{'='*60}")
print("\n✅ NEUER WORKFLOW:")
print("   💡 Idee → 📋 Konzept → 🎬 Produktion → ✂️ Editing → 👁️ Review → 🚀 Upload → 🧪 Live Test → 📊 Analyse → ✅ Winner")
