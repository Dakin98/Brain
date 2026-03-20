#!/usr/bin/env python3
import os
import json
import urllib.request
import http.server
import socketserver
import threading
import shutil
import time

AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tblmrFXGDWI4hYu46"
EXPORT_DIR = "/Users/denizakin/Downloads/Privat und Geteilt 2/eCom Email Calendar Kit/eCom Email Calendar"
SERVER_DIR = "/tmp/airtable_images"
SERVER_PORT = 8768

# Setup Server
os.makedirs(SERVER_DIR, exist_ok=True)
os.chdir(SERVER_DIR)

handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.daemon = True
thread.start()
print(f"✅ Server läuft auf http://localhost:{SERVER_PORT}")

# Nur 5 Einträge testen
test_names = ["Thanksgiving", "Cyber Monday", "Smile day", "Mother's Day", "Black Friday"]

for name in test_names:
    print(f"\n🖼️  {name}")
    
    # Record finden
    filter_formula = f"{{Name}}='{name}'"
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}?filterByFormula={urllib.request.quote(filter_formula)}"
    
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {AIRTABLE_KEY}"})
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            records = result.get("records", [])
            
            if not records:
                print("   ⚠️ Nicht gefunden")
                continue
            
            record = records[0]
            record_id = record["id"]
            
            # Check if already has uploads
            if record["fields"].get("Upload"):
                print("   ✅ Hat bereits Bilder")
                continue
            
            # Finde Bilder
            folder = os.path.join(EXPORT_DIR, name)
            if not os.path.isdir(folder):
                print("   ⚠️ Kein Ordner")
                continue
            
            images = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            if not images:
                print("   ℹ️ Keine Bilder")
                continue
            
            print(f"   📸 {len(images)} Bilder")
            
            # Kopiere und lade hoch
            urls = []
            for img in images[:5]:
                src = os.path.join(folder, img)
                dst_name = f"test_{name}_{img}".replace(' ', '_')
                dst = os.path.join(SERVER_DIR, dst_name)
                shutil.copy2(src, dst)
                urls.append(f"http://localhost:{SERVER_PORT}/{dst_name}")
            
            # Upload
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
                print("   ✅ HOCHGELADEN!")
                
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    time.sleep(1)

httpd.shutdown()
print("\n🎉 Fertig!")
