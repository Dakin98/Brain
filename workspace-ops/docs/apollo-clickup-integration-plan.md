# Apollo + ClickUp Campaign Management System

## Maton API Gateway + Apollo.io Integration

**Ziel:** Vollständig automatisiertes Campaign Management von Lead-Suche bis Reply-Handling
**Stack:** Apollo (Leads) → Maton Gateway → ClickUp (Management) → Automationen
**Status:** Planung

---

## 🏗️ ARCHITEKTUR

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APOLLO.IO                                     │
│  • People Search (ICP-basiert)                                      │
│  • Enrichment (Email, Phone, Title)                                 │
│  • Company Data (Revenue, Employees)                                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    Maton API Gateway
                    (API Key: $MATON_API_KEY)
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      CLICKUP OUTBOUND ENGINE                         │
│  📊 Campaigns ← → 👥 Lead Lists ← → 💬 Reply Management              │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    Automatisierungen
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         REPORTING                                    │
│  • Weekly Performance Dashboard                                     │
│  • Campaign Analytics                                               │
│  • Reply Rate Tracking                                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 MATON APOLLO INTEGRATION

### API Endpoints

```bash
# Base URL
https://gateway.maton.ai/apollo/v1

# Authentication
Authorization: Bearer $MATON_API_KEY
```

### 1. People Search

```bash
POST /people/search
```

**Request:**
```json
{
  "person_titles": ["CEO", "Founder", "E-commerce Manager"],
  "person_locations": ["Germany", "Austria", "Switzerland"],
  "organization_industry_tag_ids": ["5567e0c57369640002a301c0"],
  "organization_num_employees_range": ["11-50", "51-200"],
  "per_page": 100,
  "page": 1
}
```

**Response:**
```json
{
  "people": [
    {
      "id": "64a1b2c3d4e5f6g7h8i9j0k1",
      "first_name": "Max",
      "last_name": "Mustermann",
      "name": "Max Mustermann",
      "linkedin_url": "https://linkedin.com/in/maxmustermann",
      "title": "CEO",
      "organization": {
        "name": "Fashion Brand GmbH",
        "domain": "fashionbrand.de",
        "industry": "Apparel & Fashion"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 100,
    "total_entries": 2500
  }
}
```

### 2. Enrichment (Email Reveal)

```bash
POST /people/bulk_enrich
```

**Request:**
```json
{
  "people": [
    {
      "id": "64a1b2c3d4e5f6g7h8i9j0k1",
      "reveal_email": true,
      "reveal_phone": false
    }
  ]
}
```

**Response:**
```json
{
  "people": [
    {
      "id": "64a1b2c3d4e5f6g7h8i9j0k1",
      "email": "max@fashionbrand.de",
      "phone": null,
      "email_status": "verified"
    }
  ]
}
```

### 3. Company Enrichment

```bash
GET /organizations?domain=fashionbrand.de
```

---

## 📋 WORKFLOW: KOMPLETTE CAMPAIGN ERSTELLUNG

### Phase 1: ICP Definition & Lead Search (ClickUp → Apollo)

**Trigger:** Neue Lead List in ClickUp erstellt

**Ablauf:**
```
1. User erstellt Task in "👥 Lead Lists" mit:
   - List Name: "Fashion DACH Q1"
   - ICP: Fashion DACH
   - Target Count: 500

2. Webhook → Automation Script

3. Apollo API Call:
   POST /people/search
   {
     "person_titles": ["CEO", "Founder", "E-commerce Manager"],
     "person_locations": ["Germany", "Austria", "Switzerland"],
     "organization_industry_tag_ids": ["fashion_tag_id"],
     "per_page": 100
   }

4. Pagination Loop (bis 500 Leads)

5. Bulk Enrichment für alle gefundenen

6. Speichern als JSON/CSV

7. ClickUp Task updaten:
   - Total Leads: 500
   - Validated: false
   - Source: Apollo
   - Upload Date: today
   - Attachment: leads.json
```

**Script:** `apollo-lead-search.sh`

### Phase 2: Lead Validierung & Cleaning

**Trigger:** Lead List hat Status "Needs Validation"

**Ablauf:**
```
1. Script lädt leads.json

2. Validation Checks:
   - Email-Format prüfen
   - Duplikate entfernen (basierend auf email)
   - Bounce-Check (optional: ZeroBounce API)
   - Company Domain validieren

3. Bereinigte Liste: leads_cleaned.json

4. ClickUp Task updaten:
   - Validated: true
   - Total Leads: [aktualisiert nach Cleaning]
   - Attachment: leads_cleaned.json
```

