#!/bin/bash
# clickup-coldmail-onboarding.sh
# Prüft Airtable auf neue Kunden mit Cold Mail Service und erstellt ClickUp Struktur

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/clickup-coldmail-setup.py"

# Airtable Config (aus MEMORY.md)
AIRTABLE_BASE="appbGhxy9I18oIS8E"
AIRTABLE_TABLE="Kunden"

# Prüfe ob Airtable API Key existiert
if [ ! -f "$HOME/.config/airtable/api_key" ]; then
    echo "❌ Airtable API Key nicht gefunden"
    exit 1
fi

AIRTABLE_API_KEY=$(cat "$HOME/.config/airtable/api_key")

echo "🔍 Prüfe Airtable auf neue Kunden mit Cold Mail Service..."

# Query: Kunden mit Status "Active" und Cold Mail Service = true
# Airtable formula: AND({Status} = 'Active', {Cold Mail} = TRUE())

curl -s "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode "filterByFormula=AND({Status}='Active', {Cold Mail}=TRUE())" \
  -G --data-urlencode "fields[]=Kunde" \
  -G --data-urlencode "fields[]=Status" \
  -G --data-urlencode "fields[]=Cold Mail" \
  -G --data-urlencode "fields[]=ClickUp Folder Created" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
records = data.get('records', [])
print(f'📊 Gefunden: {len(records)} Kunden mit Cold Mail Service')

for r in records:
    fields = r.get('fields', {})
    kunde = fields.get('Kunde', 'Unbekannt')
    folder_created = fields.get('ClickUp Folder Created', False)
    
    if not folder_created:
        print(f'  🆕 Neuer Kunde: {kunde}')
        print(f'     ClickUp Folder muss erstellt werden!')
        # Output für Bash-Processing
        print(f'CREATE_FOLDER:{kunde}')
    else:
        print(f'  ✅ Bereits eingerichtet: {kunde}')
" | while read line; do
    if [[ $line == CREATE_FOLDER:* ]]; then
        CLIENT_NAME="${line#CREATE_FOLDER:}"
        echo ""
        echo "🚀 Erstelle Cold Mail Setup für: $CLIENT_NAME"
        
        # ClickUp Setup ausführen
        if python3 "$PYTHON_SCRIPT" "$CLIENT_NAME"; then
            echo "✅ ClickUp Setup erfolgreich"
            
            # Airtable aktualisieren (Flag setzen)
            # Hier müsste man die Record ID haben...
            echo "⚠️  Airtable Update noch nicht implementiert (Record ID fehlt)"
        else
            echo "❌ ClickUp Setup fehlgeschlagen"
        fi
    else
        echo "$line"
    fi
done

echo ""
echo "🏁 Check abgeschlossen"
