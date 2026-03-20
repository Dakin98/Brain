#!/bin/bash
# setup-creative-testing.sh - ClickUp Struktur aufbauen via curl

API_TOKEN=$(cat ~/.config/clickup/api_token 2>/dev/null)
SPACE_ID="90040311585"  # Delivery Space

if [ -z "$API_TOKEN" ]; then
    echo "❌ Kein API Token gefunden"
    exit 1
fi

echo "🚀 ClickUp Creative Testing Setup"
echo "=================================="
echo ""

# Get all folders in Delivery space
echo "📁 Lade Folder-Struktur..."
FOLDERS=$(curl -s "https://api.clickup.com/api/v2/space/$SPACE_ID/folder" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json")

# Check if we got valid response
if echo "$FOLDERS" | jq -e '.folders' > /dev/null 2>&1; then
    echo "✅ Folder-Struktur geladen"
else
    echo "❌ Fehler beim Laden: $FOLDERS"
    exit 1
fi

# Find client folders and create Creative Testing structure
echo ""
echo "🔍 Suche Client-Folders..."
echo ""

CLIENTS=("Green Cola Germany" "schnelleinfachgesund" "Ferro Berlin" "RAZECO" "ATB Bau")

for client in "${CLIENTS[@]}"; do
    echo "📂 Client: $client"
    
    # Find folder ID
    FOLDER_ID=$(echo "$FOLDERS" | jq -r ".folders[] | select(.name == \"$client\") | .id")
    
    if [ -z "$FOLDER_ID" ] || [ "$FOLDER_ID" = "null" ]; then
        echo "   ⚠️  Folder nicht gefunden"
        continue
    fi
    
    echo "   Folder ID: $FOLDER_ID"
    
    # Check if Creative Testing folder already exists
    SUBFOLDERS=$(curl -s "https://api.clickup.com/api/v2/space/$SPACE_ID/folder" \
        -H "Authorization: $API_TOKEN")
    
    # Create Creative Testing folder
    echo "   🆕 Erstelle 'Creative Testing' Folder..."
    
    CT_FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/space/$SPACE_ID/folder" \
        -H "Authorization: $API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"name\":\"Creative Testing\",\"override_statuses\":true}")
    
    if echo "$CT_FOLDER" | jq -e '.id' > /dev/null 2>&1; then
        CT_FOLDER_ID=$(echo "$CT_FOLDER" | jq -r '.id')
        echo "   ✅ Folder erstellt: $CT_FOLDER_ID"
        
        # Create Lists
        for list_name in "Creative Pipeline" "Creative Archive" "Creative Ideas"; do
            echo "      📝 Erstelle Liste: $list_name..."
            
            LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/$CT_FOLDER_ID/list" \
                -H "Authorization: $API_TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"name\":\"$list_name\",\"content\":\"Auto-generated\"}")
            
            if echo "$LIST" | jq -e '.id' > /dev/null 2>&1; then
                echo "      ✅ Liste erstellt"
            else
                echo "      ⚠️  Liste existiert oder Fehler"
            fi
        done
    else
        echo "   ⚠️  Folder existiert oder Fehler: $(echo "$CT_FOLDER" | jq -r '.err // .error // "Unknown"')"
    fi
    
    echo ""
done

echo "=================================="
echo "✅ Setup versucht!"
