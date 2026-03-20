#!/usr/bin/env python3
"""
Notion Page Content → Airtable Migration (Verbesserte Version)
Mit Progress-Reporting und Error-Handling
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Optional
from datetime import datetime
import sys

# API Keys (aus Umgebungsvariablen)
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "YOUR_NOTION_API_KEY_HERE")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")

# IDs
NOTION_DB_ID = "3465a32b-e5e0-4d52-bec3-c24ff39e1507"
AIRTABLE_BASE_ID = "appbGhxy9I18oIS8E"
AIRTABLE_TABLE_ID = "tblmrFXGDWI4hYu46"


class NotionClient:
    """Direkter Notion API Client"""
    
    BASE_URL = "https://api.notion.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.request_count = 0
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            method=method,
            headers=headers
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                self.request_count += 1
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            print(f"\n❌ HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
            raise
    
    def query_database(self, database_id: str, page_size: int = 100, start_cursor: str = None) -> dict:
        payload = {"page_size": page_size}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        return self._request("POST", f"databases/{database_id}/query", payload)
    
    def get_block_children(self, block_id: str, max_depth: int = 10) -> List[dict]:
        """Holt alle Child-Blocks einer Page (mit Tiefe-Limit)"""
        all_blocks = []
        cursor = None
        
        while True:
            url = f"{self.BASE_URL}/blocks/{block_id}/children?page_size=100"
            if cursor:
                url += f"&start_cursor={cursor}"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": "2022-06-28"
            }
            req = urllib.request.Request(url, headers=headers)
            
            try:
                with urllib.request.urlopen(req) as response:
                    self.request_count += 1
                    result = json.loads(response.read().decode())
                    blocks = result.get("results", [])
                    
                    for block in blocks:
                        all_blocks.append(block)
                        # Nur bis zu 3 Level tief gehen (toggles, etc.)
                        if block.get("has_children") and max_depth > 1:
                            try:
                                children = self.get_block_children(block["id"], max_depth - 1)
                                block["children"] = children
                            except:
                                pass
                    
                    if not result.get("has_more"):
                        break
                    cursor = result.get("next_cursor")
            except urllib.error.HTTPError:
                break
        
        return all_blocks


class AirtableClient:
    """Direkter Airtable API Client"""
    
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
    
    def update_records(self, base_id: str, table_id: str, records: List[dict]) -> dict:
        return self._request("PATCH", f"{base_id}/{table_id}", {"records": records})


def extract_text_from_rich_text(rich_text: List[dict]) -> str:
    """Extrahiert plain text aus Notion rich_text"""
    return "".join(t.get("plain_text", "") for t in rich_text)


def format_block_to_markdown(block: dict, level: int = 0) -> str:
    """Konvertiert einen Notion Block zu Markdown"""
    block_type = block.get("type")
    indent = "  " * level
    
    try:
        if block_type == "paragraph":
            text = extract_text_from_rich_text(block["paragraph"].get("rich_text", []))
            return f"{indent}{text}\n" if text else ""
        
        elif block_type == "heading_1":
            text = extract_text_from_rich_text(block["heading_1"].get("rich_text", []))
            return f"\n{indent}# {text}\n\n"
        
        elif block_type == "heading_2":
            text = extract_text_from_rich_text(block["heading_2"].get("rich_text", []))
            return f"\n{indent}## {text}\n\n"
        
        elif block_type == "heading_3":
            text = extract_text_from_rich_text(block["heading_3"].get("rich_text", []))
            return f"\n{indent}### {text}\n\n"
        
        elif block_type == "bulleted_list_item":
            text = extract_text_from_rich_text(block["bulleted_list_item"].get("rich_text", []))
            return f"{indent}• {text}\n"
        
        elif block_type == "numbered_list_item":
            text = extract_text_from_rich_text(block["numbered_list_item"].get("rich_text", []))
            return f"{indent}1. {text}\n"
        
        elif block_type == "quote":
            text = extract_text_from_rich_text(block["quote"].get("rich_text", []))
            return f"{indent}> {text}\n"
        
        elif block_type == "callout":
            text = extract_text_from_rich_text(block["callout"].get("rich_text", []))
            emoji = block["callout"].get("icon", {}).get("emoji", "💡")
            return f"\n{indent}{emoji} **{text}**\n\n"
        
        elif block_type == "divider":
            return f"\n{indent}---\n"
        
        elif block_type == "image":
            img_data = block["image"]
            url = img_data.get("external", {}).get("url") or img_data.get("file", {}).get("url")
            caption = extract_text_from_rich_text(img_data.get("caption", []))
            if url:
                return f"\n{indent}![{caption}]({url})\n"
            return ""
        
        elif block_type == "video":
            video_data = block["video"]
            url = video_data.get("external", {}).get("url") or video_data.get("file", {}).get("url")
            if url:
                return f"\n{indent}[Video: {url}]\n"
            return ""
        
        elif block_type == "toggle":
            text = extract_text_from_rich_text(block["toggle"].get("rich_text", []))
            result = f"\n{indent}▶ **{text}**\n"
            for child in block.get("children", []):
                result += format_block_to_markdown(child, level + 1)
            return result
        
        elif block_type == "to_do":
            text = extract_text_from_rich_text(block["to_do"].get("rich_text", []))
            checked = "✅" if block["to_do"].get("checked") else "⬜"
            return f"{indent}{checked} {text}\n"
        
        elif block_type == "code":
            text = extract_text_from_rich_text(block["code"].get("rich_text", []))
            language = block["code"].get("language", "")
            return f"\n```{language}\n{text}\n```\n"
        
        elif block_type == "bookmark":
            bookmark_data = block.get("bookmark", {})
            url = bookmark_data.get("url", "")
            return f"\n[Bookmark: {url}]\n" if url else ""
        
        else:
            return ""
    
    except Exception as e:
        return f"\n[Error parsing {block_type}: {str(e)}]\n"


def extract_page_content(notion: NotionClient, page_id: str) -> dict:
    """Extrahiert kompletten Content einer Notion Page"""
    try:
        blocks = notion.get_block_children(page_id)
    except:
        return {"markdown": "", "images": [], "block_count": 0}
    
    markdown_content = []
    image_urls = []
    
    for block in blocks:
        md = format_block_to_markdown(block)
        if md:
            markdown_content.append(md)
        
        # Bilder sammeln
        if block.get("type") == "image":
            img_data = block["image"]
            url = img_data.get("external", {}).get("url") or img_data.get("file", {}).get("url")
            if url:
                caption = extract_text_from_rich_text(img_data.get("caption", []))
                image_urls.append({"url": url, "caption": caption})
    
    return {
        "markdown": "".join(markdown_content).strip(),
        "images": image_urls,
        "block_count": len(blocks)
    }


def sync_content_to_airtable(verbose: bool = True):
    """Holt alle Notion Pages und speichert Content in Airtable"""
    notion = NotionClient(NOTION_API_KEY)
    airtable = AirtableClient(AIRTABLE_API_KEY)
    
    print("🔄 Starte Content-Sync: Notion → Airtable")
    print("=" * 60)
    
    # 1. Alle Airtable Records holen (mit Pagination)
    print("\n1️⃣ Lade Airtable Records...")
    airtable_records = []
    offset = None
    
    while True:
        url = f"{airtable.BASE_URL}/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}?pageSize=100"
        if offset:
            url += f"&offset={offset}"
        
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {airtable.api_key}"})
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            airtable_records.extend(result.get("records", []))
            offset = result.get("offset")
            if not offset:
                break
    
    # Mapping: Notion ID → Airtable Record ID
    notion_to_airtable = {
        r["fields"].get("Notion ID"): r["id"]
        for r in airtable_records
        if r["fields"].get("Notion ID")
    }
    
    print(f"   ✅ {len(airtable_records)} Airtable Records gefunden\n")
    
    # 2. Alle Notion Einträge holen
    print("2️⃣ Lade Notion Database...")
    all_notion_entries = []
    cursor = None
    while True:
        result = notion.query_database(NOTION_DB_ID, start_cursor=cursor)
        all_notion_entries.extend(result.get("results", []))
        
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    
    print(f"   ✅ {len(all_notion_entries)} Notion Einträge gefunden\n")
    
    # 3. Content für jede Page extrahieren und nach Airtable syncen
    print(f"3️⃣ Extrahiere Content aus {len(all_notion_entries)} Pages...")
    print("   (Dies kann mehrere Minuten dauern...)")
    print()
    
    updated = 0
    skipped = 0
    errors = 0
    batch = []
    
    for i, entry in enumerate(all_notion_entries, 1):
        page_id = entry["id"]
        props = entry.get("properties", {})
        
        # Name auslesen
        name_data = props.get("Name", {}).get("title", [])
        name = name_data[0].get("plain_text", "Unbekannt") if name_data else "Unbekannt"
        
        # Progress: alle 20 Pages
        if i % 20 == 0 or i == 1:
            progress = int((i / len(all_notion_entries)) * 100)
            print(f"   [{progress:3d}%] {i:3d}/{len(all_notion_entries)} - {name[:50]:<50}")
            sys.stdout.flush()
        
        # Airtable Record ID finden
        airtable_id = notion_to_airtable.get(page_id)
        if not airtable_id:
            skipped += 1
            continue
        
        # Content extrahieren
        try:
            content = extract_page_content(notion, page_id)
            
            # Notizen vorbereiten
            notes = content["markdown"]
            
            # Bilder anhängen
            if content["images"]:
                notes += "\n\n---\n\n**📸 Bilder:**\n"
                for img in content["images"]:
                    notes += f"\n• {img['url']}"
                    if img["caption"]:
                        notes += f" _{img['caption']}_"
            
            # Update-Request vorbereiten (Batch)
            batch.append({
                "id": airtable_id,
                "fields": {"Notizen": notes}
            })
            
            # Alle 10 Records flushen
            if len(batch) >= 10:
                airtable.update_records(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID, batch)
                updated += len(batch)
                batch = []
            
        except Exception as e:
            errors += 1
    
    # Restliche Records updaten
    if batch:
        airtable.update_records(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID, batch)
        updated += len(batch)
    
    print()
    print("=" * 60)
    print(f"✅ FERTIG!")
    print(f"   • Erfolgreich: {updated}")
    print(f"   • Übersprungen: {skipped}")
    print(f"   • Fehler: {errors}")
    print(f"   • API Requests: {notion.request_count}")
    print("=" * 60)


if __name__ == "__main__":
    import time
    start = time.time()
    sync_content_to_airtable()
    elapsed = time.time() - start
    print(f"\n⏱️  Dauer: {elapsed:.1f} Sekunden")
