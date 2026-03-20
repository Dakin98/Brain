#!/bin/bash
# Newsletter Weekly Task
# Erstellt wöchentliche Newsletter-Tasks für alle aktiven Newsletter-Kunden
# Trigger: Jeden Montag 9 Uhr via Cron

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
LOG_FILE="${WORKSPACE_DIR}/logs/newsletter-weekly.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Berechne aktuelle KW
KW=$(date +%V)
YEAR=$(date +%Y)

log "📅 Starte Weekly Newsletter Task Erstellung für KW${KW}/${YEAR}..."

# Prüfe Dependencies
if [[ -z "$CLICKUP_API_TOKEN" ]]; then
    log "❌ ERROR: CLICKUP_API_TOKEN nicht gesetzt"
    exit 1
fi

if [[ -z "$AIRTABLE_API_KEY" ]]; then
    log "❌ ERROR: AIRTABLE_API_KEY nicht gesetzt"
    exit 1
fi

# Hole aktive Newsletter-Kunden aus Airtable
# Query: Newsletter Service = true AND Newsletter Onboarding Done = true AND Status = Aktiv
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
    klaviyo_list = fields.get('Klaviyo List ID', '')
    weekly_day = fields.get('Weekly Newsletter Day', 'Mittwoch')
    
    print(f\"KUNDE:{kunde}|LIST:{klaviyo_list}|DAY:{weekly_day}\")
" | while IFS='|' read -r KUNDE_DATA; do
    
    KUNDE=$(echo "$KUNDE_DATA" | cut -d'|' -f1 | sed 's/KUNDE://')
    KLAVIYO_LIST=$(echo "$KUNDE_DATA" | cut -d'|' -f2 | sed 's/LIST://')
    DAY=$(echo "$KUNDE_DATA" | cut -d'|' -f3 | sed 's/DAY://')
    
    log "🎯 Erstelle Newsletter Task für: $KUNDE (Due: $DAY)"
    
    # Berechne Due Date basierend auf DAY
    case "$DAY" in
        "Montag")
            DUE_DAYS=0
            ;;
        "Dienstag")
            DUE_DAYS=1
            ;;
        "Mittwoch")
            DUE_DAYS=2
            ;;
        "Donnerstag")
            DUE_DAYS=3
            ;;
        "Freitag")
            DUE_DAYS=4
            ;;
        *)
            DUE_DAYS=2  # Default: Mittwoch
            ;;
    esac
    
    DUE_DATE=$(( $(date +%s) + (86400 * DUE_DAYS) ))000
    
    # Erstelle Task
    TASK_RESPONSE=$(curl -s -X POST "https://api.clickup.com/api/v2/list/${CLICKUP_LIST_ID}/task" \
        -H "Authorization: ${CLICKUP_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"📧 [${KUNDE}] Newsletter KW${KW}\",
            \"description\": \"⏱️ Aufwand: 2h\\n👤 Verantwortlich: VA\\n\\n🎯 Ziel: Wöchentlichen Newsletter für ${KUNDE} erstellen und versenden\\n\\n📧 Klaviyo List: ${KLAVIYO_LIST}\",
            \"due_date\": ${DUE_DATE},
            \"tags\": [\"newsletter\", \"weekly\", \"${KUNDE}\", \"recurring\"],
            \"status\": \"to do\"
        }")
    
    TASK_ID=$(echo "$TASK_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
    
    if [[ -n "$TASK_ID" ]]; then
        # Füge Checklist hinzu
        CHECKLIST_RESPONSE=$(curl -s -X POST "https://api.clickup.com/api/v2/task/${TASK_ID}/checklist" \
            -H "Authorization: ${CLICKUP_API_TOKEN}" \
            -H "Content-Type: application/json" \
            -d '{"name": "Weekly Newsletter Checklist"}')
        
        CHECKLIST_ID=$(echo "$CHECKLIST_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('checklist', {}).get('id', ''))" 2>/dev/null)
        
        if [[ -n "$CHECKLIST_ID" ]]; then
            ITEMS=(
                "📅 Content-Kalender prüfen (Thema der Woche)"
                "📝 Newsletter Thema festlegen"
                "🖼️ Bilder & Assets vorbereiten"
                "✍️ Copy schreiben (Headline, Body, CTA)"
                "🎨 Template anpassen (Branding konsistent)"
                "👥 Segment anpassen"
                "🧪 Test-E-Mail senden & prüfen"
                "✅ Kunden-Approval einholen (falls erforderlich)"
                "📊 Performance der letzten Woche reviewen"
                "📤 Newsletter versenden"
                "📈 48h Performance checken (Open, Click, Revenue)"
            )
            
            for ITEM in "${ITEMS[@]}"; do
                curl -s -X POST "https://api.clickup.com/api/v2/checklist/${CHECKLIST_ID}/checklist_item" \
                    -H "Authorization: ${CLICKUP_API_TOKEN}" \
                    -H "Content-Type: application/json" \
                    -d "{\"name\": \"${ITEM}\"}" > /dev/null
            done
            
            log "  ✅ Task erstellt mit 11 Checklist Items"
        fi
    else
        log "  ❌ Fehler beim Erstellen des Tasks"
    fi
done

# Sende Zusammenfassung
TASK_COUNT=$(echo "$RECORDS" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

log "🎉 Weekly Newsletter Tasks erstellt: ${TASK_COUNT} Kunden"

if [[ -n "$TELEGRAM_BOT_TOKEN" && -n "$TELEGRAM_CHAT_ID" && "$TASK_COUNT" -gt 0 ]]; then
    MESSAGE="📧%20Weekly%20Newsletter%20Tasks%20erstellt%21%0A%0AKalenderwoche%3A%20KW${KW}%2F${YEAR}%0AKunden%3A%20${TASK_COUNT}%0A%0AJeder%20Task%20enth%C3%A4lt%2011%20Checklist%20Items%20f%C3%BCr%20den%20kompletten%20Newsletter-Prozess.%0A%0A%F0%9F%91%89%20In%20ClickUp%20anzeigen"
    
    curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage?chat_id=${TELEGRAM_CHAT_ID}&text=${MESSAGE}" > /dev/null
fi
