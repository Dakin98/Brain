#!/usr/bin/env python3
"""
Notion HTML Export → Airtable (10er Schritte mit Pausen)
"""

import os
import csv
import json
import urllib.request
import base64
import time
import glob
from pathlib import Path
import sys

# API Key
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"

# Pfade
EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit"
CSV_FILE = os.path.join(EXPORT_DIR, "eCom Email Calendar 3465a32be5e04d52bec3c24ff39e1507.csv")
HTML_DIR = os.path.join(EXPORT_DIR, "eCom Email Calendar")


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
            data = {
                "records": [{
                    "id": record_id,
                    "fields": fields
                }]
            }
            self._request("PATCH", f"{BASE_ID}/{TABLE_ID}", data)
            return True
        except Exception as e:
            print(f"❌ Airtable Error: {e}")
            return False
    
    def find_record_by_name(self, name: str) -> str:
        """Findet Record ID anhand des Namens"""
        try:
            # URL-encode den Namen für die Filter-Formel
            filter_formula = f"{{Name}}='{name.replace(chr(39), chr(92)+chr(39))}'"
            url = f"{self.BASE_URL}/{BASE_ID}/{TABLE_ID}?filterByFormula={urllib.request.quote(filter_formula)}"
            
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {self.api_key}"
            })
            
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode())
                records = result.get("records", [])
                if records:
                    return records[0]["id"]
        except Exception as e:
            print(f"❌ Find Error: {e}")
        return None


