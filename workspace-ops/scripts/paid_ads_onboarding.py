#!/usr/bin/env python3
"""
Paid Ads Onboarding Automation
===============================
Creates a full ClickUp project structure for a new Paid Ads client.

Usage:
  python3 paid_ads_onboarding.py --name "🔥 Kundenname" [--airtable-record recXXX] [--dry-run]

What it creates:
  1. Folder in Delivery Space
  2. 5 Lists: Project Management, Creative Pipeline, Archive, Learnings, Creator Pool
  3. 9 Onboarding Tasks in Project Management (with due dates relative to today)
  4. 6 Paid Social Templates copied from Process Hub into Project Management
  5. 3 Custom Fields in Creative Pipeline (Creative Type, Hook Type, Testing Phase)
"""
import sys, json, time, argparse
sys.path.insert(0, '/Users/denizakin/.openclaw/workspace/skills/clickup/scripts')
from clickup_client import ClickUpClient, datetime_to_timestamp
from datetime import datetime, timedelta

# ============================================================
# CONFIG
# ============================================================
DELIVERY_SPACE_ID = "90040311585"
TEAM_ID = "9006104573"

# Process Hub → Paid Social template task IDs
PAID_SOCIAL_TEMPLATES = [
    ("86c13fa87", "Meta Ads | Analyze Ad Account", 2),
    ("86c13fgpt", "Meta Ads | Setup Ad Account", 3),
    ("86c13jpu7", "Meta Ads | Phase 1 | Message Testing", 5),
    ("86c13f9m5", "Meta Ads | Phase 2 | Creative Testing", 8),
    ("86c13jq54", "Meta Ads | Phase 3 | Audience Testing", 13),
    ("86c13jq77", "Meta Ads | Phase 4 | Scaling", 17),
]

# Onboarding tasks (name, description_template, days_offset, checklists)
# {name} will be replaced with customer name
ONBOARDING_TASKS = [
    ("🚀 Kickoff Call", 
     "Erstgespräch mit dem Kunden. Ziele definieren, Erwartungen abstimmen, Briefing sammeln.\n\n⏱️ Dauer: 60-90 Min\n👤 Teilnehmer: Team + Kunde",
     0,
     [("Kickoff Checkliste", [
         "Zugänge erhalten (Ad Accounts, Analytics, etc.)",
         "Ziele & KPIs definieren",
         "Budget besprechen",
         "Timeline abstimmen",
         "Nächste Schritte festlegen",
     ])]),
    ("🔍 Tracking Audit & Setup",
     "Tracking überprüfen und einrichten.\n\nPixel, Conversions API, Events validieren.",
     1,
     [("Tracking Checkliste", [
         "Meta Pixel prüfen",
         "Conversions API prüfen",
         "Standard Events prüfen",
         "Custom Events prüfen",
         "Google Analytics Verknüpfung",
         "UTM Parameter Setup",
         "Test-Conversion auslösen",
     ])]),
    ("📊 Account Analysis",
     "Bestehenden Ad Account analysieren. Historische Performance, Zielgruppen, Creatives bewerten.",
     2, []),
    ("💡 Creative Briefing",
     "Creative Briefing erstellen. Messaging, Hooks, Formate definieren.",
     3, []),
    ("🎬 Creative Produktion",
     "Creatives nach Briefing produzieren. Bilder, Videos, UGC.",
     5, []),
    ("👁️ Kunden Review",
     "Creatives & Strategie mit dem Kunden reviewen und Feedback einarbeiten.",
     8, []),
    ("🚀 Campaign Launch",
     "Kampagnen live schalten. Ad Sets, Budgets, Targeting final einrichten.",
     10, []),
    ("📈 Performance Check (Tag 3)",
     "Erste Performance-Analyse nach 3 Tagen. Quick Wins identifizieren, erste Optimierungen.",
     13, []),
    ("🏆 Performance Check (Tag 7)",
     "Performance-Analyse nach 7 Tagen. Winner identifizieren, Scaling-Entscheidung.",
     17, []),
]

LISTS = ["Project Management", "Creative Pipeline", "Archive", "Learnings", "Creator Pool"]

CUSTOM_FIELDS = [
    ("Creative Type", ["Image", "Video", "UGC", "Carousel"]),
    ("Hook Type", ["Problem", "Benefit", "Social Proof", "Urgency"]),
    ("Testing Phase", ["Testing", "Winner", "Scaling", "Archive"]),
]


