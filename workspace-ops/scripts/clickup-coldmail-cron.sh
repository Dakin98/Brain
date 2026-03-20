#!/bin/bash
# clickup-coldmail-cron.sh (ERWEITERT)
# Wird alle 10 Minuten aufgerufen - prüft Airtable und erstellt ClickUp Folder
# Unterstützt: Cold Mail + Email Marketing

set -e

# Bestimme Home-Verzeichnis (funktioniert auch mit crontab wo $HOME leer sein kann)
if [ -z "$HOME" ]; then
    HOME="$(eval echo ~$(whoami))"
fi

SCRIPT_DIR="${HOME}/.openclaw/workspace/scripts"
LOG_DIR="${HOME}/.openclaw/workspace/logs"
LOG_FILE="${LOG_DIR}/clickup-coldmail-cron.log"
LOCK_FILE="/tmp/clickup-coldmail-cron.lock"

# Stelle sicher dass Log-Verzeichnis existiert
mkdir -p "$LOG_DIR"

# Lock-File verhindern von doppelten Ausführungen
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE" 2>/dev/null)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "$(date): Cron läuft bereits (PID: $PID)" >> "$LOG_FILE"
        exit 0
    fi
fi

echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

# Logging
exec >> "$LOG_FILE" 2>&1
echo ""
echo "========================================"
echo "🕐 $(date): ClickUp Onboarding Cron gestartet"

# Airtable API Key prüfen
if [ ! -f "$HOME/.config/airtable/api_key" ]; then
    echo "❌ Airtable API Key nicht gefunden"
    exit 1
fi

AIRTABLE_API_KEY=$(cat "$HOME/.config/airtable/api_key")
AIRTABLE_BASE="appbGhxy9I18oIS8E"
AIRTABLE_TABLE="Kunden"

# ClickUp API Token prüfen
if [ ! -f "$HOME/.config/clickup/api_token" ]; then
    echo "❌ ClickUp API Token nicht gefunden"
    exit 1
fi

# Funktion: ClickUp Setup für einen Service ausführen
run_service_setup() {
    local SERVICE_NAME="$1"
    local CLIENT_NAME="$2"
    local SCRIPT_NAME="$3"
    local RECORD_ID="$4"
    local FIELD_NAME="$5"
    
    echo ""
    echo "🚀 Erstelle $SERVICE_NAME Setup für: $CLIENT_NAME"
    
    if python3 "$SCRIPT_DIR/$SCRIPT_NAME" "$CLIENT_NAME" 2>&1; then
        echo "✅ $SERVICE_NAME Setup erfolgreich für $CLIENT_NAME"
        
        # Airtable aktualisieren (Flag setzen)
        UPDATE_RESPONSE=$(curl -s -X PATCH "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE/$RECORD_ID" \
            -H "Authorization: Bearer $AIRTABLE_API_KEY" \
            -H "Content-Type: application/json" \
            --data "{\"fields\": {\"$FIELD_NAME\": true}}")
        
        if echo "$UPDATE_RESPONSE" | grep -q '"id"'; then
            echo "✅ Airtable aktualisiert: $FIELD_NAME = true"
        else
            echo "⚠️  Airtable Update fehlgeschlagen: $UPDATE_RESPONSE"
        fi
    else
        echo "❌ $SERVICE_NAME Setup fehlgeschlagen für $CLIENT_NAME"
    fi
}

echo "🔍 Prüfe Airtable auf neue Kunden mit Services..."

# Query: Kunden mit Status "Active" und mindestens einem Service
# Formel: AND({Status} = 'Active', OR({Cold Mail}=TRUE(), {Email Marketing}=TRUE()))

curl -s "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode "filterByFormula=AND({Status}='Aktiv',OR({Cold Mail}=TRUE(),{Email Marketing}=TRUE()))" \
  -G --data-urlencode "fields[]=Firmenname" \
  -G --data-urlencode "fields[]=Status" \
  -G --data-urlencode "fields[]=Cold Mail" \
  -G --data-urlencode "fields[]=Email Marketing" \
  -G --data-urlencode "fields[]=ClickUp Folder Created" \
  -G --data-urlencode "fields[]=ClickUp Email Marketing Created" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
records = data.get('records', [])
print(f'📊 Gefunden: {len(records)} Kunden mit Services')

for r in records:
    fields = r.get('fields', {})
    record_id = r.get('id', '')
    kunde = fields.get('Firmenname', 'Unbekannt')
    cold_mail = fields.get('Cold Mail', False)
    email_marketing = fields.get('Email Marketing', False)
    folder_created = fields.get('ClickUp Folder Created', False)
    email_created = fields.get('ClickUp Email Marketing Created', False)
    
    # Services die noch eingerichtet werden müssen
    services = []
    if cold_mail and not folder_created:
        services.append('COLD_MAIL')
    if email_marketing and not email_created:
        services.append('EMAIL_MARKETING')
    
    if services:
        # Output Format: RECORD_ID::KUNDE_NAME::SERVICES
        services_str = ','.join(services)
        print(f'PROCESS:{record_id}::{kunde}::{services_str}')
" | while IFS= read -r line; do
    if [[ $line == PROCESS:* ]]; then
        # Parse: PROCESS:record_id::client_name::services
        RECORD_ID="${line#PROCESS:}"
        SERVICES="${RECORD_ID##*::}"
        RECORD_ID="${RECORD_ID%::*}"
        CLIENT_NAME="${RECORD_ID#*::}"
        RECORD_ID="${RECORD_ID%%::*}"
        
        echo ""
        echo "📋 Kunde: $CLIENT_NAME"
        echo "   Services: $SERVICES"
        
        # Cold Mail Setup
        if [[ "$SERVICES" == *"COLD_MAIL"* ]]; then
            run_service_setup "Cold Mail" "$CLIENT_NAME" "clickup-coldmail-setup.py" "$RECORD_ID" "ClickUp Folder Created"
        fi
        
        # Email Marketing Setup
        if [[ "$SERVICES" == *"EMAIL_MARKETING"* ]]; then
            run_service_setup "Email Marketing" "$CLIENT_NAME" "clickup-emailmarketing-setup.py" "$RECORD_ID" "ClickUp Email Marketing Created"
        fi
    else
        echo "$line"
    fi
done

echo ""
echo "🏁 $(date): Cron abgeschlossen"
