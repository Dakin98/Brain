#!/bin/bash
# clickup-services-cron.sh (ERWEITERT)
# Wird wöchentlich aufgerufen - prüft Airtable und erstellt ClickUp Struktur
# Unterstützt: Cold Mail + Email Marketing + Paid Ads

set -e

# Bestimme Home-Verzeichnis
if [ -z "$HOME" ]; then
    HOME="$(eval echo ~$(whoami))"
fi

SCRIPT_DIR="${HOME}/.openclaw/workspace/scripts"
LOG_DIR="${HOME}/.openclaw/workspace/logs"
LOG_FILE="${LOG_DIR}/clickup-services-cron.log"
LOCK_FILE="/tmp/clickup-services-cron.lock"

mkdir -p "$LOG_DIR"

# Lock-File
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
echo "🕐 $(date): ClickUp Services Cron gestartet"

# Credentials prüfen
if [ ! -f "$HOME/.config/airtable/api_key" ]; then
    echo "❌ Airtable API Key nicht gefunden"
    exit 1
fi

AIRTABLE_API_KEY=$(cat "$HOME/.config/airtable/api_key")
AIRTABLE_BASE="appbGhxy9I18oIS8E"
AIRTABLE_TABLE="Kunden"

if [ ! -f "$HOME/.config/clickup/api_token" ]; then
    echo "❌ ClickUp API Token nicht gefunden"
    exit 1
fi

echo "🔍 Prüfe Airtable auf neue Kunden mit Services..."

# Query: Alle Services
curl -s "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE" \
  -H "Authorization: Bearer $AIRTABLE_API_KEY" \
  -G --data-urlencode "filterByFormula=AND({Status}='Aktiv',OR({Cold Mail}=TRUE(),{Email Marketing}=TRUE(),{Paid Ads}=TRUE()))" \
  -G --data-urlencode "fields[]=Firmenname" \
  -G --data-urlencode "fields[]=Status" \
  -G --data-urlencode "fields[]=Cold Mail" \
  -G --data-urlencode "fields[]=Email Marketing" \
  -G --data-urlencode "fields[]=Paid Ads" \
  -G --data-urlencode "fields[]=ClickUp Folder Created" \
  -G --data-urlencode "fields[]=ClickUp Email Marketing Created" \
  -G --data-urlencode "fields[]=ClickUp Paid Ads Created" \
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
    paid_ads = fields.get('Paid Ads', False)
    folder_created = fields.get('ClickUp Folder Created', False)
    email_created = fields.get('ClickUp Email Marketing Created', False)
    paid_ads_created = fields.get('ClickUp Paid Ads Created', False)
    
    services = []
    if cold_mail and not folder_created:
        services.append('COLD_MAIL')
    if email_marketing and not email_created:
        services.append('EMAIL_MARKETING')
    if paid_ads and not paid_ads_created:
        services.append('PAID_ADS')
    
    if services:
        services_str = ','.join(services)
        print(f'PROCESS:{record_id}::{kunde}::{services_str}')
" | while IFS= read -r line; do
    if [[ $line == PROCESS:* ]]; then
        RECORD_ID="${line#PROCESS:}"
        SERVICES="${RECORD_ID##*::}"
        RECORD_ID="${RECORD_ID%::*}"
        CLIENT_NAME="${RECORD_ID#*::}"
        RECORD_ID="${RECORD_ID%%::*}"
        
        echo ""
        echo "📋 Kunde: $CLIENT_NAME"
        echo "   Services: $SERVICES"
        
        # Cold Mail
        if [[ "$SERVICES" == *"COLD_MAIL"* ]]; then
            echo "🚀 Erstelle Cold Mail Setup..."
            if python3 "$SCRIPT_DIR/clickup-coldmail-setup.py" "$CLIENT_NAME" 2>&1; then
                echo "✅ Cold Mail erfolgreich"
                curl -s -X PATCH "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE/$RECORD_ID" \
                    -H "Authorization: Bearer $AIRTABLE_API_KEY" \
                    -H "Content-Type: application/json" \
                    --data '{"fields": {"ClickUp Folder Created": true}}' > /dev/null
                echo "✅ Airtable aktualisiert"
            else
                echo "❌ Cold Mail fehlgeschlagen"
            fi
        fi
        
        # Email Marketing
        if [[ "$SERVICES" == *"EMAIL_MARKETING"* ]]; then
            echo "🚀 Erstelle Email Marketing Setup..."
            if python3 "$SCRIPT_DIR/clickup-emailmarketing-setup.py" "$CLIENT_NAME" 2>&1; then
                echo "✅ Email Marketing erfolgreich"
                curl -s -X PATCH "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE/$RECORD_ID" \
                    -H "Authorization: Bearer $AIRTABLE_API_KEY" \
                    -H "Content-Type: application/json" \
                    --data '{"fields": {"ClickUp Email Marketing Created": true}}' > /dev/null
                echo "✅ Airtable aktualisiert"
            else
                echo "❌ Email Marketing fehlgeschlagen"
            fi
        fi
        
        # Paid Ads (spezieller Aufruf mit --name und --airtable-record)
        if [[ "$SERVICES" == *"PAID_ADS"* ]]; then
            echo "🚀 Erstelle Paid Ads Setup..."
            if python3 "$SCRIPT_DIR/paid_ads_onboarding.py" --name "$CLIENT_NAME" --airtable-record "$RECORD_ID" 2>&1; then
                echo "✅ Paid Ads erfolgreich"
                curl -s -X PATCH "https://api.airtable.com/v0/$AIRTABLE_BASE/$AIRTABLE_TABLE/$RECORD_ID" \
                    -H "Authorization: Bearer $AIRTABLE_API_KEY" \
                    -H "Content-Type: application/json" \
                    --data '{"fields": {"ClickUp Paid Ads Created": true}}' > /dev/null
                echo "✅ Airtable aktualisiert"
            else
                echo "❌ Paid Ads fehlgeschlagen"
            fi
        fi
    else
        echo "$line"
    fi
done

echo ""
echo "🏁 $(date): Cron abgeschlossen"
