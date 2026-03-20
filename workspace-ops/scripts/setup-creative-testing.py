#!/usr/bin/env python3
"""
ClickUp API Helper - Create Folders and Lists for Creative Testing Structure
"""

import requests
import json
import sys
import os

API_TOKEN = os.environ.get("CLICKUP_API_TOKEN") or open(os.path.expanduser("~/.config/clickup/api_token")).read().strip()
BASE_URL = "https://api.clickup.com/api/v2"

headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

def create_folder(space_id, name):
    """Create a folder in a space"""
    url = f"{BASE_URL}/space/{space_id}/folder"
    payload = {"name": name}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Folder created: {name} (ID: {data.get('id')})")
        return data.get('id')
    elif response.status_code == 400 and "name already exists" in response.text.lower():
        print(f"⚠️  Folder '{name}' already exists")
        # Try to find existing folder ID
        folders = list_folders(space_id)
        for f in folders:
            if f.get('name') == name:
                return f.get('id')
    else:
        print(f"❌ Error creating folder: {response.text}")
        return None

def create_list(folder_id, name, content=""):
    """Create a list in a folder"""
    url = f"{BASE_URL}/folder/{folder_id}/list"
    payload = {
        "name": name,
        "content": content
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ List created: {name} (ID: {data.get('id')})")
        return data.get('id')
    elif response.status_code == 400 and "name already exists" in response.text.lower():
        print(f"⚠️  List '{name}' already exists")
        return None
    else:
        print(f"❌ Error creating list: {response.text}")
        return None

def list_folders(space_id):
    """List all folders in a space"""
    url = f"{BASE_URL}/space/{space_id}/folder"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('folders', [])
    return []

def list_lists(folder_id):
    """List all lists in a folder"""
    url = f"{BASE_URL}/folder/{folder_id}/list"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('lists', [])
    return []

def main():
    # Configuration
    space_id = "90040311585"  # Delivery Space
    
    # Client folder names where we need to add Creative Testing
    clients = [
        "Green Cola Germany",
        "schnelleinfachgesund", 
        "Ferro Berlin",
        "RAZECO",
        "ATB Bau"
    ]
    
    print("🚀 Setting up Creative Testing Structure in ClickUp")
    print("=" * 60)
    print()
    
    # First, get all folders in the Delivery space
    print("📁 Finding client folders...")
    folders = list_folders(space_id)
    
    for client in clients:
        print(f"\n🔍 Looking for: {client}")
        
        # Find the client folder
        client_folder = None
        for f in folders:
            if f.get('name') == client:
                client_folder = f
                break
        
        if not client_folder:
            print(f"⚠️  Folder '{client}' not found. Skipping...")
            continue
        
        folder_id = client_folder.get('id')
        print(f"   Found folder ID: {folder_id}")
        
        # Create Creative Testing subfolder
        print(f"\n   Creating 'Creative Testing' subfolder...")
        ct_folder_id = create_folder(folder_id, "Creative Testing")
        
        if ct_folder_id:
            # Create the three lists
            print(f"   Creating lists...")
            create_list(ct_folder_id, "Creative Pipeline", "Aktive Creative Tests")
            create_list(ct_folder_id, "Creative Archive", "Abgeschlossene Tests")
            create_list(ct_folder_id, "Creative Ideas", "Creative Ideen & Konzepte")
    
    print("\n" + "=" * 60)
    print("✅ Setup complete!")

if __name__ == "__main__":
    main()
