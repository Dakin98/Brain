# 📊 Kunden Performance Report - Automation

**Stand:** 24. Februar 2026  
**Status:** Implementiert, bereit zum Testen

---

## Überblick

Automatisierter wöchentlicher Performance-Report für Paid Ads Kunden.

**Flow:** Airtable (Kunden) → Meta Ads API → Google Sheets → Email an Kunden

**Trigger:** Jeden Freitag um 17:00 Uhr (n8n Schedule)

---

## Architektur

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  n8n Cron    │────▶│  Airtable    │────▶│  Meta Ads    │
│  FR 17:00   │     │  Get Clients │     │  API Pull    │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                │
                    ┌──────────────┐     ┌──────▼───────┐
                    │  Email Send  │◀────│ Google Sheets│
                    │  HTML Report │     │ Update Tabs  │
                    └──────────────┘     └──────────────┘
                           │
                    ┌──────▼───────┐
                    │  ClickUp     │ (optional)
                    │  Creative    │
                    │  Status      │
                    └──────────────┘
```

---

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `scripts/weekly-report-extend.py` | Hauptscript: Meta Pull + Sheet Update + Email |
| `scripts/meta-ads-pull.py` | Basis-Script (unverändert, wird weiterhin genutzt) |
| `scripts/meta_reporting_pull.py` | Monatlicher Pull für Razeco (unverändert) |
| `scripts/meta-reporting-setup.sh` | Sheet-Setup bei Onboarding (unverändert) |
| `workflows/weekly-kunden-report.json` | n8n Workflow (Import in n8n.adsdrop.de) |
| `templates/weekly-report-email.html` | HTML Email-Template |

---

## Google Sheet Struktur

Jeder Kunde hat ein Sheet (erstellt bei Onboarding via `meta-reporting-setup.sh`).

### Bestehende Tabs (unverändert)
- **Campaigns** - Monatliche Campaign-Daten
- **Ad Sets** - Monatliche AdSet-Daten
- **Creatives** - Monatliche Creative-Daten

### Neue Tabs (weekly-report-extend.py)
- **Weekly Summary** - KPI-Übersicht, Budget Status, Highlights, Next Steps
- **Charts Data** - Tägliche Daten der letzten 7 Tage (Basis für Charts)
- **Campaign Performance** - Wöchentliche Campaign-Aufschlüsselung
- **Creative Overview** - Top Creatives + ClickUp Status (Winner/Testing/Loser)

### Charts (manuell einmalig erstellen)
In Google Sheets: Insert → Chart, basierend auf "Charts Data" Tab:

1. **Spend over Time** - Liniendiagramm: Spalte A (Datum) vs B (Spend)
2. **ROAS over Time** - Liniendiagramm: Spalte A vs H (ROAS)
3. **CTR over Time** - Liniendiagramm: Spalte A vs E (CTR)
4. **Clicks & Impressions** - Kombi-Chart: A vs C+D

> Charts aktualisieren sich automatisch wenn die Daten im Tab aktualisiert werden.

---

## Verwendung

### Manuell (CLI)

```bash
# Für einen einzelnen Kunden
python3 scripts/weekly-report-extend.py \
  --sheet-id 1XTMtZwPRQVR7pRZv2ZZQC_pC5_61JIhkclOsCn1uESA \
  --account-id 1538907656986107 \
  --client-name "Razeco UG" \
  --weekly-budget 500

# Für alle Kunden aus Airtable
python3 scripts/weekly-report-extend.py --all-clients

# Mit Email-Versand
python3 scripts/weekly-report-extend.py --all-clients --send-email

# Einzelkunde mit Email
python3 scripts/weekly-report-extend.py \
  --sheet-id XXXXX \
  --account-id 123456 \
  --client-name "Kunde" \
  --send-email --to kunde@example.com
```

### Automatisch (n8n)

1. Import `workflows/weekly-kunden-report.json` in n8n.adsdrop.de
2. Credentials konfigurieren:
   - **Airtable API Key** (HTTP Header Auth: `Authorization: Bearer pat...`)
   - **Meta Ads Token** (HTTP Query Auth: `access_token=EAA...`)
   - **Google Sheets OAuth2** (Service Account oder OAuth)
   - **SMTP** (für Email-Versand)
3. Workflow aktivieren → läuft jeden Freitag 17:00

---

## Datenquellen

### Airtable (appbGhxy9I18oIS8E / Kunden)
- `Meta Ad Account ID` → Account für API Pull
- `AP E-Mail` → Email-Empfänger für Report
- `Reporting Sheet` → Google Sheet URL
- `Firmenname` → Kundenname im Report
- `Wochenbudget` → Für Budget vs Spend Tracking

### Meta Ads API (v21.0)
- **Account Insights** (daily): Spend, Impressions, Clicks, CTR, CPC, CPM, ROAS, Purchases, Revenue
- **Campaign Insights**: Pro Campaign aggregiert
- **Ad Insights**: Pro Creative, inkl. Video Metrics (Hook Rate, Hold Rate)

### ClickUp (optional)
- **Space:** Delivery
- **Folder:** {Kundenname}
- **Lists:** Creative Pipeline → Task Status wird gemappt:
  - Active/Scaling → **Winner**
  - Testing/Review/Ready → **Testing**
  - Paused/Dead/Killed → **Loser**
- **Next Steps:** Tasks mit Due Date in den nächsten 7 Tagen

---

## Email

### Betreff
`Weekly Performance Report - {Kundenname} - KW{XX}`

### Inhalt
- KPI-Übersicht (Spend, ROAS, CTR, Conversions, CPC, Cost/Conv.)
- Top 5 Campaigns (Tabelle)
- Creative Overview mit Status-Badges
- Budget Status
- Next Steps aus ClickUp
- CTA-Button zum Google Sheet

### Versand
- Via `gog gmail send` (CLI) oder n8n SMTP Node
- Fallback: HTML wird als Datei gespeichert unter `/tmp/weekly-report-{kunde}-kw{XX}.html`

---

## Setup für neuen Kunden

1. **Airtable:** Felder ausfüllen (Meta Ad Account ID, AP E-Mail, Wochenbudget)
2. **Onboarding:** `meta-reporting-setup.sh` erstellt das Google Sheet automatisch
3. **Sheet URL** wird in Airtable gespeichert (Feld: Reporting Sheet)
4. **Charts** einmalig manuell im Sheet erstellen (siehe oben)
5. **Fertig** – Weekly Report läuft automatisch via n8n

---

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| Meta Token abgelaufen | Neuen Token in `.env` (META_ACCESS_TOKEN) setzen |
| Sheet nicht gefunden | Prüfe `Reporting Sheet` URL in Airtable |
| Keine Daten | Account ID prüfen, `act_` Prefix wird automatisch gehandhabt |
| Email kommt nicht an | SMTP Credentials in n8n prüfen, oder manuell via CLI senden |
| ClickUp leer | CLICKUP_TOKEN setzen, Space/Folder-Struktur prüfen |

---

## TODO / Nächste Schritte

- [ ] Charts in Google Sheets automatisch erstellen (via Sheets API batchUpdate / addChart)
- [ ] PDF Export als Email-Anhang (via `gog sheets export --format pdf`)
- [ ] Vorwoche-Vergleich (WoW Change) in KPIs
- [ ] ClickUp Token in .env einrichten
- [ ] Test-Run mit Razeco (echte Daten)
