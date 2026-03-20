#!/bin/bash
# Campaign Analytics - Updates ClickUp with campaign performance metrics
# Usage: ./campaign-analytics.sh
# Cron: 0 9 * * * (daily 9am)

set -e

# Config
CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
CAMPAIGNS_LIST_ID="901521519128"

if [[ -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: CLICKUP_API_TOKEN not set"
    exit 1
fi

TODAY=$(date +%Y-%m-%d)
echo "📊 Campaign Analytics Update - $TODAY"
echo ""

# Get all active campaigns
echo "📡 Fetching active campaigns from ClickUp..."
CAMPAIGNS=$(curl -s "https://api.clickup.com/api/v2/list/${CAMPAIGNS_LIST_ID}/task?statuses%5B%5D=Active&include_closed=false" \
    -H "Authorization: ${CLICKUP_KEY}")

# Check if any campaigns found
CAMPAIGN_COUNT=$(echo "$CAMPAIGNS" | jq -r '.tasks | length')
if [[ "$CAMPAIGN_COUNT" == "0" ]]; then
    echo "⚠️  No active campaigns found"
    exit 0
fi

echo "   Found $CAMPAIGN_COUNT active campaign(s)"
echo ""

# Process each campaign
echo "$CAMPAIGNS" | jq -c '.tasks[]' | while read -r campaign; do
    TASK_ID=$(echo "$campaign" | jq -r '.id')
    TASK_NAME=$(echo "$campaign" | jq -r '.name')
    
    echo "📝 Updating: $TASK_NAME"
    
    # Get current stats from custom fields
    LEAD_COUNT=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Lead Count").value // 0')
    
    # Simulate metrics (in real scenario, these come from Apollo or your email tool)
    # For Apollo users with Emailer API:
    # STATS=$(curl -s "https://api.apollo.io/api/v1/emailer_campaigns/${APOLLO_CAMPAIGN_ID}/stats" -H "X-Api-Key: ...")
    
    # For now, we'll use placeholder logic or manual input
    # In production, integrate with your actual email sending tool (Apollo, Instantly, etc.)
    
    echo "   Leads: $LEAD_COUNT"
    
    # If manual metrics are provided via arguments or file
    if [[ -f "/tmp/campaign_stats_${TASK_ID}.json" ]]; then
        STATS=$(cat "/tmp/campaign_stats_${TASK_ID}.json")
        SENT=$(echo "$STATS" | jq -r '.sent // 0')
        OPENED=$(echo "$STATS" | jq -r '.opened // 0')
        REPLIED=$(echo "$STATS" | jq -r '.replied // 0')
        MEETINGS=$(echo "$STATS" | jq -r '.meetings // 0')
        
        # Calculate rates
        if [[ $SENT -gt 0 ]]; then
            OPEN_RATE=$(echo "scale=1; ($OPENED / $SENT) * 100" | bc)
            REPLY_RATE=$(echo "scale=1; ($REPLIED / $SENT) * 100" | bc)
            MEETING_RATE=$(echo "scale=2; ($MEETINGS / $SENT) * 100" | bc)
        else
            OPEN_RATE=0
            REPLY_RATE=0
            MEETING_RATE=0
        fi
        
        echo "   Open Rate: ${OPEN_RATE}%"
        echo "   Reply Rate: ${REPLY_RATE}%"
        echo "   Meeting Rate: ${MEETING_RATE}%"
        
        # Update ClickUp
        curl -s -X PUT "https://api.clickup.com/api/v2/task/${TASK_ID}" \
            -H "Authorization: ${CLICKUP_KEY}" \
            -H "Content-Type: application/json" \
            -d "{
                \"custom_fields\": [
                    {\"name\": \"Reply Rate %\", \"value\": ${REPLY_RATE}},
                    {\"name\": \"Meeting Rate %\", \"value\": ${MEETING_RATE}}
                ]
            }" > /dev/null
        
        # Remove temp file
        rm "/tmp/campaign_stats_${TASK_ID}.json"
    else
        echo "   ℹ️  No stats file found. Skipping update."
        echo "      To update, create: /tmp/campaign_stats_${TASK_ID}.json"
        echo '      {"sent": 100, "opened": 45, "replied": 5, "meetings": 1}'
    fi
    
    echo ""
done

echo "✅ Campaign analytics update complete"
echo ""
echo "To integrate with your email tool:"
echo "1. Apollo: Use /emailer_campaigns/{id}/stats endpoint"
echo "2. Instantly: Use their API or webhook"
echo "3. Smartlead: Use their campaign stats API"
echo "4. Or export stats CSV and use: ./campaign-analytics-import.sh stats.csv"
