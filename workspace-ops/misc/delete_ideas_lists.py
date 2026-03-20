#!/usr/bin/env python3
"""
ClickUp: Creative Ideas Listen löschen (schlankere Struktur)
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

def delete_list(list_id):
    """Löscht eine Liste"""
    url = f"https://api.clickup.com/api/v2/list/{list_id}"
    
    req = urllib.request.Request(url, method="DELETE")
    req.add_header("Authorization", API_TOKEN)
    
    try:
        urllib.request.urlopen(req)
        return True
    except:
        return False

print("🗑️  Lösche Creative Ideas Listen (schlankere Struktur)...\n")

total_deleted = 0
errors = []

for kunde_name, folder_id in KUNDEN.items():
    print(f"📁 {kunde_name}:")
    
    # Listen holen
    lists = get_lists_in_folder(folder_id)
    
    for lst in lists:
        if "Creative Ideas" in lst['name']:
            print(f"   🗑️  {lst['name']}...", end=" ")
            
            if delete_list(lst['id']):
                print("✅ Gelöscht")
                total_deleted += 1
            else:
                print("❌ Fehler")
                errors.append(f"{kunde_name}: {lst['name']}")
            
            time.sleep(0.3)
    
    print()

print(f"{'='*60}")
print(f"🎉 Ergebnis: {total_deleted} Listen gelöscht!")

if errors:
    print(f"\n❌ Fehler ({len(errors)}):")
    for error in errors:
        print(f"   - {error}")

print(f"{'='*60}")
print("\n✅ Neue schlanke Struktur pro Kunde:")
print("   📝 Creative Pipeline  ← Alles von Idee bis Archive")
print("   📦 Creative Archive   ← Abgeschlossene Creatives")
print("   📚 Creative Learnings ← Insights & Erkenntnisse")
print("   👤 Creator Pool       ← UGC Creators für Kunden")
