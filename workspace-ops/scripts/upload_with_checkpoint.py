#!/usr/bin/env python3
"""
Bilder Upload mit Checkpoint
- Verarbeitet einen Record nach dem anderen
- Speichert Fortschritt in Datei
- Kann nach Abbruch weiter machen
"""

import os
import json
import urllib.request
import http.server
import socketserver
import threading
import shutil
import time

# Config
AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"
EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit/eCom Email Calendar"
SERVER_DIR = "/tmp/airtable_img_server"
SERVER_PORT = 8770
CHECKPOINT_FILE = "/tmp/upload_checkpoint.json"

print("="*60)
print("🚀 BILDER UPLOAD MIT CHECKPOINT")
print("="*60)

# Setup Server
os.makedirs(SERVER_DIR, exist_ok=True)
os.chdir(SERVER_DIR)
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.daemon = True
thread.start()
print(f"✅ Server läuft auf http://localhost:{SERVER_PORT}\n")

# Lade Checkpoint
completed = set()
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, 'r') as f:
        completed = set(json.load(f))
    print(f"📂 Checkpoint geladen: {len(completed)} bereits erledigt")

# Lade Records
def get_all_records():
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

print("📥 Lade Airtable Records...")
all_records = get_all_records()
print(f"✅ {len(all_records)} Records geladen\n")

# Filter: Records ohne Bilder und noch nicht erledigt
todo = [
    r for r in all_records 
    if not r["fields"].get("Upload") and r["id"] not in completed
]

print(f"⏳ {len(todo)} Records zu verarbeiten\n")

if not todo:
    print("🎉 Alles erledigt!")
    httpd.shutdown()
    exit(0)

# Verarbeite einen nach dem anderen
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
    
    # Kopiere Bilder
    urls = []
    for img in images[:10]:
        src = os.path.join(folder, img)
        safe = f"{i}_{img}".replace(' ', '_')
        dst = os.path.join(SERVER_DIR, safe)
        try:
            shutil.copy2(src, dst)
            urls.append(f"http://localhost:{SERVER_PORT}/{safe}")
        except:
            pass
    
    if not urls:
        print("      ⚠️ Kopieren fehlgeschlagen")
        continue
    
    # Upload
    try:
        data = {
            "records": [{
                "id": record_id,
                "fields": {"Upload": [{"url": u} for u in urls]}
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
            print(f"      ✅ {len(urls)} Bilder hochgeladen")
            completed.add(record_id)
            
            # Checkpoint speichern
            with open(CHECKPOINT_FILE, 'w') as f:
                json.dump(list(completed), f)
                
    except Exception as e:
        print(f"      ❌ Fehler: {str(e)[:40]}")
    
    # Pause
    if i < len(todo):
        time.sleep(2)

httpd.shutdown()
print(f"\n{'='*60}")
print("🎉 FERTIG!")
print(f"   Erledigt: {len(completed)}/{len(all_records)}")
print(f"{'='*60}")
