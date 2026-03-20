#!/usr/bin/env python3
"""
Paid Ads Onboarding Automation - ROBUSTE VERSION
Kopiert 9 Templates vollständig in neuen Kunden-Ordner
"""

import json
import subprocess
import time
import sys
import os
from datetime import datetime, timedelta

# === CONFIG ===
AIRTABLE_TOKEN = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
CLICKUP_TOKEN = os.environ.get("CLICKUP_API_KEY", "YOUR_CLICKUP_API_KEY_HERE")
AIRTABLE_BASE = "appbGhxy9I18oIS8E"
CLICKUP_SPACE = "90040311585"
PROCESS_HUB_LIST = "901507242261"

# TEMPLATES (Task IDs aus Process Hub) - IN REIHENFOLGE
TEMPLATES = [
    {"id": "86c8c26qk", "name": "Kickoff Call", "emoji": "🚀", "offset": 0},
    {"id": "86c8c26tf", "name": "Tracking Audit", "emoji": "🔍", "offset": 1},
    {"id": "86c8c298v", "name": "Account Analysis", "emoji": "📊", "offset": 2},
    {"id": "86c8c2998", "name": "Creative Briefing", "emoji": "💡", "offset": 3},
    {"id": "86c8c299k", "name": "Creative Produktion", "emoji": "🎬", "offset": 5},
    {"id": "86c8c29a6", "name": "Kunden Review", "emoji": "👁️", "offset": 8},
    {"id": "86c8c29ae", "name": "Campaign Launch", "emoji": "🚀", "offset": 10},
    {"id": "86c8c29at", "name": "Performance T3", "emoji": "📈", "offset": 13},
    {"id": "86c8c29b7", "name": "Performance T7", "emoji": "🏆", "offset": 17},
]

# === API FUNCTIONS ===

