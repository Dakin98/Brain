#!/bin/bash
# ClickUp Campaign → Apollo Sync
# Creates Apollo campaign when ClickUp campaign status changes to "Active"
# Usage: ./campaign-apollo-sync.sh [Campaign Task ID]

set -e

# Config
APOLLO_KEY="${APOLLO_API_KEY:-$(cat ~/.config/apollo/api_key 2>/dev/null || echo "")}"
CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"

CAMPAIGN_TASK_ID="${1:-}"

if [[ -z "$APOLLO_KEY" || -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: API keys not set"
    exit 1
fi

if [[ -z "$CAMPAIGN_TASK_ID" ]]; then
    echo "Usage: $0 <Campaign Task ID>"
    echo "Example: $0 86c8e72xj"
    echo ""
    echo "This script will:"
    echo "1. Get campaign details from ClickUp"
    echo "2. Get leads from associated Lead List"
    echo "3. Create Apollo sequence"
    echo "4. Create Apollo campaign"
    echo "5. Import leads to Apollo"
    echo "6. Update ClickUp with Apollo Campaign ID"
    exit 1
fi

echo "🚀 ClickUp → Apollo Campaign Sync"
echo "   Campaign Task ID: $CAMPAIGN_TASK_ID"
echo ""

# ============================================================
# STEP 1: Get Campaign Details from ClickUp
# ============================================================
echo "📡 Step 1: Fetching campaign from ClickUp..."

CAMPAIGN_TASK=$(curl -s "https://api.clickup.com/api/v2/task/${CAMPAIGN_TASK_ID}" \
    -H "Authorization: ${CLICKUP_KEY}")

# Extract fields
CAMPAIGN_NAME=$(echo "$CAMPAIGN_TASK" | jq -r '.name')
ICP_SEGMENT=$(echo "$CAMPAIGN_TASK" | jq -r '.custom_fields[] | select(.name=="ICP Segment").value // empty')
SEQUENCE_NAME=$(echo "$CAMPAIGN_TASK" | jq -r '.custom_fields[] | select(.name=="Sequence").value // empty')
DAILY_LIMIT=$(echo "$CAMPAIGN_TASK" | jq -r '.custom_fields[] | select(.name=="Daily Send Limit").value // 40')
LEAD_COUNT=$(echo "$CAMPAIGN_TASK" | jq -r '.custom_fields[] | select(.name=="Lead Count").value // 0')

# Get sequence details from description or linked task
echo "   Campaign: $CAMPAIGN_NAME"
echo "   ICP: $ICP_SEGMENT"
echo "   Daily Limit: $DAILY_LIMIT"
echo "   Target Leads: $LEAD_COUNT"
echo ""

# ============================================================
# STEP 2: Get Leads from Lead Lists (Ready Status)
# ============================================================
echo "📡 Step 2: Fetching leads from ClickUp..."

# Find leads with matching ICP and Ready status
LEADS_LIST_ID="901521519130"

# Get all leads with Ready status and matching ICP
LEADS=$(curl -s "https://api.clickup.com/api/v2/list/${LEADS_LIST_ID}/task?page=0" \
    -H "Authorization: ${CLICKUP_KEY}")

# Filter leads manually (ClickUp API filtering is limited)
READY_LEADS=$(echo "$LEADS" | jq -c '.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "Ready")' 2>/dev/null | head -n "$LEAD_COUNT")

LEAD_ARRAY=()
while IFS= read -r lead; do
    if [[ -n "$lead" ]]; then
        FIRST_NAME=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="First Name").value // empty')
        LAST_NAME=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Last Name").value // empty')
        EMAIL=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Email").value // empty')
        COMPANY=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Company").value // empty')
        TITLE=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Title").value // empty')
        
        if [[ -n "$EMAIL" && "$EMAIL" != "null" && "$EMAIL" != "empty" ]]; then
            LEAD_ARRAY+=("{\"first_name\":\"${FIRST_NAME}\",\"last_name\":\"${LAST_NAME}\",\"email\":\"${EMAIL}\",\"organization_name\":\"${COMPANY}\",\"title\":\"${TITLE}\"}")
        fi
    fi
done <<< "$READY_LEADS"

TOTAL_LEADS=${#LEAD_ARRAY[@]}
echo "   Found $TOTAL_LEADS leads with emails"

if [[ $TOTAL_LEADS -eq 0 ]]; then
    echo "❌ No leads found with Ready status and email"
    echo "   Make sure to:"
    echo "   1. Import leads with apollo-lead-import.sh"
    echo "   2. Enrich emails with apollo-enrich-leads.sh"
    echo "   3. Set Lead Status to Ready"
    exit 1
fi
echo ""

# ============================================================
# STEP 3: Get Sequence Template
# ============================================================
echo "📡 Step 3: Getting sequence template..."

# Default 5-step sequence
SEQUENCE_TEMPLATE='{
  "name": "'"$CAMPAIGN_NAME"'",
  "active": true,
  "steps": [
    {
      "step_number": 1,
      "wait_days": 0,
      "type": "email",
      "subject": "{{company}} + Meta Ads Question",
      "body": "Hi {{first_name}},\n\nSaw {{company}} is scaling fast in the DACH market.\n\nQuick question: Are you currently testing any new creative angles for your Meta Ads?\n\nReason I ask: We just helped a similar brand increase their ROAS by 40% with a specific video hook that might work for {{company}} too.\n\nWorth a 5-min chat?\n\nBest,\nDeniz"
    },
    {
      "step_number": 2,
      "wait_days": 3,
      "type": "email", 
      "subject": "Re: {{company}} + Meta Ads Question",
      "body": "Hi {{first_name}},\n\nQuick follow-up.\n\nI put together a 2-min Loom showing exactly how we structured the winning creative:\n\n[VIDEO LINK]\n\nThe key insight: We stopped selling the product and started selling the transformation.\n\nWant me to send over the full case study?\n\nDeniz"
    },
    {
      "step_number": 3,
      "wait_days": 7,
      "type": "email",
      "subject": "Case study: 40% ROAS increase", 
      "body": "Hi {{first_name}},\n\nStill thinking about your Meta Ads strategy.\n\nHere\'s the case study: [LINK]\n\nKey results:\n• 40% ROAS increase in 30 days\n• 25% lower CAC\n• 3 winning creatives identified\n\nThe best part: It worked without increasing ad spend.\n\nOpen to a quick call to see if this could work for {{company}}?\n\nDeniz"
    },
    {
      "step_number": 4,
      "wait_days": 12,
      "type": "email",
      "subject": "Should I close your file?",
      "body": "Hi {{first_name}},\n\nI don\'t want to be that guy who keeps emailing if there\'s no interest.\n\nShould I close your file or is Meta Ads optimization still on your radar for Q2?\n\nEither way, all good.\n\nDeniz"
    },
    {
      "step_number": 5,
      "wait_days": 18,
      "type": "email",
      "subject": "Last try → {{company}} growth",
      "body": "{{first_name}},\n\nThis is my last email.\n\nIf you\'re not interested in exploring how to scale {{company}}\'s Meta Ads efficiently, I totally understand.\n\nIf you change your mind, just reply \"interested\" and I\'ll send over the case study.\n\nAll the best,\nDeniz"
    }
  ]
}'

echo "   Sequence: 5 steps"
echo ""

# ============================================================
# STEP 4: Create Apollo Sequence
# ============================================================
echo "📡 Step 4: Creating Apollo sequence..."

# Note: Apollo API for sequences might be limited
# This is a simplified version - actual implementation depends on Apollo API access level

SEQUENCE_RESPONSE=$(curl -s -X POST "https://api.apollo.io/api/v1/sequences" \
    -H "X-Api-Key: ${APOLLO_KEY}" \
    -H "Content-Type: application/json" \
    -d "$SEQUENCE_TEMPLATE" 2>/dev/null || echo '{"id": null}')

SEQUENCE_ID=$(echo "$SEQUENCE_RESPONSE" | jq -r '.id // empty')

if [[ -n "$SEQUENCE_ID" && "$SEQUENCE_ID" != "null" ]]; then
    echo "   ✅ Sequence created: $SEQUENCE_ID"
else
    echo "   ⚠️  Sequence API limited or failed"
    echo "   Manual step: Create sequence in Apollo UI"
    SEQUENCE_ID="MANUAL"
fi
echo ""

# ============================================================
# STEP 5: Import Leads to Apollo
# ============================================================
echo "📡 Step 5: Importing leads to Apollo..."

# Build leads JSON
LEADS_JSON="["
first=true
for lead in "${LEAD_ARRAY[@]}"; do
    [[ "$first" == true ]] && first=false || LEADS_JSON+=","
    LEADS_JSON+="$lead"
done
LEADS_JSON+="]"

# Save to temp file for debugging
echo "$LEADS_JSON" > "/tmp/apollo_leads_${CAMPAIGN_TASK_ID}.json"

# Import to Apollo
IMPORT_RESPONSE=$(curl -s -X POST "https://api.apollo.io/api/v1/contacts/bulk_create" \
    -H "X-Api-Key: ${APOLLO_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"contacts\": $LEADS_JSON}" 2>/dev/null || echo '{"status": "error"}')

IMPORT_STATUS=$(echo "$IMPORT_RESPONSE" | jq -r '.status // "unknown"')
IMPORT_COUNT=$(echo "$IMPORT_RESPONSE" | jq -r '.contacts_created // 0')

echo "   Status: $IMPORT_STATUS"
echo "   Imported: $IMPORT_COUNT contacts"
echo ""

# ============================================================
# STEP 6: Create Apollo Campaign (if API available)
# ============================================================
echo "📡 Step 6: Creating Apollo campaign..."

# Note: Apollo Campaign API might be enterprise-only
# Fallback: Provide manual instructions

CAMPAIGN_RESPONSE=$(curl -s -X POST "https://api.apollo.io/api/v1/engagement_campaigns" \
    -H "X-Api-Key: ${APOLLO_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"${CAMPAIGN_NAME}\",
        \"sequence_id\": \"${SEQUENCE_ID}\",
        \"daily_limit\": ${DAILY_LIMIT},
        \"active\": true
    }" 2>/dev/null || echo '{"id": null}')

APOLLO_CAMPAIGN_ID=$(echo "$CAMPAIGN_RESPONSE" | jq -r '.id // empty')

if [[ -n "$APOLLO_CAMPAIGN_ID" && "$APOLLO_CAMPAIGN_ID" != "null" ]]; then
    echo "   ✅ Apollo campaign created: $APOLLO_CAMPAIGN_ID"
    echo ""
    
    # Update ClickUp with Apollo Campaign ID
    echo "📡 Step 7: Updating ClickUp..."
    curl -s -X PUT "https://api.clickup.com/api/v2/task/${CAMPAIGN_TASK_ID}" \
        -H "Authorization: ${CLICKUP_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
            \"custom_fields\": [
                {\"name\": \"Apollo Campaign ID\", \"value\": \"${APOLLO_CAMPAIGN_ID}\"},
                {\"name\": \"Campaign Status\", \"value\": \"Active\"},
                {\"name\": \"Launch Date\", \"value\": \"$(date +%Y-%m-%d)\"}
            ]
        }" > /dev/null
    
    echo "   ✅ ClickUp updated with Apollo Campaign ID"
    echo ""
    
    echo "🎉 SYNC COMPLETE!"
    echo ""
    echo "Campaign is now LIVE in Apollo:"
    echo "   Apollo Campaign ID: $APOLLO_CAMPAIGN_ID"
    echo "   Leads imported: $IMPORT_COUNT"
    echo "   Daily limit: $DAILY_LIMIT"
    echo ""
    echo "Links:"
    echo "   ClickUp: https://app.clickup.com/t/${CAMPAIGN_TASK_ID}"
    echo "   Apollo: https://app.apollo.io/#/campaigns/${APOLLO_CAMPAIGN_ID}"
    
else
    echo "   ⚠️  Apollo Campaign API not available or failed"
    echo ""
    echo "📝 MANUAL SETUP REQUIRED"
    echo ""
    echo "ClickUp is ready. Now manually in Apollo:"
    echo ""
    echo "1. Go to: https://app.apollo.io/#/sequences"
    echo "2. Create sequence: '$CAMPAIGN_NAME'"
    echo "3. Add 5 steps (copy from ClickUp task description)"
    echo ""
    echo "4. Go to: https://app.apollo.io/#/campaigns"
    echo "5. Create campaign: '$CAMPAIGN_NAME'"
    echo "6. Select sequence"
    echo "7. Import leads: /tmp/apollo_leads_${CAMPAIGN_TASK_ID}.json"
    echo "8. Set daily limit: $DAILY_LIMIT"
    echo "9. Launch campaign"
    echo ""
    echo "10. Copy Apollo Campaign ID back to ClickUp"
    
    # Save leads for manual import
    echo ""
    echo "💾 Leads saved to: /tmp/apollo_leads_${CAMPAIGN_TASK_ID}.json"
    echo "   (Ready for manual import to Apollo)"
fi

echo ""
