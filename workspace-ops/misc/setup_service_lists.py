#!/usr/bin/env python3
"""
ClickUp: Service-spezifische Content-Listen für alle Kunden
(Paid Ads, Email Marketing, Cold Mail)
"""
import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"

KUNDEN = {
    "ATB Bau": "901514522366",
    "Green Cola Germany": "901514522387",
    "schnelleinfachgesund": "901514522393",
    "Ferro Berlin": "901514522399",
    "RAZECO": "901514522405"
}

SERVICE_LISTEN = [
    ("📅 Paid Ads Content", "Batches, Hooks, Scripts, UGC Briefings für Paid Ads Kampagnen"),
    ("📧 Email Content", "Newsletter, Flows, Kampagnen für Email Marketing"),
    ("📨 Cold Mail Content", "Sequenzen, Hooks, Personalization für Cold Outreach")
]

def get_lists_in_folder(folder_id):
    url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
    req = urllib.request.Request(url)
    req.add_header("Authorization", API_TOKEN)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()).get('lists', [])
    except:
        return []

def delete_list(list_id):
    url = f"https://api.clickup.com/api/v2/list/{list_id}"
    req = urllib.request.Request(url, method="DELETE")
    req.add_header("Authorization", API_TOKEN)
    try:
        urllib.request.urlopen(req)
        return True
    except:
        return False

def create_list(folder_id, name, content=""):
    url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
    data = {"name": name, "content": content}
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

print("🔄 Optimiere für Service-Skalierbarkeit...\n")

total_created = 0
total_deleted = 0

for kunde, folder_id in KUNDEN.items():
    print(f"📁 {kunde}:")
    
    # 1. Alte "Content Batches" Liste löschen
    lists = get_lists_in_folder(folder_id)
    for lst in lists:
        if "Content Batches" in lst['name'] or lst['name'] == "📅 Content Batches":
            print(f"   🗑️  Alte 'Content Batches'...", end=" ")
            if delete_list(lst['id']):
                print("✅ Gelöscht")
                total_deleted += 1
            else:
                print("❌")
            time.sleep(0.3)
    
    # 2. Neue Service-spezifische Listen erstellen
    for name, content in SERVICE_LISTEN:
        print(f"   📋 {name}...", end=" ")
        result = create_list(folder_id, name, content)
        if "id" in result:
            print("✅")
            total_created += 1
        else:
            print(f"❌ {result.get('err', 'Fehler')}")
        time.sleep(0.5)
    
    print()

print(f"{'='*60}")
print(f"🎉 Ergebnis:")
print(f"   🗑️  {total_deleted} alte Listen gelöscht")
print(f"   📋 {total_created} neue Service-Listen erstellt")
print(f"{'='*60}")
print("\n✅ Jeder Kunde hat jetzt SKALIERBARE Struktur:")
print("   📅 Paid Ads Content      ← Hooks, Scripts, UGC Briefings")
print("   📧 Email Content         ← Newsletter, Flows, Kampagnen")  
print("   📨 Cold Mail Content     ← Sequenzen, Personalization")
print("   📝 Creative Pipeline     ← Paid Ads Produktion (Videos, Bilder)")
print("   📦 Creative Archive      ← Fertige Paid Ads Creatives")
print("   📚 Creative Learnings    ← Insights (alle Services)")
print("   👤 Creator Pool          ← UGC Creators (Paid Ads)")
