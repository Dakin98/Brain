#!/bin/bash
# Newsletter Onboarding Auto-Setup v2
# Erstellt Parent + Subtasks im Kunden-Folder

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

# Konfiguration
AIRTABLE_BASE_ID="${AIRTABLE_BASE_ID:-appbGhxy9I18oIS8E}"
AIRTABLE_TABLE_NAME="${AIRTABLE_TABLE_NAME:-Kunden}"
CLICKUP_API_TOKEN="${CLICKUP_API_TOKEN:-$(cat ~/.config/clickup/api_token 2>/dev/null || echo "")}"
TEAM_ID="9006104573"
DELIVERY_SPACE="90040311585"

# Logging
LOG_FILE="${WORKSPACE_DIR}/logs/newsletter-onboarding.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Prüfe Dependencies
if [[ -z "$CLICKUP_API_TOKEN" ]]; then
    log "❌ ERROR: CLICKUP_API_TOKEN nicht gesetzt"
    exit 1
fi

if [[ -z "$AIRTABLE_API_KEY" ]]; then
    log "❌ ERROR: AIRTABLE_API_KEY nicht gesetzt"
    exit 1
fi

# Funktion: Finde oder erstelle "📧 Email Content" Liste im Kunden-Folder
get_or_create_email_list() {
    local FOLDER_ID="$1"
    local FOLDER_NAME="$2"
    
    # Prüfe ob "📧 Email Content" Liste existiert
    LISTS=$(curl -s "https://api.clickup.com/api/v2/folder/${FOLDER_ID}/list?archived=false" \
        -H "Authorization: ${CLICKUP_API_TOKEN}")
    
    LIST_ID=$(echo "$LISTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for lst in data.get('lists', []):
    if '📧' in lst['name'] or 'Email' in lst['name']:
        print(lst['id'])
        break
" 2>/dev/null)
    
    if [[ -n "$LIST_ID" ]]; then
        echo "$LIST_ID"
        return
    fi
    
    # Erstelle neue Liste
    log "    📋 Erstelle 'Newsletter' Liste in ${FOLDER_NAME}..."
    
    NEW_LIST=$(curl -s -X POST "https://api.clickup.com/api/v2/folder/${FOLDER_ID}/list" \
        -H "Authorization: ${CLICKUP_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"📧 Newsletter\",
            \"content\": \"E-Mail Marketing Tasks für ${FOLDER_NAME}\"
        }")
    
    echo "$NEW_LIST" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null
}

# Funktion: Erstelle Parent Task
create_parent_task() {
    local LIST_ID="$1"
    local KUNDE="$2"
    
    log "    📋 Erstelle Parent Task..."
    
    TASK=$(curl -s -X POST "https://api.clickup.com/api/v2/list/${LIST_ID}/task" \
        -H "Authorization: ${CLICKUP_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"[TEMPLATE] 📧 Newsletter Workflow — ${KUNDE}\",
            \"description\": \"🎯 **Newsletter Onboarding Workflow**\\n\\n⏱️ **Gesamtaufwand:** ~2 Wochen\\n👤 **Verantwortlich:** Team\\n\\nAlle Subtasks enthalten detaillierte Checklisten.\",
            \"tags\": [\"newsletter\", \"onboarding\", \"template\"],
            \"status\": \"to do\"
        }")
    
    echo "$TASK" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null
}

# Funktion: Erstelle Subtask mit Checklist
create_subtask_with_checklist() {
    local PARENT_ID="$1"
    local NAME="$2"
    local DESCRIPTION="$3"
    local DUE_DAYS="$4"
    shift 4
    local CHECKLIST_ITEMS=("$@")
    
    DUE_DATE=$(( $(date +%s) + (86400 * DUE_DAYS) ))000
    
    log "      📝 Erstelle Subtask: ${NAME}..."
    
    # Erstelle Subtask
    SUBTASK=$(curl -s -X POST "https://api.clickup.com/api/v2/task/${PARENT_ID}/subtask" \
        -H "Authorization: ${CLICKUP_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"${NAME}\",
            \"description\": \"${DESCRIPTION}\",
            \"due_date\": ${DUE_DATE},
            \"tags\": [\"newsletter\", \"onboarding\"],
            \"status\": \"to do\"
        }")
    
    SUBTASK_ID=$(echo "$SUBTASK" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
    
    if [[ -z "$SUBTASK_ID" ]]; then
        log "      ❌ Fehler beim Erstellen des Subtasks"
        return
    fi
    
    # Erstelle Checklist
    CHECKLIST=$(curl -s -X POST "https://api.clickup.com/api/v2/task/${SUBTASK_ID}/checklist" \
        -H "Authorization: ${CLICKUP_API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d '{"name": "Checklist"}')
    
    CHECKLIST_ID=$(echo "$CHECKLIST" | python3 -c "import sys,json; print(json.load(sys.stdin).get('checklist', {}).get('id', ''))" 2>/dev/null)
    
    if [[ -n "$CHECKLIST_ID" ]]; then
        for ITEM in "${CHECKLIST_ITEMS[@]}"; do
            curl -s -X POST "https://api.clickup.com/api/v2/checklist/${CHECKLIST_ID}/checklist_item" \
                -H "Authorization: ${CLICKUP_API_TOKEN}" \
                -H "Content-Type: application/json" \
                -d "{\"name\": \"${ITEM}\"}" > /dev/null
        done
    fi
    
    echo "$SUBTASK_ID"
}

# Hole neue Newsletter-Kunden aus Airtable
log "🔍 Suche neue Newsletter-Kunden in Airtable..."

FORMULA="AND%28%7BNewsletter%20Service%7D%20%3D%20TRUE%28%29%2C%20%7BNewsletter%20Onboarding%20Done%7D%20%21%3D%20TRUE%28%29%29"

RESPONSE=$(curl -s "https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${AIRTABLE_TABLE_NAME}?filterByFormula=${FORMULA}" \
    -H "Authorization: Bearer ${AIRTABLE_API_KEY}")

RECORDS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('records', []))" 2>/dev/null)

if [[ "$RECORDS" == "[]" ]]; then
    log "✅ Keine neuen Newsletter-Kunden gefunden"
    exit 0
fi

# Verarbeite jeden Kunden
echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
records = data.get('records', [])

for record in records:
    fields = record.get('fields', {})
    record_id = record.get('id')
    
    kunde = fields.get('Firmenname', 'Unbekannt')
    
    print(f\"KUNDE:{kunde}|RECORD:{record_id}\")
" | while IFS='|' read -r KUNDE_DATA; do
    
    KUNDE=$(echo "$KUNDE_DATA" | cut -d'|' -f1 | sed 's/KUNDE://')
    RECORD_ID=$(echo "$KUNDE_DATA" | cut -d'|' -f2 | sed 's/RECORD://')
    
    log "🎯 Starte Onboarding für: $KUNDE"
    
    # Suche Kunden-Folder in ClickUp
    log "  🔍 Suche Folder für ${KUNDE}..."
    
    FOLDERS=$(curl -s "https://api.clickup.com/api/v2/space/${DELIVERY_SPACE}/folder?archived=false" \
        -H "Authorization: ${CLICKUP_API_TOKEN}")
    
    # Suche Folder mit ähnlichem Namen
    FOLDER_ID=$(echo "$FOLDERS" | python3 -c "
import sys, json, re
data = json.load(sys.stdin)
kunde = '${KUNDE}'.replace('🧪 ', '').replace(' GmbH', '').replace(' UG', '').strip().lower()

for folder in data.get('folders', []):
    folder_name = folder['name'].lower()
    # Prüfe ob Kundenname im Folder-Namen vorkommt
    if kunde in folder_name or folder_name in kunde:
        print(folder['id'])
        break
" 2>/dev/null)
    
    if [[ -z "$FOLDER_ID" ]]; then
        log "  📁 Kein Folder für ${KUNDE} gefunden, erstelle neuen Folder..."
        
        # Erstelle neuen Folder
        NEW_FOLDER=$(curl -s -X POST "https://api.clickup.com/api/v2/space/${DELIVERY_SPACE}/folder" \
            -H "Authorization: ${CLICKUP_API_TOKEN}" \
            -H "Content-Type: application/json" \
            -d "{
                \"name\": \"${KUNDE}\"
            }")
        
        FOLDER_ID=$(echo "$NEW_FOLDER" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
        
        if [[ -z "$FOLDER_ID" ]]; then
            log "  ❌ Konnte Folder nicht erstellen"
            continue
        fi
        
        FOLDER_NAME="${KUNDE}"
        log "  ✅ Folder erstellt: ${FOLDER_NAME}"
    fi
    
    FOLDER_NAME=$(echo "$FOLDERS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for folder in data.get('folders', []):
    if folder['id'] == '${FOLDER_ID}':
        print(folder['name'])
        break
" 2>/dev/null)
    
    log "  📁 Gefunden: ${FOLDER_NAME}"
    
    # Hole oder erstelle Email Content Liste
    LIST_ID=$(get_or_create_email_list "$FOLDER_ID" "$FOLDER_NAME")
    
    if [[ -z "$LIST_ID" ]]; then
        log "  ❌ Konnte keine Liste erstellen"
        continue
    fi
    
    # Erstelle Parent Task
    PARENT_ID=$(create_parent_task "$LIST_ID" "$KUNDE")
    
    if [[ -z "$PARENT_ID" ]]; then
        log "  ❌ Konnte Parent Task nicht erstellen"
        continue
    fi
    
    log "  ✅ Parent Task erstellt: ${PARENT_ID}"
    
    # Erstelle 5 Subtasks mit Checklists
    
    # Task 1: Kickoff
    ITEMS1=(
        "📧 Klaviyo Account Zugang erhalten (Admin/Besitzer Rechte)"
        "🔐 Shopify/Plattform Integration einrichten (API Keys)"
        "📋 Bestandsdaten exportieren (Kundenliste, Tags, Historie)"
        "📊 Aktuelle E-Mail Performance Daten sichern"
        "🎨 Brand Assets sammeln (Logo, Farben, Fonts, Bilder)"
        "📝 Brand Voice & Tone Guide erstellen"
        "⚖️ Rechtliche Grundlagen klären (Impressum, Datenschutz)"
        "📅 Campaign Kalender für jeden Monat erstellen"
        "🚫 Double Opt-in von ALLEN Listen entfernen"
        "📊 Starke Lead-Gen mit Pop-ups (Ziel: 10% Opt-in Rate)"
    )
    create_subtask_with_checklist "$PARENT_ID" \
        "📧 Kickoff & Zugänge sichern" \
        "⏱️ Aufwand: 1-2h\\n👤 Verantwortlich: Deniz" \
        1 "${ITEMS1[@]}" > /dev/null
    
    # Task 2: Account Setup
    ITEMS2=(
        "🏢 Account Einstellungen konfigurieren (Zeitzone, Währung, Absender)"
        "📧 Sending Domain einrichten & authentifizieren (DKIM, SPF, DMARC)"
        "📊 Tracking Domain einrichten"
        "👥 Kontakte importieren"
        "🏷️ Custom Properties anlegen"
        "🎯 Standard-Segmente erstellen (VIP, Aktiv, Inaktiv, Neukunden)"
        "💰 RFM-Segmente einrichten"
        "🛒 Product Feeds konfigurieren"
        "📱 Mobile Optimization prüfen"
        "🌐 Dedicated Sending Domain einrichten"
        "🔐 ANIBIMI erstellen"
        "📧 Whitelist-Anfrage an große Provider"
        "🧹 Liste monatlich bereinigen"
    )
    create_subtask_with_checklist "$PARENT_ID" \
        "🔧 Account Setup & Segmentierung" \
        "⏱️ Aufwand: 3-4h\\n👤 Verantwortlich: VA" \
        3 "${ITEMS2[@]}" > /dev/null
    
    # Task 3: Flow-Strategie
    ITEMS3=(
        "👋 Welcome Flow erstellen (4-8 Emails)"
        "🛒 Abandoned Cart Flow"
        "👀 Browse Abandonment Flow"
        "💰 Win-Back Flow"
        "⭐ Post-Purchase Flow"
        "🎂 Birthday Flow (falls relevant)"
        "⚡ Exit-Intent Popup konfigurieren"
        "🧪 Alle Flows testen"
        "📊 Flow Analytics Tracking einrichten"
        "⛔ Flow Exclusions korrekt setzen"
        "🧩 Conditional Logic einrichten"
        "🔄 A/B/C/D Testing für Sending Times"
    )
    create_subtask_with_checklist "$PARENT_ID" \
        "🔄 Flow-Strategie & Setup" \
        "⏱️ Aufwand: 6-8h\\n👤 Verantwortlich: Deniz + VA" \
        7 "${ITEMS3[@]}" > /dev/null
    
    # Task 4: Template Design
    ITEMS4=(
        "🎨 Brand Kit in Klaviyo einrichten"
        "📱 Master Template erstellen"
        "✉️ Newsletter Template"
        "🛍️ Product Highlight Template"
        "💬 Plain-Text Template"
        "🎂 Transactional Templates"
        "📋 Footer mit Legal Links"
        "🖼️ Bilder optimieren"
        "📱 Mobile Preview testen"
        "🧪 Dark Mode Kompatibilität prüfen"
        "🎭 GIFs verwenden für interaktive Emails"
        "📝 Plain Text Emails senden"
        "👀 IMMER Preview an sich selbst senden"
    )
    create_subtask_with_checklist "$PARENT_ID" \
        "🎨 Template Design & Branding" \
        "⏱️ Aufwand: 3-4h\\n👤 Verantwortlich: VA" \
        10 "${ITEMS4[@]}" > /dev/null
    
    # Task 5: Erste Campaign
    ITEMS5=(
        "🎯 Campaign-Ziel definieren"
        "👥 Ziel-Segment auswählen"
        "✍️ Subject Line schreiben (A/B Test)"
        "📝 E-Mail Copy erstellen"
        "🖼️ Bilder & Assets einfügen"
        "🔗 Alle Links testen"
        "📱 Preview Text optimieren"
        "🧪 Test-E-Mail an Team senden"
        "📊 Tracking & UTM Parameter setzen"
        "📅 Sendezeit planen"
        "🚀 Campaign senden"
        "📈 First 24h Monitoring"
    )
    create_subtask_with_checklist "$PARENT_ID" \
        "🚀 Erste Campaign Launch" \
        "⏱️ Aufwand: 2-3h\\n👤 Verantwortlich: Deniz" \
        14 "${ITEMS5[@]}" > /dev/null
    
    # Markiere Onboarding als erledigt in Airtable
    log "  ✅ Markiere Onboarding als erledigt in Airtable..."
    
    curl -s -X PATCH "https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${AIRTABLE_TABLE_NAME}/${RECORD_ID}" \
        -H "Authorization: Bearer ${AIRTABLE_API_KEY}" \
        -H "Content-Type: application/json" \
        -d '{
            "fields": {
                "Newsletter Onboarding Done": true
            }
        }' > /dev/null
    
    log "✅ Onboarding für $KUNDE abgeschlossen (1 Parent + 5 Subtasks)"
done

log "🎉 Newsletter Onboarding Setup abgeschlossen!"
