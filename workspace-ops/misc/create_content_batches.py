#!/usr/bin/env python3
"""
ClickUp: Content Batches Liste für alle Kunden erstellen
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

print("📅 Erstelle Content Batches Listen...\n")

total = 0
for kunde, folder_id in KUNDEN.items():
    print(f"📁 {kunde}:", end=" ")
    
    result = create_list(
        folder_id,
        "📅 Content Batches",
        "Wöchentliche Content-Planung: Ideen, Briefings, und Batch-Übersicht. Jeder Batch erzeugt 3-5 Creatives in der Creative Pipeline."
    )
    
    if "id" in result:
        print(f"✅")
        total += 1
    else:
        print(f"❌ {result.get('err', 'Fehler')}")
    
    time.sleep(0.5)

print(f"\n🎉 {total}/{len(KUNDEN)} Content Batches Listen erstellt!")
print("\n✅ Jeder Kunde hat jetzt:")
print("   📅 Content Batches      ← Planung/Briefing (wöchentlich)")
print("   📝 Creative Pipeline    ← Einzelne Creatives (Produktion)")
print("   📦 Creative Archive     ← Abgeschlossen")
print("   📚 Creative Learnings   ← Insights")
print("   👤 Creator Pool         ← UGC Creators")
