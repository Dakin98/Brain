#!/usr/bin/env python3
"""
ClickUp: Content Batch Templates für Process Library
"""
import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
PROCESS_HUB_ID = "901507242261"

def create_task(name, description, checklist_items=None, tags=None):
    url = f"https://api.clickup.com/api/v2/list/{PROCESS_HUB_ID}/task"
    
    data = {
        "name": f"[TEMPLATE] {name}",
        "description": description,
        "tags": tags or ["template", "content-batch"]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            task = json.loads(response.read().decode())
            task_id = task.get("id")
            
            if checklist_items and task_id:
                add_checklist(task_id, "Checklist", checklist_items)
            
            return task
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

def add_checklist(task_id, name, items):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/checklist"
    data = {"name": name}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            checklist = json.loads(response.read().decode())
            checklist_id = checklist.get("checklist", {}).get("id")
            
            for item in items:
                add_checklist_item(checklist_id, item)
    except Exception as e:
        print(f"   Checklist Error: {e}")

def add_checklist_item(checklist_id, name):
    url = f"https://api.clickup.com/api/v2/checklist/{checklist_id}/checklist_item"
    data = {"name": name}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        urllib.request.urlopen(req)
    except:
        pass

print("🚀 Erstelle Content Batch Templates...\n")

# Template 1: Paid Ads Content Batch
print("📋 Paid Ads Content Batch...")
task1 = create_task(
    "📅 Paid Ads Content Batch — KW{XX}",
    """🎯 ZIEL: 3-5 neue Creatives für Paid Ads Kampagnen

⏱️ Aufwand: 4-6 Stunden
👤 Verantwortlich: Deniz
📦 Output: 3-5 Creatives in Creative Pipeline

🔗 Workflow:
1. Diesen Task bearbeiten (Ideen + Briefings)
2. Einzelne Creative-Tasks in "Creative Pipeline" erstellen
3. Creatives produzieren lassen (Creator/VA)
4. Fertige Creatives in Ads hochladen

✅ Quality Gate: Alle 3-5 Creatives haben klare Hooks, Angles und Format-Definition""",
    [
        "Winning Creatives der letzten 14 Tage analysieren (CTR, Hook Rate)",
        "3-5 neue Hook-Varianten brainstormen (Problem-Agitate, Social Proof, Bold Claim)",
        "Format-Mix definieren (Static, UGC, VSL?) je nach Account-Bedarf",
        "Angles für jeden Hook schreiben (Problem → Lösung → CTA)",
        "Für UGC: Creator-Briefing erstellen (Script, B-Roll Anweisungen)",
        "Für Static: Canva/Figma Templates befüllen (Texte, Bilder)",
        "Für VSL: Skript schreiben (Hook in ersten 3 Sekunden!)",
        "3-5 Creative-Tasks in Creative Pipeline erstellen (verlinken zu diesem Batch)",
        "Creators/VA briefen und Deadlines setzen",
        "Diesen Batch-Task auf 'Fertig' setzen → Produktion läuft"
    ],
    ["template", "paid-ads", "content-batch"]
)
print(f"   {'✅' if 'id' in task1 else '❌'}")
time.sleep(0.5)

# Template 2: Email Content Batch  
print("📧 Email Content Batch...")
task2 = create_task(
    "📧 Email Content Batch — KW{XX}",
    """🎯 ZIEL: Newsletter oder Flow-Email für Klaviyo

⏱️ Aufwand: 2-3 Stunden
👤 Verantwortlich: Deniz
📦 Output: Fertige Email in Klaviyo

✅ Quality Gate: Email hat klaren CTA, Brand Voice passt, Mobile-optimiert""",
    [
        "Notion Kalender prüfen (Thema der Woche)",
        "Website/Shop des Kunden analysieren (neue Produkte, Angebote)",
        "Subject Lines brainstormen (5 Varianten, emoji ja/nein?)",
        "Email-Struktur: Hook → Story/Value → CTA",
        "Copy schreiben (Preview Text, Body, CTA Button)",
        "Bilder auswählen oder Design anfordern",
        "In Klaviyo Template einfügen",
        "Mobile Preview prüfen (60% öffnen auf Handy!)",
        "Test-Email senden (Rechtschreibung, Links)",
        "Für Review an Kunden senden (wenn nötig)"
    ],
    ["template", "email-marketing", "content-batch"]
)
print(f"   {'✅' if 'id' in task2 else '❌'}")
time.sleep(0.5)

# Template 3: Cold Mail Content Batch
print("📨 Cold Mail Content Batch...")
task3 = create_task(
    "📨 Cold Mail Content Batch — KW{XX}",
    """🎯 ZIEL: Neue Sequenz oder Sequenz-Update für Cold Outreach

⏱️ Aufwand: 3-4 Stunden
👤 Verantwortlich: Deniz
📦 Output: Copy für Instantly Sequenz

✅ Quality Gate: Personalisiert, nicht zu verkaufsorientiert, klare CTA""",
    [
        "Zielgruppe/Ideal Customer Profile reviewen",
        "Lead-Liste qualität prüfen (neue Leads von Apollo?)",
        "Pain Points der Zielgruppe definieren",
        "Sequenz-Struktur planen (Touch 1-4: Cold → Follow-up → Value → Break-up)",
        "Subject Lines schreiben (kein Spam-Trigger!)",
        "Email 1 (Cold): Personalisierung + Hook + Soft CTA",
        "Email 2 (Follow-up): Kurze Erinnerung + zusätzlicher Value",
        "Email 3 (Value): Case Study, Statistik oder Insight",
        "Email 4 (Break-up): Letzter Versuch + Alternativer CTA",
        "In Instantly einfügen und Variablen testen ({{first_name}}, {{company}})",
        "Test-Email an sich selbst schicken"
    ],
    ["template", "cold-mail", "content-batch"]
)
print(f"   {'✅' if 'id' in task3 else '❌'}")
time.sleep(0.5)

print("\n🎉 Alle Content Batch Templates erstellt!")
print("\n📍 Ort: Process Library → Process Hub")
print("🏷️  Filter: Tags 'template' + 'content-batch'")
print("\n💡 Nutzung:")
print("   1. Filter: Tags = 'content-batch'")
print("   2. Passendes Template duplizieren")
print("   3. In Kunden-Folder → Content-Liste verschieben")
print("   4. KW anpassen, Due Date setzen")
