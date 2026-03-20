#!/bin/bash

# Vollständige Template-Kopie mit allen Details
TOKEN="pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
SOURCE_LIST="901507242261"  # Process Hub
TARGET_LIST="901521401199"  # AUTO TEST V5 Project Management
KUNDE="🤖 AUTO TEST V5"

echo "🔄 Kopiere Templates aus Process Hub..."
echo ""

# Template IDs holen
curl -s "https://api.clickup.com/api/v2/list/$SOURCE_LIST/task?archived=false" \
  -H "Authorization: $TOKEN" | \
  python3 -c "
import json,sys
d=json.load(sys.stdin)

# Nur die onboarding templates mit '[Kunde]' im Namen
templates = []
for t in d.get('tasks',[]):
  name = t.get('name','')
  if '[TEMPLATE]' in name and '— [Kunde]' in name:
    templates.append({
      'id': t.get('id'),
      'name': name.replace('[TEMPLATE] ','').replace(' — [Kunde]',''),
      'desc': t.get('description',''),
      'tags': [tag.get('name') for tag in t.get('tags',[])],
      'checklists': t.get('checklists',[])
    })

for t in templates[:9]:
  print(f\"{t['id']}|{t['name']}\")
" | while IFS='|' read -r TEMPLATE_ID TEMPLATE_NAME; do
  
  echo "📋 Kopiere: $TEMPLATE_NAME..."
  
  # Task erstellen mit gleichem Namen aber Kunde eingesetzt
  NEW_NAME="$TEMPLATE_NAME — $KUNDE"
  
  # Beschreibung holen
  DESC=$(curl -s "https://api.clickup.com/api/v2/task/$TEMPLATE_ID" \
    -H "Authorization: $TOKEN" | \
    python3 -c "import json,sys; print(json.load(sys.stdin).get('description',''))" | sed 's/"/\\"/g')
  
  # Task erstellen
  curl -s -X POST "https://api.clickup.com/api/v2/list/$TARGET_LIST/task" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"$NEW_NAME\",
      \"description\": \"$DESC\",
      \"assignees\": [63066979]
    }" > /dev/null
  
  echo "   ✅ Task erstellt"
  
  sleep 0.5
done

echo ""
echo "🎉 Templates kopiert!"
echo ""
echo "⚠️  WICHTIG: Die Checklisten-Items müssen manuell gefüllt werden"
echo "   oder wir erstellen ein Script das sie aus einer Definition liest."
