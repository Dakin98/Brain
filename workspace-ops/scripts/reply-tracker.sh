#!/bin/bash
# Reply Tracker - Daily reply monitoring and action items
# Usage: ./reply-tracker.sh [add|list|stats]

set -e

CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
HOT_LEADS_ID="901521519130"

if [[ -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: CLICKUP_API_TOKEN not set"
    exit 1
fi

COMMAND="${1:-list}"

case "$COMMAND" in
    "list"|"")
        echo ""
        echo "🔥 TODAY'S REPLIES - Action Required"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        
        # Get all hot leads with New Reply status
        LEADS=$(curl -s "https://api.clickup.com/api/v2/list/${HOT_LEADS_ID}/task" \
            -H "Authorization: ${CLICKUP_KEY}")
        
        NEW_REPLIES=$(echo "$LEADS" | jq -c '[.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "New Reply")]')
        COUNT=$(echo "$NEW_REPLIES" | jq -r 'length')
        
        if [[ "$COUNT" -eq 0 ]]; then
            echo "  ✅ No new replies requiring action"
            echo ""
            echo "  Last checked: $(date '+%H:%M')"
        else
            echo "  Found $COUNT new reply(ies):"
            echo ""
            
            echo "$NEW_REPLIES" | jq -c '.[]' | while read -r lead; do
                TASK_ID=$(echo "$lead" | jq -r '.id')
                NAME=$(echo "$lead" | jq -r '.name')
                COMPANY=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Company").value // "N/A"')
                EMAIL=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Email").value // "N/A"')
                TYPE=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Reply Type").value // "Unknown"')
                PRIORITY=$(echo "$lead" | jq -r '.custom_fields[] | select(.name=="Priority").value // "Warm"')
                
                # Emoji based on type
                case "$TYPE" in
                    "Interested") EMOJI="🔥" ;;
                    "Question") EMOJI="❓" ;;
                    "Referral") EMOJI="🔗" ;;
                    *) EMOJI="💬" ;;
                esac
                
                echo "  $EMOJI $NAME ($COMPANY)"
                echo "     Email: $EMAIL"
                echo "     Type: $TYPE | Priority: $PRIORITY"
                echo "     Link: https://app.clickup.com/t/${TASK_ID}"
                echo ""
            done
            
            echo "  ─────────────────────────────────────────────────────────"
            echo "  Quick Actions:"
            echo "  • Open ClickUp to respond"
            echo "  • Update status after responding"
            echo "  • Book meetings directly in task"
        fi
        echo ""
        ;;
        
    "stats")
        echo ""
        echo "📊 REPLY STATISTICS"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        
        LEADS=$(curl -s "https://api.clickup.com/api/v2/list/${HOT_LEADS_ID}/task" \
            -H "Authorization: ${CLICKUP_KEY}")
        
        # By Type
        echo "By Reply Type:"
        echo "$LEADS" | jq -r '.tasks | group_by(.custom_fields[] | select(.name=="Reply Type").value) | map({type: .[0].custom_fields[] | select(.name=="Reply Type").value, count: length}) | .[] | "  • \(.type): \(.count)"' 2>/dev/null
        
        echo ""
        echo "By Status:"
        echo "$LEADS" | jq -r '.tasks | group_by(.custom_fields[] | select(.name=="Lead Status").value) | map({status: .[0].custom_fields[] | select(.name=="Lead Status").value, count: length}) | .[] | "  • \(.status): \(.count)"' 2>/dev/null
        
        echo ""
        echo "By Priority:"
        echo "$LEADS" | jq -r '.tasks | group_by(.custom_fields[] | select(.name=="Priority").value) | map({priority: .[0].custom_fields[] | select(.name=="Priority").value, count: length}) | .[] | "  • \(.priority): \(.count)"' 2>/dev/null
        
        echo ""
        ;;
        
    "add")
        echo ""
        echo "➕ ADD NEW REPLY TO TRACKING"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        echo "Use this when you get a reply in Instantly:"
        echo ""
        echo "Manual entry in ClickUp:"
        echo "1. Go to: 🔥 Hot Leads"
        echo "2. Click: + Add Task"
        echo "3. Name: 🔥 [Lead Name] - [Company]"
        echo "4. Fill Custom Fields:"
        echo "   • Lead Name, Email, Company"
        echo "   • Reply Type: Interested/Question/Referral"
        echo "   • Lead Status: New Reply"
        echo "   • Priority: Hot/Warm/Cold"
        echo "   • Notes: [Paste reply text]"
        echo ""
        echo "Or use ClickUp Form (if set up)"
        echo ""
        ;;
        
    *)
        echo "Usage: $0 [list|stats|add]"
        echo ""
        echo "Commands:"
        echo "  list  - Show today's replies needing action (default)"
        echo "  stats - Show reply statistics"
        echo "  add   - Instructions for adding new reply"
        ;;
esac
