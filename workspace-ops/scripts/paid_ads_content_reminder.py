#!/usr/bin/env python3
"""
Paid Ads: Content Reminder Automation
Prüft Airtable auf Paid Ads Kunden und erstellt wöchentliche Content Batch Tasks in ClickUp
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# === CONFIG ===
AIRTABLE_TOKEN = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
CLICKUP_TOKEN = os.environ.get("CLICKUP_API_KEY", "YOUR_CLICKUP_API_KEY_HERE")
AIRTABLE_BASE = "appbGhxy9I18oIS8E"
CLICKUP_SPACE = "90040311585"

# Telegram Config (from environment or default)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7348148375")  # Deniz

def telegram_notify(message):
    """Sende Telegram Benachrichtigung an Deniz"""
    # Verwende den message tool statt direktem API call
    # Dies wird vom aufrufenden Script übernommen
    pass

def airtable_request(method, endpoint, data=None):
    """Airtable API Request"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode() if data else None,
            headers=headers,
            method=method
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": json.loads(e.read().decode())}
    except Exception as e:
        return {"error": str(e)}

def clickup_request(method, endpoint, data=None):
    """ClickUp API Request"""
    url = f"https://api.clickup.com/api/v2/{endpoint}"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            headers=headers,
            method=method
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        try:
            return {"error": json.loads(err_body)}
        except:
            return {"error": err_body}
    except Exception as e:
        return {"error": str(e)}

def get_paid_ads_customers():
    """Holt alle Kunden mit Paid Ads (Meta Ad Account ID vorhanden)"""
    # Filter: Status = Aktiv AND Meta Ad Account ID ist nicht leer
    filter_formula = "AND({Status}='Aktiv', NOT({Meta Ad Account ID}=''), NOT({Meta Ad Account ID}=BLANK()))"
    
    result = airtable_request(
        "GET",
        f"Kunden?filterByFormula={filter_formula.replace(' ', '%20').replace('=', '%3D')}&fields[]=Firmenname&fields[]=ClickUp%20Folder%20ID&fields[]=Meta%20Ad%20Account%20ID"
    )
    
    if "error" in result:
        print(f"❌ Airtable Fehler: {result['error']}")
        return []
    
    customers = []
    for record in result.get("records", []):
        fields = record.get("fields", {})
        customers.append({
            "id": record["id"],
            "name": fields.get("Firmenname", "Unbekannt"),
            "folder_id": fields.get("ClickUp Folder ID"),
            "meta_account": fields.get("Meta Ad Account ID")
        })
    
    return customers

def get_content_list_id(folder_id):
    """Findet die '📅 Paid Ads Content' Liste im Folder"""
    result = clickup_request("GET", f"folder/{folder_id}/list")
    
    if "error" in result:
        return None
    
    for lst in result.get("lists", []):
        if "Paid Ads Content" in lst["name"] or "Content" in lst["name"]:
            return lst["id"]
    
    return None

def create_content_batch_task(list_id, customer_name, kw):
    """Erstellt einen Content Batch Task"""
    due_date = datetime.now() + timedelta(days=7)  # Fällig in einer Woche
    
    task_data = {
        "name": f"📅 Paid Ads Content Batch — {kw}",
        "description": f"""🎯 **ZIEL:** 3-5 neue Creatives für {customer_name} Paid Ads Kampagnen

⏱️ Aufwand: 4-6 Stunden
👤 Verantwortlich: Deniz
📦 Output: 3-5 Creatives in Creative Pipeline

🔗 **Workflow:**
1. Diesen Task bearbeiten (Ideen + Briefings)
2. Einzelne Creative-Tasks in "📝 Creative Pipeline" erstellen
3. Creatives produzieren lassen (Creator/VA)
4. Fertige Creatives in Ads hochladen

✅ **Quality Gate:** Alle 3-5 Creatives haben klare Hooks, Angles und Format-Definition""",
        "due_date": int(due_date.timestamp() * 1000),
        "assignees": [63066979],  # Deniz
        "tags": ["content-batch", "paid-ads"],
        "checklists": [
            {
                "name": "Content Batch Checklist",
                "items": [
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
                ]
            }
        ]
    }
    
    result = clickup_request("POST", f"list/{list_id}/task", task_data)
    return result

def main():
    print("=" * 60)
    print("📅 Paid Ads: Content Reminder Automation")
    print("=" * 60)
    print()
    
    # Aktuelle Kalenderwoche
    now = datetime.now()
    kw = f"KW{now.strftime('%V')}"
    date_str = now.strftime("%d.%m.%Y")
    
    print(f"📆 Zeitraum: {kw} ({date_str})")
    print()
    
    # 1. Paid Ads Kunden holen
    print("🔍 Suche Paid Ads Kunden in Airtable...")
    customers = get_paid_ads_customers()
    
    if not customers:
        print("   ℹ️ Keine Paid Ads Kunden gefunden.")
        return {
            "status": "no_customers",
            "message": "Keine Paid Ads Kunden in Airtable gefunden."
        }
    
    print(f"   ✅ {len(customers)} Paid Ads Kunden gefunden:")
    for c in customers:
        print(f"      • {c['name']}")
    print()
    
    # 2. Für jeden Kunden Content Batch erstellen
    created_tasks = []
    skipped = []
    errors = []
    
    for customer in customers:
        print(f"📋 {customer['name']}:")
        
        if not customer["folder_id"]:
            print(f"   ⚠️  Kein ClickUp Folder ID → übersprungen")
            skipped.append({"name": customer["name"], "reason": "Kein Folder ID"})
            continue
        
        # Liste finden
        list_id = get_content_list_id(customer["folder_id"])
        if not list_id:
            print(f"   ⚠️  Keine 'Paid Ads Content' Liste gefunden → übersprungen")
            skipped.append({"name": customer["name"], "reason": "Keine Content Liste"})
            continue
        
        # Task erstellen
        result = create_content_batch_task(list_id, customer["name"], kw)
        
        if "error" in result:
            print(f"   ❌ Fehler: {result['error']}")
            errors.append({"name": customer["name"], "error": str(result['error'])[:100]})
        elif "id" in result:
            task_url = f"https://app.clickup.com/t/{result['id']}"
            print(f"   ✅ Task erstellt: {task_url}")
            created_tasks.append({
                "name": customer["name"],
                "task_id": result["id"],
                "url": task_url
            })
        else:
            print(f"   ❌ Unbekannter Fehler: {result}")
            errors.append({"name": customer["name"], "error": "Unbekannter Fehler"})
    
    print()
    print("=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"   ✅ Erstellt: {len(created_tasks)} Tasks")
    print(f"   ⏭️  Übersprungen: {len(skipped)}")
    print(f"   ❌ Fehler: {len(errors)}")
    print()
    
    # Ergebnis zurückgeben
    return {
        "status": "success" if created_tasks else "partial",
        "kw": kw,
        "date": date_str,
        "created": created_tasks,
        "skipped": skipped,
        "errors": errors
    }

if __name__ == "__main__":
    result = main()
    # Output als JSON für weitere Verarbeitung
    print(json.dumps(result, indent=2, ensure_ascii=False))