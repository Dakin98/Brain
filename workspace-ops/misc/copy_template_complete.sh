#!/bin/bash
# TEMPLATE KOPIERER - Kopiert ein Template vollständig in einen Kunden-Ordner

TOKEN="pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"

# Parameter:
# $1 = Source Task ID (aus Process Hub)
# $2 = Target List ID (Project Management des Kunden)
# $3 = Kundenname

SOURCE_TASK_ID="$1"
TARGET_LIST_ID="$2"
KUNDE="$3"

echo "🔄 Kopiere Template: $SOURCE_TASK_ID → $TARGET_LIST_ID"
echo "   Kunde: $KUNDE"
echo ""

# 1. SOURCE TASK DETAILS HOLEN
echo "📋 1. Lese Template-Details..."
TASK_DATA=$(curl -s "https://api.clickup.com/api/v2/task/$SOURCE_TASK_ID" \
  -H "Authorization: $TOKEN")

NAME=$(echo "$TASK_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin).get('name','').replace('[TEMPLATE] ','').replace(' — [Kunde]', ''))")
DESC=$(echo "$TASK_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin).get('description',''))")

echo "   Name: $NAME"
echo ""

# 2. NEUEN TASK ERSTELLEN
echo "🏗️  2. Erstelle neuen Task..."
NEW_TASK=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$TARGET_LIST_ID/task" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$NAME — $KUNDE\",
    \"description\": \"$DESC\",
    \"assignees\": [63066979]
  }")

NEW_TASK_ID=$(echo "$NEW_TASK" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))")
echo "   Neue Task ID: $NEW_TASK_ID"
echo ""

# 3. CHECKLISTEN KOPIEREN
echo "📋 3. Kopiere Checklisten..."

# Anzahl der Checklisten
CHECKLIST_COUNT=$(echo "$TASK_DATA" | python3 -c "import json,sys; print(len(json.load(sys.stdin).get('checklists',[])))")
echo "   Gefunden: $CHECKLIST_COUNT Checkliste(n)"

# Für jede Checkliste
for ((i=0; i<CHECKLIST_COUNT; i++)); do
  CL_NAME=$(echo "$TASK_DATA" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('checklists',[][$i].get('name','Checkliste'))")
  
  # Checkliste erstellen
  NEW_CL=$(curl -s -X POST "https://api.clickup.com/api/v2/task/$NEW_TASK_ID/checklist" \
    -H "Authorization: $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"$CL_NAME\"}")
  
  NEW_CL_ID=$(echo "$NEW_CL" | python3 -c "import json,sys; print(json.load(sys.stdin).get('checklist',{}).get('id',''))")
  
  # Items auslesen und kopieren
  ITEMS=$(echo "$TASK_DATA" | python3 -c "import json,sys; d=json.load(sys.stdin); cl=d.get('checklists',[][$i]; print('|'.join([item.get('name','') for item in cl.get('items',[])]))")
  
  echo "   Checkliste '$CL_NAME': ${#ITEMS[@]} Items"
  
  # Jedes Item hinzufügen
  echo "$ITEMS" | tr '|' '\n' | while read ITEM_NAME; do
    if [ -n "$ITEM_NAME" ]; then
      curl -s -X POST "https://api.clickup.com/api/v2/checklist/$NEW_CL_ID/checklist_item" \
        -H "Authorization: $TOKEN" \
        -d "{\"name\": \"$ITEM_NAME\"}" > /dev/null
    fi
  done
done

echo ""
echo "✅ Template vollständig kopiert!"
echo ""
echo "Neuer Task: $NEW_TASK_ID"
