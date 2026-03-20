#!/usr/bin/env python3
"""
Weekly Kunden Performance Report - Sheet Extension & Email
Extends the existing meta-reporting-setup with:
  - Weekly Summary tab
  - Charts data tab (for ROAS, CTR, Spend over time)
  - Creative Status from ClickUp
  - Budget vs Spend tracking
  - Highlights section
  - Email sending via n8n

Usage:
  # Extend existing sheet with weekly data + charts
  python3 weekly-report-extend.py --sheet-id XXXXX --account-id 123456

  # Run for all clients (reads from Airtable)
  python3 weekly-report-extend.py --all-clients

  # Just send email (data already in sheet)
  python3 weekly-report-extend.py --sheet-id XXXXX --send-email --to client@example.com --client-name "Razeco"

Env vars (from .env):
  META_ACCESS_TOKEN, AIRTABLE_API_KEY, MATON_API_KEY, N8N_API_KEY, N8N_BASE_URL
"""

import subprocess
import json
import sys
import os
import re
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote

# --- Load .env ---
ENV_PATH = os.path.expanduser("~/.openclaw/workspace/.env")
def load_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k, v)
load_env()

META_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")
AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY", "")
MATON_KEY = os.environ.get("MATON_API_KEY", "")
N8N_KEY = os.environ.get("N8N_API_KEY", "")
N8N_BASE = os.environ.get("N8N_BASE_URL", "https://n8n.adsdrop.de")
AIRTABLE_BASE = "appbGhxy9I18oIS8E"

# ClickUp config
CLICKUP_TOKEN = os.environ.get("CLICKUP_TOKEN", "")

# --- HTTP helpers ---
def http_request(url, headers=None, data=None, method=None):
    req = Request(url, data=data.encode() if isinstance(data, str) else data, method=method)
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        resp = urlopen(req, timeout=30)
        return json.loads(resp.read())
    except Exception as e:
        print(f"❌ HTTP error: {e}", file=sys.stderr)
        return None

def http_get(url, headers=None):
    return http_request(url, headers)

