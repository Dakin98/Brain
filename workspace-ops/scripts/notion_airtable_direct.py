#!/usr/bin/env python3
"""
Direkte API-Integration: Notion ↔ Airtable
Ohne Maton-Gateway - nur reine API-Calls
"""

import os
import json
import urllib.request
from typing import List, Dict, Optional

# API Keys (aus Umgebungsvariablen oder ersetzen)
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "YOUR_NOTION_API_KEY_HERE")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")

# IDs
NOTION_DB_ID = "3465a32b-e5e0-4d52-bec3-c24ff39e1507"
AIRTABLE_BASE_ID = "appbGhxy9I18oIS8E"
AIRTABLE_TABLE_ID = "tblmrFXGDWI4hYu46"  # 📧 Email Calendar


class NotionClient:
    """Direkter Notion API Client"""
    
    BASE_URL = "https://api.notion.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            method=method,
            headers=headers
        )
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    def query_database(self, database_id: str, page_size: int = 100, start_cursor: str = None) -> dict:
        """Query eine Notion Database"""
        payload = {"page_size": page_size}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        
        return self._request("POST", f"databases/{database_id}/query", payload)
    
    def get_database(self, database_id: str) -> dict:
        """Database Schema abrufen"""
        return self._request("GET", f"databases/{database_id}")
    
    def get_page_content(self, page_id: str) -> List[dict]:
        """Block-Content einer Page abrufen"""
        result = self._request("GET", f"blocks/{page_id}/children")
        return result.get("results", [])


class AirtableClient:
    """Direkter Airtable API Client"""
    
    BASE_URL = "https://api.airtable.com/v0"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            method=method,
            headers=headers
        )
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    def list_records(self, base_id: str, table_id: str, **params) -> dict:
        """Records aus einer Tabelle abrufen"""
        query = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items())
        endpoint = f"{base_id}/{table_id}"
        if query:
            endpoint += f"?{query}"
        return self._request("GET", endpoint)
    
    def get_record(self, base_id: str, table_id: str, record_id: str) -> dict:
        """Einzelnen Record abrufen"""
        return self._request("GET", f"{base_id}/{table_id}/{record_id}")
    
    def create_records(self, base_id: str, table_id: str, records: List[dict]) -> dict:
        """Records erstellen (max 10 pro Request)"""
        return self._request("POST", f"{base_id}/{table_id}", {"records": records})
    
    def update_records(self, base_id: str, table_id: str, records: List[dict]) -> dict:
        """Records updaten (PATCH - partial)"""
        return self._request("PATCH", f"{base_id}/{table_id}", {"records": records})
    
    def delete_records(self, base_id: str, table_id: str, record_ids: List[str]) -> dict:
        """Records löschen (max 10 pro Request)"""
        ids_param = "&".join(f"records[]={rid}" for rid in record_ids)
        return self._request("DELETE", f"{base_id}/{table_id}?{ids_param}")
    
    def get_base_schema(self, base_id: str) -> dict:
        """Base Schema (Tabellen, Felder) abrufen"""
        # Meta-API ist anders endpoint
        url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())


def sync_notion_to_airtable():
    """
    Beispiel: Sync Email Calendar von Notion nach Airtable
    """
    notion = NotionClient(NOTION_API_KEY)
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    print("📥 Lade Daten aus Notion...")
    
    # Alle Notion Einträge holen (mit Pagination)
    all_entries = []
    cursor = None
    
    while True:
        result = notion.query_database(NOTION_DB_ID, start_cursor=cursor)
        entries = result.get("results", [])
        
        for entry in entries:
            props = entry.get("properties", {})
            
            # Daten extrahieren
            name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "")
            date = props.get("Date", {}).get("date", {}).get("start")
            email_type = props.get("Email Type", {}).get("multi_select", [{}])[0].get("name", "Content")
            
            all_entries.append({
                "notion_id": entry["id"],
                "name": name,
                "date": date,
                "email_type": email_type
            })
        
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    
    print(f"✅ {len(all_entries)} Einträge aus Notion geladen")
    
    # In Airtable importieren (in Batches von 10)
    print("📤 Importiere nach Airtable...")
    
    batch = []
    created = 0
    
    for entry in all_entries:
        batch.append({
            "fields": {
                "Name": entry["name"],
                "Datum": entry["date"],
                "Email Typ": entry["email_type"],
                "Notion ID": entry["notion_id"],
                "Status": "Idee"
            }
        })
        
        if len(batch) >= 10:
            result = airtable.create_records(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID, batch)
            created += len(result.get("records", []))
            batch = []
    
    # Restliche Records
    if batch:
        result = airtable.create_records(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID, batch)
        created += len(result.get("records", []))
    
    print(f"✅ {created} Einträge in Airtable erstellt")


def get_weekly_topics():
    """
    Beispiel: Diese Woche anstehende Newsletter-Themen abrufen
    """
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    # Heutiges Datum
    from datetime import datetime, timedelta
    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Filter: Datum zwischen heute und nächste Woche
    # Airtable Filter Formula Syntax
    filter_formula = f"AND(IS_AFTER({{Datum}}, '{today}'), IS_BEFORE({{Datum}}, '{next_week}'))"
    
    result = airtable.list_records(
        AIRTABLE_BASE_ID, 
        AIRTABLE_TABLE_ID,
        filterByFormula=filter_formula,
        sort="[{'field':'Datum','direction':'asc'}]"
    )
    
    records = result.get("records", [])
    print(f"\n📅 Newsletter-Themen diese Woche ({len(records)}):")
    
    for r in records:
        fields = r["fields"]
        print(f"  {fields.get('Datum')} - {fields.get('Name')} ({fields.get('Email Typ')})")


def update_status(record_id: str, new_status: str):
    """
    Beispiel: Status eines Newsletter-Themas updaten
    """
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    result = airtable.update_records(
        AIRTABLE_BASE_ID,
        AIRTABLE_TABLE_ID,
        [{"id": record_id, "fields": {"Status": new_status}}]
    )
    
    print(f"✅ Status updated: {result['records'][0]['fields'].get('Name')}")


if __name__ == "__main__":
    print("=" * 50)
    print("Notion ↔ Airtable Direkt-API Demo")
    print("=" * 50)
    
    # Beispiel: Schema anzeigen
    notion = NotionClient(NOTION_API_KEY)
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    print("\n1️⃣ Notion Database Schema:")
    db = notion.get_database(NOTION_DB_ID)
    print(f"   Titel: {db.get('title', [{}])[0].get('plain_text', 'N/A')}")
    print(f"   Properties: {list(db.get('properties', {}).keys())}")
    
    print("\n2️⃣ Airtable Schema:")
    schema = airtable.get_base_schema(AIRTABLE_BASE_ID)
    for table in schema.get("tables", []):
        if table["id"] == AIRTABLE_TABLE_ID:
            print(f"   Tabelle: {table['name']}")
            print(f"   Felder: {[f['name'] for f in table['fields']]}")
    
    print("\n" + "=" * 50)
    print("Nutze die Funktionen:")
    print("  - sync_notion_to_airtable()")
    print("  - get_weekly_topics()")
    print("  - update_status('recXXX', 'In Arbeit')")
    print("=" * 50)
