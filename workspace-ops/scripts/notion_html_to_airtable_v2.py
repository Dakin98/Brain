#!/usr/bin/env python3
"""
Notion HTML Export → Airtable (KORRIGIERT)
10er Batches mit Pausen
"""

import os
import csv
import json
import urllib.request
import http.server
import socketserver
import threading
import time
import re
from pathlib import Path

# API Key
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"

# Pfade
EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit"
CSV_FILE = os.path.join(EXPORT_DIR, "eCom Email Calendar 3465a32be5e04d52bec3c24ff39e1507.csv")
HTML_DIR = os.path.join(EXPORT_DIR, "eCom Email Calendar")

# Server für Bilder
SERVER_PORT = 8766
SERVER_URL = f"http://localhost:{SERVER_PORT}"
DOWNLOAD_DIR = "/tmp/notion_export_images"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


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
    
    def update_record(self, record_id: str, fields: dict) -> bool:
        try:
            data = {"records": [{"id": record_id, "fields": fields}]}
            self._request("PATCH", f"{BASE_ID}/{TABLE_ID}", data)
            return True
        except Exception as e:
            print(f"❌ Airtable Error: {e}")
            return False
    
    def find_record_by_name(self, name: str) -> str:
        try:
            # Suche exakt oder Teilweise
            filter_formula = f"{{Name}}='{name}'"
            url = f"{self.BASE_URL}/{BASE_ID}/{TABLE_ID}?filterByFormula={urllib.request.quote(filter_formula)}"
            
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}"})
            
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode())
                records = result.get("records", [])
                if records:
                    return records[0]["id"]
                
                # Wenn nicht gefunden, liste alle und suche manuell
                return self._manual_search(name)
        except Exception as e:
            return self._manual_search(name)
    
    def _manual_search(self, name: str) -> str:
        """Manuelle Suche durch alle Records"""
        try:
            all_records = []
            offset = None
            
            while True:
                url = f"{self.BASE_URL}/{BASE_ID}/{TABLE_ID}?pageSize=100"
                if offset:
                    url += f"&offset={offset}"
                
                req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}"})
                with urllib.request.urlopen(req) as resp:
                    result = json.loads(resp.read().decode())
                    all_records.extend(result.get("records", []))
                    offset = result.get("offset")
                    if not offset:
                        break
            
            # Suche nach Name (case-insensitive, partial match)
            name_lower = name.lower()
            for r in all_records:
                record_name = r["fields"].get("Name", "")
                if name_lower in record_name.lower() or record_name.lower() in name_lower:
                    return r["id"]
            
            return None
        except:
            return None
    
    def add_attachments_via_url(self, record_id: str, urls: list) -> bool:
        try:
            attachments = [{"url": url} for url in urls]
            data = {"records": [{"id": record_id, "fields": {"Upload": attachments}}]}
            self._request("PATCH", f"{BASE_ID}/{TABLE_ID}", data)
            return True
        except Exception as e:
            print(f"❌ Upload Error: {str(e)[:60]}")
            return False


