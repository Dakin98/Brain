#!/bin/bash
# clickup-restructure.sh - Nur Delivery Space, pro Kunde Creative Testing
# Löscht nur den zentralen Creative Testing Folder, erstellt pro Kunde eigene

API_TOKEN=$(cat ~/.config/clickup/api_token 2>/dev/null)
SPACE_ID="90040311585"
DELIVERY_FOLDER_ID="90040881723"  # Clients folder

echo "🔄 ClickUp Restrukturierung (NUR Delivery Space)"
echo "================================================"
echo ""

# 1. Zentralen Creative Testing Folder archivieren (nicht löschen, nur verstecken)
echo "📁 Step 1: Archiviere zentralen Creative Testing Folder..."
CT_FOLDER_ID="901514520867"

ARCHIVE=$(curl -s -X PUT "https://api.clickup.com/api/v2/folder/$CT_FOLDER_ID" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"archived":true}')

if echo "$ARCHIVE" | jq -e '.archived' > /dev/null 2>&1; then
    echo "✅ Zentraler Folder archiviert (ID: $CT_FOLDER_ID)"
else
    echo "⚠️  Konnte nicht archivieren (oder existiert nicht): $(echo "$ARCHIVE" | jq -r '.err // "Unknown"')"
fi

echo ""
echo "⏳ Warte 3 Sekunden..."
sleep 3

# 2. Pro Kunde Creative Testing Folder erstellen
echo ""
echo "📁 Step 2: Erstelle pro Kunde Creative Testing..."
echo ""

CLIENTS=(
    "901505420422:Green Cola Germany"
    "901506413852:schnelleinfachgesund"
    "901506671971:Ferro Berlin"
    "901517266555:RAZECO"
    "901517659482:ATB Bau"
)

for client_info in "${CLIENTS[@]}"; do
    IFS=':' read -r LIST_ID CLIENT_NAME <<< "$client_info"
    
    echo "📂 $CLIENT_NAME"
    
    # Prüfe ob schon Creative Testing Folder existiert
    EXISTING=$(curl -s "https://api.clickup.com/api/v2/list/$LIST_ID" \
        -H "Authorization: $API_TOKEN" 2>/dev/null | jq -r '.name' 2>/dev/null)
    
    if [ "$EXISTING" = "Creative Testing" ]; then
        echo "   ⚠️  Existiert bereits, überspringe"
        continue
    fi
    
    # Hole Space ID der Liste
    LIST_SPACE=$(curl -s "https://api.clickup.com/api/v2/list/$LIST_ID" \
        -H "Authorization: $API_TOKEN" 2>/dev/null | jq -r '.space.id' 2>/dev/null)
    
    if [ -z "$LIST_SPACE" ] || [ "$LIST_SPACE" = "null" ]; then
        echo "   ❌ Konnte Space ID nicht ermitteln"
        continue
    fi
    
    # Erstelle Folder in diesem Space
    echo "   🆕 Erstelle Folder..."
    FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/space/$LIST_SPACE/folder" \
        -H "Authorization: $API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"Creative Testing\",\"override_statuses\":true}")
    
    if echo "$FOLDER" | jq -e '.id' > /dev/null 2>&1; then
        FOLDER_ID=$(echo "$FOLDER" | jq -r '.id')
        echo "   ✅ Folder: $FOLDER_ID"
        
        # Erstelle 3 Listen
        for list_name in "Creative Pipeline" "Creative Archive" "Creative Ideas"; do
            echo "      📝 $list_name..."
            LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$FOLDER_ID/list" \
                -H "Authorization: $API_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"name\":\"$list_name\",\"content\":\"Auto-generated for $CLIENT_NAME\"}")
            
            if echo "$LIST" | jq -e '.id' > /dev/null 2>&1; then
                echo "      ✅"
            else
                echo "      ⚠️  Existiert oder Fehler"
            fi
            sleep 1
        done
    else
        ERR=$(echo "$FOLDER" | jq -r '.err // .error // "Unknown"')
        echo "   ❌ Fehler: $ERR"
    fi
    
    echo ""
    echo "⏳ Warte 3 Sekunden..."
    sleep 3
    echo ""
done

echo "================================================"
echo "✅ Restrukturierung abgeschlossen!"
