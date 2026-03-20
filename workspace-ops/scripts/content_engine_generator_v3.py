#!/usr/bin/env python3
"""
Content Engine Generator v3 — With Drive Folder Integration
Generiert Content + erstellt automatisch Drive-Ordnerstruktur

Usage:
    python3 content_engine_generator_v3.py --task-id "TASK_ID"
"""

import os
import sys
import json
import subprocess
import re

# Import the v2 generator functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_engine_generator_v2 import (
    ClickUpClient, ContentGeneratorV2, generate_content_v2,
    LIST_CONTENT_IDEAS, LIST_YOUTUBE, LIST_SHORTS,
    LIST_LINKEDIN, LIST_NEWSLETTER
)

def create_drive_folder(video_title):
    """Create Drive folder structure for video"""
    script_path = os.path.expanduser("~/.openclaw/workspace/scripts/create-content-drive.sh")
    
    try:
        result = subprocess.run(
            ["bash", script_path, video_title],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Extract OUTPUT_PATH from script output
        output = result.stdout
        for line in output.split('\n'):
            if line.startswith("OUTPUT_PATH:"):
                return line.replace("OUTPUT_PATH:", "").strip()
        
        return f"2 Intern/Content Engine/02_EDIT/Final_Videos/{video_title.replace(' ', '_')}"
    except Exception as e:
        print(f"  ⚠️ Drive folder creation failed: {e}")
        return None

def generate_content_with_drive(task_id=None, manual_input=None):
    """Generate content and create Drive folder"""
    
    # Get task info first
    clickup = ClickUpClient()
    
    if task_id:
        task = clickup.get_task(task_id)
        topic = task.get("name", "")
    else:
        topic = manual_input.get("title", "Content Topic")
    
    print(f"🎬 Generating content for: {topic}")
    print("=" * 60)
    
    # Step 1: Generate content
    print("\n1️⃣ Generating content with Brand Voice...")
    content = generate_content_v2(task_id=task_id, manual_input=manual_input)
    
    # Step 2: Create Drive folder
    print("\n2️⃣ Creating Drive folder structure...")
    drive_path = create_drive_folder(topic)
    
    if drive_path:
        print(f"   ✅ Drive folder: {drive_path}")
        
        # Add Drive path to content
        content['drive_path'] = drive_path
        
        # Add Drive info to ClickUp comment
        drive_info = f"""
## 📁 GOOGLE DRIVE ORDNER

**Pfad:** `{drive_path}`

**Struktur:**
```
2 Intern/Content Engine/
├── 01_RAW/YouTube_Recordings/{topic.replace(' ', '_')}/
├── 02_EDIT/Final_Videos/{topic.replace(' ', '_')}/
├── 03_ASSETS/Shorts/{topic.replace(' ', '_')}/
└── 04_ARCHIVE/Published/{topic.replace(' ', '_')}/
```

**Next Steps:**
1. RAW Aufnahmen in `01_RAW` ablegen
2. Edit in `02_EDIT`
3. Assets in `03_ASSETS`
4. Nach Publish: Alles in `04_ARCHIVE`

*Template lokal erstellt unter: /tmp/content_engine_template/*
"""
    else:
        drive_info = "\n## 📁 GOOGLE DRIVE\n\n*Drive folder creation skipped*\n"
    
    # Step 3: Post to ClickUp
    print("\n3️⃣ Posting to ClickUp...")
    
    if task_id:
        # Post content comments
        clickup.add_comment(task_id, content['youtube'])
        
        for post_type, post_content in content['linkedin'].items():
            clickup.add_comment(task_id, post_content)
        
        clickup.add_comment(task_id, content['newsletter'])
        
        shorts_content = "# 📱 SHORTS STRATEGIE\n\n"
        for short_key, short_data in content['shorts'].items():
            shorts_content += f"""## {short_data['title']}
**Timestamp:** {short_data['timestamp']}
**Hook:** {short_data['hook_text']}
**Caption:** {short_data['caption']}

---

"""
        clickup.add_comment(task_id, shorts_content)
        
        # Post Drive info
        clickup.add_comment(task_id, drive_info)
        
        # Summary
        summary = f"""✅ **CONTENT GENERATION COMPLETE v3**

**Topic:** {content['topic']}
**Pillar:** {content['pillar']}
**Drive Path:** {drive_path or 'N/A'}

**Generated:**
- 🎬 YouTube Script (10-15 min)
- 💼 3 LinkedIn Posts
- 📧 Newsletter Draft  
- 📱 3 Shorts Strategy
- 📁 Drive Folder Structure

**Next Steps:**
1. Review content in comments above
2. Create Drive folders (see comment)
3. Saturday: Record video
4. Follow-up tasks created automatically
"""
        clickup.add_comment(task_id, summary)
        print("   ✅ All content posted to ClickUp")
    
    # Step 4: Create follow-up tasks
    print("\n4️⃣ Creating follow-up tasks...")
    from content_engine_generator_v2 import create_follow_up_tasks
    from datetime import datetime
    create_follow_up_tasks(LIST_CONTENT_IDEAS, content['topic'], content)
    print("   ✅ Follow-up tasks created")
    
    # Step 5: Update task status
    print("\n5️⃣ Updating task status...")
    try:
        clickup.update_task_status(task_id, "done")
        print("   ✅ Status updated to 'done'")
    except:
        print("   ⚠️ Status update failed (status may not exist)")
    
    print("\n" + "=" * 60)
    print("✅ Content Engine v3 Complete!")
    print(f"📁 Drive: {drive_path}")
    print("=" * 60)
    
    return content

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Content Engine Generator v3")
    parser.add_argument("--task-id", help="ClickUp task ID")
    parser.add_argument("--manual", action="store_true", help="Manual mode")
    parser.add_argument("--title", help="Content title")
    parser.add_argument("--pillar", default="tutorials", help="Content pillar")
    parser.add_argument("--audience", default="ecom", help="Target audience")
    parser.add_argument("--keywords", help="Comma-separated keywords")
    
    args = parser.parse_args()
    
    if args.manual:
        manual_input = {
            "title": args.title or "Meta Ads Content",
            "pillar": args.pillar,
            "audience": args.audience,
            "keywords": args.keywords.split(",") if args.keywords else []
        }
        content = generate_content_with_drive(manual_input=manual_input)
        print(json.dumps({k: str(v)[:200] for k, v in content.items()}, indent=2))
    elif args.task_id:
        generate_content_with_drive(task_id=args.task_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
