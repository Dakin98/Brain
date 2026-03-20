# Newsletter/Klaviyo Kunden Automatisierung — Konzept

> Automatische Task-Erstellung und wiederkehrende Prozesse für Email Marketing Kunden

---

## Übersicht

| Komponente | Zweck | Frequenz |
|------------|-------|----------|
| **Onboarding Auto-Setup** | Erstellt Initial-Tasks bei neuem Klaviyo-Kunden | Einmalig (bei Status "Active") |
| **Weekly Newsletter Task** | Erstellt wöchentlichen Newsletter-Task | Jeden Montag 9 Uhr |
| **Monthly Reporting Task** | Erstellt monatlichen Reporting-Task | 1. des Monats |
| **Flow Check Task** | Prüft Flow-Performance | 1. & 15. des Monats |
| **List Hygiene Task** | Erinnert an Listen-Bereinigung | Monatlich (letzter Freitag) |

---

## Airtable Struktur

### Neue Felder in Kunden-Tabelle

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `Klaviyo Account ID` | Text | Klaviyo Public API Key |
| `Klaviyo Private Key` | Text | Private API Key (verschlüsselt) |
| `Klaviyo List ID` | Text | Haupt-Liste für Campaigns |
| `Newsletter Service` | Checkbox | Aktiv wenn Newsletter-Service gebucht |
| `Newsletter Onboarding Done` | Checkbox | Tasks wurden erstellt |
| `Weekly Newsletter Day` | Single Select | Montag/Dienstag/Mittwoch |
| `Newsletter ClickUp List ID` | Text | Wo Tasks erstellt werden |

---

## 1. Onboarding Auto-Setup

### Trigger
- Cron: Alle 10 Minuten
- Bedingung: `Newsletter Service = true` AND `Newsletter Onboarding Done = false`

### Erstellte Tasks

#### Task 1: 📧 Kickoff & Zugänge (Due: +1 Tag)
- Klaviyo Account Zugang sichern
- Brand Assets sammeln
- Shopify Integration prüfen

#### Task 2: 🔧 Account Setup (Due: +3 Tage)
- Sending Domain einrichten
- Segmente erstellen
- Pop-ups konfigurieren

#### Task 3: 🔄 Flow-Setup (Due: +7 Tage)
- Welcome Flow
- Abandoned Cart
- Browse Abandonment
- Post-Purchase

#### Task 4: 🎨 Template Design (Due: +10 Tage)
- Brand Kit
- Master Template
- Newsletter Template

#### Task 5: 🚀 Erste Campaign (Due: +14 Tage)
- Welcome Email senden
- Erste Newsletter planen

### Danach
- `Newsletter Onboarding Done = true` setzen
- Wiederkehrende Tasks aktivieren

---

## 2. Wiederkehrende Tasks

### Weekly Newsletter Task (Montag 9 Uhr)

**Für jeden aktiven Newsletter-Kunden:**

```
Name: 📧 [KUNDE] Newsletter KW{XX}
Due: Diese Woche (z.B. Mittwoch)
Checklist:
  □ Thema festlegen (Content-Kalender prüfen)
  □ Copy schreiben
  □ Bilder vorbereiten
  □ Template anpassen
  □ Test-E-Mail senden
  □ Kunden-Approval einholen
  □ Newsletter versenden
  □ Performance nach 48h checken
```

### Monthly Reporting Task (1. des Monats)

```
Name: 📊 [KUNDE] Monthly Report {Monat}
Due: +5 Tage
Checklist:
  □ KPIs exportieren (Open Rate, CTR, Revenue)
  □ Flow Performance analysieren
  □ Benchmarks vergleichen
  □ Top/Worst Campaigns identifizieren
  □ Optimierungs-Ideen sammeln
  □ Report für Kunden erstellen
  □ Kunden-Call vorbereiten
```

### Flow Check Task (1. & 15.)

```
Name: 🔄 [KUNDE] Flow Performance Check
Due: +3 Tage
Checklist:
  □ Welcome Flow Metrics checken
  □ Abandoned Cart Performance
  □ Browse Abandonment Rates
  □ Post-Purchase Revenue
  □ A/B Test Ergebnisse prüfen
  □ Underperforming Flows optimieren
```

### List Hygiene Task (letzter Freitag)

```
Name: 🧹 [KUNDE] List Hygiene
Due: +2 Tage
Checklist:
  □ Bounces bereinigen
  □ Unsubscribes prüfen
  □ Inaktive Segmente aktualisieren
  □ List Growth Rate checken
  □ Deliverability Metrics prüfen
```

