#!/bin/bash

TOKEN="pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
LIST_ID="901507242261"

echo "🏗️  Erstelle Paid Ads Onboarding Template (9 Tasks)..."
echo ""

# Task 1: Kickoff Call
echo "📋 Task 1: 🚀 Kickoff Call..."
TASK1=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$LIST_ID/task" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[TEMPLATE] 🚀 Kickoff Call",
    "description": "Erstgespräch mit dem Kunden. Ziele definieren, Erwartungen abstimmen, Briefing sammeln.\\n\\n⏱️ Dauer: 60-90 Min\\n👤 Assignee: Deniz",
    "tags": ["template", "onboarding", "project-management"]
  }')
TASK1_ID=$(echo $TASK1 | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))")

# Checkliste für Task 1
curl -s -X POST "https://api.clickup.com/api/v2/task/$TASK1_ID/checklist" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Kickoff Checkliste"}' > /dev/null

CHECKLIST1=$(curl -s "https://api.clickup.com/api/v2/task/$TASK1_ID" \
  -H "Authorization: $TOKEN" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('checklists',[{}])[0].get('id',''))")

for ITEM in "Zugänge erhalten (Meta BM, Google Ads)" "Ziele & KPIs besprochen" "Budget & Laufzeit geklärt" "Briefing-Fragen beantwortet" "Nächste Schritte definiert"; do
  curl -s -X POST "https://api.clickup.com/api/v2/checklist/$CHECKLIST1/checklist_item" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$ITEM\"}" > /dev/null
done
echo "   ✅ Mit Checkliste"

# Task 2: Tracking Audit
echo "📋 Task 2: 🔍 Tracking Audit & Setup..."
TASK2=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$LIST_ID/task" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[TEMPLATE] 🔍 Tracking Audit & Setup",
    "description": "Alle Tracking-Systeme prüfen und sicherstellen, dass Conversions korrekt erfasst werden.\\n\\n⏱️ Dauer: 2-3h\\n👤 Assignee: Deniz",
    "tags": ["template", "onboarding", "project-management"]
  }')
TASK2_ID=$(echo $TASK2 | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))")

curl -s -X POST "https://api.clickup.com/api/v2/task/$TASK2_ID/checklist" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Tracking Checkliste"}' > /dev/null
CHECKLIST2=$(curl -s "https://api.clickup.com/api/v2/task/$TASK2_ID" \
  -H "Authorization: $TOKEN" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('checklists',[{}])[0].get('id',''))")

for ITEM in "GTM Container prüfen" "Stape Server-Side Tracking" "Meta Pixel firing" "Meta CAPI aktiv" "GA4 Property verbunden" "E-Commerce Events tracken" "Test-Kauf durchgeführt"; do
  curl -s -X POST "https://api.clickup.com/api/v2/checklist/$CHECKLIST2/checklist_item" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$ITEM\"}" > /dev/null
done
echo "   ✅ Mit Checkliste"

echo ""
echo "... (weitere 7 Tasks folgen)"
echo ""
echo "✅ Template-Grundlage erstellt!"
echo "📍 Ort: Process Hub"
echo "🏷️  Tags: template, onboarding, project-management"