def run_onboarding(customer_name, airtable_record=None, dry_run=False):
    client = ClickUpClient()
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    results = {
        "customer": customer_name,
        "folder": None,
        "lists": [],
        "tasks": [],
        "custom_fields": [],
        "errors": [],
    }

    # ── Step 1: Create Folder ──
    print(f"=== Step 1: Creating Folder '{customer_name}' ===")
    if dry_run:
        folder_id = "DRY_RUN"
        print(f"  [DRY RUN] Would create folder '{customer_name}'")
    else:
        try:
            folder = client.create_folder(DELIVERY_SPACE_ID, customer_name)
            folder_id = folder["id"]
            results["folder"] = {"id": folder_id, "name": folder.get("name")}
            print(f"✅ Folder: {folder_id}")
        except Exception as e:
            print(f"⚠️  Folder creation failed (probably exists): {e}")
            # Try to find existing folder
            try:
                folders_data = client.list_folders(DELIVERY_SPACE_ID)
                folders = folders_data.get("folders", [])
                for f in folders:
                    if f.get("name") == customer_name:
                        folder_id = f["id"]
                        results["folder"] = {"id": folder_id, "name": f.get("name")}
                        print(f"✅ Found existing folder: {folder_id}")
                        break
            except Exception as e2:
                print(f"❌ Could not find existing folder: {e2}")
                return results
            
            if not folder_id:
                print("❌ No folder available")
                return results

    # ── Step 2: Create Lists ──
    print(f"\n=== Step 2: Creating {len(LISTS)} Lists ===")
    list_ids = {}
    for name in LISTS:
        if dry_run:
            list_ids[name] = "DRY_RUN"
            print(f"  [DRY RUN] Would create list '{name}'")
        else:
            try:
                lst = client.create_list(name, folder_id=folder_id)
                list_ids[name] = lst["id"]
                results["lists"].append({"id": lst["id"], "name": name})
                print(f"✅ '{name}': {lst['id']}")
                time.sleep(0.3)
            except Exception as e:
                results["errors"].append(f"List '{name}': {e}")
                print(f"❌ '{name}': {e}")

    pm_list_id = list_ids.get("Project Management")
    cp_list_id = list_ids.get("Creative Pipeline")

    # ── Step 3: Onboarding Tasks → Project Management ──
    print(f"\n=== Step 3: Creating Onboarding Tasks ===")
    if pm_list_id and not dry_run:
        for task_name, description, days_offset, checklists in ONBOARDING_TASKS:
            due = today + timedelta(days=days_offset)
            due_ts = datetime_to_timestamp(due)
            try:
                task = client.create_task(
                    pm_list_id, task_name,
                    description=description,
                    due_date=due_ts,
                    due_date_time=False,
                    tags=["onboarding", "project-management"]
                )
                task_id = task["id"]
                results["tasks"].append({"id": task_id, "name": task_name, "due": due.strftime("%Y-%m-%d"), "list": "Project Management", "type": "onboarding"})
                print(f"✅ {task_name} (due: {due.strftime('%Y-%m-%d')})")
                
                # Create checklists
                for cl_name, items in checklists:
                    try:
                        new_cl = client.post(f"/task/{task_id}/checklist", data={"name": cl_name})
                        new_cl_id = new_cl.get("checklist", {}).get("id")
                        if new_cl_id:
                            for item_name in items:
                                client.post(f"/checklist/{new_cl_id}/checklist_item", data={"name": item_name})
                                time.sleep(0.1)
                        print(f"   📝 {cl_name} ({len(items)} items)")
                    except Exception as ce:
                        results["errors"].append(f"Checklist '{cl_name}': {ce}")
                
                time.sleep(0.3)
            except Exception as e:
                results["errors"].append(f"Task '{task_name}': {e}")
                print(f"❌ {task_name}: {e}")
    elif dry_run:
        for task_name, _, days_offset, _ in ONBOARDING_TASKS:
            print(f"  [DRY RUN] {task_name} (due: +{days_offset}d)")

    # ── Step 4: Paid Social Templates → Project Management ──
    print(f"\n=== Step 4: Copying Paid Social Templates from Process Hub ===")
    if pm_list_id and not dry_run:
        for tmpl_id, fallback_name, days_offset in PAID_SOCIAL_TEMPLATES:
            due = today + timedelta(days=days_offset)
            due_ts = datetime_to_timestamp(due)
            
            # Fetch template
            description = ""
            checklists_data = []
            task_name = fallback_name
            try:
                tmpl = client.get_task(tmpl_id, include_subtasks=True)
                description = tmpl.get("description", "") or tmpl.get("text_content", "") or ""
                task_name = tmpl.get("name", fallback_name)
                checklists_data = tmpl.get("checklists", [])
            except Exception as e:
                print(f"  ⚠️ Template {tmpl_id} not found, using fallback name")
                description = f"[Template {tmpl_id}]"
            
            try:
                task = client.create_task(
                    pm_list_id, task_name,
                    description=description,
                    due_date=due_ts,
                    due_date_time=False,
                    tags=["onboarding", "paid-ads"]
                )
                task_id = task["id"]
                results["tasks"].append({"id": task_id, "name": task_name, "due": due.strftime("%Y-%m-%d"), "list": "Project Management", "type": "template"})
                print(f"✅ {task_name} (due: {due.strftime('%Y-%m-%d')})")
                
                # Copy checklists from template
                for cl in checklists_data:
                    cl_name = cl.get("name", "Checklist")
                    items = cl.get("items", [])
                    if not items:
                        continue
                    try:
                        new_cl = client.post(f"/task/{task_id}/checklist", data={"name": cl_name})
                        new_cl_id = new_cl.get("checklist", {}).get("id")
                        if new_cl_id:
                            for item in items:
                                item_name = item.get("name", "")
                                if item_name:
                                    client.post(f"/checklist/{new_cl_id}/checklist_item", data={"name": item_name})
                                    time.sleep(0.1)
                        print(f"   📝 {cl_name} ({len(items)} items)")
                    except Exception as ce:
                        results["errors"].append(f"Checklist '{cl_name}': {ce}")
                
                time.sleep(0.3)
            except Exception as e:
                results["errors"].append(f"Task '{task_name}': {e}")
                print(f"❌ {task_name}: {e}")
    elif dry_run:
        for _, name, days_offset in PAID_SOCIAL_TEMPLATES:
            print(f"  [DRY RUN] {name} (due: +{days_offset}d)")

    # ── Step 5: Custom Fields → Creative Pipeline ──
    print(f"\n=== Step 5: Custom Fields in Creative Pipeline ===")
    if cp_list_id and not dry_run:
        for field_name, options in CUSTOM_FIELDS:
            try:
                resp = client.post(f"/list/{cp_list_id}/field", data={
                    "name": field_name,
                    "type": "drop_down",
                    "type_config": {"options": [{"name": opt, "color": None} for opt in options]}
                })
                results["custom_fields"].append({"name": field_name, "options": options, "id": resp.get("id", "")})
                print(f"✅ {field_name}: {options}")
            except Exception as e:
                results["errors"].append(f"Field '{field_name}': {e}")
                print(f"❌ {field_name}: {e}")
    elif dry_run:
        for field_name, options in CUSTOM_FIELDS:
            print(f"  [DRY RUN] {field_name}: {options}")

    # ── Summary ──
    folder_url = f"https://app.clickup.com/{TEAM_ID}/v/o/s/{DELIVERY_SPACE_ID}?p={folder_id}" if folder_id != "DRY_RUN" else "N/A"
    
    print(f"\n{'='*60}")
    print(f"📊 ONBOARDING COMPLETE — {customer_name}")
    print(f"{'='*60}")
    print(f"Folder: {folder_id}")
    print(f"URL: {folder_url}")
    print(f"Lists: {len(results['lists'])}")
    print(f"Tasks: {len(results['tasks'])} ({sum(1 for t in results['tasks'] if t.get('type')=='onboarding')} onboarding + {sum(1 for t in results['tasks'] if t.get('type')=='template')} templates)")
    print(f"Custom Fields: {len(results['custom_fields'])}")
    if results['errors']:
        print(f"\n⚠️ {len(results['errors'])} Errors:")
        for e in results['errors']:
            print(f"  - {e}")
    else:
        print("✅ 0 Errors")
    
    if airtable_record:
        print(f"\n📎 Airtable: Folder ID '{folder_id}' → Record {airtable_record}")
        # TODO: Airtable API integration when token is configured
    
    results["folder_url"] = folder_url
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paid Ads Onboarding Automation")
    parser.add_argument("--name", required=True, help="Customer/Folder name (e.g. '🔥 Kundenname')")
    parser.add_argument("--airtable-record", help="Airtable record ID to update with folder ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating anything")
    args = parser.parse_args()
    
    results = run_onboarding(args.name, args.airtable_record, args.dry_run)
    
    # Output JSON
    print("\n__JSON__")
    print(json.dumps(results, indent=2))