def start_local_server():
    """Startet lokalen Server für Bilder"""
    os.chdir(DOWNLOAD_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
    
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    
    return httpd


def find_html_file(name: str) -> str:
    """Findet HTML-Datei für einen Eintrag"""
    # Format: "Name ID.html"
    for file in os.listdir(HTML_DIR):
        if file.endswith('.html') and file.startswith(name + ' '):
            return os.path.join(HTML_DIR, file)
    return None


def find_image_folder(name: str) -> str:
    """Findet Bilder-Ordner für einen Eintrag"""
    folder_path = os.path.join(HTML_DIR, name)
    if os.path.isdir(folder_path):
        return folder_path
    return None


def copy_images_to_server(folder_path: str, prefix: str) -> list:
    """Kopiert Bilder zum Server-Ordner und gibt URLs zurück"""
    import shutil
    
    urls = []
    if not folder_path or not os.path.exists(folder_path):
        return urls
    
    for img_file in os.listdir(folder_path):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            src = os.path.join(folder_path, img_file)
            dst_name = f"{prefix}_{img_file}".replace(' ', '_')
            dst = os.path.join(DOWNLOAD_DIR, dst_name)
            
            try:
                shutil.copy2(src, dst)
                urls.append(f"{SERVER_URL}/{dst_name}")
            except:
                pass
    
    return urls


def extract_text_from_html(html_path: str) -> str:
    """Extrahiert Text aus HTML"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Einfacher Text-Extraction
        text = re.sub('<[^<]+?>', ' ', html)
        # Entferne überflüssige Leerzeichen
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        # Limit für Airtable
        if len(text) > 50000:
            text = text[:50000] + "\n\n[Content truncated...]"
        
        return text
    except:
        return ""


def process_batch(airtable: AirtableClient, entries: list, batch_num: int, total_batches: int, server):
    """Verarbeitet einen Batch"""
    print(f"\n{'='*60}")
    print(f"📦 BATCH {batch_num}/{total_batches} ({len(entries)} Einträge)")
    print(f"{'='*60}\n")
    
    success_count = 0
    error_count = 0
    
    for i, entry in enumerate(entries, 1):
        name = entry['name']
        
        print(f"[{i}/{len(entries)}] {name[:50]}")
        
        # 1. Record finden
        record_id = airtable.find_record_by_name(name)
        if not record_id:
            print(f"   ⚠️ Nicht in Airtable gefunden")
            error_count += 1
            continue
        
        # 2. HTML-Datei finden
        html_file = find_html_file(name)
        
        # 3. Text extrahieren
        if html_file:
            text = extract_text_from_html(html_file)
            if text:
                if airtable.update_record(record_id, {"Notizen": text}):
                    print(f"   ✅ Text ({len(text)} chars)")
                else:
                    print(f"   ❌ Text-Update fehlgeschlagen")
        
        # 4. Bilder verarbeiten
        img_folder = find_image_folder(name)
        if img_folder:
            # Bilder zum Server kopieren
            prefix = name.replace(' ', '_')[:20]
            img_urls = copy_images_to_server(img_folder, prefix)
            
            if img_urls:
                print(f"   📸 {len(img_urls)} Bilder")
                
                # Zu Airtable hochladen
                if airtable.add_attachments_via_url(record_id, img_urls):
                    print(f"   ✅ Bilder hochgeladen")
                    success_count += 1
                else:
                    print(f"   ❌ Bilder-Upload fehlgeschlagen")
                    error_count += 1
            else:
                print(f"   ℹ️ Keine Bilder im Ordner")
                success_count += 1
        else:
            print(f"   ℹ️ Kein Bilder-Ordner")
            success_count += 1
        
        time.sleep(0.3)
    
    print(f"\n✅ Batch {batch_num} fertig: {success_count} OK, {error_count} Fehler")
    return success_count, error_count


def main():
    print("🚀 Notion HTML Export → Airtable")
    print("=" * 60)
    
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    # 1. CSV laden
    print("\n📂 Lade CSV...")
    entries = []
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if name:
                entries.append({
                    'name': name,
                    'date': row.get('Date', ''),
                    'email_type': row.get('Email Type', '')
                })
    
    print(f"✅ {len(entries)} Einträge gefunden")
    
    # 2. Server starten
    print("\n🌐 Starte lokalen Bilder-Server...")
    server = start_local_server()
    time.sleep(1)
    
    # 3. Batches verarbeiten
    BATCH_SIZE = 10
    total_batches = (len(entries) + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\n⏳ {total_batches} Batches à {BATCH_SIZE} Einträge")
    
    total_success = 0
    total_error = 0
    
    for batch_num in range(1, total_batches + 1):
        start_idx = (batch_num - 1) * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(entries))
        batch = entries[start_idx:end_idx]
        
        success, errors = process_batch(airtable, batch, batch_num, total_batches, server)
        total_success += success
        total_error += errors
        
        # Pause nach Batch
        if batch_num < total_batches:
            print(f"\n⏸️  PAUSE nach Batch {batch_num}")
            print(f"   Bisher: {total_success} OK, {total_error} Fehler")
            print(f"   Noch {total_batches - batch_num} Batches übrig")
            
            print("   ⏳ Warte 10 Sekunden... (Ctrl+C zum Abbruch)")
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                print("\n\n🛑 Abgebrochen")
                break
    
    server.shutdown()
    print(f"\n{'='*60}")
    print(f"🎉 FERTIG!")
    print(f"   Total: {total_success} OK, {total_error} Fehler")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
