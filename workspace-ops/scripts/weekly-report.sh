#!/bin/bash
# Weekly Outbound Report - Comprehensive weekly performance
# Usage: ./weekly-report.sh
# Cron: 0 9 * * 1 (Monday 9am)

set -e

CLICKUP_KEY="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
CAMPAIGN_ID="901521519128"
HOT_LEADS_ID="901521519130"

if [[ -z "$CLICKUP_KEY" ]]; then
    echo "❌ Error: CLICKUP_API_TOKEN not set"
    exit 1
fi

WEEK=$(date +%V)
YEAR=$(date +%Y)
REPORT_FILE="/tmp/outbound_weekly_${YEAR}_W${WEEK}.md"

echo "Generating Weekly Report..."

# ============================================================
# HEADER
# ============================================================
cat > "$REPORT_FILE" << EOF
# 📊 Weekly Outbound Report - KW ${WEEK} (${YEAR})

**Period:** $(date -v-7d +%d.%m) - $(date +%d.%m.%Y)  
**Generated:** $(date '+%d.%m.%Y %H:%M')

---

## 🎯 EXECUTIVE SUMMARY

EOF

# ============================================================
# CAMPAIGN PERFORMANCE
# ============================================================
CAMPAIGNS=$(curl -s "https://api.clickup.com/api/v2/list/${CAMPAIGN_ID}/task" \
    -H "Authorization: ${CLICKUP_KEY}")

cat >> "$REPORT_FILE" << EOF
## 📈 Campaign Performance

| Campaign | Status | Leads | Sent | Replies | Rate % | Meetings |
|----------|--------|-------|------|---------|--------|----------|
EOF

TOTAL_SENT=0
TOTAL_REPLIES=0
TOTAL_MEETINGS=0

echo "$CAMPAIGNS" | jq -c '.tasks[]' | while read -r campaign; do
    NAME=$(echo "$campaign" | jq -r '.name' | cut -c1-20)
    STATUS=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Campaign Status").value // "Draft"')
    LEADS=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Total Leads").value // 0')
    SENT=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Sent Count").value // 0')
    REPLIES=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Replies").value // 0')
    RATE=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Reply Rate %").value // 0')
    MEETINGS=$(echo "$campaign" | jq -r '.custom_fields[] | select(.name=="Meetings").value // 0')
    
    # Emoji for status
    case "$STATUS" in
        "Active") STATUS_EMOJI="🟢" ;;
        "Paused") STATUS_EMOJI="⏸️" ;;
        "Completed") STATUS_EMOJI="✅" ;;
        *) STATUS_EMOJI="⚪" ;;
    esac
    
    echo "| $NAME | $STATUS_EMOJI $STATUS | $LEADS | $SENT | $REPLIES | ${RATE}% | $MEETINGS |" >> "$REPORT_FILE"
done

# Totals
TOTAL_SENT=$(echo "$CAMPAIGNS" | jq -r '[.tasks[].custom_fields[] | select(.name=="Sent Count").value // 0] | add')
TOTAL_REPLIES=$(echo "$CAMPAIGNS" | jq -r '[.tasks[].custom_fields[] | select(.name=="Replies").value // 0] | add')
TOTAL_MEETINGS=$(echo "$CAMPAIGNS" | jq -r '[.tasks[].custom_fields[] | select(.name=="Meetings").value // 0] | add')

if [[ "$TOTAL_SENT" -gt 0 ]]; then
    AVG_RATE=$(echo "scale=1; ($TOTAL_REPLIES / $TOTAL_SENT) * 100" | bc)
else
    AVG_RATE=0
fi

cat >> "$REPORT_FILE" << EOF
| **TOTAL** | | | **$TOTAL_SENT** | **$TOTAL_REPLIES** | **${AVG_RATE}%** | **$TOTAL_MEETINGS** |

**Key Metrics:**
- **Total Emails Sent:** $TOTAL_SENT
- **Total Replies:** $TOTAL_REPLIES
- **Average Reply Rate:** ${AVG_RATE}%
- **Meetings Booked:** $TOTAL_MEETINGS

---

