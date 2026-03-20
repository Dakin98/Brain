#!/usr/bin/env python3
"""
Nur Bilder hochladen - Schritt für Schritt
"""

import os
import json
import urllib.request
import http.server
import socketserver
import threading
import time
import shutil

AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"

EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit/eCom Email Calendar"
SERVER_DIR = "/tmp/airtable_images"
SERVER_PORT = 8767

# Setup
os.makedirs(SERVER_DIR, exist_ok=True)
os.chdir(SERVER_DIR)

# Starte Server
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.daemon = True
thread.start()
print(f"🌐 Server läuft auf http://localhost:{SERVER_PORT}")
time.sleep(1)

# Lade alle Airtable Records
print("\n📥 Lade Airtable Records...")
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

print(f"✅ {len(records)} Records geladen")

# Filter: Nur Records ohne Uploads
todo = [r for r in records if not r["fields"].get("Upload")]
print(f"⏳ {len(todo)} ohne Bilder")

# Verarbeite in Batches von 5
BATCH_SIZE = 5
total = len(todo)

for i in range(0, total, BATCH_SIZE):
    batch = todo[i:i+BATCH_SIZE]
    batch_num = (i // BATCH_SIZE) + 1
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\n{'='*50}")
    print(f"📦 Batch {batch_num}/{total_batches}")
    print(f"{'='*50}")
    
    for record in batch:
        name = record["fields"].get("Name", "Unbekannt")
        record_id = record["id"]
        
        print(f"\n🖼️  {name[:45]}")
        
        # Suche Ordner mit Bildern
        folder_path = os.path.join(EXPORT_DIR, name)
        if not os.path.isdir(folder_path):
            print("   ⚠️ Kein Ordner")
            continue
        
        # Finde Bilder
        images = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if not images:
            print("   ℹ️ Keine Bilder")
            continue
        
        print(f"   📸 {len(images)} Bilder gefunden")
        
        # Kopiere Bilder zu Server und sammle URLs
        urls = []
        for img in images[:10]:  # Max 10
            src = os.path.join(folder_path, img)
            safe_name = f"{name[:20]}_{img}".replace(' ', '_').replace('/', '_')
            dst = os.path.join(SERVER_DIR, safe_name)
            
            try:
                shutil.copy2(src, dst)
                urls.append(f"http://localhost:{SERVER_PORT}/{safe_name}")
            except Exception as e:
                print(f"   ❌ Kopieren fehlgeschlagen: {e}")
        
        if not urls:
            continue
        
        # Lade zu Airtable hoch
        print(f"   ⬆️  Lade hoch...", end=" ")
        try:
            attachments = [{"url": url} for url in urls]
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
            
            with urllib.request.urlopen(req) as resp:
                print("✅")
                
        except Exception as e:
            print(f"❌ {str(e)[:50]}")
    
    # Pause
    if i + BATCH_SIZE < total:
        print(f"\n⏸️  PAUSE - Warte 10 Sekunden...")
        time.sleep(10)

httpd.shutdown()
print(f"\n{'='*50}")
print("🎉 FERTIG!")
print(f"{'='*50}")
