#!/bin/bash
# clickup-migrate-remaining.sh - Langsame Migration der restlichen Kunden
# Mit Pausen zwischen jedem Kunden

API_TOKEN=$(cat ~/.config/clickup/api_token 2>/dev/null)
SPACE_ID="90040311585"

echo "🐢 Langsame Migration der restlichen Kunden"
echo "==========================================="
echo ""
echo "⏱️  10 Sekunden Pause zwischen jedem Kunden"
echo ""

CLIENTS=(
    "901505420422:Green Cola Germany"
    "901506413852:schnelleinfachgesund"
    "901506671971:Ferro Berlin"
    "901517266555:RAZECO"
)

for client_info in "${CLIENTS[@]}"; do
    IFS=':' read -r OLD_LIST_ID CLIENT_NAME <<< "$client_info"
    
    echo "=========================================="
    echo "📂 Starte: $CLIENT_NAME"
    echo "=========================================="
    echo ""
    
    # 1. Prüfe Tasks
    echo "📋 Prüfe Tasks..."
    TASKS=$(curl -s "https://api.clickup.com/api/v2/list/$OLD_LIST_ID/task" \
        -H "Authorization: $API_TOKEN" | jq -r '.tasks | length')
    echo "   Gefunden: $TASKS Tasks"
    echo ""
    
    # 2. Erstelle neuen Folder
    echo "📁 Erstelle Folder '$CLIENT_NAME (Folder)'..."
    NEW_FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/space/$SPACE_ID/folder" \
        -H "Authorization: $API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"$CLIENT_NAME (Folder)\",\"override_statuses\":true}")
    
    if echo "$NEW_FOLDER" | jq -e '.id' > /dev/null 2>&1; then
        FOLDER_ID=$(echo "$NEW_FOLDER" | jq -r '.id')
        echo "   ✅ Folder: $FOLDER_ID"
    else
        echo "   ❌ Fehler: $(echo "$NEW_FOLDER" | jq -r '.err // .error // "Unknown"')"
        echo "   ⏭️  Überspringe diesen Kunden..."
        sleep 5
        continue
    fi
    echo ""
    
    # 3. Migriere Tasks falls vorhanden
    if [ "$TASKS" -gt 0 ]; then
        echo "📦 Migriere $TASKS Tasks..."
        
        OLD_TASKS_LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$FOLDER_ID/list" \
            -H "Authorization: $API_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"name":"Bestehende Tasks","content":"Gemigrierte Tasks"}')
        
        if echo "$OLD_TASKS_LIST" | jq -e '.id' > /dev/null 2>&1; then
            NEW_LIST_ID=$(echo "$OLD_TASKS_LIST" | jq -r '.id')
            
            # Verschiebe Tasks
            curl -s "https://api.clickup.com/api/v2/list/$OLD_LIST_ID/task" \
                -H "Authorization: $API_TOKEN" | jq -r '.tasks[].id' 2>/dev/null | while read task_id; do
                
                curl -s -X PUT "https://api.clickup.com/api/v2/task/$task_id" \
                    -H "Authorization: $API_TOKEN" \
                    -H "Content-Type: application/json" \
                    -d "{\"list_id\":\"$NEW_LIST_ID\"}" > /dev/null
                
                sleep 1
            done
            echo "   ✅ Tasks migriert"
        fi
        echo ""
    fi
    
    # 4. Erstelle 3 Creative Testing Listen
    echo "📝 Erstelle Listen..."
    for list_name in "Creative Pipeline" "Creative Archive" "Creative Ideas"; do
        echo "   📝 $list_name..."
        LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$FOLDER_ID/list" \
            -H "Authorization: $API_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{\"name\":\"$list_name\",\"content\":\"$CLIENT_NAME - $list_name\"}")
        
        if echo "$LIST" | jq -e '.id' > /dev/null 2>&1; then
            echo "      ✅"
        else
            echo "      ⚠️  $(echo "$LIST" | jq -r '.err // "Existiert"')"
        fi
        sleep 2
    done
    echo ""
    
    # 5. Archiviere alte Liste
    echo "🗑️  Archiviere alte Liste..."
    curl -s -X PUT "https://api.clickup.com/api/v2/list/$OLD_LIST_ID" \
        -H "Authorization: $API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"archived":true}' > /dev/null
    echo "   ✅ Archiviert"
    echo ""
    
    echo "✅ $CLIENT_NAME fertig!"
    echo ""
    
    # Pause vor nächstem Kunden
    if [ "$client_info" != "${CLIENTS[-1]}" ]; then
        echo "⏳ Pause: 10 Sekunden..."
        sleep 10
        echo ""
    fi
done

echo "==========================================="
echo "✅ ALLE KUNDEN FERTIG!"
echo "==========================================="
