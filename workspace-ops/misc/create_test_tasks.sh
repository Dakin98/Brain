#!/bin/bash

LIST_ID="901521395731"
TOKEN="pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
KUNDE="🧪 TEST Automation Kunde"

# Tasks definieren
TASKS=(
  "🚀 Kickoff Call:0"
  "🔍 Tracking Audit:1"
  "📊 Account Analysis:2"
  "💡 Creative Briefing:3"
  "🎬 Creative Produktion:5"
  "👁️ Kunden Review:8"
  "🚀 Campaign Launch:10"
  "📈 Performance Check Tag 3:13"
  "🏆 Performance Check Tag 7:17"
)

# Aktuelles Datum
NOW=$(date +%s)

echo "📝 Erstelle 9 Tasks für $KUNDE..."
echo ""

for TASK in "${TASKS[@]}"; do
  NAME=$(echo $TASK | cut -d':' -f1)
  OFFSET=$(echo $TASK | cut -d':' -f2)
  
  # Due Date berechnen
  DUE=$((NOW + OFFSET * 86400 * 1000))
  
  echo "📋 $NAME (Tag +$OFFSET)..."
  
  curl -s -X POST "https://api.clickup.com/api/v2/list/$LIST_ID/task" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"$NAME — $KUNDE\",
      \"description\": \"Automatisch erstellt für $KUNDE\",
      \"due_date\": $DUE,
      \"assignees\": [63066979]
    }" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'   ✅ {d.get(\"name\",\"ERROR\")}')"
  
  sleep 0.5
done

echo ""
echo "🎉 Alle 9 Tasks erstellt!"