**Script:** `lead-validation.sh`

### Phase 3: Campaign Setup (Apollo → ClickUp)

**Trigger:** Neue Campaign in ClickUp erstellt

**Ablauf:**
```
1. User erstellt Task in "📊 Campaigns" mit:
   - Campaign Name: "Fashion DACH - Case Study"
   - ICP: Fashion DACH
   - Sequence: "Case Study Sequence"
   - Daily Send Limit: 40

2. Webhook → Automation Script

3. Prüfen: Lead List mit ICP vorhanden?
   → Wenn nein: Fehlermeldung

4. Campaign in Apollo erstellen (falls API verfügbar)
   ODER: Campaign-ID generieren für Tracking

5. ClickUp Task updaten:
   - Lead Count: [aus Lead List]
   - Campaign Status: Draft
   - Launch Date: [berechnet]

6. Erstelle Sub-Tasks:
   - [ ] Sequence finalisieren
   - [ ] Test-Emails senden
   - [ ] Campaign launch
```

**Script:** `campaign-setup.sh`

### Phase 4: Reply Management (Apollo → ClickUp)

**Trigger:** Neue Antwort in Apollo

**Ablauf:**
```
1. Apollo Webhook (oder Cron-Check alle 15 Min)

2. Neue Replies abrufen:
   GET /emailer_messages/search
   {
     "status": "replied",
     "updated_at[gte]": "2026-02-24T10:00:00Z"
   }

3. Für jede Antwort:
   
   a) Lead Info anreichern (Name, Company, Campaign)
   
   b) Reply kategorisieren:
      - "Interested" → Keywords: "interested", "call", "meeting", "price"
      - "Question" → Keywords: "how", "what", "?"
      - "Not Interested" → Keywords: "not interested", "no", "unsubscribe"
      - "OOO" → Keywords: "out of office", "vacation"
   
   c) ClickUp Task erstellen in "💬 Reply Management":
      - Lead Name: [Name]
      - Email: [Email]
      - Company: [Company]
      - Campaign: [Campaign Name]
      - Reply Type: [Kategorie]
      - Reply Snippet: [Erste 200 Zeichen]
   
   d) Wenn "Interested":
      - Priorität: High
      - Due Date: +4h (schnelle Antwort)
      - CRM Task verlinken (falls vorhanden)

4. Apollo markieren als "processed"
```

**Script:** `reply-sync.sh` (alle 15 Min via Cron)

### Phase 5: Performance Tracking

**Trigger:** Täglich 9 Uhr (Cron)

**Ablauf:**
```
1. Alle aktiven Campaigns aus ClickUp laden

2. Für jede Campaign Apollo Stats abrufen:
   GET /emailer_campaigns/[campaign_id]/stats
   
   Response:
   {
     "emails_sent": 1200,
     "emails_opened": 480,
     "emails_replied": 36,
     "meetings_booked": 4
   }

3. Berechnungen:
   - Open Rate: (480/1200) * 100 = 40%
   - Reply Rate: (36/1200) * 100 = 3%
   - Meeting Rate: (4/1200) * 100 = 0.33%

4. ClickUp Campaign Task updaten:
   - Reply Rate %: 3
   - Meeting Rate %: 0.33

5. Weekly Report erstellen (Montag 9 Uhr):
   - Alle Campaigns aggregiert
   - Beste/Worste Campaign
   - Empfehlungen
```

**Script:** `campaign-analytics.sh`

---

## 🤖 AUTOMATISIERUNGEN

### 1. Apollo Lead Search Automation

**Script:** `scripts/apollo-lead-search.sh`

```bash
#!/bin/bash
# Usage: ./apollo-lead-search.sh "List Task ID" "ICP" "Target Count"

LIST_TASK_ID=$1
ICP=$2
TARGET_COUNT=$3

# Maton API Key
MATON_KEY=${MATON_API_KEY}

# ClickUp API Key
CLICKUP_KEY=${CLICKUP_API_TOKEN}

# 1. Apollo Search basierend auf ICP
case $ICP in
  "Fashion DACH")
    TITLES='["CEO","Founder","E-commerce Manager"]'
    LOCATIONS='["Germany","Austria","Switzerland"]'
    INDUSTRY="fashion"
    ;;
  "Beauty DACH")
    TITLES='["CEO","Founder","Marketing Manager"]'
    LOCATIONS='["Germany","Austria","Switzerland"]'
    INDUSTRY="beauty"
    ;;
esac

# 2. Apollo API Call
curl -s -X POST "https://gateway.maton.ai/apollo/v1/people/search" \
  -H "Authorization: Bearer $MATON_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"person_titles\": $TITLES,
    \"person_locations\": $LOCATIONS,
    \"per_page\": 100,
    \"page\": 1
  }" > leads_raw.json

# 3. Pagination & Enrichment (Loop)
# ... (mehrere Calls bis Target Count erreicht)

# 4. Upload zu ClickUp als Attachment
# Update Custom Fields
```

