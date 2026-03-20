#!/bin/bash
# Outbound Dashboard - Real-time Campaign Performance
# Usage: ./outbound-dashboard.sh

set -e

CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
CAMPAIGN_LIST_ID="901521519128"
HOT_LEADS_LIST_ID="901521519130"

if [[ -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: CLICKUP_API_TOKEN not set"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║           📊 OUTBOUND DASHBOARD - $(date '+%d.%m.%Y %H:%M')          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# CAMPAIGN PERFORMANCE
# ============================================================
echo "📈 ACTIVE CAMPAIGNS"
echo "═══════════════════════════════════════════════════════════"
echo ""

CAMPAIGNS=$(curl -s "https://api.clickup.com/api/v2/list/${CAMPAIGN_LIST_ID}/task" \
    -H "Authorization: ${CLICKUP_KEY}")

# Count campaigns
TOTAL_CAMPAIGNS=$(echo "$CAMPAIGNS" | jq -r '.tasks | length')
ACTIVE_CAMPAIGNS=$(echo "$CAMPAIGNS" | jq -r '[.tasks[] | select(.custom_fields[]?.name? == "Campaign Status" and .custom_fields[]?.value? == "Active")] | length')

echo "Total Campaigns: $TOTAL_CAMPAIGNS | Active: $ACTIVE_CAMPAIGNS"
echo ""

# Table Header
printf "%-25s %8s %8s %8s %8s %10s\n" "Campaign" "Leads" "Sent" "Replies" "Rate%" "Meetings"
echo "───────────────────────────────────────────────────────────────────────"

# Active campaigns details
echo "$CAMPAIGNS" | jq -c '.tasks[]' | while read -r campaign; do
    STATUS=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Campaign Status").value // "Draft"')
    
    if [[ "$STATUS" == "Active" ]]; then
        NAME=$(echo "$campaign" | jq -r '.name' | cut -c1-25)
        LEADS=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Total Leads").value // 0')
        SENT=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Sent Count").value // 0')
        REPLIES=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Replies").value // 0')
        RATE=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Reply Rate %").value // 0')
        MEETINGS=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Meetings").value // 0')
        
        printf "%-25s %8s %8s %8s %8s %10s\n" "$NAME" "$LEADS" "$SENT" "$REPLIES" "${RATE}%" "$MEETINGS"
    fi
done

echo ""

# ============================================================
# HOT LEADS PIPELINE
# ============================================================
echo "🔥 HOT LEADS PIPELINE"
echo "═══════════════════════════════════════════════════════════"
echo ""

HOT_LEADS=$(curl -s "https://api.clickup.com/api/v2/list/${HOT_LEADS_LIST_ID}/task" \
    -H "Authorization: ${CLICKUP_KEY}")

# Count by status
echo "$HOT_LEADS" | jq -r '.tasks | group_by(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value?) | map({status: .[0].custom_fields[] | select(.name=="Lead Status").value, count: length}) | .[] | "\(.status): \(.count)"' 2>/dev/null | sort | uniq -c | awk '{print $2, $1}' | while read -r line; do
    echo "  • $line"
done

TOTAL_HOT=$(echo "$HOT_LEADS" | jq -r '.tasks | length')
NEW_REPLIES=$(echo "$HOT_LEADS" | jq -r '[.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "New Reply")] | length')
MEETING_BOOKED=$(echo "$HOT_LEADS" | jq -r '[.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "Meeting Booked")] | length')

echo ""
echo "  Total Hot Leads: $TOTAL_HOT"
echo "  New Replies (Action needed): $NEW_REPLIES"
echo "  Meetings Booked: $MEETING_BOOKED"
echo ""

# ============================================================
# PRIORITY LEADS
# ============================================================
echo "🚨 PRIORITY ACTION ITEMS"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [[ "$NEW_REPLIES" -gt 0 ]]; then
    echo "New Replies requiring action:"
    echo "$HOT_LEADS" | jq -c '.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "New Reply")' | while read -r lead; do
        NAME=$(echo "$lead" | jq -r '.name')
        COMPANY=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Company").value // "N/A"')
        TYPE=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Reply Type").value // "Unknown"')
        echo "  🔥 $NAME ($COMPANY) - $TYPE"
    done
else
    echo "  ✅ No new replies requiring action"
fi

echo ""

# ============================================================
# THIS WEEK'S PERFORMANCE
# ============================================================
echo "📅 THIS WEEK'S SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Calculate totals
TOTAL_SENT=$(echo "$CAMPAIGNS" | jq -r '[.tasks[].custom_fields[] | select(.name=="Sent Count").value // 0] | add')
TOTAL_REPLIES=$(echo "$CAMPAIGNS" | jq -r '[.tasks[].custom_fields[] | select(.name=="Replies").value // 0] | add')
TOTAL_MEETINGS=$(echo "$CAMPAIGNS" | jq -r '[.tasks[].custom_fields[] | select(.name=="Meetings").value // 0] | add')

if [[ "$TOTAL_SENT" -gt 0 ]]; then
    OVERALL_RATE=$(echo "scale=1; ($TOTAL_REPLIES / $TOTAL_SENT) * 100" | bc)
else
    OVERALL_RATE=0
fi

echo "  Emails Sent: $TOTAL_SENT"
echo "  Replies Received: $TOTAL_REPLIES"
echo "  Overall Reply Rate: ${OVERALL_RATE}%"
echo "  Meetings Booked: $TOTAL_MEETINGS"
echo ""

# ============================================================
# RECOMMENDATIONS
# ============================================================
echo "💡 RECOMMENDATIONS"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [[ "$NEW_REPLIES" -gt 5 ]]; then
    echo "  ⚠️  You have $NEW_REPLIES new replies - time to respond!"
fi

if [[ $(echo "$OVERALL_RATE < 3" | bc) -eq 1 ]]; then
    echo "  📉 Reply rate below 3% - consider optimizing subject lines"
fi

if [[ "$MEETING_BOOKED" -eq 0 && "$TOTAL_REPLIES" -gt 10 ]]; then
    echo "  🤔 Many replies but no meetings - strengthen your CTA"
fi

if [[ "$ACTIVE_CAMPAIGNS" -eq 0 ]]; then
    echo "  🚀 No active campaigns - time to launch a new one!"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Dashboard updated: $(date '+%H:%M')                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
