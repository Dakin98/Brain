# 🚀 ClickUp → Apollo Auto-Sync Workflow

## Vollautomatisierter Campaign-Launch

**Workflow:** Leads importieren → ClickUp Campaign planen → Status "Active" → Apollo Campaign automatisch erstellen

---

## 🎯 ÜBERSICHT

### Was passiert automatisch?

```
You in ClickUp:
├── 1. Leads importieren (Script)
├── 2. Leads qualifizieren (Status: Ready)
├── 3. Campaign Task erstellen
├── 4. Status → "Active"
└── 5. 🔄 AUTO: Apollo Campaign wird erstellt!
```

**Automatisch:**
- ✅ Leads aus ClickUp exportiert
- ✅ Apollo Sequence erstellt
- ✅ Leads in Apollo importiert
- ✅ Apollo Campaign gestartet
- ✅ ClickUp mit Apollo ID aktualisiert

---

## 📋 SCHRITT-FÜR-SCHRITT

### Phase 1: Leads Importieren (10 Min)

#### Schritt 1.1: Lead List erstellen

**ClickUp:**
- Growth Space → 🚀 Outbound Engine → 👥 Lead Lists
- + Add Task

**Ausfüllen:**
```
Task Name: 🎯 Fashion DACH - März 2024
List Name: Fashion DACH Q1
ICP: Fashion DACH
Source: Apollo
```

**Task ID kopieren** (z.B. `86c8e72xj`)

#### Schritt 1.2: Import starten

```bash
cd ~/.openclaw/workspace/scripts
./apollo-lead-import.sh "86c8e72xj" "Fashion DACH" 500
```

**Was passiert:**
- Script sucht 500 Leads in Apollo
- Erstellt Folder: "📂 Fashion DACH - 24.02.2024"
- Jeder Lead = eigener Task mit Custom Fields
- Dauer: ~5-10 Minuten

#### Schritt 1.3: Emails anreichern

```bash
./apollo-enrich-leads.sh 901521519130 100
```

**Was passiert:**
- Holt Emails für "available" Leads
- Updated Email Status → "enriched"

---

### Phase 2: Leads Qualifizieren (30 Min)

#### Schritt 2.1: Leads reviewen

**In ClickUp:**
- Öffne Folder: "📂 Fashion DACH - 24.02.2024"
- Gehe durch jeden Lead (oder filtere)

#### Schritt 2.2: Qualifizieren

**Pro Lead:**
1. **LinkedIn öffnen** (Custom Field: LinkedIn URL)
2. **Profil prüfen:**
   - Aktiv im E-Commerce?
   - Passende Firmengröße?
   - Richtige Branche?
3. **Status setzen:**
   - ✅ Gut → Lead Status = "Ready"
   - ❌ Schlecht → Lead Status = "Bounce"
   - 🤔 Unsicher → Notizen hinzufügen

**Tip:** Nutze Board View mit Spalten nach Status!

#### Schritt 2.3: Ergebnis

**Filter:** `Lead Status` = `Ready`

Sollte zeigen: ~350-400 Ready Leads

---

### Phase 3: Campaign Planen (5 Min)

#### Schritt 3.1: Campaign Task erstellen

**ClickUp:**
- Growth Space → 🚀 Outbound Engine → 📊 Campaigns
- + Add Task

**Ausfüllen:**
```
Task Name: Fashion DACH - Case Study - März
Campaign Name: Fashion DACH - Case Study - März
ICP Segment: Fashion DACH
Sequence: Case Study Angle (oder später einfügen)
Lead Count: 350 (oder wie viele Ready)
Daily Send Limit: 40
Launch Date: [heute + 1 Tag]
Campaign Status: Draft ← Wichtig!
```

#### Schritt 3.2: Sequence hinzufügen

**In Task Description:**
```markdown
## Sequence

### Step 1 (Day 0)
Subject: {{company}} + Meta Ads Question
Body: [Email Text]

### Step 2 (Day 3)
Subject: Re: {{company}} + Meta Ads Question  
Body: [Email Text]

... (weitere Steps)
```

**Oder:** Link zu Sequence Task

#### Schritt 3.3: Task ID kopieren

Z.B.: `901600000002`

---

### Phase 4: AUTO-SYNC nach "Active" (1 Min)

#### Schritt 4.1: Status auf "Active" setzen

**In ClickUp:**
- Campaign Task öffnen
- Custom Field: `Campaign Status` → `Active`
- Speichern

#### Schritt 4.2: Sync Script ausführen

```bash
./campaign-apollo-sync.sh "901600000002"
```

**Was passiert automatisch:**

```
🚀 ClickUp → Apollo Campaign Sync

📡 Step 1: Fetching campaign from ClickUp...
   Campaign: Fashion DACH - Case Study - März
   ICP: Fashion DACH
   Daily Limit: 40
   Target Leads: 350

📡 Step 2: Fetching leads from ClickUp...
   Found 350 leads with emails

📡 Step 3: Getting sequence template...
   Sequence: 5 steps

📡 Step 4: Creating Apollo sequence...
   ✅ Sequence created: seq_12345

📡 Step 5: Importing leads to Apollo...
   Status: success
   Imported: 350 contacts

📡 Step 6: Creating Apollo campaign...
   ✅ Apollo campaign created: camp_67890

📡 Step 7: Updating ClickUp...
   ✅ ClickUp updated with Apollo Campaign ID

🎉 SYNC COMPLETE!

Campaign is now LIVE in Apollo:
   Apollo Campaign ID: camp_67890
   Leads imported: 350
   Daily limit: 40

Links:
   ClickUp: https://app.clickup.com/t/901600000002
   Apollo: https://app.apollo.io/#/campaigns/camp_67890
```