### 2. Reply Sync Automation

**Script:** `scripts/apollo-reply-sync.sh`

```bash
#!/bin/bash
# Usage: ./apollo-reply-sync.sh
# Cron: */15 * * * *

MATON_KEY=${MATON_API_KEY}
CLICKUP_KEY=${CLICKUP_API_TOKEN}
REPLY_LIST_ID="901521519132"  # Reply Management

# 1. Letzte Check-Zeit laden
LAST_CHECK=$(cat .last_reply_check 2>/dev/null || echo "2026-01-01T00:00:00Z")

# 2. Neue Replies abrufen
curl -s -X GET "https://gateway.maton.ai/apollo/v1/emailer_messages/search?status=replied&updated_at[gte]=${LAST_CHECK}" \
  -H "Authorization: Bearer $MATON_KEY" | jq -r '.emailer_messages[] | select(.status == "replied")' > new_replies.json

# 3. Für jede Reply ClickUp Task erstellen
jq -c '.[]' new_replies.json | while read reply; do
  LEAD_NAME=$(echo $reply | jq -r '.contact_name')
  LEAD_EMAIL=$(echo $reply | jq -r '.contact_email')
  CAMPAIGN=$(echo $reply | jq -r '.campaign_name')
  SNIPPET=$(echo $reply | jq -r '.body' | head -c 200)
  
  # Reply Type klassifizieren
  if echo "$SNIPPET" | grep -qi "interested\|call\|meeting"; then
    TYPE="Interested"
    PRIORITY=2  # High
  elif echo "$SNIPPET" | grep -qi "how\|what\|?"; then
    TYPE="Question"
    PRIORITY=3  # Normal
  elif echo "$SNIPPET" | grep -qi "not interested\|no"; then
    TYPE="Not Interested"
    PRIORITY=4  # Low
  elif echo "$SNIPPET" | grep -qi "out of office\|vacation"; then
    TYPE="OOO"
    PRIORITY=4  # Low
  else
    TYPE="Other"
    PRIORITY=3
  fi
  
  # ClickUp Task erstellen
  curl -s -X POST "https://api.clickup.com/api/v2/list/${REPLY_LIST_ID}/task" \
    -H "Authorization: ${CLICKUP_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"📩 Reply: ${LEAD_NAME}\",
      \"description\": \"${SNIPPET}...\",
      \"priority\": ${PRIORITY},
      \"custom_fields\": [
        {\"name\": \"Lead Name\", \"value\": \"${LEAD_NAME}\"},
        {\"name\": \"Email\", \"value\": \"${LEAD_EMAIL}\"},
        {\"name\": \"Campaign\", \"value\": \"${CAMPAIGN}\"},
        {\"name\": \"Reply Type\", \"value\": \"${TYPE}\"},
        {\"name\": \"Reply Snippet\", \"value\": \"${SNIPPET}\"}
      ]
    }"
done

# 4. Aktuelle Zeit speichern
date -u +%Y-%m-%dT%H:%M:%SZ > .last_reply_check
```

### 3. Campaign Analytics Automation

**Script:** `scripts/apollo-campaign-analytics.sh`

```bash
#!/bin/bash
# Usage: ./apollo-campaign-analytics.sh
# Cron: 0 9 * * * (täglich 9 Uhr)

MATON_KEY=${MATON_API_KEY}
CLICKUP_KEY=${CLICKUP_API_TOKEN}
CAMPAIGNS_LIST_ID="901521519128"

# 1. Alle aktiven Campaigns aus ClickUp laden
curl -s "https://api.clickup.com/api/v2/list/${CAMPAIGNS_LIST_ID}/task?statuses%5B%5D=Active" \
  -H "Authorization: ${CLICKUP_KEY}" | jq -r '.tasks[] | {id: .id, name: .name, apollo_id: .custom_fields[] | select(.name=="Apollo Campaign ID").value}' > active_campaigns.json

# 2. Für jede Campaign Stats abrufen
jq -c '.[]' active_campaigns.json | while read campaign; do
  TASK_ID=$(echo $campaign | jq -r '.id')
  APOLLO_ID=$(echo $campaign | jq -r '.apollo_id')
  
  # Apollo Stats
  STATS=$(curl -s "https://gateway.maton.ai/apollo/v1/emailer_campaigns/${APOLLO_ID}/stats" \
    -H "Authorization: Bearer $MATON_KEY")
  
  SENT=$(echo $STATS | jq -r '.emails_sent')
  OPENED=$(echo $STATS | jq -r '.emails_opened')
  REPLIED=$(echo $STATS | jq -r '.emails_replied')
  
  # Berechnungen
  OPEN_RATE=$(echo "scale=2; ($OPENED / $SENT) * 100" | bc)
  REPLY_RATE=$(echo "scale=2; ($REPLIED / $SENT) * 100" | bc)
  
  # ClickUp updaten
  curl -s -X PUT "https://api.clickup.com/api/v2/task/${TASK_ID}" \
    -H "Authorization: ${CLICKUP_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"custom_fields\": [
        {\"name\": \"Reply Rate %\", \"value\": ${REPLY_RATE}},
        {\"name\": \"Open Rate %\", \"value\": ${OPEN_RATE}}
      ]
    }"
done
```

