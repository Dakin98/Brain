#!/bin/bash
# Fetch this week's newsletter topics from Notion eCom Email Calendar
# Maps 2023 dates to current year by matching month+day to current week
# Output: JSON array of newsletter entries for this week

set -e

NOTION_KEY=$(cat ~/.config/notion/api_key)
DS_ID="f973c96b-5659-4fd8-97c2-63984dbd89d9"

# Get current week bounds (Monday to Sunday)
WEEK_START=$(date -v-monday "+%m-%d" 2>/dev/null || date -d "last monday" "+%m-%d")
TODAY_DOW=$(date "+%u")  # 1=Mon, 7=Sun

# Calculate this week's date range in MM-DD
python3 << 'PYEOF'
import urllib.request, json, os, sys
from datetime import datetime, timedelta

NOTION_KEY = os.environ.get("NOTION_KEY_OVERRIDE") or open(os.path.expanduser("~/.config/notion/api_key")).read().strip()
DS_ID = "f973c96b-5659-4fd8-97c2-63984dbd89d9"

today = datetime.now()
# Monday of this week
monday = today - timedelta(days=today.weekday())
sunday = monday + timedelta(days=6)

print(f"📅 Woche: {monday.strftime('%d.%m.')} – {sunday.strftime('%d.%m.%Y')}", file=sys.stderr)

# Fetch ALL entries from Notion (paginate)
all_entries = []
has_more = True
start_cursor = None

while has_more:
    body = {"page_size": 100}
    if start_cursor:
        body["start_cursor"] = start_cursor
    
    req = urllib.request.Request(
        f"https://api.notion.com/v1/data_sources/{DS_ID}/query",
        data=json.dumps(body).encode(),
        method="POST"
    )
    req.add_header("Authorization", f"Bearer {NOTION_KEY}")
    req.add_header("Notion-Version", "2025-09-03")
    req.add_header("Content-Type", "application/json")
    
    resp = json.loads(urllib.request.urlopen(req).read())
    all_entries.extend(resp.get("results", []))
    has_more = resp.get("has_more", False)
    start_cursor = resp.get("next_cursor")

print(f"📊 {len(all_entries)} Einträge total in Notion", file=sys.stderr)

# Match entries by month+day to this week
week_entries = []
for entry in all_entries:
    props = entry["properties"]
    date_prop = props.get("Date", {}).get("date")
    if not date_prop or not date_prop.get("start"):
        continue
    
    entry_date = datetime.strptime(date_prop["start"], "%Y-%m-%d")
    # Map to current year, match against this week
    try:
        mapped = entry_date.replace(year=today.year)
    except ValueError:
        continue  # Feb 29 in non-leap year
    
    if monday.date() <= mapped.date() <= sunday.date():
        name = "".join([t["plain_text"] for t in props.get("Name", {}).get("title", [])])
        types = [s["name"] for s in props.get("Email Type", {}).get("multi_select", [])]
        
        # Fetch page content (bullet points, etc.)
        page_id = entry["id"]
        try:
            creq = urllib.request.Request(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
            )
            creq.add_header("Authorization", f"Bearer {NOTION_KEY}")
            creq.add_header("Notion-Version", "2025-09-03")
            blocks = json.loads(urllib.request.urlopen(creq).read())
            
            content_lines = []
            for b in blocks.get("results", []):
                bt = b["type"]
                if bt in ("paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "quote"):
                    text = "".join([r["plain_text"] for r in b.get(bt, {}).get("rich_text", [])])
                    if text.strip():
                        prefix = "• " if bt == "bulleted_list_item" else ""
                        content_lines.append(f"{prefix}{text}")
                elif bt == "callout":
                    text = "".join([r["plain_text"] for r in b.get("callout", {}).get("rich_text", [])])
                    if text.strip():
                        content_lines.append(f"💡 {text}")
            
            content = "\n".join(content_lines)
        except Exception as e:
            content = ""
            print(f"  ⚠️ Could not fetch content for '{name}': {e}", file=sys.stderr)
        
        week_entries.append({
            "name": name,
            "date": mapped.strftime("%Y-%m-%d"),
            "original_date": date_prop["start"],
            "types": types,
            "content": content,
            "page_id": page_id
        })
        print(f"  ✅ {mapped.strftime('%d.%m.')} | {name} | {types}", file=sys.stderr)

if not week_entries:
    print("ℹ️ Keine Newsletter-Themen für diese Woche gefunden.", file=sys.stderr)

# Sort by date
week_entries.sort(key=lambda x: x["date"])
print(json.dumps(week_entries, ensure_ascii=False))
PYEOF
