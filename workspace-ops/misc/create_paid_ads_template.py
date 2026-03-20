#!/usr/bin/env python3
"""
ClickUp: Paid Ads Task Template erstellen
Erstellt Tasks mit Checklisten für den Paid Ads Workflow
"""
import urllib.request, os, json

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
LIST_ID = "901521337307"  # Creative Pipeline

def create_task(name, description, checklist_items=None):
    """Erstellt einen Task mit Checkliste"""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    
    data = {
        "name": name,
        "description": description
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            task = json.loads(response.read().decode())
            task_id = task.get("id")
            
            # Checkliste hinzufügen wenn vorhanden
            if checklist_items and task_id:
                add_checklist(task_id, name, checklist_items)
            
            return task
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

def add_checklist(task_id, name, items):
    """Fügt eine Checkliste zu einem Task hinzu"""
    url = f"https://api.clickup.com/api/v2/task/{task_id}/checklist"
    
    data = {
        "name": f"Checklist: {name}"
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            checklist = json.loads(response.read().decode())
            checklist_id = checklist.get("checklist", {}).get("id")
            
            # Items hinzufügen
            for item in items:
                add_checklist_item(checklist_id, item)
    except Exception as e:
        print(f"   Checklist Error: {e}")

def add_checklist_item(checklist_id, name):
    """Fügt ein Item zur Checkliste hinzu"""
    url = f"https://api.clickup.com/api/v2/checklist/{checklist_id}/checklist_item"
    
    data = {"name": name}
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Authorization", API_TOKEN)
    req.add_header("Content-Type", "application/json")
    
    try:
        urllib.request.urlopen(req)
    except:
        pass

print("🚀 Erstelle Paid Ads Tasks...\n")

# Task 1: Kickoff Call
task1 = create_task(
    "🚀 Kickoff Call",
    "Erstgespräch mit dem Kunden. Ziele definieren, Erwartungen abstimmen, Briefing sammeln.",
    [
        "Zugänge erhalten (Meta BM, Google Ads, etc.)",
        "Ziele & KPIs besprochen",
        "Budget & Laufzeit geklärt",
        "Briefing-Fragen beantwortet",
        "Nächste Schritte definiert",
        "Termin für Tracking-Check vereinbart"
    ]
)
print(f"📋 Kickoff Call... {'✅' if 'id' in task1 else '❌'}")

# Task 2: Tracking Audit
task2 = create_task(
    "🔍 Tracking Audit & Setup",
    "Alle Tracking-Systeme prüfen und sicherstellen, dass Conversions korrekt erfasst werden.",
    [
        "GTM (Google Tag Manager) Container prüfen",
        "Stape Server-Side Tracking eingerichtet",
        "Meta Pixel firing korrekt",
        "Meta CAPI (Conversions API) aktiv",
        "GA4 Property verbunden",
        "E-Commerce Events tracken (Purchase, AddToCart, etc.)",
        "Test-Kauf durchgeführt"
    ]
)
print(f"📋 Tracking Audit... {'✅' if 'id' in task2 else '❌'}")

# Task 3: Account Analysis
task3 = create_task(
    "📊 Account Analysis",
    "Bestandsaufnahme: Was lief bisher? Winner & Loser identifizieren.",
    [
        "Alte Ads exportieren (letzte 90 Tage)",
        "Performance-Daten analysieren",
        "Winner Creatives identifizieren",
        "Loser Patterns erkennen",
        "Audience Insights notieren",
        "Wettbewerber-Research",
        "Insights in Creative Ideas dokumentieren"
    ]
)
print(f"📋 Account Analysis... {'✅' if 'id' in task3 else '❌'}")

# Task 4: Creative Briefing
task4 = create_task(
    "💡 Creative Briefing",
    "Angles, Hooks & Konzepte für den ersten Batch definieren.",
    [
        "Research-Ergebnisse auswerten",
        "Kunden-Input zusammenfassen",
        "3-5 Haupt-Angles definieren",
        "Hooks pro Angle brainstormen",
        "Format-Mix planen (Static, VSL, UGC)",
        "Creative Plan mit Kunden abstimmen",
        "Briefing für Creators/VA erstellen"
    ]
)
print(f"📋 Creative Briefing... {'✅' if 'id' in task4 else '❌'}")

# Task 5: Creative Produktion
task5 = create_task(
    "🎬 Creative Produktion (Batch 1 - 5 Stück)",
    "5 Creatives produzieren: Editing, Motion, Sound, Export.",
    [
        "Rohmaterial von Creators erhalten",
        "Editing durchführen (VA/Freelancer)",
        "Motion Graphics hinzufügen",
        "Sound & Musik",
        "Hooks/CTAs einfügen",
        "Alle Formate exportieren (1:1, 9:16, 4:5)",
        "Quality Check durchführen"
    ]
)
print(f"📋 Creative Produktion... {'✅' if 'id' in task5 else '❌'}")

# Task 6: Kunden Review
task6 = create_task(
    "👁️ Kunden Review",
    "Creatives präsentieren, Feedback sammeln, Finalisierung.",
    [
        "Preview-Links erstellen",
        "Kunden-Präsentation vorbereiten",
        "Feedback-Runde durchführen",
        "Änderungen dokumentieren",
        "Final Assets erstellen",
        "Kunden-Approval einholen"
    ]
)
print(f"📋 Kunden Review... {'✅' if 'id' in task6 else '❌'}")

# Task 7: Campaign Launch
task7 = create_task(
    "🚀 Campaign Launch",
    "Ads live schalten: €50/Tag Test-Budget, Tracking prüfen.",
    [
        "Campaign-Struktur aufbauen",
        "Ad Sets mit Targeting erstellen",
        "Creatives hochladen",
        "Tracking-URLs prüfen",
        "Budget: €50/Tag Test",
        "Bidding-Strategie setzen",
        "Ads aktivieren",
        "Erste 24h Monitoring"
    ]
)
print(f"📋 Campaign Launch... {'✅' if 'id' in task7 else '❌'}")

# Task 8: Performance Check Day 3
task8 = create_task(
    "📈 Performance Check (Tag 3)",
    "Erste Analyse nach 3 Tagen: Daten auswerten, erste Optimierungen.",
    [
        "Spend, CTR, CPM checken",
        "Pixel-Firing verifizieren",
        "Erste Conversions beobachten",
        "Creative Performance vergleichen",
        "Budget-Adjustments (Scale/Pause)",
        "Learnings dokumentieren"
    ]
)
print(f"📋 Performance Check Day 3... {'✅' if 'id' in task8 else '❌'}")

# Task 9: Performance Check Day 7 (Winner/Loser)
task9 = create_task(
    "🏆 Performance Check (Tag 7) - Winner/Loser",
    "Nach 7 Tagen: Winner identifizieren, Loser pausieren, Scale-Plan erstellen.",
    [
        "ROAS/CPA pro Creative analysieren",
        "Winners markieren (Scale) ✅",
        "Losers identifizieren (Pause) ❌",
        "Iterieren-Liste erstellen 🔁",
        "Scale-Budget planen",
        "Neue Batches briefen",
        "Kunden-Update senden"
    ]
)
print(f"📋 Performance Check Day 7... {'✅' if 'id' in task9 else '❌'}")

print("\n🎉 Alle Paid Ads Tasks erstellt!")
print("\n💡 Tipp: Diese Tasks als Template speichern:")
print("   1. Alle Tasks auswählen")
print("   2. Rechtsklick → 'Als Template speichern'")
print("   3. Name: 'Paid Ads - Standard Flow'")