def curl_api(method, url, headers=None, data=None):
    """Zuverlässiger API Call mit curl"""
    cmd = ["curl", "-s", "-X", method, url]
    
    if headers:
        for key, val in headers.items():
            cmd.extend(["-H", f"{key}: {val}"])
    
    if data:
        cmd.extend(["-d", json.dumps(data, ensure_ascii=False)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {"error": f"curl failed: {result.stderr}"}
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {result.stdout[:200]}"}
    except Exception as e:
        return {"error": str(e)}

def get_new_customer():
    """Finde neuen Kunden in Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Kunden"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    
    # Suche nach Kunden mit Status=Aktiv, Services=Paid Ads, ohne Folder ID
    filter_formula = "AND({Status}='Aktiv', FIND('Paid Ads', {Services}), OR({ClickUp Folder ID}='', {ClickUp Folder ID}=BLANK()))"
    
    result = curl_api("GET", f"{url}?filterByFormula={filter_formula}&maxRecords=1", headers)
    
    records = result.get("records", [])
    if not records:
        return None
    
    return {
        "id": records[0]["id"],
        "name": records[0]["fields"].get("Firmenname", "Unbekannt"),
        "fields": records[0]["fields"]
    }

def create_folder(name):
    """Erstelle ClickUp Folder"""
    url = f"https://api.clickup.com/api/v2/space/{CLICKUP_SPACE}/folder"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {"name": name}
    
    result = curl_api("POST", url, headers, data)
    return result.get("id")

def create_list(folder_id, name):
    """Erstelle Liste im Folder"""
    url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {"name": name}
    
    result = curl_api("POST", url, headers, data)
    return result.get("id")

def get_template_details(template_id):
    """Hole Template-Details inkl. Checklisten"""
    url = f"https://api.clickup.com/api/v2/task/{template_id}"
    headers = {"Authorization": CLICKUP_TOKEN}
    
    return curl_api("GET", url, headers)

def create_task(list_id, name, description, due_date, assignee=63066979):
    """Erstelle neuen Task"""
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "description": description,
        "due_date": due_date,
        "assignees": [assignee]
    }
    
    return curl_api("POST", url, headers, data)

def create_checklist(task_id, name):
    """Erstelle Checkliste"""
    url = f"https://api.clickup.com/api/v2/task/{task_id}/checklist"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {"name": name}
    
    result = curl_api("POST", url, headers, data)
    return result.get("checklist", {}).get("id")

def create_checklist_item(checklist_id, name):
    """Erstelle Checklisten-Item"""
    url = f"https://api.clickup.com/api/v2/checklist/{checklist_id}/checklist_item"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {"name": name}
    
    return curl_api("POST", url, headers, data)

def update_airtable(customer_id, folder_id):
    """Speichere Folder ID in Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Kunden/{customer_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"fields": {"ClickUp Folder ID": folder_id}}
    
    return curl_api("PATCH", url, headers, data)

# === MAIN ===

def main():
    print("=" * 60)
    print("🚀 Paid Ads Onboarding Automation")
    print("=" * 60)
    print()
    
    # 1. Neuen Kunden finden
    print("📋 SCHRITT 1: Suche neuen Kunden in Airtable...")
    customer = get_new_customer()
    
    if not customer:
        print("   ℹ️  Keine neuen Kunden gefunden.")
        print("   (Alle Kunden haben bereits ClickUp Folder IDs)")
        return
    
    print(f"   ✅ Kunde gefunden: {customer['name']}")
    print()
    
    # 2. ClickUp Folder erstellen
    print("🏗️  SCHRITT 2: Erstelle ClickUp Folder...")
    folder_id = create_folder(customer['name'])
    
    if not folder_id:
        print("   ❌ FEHLER: Konnte Folder nicht erstellen")
        return
    
    print(f"   ✅ Folder ID: {folder_id}")
    print()
    
    # 3. Folder ID in Airtable speichern
    print("💾 SCHRITT 3: Speichere Folder ID in Airtable...")
    update_result = update_airtable(customer['id'], folder_id)
    
    if "error" in update_result:
        print(f"   ⚠️  Warnung: {update_result['error']}")
    else:
        print("   ✅ Gespeichert")
    print()
    
    # 4. 6 Listen erstellen
    print("📂 SCHRITT 4: Erstelle 6 Listen...")
    lists = {}
    list_names = [
        "📋 Project Management",
        "📅 Paid Ads Content", 
        "📝 Creative Pipeline",
        "📦 Creative Archive",
        "📚 Creative Learnings",
        "👤 Creator Pool"
    ]
    
    for list_name in list_names:
        print(f"   {list_name}...", end=" ")
        list_id = create_list(folder_id, list_name)
        
        if list_id:
            lists[list_name] = list_id
            print("✅")
        else:
            print("❌")
        
        time.sleep(0.5)
    
    pm_list_id = lists.get("📋 Project Management")
    if not pm_list_id:
        print("   ❌ FEHLER: Project Management Liste konnte nicht erstellt werden")
        return
    
    print()
    
    # 5. 9 Templates kopieren
    print("📋 SCHRITT 5: Kopiere 9 Templates aus Process Hub...")
    print()
    
    now = datetime.now()
    success_count = 0
    
    for i, template in enumerate(TEMPLATES, 1):
        print(f"   {i}/9 {template['emoji']} {template['name']}...")
        
        # Template-Details holen
        template_data = get_template_details(template['id'])
        
        if "error" in template_data:
            print(f"      ❌ Fehler beim Lesen Template: {template_data['error']}")
            continue
        
        # Task-Daten extrahieren
        template_name = template_data.get("name", "").replace("[TEMPLATE] ", "").replace(" — [Kunde]", "")
        template_desc = template_data.get("description", "")
        
        # Due Date berechnen
        due_date = now + timedelta(days=template['offset'])
        due_timestamp = int(due_date.timestamp() * 1000)
        
        # Task erstellen
        new_task = create_task(
            pm_list_id,
            f"{template['emoji']} {template_name} — {customer['name']}",
            template_desc,
            due_timestamp
        )
        
        if "error" in new_task:
            print(f"      ❌ Fehler beim Erstellen Task: {new_task['error']}")
            continue
        
        new_task_id = new_task.get("id")
        
        if not new_task_id:
            print(f"      ❌ Keine Task ID erhalten")
            continue
        
        # Checklisten kopieren
        checklists = template_data.get("checklists", [])
        total_items = 0
        
        for checklist in checklists:
            checklist_name = checklist.get("name", "Checkliste")
            
            # Neue Checkliste erstellen
            new_cl_id = create_checklist(new_task_id, checklist_name)
            
            if not new_cl_id:
                continue
            
            # Items kopieren
            items = checklist.get("items", [])
            for item in items:
                item_name = item.get("name", "")
                if item_name:
                    create_checklist_item(new_cl_id, item_name)
                    total_items += 1
            
            time.sleep(0.1)
        
        print(f"      ✅ Task erstellt + {total_items} Checklisten-Items")
        success_count += 1
        time.sleep(0.5)
    
    print()
    
    # 6. Zusammenfassung
    print("=" * 60)
    print("🎉 AUTOMATION ABGESCHLOSSEN!")
    print("=" * 60)
    print(f"   Kunde: {customer['name']}")
    print(f"   Folder ID: {folder_id}")
    print(f"   Listen: 6 erstellt")
    print(f"   Tasks: {success_count}/9 mit Checklisten")
    print()

if __name__ == "__main__":
    main()
