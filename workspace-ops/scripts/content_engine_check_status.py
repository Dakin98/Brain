#!/usr/bin/env python3
"""
Content Engine Status Checker
Checks ClickUp for tasks with "Claude Generate" status and triggers generator
Used as cron fallback if webhook fails
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl
import subprocess

CLICKUP_BASE = "https://api.clickup.com/api/v2"
LIST_CONTENT_IDEAS = "901521521000"

def get_api_token():
    config_path = os.path.expanduser("~/.config/clickup/api_token")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return f.read().strip()
    return os.environ.get("CLICKUP_API_TOKEN")

def clickup_request(endpoint):
    headers = {"Authorization": get_api_token()}
    url = f"{CLICKUP_BASE}{endpoint}"
    req = urllib.request.Request(url, headers=headers)
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code}")
        return None

def get_tasks_by_status(list_id, status):
    """Get all tasks with specific status"""
    endpoint = f"/list/{list_id}/task?statuses%5B%5D={status.replace(' ', '%20')}"
    return clickup_request(endpoint)

def trigger_generation(task_id):
    """Trigger content generation for task"""
    script_path = os.path.expanduser("~/.openclaw/workspace-ops/scripts/content_engine_generator_v2.py")
    result = subprocess.run(
        ["python3", script_path, "--task-id", task_id],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print(f"[{os.path.basename(__file__)}] Checking for 'claude generate' tasks...")
    
    # Get tasks waiting for generation
    tasks = get_tasks_by_status(LIST_CONTENT_IDEAS, "claude generate")
    
    if not tasks or not tasks.get("tasks"):
        print("No tasks waiting for generation.")
        return
    
    print(f"Found {len(tasks['tasks'])} task(s) to process")
    
    for task in tasks["tasks"]:
        task_id = task["id"]
        task_name = task["name"]
        
        print(f"Processing: {task_name} ({task_id})")
        
        success, stdout, stderr = trigger_generation(task_id)
        
        if success:
            print(f"✅ Successfully generated content for: {task_name}")
        else:
            print(f"❌ Failed to generate content for: {task_name}")
            print(f"Error: {stderr}")

if __name__ == "__main__":
    main()
