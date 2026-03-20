#!/bin/bash
# Apollo Lead Import - Creates individual ClickUp tasks for each lead
# Usage: ./apollo-lead-import.sh "[Lead List Task ID]" "[ICP]" [Count]

set -e

# Config
APOLLO_KEY="${APOLLO_API_KEY:-$(cat ~/.config/apollo/api_key 2>/dev/null || echo "")}"
CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"

# Args
PARENT_TASK_ID="${1:-}"
ICP="${2:-}"
TARGET_COUNT="${3:-100}"

if [[ -z "$APOLLO_KEY" || -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: API keys not set"
    exit 1
fi

if [[ -z "$PARENT_TASK_ID" || -z "$ICP" ]]; then
    echo "Usage: $0 <Parent Lead List Task ID> <ICP> [Count]"
    echo "Example: $0 86c8e72xj 'Fashion DACH' 500"
    exit 1
fi

echo "🚀 Apollo Lead Import to ClickUp"
echo "   Parent Task: $PARENT_TASK_ID"
echo "   ICP: $ICP"
echo "   Target: $TARGET_COUNT leads"
echo ""

# Get the Lead List ID from the parent task
PARENT_TASK=$(curl -s "https://api.clickup.com/api/v2/task/${PARENT_TASK_ID}" \
    -H "Authorization: ${CLICKUP_KEY}")

LIST_ID=$(echo "$PARENT_TASK" | jq -r '.list.id')
LIST_NAME=$(echo "$PARENT_TASK" | jq -r '.list.name')

echo "   List: $LIST_NAME (ID: $LIST_ID)"
echo ""

# ICP Config
case "$ICP" in
    "Fashion DACH")
        TITLES='["CEO","Founder","E-commerce Manager","Managing Director","Geschäftsführer"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        ;;
    "Beauty DACH")
        TITLES='["CEO","Founder","Marketing Manager","Brand Manager"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        ;;
    "Home & Living")
        TITLES='["CEO","Founder","E-commerce Manager","Sales Manager"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        ;;
    "Food & Bev")
        TITLES='["CEO","Founder","E-commerce Manager","Managing Director"]'
        LOCATIONS='["Germany","Austria","Switzerland"]'
        ;;
    *)
        echo "❌ Unknown ICP: $ICP"
        exit 1
        ;;
esac

# Create folder for leads
IMPORT_FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/list/${LIST_ID}/folder" \
    -H "Authorization: ${CLICKUP_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"📂 ${ICP} - $(date +%d.%m.%Y)\"
    }")

FOLDER_ID=$(echo "$IMPORT_FOLDER" | jq -r '.id')

echo "📁 Created folder: ${ICP} - $(date +%d.%m.%Y)"
echo ""

# Fetch leads from Apollo
echo "📡 Fetching leads from Apollo..."

PAGE=1
COLLECTED=0
PER_PAGE=100
LEADS_DATA=""

