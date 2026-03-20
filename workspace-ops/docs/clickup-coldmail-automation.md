# ClickUp Cold Mail Automatisierung

Erstellt automatisch Cold Mail Listen + Tasks für neue Kunden beim Onboarding.

## Übersicht

```
Airtable (neuer Kunde + Cold Mail = true)
    ↓
Cron/n8n triggert Script
    ↓
ClickUp: Folder + Liste + 6 Tasks mit Checklisten
```

## Setup

### 1. Credentials prüfen

```bash
# ClickUp API Token
cat ~/.config/clickup/api_token

# Airtable API Key
cat ~/.config/airtable/api_key
```

### 2. Manuelles Testen

```bash
# Dry Run (nichts wird erstellt)
python3 scripts/clickup-coldmail-setup.py "Musterfirma GmbH" --dry-run

# Echten Kunden erstellen
python3 scripts/clickup-coldmail-setup.py "Musterfirma GmbH"
```

### 3. Airtable Integration testen

```bash
# Prüft alle Kunden mit Cold Mail Service
./scripts/clickup-coldmail-onboarding.sh
```

## Airtable Schema

Für die Automatisierung brauchst du in der **Kunden** Tabelle:

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `Kunde` | Text | Firmenname |
| `Status` | Single Select | Prospect → Onboarding → Active |
| `Cold Mail` | Checkbox | Service aktiviert? |
| `ClickUp Folder Created` | Checkbox | Wurde Folder bereits erstellt? |

## n8n Workflow

### Option 1: Airtable Webhook (empfohlen)

1. **Airtable Automation** erstellen:
   - Trigger: When record matches condition
   - Condition: `Status` = "Active" AND `Cold Mail` = true
   - Action: Send webhook to n8n

2. **n8n Workflow**:
   - Webhook node (POST)
   - Execute Command node:
     ```bash
     python3 /Users/denizakin/.openclaw/workspace/scripts/clickup-coldmail-setup.py "{{$json.body.client_name}}"
     ```
   - Airtable node: Update record → `ClickUp Folder Created` = true

### Option 2: Cron-basiert (alle 10 Min)

```bash
# Cronjob einrichten
*/10 * * * * /Users/denizakin/.openclaw/workspace/scripts/clickup-coldmail-onboarding.sh >> /var/log/clickup-automation.log 2>&1
```

## Template Tasks

Die 6 Tasks werden aus dem **Process Hub** kopiert:

1. 🌐 Domain & Inbox Setup (13 Checklist-Items)
2. 🔍 Lead List Preparation (12 Checklist-Items)
3. ✍️ Sequenz & Copy Writing (14 Checklist-Items)
4. 🚀 Campaign Launch in Instantly (11 Checklist-Items)
5. 💬 Reply Management Setup (11 Checklist-Items)
6. 📈 Weekly Optimization (14 Checklist-Items)

**Gesamt: 75 Checklist-Items**

## Was wird erstellt?

```
Delivery Space
└── 📁 [Kundenname] (Folder)
    └── 📋 Cold Mail (Liste)
        ├── 🌐 Domain & Inbox Setup
        ├── 🔍 Lead List Preparation
        ├── ✍️ Sequenz & Copy Writing
        ├── 🚀 Campaign Launch in Instantly
        ├── 💬 Reply Management Setup
        └── 📈 Weekly Optimization
```

## Troubleshooting

### "Folder already exists"
- Das Script versucht den Folder zu erstellen
- Wenn er existiert, bricht es ab
- TODO: Existierenden Folder wiederverwenden

### Checklisten werden nicht kopiert
- Prüfe ob Template-Tasks Checklisten haben
- API Token braucht ausreichende Permissions

### Airtable Connection failed
- API Key prüfen: `cat ~/.config/airtable/api_key`
- Base ID prüfen: `appbGhxy9I18oIS8E`
- Table Name: "Kunden" (nicht "Kunden View")

## Erweiterungen

### Andere Services

Für Paid Ads, Email Marketing, etc.:

```python
# In clickup-coldmail-setup.py
SERVICE_TEMPLATES = {
    "cold_mail": ["86c8bd11p", "86c8bd14a", ...],
    "paid_ads": ["...", "..."],
    "email_marketing": ["...", "..."],
}
```

### Mehrere Listen pro Kunde

```python
def setup_full_client(client, space_id, client_name, services):
    for service in services:
        if service == "cold_mail":
            setup_cold_mail_for_client(client, space_id, client_name)
        elif service == "paid_ads":
            setup_paid_ads_for_client(client, space_id, client_name)
```
