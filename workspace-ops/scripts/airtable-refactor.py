#!/usr/bin/env python3
"""
Airtable Refactor Script
Migriert Daten aus Klaviyo Accounts + Stripe Kunden → Kunden Tabelle
Löscht dann die redundanten Tabellen
"""

import requests
import json
import sys
import time

# CONFIG - Hier deinen Airtable API Token eintragen
AIRTABLE_TOKEN = os.environ.get("AIRTABLE_API_KEY", "YOUR_AIRTABLE_API_KEY_HERE")
BASE_ID = "appbGhxy9I18oIS8E"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

def get_table_schema():
    """Get all tables and their fields"""
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def create_field(table_id, name, field_type, options=None):
    """Create a new field in a table"""
    url = f"https://api.airtable.com/v0/meta/tables/{table_id}/fields"
    data = {"name": name, "type": field_type}
    if options:
        data["options"] = options
    
    resp = requests.post(url, headers=HEADERS, json=data)
    if resp.status_code == 200:
        print(f"  ✓ Created field: {name}")
        return resp.json()
    elif resp.status_code == 422 and "already exists" in resp.text.lower():
        print(f"  ℹ Field exists: {name}")
        return None
    else:
        print(f"  ✗ Error creating {name}: {resp.status_code} - {resp.text[:200]}")
        return None

def get_records(table_id, filter_formula=None):
    """Get all records from a table"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_id}"
    params = {}
    if filter_formula:
        params["filterByFormula"] = filter_formula
    
    records = []
    while True:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        records.extend(data.get("records", []))
        
        if not data.get("offset"):
            break
        params["offset"] = data["offset"]
    
    return records

def update_record(table_id, record_id, fields):
    """Update a record"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_id}/{record_id}"
    data = {"fields": fields}
    resp = requests.patch(url, headers=HEADERS, json=data)
    if resp.status_code == 200:
        return True
    else:
        print(f"    ✗ Update failed: {resp.status_code} - {resp.text[:200]}")
        return False

def migrate_stripe_data(kunden_table_id, stripe_kunden_table_id):
    """Migrate Stripe data to Kunden table"""
    print("\n📊 Migrating Stripe Kunden data...")
    
    # Get all Stripe Kunden records
    stripe_records = get_records(stripe_kunden_table_id)
    print(f"  Found {len(stripe_records)} Stripe Kunden records")
    
    migrated = 0
    for stripe_rec in stripe_records:
        fields = stripe_rec.get("fields", {})
        
        # Get linked Kunde
        linked_kunden = fields.get("Kunde", [])
        if not linked_kunden:
            print(f"  ⚠ Stripe record {fields.get('Titel')} has no linked Kunde")
            continue
        
        kunde_id = linked_kunden[0]
        
        # Prepare data to migrate
        update_fields = {}
        if fields.get("Stripe Subscription ID"):
            update_fields["Stripe Subscription ID"] = fields["Stripe Subscription ID"]
        if fields.get("Abo-Status"):
            update_fields["Stripe Abo-Status"] = fields["Abo-Status"]
        if fields.get("Monatlicher Betrag"):
            update_fields["Stripe Monatlicher Betrag"] = fields["Monatlicher Betrag"]
        
        if update_fields:
            if update_record(kunden_table_id, kunde_id, update_fields):
                migrated += 1
                print(f"  ✓ Migrated {fields.get('Titel', 'Unknown')}")
        else:
            print(f"  ℹ No data to migrate for {fields.get('Titel', 'Unknown')}")
        
        time.sleep(0.2)  # Rate limiting
    
    print(f"\n  Total migrated: {migrated}/{len(stripe_records)}")
    return migrated

