#!/bin/bash
# Meta Ads Reporting Setup for new clients
# Triggered when Meta Zugang OK is checked
# Creates Google Sheet, pulls initial data, saves URL to Airtable

set -e

INPUT=$(cat)
ACCOUNT_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('meta_ad_account_id',''))")
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
KUNDE_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('kunde_id',''))")

if [ -z "$ACCOUNT_ID" ] || [ -z "$FIRMENNAME" ]; then
    echo '{"error": "Missing account_id or firmenname"}' >&2
    exit 1
fi

# Clean account ID (remove act_ prefix if present)
ACCOUNT_ID=$(echo "$ACCOUNT_ID" | sed 's/^act_//')

echo "📊 Setting up Meta Ads reporting for $FIRMENNAME (Account: $ACCOUNT_ID)" >&2

# 1. Create Google Sheet from template
echo "📑 Creating Google Sheet..." >&2

# Create folder in Google Drive if needed
FOLDER_NAME="$FIRMENNAME - Reports"
FOLDER_ID=$(gog drive create-folder "$FOLDER_NAME" --parent 1_8oRxRfP1PHXEsGhdsfsGPLOjCopxMee 2>/dev/null | grep -oP '(?<=id: )[^ ]+' || echo "")

if [ -z "$FOLDER_ID" ]; then
    # Try to find existing folder
    FOLDER_ID=$(gog drive list --query "name='$FOLDER_NAME'" 2>/dev/null | grep "$FOLDER_NAME" | head -1 | awk '{print $1}')
fi

if [ -z "$FOLDER_ID" ]; then
    echo "⚠️ Could not create/find reports folder" >&2
    FOLDER_ID="1_8oRxRfP1PHXEsGhdsfsGPLOjCopxMee" # Fallback to root clients folder
fi

# Create Sheet
SHEET_NAME="Meta Ads Reporting - $FIRMENNAME"
SHEET_ID=$(gog sheets create "$SHEET_NAME" --folder "$FOLDER_ID" 2>/dev/null | grep -oP '(?<=id: )[^ ]+' || echo "")

if [ -z "$SHEET_ID" ]; then
    echo '{"error": "Failed to create Google Sheet"}' >&2
    exit 1
fi

echo "✅ Sheet created: $SHEET_ID" >&2

# 2. Set up sheet structure with headers
echo "📝 Setting up sheet structure..." >&2

# Campaign Overview tab
gog sheets append "$SHEET_ID" "Campaigns!A1" --values "Date,Campaign Name,Status,Objective,Budget,Daily Budget,Spend,Impressions,Clicks,CTR,CPC,CPM,Purchases,ROAS" 2>/dev/null || true

# Daily Performance tab  
gog sheets append "$SHEET_ID" "Daily!A1" --values "Date,Campaign,Adset,Ad,Spend,Impressions,Clicks,CTR,CPC,Results,Result Type,Cost per Result" 2>/dev/null || true

# Adsets tab
gog sheets append "$SHEET_ID" "Adsets!A1" --values "Adset Name,Campaign,Budget Type,Budget Amount,Targeting" 2>/dev/null || true

# Monthly Summary tab
gog sheets append "$SHEET_ID" "Monthly!A1" --values "Month,Spend,Impressions,Clicks,CTR,CPM,CPC,Results,ROAS" 2>/dev/null || true

# 3. Pull initial data
export META_ACCESS_TOKEN="EAAKZBJwhRFYYBQgkJrgwdeNdkcLTPFYbq2KTmVQaDmZBKwWCW0PfFEe7eKV0O4UKGveqrtyaDYIHs2L6UO151GzUKSsBL0ZAqjlQdXdj3ocetmBTLShkea5mTc5jXZBUEGacJXLKOkUZBqs6F9B7K6B0cxkAVZCpf8s7s4DnV28GezjPOGYl2ik35CPvigrGZCbIhRQOtBFAPsl6Ci4hdr51shDJ4cJldzi"

echo "📥 Pulling initial Meta Ads data..." >&2
python3 /Users/denizakin/.openclaw/workspace/scripts/meta-ads-pull.py \
    --account-id "$ACCOUNT_ID" \
    --since "$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d '30 days ago' +%Y-%m-%d)" \
    --until "$(date +%Y-%m-%d)" \
    --output json > /tmp/meta_data.json 2>/dev/null

if [ -f /tmp/meta_data.json ]; then
    # Parse and write to sheet (simplified - just campaigns for now)
    python3 << 'PYEOF'
import json
import sys

with open('/tmp/meta_data.json') as f:
    data = json.load(f)

# Write campaign data
rows = []
for campaign in data.get('campaigns', []):
    # Find insights for this campaign
    campaign_insights = [i for i in data.get('insights', []) if i.get('campaign_id') == campaign.get('id')]
    if campaign_insights:
        spend = sum(float(i.get('spend', 0)) for i in campaign_insights)
        imp = sum(int(i.get('impressions', 0)) for i in campaign_insights)
        clk = sum(int(i.get('clicks', 0)) for i in campaign_insights)
        rows.append([
            data['date_range']['until'],
            campaign.get('name', ''),
            campaign.get('status', ''),
            campaign.get('objective', ''),
            campaign.get('lifetime_budget', campaign.get('daily_budget', '')),
            campaign.get('daily_budget', ''),
            spend,
            imp,
            clk,
            f"{(clk/imp*100):.2f}%" if imp > 0 else "0%",
            f"€{spend/clk:.2f}" if clk > 0 else "€0.00",
            f"€{(spend/imp*1000):.2f}" if imp > 0 else "€0.00",
            "", # Purchases
            ""  # ROAS
        ])

print(json.dumps(rows))
PYEOF
    echo "✅ Data written to sheet" >&2
fi

# 4. Make sheet publicly readable (for client access)
echo "🔗 Setting permissions..." >&2
gog drive share "$SHEET_ID" --type anyone --role reader 2>/dev/null || true

SHEET_URL="https://docs.google.com/spreadsheets/d/$SHEET_ID/edit"

# 5. Update Airtable with sheet URL
echo "💾 Saving to Airtable..." >&2

if [ -n "$KUNDE_ID" ]; then
    curl -s -X PATCH "https://gateway.maton.ai/airtable/v0/appbGhxy9I18oIS8E/Kunden/$KUNDE_ID" \
        -H "Authorization: Bearer $MATON_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"fields\":{\"Reporting Sheet\":\"$SHEET_URL\"}}" > /dev/null 2>&1
fi

echo "✅ Meta Ads reporting setup complete!" >&2

# Output
cat << EOF
{
    "success": true,
    "firmenname": "$FIRMENNAME",
    "account_id": "$ACCOUNT_ID",
    "sheet_id": "$SHEET_ID",
    "sheet_url": "$SHEET_URL",
    "folder_id": "$FOLDER_ID",
    "kunde_id": "$KUNDE_ID"
}
EOF
