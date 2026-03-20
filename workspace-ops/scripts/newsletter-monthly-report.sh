#!/bin/bash
# Newsletter Monthly Reporting Task
# Erstellt monatliche Reporting-Tasks für alle aktiven Newsletter-Kunden
# Trigger: 1. des Monats 9 Uhr via Cron

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

# Konfiguration
AIRTABLE_BASE_ID="${AIRTABLE_BASE_ID:-appbGhxy9I18oIS8E}"
AIRTABLE_TABLE_NAME="${AIRTABLE_TABLE_NAME:-Kunden}"
CLICKUP_API_TOKEN="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
CLICKUP_LIST_ID="${CLICKUP_LIST_ID:-901507242261}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-6607099798}"

# Logging
LOG_FILE="${WORKSPACE_DIR}/logs/newsletter-monthly.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Berechne aktuellen Monat
MONAT=$(date +%B)
YEAR=$(date +%Y)

log "📊 Starte Monthly Reporting Task Erstellung für ${MONAT} ${YEAR}..."

# Prüfe Dependencies
if [[ -z "$CLICKUP_API_TOKEN" ]]; then
    log "❌ ERROR: CLICKUP_API_TOKEN nicht gesetzt"
    exit 1
fi

if [[ -z "$AIRTABLE_API_KEY" ]]; then
    log "❌ ERROR: AIRTABLE_API_KEY nicht gesetzt"
    exit 1
fi

# Hole aktive Newsletter-Kunden
FORMULA="AND%28%7BNewsletter%20Service%7D%20%3D%20TRUE%28%29%2C%20%7BNewsletter%20Onboarding%20Done%7D%20%3D%20TRUE%28%29%2C%20%7BStatus%7D%20%3D%20%27Aktiv%27%29"

RESPONSE=$(curl -s "https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${AIRTABLE_TABLE_NAME}?filterByFormula=${FORMULA}" \
    -H "Authorization: Bearer ${AIRTABLE_API_KEY}")

RECORDS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('records', []))" 2>/dev/null)

if [[ "$RECORDS" == "[]" ]]; then
    log "ℹ️ Keine aktiven Newsletter-Kunden gefunden"
    exit 0
fi

# Verarbeite jeden Kunden
echo "$RESPONSE" | python3 -c "
import sys, json

data = json.load(sys.stdin)
records = data.get('records', [])

for record in records:
    fields = record.get('fields', {})
    
    kunde = fields.get('Firmenname', 'Unbekannt')
    klaviyo_account = fields.get('Klaviyo Account ID', '')
    
    print(f\"KUNDE:{kunde}|ACCOUNT:{klaviyo_account}\")
" | while IFS='|' read -r KUNDE_DATA; do
    
    KUNDE=$(echo "$KUNDE_DATA" | cut -d'|' -f1 | sed 's/KUNDE://')
    
    log "🎯 Erstelle Monthly Report für: $KUNDE"
    
    # Due Date: +5 Tage
    DUE_DATE=$(( $(date +%s) + 432000 ))000
    
    # Erstelle Task
    TASK_RESPONSE=$(curl -s -X POST "https://api.clickup.com/api/v2/list/${CLICKUP_LIST_ID}/task" \
        -H "Authorization: ${CLICKUP_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"📊 [${KUNDE}] Monthly Report ${MONAT} ${YEAR}\",
            \"description\": \"⏱️ Aufwand: 2-3h\\n👤 Verantwortlich: Deniz\\n\\n🎯 Ziel: Performance des Vormonats analysieren und Report für Kunden erstellen\",
            \"due_date\": ${DUE_DATE},
            \"tags\": [\"newsletter\", \"monthly\", \"reporting\", \"${KUNDE}\", \"recurring\"],
            \"status\": \"to do\"
        }")
    
    TASK_ID=$(echo "$TASK_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
    
    if [[ -n "$TASK_ID" ]]; then
        # Füge Checklist hinzu
        CHECKLIST_RESPONSE=$(curl -s -X POST "https://api.clickup.com/api/v2/task/${TASK_ID}/checklist" \
            -H "Authorization: ${CLICKUP_API_TOKEN}" \
            -H "Content-Type: application/json" \
            -d '{"name": "Monthly Review Checklist"}')
        
        CHECKLIST_ID=$(echo "$CHECKLIST_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('checklist', {}).get('id', ''))" 2>/dev/null)
        
        if [[ -n "$CHECKLIST_ID" ]]; then
            ITEMS=(
                "📊 Monatliche KPIs sammeln (Open Rate, CTR, Revenue, Unsubscribes)"
                "📈 Benchmarks vergleichen (vs. letzter Monat / Industry Average)"
                "🏆 Top-Performing Campaigns identifizieren"
                "💀 Underperformers analysieren (Was lief schief?)"
                "🔄 Flow Performance checken (Revenue per Recipient)"
                "📧 List Hygiene (Bounces, Unsubscribes bereinigen)"
                "🧪 A/B Test Ergebnisse dokumentieren"
                "💡 Optimierungs-Ideen sammeln"
                "📝 Report für Kunden erstellen"
                "🎯 Nächstes Monats-Ziel setzen"
                "🔧 Flows & Segmente anpassen (basierend auf Daten)"
                "🤝 Kunden-Call vorbereiten (Ergebnisse präsentieren)"
            )
            
            for ITEM in "${ITEMS[@]}"; do
                curl -s -X POST "https://api.clickup.com/api/v2/checklist/${CHECKLIST_ID}/checklist_item" \
                    -H "Authorization: ${CLICKUP_API_TOKEN}" \
                    -H "Content-Type: application/json" \
                    -d "{\"name\": \"${ITEM}\"}" > /dev/null
            done
            
            log "  ✅ Task erstellt mit 12 Checklist Items"
        fi
    else
        log "  ❌ Fehler beim Erstellen des Tasks"
    fi
done

# Sende Zusammenfassung
TASK_COUNT=$(echo "$RECORDS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

log "🎉 Monthly Reporting Tasks erstellt: ${TASK_COUNT} Kunden"

if [[ -n "$TELEGRAM_BOT_TOKEN" && -n "$TELEGRAM_CHAT_ID" && "$TASK_COUNT" -gt 0 ]]; then
    MESSAGE="📊%20Monthly%20Reporting%20Tasks%20erstellt%21%0A%0AMonat%3A%20${MONAT}%20${YEAR}%0AKunden%3A%20${TASK_COUNT}%0A%0AJeder%20Task%20enth%C3%A4lt%2012%20Checklist%20Items%20f%C3%BCr%20die%20monatliche%20Performance-Analyse.%0A%0A%F0%9F%91%89%20In%20ClickUp%20anzeigen"
    
    curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=${TELEGRAM_CHAT_ID}&text=${MESSAGE}" > /dev/null
fi
