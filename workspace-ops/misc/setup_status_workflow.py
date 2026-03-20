#!/usr/bin/env python3
"""
ClickUp Status Workflow Setup für Creative Pipeline
"""

import urllib.request
import json
import time

API_TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
LIST_ID = "901521337307"

def create_status(status_name, color, status_type="open"):
    """Erstellt einen Status"""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/status"
    
    data = {
        "status_name": status_name,
        "color": color,
        "type": status_type
    }
    
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"err": str(e)}

print("🚀 Erstelle Status-Workflow für Creative Pipeline...\n")

statuses = [
    ("💡 Idee", "#9b59b6"),
    ("📋 Konzept", "#3498db"),
    ("🎬 Produktion", "#f39c12"),
    ("👁️ Review", "#e74c3c"),
    ("🧪 Live Test", "#1abc9c"),
    ("📊 Analyse", "#34495e"),
    ("✅ Winner", "#2ecc71"),
    ("🔁 Iterieren", "#e67e22"),
    ("❌ Loser", "#95a5a6"),
    ("📦 Archiv", "#7f8c8d"),
]

for status_name, color in statuses:
    print(f"📍 Erstelle: {status_name}...")
    result = create_status(status_name, color)
    if "err" in result:
        print(f"   ❌ {result['err']}")
    else:
        print(f"   ✅ {result.get('status', status_name)}")
    time.sleep(0.5)

print("\n✅ Status-Workflow fertig!")