def migrate_klaviyo_data(kunden_table_id, klaviyo_table_id):
    """Migrate Klaviyo data to Kunden table"""
    print("\n📧 Migrating Klaviyo Accounts data...")
    
    klaviyo_records = get_records(klaviyo_table_id)
    print(f"  Found {len(klaviyo_records)} Klaviyo records")
    
    migrated = 0
    for klav_rec in klaviyo_records:
        fields = klaviyo_rec.get("fields", {})
        
        linked_kunden = fields.get("Kunde", [])
        if not linked_kunden:
            print(f"  ⚠ Klaviyo record {fields.get('Titel')} has no linked Kunde")
            continue
        
        kunde_id = linked_kunden[0]
        
        update_fields = {}
        if fields.get("API Key"):
            update_fields["Klaviyo API Key"] = fields["API Key"]
        # Note: Klaviyo Segments Done is already in Kunden
        
        if update_fields:
            if update_record(kunden_table_id, kunde_id, update_fields):
                migrated += 1
                print(f"  ✓ Migrated {fields.get('Titel', 'Unknown')}")
        
        time.sleep(0.2)
    
    print(f"\n  Total migrated: {migrated}/{len(klaviyo_records)}")
    return migrated

def delete_table(table_id):
    """Delete a table (Airtable doesn't support this via API easily, so we just mark it)"""
    print(f"\n🗑 To delete table {table_id}:")
    print("  1. Go to Airtable UI")
    print("  2. Right-click table tab → Delete table")
    print("  (API deletion requires Enterprise plan)")

def main():
    print("="*60)
    print("Airtable Refactor Tool")
    print("="*60)
    
    if AIRTABLE_TOKEN == "patXXXXXXXXXXXXXX":
        print("\n❌ ERROR: Please set your AIRTABLE_TOKEN in the script!")
        print("Get it from: https://airtable.com/create/tokens")
        sys.exit(1)
    
    print("\n🔍 Fetching schema...")
    schema = get_table_schema()
    
    tables = {t["name"]: t for t in schema["tables"]}
    
    # Find table IDs
    kunden_id = tables.get("Kunden", {}).get("id")
    stripe_id = tables.get("Stripe Kunden", {}).get("id")
    klaviyo_id = tables.get("Klaviyo Accounts", {}).get("id")
    table1_id = tables.get("Table 1", {}).get("id")
    
    if not kunden_id:
        print("❌ Kunden table not found!")
        sys.exit(1)
    
    print(f"  ✓ Kunden: {kunden_id}")
    print(f"  ✓ Stripe Kunden: {stripe_id or 'NOT FOUND'}")
    print(f"  ✓ Klaviyo Accounts: {klaviyo_id or 'NOT FOUND'}")
    print(f"  ✓ Table 1: {table1_id or 'NOT FOUND'}")
    
    # Step 1: Create new fields
    print("\n" + "="*60)
    print("Step 1: Creating new fields in Kunden table...")
    print("="*60)
    
    # Stripe fields
    create_field(kunden_id, "Stripe Subscription ID", "singleLineText")
    create_field(kunden_id, "Stripe Abo-Status", "singleSelect", {
        "choices": [
            {"name": "Aktiv", "color": "greenBright2"},
            {"name": "Pausiert", "color": "yellowBright2"},
            {"name": "Gekündigt", "color": "redBright2"},
            {"name": "Testphase", "color": "blueBright2"}
        ]
    })
    create_field(kunden_id, "Stripe Monatlicher Betrag", "currency", {"symbol": "€", "precision": 2})
    
    # Confirm before migration
    print("\n" + "="*60)
    print("Step 2: Data Migration")
    print("="*60)
    
    confirm = input("\n⚠️  Ready to migrate data? This will modify records. (yes/no): ")
    if confirm.lower() != "yes":
        print("Aborted.")
        return
    
    # Migrate Stripe
    if stripe_id:
        migrate_stripe_data(kunden_id, stripe_id)
    else:
        print("  ℹ No Stripe Kunden table found")
    
    # Migrate Klaviyo
    if klaviyo_id:
        migrate_klaviyo_data(kunden_id, klaviyo_id)
    else:
        print("  ℹ No Klaviyo Accounts table found")
    
    # Summary
    print("\n" + "="*60)
    print("✅ Migration complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Verify data in Airtable UI")
    print("2. Update scripts to use new field names")
    print("3. Delete redundant tables in Airtable UI:")
    if stripe_id:
        print(f"   - Stripe Kunden ({stripe_id})")
    if klaviyo_id:
        print(f"   - Klaviyo Accounts ({klaviyo_id})")
    if table1_id:
        print(f"   - Table 1 ({table1_id})")
    print("4. Remove old linked fields from Kunden table")

if __name__ == "__main__":
    main()
