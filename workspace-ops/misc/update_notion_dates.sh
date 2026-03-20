#!/bin/bash

NOTION_KEY=$(cat ~/.config/notion/api_key)
NOTION_DB_ID="3465a32b-e5e0-4d52-bec3-c24ff39e1507"

# Hole alle Einträge
echo "Hole alle Einträge aus Notion..."
ENTRIES=$(curl -s -X POST "https://api.notion.com/v1/databases/$NOTION_DB_ID/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 100}')

# Zähler
UPDATED=0
FAILED=0

# Verarbeite jeden Eintrag
echo "$ENTRIES" | jq -c '.results[] | select(.properties.Date.date != null) | {id: .id, date: .properties.Date.date.start, name: .properties.Name.title[0].text.content}' | while read -r entry; do
    ID=$(echo "$entry" | jq -r '.id')
    OLD_DATE=$(echo "$entry" | jq -r '.date')
    NAME=$(echo "$entry" | jq -r '.name')
    
    # Ersetze 2023 mit 2026
    NEW_DATE=$(echo "$OLD_DATE" | sed 's/2023/2026/')
    
    echo "Aktualisiere: $NAME | $OLD_DATE -> $NEW_DATE"
    
    # Update über Notion API
    RESPONSE=$(curl -s -X PATCH "https://api.notion.com/v1/pages/$ID" \
      -H "Authorization: Bearer $NOTION_KEY" \
      -H "Notion-Version: 2022-06-28" \
      -H "Content-Type: application/json" \
      -d "{
        \"properties\": {
          \"Date\": {
            \"date\": {
              \"start\": \"$NEW_DATE\"
            }
          }
        }
      }")
    
    if echo "$RESPONSE" | jq -e '.object == "page"' > /dev/null 2>&1; then
        echo "  ✓ Erfolgreich aktualisiert"
        ((UPDATED++))
    else
        echo "  ✗ Fehler: $(echo "$RESPONSE" | jq -r '.message // "Unbekannter Fehler"')"
        ((FAILED++))
    fi
    
    # Kurze Pause um Rate Limits zu vermeiden
    sleep 0.3
done

echo ""
echo "========================================="
echo "Update abgeschlossen!"
echo "Erfolgreich: $UPDATED"
echo "Fehler: $FAILED"
