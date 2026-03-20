#!/bin/bash
# Apollo Lead Search Script for ClickUp Integration
# Usage: ./apollo-lead-search.sh "List Task ID" "ICP" "Target Count"

set -e

# Config
APOLLO_KEY="${APOLLO_API_KEY:-$(cat ~/.config/apollo/api_key 2>/dev/null || echo "")}"
CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
LEAD_LISTS_ID="901521519130"

# Args
LIST_TASK_ID="${1:-}"
ICP="${2:-}"
TARGET_COUNT="${3:-100}"

if [[ -z "$APOLLO_KEY" ]]; then
    echo "❌ Error: APOLLO_API_KEY not set"
    exit 1
fi

if [[ -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: CLICKUP_API_TOKEN not set"
    exit 1
fi

if [[ -z "$LIST_TASK_ID" || -z "$ICP" ]]; then
    echo "Usage: $0 <ClickUp Task ID> <ICP> [Target Count]"
    echo "Example: $0 86c8e72xj 'Fashion DACH' 500"
    exit 1
fi

echo "🚀 Starting Apollo Lead Search..."
echo "   Task ID: $LIST_TASK_ID"
echo "   ICP: $ICP"
echo "   Target: $TARGET_COUNT leads"
echo ""

# ICP Config
case "$ICP" in
    "Fashion DACH")
        TITLES='["CEO","Founder","E-commerce Manager","Managing Director"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        INDUSTRIES='["5567e0c57369640002a301c0","5567e0c67369640002a302c0"]'  # Fashion tags
        ;;
    "Beauty DACH")
        TITLES='["CEO","Founder","Marketing Manager","Brand Manager"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        INDUSTRIES='["5567e0c57369640002a301c0"]'  # Beauty/Fashion
        ;;
    "Home & Living")
        TITLES='["CEO","Founder","E-commerce Manager","Sales Manager"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        INDUSTRIES='["5567e0c47369640002a300c0"]'  # Home goods
        ;;
    "Food & Bev")
        TITLES='["CEO","Founder","E-commerce Manager"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        INDUSTRIES='["5567e0c47369640002a30000"]'  # Food/Beverage
        ;;
    *)
        echo "❌ Unknown ICP: $ICP"
        echo "Available: Fashion DACH, Beauty DACH, Home & Living, Food & Bev"
        exit 1
        ;;
esac

# Create temp file for leads
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

echo "📡 Fetching leads from Apollo..."

# Pagination variables
PAGE=1
COLLECTED=0
PER_PAGE=100

while [[ $COLLECTED -lt $TARGET_COUNT ]]; do
    echo "   Page $PAGE..."
    
    # Apollo API Call
    RESPONSE=$(curl -s -X POST "https://api.apollo.io/api/v1/mixed_people/api_search" \
        -H "X-Api-Key: ${APOLLO_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
            \"person_titles\": ${TITLES},
            \"person_locations\": ${LOCATIONS},
            \"per_page\": ${PER_PAGE},
            \"page\": ${PAGE}
        }")
    
    # Check for errors
    if echo "$RESPONSE" | grep -q '"error"'; then
        echo "❌ API Error: $(echo "$RESPONSE" | jq -r '.error // .error_message // "Unknown"')"
        break
    fi
    
    # Extract people
    PEOPLE=$(echo "$RESPONSE" | jq -c '.people[] // empty' 2>/dev/null)
    
    if [[ -z "$PEOPLE" ]]; then
        echo "   No more leads available"
        break
    fi
    
    # Process each person
    echo "$PEOPLE" | while read -r person; do
        PERSON_ID=$(echo "$person" | jq -r '.id')
        FIRST_NAME=$(echo "$person" | jq -r '.first_name // empty')
        LAST_NAME=$(echo "$person" | jq -r '.last_name // empty')
        TITLE=$(echo "$person" | jq -r '.title // empty')
        ORG_NAME=$(echo "$person" | jq -r '.organization.name // empty')
        HAS_EMAIL=$(echo "$person" | jq -r '.has_email // false')
        LINKEDIN=$(echo "$person" | jq -r '.linkedin_url // empty')
        
        # Build JSON object
        echo "{
            \"apollo_id\": \"$PERSON_ID\",
            \"first_name\": \"$FIRST_NAME\",
            \"last_name\": \"$LAST_NAME\",
            \"name\": \"$FIRST_NAME $LAST_NAME\",
            \"title\": \"$TITLE\",
            \"company\": \"$ORG_NAME\",
            \"has_email\": $HAS_EMAIL,
            \"linkedin_url\": \"$LINKEDIN\",
            \"icp\": \"$ICP\"
        }" >> "$TEMP_FILE"
        
        echo "$TEMP_FILE" | wc -l | xargs -I {} echo -ne "\r   Collected: {}"
    done
    
    COLLECTED=$(cat "$TEMP_FILE" | wc -l)
    echo ""
    
    if [[ $COLLECTED -ge $TARGET_COUNT ]]; then
        break
    fi
    
    PAGE=$((PAGE + 1))
    sleep 0.5  # Rate limiting
    
    # Safety break
    if [[ $PAGE -gt 20 ]]; then
        echo "⚠️  Reached max pages (20)"
        break
    fi
done

FINAL_COUNT=$(cat "$TEMP_FILE" | wc -l)
echo ""
echo "✅ Collected $FINAL_COUNT leads"

# Convert to proper JSON array
echo "[$TEMP_FILE]"
echo "📝 Processing and validating..."

# Create JSON file with array structure
LEADS_FILE="/tmp/leads_${LIST_TASK_ID}_$(date +%s).json"
echo '{"leads":[' > "$LEADS_FILE"
first=true
while read -r line; do
    [[ "$first" == true ]] && first=false || echo "," >> "$LEADS_FILE"
    echo -n "$line" >> "$LEADS_FILE"
done < "$TEMP_FILE"
echo ']}' >> "$LEADS_FILE"

echo "💾 Saved to: $LEADS_FILE"

# Update ClickUp Task
echo "📤 Updating ClickUp..."

# Upload as attachment
curl -s -X POST "https://api.clickup.com/api/v2/task/${LIST_TASK_ID}/attachment" \
    -H "Authorization: ${CLICKUP_KEY}" \
    -F "filename=leads.json" \
    -F "file=@${LEADS_FILE}"

# Update custom fields
TODAY=$(date +%Y-%m-%d)
curl -s -X PUT "https://api.clickup.com/api/v2/task/${LIST_TASK_ID}" \
    -H "Authorization: ${CLICKUP_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
        \"custom_fields\": [
            {\"name\": \"Total Leads\", \"value\": ${FINAL_COUNT}},
            {\"name\": \"Upload Date\", \"value\": \"${TODAY}\"},
            {\"name\": \"Source\", \"value\": \"Apollo\"}
        ]
    }" > /dev/null

echo ""
echo "✅ Done! ClickUp task updated."
echo "🔗 Task: https://app.clickup.com/t/${LIST_TASK_ID}"
echo ""
echo "Next steps:"
echo "1. Validate leads: ./lead-validation.sh ${LIST_TASK_ID}"
echo "2. Enrich emails (optional): ./apollo-enrich-emails.sh ${LIST_TASK_ID}"
echo "3. Create campaign: ./campaign-setup.sh ${LIST_TASK_ID}"
