#!/bin/bash
# Notion/Airtable direkte API CLI Tools
# Nutzung: source notion_airtable_cli.sh

NOTION_KEY="${NOTION_API_KEY:-YOUR_NOTION_API_KEY_HERE}"
AIRTABLE_KEY="${AIRTABLE_API_KEY:-YOUR_AIRTABLE_API_KEY_HERE}"
AIRTABLE_BASE="appbGhxy9I18oIS8E"
EMAIL_TABLE="tblmrFXGDWI4hYu46"

# 📧 Diese Woche anzeigen
email-this-week() {
    local today=$(date +%Y-%m-%d)
    local next_week=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d "+7 days" +%Y-%m-%d)
    
    echo "📅 Newsletter-Themen bis $next_week:"
    echo ""
    
    python3 << EOF
import urllib.request, json

url = "https://api.airtable.com/v0/$AIRTABLE_BASE/$EMAIL_TABLE"
headers = {"Authorization": "Bearer $AIRTABLE_KEY"}

# Alle holen und filtern
all_records = []
offset = None
while True:
    req_url = url + "?sort[0][field]=Datum&sort[0][direction]=asc"
    if offset:
        req_url += f"&offset={offset}"
    
    req = urllib.request.Request(req_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        all_records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break

# Filtern
from datetime import datetime
today = datetime.strptime("$today", "%Y-%m-%d")
next_week = datetime.strptime("$next_week", "%Y-%m-%d")

for r in all_records:
    f = r["fields"]
    date_str = f.get("Datum")
    if date_str:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        if today <= d <= next_week:
            status = f.get("Status", "Idee")
            icon = "⬜"
            if status == "Fertig":
                icon = "✅"
            elif status == "In Arbeit":
                icon = "🔄"
            print(f"{icon} {date_str} | {f.get('Name', 'N/A')[:40]:40} | {f.get('Email Typ', 'N/A')}")
EOF
}

# 🔍 In Email Calendar suchen
email-search() {
    local query="$1"
    [ -z "$query" ] && { echo "Usage: email-search <suchbegriff>"; return 1; }
    
    python3 << EOF
import urllib.request, json

url = "https://api.airtable.com/v0/$AIRTABLE_BASE/$EMAIL_TABLE"
headers = {"Authorization": "Bearer $AIRTABLE_KEY"}

# Filter formula
filter_by = f"FIND(LOWER('$query'), LOWER({{Name}}))"
req_url = url + f"?filterByFormula={urllib.request.quote(filter_by)}"

req = urllib.request.Request(req_url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        records = data.get("records", [])
        print(f"🔍 {len(records)} Ergebnisse für '$query':")
        print()
        for r in records:
            f = r["fields"]
            print(f"  {f.get('Datum', 'N/A')} | {f.get('Name', 'N/A')} ({f.get('Email Typ', 'N/A')})")
except urllib.error.HTTPError as e:
    print(f"Error: {e.read().decode()}")
EOF
}

# 📊 Statistiken anzeigen
email-stats() {
    python3 << EOF
import urllib.request, json
from collections import Counter

url = "https://api.airtable.com/v0/$AIRTABLE_BASE/$EMAIL_TABLE"
headers = {"Authorization": "Bearer $AIRTABLE_KEY"}

all_records = []
offset = None
while True:
    req_url = url + "?pageSize=100"
    if offset:
        req_url += f"&offset={offset}"
    
    req = urllib.request.Request(req_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        all_records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break

print(f"📧 Email Calendar Statistiken")
print(f"{'='*40}")
print(f"Gesamt: {len(all_records)} Newsletter-Themen")
print()

# Nach Typ
types = Counter(r["fields"].get("Email Typ", "Unbekannt") for r in all_records)
print("Nach Typ:")
for t, count in types.most_common():
    bar = "█" * (count // 2)
    print(f"  {t:15} {count:3} {bar}")

print()

# Nach Status
statuses = Counter(r["fields"].get("Status", "Idee") for r in all_records)
print("Nach Status:")
for s, count in statuses.most_common():
    icon = "⬜"
    if s == "Fertig": icon = "✅"
    elif s == "In Arbeit": icon = "🔄"
    elif s == "Gesendet": icon = "📤"
    print(f"  {icon} {s:15} {count}")
EOF
}

# ✏️ Status updaten
email-status() {
    local record_id="$1"
    local new_status="$2"
    
    [ -z "$record_id" ] && { echo "Usage: email-status <record_id> <status>"; return 1; }
    [ -z "$new_status" ] && { echo "Status required: Idee, Geplant, In Arbeit, Fertig, Gesendet"; return 1; }
    
    python3 << EOF
import urllib.request, json

url = f"https://api.airtable.com/v0/$AIRTABLE_BASE/$EMAIL_TABLE"
headers = {
    "Authorization": "Bearer $AIRTABLE_KEY",
    "Content-Type": "application/json"
}

data = json.dumps({
    "records": [{"id": "$record_id", "fields": {"Status": "$new_status"}}]
}).encode()

req = urllib.request.Request(url, data=data, method="PATCH", headers=headers)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    name = result["records"][0]["fields"].get("Name", "Unbekannt")
    print(f"✅ '{name}' → Status: $new_status")
EOF
}

# 📝 Notion-Inhalte anzeigen
notion-content() {
    local page_id="$1"
    [ -z "$page_id" ] && { echo "Usage: notion-content <page_id>"; return 1; }
    
    python3 << EOF
import urllib.request, json

url = f"https://api.notion.com/v1/blocks/$page_id/children"
headers = {
    "Authorization": "Bearer $NOTION_KEY",
    "Notion-Version": "2022-06-28"
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode())
    
    print("📝 Notion Page Content:")
    print()
    
    for block in data.get("results", []):
        block_type = block.get("type")
        
        if block_type == "paragraph":
            text = "".join(t.get("plain_text", "") for t in block["paragraph"].get("rich_text", []))
            if text:
                print(text)
        
        elif block_type == "bulleted_list_item":
            text = "".join(t.get("plain_text", "") for t in block["bulleted_list_item"].get("rich_text", []))
            print(f"  • {text}")
        
        elif block_type == "numbered_list_item":
            text = "".join(t.get("plain_text", "") for t in block["numbered_list_item"].get("rich_text", []))
            print(f"  1. {text}")
        
        elif block_type == "heading_1":
            text = "".join(t.get("plain_text", "") for t in block["heading_1"].get("rich_text", []))
            print(f"\n# {text}")
        
        elif block_type == "heading_2":
            text = "".join(t.get("plain_text", "") for t in block["heading_2"].get("rich_text", []))
            print(f"\n## {text}")
        
        elif block_type == "image":
            img_url = block["image"].get("external", {}).get("url") or block["image"].get("file", {}).get("url")
            if img_url:
                print(f"  [Bild: {img_url[:60]}...]")
EOF
}

echo "✅ Notion/Airtable CLI Tools geladen!"
echo ""
echo "Verfügbare Befehle:"
echo "  email-this-week    - Diese Woche anstehende Newsletter"
echo "  email-search <q>   - Im Calendar suchen"
echo "  email-stats        - Statistiken anzeigen"
echo "  email-status <id> <status> - Status ändern"
echo "  notion-content <id> - Notion Page Content anzeigen"
