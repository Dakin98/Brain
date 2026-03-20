#!/bin/bash
# check-airtable-fields.sh
# Prüft ob alle benötigten Felder in Airtable existieren

AIRTABLE_API_KEY=$(cat ~/.config/airtable/api_key 2>/dev/null)
AIRTABLE_BASE="appbGhxy9I18oIS8E"

echo "🔍 Prüfe Airtable Felder für ClickUp Automatisierung..."
echo ""

# Hole alle Felder
curl -s "https://api.airtable.com/v0/meta/bases/$AIRTABLE_BASE/tables" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" | python3 -c "
import json, sys
data = json.load(sys.stdin)

required_fields = [
    'Cold Mail',
    'Email Marketing', 
    'ClickUp Folder Created',
    'ClickUp Email Marketing Created'
]

for table in data.get('tables', []):
    if table['name'] == 'Kunden':
        existing_fields = [f['name'] for f in table['fields']]
        
        print('📋 Gefundene Felder:')
        for field in required_fields:
            status = '✅' if field in existing_fields else '❌ FEHLER'
            print(f'   {status} {field}')
        
        missing = [f for f in required_fields if f not in existing_fields]
        print('')
        if missing:
            print(f'❌ {len(missing)} Feld(er) fehlen!')
            print('👉 Anleitung: docs/airtable-setup-clickup.md')
        else:
            print('✅ Alle Felder vorhanden! Bereit für Automatisierung.')
" || echo "❌ Fehler beim Abrufen der Felder"
