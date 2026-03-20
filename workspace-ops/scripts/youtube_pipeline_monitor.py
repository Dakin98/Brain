#!/usr/bin/env python3
"""
YouTube Pipeline Status Monitor
Erstellt Drive-Ordner wenn Status = "Recording Prep"

Usage:
    python3 youtube_pipeline_monitor.py
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl
import subprocess

CLICKUP_BASE = "https://api.clickup.com/api/v2"
LIST_YOUTUBE = "901521521003"

def get_api_token():
    config_path = os.path.expanduser("~/.config/clickup/api_token")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return f.read().strip()
    return os.environ.get("CLICKUP_API_TOKEN")

def clickup_request(method, endpoint, data=None):
    headers = {
        "Authorization": get_api_token(),
        "Content-Type": "application/json"
    }
    url = f"{CLICKUP_BASE}{endpoint}"
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  ⚠️ Error {e.code}")
        return None

def get_tasks_by_status(list_id, status):
    """Get all tasks with specific status"""
    endpoint = f"/list/{list_id}/task?statuses%5B%5D={status.replace(' ', '%20').replace('🎬', '')}"
    return clickup_request("GET", endpoint)

def create_drive_folder(video_title):
    """Create Drive folder structure"""
    script_path = os.path.expanduser("~/.openclaw/workspace/scripts/create-content-drive.sh")
    
    try:
        result = subprocess.run(
            ["bash", script_path, video_title],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Extract OUTPUT_PATH
        for line in result.stdout.split('\n'):
            if line.startswith("OUTPUT_PATH:"):
                return line.replace("OUTPUT_PATH:", "").strip()
        
        return None
    except Exception as e:
        print(f"  ⚠️ Drive folder creation failed: {e}")
        return None

def add_comment(task_id, comment):
    """Add comment to task"""
    data = {"comment_text": comment, "notify_all": False}
    return clickup_request("POST", f"/task/{task_id}/comment", data)

def update_task_status(task_id, status):
    """Update task status"""
    return clickup_request("PUT", f"/task/{task_id}", {"status": status})

def check_and_process_recording_prep():
    """Check for tasks in 'Recording Prep' status and create drive folders"""
    
    print("🎬 Checking YouTube Pipeline for 'Recording Prep' tasks...")
    
    # Try different status name variations
    status_variations = ["recording prep", "🎬 recording prep", "Recording Prep", "🎬 Recording Prep"]
    
    tasks_found = []
    for status in status_variations:
        result = get_tasks_by_status(LIST_YOUTUBE, status)
        if result and result.get("tasks"):
            tasks_found.extend(result["tasks"])
    
    if not tasks_found:
        print("  No tasks waiting for Recording Prep.")
        return
    
    print(f"  Found {len(tasks_found)} task(s) to process")
    
    for task in tasks_found:
        task_id = task["id"]
        task_name = task["name"]
        
        print(f"\n  Processing: {task_name}")
        
        # Check if already processed (has drive comment)
        comments = clickup_request("GET", f"/task/{task_id}/comment")
        if comments:
            for comment in comments.get("comments", []):
                if "GOOGLE DRIVE" in comment.get("comment_text", ""):
                    print(f"    ⏭️ Already processed, skipping")
                    continue
        
        # Create Drive folder
        print(f"    📁 Creating Drive folder...")
        drive_path = create_drive_folder(task_name)
        
        if drive_path:
            # Add comment with drive info
            drive_comment = f"""## 📁 GOOGLE DRIVE ORDNER ERSTELLT

**Pfad:** `{drive_path}`

**Ordnerstruktur:**
```
2 Intern/Content Engine/
├── 01_RAW/YouTube_Recordings/{task_name.replace(' ', '_')}/
│   ├── Main_Take/
│   └── B_Roll/
├── 02_EDIT/Final_Videos/{task_name.replace(' ', '_')}/
│   ├── 4K_Master/
│   └── 1080p_Web/
├── 02_EDIT/Thumbnails/{task_name.replace(' ', '_')}/
│   ├── PSD_Source/
│   └── PNG_Export/
└── 03_ASSETS/Shorts/{task_name.replace(' ', '_')}/
    ├── Short_1/
    ├── Short_2/
    └── Short_3/
```

**✅ Nächster Schritt:** Status auf "Recording" setzen und aufnehmen!

*Template lokal unter: /tmp/content_engine_template/{task_name.replace(' ', '_')}/*
"""
            add_comment(task_id, drive_comment)
            print(f"    ✅ Drive folder created and comment added")
            
            # Update status to "Recording"
            update_task_status(task_id, "recording")
            print(f"    ✅ Status updated to 'recording'")
        else:
            print(f"    ❌ Failed to create drive folder")

def main():
    print("=" * 60)
    print("🎬 YouTube Pipeline Monitor — Drive Folder Automation")
    print("=" * 60)
    check_and_process_recording_prep()
    print("\n" + "=" * 60)
    print("✅ Check complete!")

if __name__ == "__main__":
    main()