def parse_html_content(html_path: str) -> tuple:
    """Liest HTML-Datei und extrahiert Text + Bilder"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except:
        return "", []
    
    # Einfacher Text-Extraction (zwischen <body> und </body>)
    text_parts = []
    images = []
    
    # Suche nach Bildern im HTML
    # Notion Export hat Bilder als <img src="...">
    import re
    
    # Text extrahieren (einfache Version)
    # Entferne HTML-Tags
    text = re.sub('<[^<]+?>', '', html)
    # Entferne überflüssige Leerzeilen
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    
    # Bilder suchen
    img_pattern = r'<img[^>]+src="([^"]+)"'
    img_matches = re.findall(img_pattern, html)
    
    # Bild-Pfade auflösen
    html_dir = os.path.dirname(html_path)
    for img_src in img_matches:
        if not img_src.startswith('http'):
            # Lokaler Pfad
            full_path = os.path.join(html_dir, img_src)
            if os.path.exists(full_path):
                images.append(full_path)
    
    # Auch nach Bildern im gleichen Ordner suchen (Notion Struktur)
    folder_name = os.path.splitext(os.path.basename(html_path))[0]
    # Ordner ohne ID-Teil
    folder_base = folder_name.rsplit(' ', 1)[0] if ' ' in folder_name else folder_name
    
    # Suche nach Ordner mit ähnlichem Namen
    for item in os.listdir(html_dir):
        item_path = os.path.join(html_dir, item)
        if os.path.isdir(item_path) and folder_base in item:
            # Bilder im Ordner finden
            for img_file in os.listdir(item_path):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    img_path = os.path.join(item_path, img_file)
                    if img_path not in images:
                        images.append(img_path)
    
    return text, images


def upload_image_to_airtable(airtable: AirtableClient, record_id: str, image_path: str) -> bool:
    """Lädt ein Bild zu einem Airtable Record hoch"""
    try:
        # Bild als Base64 kodieren
        with open(image_path, 'rb') as f:
            content = f.read()
        
        filename = os.path.basename(image_path)
        b64_content = base64.b64encode(content).decode('utf-8')
        
        data = {
            "records": [{
                "id": record_id,
                "fields": {
                    "Upload": [{"filename": filename, "content": b64_content}]
                }
            }]
        }
        
        airtable._request("PATCH", f"{BASE_ID}/{TABLE_ID}", data)
        return True
        
    except Exception as e:
        print(f"❌ Upload Error: {e}")
        return False


def process_batch(airtable: AirtableClient, entries: list, batch_num: int, total_batches: int):
    """Verarbeitet einen Batch von 10 Einträgen"""
    print(f"\n{'='*60}")
    print(f"📦 BATCH {batch_num}/{total_batches} ({len(entries)} Einträge)")
    print(f"{'='*60}\n")
    
    success_count = 0
    error_count = 0
    
    for i, entry in enumerate(entries, 1):
        name = entry['name']
        date = entry['date']
        email_type = entry['email_type']
        html_file = entry['html_file']
        
        print(f"[{i}/{len(entries)}] {name[:50]}")
        
        # 1. Record in Airtable finden
        record_id = airtable.find_record_by_name(name)
        if not record_id:
            print(f"   ⚠️ Nicht in Airtable gefunden")
            error_count += 1
            continue
        
        # 2. HTML parsen
        if html_file and os.path.exists(html_file):
            text, images = parse_html_content(html_file)
            
            # 3. Notizen updaten (mit Content)
            if text:
                # Truncieren falls zu lang (Airtable Limit: 100k Zeichen)
                if len(text) > 50000:
                    text = text[:50000] + "\n\n[Content truncated...]"
                
                success = airtable.update_record(record_id, {"Notizen": text})
                if success:
                    print(f"   ✅ Text ({len(text)} chars)")
                else:
                    print(f"   ❌ Text failed")
            
            # 4. Bilder hochladen (max 10 pro Record)
            if images:
                print(f"   📸 {len(images)} Bilder")
                uploaded = 0
                for img_path in images[:10]:  # Max 10 Bilder
                    if upload_image_to_airtable(airtable, record_id, img_path):
                        uploaded += 1
                    time.sleep(0.2)  # Kurze Pause zwischen Bildern
                print(f"   ✅ {uploaded}/{len(images[:10])} Bilder hochgeladen")
            else:
                print(f"   ℹ️  Keine Bilder")
            
            success_count += 1
        else:
            print(f"   ⚠️ HTML nicht gefunden: {html_file}")
            error_count += 1
        
        time.sleep(0.5)  # Pause zwischen Records
    
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
            name = row.get('Name') or row.get('name', '')
            date = row.get('Date') or row.get('date', '')
            email_type = row.get('Email Type') or row.get('email_type', '')
            
            if not name:
                print(f"   ⚠️ Überspringe Eintrag ohne Name")
                continue
            
            # HTML-Datei finden
            html_file = None
            # Suche nach Datei die mit dem Namen beginnt
            for file in os.listdir(HTML_DIR):
                if file.endswith('.html') and file.startswith(name):
                    html_file = os.path.join(HTML_DIR, file)
                    break
            
            entries.append({
                'name': name,
                'date': date,
                'email_type': email_type,
                'html_file': html_file
            })
    
    print(f"✅ {len(entries)} Einträge gefunden")
    
    # 2. In Batches von 10 verarbeiten
    BATCH_SIZE = 10
    total_batches = (len(entries) + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\n⏳ Werde {total_batches} Batches à {BATCH_SIZE} Einträge verarbeiten")
    print("💡 Nach jedem Batch wird pausiert")
    
    total_success = 0
    total_error = 0
    
    for batch_num in range(1, total_batches + 1):
        start_idx = (batch_num - 1) * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(entries))
        batch = entries[start_idx:end_idx]
        
        # Batch verarbeiten
        success, errors = process_batch(airtable, batch, batch_num, total_batches)
        total_success += success
        total_error += errors
        
        # Pause nach Batch (außer letzter)
        if batch_num < total_batches:
            print(f"\n⏸️  PAUSE nach Batch {batch_num}")
            print(f"   Bisher: {total_success} OK, {total_error} Fehler")
            input("   ⏎ Enter drücken für nächsten Batch...")
    
    # Fertig
    print(f"\n{'='*60}")
    print(f"🎉 FERTIG!")
    print(f"   Total: {total_success} OK, {total_error} Fehler")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
