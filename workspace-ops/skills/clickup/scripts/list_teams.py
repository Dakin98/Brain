#!/usr/bin/env python3
"""
List all ClickUp teams/workspaces
"""
import json
import sys
sys.path.insert(0, '/Users/denizakin/.openclaw/workspace/skills/clickup/scripts')

from clickup_client import ClickUpClient

def main():
    try:
        client = ClickUpClient()
        teams = client.list_teams()
        
        print("\n" + "="*60)
        print("ClickUp Teams/Workspaces")
        print("="*60 + "\n")
        
        for team in teams.get('teams', []):
            print(f"📁 {team['name']}")
            print(f"   ID: {team['id']}")
            print(f"   Members: {len(team.get('members', []))}")
            if team.get('color'):
                print(f"   Color: {team['color']}")
            print()
        
        print(f"Total teams: {len(teams.get('teams', []))}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()