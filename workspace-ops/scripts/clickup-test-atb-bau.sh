#!/bin/bash
# clickup-test-atb-bau.sh - Proof of Concept für ATB Bau

API_TOKEN=$(cat ~/.config/clickup/api_token 2>/dev/null)
SPACE_ID="90040311585"
ATB_LIST_ID="901517659482"

echo "🧪 Proof of Concept: ATB Bau"
echo "============================"
echo ""

# 1. Hole aktuelle Tasks aus ATB Bau Liste
echo "📋 Step 1: Prüfe bestehende Tasks..."
TASKS=$(curl -s "https://api.clickup.com/api/v2/list/$ATB_LIST_ID/task" \
    -H "Authorization: $API_TOKEN" | jq -r '.tasks | length')

echo "   Gefunden: $TASKS Tasks"
if [ "$TASKS" -gt 0 ]; then
    echo "   ⚠️  Achtung: $TASKS Tasks müssen migriert werden!"
fi
echo ""

# 2. Erstelle neuen Folder "ATB Bau (Folder)"
echo "📁 Step 2: Erstelle neuen Folder..."
NEW_FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/space/$SPACE_ID/folder" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"ATB Bau (Folder)","override_statuses":true}')

if echo "$NEW_FOLDER" | jq -e '.id' > /dev/null 2>&1; then
    NEW_FOLDER_ID=$(echo "$NEW_FOLDER" | jq -r '.id')
    echo "   ✅ Folder erstellt: $NEW_FOLDER_ID"
else
    echo "   ❌ Fehler: $(echo "$NEW_FOLDER" | jq -r '.err // .error // "Unknown"')"
    exit 1
fi
echo ""

# 3. Verschiebe bestehende Tasks (falls vorhanden)
if [ "$TASKS" -gt 0 ]; then
    echo "📦 Step 3: Migriere $TASKS Tasks..."
    
    # Erstelle erst eine Liste im neuen Folder für die alten Tasks
    OLD_TASKS_LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$NEW_FOLDER_ID/list" \
        -H "Authorization: $API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"name":"Bestehende Tasks","content":"Gemigriert aus alter Liste"}')
    
    if echo "$OLD_TASKS_LIST" | jq -e '.id' > /dev/null 2>&1; then
        OLD_LIST_ID=$(echo "$OLD_TASKS_LIST" | jq -r '.id')
        echo "   ✅ Liste für alte Tasks: $OLD_LIST_ID"
        
        # Tasks verschieben
        echo "   🔄 Verschiebe Tasks..."
        curl -s "https://api.clickup.com/api/v2/list/$ATB_LIST_ID/task" \
            -H "Authorization: $API_TOKEN" | jq -r '.tasks[].id' | while read task_id; do
            
            MOVE=$(curl -s -X PUT "https://api.clickup.com/api/v2/task/$task_id" \
                -H "Authorization: $API_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"list_id\":\"$OLD_LIST_ID\"}")
            
            if echo "$MOVE" | jq -e '.id' > /dev/null 2>&1; then
                echo "      ✅ Task $task_id verschoben"
            else
                echo "      ⚠️  Task $task_id: $(echo "$MOVE" | jq -r '.err // "Error"')"
            fi
            sleep 1
        done
    fi
    echo ""
fi

# 4. Erstelle Creative Testing Folder
echo "🎨 Step 4: Erstelle Creative Testing..."
CT_FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$NEW_FOLDER_ID/folder" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"Creative Testing"}')

if echo "$CT_FOLDER" | jq -e '.id' > /dev/null 2>&1; then
    CT_ID=$(echo "$CT_FOLDER" | jq -r '.id')
    echo "   ✅ Creative Testing Folder: $CT_ID"
else
    # Manche ClickUp-Versionen erlauben keine verschachtelten Folders
    echo "   ⚠️  Verschachtelte Folders nicht möglich, erstelle Listen direkt..."
    CT_ID="$NEW_FOLDER_ID"
fi
echo ""

# 5. Erstelle die 3 Listen
echo "📝 Step 5: Erstelle Listen..."
for list_name in "Creative Pipeline" "Creative Archive" "Creative Ideas"; do
    echo "   📝 $list_name..."
    LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$CT_ID/list" \
        -H "Authorization: $API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"$list_name\",\"content\":\"ATB Bau - $list_name\"}")
    
    if echo "$LIST" | jq -e '.id' > /dev/null 2>&1; then
        echo "      ✅ ID: $(echo "$LIST" | jq -r '.id')"
    else
        echo "      ⚠️  $(echo "$LIST" | jq -r '.err // "Existiert oder Fehler"')"
    fi
    sleep 2
done
echo ""

# 6. Alte Liste archivieren
echo "🗑️  Step 6: Archiviere alte Liste..."
ARCHIVE=$(curl -s -X PUT "https://api.clickup.com/api/v2/list/$ATB_LIST_ID" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"archived":true}')

if echo "$ARCHIVE" | jq -e '.archived' > /dev/null 2>&1; then
    echo "   ✅ Alte Liste archiviert"
else
    echo "   ⚠️  Konnte nicht archivieren"
fi
echo ""

echo "============================"
echo "✅ Proof of Concept fertig!"
echo ""
echo "Neue Struktur:"
echo "  ATB Bau (Folder)/"
echo "  ├── Bestehende Tasks (falls vorhanden)"
echo "  ├── Creative Pipeline"
echo "  ├── Creative Archive"
echo "  └── Creative Ideas"
echo ""
echo "IDs:"
echo "  Folder: $NEW_FOLDER_ID"
