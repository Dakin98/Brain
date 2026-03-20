#!/usr/bin/env python3
"""
Start time tracking for a ClickUp task
"""
import argparse
import sys
sys.path.insert(0, '/Users/denizakin/.openclaw/workspace/skills/clickup/scripts')

from clickup_client import ClickUpClient

def main():
    parser = argparse.ArgumentParser(description='Start ClickUp timer')
    parser.add_argument('--team-id', required=True, help='Team ID')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--description', help='Time entry description')
    parser.add_argument('--billable', action='store_true', help='Mark as billable')
    
    args = parser.parse_args()
    
    try:
        client = ClickUpClient()
        
        result = client.start_timer(
            args.team_id,
            args.task_id,
            description=args.description,
            billable=args.billable
        )
        
        print("\n" + "="*60)
        print("✓ Timer started")
        print("="*60)
        print(f"Task ID: {args.task_id}")
        print(f"Started at: {result.get('data', {}).get('start', 'N/A')}")
        print()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()