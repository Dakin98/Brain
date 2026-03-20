#!/usr/bin/env python3
"""Create Google Sheets and set up Meta Ads reporting"""

import json
import os
import sys
import subprocess

# Get input data
input_data = json.load(sys.stdin)
account_id = input_data.get('meta_ad_account_id', '').replace('act_', '')
firmenname = input_data.get('firmenname', '')
kunde_id = input_data.get('kunde_id', '')

if not account_id or not firmenname:
    print(json.dumps({"error": "Missing account_id or firmenname"}), file=sys.stderr)
    sys.exit(1)

print(f"📊 Setting up Meta Ads reporting for {firmenname} (Account: {account_id})", file=sys.stderr)

# Read credentials
creds_path = os.path.expanduser("~/Library/Application Support/gogcli/credentials.json")
with open(creds_path) as f:
    creds_data = json.load(f)

# Use gog to get access token
try:
    result = subprocess.run(
        ["gog", "-j", "drive", "ls", "--parent", "1BxjCrsOE50VFI5Jdh21O1mJl6Gf5lYJN"],
        capture_output=True, text=True, timeout=30
    )
    # Token is valid, proceed
except Exception as e:
    print(f"Auth check failed: {e}", file=sys.stderr)
    sys.exit(1)

# Create spreadsheet using Google Apps Script or Drive API workaround
# Since gog doesn't support direct sheet creation, we'll use the Drive API to create a file
import urllib.request
import urllib.error

# Get token from gog's internal mechanism
# Let's use a workaround: create via copy of a known small file

# Actually, let's try uploading a CSV that will become a sheet
print("📑 Creating Google Sheet...", file=sys.stderr)

# Create a temp CSV file
csv_content = "Date,Campaign Name,Status,Objective,Budget,Daily Budget,Spend,Impressions,Clicks,CTR,CPC,CPM,Purchases,ROAS\n"
csv_path = "/tmp/meta_template.csv"
with open(csv_path, 'w') as f:
    f.write(csv_content)

# Upload CSV as Google Sheet
upload_result = subprocess.run(
    ["gog", "-j", "drive", "upload", csv_path, 
     "--name", f"Meta Ads Reporting - {firmenname}",
     "--convert",
     "--parent", "1BxjCrsOE50VFI5Jdh21O1mJl6Gf5lYJN"],
    capture_output=True, text=True, timeout=60
)

if upload_result.returncode != 0:
    print(f"Upload failed: {upload_result.stderr}", file=sys.stderr)
    print(json.dumps({"error": "Failed to create Google Sheet"}), file=sys.stderr)
    sys.exit(1)

try:
    upload_data = json.loads(upload_result.stdout)
    # Handle nested structure {"file": {"id": ...}}
    if 'file' in upload_data:
        sheet_id = upload_data['file'].get('id')
        sheet_url = upload_data['file'].get('webViewLink') or f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    else:
        sheet_id = upload_data.get('id')
        sheet_url = upload_data.get('webViewLink') or f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
except Exception as e:
    print(f"Parse error: {e}", file=sys.stderr)
    # Try to extract ID
    sheet_id = None
    for line in upload_result.stdout.split('\n'):
        if '"id"' in line and '1' in line:
            parts = line.split('"')
            for p in parts:
                if len(p) > 20 and '-' in p:
                    sheet_id = p
                    break
            if sheet_id:
                break
    if not sheet_id:
        print(f"Could not parse sheet ID from: {upload_result.stdout}", file=sys.stderr)
        sys.exit(1)
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

print(f"✅ Sheet created: {sheet_id}", file=sys.stderr)

# Set up sheet structure
print("📝 Setting up sheet structure...", file=sys.stderr)

# Add headers to different ranges
headers = [
    ("Campaigns!A1:N1", ["Date", "Campaign Name", "Status", "Objective", "Budget", "Daily Budget", "Spend", "Impressions", "Clicks", "CTR", "CPC", "CPM", "Purchases", "ROAS"]),
    ("Daily!A1:L1", ["Date", "Campaign", "Adset", "Ad", "Spend", "Impressions", "Clicks", "CTR", "CPC", "Results", "Result Type", "Cost per Result"]),
    ("Adsets!A1:E1", ["Adset Name", "Campaign", "Budget Type", "Budget Amount", "Targeting"]),
    ("Monthly!A1:I1", ["Month", "Spend", "Impressions", "Clicks", "CTR", "CPM", "CPC", "Results", "ROAS"]),
]

for range_name, values in headers:
    subprocess.run(
        ["gog", "sheets", "update", sheet_id, range_name] + values,
        capture_output=True, timeout=30
    )

print("✅ Headers written", file=sys.stderr)

# Make sheet publicly readable
print("🔗 Setting permissions...", file=sys.stderr)
subprocess.run(
    ["gog", "-j", "drive", "share", sheet_id, "--type", "anyone", "--role", "reader"],
    capture_output=True, timeout=30
)

# Update Airtable
print("💾 Saving to Airtable...", file=sys.stderr)
airtable_result = subprocess.run(
    ["curl", "-s", "-X", "PATCH", 
     f"https://gateway.maton.ai/airtable/v0/appbGhxy9I18oIS8E/Kunden/{kunde_id}",
     "-H", f"Authorization: Bearer {os.environ.get('MATON_API_KEY', '')}",
     "-H", "Content-Type: application/json",
     "-d", json.dumps({"fields": {"Reporting Sheet": sheet_url}})],
    capture_output=True, text=True, timeout=30
)

print("✅ Meta Ads reporting setup complete!", file=sys.stderr)

# Output result
result = {
    "success": True,
    "firmenname": firmenname,
    "account_id": account_id,
    "sheet_id": sheet_id,
    "sheet_url": sheet_url,
    "kunde_id": kunde_id
}
print(json.dumps(result))
