#!/usr/bin/env python3
"""
Bilder Upload mit Base64 Encoding
Funktioniert ohne externen Server
"""

import os
import json
import urllib.request
import base64
import time

# Config
AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"
EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit/eCom Email Calendar"
CHECKPOINT_FILE = "/tmp/upload_checkpoint_v2.json"

print("="*60)
print("🚀 BILDER UPLOAD (Base64)")
print("="*60)

# Lade Checkpoint
completed = set()
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, 'r') as f:
        completed = set(json.load(f))
    print(f"📂 Checkpoint: {len(completed)} erledigt\n")

# Lade Records
def get_records():
    records = []
    offset = None
    while True:
        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}?pageSize=100"
        if offset:
            url += f"&offset={offset}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {AIRTABLE_KEY}"})
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            records.extend(result.get("records", []))
            offset = result.get("offset")
            if not offset:
                break
    return records

print("📥 Lade Records...")
all_records = get_records()
print(f"✅ {len(all_records)} Records\n")

# Filter
todo = [r for r in all_records if not r["fields"].get("Upload") and r["id"] not in completed]
print(f"⏳ {len(todo)} zu verarbeiten\n")

if not todo:
    print("🎉 Alles erledigt!")
    exit(0)

# Verarbeite
for i, record in enumerate(todo, 1):
    name = record["fields"].get("Name", "Unbekannt")
    record_id = record["id"]
    
    print(f"[{i}/{len(todo)}] {name[:45]}")
    
    # Finde Bilder
    folder = os.path.join(EXPORT_DIR, name)
    if not os.path.isdir(folder):
        print("      ⚠️ Kein Ordner")
        completed.add(record_id)
        continue
    
    images = [f for f in os.listdir(folder) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    
    if not images:
        print("      ℹ️ Keine Bilder")
        completed.add(record_id)
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump(list(completed), f)
        continue
    
    # Lade Bilder als Base64
    attachments = []
    for img in images[:10]:
        img_path = os.path.join(folder, img)
        try:
            with open(img_path, 'rb') as f:
                content = f.read()
            b64 = base64.b64encode(content).decode('utf-8')
            attachments.append({"filename": img, "content": b64})
        except Exception as e:
            print(f"      ⚠️ Fehler bei {img}: {e}")
    
    if not attachments:
        print("      ❌ Keine Bilder konnten geladen werden")
        continue
    
    # Upload
    try:
        data = {
            "records": [{
                "id": record_id,
                "fields": {"Upload": attachments}
            }]
        }
        
        req = urllib.request.Request(
            f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}",
            data=json.dumps(data).encode(),
            method="PATCH",
            headers={
                "Authorization": f"Bearer {AIRTABLE_KEY}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(req):
            print(f"      ✅ {len(attachments)} Bilder")
            completed.add(record_id)
            
            # Checkpoint
            with open(CHECKPOINT_FILE, 'w') as f:
                json.dump(list(completed), f)
                
    except Exception as e:
        print(f"      ❌ Upload fehlgeschlagen: {str(e)[:50]}")
    
    # Pause
    time.sleep(1)

print(f"\n{'='*60}")
print("🎉 FERTIG!")
print(f"   Erledigt: {len(completed)}/{len(all_records)}")
print(f"{'='*60}")
