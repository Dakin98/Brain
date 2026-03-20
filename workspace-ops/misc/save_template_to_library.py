#!/usr/bin/env python3
"""
ClickUp: Paid Ads Template in Process Library speichern
"""
import urllib.request, os, json

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
TEMPLATE_LIST_ID = "901507242261"  # Process Hub

def create_task(name, description, checklist_items=None):
    url = f"https://api.clickup.com/api/v2/list/{TEMPLATE_LIST_ID}/task"
    
    # Tags hinzufügen für einfaches Filtern
    data = {
        "name": f"[TEMPLATE] {name}",
        "description": f"📋 PAID ADS TEMPLATE\n\n{description}\n\n---\n💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben",
        "tags": ["template", "paid-ads", "workflow"]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            task = json.loads(response.read().decode())
            task_id = task.get("id")
            
            if checklist_items and task_id:
                add_checklist(task_id, name, checklist_items)
            
            return task
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

def add_checklist(task_id, name, items):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/checklist"
    data = {"name": f"Checklist"}
    
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

print("🚀 Speichere Paid Ads Template in Process Library...\n")

templates = [
    ("🚀 Kickoff Call", "Erstgespräch mit dem Kunden. Ziele definieren, Erwartungen abstimmen, Briefing sammeln.", [
        "Zugänge erhalten (Meta BM, Google Ads, etc.)",
        "Ziele & KPIs besprochen",
        "Budget & Laufzeit geklärt",
        "Briefing-Fragen beantwortet",
        "Nächste Schritte definiert",
        "Termin für Tracking-Check vereinbart"
    ]),
    ("🔍 Tracking Audit & Setup", "Alle Tracking-Systeme prüfen und sicherstellen, dass Conversions korrekt erfasst werden.", [
        "GTM (Google Tag Manager) Container prüfen",
        "Stape Server-Side Tracking eingerichtet",
        "Meta Pixel firing korrekt",
        "Meta CAPI (Conversions API) aktiv",
        "GA4 Property verbunden",
        "E-Commerce Events tracken",
        "Test-Kauf durchgeführt"
    ]),
    ("📊 Account Analysis", "Bestandsaufnahme: Was lief bisher? Winner & Loser identifizieren.", [
        "Alte Ads exportieren (letzte 90 Tage)",
        "Performance-Daten analysieren",
        "Winner Creatives identifizieren",
        "Loser Patterns erkennen",
        "Audience Insights notieren",
        "Wettbewerber-Research",
        "Insights in Creative Ideas dokumentieren"
    ]),
    ("💡 Creative Briefing", "Angles, Hooks & Konzepte für den ersten Batch definieren.", [
        "Research-Ergebnisse auswerten",
        "Kunden-Input zusammenfassen",
        "3-5 Haupt-Angles definieren",
        "Hooks pro Angle brainstormen",
        "Format-Mix planen (Static, VSL, UGC)",
        "Creative Plan mit Kunden abstimmen",
        "Briefing für Creators/VA erstellen"
    ]),
    ("🎬 Creative Produktion (Batch 1)", "5 Creatives produzieren: Editing, Motion, Sound, Export.", [
        "Rohmaterial von Creators erhalten",
        "Editing durchführen (VA/Freelancer)",
        "Motion Graphics hinzufügen",
        "Sound & Musik",
        "Hooks/CTAs einfügen",
        "Alle Formate exportieren",
        "Quality Check durchführen"
    ]),
    ("👁️ Kunden Review", "Creatives präsentieren, Feedback sammeln, Finalisierung.", [
        "Preview-Links erstellen",
        "Kunden-Präsentation vorbereiten",
        "Feedback-Runde durchführen",
        "Änderungen dokumentieren",
        "Final Assets erstellen",
        "Kunden-Approval einholen"
    ]),
    ("🚀 Campaign Launch", "Ads live schalten: €50/Tag Test-Budget, Tracking prüfen.", [
        "Campaign-Struktur aufbauen",
        "Ad Sets mit Targeting erstellen",
        "Creatives hochladen",
        "Tracking-URLs prüfen",
        "Budget: €50/Tag Test",
        "Bidding-Strategie setzen",
        "Ads aktivieren",
        "Erste 24h Monitoring"
    ]),
    ("📈 Performance Check (Tag 3)", "Erste Analyse nach 3 Tagen: Daten auswerten, erste Optimierungen.", [
        "Spend, CTR, CPM checken",
        "Pixel-Firing verifizieren",
        "Erste Conversions beobachten",
        "Creative Performance vergleichen",
        "Budget-Adjustments",
        "Learnings dokumentieren"
    ]),
    ("🏆 Performance Check (Tag 7) - Winner/Loser", "Nach 7 Tagen: Winner identifizieren, Loser pausieren, Scale-Plan erstellen.", [
        "ROAS/CPA pro Creative analysieren",
        "Winners markieren (Scale)",
        "Losers identifizieren (Pause)",
        "Iterieren-Liste erstellen",
        "Scale-Budget planen",
        "Neue Batches briefen",
        "Kunden-Update senden"
    ])
]

success_count = 0
for name, desc, checklist in templates:
    print(f"📋 {name}...")
    result = create_task(name, desc, checklist)
    if "id" in result:
        print(f"   ✅ Gespeichert")
        success_count += 1
    else:
        print(f"   ❌ {result.get('err', 'Fehler')}")

print(f"\n🎉 {success_count}/{len(templates)} Templates gespeichert!")
print(f"\n📍 Ort: Process Library → Process Hub")
print("🏷️  Filter: Tags 'template' + 'paid-ads'")
print("\n💡 Nutzung:")
print("   1. In Process Hub → Filter: Tags = 'paid-ads'")
print("   2. Alle 9 Tasks auswählen")
print("   3. 'Duplicate Tasks' → Ziel: Kunden-Projekt")