---

## 3. Cron-Jobs

### Cron 1: Newsletter Onboarding Setup
```json
{
  "id": "newsletter-onboarding-setup",
  "schedule": "*/10 * * * *",
  "task": "Prüfe neue Newsletter-Kunden → Erstelle Onboarding-Tasks",
  "script": "scripts/newsletter-onboarding-setup.sh"
}
```

### Cron 2: Weekly Newsletter Task
```json
{
  "id": "newsletter-weekly-task",
  "schedule": "0 9 * * 1",
  "task": "Erstelle wöchentliche Newsletter-Tasks",
  "script": "scripts/newsletter-weekly-task.sh"
}
```

### Cron 3: Monthly Reporting Task
```json
{
  "id": "newsletter-monthly-report",
  "schedule": "0 9 1 * *",
  "task": "Erstelle monatliche Reporting-Tasks",
  "script": "scripts/newsletter-monthly-report.sh"
}
```

### Cron 4: Flow Check Task
```json
{
  "id": "newsletter-flow-check",
  "schedule": "0 9 1,15 * *",
  "task": "Erstelle Flow-Check-Tasks",
  "script": "scripts/newsletter-flow-check.sh"
}
```

---

## 4. Scripts

### newsletter-onboarding-setup.sh
```bash
#!/bin/bash
# 1. Lade Kunden aus Airtable (Newsletter Service = true, Onboarding Done = false)
# 2. Für jeden Kunde:
#    - Erstelle 5 Onboarding-Tasks in ClickUp
#    - Setze Newsletter Onboarding Done = true
#    - Sende Slack/Telegram Notification
```

### newsletter-weekly-task.sh
```bash
#!/bin/bash
# 1. Lade aktive Newsletter-Kunden
# 2. Berechne aktuelle Kalenderwoche
# 3. Für jeden Kunde:
#    - Erstelle "Newsletter KW{XX}" Task
#    - Füge Checklist Items hinzu
#    - Setze Due Date (Mittwoch oder konfigurierter Tag)
```

---

## 5. ClickUp Integration

### ClickUp API Calls

#### Task erstellen
```bash
curl -X POST "https://api.clickup.com/api/v2/list/{LIST_ID}/task" \
  -H "Authorization: pk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "📧 [KUNDE] Newsletter KW12",
    "description": "Wöchentlicher Newsletter für [KUNDE]",
    "due_date": 1772006400000,
    "assignees": [USER_ID],
    "tags": ["newsletter", "weekly", "klaviyo"],
    "checklists": [...]
  }'
```

#### Checklist Items hinzufügen
```bash
curl -X POST "https://api.clickup.com/api/v2/checklist/{CHECKLIST_ID}/checklist_item" \
  -H "Authorization: pk_..." \
  -d '{"name": "Thema festlegen"}'
```

---

## 6. Notification Templates

### Slack/Telegram: Neue Tasks erstellt
```
🎯 Neue Newsletter-Tasks erstellt!

Kunde: [KUNDE]
Typ: Weekly Newsletter KW12
Due: Mittwoch, 26. Feb
Tasks: 1
Checklist Items: 11

👉 In ClickUp öffnen
```

### Slack/Telegram: Onboarding abgeschlossen
```
✅ Newsletter Onboarding abgeschlossen!

Kunde: [KUNDE]
Status: Active
Wiederkehrende Tasks: Aktiviert

Nächste Tasks:
• Newsletter KW12 (Mittwoch)
• Monthly Report März (1.3.)
```

---

## 7. Implementierungs-Schritte

1. **Airtable Felder erstellen** (5 Min)
2. **ClickUp List ID** für Newsletter-Kunden ermitteln (2 Min)
3. **Scripts erstellen** (30 Min)
4. **Cron-Jobs einrichten** (10 Min)
5. **Test mit Dummy-Kunde** (15 Min)

---

## Vergleich: Paid Ads vs Newsletter

| Feature | Paid Ads | Newsletter |
|---------|----------|------------|
| **Onboarding** | Google Sheet + Scripts | ClickUp Tasks + Checklists |
| **Wiederkehrend** | Monthly Update (Daten) | Weekly Tasks + Monthly Report |
| **Datenquelle** | Meta API | Klaviyo API |
| **Output** | Google Sheet | ClickUp Tasks |
| **Frequenz** | Monatlich | Wöchentlich + Monatlich |

---

Soll ich jetzt die Scripts erstellen und die Cron-Jobs einrichten?