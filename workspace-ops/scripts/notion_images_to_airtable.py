#!/usr/bin/env python3
"""
Notion Bilder → Airtable Attachments (MIT LOKALEM SERVER)
1. Lade Bilder herunter
2. Starte lokalen HTTP Server
3. Sende lokale URLs zu Airtable
4. Airtable lädt von lokalem Server
"""

import os
import json
import urllib.request
import http.server
import socketserver
import threading
from typing import List, Dict
import sys
import time

# API Keys (aus Umgebungsvariablen)
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "YOUR_NOTION_API_KEY_HERE")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")

# IDs
NOTION_DB_ID = "3465a32b-e5e0-4d52-bec3-c24ff39e1507"
AIRTABLE_BASE_ID = "appbGhxy9I18oIS8E"
AIRTABLE_TABLE_ID = "tblmrFXGDWI4hYu46"

# Download folder
DOWNLOAD_DIR = "/tmp/notion_images"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Server config
SERVER_PORT = 8765
SERVER_URL = f"http://localhost:{SERVER_PORT}"


class NotionClient:
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
    
    def query_database(self, database_id: str, start_cursor: str = None) -> dict:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        return self._request("POST", f"databases/{database_id}/query", payload)
    
    def get_block_children(self, block_id: str) -> List[dict]:
        all_blocks = []
        cursor = None
        
        while True:
            url = f"{self.BASE_URL}/blocks/{block_id}/children?page_size=100"
            if cursor:
                url += f"&start_cursor={cursor}"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": "2022-06-28"
            }
            req = urllib.request.Request(url, headers=headers)
            
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode())
                    blocks = result.get("results", [])
                    all_blocks.extend(blocks)
                    
                    if not result.get("has_more"):
                        break
                    cursor = result.get("next_cursor")
            except:
                break
        
        return all_blocks
    
    def download_image(self, url: str, filename: str) -> str:
        """Lädt ein Bild herunter"""
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            })
            
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            
            return filepath
        except Exception as e:
            return None


class AirtableClient:
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
    
    def add_attachments_via_url(self, base_id: str, table_id: str, record_id: str, field_name: str, urls: List[str]) -> bool:
        """Fügt Attachments via URL hinzu (Airtable lädt dann selbst herunter)"""
        try:
            attachments = [{"url": url} for url in urls]
            
            data = {
                "records": [{
                    "id": record_id,
                    "fields": {
                        field_name: attachments
                    }
                }]
            }
            
            result = self._request("PATCH", f"{base_id}/{table_id}", data)
            return True
        except Exception as e:
            print(f"\n      ❌ Upload failed: {str(e)[:60]}")
            return False


def get_fresh_image_urls(notion: NotionClient, page_id: str) -> List[Dict]:
    """Holt frische Bild-URLs direkt von der Notion API"""
    blocks = notion.get_block_children(page_id)
    images = []
    
    for block in blocks:
        if block.get("type") == "image":
            img_data = block["image"]
            url = img_data.get("external", {}).get("url") or img_data.get("file", {}).get("url")
            
            if url:
                ext = "jpg"
                if "/" in url:
                    original = url.split("/")[-1].split("?")[0]
                    if "." in original:
                        ext = original.split(".")[-1][:4]
                
                filename = f"{page_id}_{len(images)}.{ext}"
                
                images.append({
                    "url": url,
                    "filename": filename
                })
    
    return images


def start_local_server():
    """Startet einen lokalen HTTP Server für die Bilder"""
    os.chdir(DOWNLOAD_DIR)
    
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
    
    print(f"\n🌐 Lokaler Server gestartet auf {SERVER_URL}")
    print(f"   Serving files from: {DOWNLOAD_DIR}\n")
    
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    return httpd