## 🔥 Hot Leads Pipeline

EOF

# ============================================================
# HOT LEADS ANALYSIS
# ============================================================
HOT_LEADS=$(curl -s "https://api.clickup.com/api/v2/list/${HOT_LEADS_ID}/task" \
    -H "Authorization: ${CLICKUP_KEY}")

TOTAL_HOT=$(echo "$HOT_LEADS" | jq -r '.tasks | length')

cat >> "$REPORT_FILE" << EOF
**Total Hot Leads:** $TOTAL_HOT

### By Status

EOF

echo "$HOT_LEADS" | jq -r '.tasks | group_by(.custom_fields[]? | select(.name=="Lead Status").value) | map({status: .[0].custom_fields[] | select(.name=="Lead Status").value, count: length}) | sort_by(.count) | reverse | .[] | "- **\(.status):** \(.count)"' >> "$REPORT_FILE" 2>/dev/null

cat >> "$REPORT_FILE" << EOF

### By Reply Type

EOF

echo "$HOT_LEADS" | jq -r '.tasks | group_by(.custom_fields[]? | select(.name=="Reply Type").value) | map({type: .[0].custom_fields[] | select(.name=="Reply Type").value, count: length}) | sort_by(.count) | reverse | .[] | "- **\(.type):** \(.count)"' >> "$REPORT_FILE" 2>/dev/null

# High Value Leads
MEETING_VALUE=$(echo "$HOT_LEADS" | jq -r '[.tasks[] | select(.custom_fields[]?.name? == "Lead Status" and .custom_fields[]?.value? == "Meeting Booked") | .custom_fields[] | select(.name=="Est. Deal Value").value // 0] | add')

cat >> "$REPORT_FILE" << EOF

**Estimated Pipeline Value:** €$MEETING_VALUE

---

## 💡 Insights & Recommendations

EOF

# ============================================================
# RECOMMENDATIONS
# ============================================================

# Check reply rate
if [[ $(echo "$AVG_RATE < 3" | bc) -eq 1 ]]; then
    echo "⚠️ **Low Reply Rate Alert:** Your average reply rate is ${AVG_RATE}%, which is below the 3% benchmark." >> "$REPORT_FILE"
    echo "   - *Recommendation:* Test new subject lines with more curiosity/personalization" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Check meetings
if [[ "$TOTAL_MEETINGS" -eq 0 && "$TOTAL_REPLIES" -gt 10 ]]; then
    echo "🤔 **Conversion Gap:** You have $TOTAL_REPLIES replies but 0 meetings booked." >> "$REPORT_FILE"
    echo "   - *Recommendation:* Strengthen your CTA and make it easier to book a call" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Check active campaigns
ACTIVE_COUNT=$(echo "$CAMPAIGNS" | jq -r '[.tasks[] | select(.custom_fields[]?.name? == "Campaign Status" and .custom_fields[]?.value? == "Active")] | length')
if [[ "$ACTIVE_COUNT" -eq 0 ]]; then
    echo "🚀 **No Active Campaigns:** You currently have no active outreach campaigns." >> "$REPORT_FILE"
    echo "   - *Recommendation:* Launch a new campaign this week" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Success message
if [[ $(echo "$AVG_RATE >= 5" | bc) -eq 1 ]]; then
    echo "✅ **Great Performance:** Your reply rate of ${AVG_RATE}% is above average!" >> "$REPORT_FILE"
    echo "   - *Recommendation:* Scale this campaign and document what's working" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF
---

## ✅ Action Items for Next Week

- [ ] Review low-performing campaigns
- [ ] Follow up on "New Reply" leads
- [ ] Book meetings with interested prospects
- [ ] Prepare new lead list for next campaign
- [ ] Optimize email sequences based on data

---

*Report generated automatically by Outbound Engine*
EOF

echo ""
echo "✅ Weekly Report Generated!"
echo "   File: $REPORT_FILE"
echo ""
echo "Report Preview:"
echo "═══════════════════════════════════════════════════════════════"
head -50 "$REPORT_FILE"
echo "..."
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "To view full report: cat $REPORT_FILE"
