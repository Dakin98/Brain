#!/bin/bash
# Apollo Reply Sync - Polls Apollo for new replies and creates ClickUp tasks
# Usage: ./apollo-reply-sync.sh
# Cron: */15 * * * *

set -e

# Config
APOLLO_KEY="${APOLLO_API_KEY:-$(cat ~/.config/apollo/api_key 2>/dev/null || echo "")}"
CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
REPLY_LIST_ID="901521519132"
CAMPAIGNS_LIST_ID="901521519128"
STATE_FILE="${HOME}/.apollo_reply_sync.state"

if [[ -z "$APOLLO_KEY" || -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: API keys not configured"
    exit 1
fi

# Get last check time
LAST_CHECK=$(cat "$STATE_FILE" 2>/dev/null || echo "2026-02-01T00:00:00Z")
CURRENT_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "🔄 Apollo Reply Sync"
echo "   Last check: $LAST_CHECK"
echo "   Current: $CURRENT_TIME"
echo ""

# Note: Apollo doesn't have a public "replies" endpoint in the standard API
# This script assumes you have access to Apollo's emailer API or use webhooks
# For now, we'll create a framework that can be adapted

echo "⚠️  Note: Apollo Emailer API access required for automatic reply sync"
echo "   Alternative: Manual import via CSV or Zapier/Make integration"
echo ""

# Manual Reply Import Function
import_manual_replies() {
    local CSV_FILE="${1:-replies.csv}"
    
    if [[ ! -f "$CSV_FILE" ]]; then
        echo "❌ CSV file not found: $CSV_FILE"
        echo "Expected columns: email, name, company, campaign, reply_text, date"
        return 1
    fi
    
    echo "📥 Importing replies from $CSV_FILE..."
    
    # Process CSV (skip header)
    tail -n +2 "$CSV_FILE" | while IFS=',' read -r email name company campaign reply_text date; do
        # Clean up fields
        email=$(echo "$email" | tr -d '"')
        name=$(echo "$name" | tr -d '"')
        company=$(echo "$company" | tr -d '"')
        campaign=$(echo "$campaign" | tr -d '"')
        reply_text=$(echo "$reply_text" | tr -d '"')
        
        # Classify reply
        reply_lower=$(echo "$reply_text" | tr '[:upper:]' '[:lower:]')
        
        if [[ "$reply_lower" =~ (interested|call|meeting|book|schedule|demo|price|quote) ]]; then
            TYPE="Interested"
            PRIORITY=2  # High
            EMOJI="🔥"
        elif [[ "$reply_lower" =~ (how|what|when|where|why|\?) ]]; then
            TYPE="Question"
            PRIORITY=3  # Normal
            EMOJI="❓"
        elif [[ "$reply_lower" =~ (not interested|no thanks|unsubscribe|remove|stop) ]]; then
            TYPE="Not Interested"
            PRIORITY=4  # Low
            EMOJI="❌"
        elif [[ "$reply_lower" =~ (out of office|vacation|away|ooo) ]]; then
            TYPE="OOO"
            PRIORITY=4  # Low
            EMOJI="🏖️"
        elif [[ "$reply_lower" =~ (refer|forward|colleague) ]]; then
            TYPE="Referral"
            PRIORITY=2  # High
            EMOJI="🔗"
        else
            TYPE="Other"
            PRIORITY=3
            EMOJI="💬"
        fi
        
        # Create ClickUp task
        echo "   Creating task: $EMOJI $name ($TYPE)"
        
        curl -s -X POST "https://api.clickup.com/api/v2/list/${REPLY_LIST_ID}/task" \
            -H "Authorization: ${CLICKUP_KEY}" \
            -H "Content-Type: application/json" \
            -d "{
                \"name\": \"${EMOJI} Reply: ${name}\",
                \"description\": \"**Campaign:** ${campaign}\\n\\n**Reply:**\\n${reply_text}\",
                \"priority\": ${PRIORITY},
                \"due_date\": $(if [[ "$TYPE" == "Interested" ]]; then echo "$(date -v+4H +%s)000"; else echo "null"; fi),
                \"custom_fields\": [
                    {\"name\": \"Lead Name\", \"value\": \"${name}\"},
                    {\"name\": \"Email\", \"value\": \"${email}\"},
                    {\"name\": \"Company\", \"value\": \"${company}\"},
                    {\"name\": \"Campaign\", \"value\": \"${campaign}\"},
                    {\"name\": \"Reply Type\", \"value\": \"${TYPE}\"},
                    {\"name\": \"Reply Snippet\", \"value\": \"${reply_text:0:200}\"}
                ]
            }" > /dev/null
        
        sleep 0.2
    done
    
    echo "✅ Import complete"
}

# Check if CSV file provided
if [[ -n "$1" ]]; then
    import_manual_replies "$1"
else
    echo "Usage:"
    echo "  Automatic sync: ./apollo-reply-sync.sh (requires Apollo Emailer API)"
    echo "  Manual import:  ./apollo-reply-sync.sh replies.csv"
    echo ""
    echo "CSV Format: email,name,company,campaign,reply_text,date"
    echo ""
    echo "To enable automatic sync, you need:"
    echo "1. Apollo Emailer API access (enterprise plan)"
    echo "2. Webhook setup from Apollo to your endpoint"
    echo "3. Or use Zapier/Make to bridge Apollo → ClickUp"
fi

# Save state
echo "$CURRENT_TIME" > "$STATE_FILE"