# --- gog CLI helpers ---
def gog_sheets_get(sheet_id, range_str):
    result = subprocess.run(
        ["gog", "sheets", "get", sheet_id, range_str, "--json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout)
        return data.get("values", [])
    except:
        return []

def gog_sheets_append(sheet_id, tab_range, values):
    if not values:
        return True
    result = subprocess.run(
        ["gog", "sheets", "append", sheet_id, tab_range,
         "--values-json", json.dumps(values),
         "--insert", "INSERT_ROWS",
         "--input", "USER_ENTERED"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️ Append error: {result.stderr[:200]}", file=sys.stderr)
        return False
    return True

def gog_sheets_update(sheet_id, range_str, values):
    result = subprocess.run(
        ["gog", "sheets", "update", sheet_id, range_str,
         "--values-json", json.dumps(values),
         "--input", "USER_ENTERED"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️ Update error: {result.stderr[:200]}", file=sys.stderr)
        return False
    return True

def gog_sheets_clear(sheet_id, range_str):
    subprocess.run(["gog", "sheets", "clear", sheet_id, range_str, "-y"],
                    capture_output=True, text=True)

# --- Meta Ads API ---
def meta_api_get(account_id, level, fields, since, until):
    all_data = []
    params = urlencode({
        "level": level,
        "fields": fields,
        "time_range": json.dumps({"since": since, "until": until}),
        "time_increment": "1" if level == "account" else "all_days",
        "limit": "500",
        "filtering": json.dumps([{"field": "spend", "operator": "GREATER_THAN", "value": "0"}]),
        "access_token": META_TOKEN
    })
    url = f"https://graph.facebook.com/v21.0/{account_id}/insights?{params}"
    while url:
        data = http_get(url)
        if not data:
            break
        all_data.extend(data.get("data", []))
        url = data.get("paging", {}).get("next")
    return all_data

def extract_action(actions, action_types):
    if not actions:
        return 0
    for at in action_types:
        for a in (actions or []):
            if a.get("action_type") == at:
                return a.get("value", 0)
    return 0

PURCHASE_TYPES = ["offsite_conversion.fb_pixel_purchase", "purchase", "omni_purchase"]
LEAD_TYPES = ["lead", "onsite_conversion.lead_grouped"]

# --- ClickUp Integration ---
def get_clickup_creative_status(client_name):
    """Pull creative statuses from ClickUp for a client.
    Returns list of {name, status, list_name}"""
    if not CLICKUP_TOKEN:
        print("  ⚠️ No CLICKUP_TOKEN, skipping ClickUp", file=sys.stderr)
        return []
    
    # Search for the client's space/folder
    # Using ClickUp API v2
    headers = {"Authorization": CLICKUP_TOKEN}
    
    # Get teams
    teams = http_get("https://api.clickup.com/api/v2/team", headers)
    if not teams or not teams.get("teams"):
        return []
    
    team_id = teams["teams"][0]["id"]
    
    # Get spaces
    spaces = http_get(f"https://api.clickup.com/api/v2/team/{team_id}/space?archived=false", headers)
    if not spaces:
        return []
    
    # Find "Delivery" space
    delivery_space = None
    for s in spaces.get("spaces", []):
        if "delivery" in s["name"].lower() or "kunden" in s["name"].lower():
            delivery_space = s["id"]
            break
    
    if not delivery_space:
        return []
    
    # Get folders in space
    folders = http_get(f"https://api.clickup.com/api/v2/space/{delivery_space}/folder?archived=false", headers)
    if not folders:
        return []
    
    # Find client folder
    client_folder = None
    for f in folders.get("folders", []):
        if client_name.lower() in f["name"].lower():
            client_folder = f["id"]
            break
    
    if not client_folder:
        return []
    
    # Get lists in folder
    lists = http_get(f"https://api.clickup.com/api/v2/folder/{client_folder}/list?archived=false", headers)
    if not lists:
        return []
    
    creatives = []
    for lst in lists.get("lists", []):
        if "creative" in lst["name"].lower() or "pipeline" in lst["name"].lower():
            # Get tasks
            tasks = http_get(f"https://api.clickup.com/api/v2/list/{lst['id']}/task?archived=false&subtasks=true", headers)
            if tasks:
                for t in tasks.get("tasks", []):
                    status_name = t.get("status", {}).get("status", "").lower()
                    # Map to Winner/Testing/Loser
                    if "winner" in status_name or "active" in status_name or "scaling" in status_name:
                        mapped = "Winner"
                    elif "test" in status_name or "review" in status_name or "ready" in status_name:
                        mapped = "Testing"
                    elif "loser" in status_name or "paused" in status_name or "dead" in status_name or "killed" in status_name:
                        mapped = "Loser"
                    else:
                        mapped = status_name.title()
                    
                    creatives.append({
                        "name": t.get("name", ""),
                        "status": mapped,
                        "raw_status": t.get("status", {}).get("status", ""),
                        "list": lst["name"]
                    })
    
    return creatives

def get_clickup_next_steps(client_name):
    """Get planned tasks for this week from ClickUp."""
    if not CLICKUP_TOKEN:
        return []
    
    headers = {"Authorization": CLICKUP_TOKEN}
    teams = http_get("https://api.clickup.com/api/v2/team", headers)
    if not teams or not teams.get("teams"):
        return []
    
    team_id = teams["teams"][0]["id"]
    
    # Search tasks due this week
    now = datetime.now()
    week_end = now + timedelta(days=7)
    
    params = urlencode({
        "team_ids[]": team_id,
        "due_date_gt": str(int(now.timestamp() * 1000)),
        "due_date_lt": str(int(week_end.timestamp() * 1000)),
        "include_closed": "false"
    })
    
    # Filter by client name in task/list name
    tasks = http_get(f"https://api.clickup.com/api/v2/team/{team_id}/task?{params}", headers)
    if not tasks:
        return []
    
    steps = []
    for t in tasks.get("tasks", []):
        folder_name = t.get("folder", {}).get("name", "")
        if client_name.lower() in folder_name.lower() or client_name.lower() in t.get("list", {}).get("name", "").lower():
            steps.append(t.get("name", ""))
    
    return steps[:10]

# --- Airtable ---
def get_clients_from_airtable():
    if not AIRTABLE_KEY:
        return []
    headers = {"Authorization": f"Bearer {AIRTABLE_KEY}"}
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE}/{quote('Kunden')}"
    data = http_get(url, headers)
    if not data:
        return []
    
    clients = []
    for rec in data.get("records", []):
        f = rec.get("fields", {})
        ad_account = f.get("Meta Ad Account ID", "")
        if ad_account:
            clients.append({
                "name": f.get("Firmenname", f.get("Name", "")),
                "ad_account_id": str(ad_account).replace("act_", ""),
                "email": f.get("AP E-Mail", f.get("Email", "")),
                "sheet_id": extract_sheet_id(f.get("Reporting Sheet", "")),
                "airtable_id": rec.get("id"),
                "weekly_budget": float(f.get("Wochenbudget", 0) or 0),
            })
    return clients

def extract_sheet_id(url):
    if not url:
        return ""
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    return m.group(1) if m else url

# --- Report Builder ---

def build_weekly_report(sheet_id, account_id, client_name="", weekly_budget=0):
    """Pull last 7 days of data and write to Weekly Summary + Charts tabs."""
    
    until = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    kw = datetime.now().isocalendar()[1]
    
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"📊 Weekly Report: {client_name or account_id}", file=sys.stderr)
    print(f"📅 {since} → {until} (KW{kw})", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)
    
    act_id = f"act_{account_id}" if not account_id.startswith("act_") else account_id
    
    # --- 1. Pull daily account-level data (for charts) ---
    print("  📥 Pulling daily data...", file=sys.stderr)
    daily_data = meta_api_get(act_id, "account",
        "impressions,clicks,ctr,cpc,cpm,spend,actions,action_values,purchase_roas",
        since, until)
    
    daily_rows = [["Datum", "Spend", "Impressions", "Clicks", "CTR", "CPC", "CPM", "ROAS", "Purchases", "Revenue"]]
    total_spend = 0
    total_imp = 0
    total_clicks = 0
    total_purchases = 0
    total_revenue = 0
    
    for d in sorted(daily_data, key=lambda x: x.get("date_start", "")):
        spend = float(d.get("spend", 0))
        imp = int(d.get("impressions", 0))
        clicks = int(d.get("clicks", 0))
        purchases = int(extract_action(d.get("actions"), PURCHASE_TYPES) or 0)
        revenue = float(extract_action(d.get("action_values"), PURCHASE_TYPES) or 0)
        roas_list = d.get("purchase_roas", [])
        roas = float(roas_list[0]["value"]) if roas_list else (revenue / spend if spend > 0 else 0)
        
        total_spend += spend
        total_imp += imp
        total_clicks += clicks
        total_purchases += purchases
        total_revenue += revenue
        
        daily_rows.append([
            d.get("date_start", ""),
            round(spend, 2),
            imp,
            clicks,
            round(float(d.get("ctr", 0)), 2),
            round(float(d.get("cpc", 0)), 2),
            round(float(d.get("cpm", 0)), 2),
            round(roas, 2),
            purchases,
            round(revenue, 2)
        ])
    
    # --- 2. Pull campaign-level data ---
    print("  📥 Pulling campaign data...", file=sys.stderr)
    camp_data = meta_api_get(act_id, "campaign",
        "campaign_id,campaign_name,objective,spend,impressions,clicks,ctr,cpm,actions,action_values,cost_per_action_type",
        since, until)
    
    camp_rows = [["Campaign", "Objective", "Spend", "Impressions", "Clicks", "CTR", "Purchases", "Revenue", "ROAS", "CPA"]]
    for c in sorted(camp_data, key=lambda x: float(x.get("spend", 0)), reverse=True):
        spend = float(c.get("spend", 0))
        purchases = int(extract_action(c.get("actions"), PURCHASE_TYPES) or 0)
        revenue = float(extract_action(c.get("action_values"), PURCHASE_TYPES) or 0)
        roas = round(revenue / spend, 2) if spend > 0 else 0
        cpa = round(spend / purchases, 2) if purchases > 0 else 0
        camp_rows.append([
            c.get("campaign_name", ""),
            c.get("objective", ""),
            round(spend, 2),
            int(c.get("impressions", 0)),
            int(c.get("clicks", 0)),
            round(float(c.get("ctr", 0)), 2),
            purchases,
            round(revenue, 2),
            roas,
            cpa
        ])
    
    # --- 3. Pull ad-level data (creative performance) ---
    print("  📥 Pulling creative data...", file=sys.stderr)
    ad_data = meta_api_get(act_id, "ad",
        "ad_id,ad_name,campaign_name,spend,impressions,clicks,ctr,cpc,cpm,actions,action_values,video_play_actions,video_p100_watched_actions",
        since, until)
    
    # Get ClickUp creative statuses
    print("  📥 Pulling ClickUp creative status...", file=sys.stderr)
    clickup_creatives = get_clickup_creative_status(client_name) if client_name else []
    clickup_map = {c["name"].lower(): c["status"] for c in clickup_creatives}
    
    creative_rows = [["Ad Name", "Campaign", "Spend", "Impressions", "Clicks", "CTR", "Hook Rate", "Hold Rate", "Status"]]
    for a in sorted(ad_data, key=lambda x: float(x.get("spend", 0)), reverse=True)[:20]:
        imp = int(a.get("impressions", 0))
        video_plays = int(extract_action(a.get("video_play_actions"), ["video_view"]) or 0)
        thruplay = int(extract_action(a.get("video_p100_watched_actions"), ["video_view"]) or 0)
        hook_rate = round((video_plays / imp) * 100, 1) if imp > 0 and video_plays > 0 else ""
        hold_rate = round((thruplay / video_plays) * 100, 1) if video_plays > 0 and thruplay > 0 else ""
        
        ad_name = a.get("ad_name", "")
        status = clickup_map.get(ad_name.lower(), "")
        if not status:
            # Try fuzzy match
            for ck, cv in clickup_map.items():
                if ck in ad_name.lower() or ad_name.lower() in ck:
                    status = cv
                    break
        
        creative_rows.append([
            ad_name,
            a.get("campaign_name", ""),
            round(float(a.get("spend", 0)), 2),
            imp,
            int(a.get("clicks", 0)),
            round(float(a.get("ctr", 0)), 2),
            hook_rate,
            hold_rate,
            status
        ])
    
    # --- 4. Build highlights/summary ---
    avg_ctr = round((total_clicks / total_imp * 100) if total_imp > 0 else 0, 2)
    avg_roas = round(total_revenue / total_spend if total_spend > 0 else 0, 2)
    cpa = round(total_spend / total_purchases if total_purchases > 0 else 0, 2)
    budget_pct = round((total_spend / weekly_budget * 100) if weekly_budget > 0 else 0, 1)
    
    # Next steps from ClickUp
    print("  📥 Pulling next steps from ClickUp...", file=sys.stderr)
    next_steps = get_clickup_next_steps(client_name) if client_name else []
    
    summary_rows = [
        ["Weekly Performance Summary"],
        [f"Zeitraum: {since} bis {until} (KW{kw})"],
        [""],
        ["📊 KPIs", ""],
        ["Total Spend", f"€{total_spend:,.2f}"],
        ["Impressions", f"{total_imp:,}"],
        ["Clicks", f"{total_clicks:,}"],
        ["CTR", f"{avg_ctr}%"],
        ["Purchases", str(total_purchases)],
        ["Revenue", f"€{total_revenue:,.2f}"],
        ["ROAS", f"{avg_roas}x"],
        ["Cost per Purchase", f"€{cpa}"],
        [""],
        ["💰 Budget Status", ""],
        ["Wochenbudget", f"€{weekly_budget:,.2f}" if weekly_budget else "N/A"],
        ["Ausgegeben", f"€{total_spend:,.2f}"],
        ["Verbrauch", f"{budget_pct}%" if weekly_budget else "N/A"],
        ["Verbleibend", f"€{max(0, weekly_budget - total_spend):,.2f}" if weekly_budget else "N/A"],
        [""],
        ["🏆 Highlights", ""],
    ]
    
    # Auto-generate highlights
    if camp_data:
        best_camp = max(camp_data, key=lambda x: float(extract_action(x.get("action_values"), PURCHASE_TYPES) or 0) / max(float(x.get("spend", 0)), 0.01))
        summary_rows.append([f"Beste Campaign: {best_camp.get('campaign_name', '')}", ""])
    
    if ad_data:
        best_ctr_ad = max(ad_data, key=lambda x: float(x.get("ctr", 0)))
        summary_rows.append([f"Bestes Creative (CTR): {best_ctr_ad.get('ad_name', '')[:50]} ({float(best_ctr_ad.get('ctr', 0)):.2f}%)", ""])
    
    summary_rows.append([""])
    summary_rows.append(["📋 Next Steps (aus ClickUp)", ""])
    if next_steps:
        for step in next_steps:
            summary_rows.append([f"• {step}", ""])
    else:
        summary_rows.append(["• Keine Tasks diese Woche in ClickUp", ""])
    
    # --- 5. Write to Google Sheet ---
    print("  📝 Writing to Google Sheet...", file=sys.stderr)
    
    # Clear and write Weekly Summary tab
    gog_sheets_clear(sheet_id, "Weekly Summary!A:Z")
    gog_sheets_update(sheet_id, "Weekly Summary!A1", summary_rows)
    print("  ✅ Weekly Summary", file=sys.stderr)
    
    # Clear and write Charts Data tab (for chart source)
    gog_sheets_clear(sheet_id, "Charts Data!A:Z")
    gog_sheets_update(sheet_id, "Charts Data!A1", daily_rows)
    print("  ✅ Charts Data", file=sys.stderr)
    
    # Clear and write Campaign Performance tab
    gog_sheets_clear(sheet_id, "Campaign Performance!A:Z")
    gog_sheets_update(sheet_id, "Campaign Performance!A1", camp_rows)
    print("  ✅ Campaign Performance", file=sys.stderr)
    
    # Clear and write Creative Overview tab
    gog_sheets_clear(sheet_id, "Creative Overview!A:Z")
    gog_sheets_update(sheet_id, "Creative Overview!A1", creative_rows)
    print("  ✅ Creative Overview", file=sys.stderr)
    
    print(f"\n✅ Report fertig: https://docs.google.com/spreadsheets/d/{sheet_id}/edit", file=sys.stderr)
    
    return {
        "sheet_id": sheet_id,
        "sheet_url": f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit",
        "client_name": client_name,
        "kw": kw,
        "period": {"since": since, "until": until},
        "summary": {
            "total_spend": total_spend,
            "total_impressions": total_imp,
            "total_clicks": total_clicks,
            "avg_ctr": avg_ctr,
            "total_purchases": total_purchases,
            "total_revenue": total_revenue,
            "avg_roas": avg_roas,
            "cpa": cpa,
            "weekly_budget": weekly_budget,
            "budget_pct": budget_pct,
        },
        "campaigns": [r for r in camp_rows[1:]],  # skip header
        "creatives": [r for r in creative_rows[1:]],
        "next_steps": next_steps,
    }

# --- Sheet Setup (add missing tabs) ---

def ensure_tabs_exist(sheet_id):
    """Ensure the sheet has all required tabs."""
    # Get existing tabs
    result = subprocess.run(
        ["gog", "sheets", "metadata", sheet_id, "--json"],
        capture_output=True, text=True
    )
    existing_tabs = set()
    if result.returncode == 0:
        try:
            meta = json.loads(result.stdout)
            for sheet in meta.get("sheets", []):
                existing_tabs.add(sheet.get("properties", {}).get("title", ""))
        except:
            pass
    
    needed = ["Weekly Summary", "Charts Data", "Campaign Performance", "Creative Overview"]
    for tab in needed:
        if tab not in existing_tabs:
            print(f"  📑 Creating tab: {tab}", file=sys.stderr)
            # Use gog or a workaround to add a sheet tab
            # gog doesn't have addSheet, so we write to the tab which auto-creates it
            gog_sheets_update(sheet_id, f"{tab}!A1", [["Wird geladen..."]])
    
    return True

# --- Email ---

def send_report_email(report_data, to_email, sender_email="deniz@adsdrop.de"):
    """Send the weekly report email via n8n webhook or SMTP."""
    s = report_data["summary"]
    kw = report_data["kw"]
    client = report_data["client_name"]
    
    # Build email from template
    template_path = os.path.expanduser("~/.openclaw/workspace/templates/weekly-report-email.html")
    if os.path.exists(template_path):
        with open(template_path) as f:
            html = f.read()
    else:
        html = build_fallback_email_html(report_data)
    
    # Replace placeholders
    replacements = {
        "{{client_name}}": client,
        "{{calendar_week}}": str(kw),
        "{{date_range}}": f"{report_data['period']['since']} – {report_data['period']['until']}",
        "{{total_spend}}": f"{s['total_spend']:,.2f}",
        "{{roas}}": f"{s['avg_roas']:.2f}",
        "{{total_purchases}}": str(s['total_purchases']),
        "{{ctr}}": f"{s['avg_ctr']:.2f}",
        "{{cpc}}": f"{s.get('cpa', 0):.2f}",
        "{{cost_per_purchase}}": f"{s['cpa']:.2f}",
        "{{weekly_budget}}": f"{s['weekly_budget']:,.2f}" if s['weekly_budget'] else "N/A",
        "{{budget_pct}}": f"{s['budget_pct']:.0f}" if s['weekly_budget'] else "N/A",
        "{{budget_remaining}}": f"{max(0, s['weekly_budget'] - s['total_spend']):,.2f}" if s['weekly_budget'] else "N/A",
        "{{sheet_link}}": report_data["sheet_url"],
        "{{sender_email}}": sender_email,
    }
    
    for k, v in replacements.items():
        html = html.replace(k, str(v))
    
    # Replace campaign rows
    camp_html = ""
    for c in report_data.get("campaigns", [])[:5]:
        camp_html += f"<tr><td><strong>{c[0]}</strong></td><td>€{c[2]}</td><td>{c[8]}x</td><td>{c[5]}%</td><td>{c[6]}</td></tr>\n"
    html = re.sub(r'\{\{#campaigns\}\}.*?\{\{/campaigns\}\}', camp_html, html, flags=re.DOTALL)
    
    # Replace creative rows
    creative_html = ""
    for c in report_data.get("creatives", [])[:8]:
        status = c[8] if len(c) > 8 else ""
        status_class = status.lower() if status in ["Winner", "Testing", "Loser"] else "testing"
        creative_html += f'<tr><td>{c[0][:40]}</td><td>€{c[2]}</td><td>{c[5]}%</td><td><span class="status-badge status-{status_class}">{status}</span></td></tr>\n'
    html = re.sub(r'\{\{#creatives\}\}.*?\{\{/creatives\}\}', creative_html, html, flags=re.DOTALL)
    
    # Replace next steps
    steps_html = ""
    for step in report_data.get("next_steps", ["Keine geplanten Tasks diese Woche"]):
        steps_html += f"<li>{step}</li>\n"
    html = re.sub(r'\{\{#next_steps\}\}.*?\{\{/next_steps\}\}', steps_html, html, flags=re.DOTALL)
    
    subject = f"Weekly Performance Report - {client} - KW{kw}"
    
    # Try sending via n8n webhook
    print(f"  📧 Sending email to {to_email}...", file=sys.stderr)
    
    # Option 1: Use gog gmail send
    result = subprocess.run(
        ["gog", "gmail", "send",
         "--to", to_email,
         "--subject", subject,
         "--html", "-"],
        input=html, capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"  ✅ Email sent to {to_email}", file=sys.stderr)
        return True
    else:
        print(f"  ⚠️ gog gmail failed: {result.stderr[:200]}", file=sys.stderr)
        # Fallback: save HTML for manual send
        out_path = f"/tmp/weekly-report-{client.lower().replace(' ', '-')}-kw{kw}.html"
        with open(out_path, "w") as f:
            f.write(html)
        print(f"  📄 Email HTML saved to {out_path}", file=sys.stderr)
        return False

def build_fallback_email_html(report_data):
    """Simple fallback if template not found."""
    s = report_data["summary"]
    return f"""<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
    <h2>Weekly Performance Report - {report_data['client_name']}</h2>
    <p>KW{report_data['kw']} | {report_data['period']['since']} – {report_data['period']['until']}</p>
    <table style="width:100%;border-collapse:collapse;">
    <tr><td style="padding:8px;border:1px solid #ddd;"><strong>Spend</strong></td><td style="padding:8px;border:1px solid #ddd;">€{s['total_spend']:,.2f}</td></tr>
    <tr><td style="padding:8px;border:1px solid #ddd;"><strong>ROAS</strong></td><td style="padding:8px;border:1px solid #ddd;">{s['avg_roas']:.2f}x</td></tr>
    <tr><td style="padding:8px;border:1px solid #ddd;"><strong>CTR</strong></td><td style="padding:8px;border:1px solid #ddd;">{s['avg_ctr']:.2f}%</td></tr>
    <tr><td style="padding:8px;border:1px solid #ddd;"><strong>Purchases</strong></td><td style="padding:8px;border:1px solid #ddd;">{s['total_purchases']}</td></tr>
    </table>
    <p><a href="{report_data['sheet_url']}">📄 Vollständiger Report</a></p>
    </body></html>"""

# --- Main ---

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Weekly Kunden Performance Report")
    parser.add_argument("--sheet-id", help="Google Sheet ID")
    parser.add_argument("--account-id", help="Meta Ad Account ID (without act_)")
    parser.add_argument("--client-name", default="", help="Client name")
    parser.add_argument("--weekly-budget", type=float, default=0, help="Weekly ad budget")
    parser.add_argument("--all-clients", action="store_true", help="Run for all clients from Airtable")
    parser.add_argument("--send-email", action="store_true", help="Send email after report")
    parser.add_argument("--to", help="Email recipient")
    parser.add_argument("--dry-run", action="store_true", help="Don't write, just print")
    args = parser.parse_args()
    
    if args.all_clients:
        clients = get_clients_from_airtable()
        if not clients:
            print("❌ No clients found in Airtable", file=sys.stderr)
            sys.exit(1)
        
        print(f"👥 Found {len(clients)} clients with Meta Ad Account", file=sys.stderr)
        results = []
        
        for client in clients:
            if not client["sheet_id"]:
                print(f"  ⚠️ {client['name']}: No sheet ID, skipping", file=sys.stderr)
                continue
            
            ensure_tabs_exist(client["sheet_id"])
            report = build_weekly_report(
                client["sheet_id"],
                client["ad_account_id"],
                client["name"],
                client.get("weekly_budget", 0)
            )
            
            if args.send_email and client.get("email"):
                send_report_email(report, client["email"])
            
            results.append(report)
        
        print(json.dumps(results, indent=2, default=str))
    
    elif args.sheet_id and args.account_id:
        ensure_tabs_exist(args.sheet_id)
        report = build_weekly_report(
            args.sheet_id,
            args.account_id,
            args.client_name,
            args.weekly_budget
        )
        
        if args.send_email and args.to:
            send_report_email(report, args.to)
        
        print(json.dumps(report, indent=2, default=str))
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