---

## 📊 REPORTING DASHBOARD

### Weekly Outbound Report

**Automatisch generiert (Montag 9 Uhr):**

```
📊 OUTBOUND REPORT - KW 9

CAMPAIGNS:
┌─────────────────────────────┬────────┬────────┬────────┬─────────┐
│ Campaign                    │ Sent   │ Open % │ Reply% │ Meetings│
├─────────────────────────────┼────────┼────────┼────────┼─────────┤
│ Fashion DACH - Case Study   │ 400    │ 52%    │ 4.2%   │ 2       │
│ Beauty DACH - Problem       │ 320    │ 48%    │ 3.1%   │ 1       │
│ Home & Living - Social Proof│ 280    │ 45%    │ 2.8%   │ 1       │
├─────────────────────────────┼────────┼────────┼────────┼─────────┤
│ TOTAL                       │ 1000   │ 48.3%  │ 3.4%   │ 4       │
└─────────────────────────────┴────────┴────────┴────────┴─────────┘

REPLIES:
┌──────────────────┬───────┐
│ Type             │ Count │
├──────────────────┼───────┤
│ Interested       │ 18    │
│ Question         │ 12    │
│ Not Interested   │ 8     │
│ OOO              │ 4     │
├──────────────────┼───────┤
│ TOTAL            │ 42    │
└──────────────────┴───────┘

INSIGHTS:
✅ Fashion DACH performt am besten (4.2% Reply Rate)
⚠️ Home & Living unter 3% → Sequence anpassen
💡 Mehr "Case Study" Angles testen

ACTION ITEMS:
- [ ] Fashion Sequence skalieren (+200 Leads)
- [ ] Home & Living Subject Lines A/B testen
- [ ] 4 Meetings vorbereiten
```

---

## 🚀 IMPLEMENTIERUNGS-PLAN

### Woche 1: Foundation

| Tag | Aufgabe | Zeit |
|-----|---------|------|
| Mo | Maton Apollo API testen (Credits checken) | 1h |
| Mo | Lead Search Script bauen | 4h |
| Di | Reply Sync Script bauen | 4h |
| Mi | Campaign Analytics Script bauen | 3h |
| Do | Testing & Bugfixing | 3h |
| Fr | Documentation & Handover | 2h |

### Woche 2: Optimierung

| Tag | Aufgabe |
|-----|---------|
| Mo | Erste Live-Searches |
| Di | Reply-Handling Workflow testen |
| Mi | Analytics Dashboard bauen |
| Do | Weekly Report Automation |
| Fr | Performance Review & Tweaks |

---

## ✅ CHECKLISTE

### Vorbereitung
- [ ] Maton API Key verifizieren
- [ ] Apollo API Key verifizieren
- [ ] Credits-Status checken (Apollo)
- [ ] Rate Limits dokumentieren

### Scripts
- [ ] `apollo-lead-search.sh`
- [ ] `lead-validation.sh`
- [ ] `campaign-setup.sh`
- [ ] `reply-sync.sh`
- [ ] `campaign-analytics.sh`
- [ ] `weekly-report.sh`

### ClickUp Integration
- [ ] Webhooks einrichten
- [ ] Custom Fields finalisieren
- [ ] Templates erstellen
- [ ] Views konfigurieren

### Testing
- [ ] Test-Search (50 Leads)
- [ ] Test-Enrichment (10 Leads)
- [ ] Test-Reply Sync
- [ ] Test-Analytics

### Documentation
- [ ] API Reference
- [ ] Troubleshooting Guide
- [ ] User Guide

---

**Nächster Schritt:** Vorbereitung checken & erste Scripts bauen
