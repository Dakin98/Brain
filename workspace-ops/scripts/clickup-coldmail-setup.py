#!/usr/bin/env python3
"""
ClickUp Cold Mail Template Automation
Erstellt Cold Mail Liste mit allen Tasks für neue Kunden
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import ssl
import argparse
from datetime import datetime, timedelta

BASE_URL = "https://api.clickup.com/api/v2"
DEFAULT_TIMEOUT = 30

# Template Task IDs (aus dem Process Hub)
TEMPLATE_TASKS = [
    ("86c8bd11p", "🌐 Domain & Inbox Setup"),
    ("86c8bd14a", "🔍 Lead List Preparation"),
    ("86c8bd16y", "✍️ Sequenz & Copy Writing"),
    ("86c8bd1a7", "🚀 Campaign Launch in Instantly"),
    ("86c8bd1dd", "💬 Reply Management Setup"),
    ("86c8bd1fv", "📈 Weekly Optimization"),
]

class ClickUpClient:
    def __init__(self, api_token=None):
        if api_token is None:
            api_token = self._get_api_token()
        self.api_token = api_token
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
    
    def _get_api_token(self):
        config_path = os.path.expanduser("~/.config/clickup/api_token")
        if os.path.exists(config_path):
            with open(config_path) as f:
                return f.read().strip()
        token = os.environ.get("CLICKUP_API_TOKEN")
        if token:
            return token
        raise ValueError("ClickUp API token not found")
    
    def _request(self, method, endpoint, data=None, params=None):
        url = f"{BASE_URL}{endpoint}"
        if params:
            query_string = "&".join(f"{k}={urllib.parse.quote(str(v))}" 
                                   for k, v in params.items() if v is not None)
            if query_string:
                url += f"?{query_string}"
        
        req = urllib.request.Request(
            url,
            headers=self.headers,
            method=method
        )
        
        if data and method in ["POST", "PUT"]:
            req.data = json.dumps(data).encode()
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=DEFAULT_TIMEOUT) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"Error {e.code}: {error_body}")
            raise
    
    def get_task(self, task_id):
        return self._request("GET", f"/task/{task_id}")
    
    def create_folder(self, space_id, name):
        data = {"name": name}
        return self._request("POST", f"/space/{space_id}/folder", data=data)
    
    def create_list(self, folder_id, name, content=""):
        data = {"name": name, "content": content}
        return self._request("POST", f"/folder/{folder_id}/list", data=data)
    
    def create_task(self, list_id, name, description="", assignees=None, due_date=None, priority=None):
        data = {"name": name, "description": description}
        if assignees:
            data["assignees"] = assignees
        if due_date:
            data["due_date"] = due_date
        if priority:
            data["priority"] = priority
        return self._request("POST", f"/list/{list_id}/task", data=data)
    
    def create_checklist(self, task_id, name):
        data = {"name": name}
        return self._request("POST", f"/task/{task_id}/checklist", data=data)
    
    def create_checklist_item(self, checklist_id, name, assignee=None):
        data = {"name": name}
        if assignee:
            data["assignee"] = assignee
        return self._request("POST", f"/checklist/{checklist_id}/checklist_item", data=data)


def copy_task_with_checklists(client, template_task_id, list_id, prefix=""):
    """Kopiert einen Task inkl. aller Checklisten"""
    # Original Task laden
    original = client.get_task(template_task_id)
    
    # Neuen Task erstellen
    task_name = f"{prefix}{original['name']}"
    if task_name.startswith("[TEMPLATE] "):
        task_name = task_name.replace("[TEMPLATE] ", "")
    
    new_task = client.create_task(
        list_id=list_id,
        name=task_name,
        description=original.get('description', ''),
        priority=original.get('priority', {}).get('id') if original.get('priority') else None
    )
    
    print(f"  ✅ Task erstellt: {task_name}")
    
    # Checklisten kopieren
    for checklist in original.get('checklists', []):
        try:
            new_checklist = client.create_checklist(new_task['id'], checklist['name'])
            checklist_id = new_checklist.get('checklist', {}).get('id') or new_checklist.get('id')
            print(f"    📋 Checklist: {checklist['name']} (ID: {checklist_id})")
            
            for item in checklist.get('items', []):
                try:
                    client.create_checklist_item(
                        checklist_id,
                        item['name'],
                        assignee=item.get('assignee', {}).get('id') if item.get('assignee') else None
                    )
                except Exception as e:
                    print(f"      ⚠️  Item fehlgeschlagen: {item['name']} - {e}")
        except Exception as e:
            print(f"    ⚠️  Checklist fehlgeschlagen: {checklist['name']} - {e}")
    
    return new_task


def setup_cold_mail_for_client(client, space_id, client_name):
    """
    Erstellt Cold Mail Setup für einen neuen Kunden:
    1. Folder erstellen (falls nicht existiert)
    2. Liste "Cold Mail" erstellen
    3. Alle 6 Template-Tasks kopieren
    """
    print(f"\n🚀 Cold Mail Setup für: {client_name}")
    print("=" * 60)
    
    # 1. Folder erstellen
    try:
        folder = client.create_folder(space_id, client_name)
        print(f"📁 Folder erstellt: {folder['name']} (ID: {folder['id']})")
    except Exception as e:
        print(f"⚠️  Folder konnte nicht erstellt werden (existiert evtl. schon): {e}")
        # Folder ID manuell suchen
        print("   Suche existierenden Folder...")
        return None
    
    folder_id = folder['id']
    
    # 2. Liste "Cold Mail" erstellen
    list_obj = client.create_list(
        folder_id=folder_id,
        name="Cold Mail",
        content=f"Cold Mail Kampagne für {client_name}"
    )
    print(f"📋 Liste erstellt: {list_obj['name']} (ID: {list_obj['id']})")
    list_id = list_obj['id']
    
    # 3. Alle Template-Tasks kopieren
    print(f"\n📥 Kopiere {len(TEMPLATE_TASKS)} Tasks aus Template...")
    created_tasks = []
    for task_id, task_name in TEMPLATE_TASKS:
        try:
            new_task = copy_task_with_checklists(client, task_id, list_id)
            created_tasks.append(new_task)
        except Exception as e:
            print(f"  ❌ Fehler beim Kopieren von {task_name}: {e}")
    
    print(f"\n✅ Fertig! {len(created_tasks)} Tasks erstellt")
    print(f"   Folder: https://app.clickup.com/{folder_id}")
    print(f"   Liste: https://app.clickup.com/{list_id}")
    
    return {
        "folder_id": folder_id,
        "list_id": list_id,
        "tasks": created_tasks
    }


def main():
    parser = argparse.ArgumentParser(description="Cold Mail Template Setup für ClickUp Kunden")
    parser.add_argument("client_name", help="Name des Kunden (für Folder)")
    parser.add_argument("--space-id", default="90040311585", 
                       help="Space ID (default: Delivery Space)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Nur simulieren, nichts erstellen")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print(f"🔍 DRY RUN für: {args.client_name}")
        print(f"   Space ID: {args.space_id}")
        print(f"   Es würden {len(TEMPLATE_TASKS)} Tasks kopiert werden:")
        for _, name in TEMPLATE_TASKS:
            print(f"     - {name}")
        return
    
    client = ClickUpClient()
    result = setup_cold_mail_for_client(client, args.space_id, args.client_name)
    
    if result:
        print(f"\n🎉 Cold Mail Setup komplett für {args.client_name}!")
    else:
        print(f"\n❌ Setup fehlgeschlagen")
        return 1


if __name__ == "__main__":
    main()
