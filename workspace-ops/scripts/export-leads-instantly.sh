#!/bin/bash
# Export ClickUp Leads to Instantly CSV Format
# Usage: ./export-leads-instantly.sh [Lead List ID] [Status Filter]

set -e

CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
LEAD_LIST_ID="${1:-901521519130}"
STATUS_FILTER="${2:-Ready}"  # Default: Ready leads only

if [[ -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: CLICKUP_API_TOKEN not set"
    exit 1
fi

echo "🚀 Exporting Leads for Instantly"
echo "   List ID: $LEAD_LIST_ID"
echo "   Status Filter: $STATUS_FILTER"
echo ""

# Fetch leads from ClickUp
echo "📡 Fetching leads..."

# Get all tasks from list
TASKS=$(curl -s "https://api.clickup.com/api/v2/list/${LEAD_LIST_ID}/task?page=0" \
    -H "Authorization: ${CLICKUP_KEY}")

# Filter by status manually (since API filtering can be tricky)
FILTERED_LEADS=$(echo "$TASKS" | jq -c '.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "'"$STATUS_FILTER"'")')

LEAD_COUNT=$(echo "$FILTERED_LEADS" | jq -s 'length')

echo "   Found $LEAD_COUNT leads with status: $STATUS_FILTER"
echo ""

if [[ "$LEAD_COUNT" -eq 0 ]]; then
    echo "❌ No leads found with status '$STATUS_FILTER'"
    echo "   Available statuses: New, Enriching, Ready, Contacted, Replied, Meeting, Closed, Bounce"
    exit 1
fi

# Create CSV file
CSV_FILE="/tmp/instantly_leads_$(date +%Y%m%d_%H%M%S).csv"

# Instantly CSV Format:
# email,first_name,last_name,company,title,phone,website,custom_1,custom_2,...

echo "email,first_name,last_name,company,title,linkedin_url,apollo_id,lead_status,icp_segment" > "$CSV_FILE"

echo "$FILTERED_LEADS" | while read -r lead; do
    EMAIL=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Email").value // empty')
    FIRST_NAME=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="First Name").value // empty')
    LAST_NAME=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Last Name").value // empty')
    COMPANY=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Company").value // empty')
    TITLE=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Title").value // empty')
    LINKEDIN=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="LinkedIn URL").value // empty')
    APOLLO_ID=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Apollo ID").value // empty')
    ICP=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="ICP Segment").value // empty')
    
    # Only export if email exists
    if [[ -n "$EMAIL" && "$EMAIL" != "null" && "$EMAIL" != "empty" ]]; then
        # Escape commas in fields
        COMPANY_ESC=$(echo "$COMPANY" | sed 's/,/ /g')
        TITLE_ESC=$(echo "$TITLE" | sed 's/,/ /g')
        
        echo "${EMAIL},${FIRST_NAME},${LAST_NAME},${COMPANY_ESC},${TITLE_ESC},${LINKEDIN},${APOLLO_ID},${STATUS_FILTER},${ICP}" >> "$CSV_FILE"
    fi
done

# Count exported lines (minus header)
EXPORTED_COUNT=$(($(wc -l < "$CSV_FILE") - 1))

echo "✅ Export complete!"
echo "   File: $CSV_FILE"
echo "   Leads exported: $EXPORTED_COUNT"
echo ""
echo "📋 Next steps:"
echo "1. Open Instantly.ai"
echo "2. Go to Campaigns → Import Leads"
echo "3. Upload: $CSV_FILE"
echo "4. Map fields:"
echo "   - email → Email"
echo "   - first_name → First Name"
echo "   - last_name → Last Name"
echo "   - company → Company"
echo "   - title → Title"
echo "   - linkedin_url → Custom Field"
echo ""
echo "5. Create/Select Campaign"
echo "6. Launch! 🚀"
echo ""

# Show preview
echo "📊 Preview (first 5 leads):"
echo "---"
head -6 "$CSV_FILE"
echo "---"