def sync_images_to_airtable():
    """Hauptfunktion"""
    notion = NotionClient(NOTION_API_KEY)
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    print("🖼️  Starte Bilder-Sync: Notion → Airtable")
    print("=" * 60)
    
    # 1. Alle Airtable Records holen
    print("\n1️⃣ Lade Airtable Records...")
    airtable_records = []
    offset = None
    
    while True:
        url = f"{airtable.BASE_URL}/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}?pageSize=100"
        if offset:
            url += f"&offset={offset}"
        
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {airtable.api_key}"})
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            airtable_records.extend(result.get("records", []))
            offset = result.get("offset")
            if not offset:
                break
    
    notion_to_airtable = {
        r["fields"].get("Notion ID"): {"id": r["id"], "name": r["fields"].get("Name", "Unbekannt")}
        for r in airtable_records
        if r["fields"].get("Notion ID")
    }
    
    print(f"   ✅ {len(airtable_records)} Records gefunden")
    
    # 2. Alle Notion Einträge holen
    print("\n2️⃣ Lade Notion Database...")
    all_notion_entries = []
    cursor = None
    
    while True:
        result = notion.query_database(NOTION_DB_ID, start_cursor=cursor)
        all_notion_entries.extend(result.get("results", []))
        
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    
    print(f"   ✅ {len(all_notion_entries)} Notion Einträge gefunden")
    
    # 3. Lokaler Server starten
    server = start_local_server()
    time.sleep(1)  # Server Zeit zum Starten geben
    
    # 4. Für jede Page Bilder extrahieren und hochladen
    print(f"3️⃣ Lade Bilder herunter und sende zu Airtable...")
    print("=" * 60)
    
    total_images = 0
    uploaded_images = 0
    errors = 0
    
    for i, entry in enumerate(all_notion_entries, 1):
        page_id = entry["id"]
        props = entry.get("properties", {})
        
        name_data = props.get("Name", {}).get("title", [])
        name = name_data[0].get("plain_text", "Unbekannt") if name_data else "Unbekannt"
        
        # Progress
        progress = int((i / len(all_notion_entries)) * 100)
        print(f"\n[{progress:3d}%] {i:3d}/{len(all_notion_entries)} - {name[:45]}")
        
        # Airtable Record finden
        at_record = notion_to_airtable.get(page_id)
        if not at_record:
            print("   ⚠️ Kein Airtable Record gefunden")
            continue
        
        # Bilder holen
        images = get_fresh_image_urls(notion, page_id)
        
        if not images:
            print("   ℹ️  Keine Bilder")
            continue
        
        total_images += len(images)
        print(f"   📸 {len(images)} Bilder gefunden")
        
        # Bilder herunterladen
        local_urls = []
        for img_idx, img in enumerate(images, 1):
            print(f"      [{img_idx}/{len(images)}] Download: {img['filename'][:40]}...", end=" ")
            sys.stdout.flush()
            
            filepath = notion.download_image(img["url"], img["filename"])
            
            if filepath and os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                print(f"✅ ({file_size} bytes)")
                # Lokale URL erstellen
                local_url = f"{SERVER_URL}/{img['filename']}"
                local_urls.append(local_url)
            else:
                print("❌")
                errors += 1
        
        # Zu Airtable hochladen (batch für alle Bilder dieser Page)
        if local_urls:
            print(f"      Upload zu Airtable...", end=" ")
            sys.stdout.flush()
            
            success = airtable.add_attachments_via_url(
                AIRTABLE_BASE_ID,
                AIRTABLE_TABLE_ID,
                at_record["id"],
                "Upload",
                local_urls
            )
            
            if success:
                print("✅")
                uploaded_images += len(local_urls)
            else:
                print("❌")
                errors += len(local_urls)
        
        # Kurze Pause
        time.sleep(0.3)
    
    print()
    print("=" * 60)
    print(f"✅ FERTIG!")
    print(f"   • Gesamt Bilder: {total_images}")
    print(f"   • Hochgeladen: {uploaded_images}")
    print(f"   • Fehler: {errors}")
    print("=" * 60)
    
    # Server stoppen
    server.shutdown()
    print("\n🛑 Lokaler Server gestoppt")


if __name__ == "__main__":
    sync_images_to_airtable()
