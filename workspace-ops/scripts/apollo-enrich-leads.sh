#!/bin/bash
# Apollo Email Enrichment - Enriches emails for leads with status "available"
# Usage: ./apollo-enrich-leads.sh [Lead List ID] [Limit]

set -e

APOLLO_KEY="${APOLLO_API_KEY:-$(cat ~/.config/apollo/api_key 2>/dev/null || echo "")}"
CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"

LIST_ID="${1:-901521519130}"  # Default: Lead Lists
LIMIT="${2:-50}"  # Default: 50 leads per run

if [[ -z "$APOLLO_KEY" || -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: API keys not set"
    exit 1
fi

echo "🚀 Apollo Email Enrichment"
echo "   List ID: $LIST_ID"
echo "   Limit: $LIMIT leads"
echo ""

# Get leads with "available" email status
echo "📡 Fetching leads with available emails..."

LEADS=$(curl -s "https://api.clickup.com/api/v2/list/${LIST_ID}/task?custom_fields=%5B%7B%22field_id%22%3A%222bab6630-5eec-4a43-95f0-f5e85ec31b33%22%2C%22value%22%3A%22available%22%7D%5D&page=0" \
    -H "Authorization: ${CLICKUP_KEY}")

# Count leads
LEAD_COUNT=$(echo "$LEADS" | jq -r '.tasks | length')
echo "   Found $LEAD_COUNT leads with available emails"
echo ""

if [[ "$LEAD_COUNT" -eq 0 ]]; then
    echo "⚠️  No leads with 'available' email status found"
    echo "   Run lead import first or check lead status"
    exit 0
fi

# Process leads
ENRICHED=0

echo "$LEADS" | jq -c '.tasks[:'$LIMIT']' | jq -c '.[]' | while read -r lead; do
    TASK_ID=$(echo "$lead" | jq -r '.id')
    TASK_NAME=$(echo "$lead" | jq -r '.name')
    APOLLO_ID=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Apollo ID").value // empty')
    
    if [[ -z "$APOLLO_ID" || "$APOLLO_ID" == "null" ]]; then
        echo "   ⚠️  Skipping $TASK_NAME - no Apollo ID"
        continue
    fi
    
    echo "   Enriching: $TASK_NAME (Apollo: $APOLLO_ID)"
    
    # Update status to "Enriching"
    curl -s -X PUT "https://api.clickup.com/api/v2/task/${TASK_ID}" \
        -H "Authorization: ${CLICKUP_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "custom_fields": [
                {"name": "Email Status", "value": "enriching"}
            ]
        }' > /dev/null
    
    # Get email from Apollo
    PERSON_DATA=$(curl -s "https://api.apollo.io/v1/people/${APOLLO_ID}?reveal_email=true" \
        -H "X-Api-Key: ${APOLLO_KEY}")
    
    EMAIL=$(echo "$PERSON_DATA" | jq -r '.person.email // empty')
    
    if [[ -n "$EMAIL" && "$EMAIL" != "null" ]]; then
        echo "     ✉️  Found: $EMAIL"
        
        # Update ClickUp with email
        curl -s -X PUT "https://api.clickup.com/api/v2/task/${TASK_ID}" \
            -H "Authorization: ${CLICKUP_KEY}" \
            -H "Content-Type: application/json" \
            -d "{
                \"custom_fields\": [
                    {\"name\": \"Email\", \"value\": \"${EMAIL}\"},
                    {\"name\": \"Email Status\", \"value\": \"enriched\"}
                ]
            }" > /dev/null
        
        ENRICHED=$((ENRICHED + 1))
    else
        echo "     ❌ No email found"
        
        # Update status to unknown
        curl -s -X PUT "https://api.clickup.com/api/v2/task/${TASK_ID}" \
            -H "Authorization: ${CLICKUP_KEY}" \
            -H "Content-Type: application/json" \
            -d '{
                "custom_fields": [
                    {"name": "Email Status", "value": "unknown"}
                ]
            }' > /dev/null
    fi
    
    # Rate limiting
    sleep 0.5
done

echo ""
echo "✅ Enrichment complete!"
echo "   Enriched: $ENRICHED emails"
echo ""
echo "Next steps:"
echo "1. Review enriched leads in ClickUp"
echo "2. Mark ready leads: Lead Status → Ready"
echo "3. Create campaign from ready leads"
