#!/usr/bin/env python3
"""
Bilder Upload - Schritt für Schritt mit Fortschritt
"""

import os
import json
import urllib.request
import http.server
import socketserver
import threading
import shutil
import time
import sys

AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"
EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit/eCom Email Calendar"
SERVER_DIR = "/tmp/airtable_images2"
SERVER_PORT = 8769

print("="*60)
print("🚀 BILDER UPLOAD ZU AIRTABLE")
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

# Lade alle Records (mit Progress)
print("📥 Lade Airtable Records...")
records = []
offset = None
count = 0

while True:
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}?pageSize=100"
    if offset:
        url += f"&offset={offset}"
    
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {AIRTABLE_KEY}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        batch = result.get("records", [])
        records.extend(batch)
        count += len(batch)
        print(f"   ... {count} Records geladen", end="\r")
        sys.stdout.flush()
        
        offset = result.get("offset")
        if not offset:
            break

print(f"\n✅ {len(records)} Records geladen")

# Filter: Nur ohne Uploads
todo = [r for r in records if not r["fields"].get("Upload")]
print(f"⏳ {len(todo)} brauchen Bilder\n")

if not todo:
    print("🎉 Alle Records haben bereits Bilder!")
    httpd.shutdown()
    exit(0)

# Verarbeite in Batches
BATCH_SIZE = 5
success_count = 0
error_count = 0

for i, record in enumerate(todo):
    name = record["fields"].get("Name", "Unbekannt")
    record_id = record["id"]
    progress = int(((i+1) / len(todo)) * 100)
    
    print(f"[{progress:3d}%] {i+1}/{len(todo)}: {name[:40]}")
    
    # Finde Bilder
    folder = os.path.join(EXPORT_DIR, name)
    if not os.path.isdir(folder):
        print("      ⚠️ Kein Ordner")
        error_count += 1
        continue
    
    images = [f for f in os.listdir(folder) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    
    if not images:
        print("      ℹ️ Keine Bilder")
        continue
    
    # Kopiere Bilder
    urls = []
    for img in images[:10]:
        src = os.path.join(folder, img)
        safe_name = f"{i}_{img}".replace(' ', '_').replace('/', '_')
        dst = os.path.join(SERVER_DIR, safe_name)
        try:
            shutil.copy2(src, dst)
            urls.append(f"http://localhost:{SERVER_PORT}/{safe_name}")
        except:
            pass
    
    if not urls:
        print("      ⚠️ Konnte Bilder nicht kopieren")
        error_count += 1
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
        
        with urllib.request.urlopen(req) as resp:
            print(f"      ✅ {len(urls)} Bilder hochgeladen")
            success_count += 1
            
    except Exception as e:
        print(f"      ❌ Upload fehlgeschlagen: {str(e)[:40]}")
        error_count += 1
    
    # Pause alle 5
    if (i + 1) % BATCH_SIZE == 0 and i < len(todo) - 1:
        print(f"\n⏸️  Pause... (Ctrl+C zum Stoppen)\n")
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Gestoppt")
            break

httpd.shutdown()

print("\n" + "="*60)
print("🎉 FERTIG!")
print(f"   Erfolgreich: {success_count}")
print(f"   Fehler: {error_count}")
print("="*60)
