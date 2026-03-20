#!/bin/bash
# Create Dummy Data for ClickUp Outbound Demo

TOKEN="pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
FOLDER_ID="901514663975"

echo "🎨 Creating Dummy Data..."

# Get List IDs
LISTS=$(curl -s "https://api.clickup.com/api/v2/folder/${FOLDER_ID}/list" \
  -H "Authorization: ${TOKEN}")

CAMPAIGN_ID=$(echo "$LISTS" | jq -r '.lists[] | select(.name | contains("Campaign")) | .id')
HOT_LEADS_ID=$(echo "$LISTS" | jq -r '.lists[] | select(.name | contains("Hot")) | .id')

echo "Found Lists:"
echo "  Campaign: $CAMPAIGN_ID"
echo "  Hot Leads: $HOT_LEADS_ID"

# Campaign 1
echo "Creating Campaign 1..."
curl -s -X POST "https://api.clickup.com/api/v2/list/${CAMPAIGN_ID}/task" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "name": "📊 Fashion DACH - März 2024",
  "custom_fields": [
    {"name": "Campaign Name", "value": "Fashion DACH - März 2024"},
    {"name": "ICP Segment", "value": "Fashion DACH"},
    {"name": "Campaign Status", "value": "Active"},
    {"name": "Total Leads", "value": 350},
    {"name": "Sent Count", "value": 280},
    {"name": "Replies", "value": 18},
    {"name": "Interested", "value": 12},
    {"name": "Meetings", "value": 3},
    {"name": "Reply Rate %", "value": 6.4}
  ]
}
EOF

# Campaign 2
echo "Creating Campaign 2..."
curl -s -X POST "https://api.clickup.com/api/v2/list/${CAMPAIGN_ID}/task" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "name": "📊 Beauty DACH - Q1 Test",
  "custom_fields": [
    {"name": "Campaign Name", "value": "Beauty DACH - Q1 Test"},
    {"name": "ICP Segment", "value": "Beauty DACH"},
    {"name": "Campaign Status", "value": "Active"},
    {"name": "Total Leads", "value": 200},
    {"name": "Sent Count", "value": 120},
    {"name": "Replies", "value": 4},
    {"name": "Interested", "value": 2},
    {"name": "Meetings", "value": 0},
    {"name": "Reply Rate %", "value": 3.3}
  ]
}
EOF

# Hot Lead 1
echo "Creating Hot Lead 1..."
curl -s -X POST "https://api.clickup.com/api/v2/list/${HOT_LEADS_ID}/task" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "name": "🔥 Max Mustermann - Fashion Brand GmbH",
  "description": "Reply: Hi Deniz, thanks for reaching out! This sounds very interesting. We are actually looking to scale our Meta Ads in Q2. Can we schedule a call next week? Best, Max",
  "priority": 2,
  "custom_fields": [
    {"name": "Lead Name", "value": "Max Mustermann"},
    {"name": "First Name", "value": "Max"},
    {"name": "Email", "value": "max@fashionbrand.de"},
    {"name": "Title", "value": "CEO"},
    {"name": "Company", "value": "Fashion Brand GmbH"},
    {"name": "Reply Type", "value": "Interested"},
    {"name": "Lead Status", "value": "New Reply"},
    {"name": "Priority", "value": "🔥 Hot"},
    {"name": "Est. Deal Value", "value": 15000},
    {"name": "Next Action", "value": "Send calendar link"}
  ]
}
EOF

# Hot Lead 2
echo "Creating Hot Lead 2..."
curl -s -X POST "https://api.clickup.com/api/v2/list/${HOT_LEADS_ID}/task" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "name": "❓ Laura Schmidt - Beauty Co",
  "description": "Reply: Hi Deniz, what exactly do you mean by creative testing? Is this something we can do in-house or do we need external support? Laura",
  "priority": 3,
  "custom_fields": [
    {"name": "Lead Name", "value": "Laura Schmidt"},
    {"name": "First Name", "value": "Laura"},
    {"name": "Email", "value": "laura@beautyco.de"},
    {"name": "Title", "value": "Marketing Manager"},
    {"name": "Company", "value": "Beauty Co"},
    {"name": "Reply Type", "value": "Question"},
    {"name": "Lead Status", "value": "New Reply"},
    {"name": "Priority", "value": "🌡️ Warm"},
    {"name": "Est. Deal Value", "value": 8000},
    {"name": "Next Action", "value": "Answer question + CTA"}
  ]
}
EOF

# Hot Lead 3
echo "Creating Hot Lead 3..."
curl -s -X POST "https://api.clickup.com/api/v2/list/${HOT_LEADS_ID}/task" \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "name": "🔥 Jannis Weber - Home Living AG",
  "description": "Reply: Hi Deniz, yes lets talk! Tuesday 2pm works for me. Looking forward to it. Jannis",
  "priority": 2,
  "custom_fields": [
    {"name": "Lead Name", "value": "Jannis Weber"},
    {"name": "First Name", "value": "Jannis"},
    {"name": "Email", "value": "jannis@homeliving.de"},
    {"name": "Title", "value": "Founder"},
    {"name": "Company", "value": "Home Living AG"},
    {"name": "Reply Type", "value": "Interested"},
    {"name": "Lead Status", "value": "Meeting Booked"},
    {"name": "Priority", "value": "🔥 Hot"},
    {"name": "Est. Deal Value", "value": 25000},
    {"name": "Next Action", "value": "Prepare for call"}
  ]
}
EOF

echo ""
echo "✅ Dummy data created!"