---

## ✅ ERGEBNIS

### In ClickUp:
- Campaign Status: `Active` ✅
- Apollo Campaign ID: `camp_67890` ✅
- Launch Date: Heute ✅

### In Apollo:
- Sequence erstellt ✅
- 350 Leads importiert ✅
- Campaign läuft ✅
- 40 Emails/Tag werden versendet ✅

---

## 🤖 AUTOMATISIERUNG (Optional)

### Variante A: Manuelles Script (aktuell)
```bash
# Nach Status-Änderung auf "Active"
./campaign-apollo-sync.sh "[TASK_ID]"
```

### Variante B: Webhook Automation (empfohlen)

**Setup für echte Automatisierung:**

1. **n8n oder Make.com** einrichten
2. **ClickUp Trigger:** Wenn Campaign Status = "Active"
3. **HTTP Request:** Script aufrufen oder direkt APIs callen

**n8n Workflow:**
```
ClickUp Webhook (Campaign Status = Active)
    ↓
HTTP Request → campaign-apollo-sync.sh
    ↓
Slack Notification: "Campaign launched!"
```

### Variante C: Cron-Check (einfach)

```bash
# Cronjob: Alle 5 Min prüfen
*/5 * * * * cd ~/.openclaw/workspace/scripts && ./campaign-auto-launch.sh
```

**Script `campaign-auto-launch.sh`:**
```bash
#!/bin/bash
# Checks for campaigns with status "Draft" and launch_date = today
# Auto-launches them

CAMPAIGNS=$(curl -s "https://api.clickup.com/api/v2/list/901521519128/task?statuses%5B%5D=Draft" \
    -H "Authorization: $CLICKUP_API_TOKEN")

# Filter campaigns with launch_date = today
# ... (logic here)

# For each campaign:
./campaign-apollo-sync.sh "$TASK_ID"
```

---

## 📊 POST-LAUNCH MONITORING

### Täglich (9 Uhr):

```bash
# Check campaign performance
./campaign-analytics.sh
```

**Was wird aktualisiert:**
- ClickUp: Reply Rate %
- ClickUp: Meeting Rate %

### Wöchentlich (Montag):

```bash
# Generate report
./weekly-outbound-report.sh
```

**Report enthält:**
- Alle Campaigns Performance
- Reply-Statistiken
- Action Items

---

## 🛠️ TROUBLESHOOTING

### "No leads found with Ready status"

**Problem:** Leads haben nicht "Ready" Status

**Lösung:**
```bash
# Leads qualifizieren
# In ClickUp: Lead Status → Ready
```

### "No leads found with emails"

**Problem:** Emails nicht angereichert

**Lösung:**
```bash
./apollo-enrich-leads.sh 901521519130 100
```

### Apollo API Error

**Problem:** Apollo API Limits oder Enterprise-Features

**Lösung:**
- Script zeigt dann "MANUAL SETUP REQUIRED"
- Leads werden exportiert nach `/tmp/apollo_leads_[ID].json`
- Manuelles Import in Apollo UI

---

## 🎯 BEFEHLE REFERENZ

### Kompletter Workflow

```bash
# 1. Ins Script-Verzeichnis
cd ~/.openclaw/workspace/scripts

# 2. Leads importieren
./apollo-lead-import.sh "[LEAD_LIST_TASK_ID]" "[ICP]" [COUNT]

# 3. Emails anreichern
./apollo-enrich-leads.sh [LIST_ID] [LIMIT]

# 4. (In ClickUp: Leads qualifizieren → Status: Ready)

# 5. Campaign auf "Active" setzen (in ClickUp)

# 6. Auto-Sync ausführen
./campaign-apollo-sync.sh "[CAMPAIGN_TASK_ID]"

# 7. Monitoring (täglich)
./campaign-analytics.sh

# 8. Weekly Report (montags)
./weekly-outbound-report.sh
```

---

## 🚀 SCHNELLSTART

**Teste den Workflow mit 10 Leads:**

```bash
# 1. Lead List Task erstellen in ClickUp
# 2. Task ID kopieren

# 3. 10 Leads importieren
./apollo-lead-import.sh "[YOUR_TASK_ID]" "Fashion DACH" 10

# 4. In ClickUp: Leads auf "Ready" setzen

# 5. Campaign Task erstellen (Status: Draft)
# 6. Campaign Task ID kopieren

# 7. Auf "Active" setzen (in ClickUp)

# 8. Sync ausführen
./campaign-apollo-sync.sh "[CAMPAIGN_TASK_ID]"
```

**Dauer:** ~15 Minuten für ersten Test

---

**Bereit für deinen ersten Auto-Sync?** 🚀

Erstelle eine Lead List + Campaign und teste das System!
