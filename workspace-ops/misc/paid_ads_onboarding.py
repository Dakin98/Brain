#!/usr/bin/env python3
"""
Paid Ads Onboarding Automation
Kopiert 9 Templates aus Process Hub vollständig in neuen Kunden-Ordner
"""

import json
import subprocess
import time
import sys
import os

# CONFIG
AIRTABLE_TOKEN = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
CLICKUP_TOKEN = os.environ.get("CLICKUP_API_KEY", "YOUR_CLICKUP_API_KEY_HERE")
AIRTABLE_BASE = "appbGhxy9I18oIS8E"
CLICKUP_SPACE = "90040311585"
PROCESS_HUB_LIST = "901507242261"

# TEMPLATES (Task IDs aus Process Hub)
TEMPLATES = [
    {"id": "86c8c26qk", "name": "🚀 Kickoff Call", "offset": 0},
    {"id": "86c8c26tf", "name": "🔍 Tracking Audit", "offset": 1},
    {"id": "86c8c298v", "name": "📊 Account Analysis", "offset": 2},
    {"id": "86c8c2998", "name": "💡 Creative Briefing", "offset": 3},
    {"id": "86c8c299k", "name": "🎬 Creative Produktion", "offset": 5},
    {"id": "86c8c29a6", "name": "👁️ Kunden Review", "offset": 8},
    {"id": "86c8c29ae", "name": "🚀 Campaign Launch", "offset": 10},
    {"id": "86c8c29at", "name": "📈 Performance T3", "offset": 13},
    {"id": "86c8c29b7", "name": "🏆 Performance T7", "offset": 17},
]

def api_call(method, url, headers=None, data=None):
    """API Call mit curl"""
    cmd = ["curl", "-s", "-X", method, url]
    
    if headers:
        for key, val in headers.items():
            cmd.extend(["-H", f"{key}: {val}"])
    
    if data:
        cmd.extend(["-d", json.dumps(data)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except:
        return {"error": result.stdout}

def get_new_customer():
    """Finde neuen Kunden in Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Kunden"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    
    # Filter: Status=Aktiv, Services=Paid Ads, ClickUp Folder ID=leer
    filter_formula = "AND({Status}='Aktiv', FIND('Paid Ads', {Services}), OR({ClickUp Folder ID}='', {ClickUp Folder ID}=BLANK()))"
    
    result = api_call("GET", f"{url}?filterByFormula={filter_formula}&maxRecords=1", headers)
    
    records = result.get("records", [])
    if not records:
        return None
    
    return {
        "id": records[0]["id"],
        "name": records[0]["fields"].get("Firmenname", "Unbekannt"),
        "fields": records[0]["fields"]
    }

def create_clickup_folder(customer_name):
    """Erstelle ClickUp Folder"""
    url = f"https://api.clickup.com/api/v2/space/{CLICKUP_SPACE}/folder"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {"name": customer_name}
    
    result = api_call("POST", url, headers, data)
    return result.get("id")

def create_list(folder_id, list_name):
    """Erstelle Liste im Folder"""
    url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {"name": list_name}
    
    result = api_call("POST", url, headers, data)
    return result.get("id")

def copy_template(template_id, target_list_id, customer_name, due_date, assignee=63066979):
    """Kopiere Template inkl. aller Checklisten"""
    
    # 1. Template Details holen
    url = f"https://api.clickup.com/api/v2/task/{template_id}"
    headers = {"Authorization": CLICKUP_TOKEN}
    template = api_call("GET", url, headers)
    
    if "error" in template:
        print(f"   ❌ Fehler beim Lesen Template {template_id}")
        return None
    
    # 2. Neuen Task erstellen
    name = template.get("name", "").replace("[TEMPLATE] ", "").replace(" — [Kunde]", "")
    desc = template.get("description", "")
    
    url = f"https://api.clickup.com/api/v2/list/{target_list_id}/task"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "name": f"{name} — {customer_name}",
        "description": desc,
        "due_date": due_date,
        "assignees": [assignee]
    }
    
    new_task = api_call("POST", url, headers, data)
    new_task_id = new_task.get("id")
    
    if not new_task_id:
        print(f"   ❌ Fehler beim Erstellen Task")
        return None
    
    # 3. Checklisten kopieren
    checklists = template.get("checklists", [])
    for checklist in checklists:
        # Checkliste erstellen
        url = f"https://api.clickup.com/api/v2/task/{new_task_id}/checklist"
        cl_data = {"name": checklist.get("name", "Checkliste")}
        new_cl = api_call("POST", url, headers, cl_data)
        new_cl_id = new_cl.get("checklist", {}).get("id")
        
        if new_cl_id:
            # Items kopieren
            items = checklist.get("items", [])
            for item in items:
                url = f"https://api.clickup.com/api/v2/checklist/{new_cl_id}/checklist_item"
                item_data = {"name": item.get("name", "")}
                api_call("POST", url, headers, item_data)
    
    return new_task_id

def update_airtable(customer_id, folder_id):
    """Speichere Folder ID in Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Kunden/{customer_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"fields": {"ClickUp Folder ID": folder_id}}
    
    api_call("PATCH", url, headers, data)

def main():
    print("🚀 Paid Ads Onboarding Automation")
    print("=================================")
    print()
    
    # 1. Neuen Kunden finden
    print("📋 Suche neuen Kunden...")
    customer = get_new_customer()
    
    if not customer:
        print("   ℹ️  Keine neuen Kunden gefunden")
        return
    
    print(f"   ✅ Kunde: {customer['name']}")
    print()
    
    # 2. ClickUp Folder erstellen
    print("🏗️  Erstelle ClickUp Folder...")
    folder_id = create_clickup_folder(customer['name'])
    if not folder_id:
        print("   ❌ Fehler beim Erstellen Folder")
        return
    print(f"   ✅ Folder ID: {folder_id}")
    print()
    
    # 3. Listen erstellen
    print("📂 Erstelle 6 Listen...")
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
        list_id = create_list(folder_id, list_name)
        lists[list_name] = list_id
        print(f"   ✅ {list_name}")
        time.sleep(0.3)
    
    pm_list_id = lists["📋 Project Management"]
    print()
    
    # 4. Templates kopieren
    print("📋 Kopiere 9 Templates mit Checklisten...")
    from datetime import datetime, timedelta
    now = datetime.now()
    
    for i, template in enumerate(TEMPLATES, 1):
        print(f"   {i}/9: {template['name']}...", end=" ")
        
        # Due Date berechnen
        due = now + timedelta(days=template['offset'])
        due_timestamp = int(due.timestamp() * 1000)
        
        # Template kopieren
        task_id = copy_template(
            template['id'],
            pm_list_id,
            customer['name'],
            due_timestamp
        )
        
        if task_id:
            print("✅")
        else:
            print("❌")
        
        time.sleep(0.5)
    
    print()
    
    # 5. Airtable updaten
    print("💾 Speichere Folder ID in Airtable...")
    update_airtable(customer['id'], folder_id)
    print("   ✅ Gespeichert")
    print()
    
    print("🎉 AUTOMATION ABGESCHLOSSEN!")
    print(f"   Kunde: {customer['name']}")
    print(f"   Folder ID: {folder_id}")
    print(f"   9 Tasks mit Checklisten erstellt")

if __name__ == "__main__":
    main()
