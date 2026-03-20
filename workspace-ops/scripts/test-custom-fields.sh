#!/bin/bash
# test-custom-fields.sh - Teste ob Custom Fields via API gehen

API_TOKEN=$(cat ~/.config/clickup/api_token 2>/dev/null)

# Eine der neuen Creative Pipeline Listen (Green Cola)
LIST_ID="901521339041"

echo "🧪 Teste Custom Field API..."
echo "=============================="
echo ""

# Versuche ein Custom Field zu erstellen
echo "📡 Erstelle Test-Field 'Client'..."

RESULT=$(curl -s -X POST "https://api.clickup.com/api/v2/list/$LIST_ID/field" \
    -H "Authorization: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Client",
        "type": "drop_down",
        "type_config": {
            "options": [
                {"name": "Green Cola Germany", "color": "#000000"},
                {"name": "schnelleinfachgesund", "color": "#000000"}
            ]
        }
    }')

echo ""
echo "Antwort:"
echo "$RESULT" | jq . 2>/dev/null || echo "$RESULT"
echo ""

if echo "$RESULT" | jq -e '.id' > /dev/null 2>&1; then
    echo "✅ GEHT! Custom Fields können via API erstellt werden."
    echo ""
    echo "Ich erstelle jetzt alle 14 Felder automatisch..."
    exit 0
else
    ERR=$(echo "$RESULT" | jq -r '.err // .EC // .error // "Unknown"')
    echo "❌ GEHT NICHT: $ERR"
    echo ""
    echo "Dein Plan erlaubt keine Custom Field API."
    echo "Du musst die 14 Felder manuell in ClickUp UI anlegen."
    exit 1
fi