while [[ $COLLECTED -lt $TARGET_COUNT ]]; do
    echo "   Page $PAGE..."
    
    RESPONSE=$(curl -s -X POST "https://api.apollo.io/api/v1/mixed_people/api_search" \
        -H "X-Api-Key: ${APOLLO_KEY}" \
        -H "Content-Type: application/json" \
        -d "{
            \"person_titles\": ${TITLES},
            \"person_locations\": ${LOCATIONS},
            \"per_page\": ${PER_PAGE},
            \"page\": ${PAGE}
        }")
    
    # Extract people
    PEOPLE=$(echo "$RESPONSE" | jq -c '.people[] // empty' 2>/dev/null)
    
    if [[ -z "$PEOPLE" ]]; then
        echo "   No more leads available"
        break
    fi
    
    # Process each person
    while IFS= read -r person; do
        if [[ $COLLECTED -ge $TARGET_COUNT ]]; then
            break
        fi
        
        PERSON_ID=$(echo "$person" | jq -r '.id')
        FIRST_NAME=$(echo "$person" | jq -r '.first_name // empty')
        LAST_NAME=$(echo "$person" | jq -r '.last_name // empty')
        TITLE=$(echo "$person" | jq -r '.title // empty')
        ORG_NAME=$(echo "$person" | jq -r '.organization.name // empty')
        HAS_EMAIL=$(echo "$person" | jq -r '.has_email // false')
        LINKEDIN=$(echo "$person" | jq -r '.linkedin_url // empty')
        
        # Create lead name
        LEAD_NAME="${FIRST_NAME} ${LAST_NAME}"
        if [[ -z "$LEAD_NAME" || "$LEAD_NAME" == " " ]]; then
            LEAD_NAME="Lead ${COLLECTED}"
        fi
        
        # Email status
        EMAIL_STATUS="unknown"
        if [[ "$HAS_EMAIL" == "true" ]]; then
            EMAIL_STATUS="available"
        fi
        
        # Create task in ClickUp
        TASK=$(curl -s -X POST "https://api.clickup.com/api/v2/list/${LIST_ID}/task" \
            -H "Authorization: ${CLICKUP_KEY}" \
            -H "Content-Type: application/json" \
            -d "{
                \"name\": \"👤 ${LEAD_NAME}\",
                \"description\": \"**Title:** ${TITLE}\\n\\n**Company:** ${ORG_NAME}\\n\\n**LinkedIn:** ${LINKEDIN}\\n\\n**Apollo ID:** ${PERSON_ID}\",
                \"parent\": \"${FOLDER_ID}\",
                \"custom_fields\": [
                    {\"name\": \"Lead Name\", \"value\": \"${LEAD_NAME}\"},
                    {\"name\": \"First Name\", \"value\": \"${FIRST_NAME}\"},
                    {\"name\": \"Last Name\", \"value\": \"${LAST_NAME}\"},
                    {\"name\": \"Title\", \"value\": \"${TITLE}\"},
                    {\"name\": \"Company\", \"value\": \"${ORG_NAME}\"},
                    {\"name\": \"LinkedIn URL\", \"value\": \"${LINKEDIN}\"},
                    {\"name\": \"Apollo ID\", \"value\": \"${PERSON_ID}\"},
                    {\"name\": \"ICP Segment\", \"value\": \"${ICP}\"},
                    {\"name\": \"Email Status\", \"value\": \"${EMAIL_STATUS}\"},
                    {\"name\": \"Lead Status\", \"value\": \"New\"}
                ]
            }" 2>/dev/null)
        
        COLLECTED=$((COLLECTED + 1))
        
        if [[ $((COLLECTED % 10)) -eq 0 ]]; then
            echo -ne "\r   Created: $COLLECTED leads"
        fi
        
        # Rate limiting
        sleep 0.3
        
    done <<< "$PEOPLE"
    
    if [[ $COLLECTED -ge $TARGET_COUNT ]]; then
        break
    fi
    
    PAGE=$((PAGE + 1))
    
    # Safety break
    if [[ $PAGE -gt 20 ]]; then
        echo "⚠️  Reached max pages"
        break
    fi
done

echo ""
echo ""
echo "✅ Created $COLLECTED individual lead tasks"
echo ""

# Update parent task
curl -s -X PUT "https://api.clickup.com/api/v2/task/${PARENT_TASK_ID}" \
    -H "Authorization: ${CLICKUP_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
        \"custom_fields\": [
            {\"name\": \"Total Leads\", \"value\": ${COLLECTED}},
            {\"name\": \"Upload Date\", \"value\": \"$(date +%Y-%m-%d)\"},
            {\"name\": \"Validated\", \"value\": true}
        ]
    }" > /dev/null

echo "📊 Updated parent task with count: $COLLECTED"
echo ""
echo "🔗 View leads: https://app.clickup.com/${LIST_ID}"
echo ""
echo "Next steps:"
echo "1. Review leads in ClickUp"
echo "2. Enrich emails: ./apollo-enrich-leads.sh ${FOLDER_ID}"
echo "3. Create campaign from folder"
