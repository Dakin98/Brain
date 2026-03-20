# Newsletter Automation — Airtable Setup

> Diese Felder müssen in der "Kunden" Tabelle in Airtable manuell angelegt werden

---

## Erforderliche Felder

| Feldname | Feldtyp | Beschreibung | Beispiel |
|----------|---------|--------------|----------|
| **Newsletter Service** | Checkbox | Aktiviert wenn Kunde Newsletter-Service gebucht hat | ☑️ |
| **Newsletter Onboarding Done** | Checkbox | Wird automatisch gesetzt wenn Onboarding-Tasks erstellt wurden | ☑️ |
| **Klaviyo Account ID** | Single line text | Public API Key aus Klaviyo | `Xq8yQe` |
| **Klaviyo Private Key** | Single line text | Private API Key (verschlüsselt speichern!) | `pk_...` |
| **Klaviyo List ID** | Single line text | ID der Haupt-Liste für Campaigns | `ThKApp` |
| **Weekly Newsletter Day** | Single select | An welchem Tag der Newsletter versendet wird | `Mittwoch` |

---

## Optionale Felder (für Erweiterungen)

| Feldname | Feldtyp | Beschreibung |
|----------|---------|--------------|
| **Newsletter Package** | Single select | `Basic`, `Pro`, `Enterprise` |
| **Emails per Month** | Number | Wie viele Campaigns pro Monat |
| **Last Newsletter Date** | Date | Wann wurde der letzte Newsletter gesendet |
| **Newsletter Performance Score** | Rating | 1-5 Sterne Performance |

---

## Einrichtung Schritt-für-Schritt

### 1. Neue Felder anlegen

1. Öffne Airtable → adsdrop Hub → Kunden Tabelle
2. Klicke auf "+" neben dem letzten Feld
3. Füge die 6 erforderlichen Felder hinzu

### 2. Newsletter Service aktivieren

Für Kunden die Newsletter gebucht haben:

```
☑️ Newsletter Service = true
📧 Klaviyo Account ID = Xq8yQe
📧 Klaviyo List ID = ThKApp
📅 Weekly Newsletter Day = Mittwoch
```

### 3. Onboarding Prozess

Wenn `Newsletter Service = true` und `Newsletter Onboarding Done = false`:

→ Cronjob erstellt automatisch 5 Onboarding-Tasks in ClickUp

→ Nach Erstellung wird `Newsletter Onboarding Done = true` gesetzt

→ Wiederkehrende Tasks werden aktiviert

---

## Automation Flow

```
Neuer Kunde mit Newsletter Service
         ↓
Newsletter Service = ☑️
Newsletter Onboarding Done = ☐
         ↓
[Cron: Alle 10 Min]
         ↓
Erstelle 5 Onboarding Tasks:
  1. Kickoff & Zugänge (Due: +1 Tag)
  2. Account Setup (Due: +3 Tage)
  3. Flow-Strategie (Due: +7 Tage)
  4. Template Design (Due: +10 Tage)
  5. Erste Campaign (Due: +14 Tage)
         ↓
Setze Newsletter Onboarding Done = ☑️
         ↓
Wiederkehrende Tasks aktiviert:
  • Weekly Newsletter (Montag 9 Uhr)
  • Monthly Report (1. des Monats)
  • Flow Check (1. & 15.)
```

---

## Testen

### Manuelles Testen

```bash
# Onboarding Setup testen
export AIRTABLE_API_KEY="your_key"
export CLICKUP_API_TOKEN="your_token"
export TELEGRAM_BOT_TOKEN="your_bot_token"

./scripts/newsletter-onboarding-setup.sh
```

### Logs prüfen

```bash
# Real-time Log
tail -f ~/.openclaw/workspace/logs/newsletter-onboarding.log

# Weekly Log
tail -f ~/.openclaw/workspace/logs/newsletter-weekly.log
```

---

## Troubleshooting

### Problem: Keine Tasks werden erstellt

**Prüfen:**
1. Ist `AIRTABLE_API_KEY` gesetzt?
2. Ist `CLICKUP_API_TOKEN` korrekt?
3. Sind die Feldnamen in Airtable exakt wie dokumentiert?
4. Gibt es Kunden mit `Newsletter Service = true`?

### Problem: ClickUp API Error

**Prüfen:**
1. Ist der API Token gültig?
2. Hat der Token Zugriff auf die List ID?
3. Ist die List ID korrekt?

### Problem: Keine Telegram Notifications

**Prüfen:**
1. Ist `TELEGRAM_BOT_TOKEN` gesetzt?
2. Ist `TELEGRAM_CHAT_ID` korrekt?
3. Funktioniert der Bot? (Test mit curl)

---

## Scripts Übersicht

| Script | Zweck | Frequenz |
|--------|-------|----------|
| `newsletter-onboarding-setup.sh` | Onboarding-Tasks für neue Kunden | Alle 10 Min |
| `newsletter-weekly-task.sh` | Weekly Newsletter Tasks | Montag 9 Uhr |
| `newsletter-monthly-report.sh` | Monthly Reporting Tasks | 1. des Monats 9 Uhr |
| `newsletter-flow-check.sh` | Flow Performance Check | 1. & 15. 9 Uhr |

---

## Nächste Schritte

1. ✅ Airtable Felder anlegen
2. ✅ API Keys in `.env` oder Umgebungsvariablen setzen
3. ✅ Test mit einem Dummy-Kunden
4. ✅ Produktiv schalten
