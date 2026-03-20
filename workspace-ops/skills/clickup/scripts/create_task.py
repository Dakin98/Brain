#!/usr/bin/env python3
"""
Create a new task in ClickUp
"""
import argparse
import json
import sys
sys.path.insert(0, '/Users/denizakin/.openclaw/workspace/skills/clickup/scripts')

from clickup_client import ClickUpClient, datetime_to_timestamp
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Create a ClickUp task')
    parser.add_argument('--list-id', required=True, help='List ID to create task in')
    parser.add_argument('--name', required=True, help='Task name')
    parser.add_argument('--description', help='Task description')
    parser.add_argument('--assignees', help='Comma-separated user IDs')
    parser.add_argument('--due-date', help='Due date (YYYY-MM-DD)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--priority', choices=['1', '2', '3', '4'], help='Priority (1=urgent, 4=low)')
    parser.add_argument('--tags', help='Comma-separated tags')
    parser.add_argument('--status', help='Initial status')
    parser.add_argument('--notify-all', action='store_true', help='Notify all assignees')
    
    args = parser.parse_args()
    
    try:
        client = ClickUpClient()
        
        # Build task data
        task_data = {
            "name": args.name
        }
        
        if args.description:
            task_data["description"] = args.description
        
        if args.assignees:
            task_data["assignees"] = [int(a.strip()) for a in args.assignees.split(',')]
        
        if args.due_date:
            dt = datetime.strptime(args.due_date, "%Y-%m-%d")
            task_data["due_date"] = datetime_to_timestamp(dt)
            task_data["due_date_time"] = False
        
        if args.start_date:
            dt = datetime.strptime(args.start_date, "%Y-%m-%d")
            task_data["start_date"] = datetime_to_timestamp(dt)
            task_data["start_date_time"] = False
        
        if args.priority:
            task_data["priority"] = int(args.priority)
        
        if args.tags:
            task_data["tags"] = [t.strip() for t in args.tags.split(',')]
        
        if args.status:
            task_data["status"] = args.status
        
        task_data["notify_all"] = args.notify_all
        
        # Create task
        task = client.create_task(args.list_id, args.name, **task_data)
        
        print("\n" + "="*60)
        print("✓ Task created successfully")
        print("="*60)
        print(f"Name: {task['name']}")
        print(f"ID: {task['id']}")
        print(f"URL: {task.get('url', 'N/A')}")
        
        if task.get('assignees'):
            print(f"Assignees: {', '.join(str(a['id']) for a in task['assignees'])}")
        
        if task.get('due_date'):
            due = datetime.fromtimestamp(task['due_date'] / 1000)
            print(f"Due: {due.strftime('%Y-%m-%d')}")
        
        if task.get('priority'):
            priority_map = {1: 'urgent', 2: 'high', 3: 'normal', 4: 'low'}
            print(f"Priority: {priority_map.get(task['priority'], 'unknown')}")
        
        print()
        
        # Output JSON for piping
        print(json.dumps(task))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()