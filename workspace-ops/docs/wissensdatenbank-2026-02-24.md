# 📚 Wissensdatenbank - Agentur Automatisierung

**Stand:** 24. Februar 2026, 11:30 Uhr  
**Zusammengestellt aus:** Alle Docs, Scripts, MEMORY.md und aktuellen Implementierungen

---

## 🎯 ARCHITEKTUR - Big Picture

### Gesamtsystem
```
┌─────────────────────────────────────────────────────────────┐
│                     AIRTABLE (Zentrale)                      │
│  • Kunden-Stammdaten                                         │
│  • Services (Cold Mail, Email Marketing, Paid Ads, etc.)    │
│  • Status-Tracking (Onboarding → Active)                     │
│  • API Keys & Zugangsdaten                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    AUTOMATISIERUNGS-LAYER                    │
│  Cronjobs (Montag 9:00 Uhr):                                 │
│  • clickup-services-cron.sh → Onboarding-Tasks              │
│  • notion-weekly-newsletters.sh → Newsletter-Campaigns      │
│  • newsletter-weekly-task.sh → ClickUp Review-Tasks         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────┬──────────────────┬────────────────────┐
│      CLICKUP        │     KLAVIYO      │      NOTION        │
│  • Task Management  │  • Campaigns     │  • Content Plan    │
│  • SOPs & Checklist │  • Templates     │  • 177 Themes      │
│  • Project Folders  │  • Segmente      │  • Email Calendar  │
└─────────────────────┴──────────────────┴────────────────────┘
```

---

## ✅ AKTIVE AUTOMATISIERUNGEN (Live)

### 1. ClickUp Onboarding (Montag 9:00 Uhr)

**Script:** `scripts/clickup-services-cron.sh`

| Service | Tasks | Airtable-Trigger | Status-Feld |
|---------|-------|------------------|-------------|
| 📨 **Cold Mail** | 6 Tasks (75 Items) | `Cold Mail = true` | `ClickUp Folder Created` |
| 📧 **Email Marketing** | 7 Tasks | `Email Marketing = true` | `ClickUp Email Marketing Created` |
| 🎯 **Paid Ads** | 15 Tasks + 5 Listen + 3 Custom Fields | `Paid Ads = true` | `ClickUp Paid Ads Created` |

**Was passiert:**
1. Prüft alle Kunden mit `Status = Aktiv`
2. Für jeden aktivierten Service → erstellt ClickUp Struktur
3. Markiert in Airtable als erledigt (Checkbox)
4. Nächster Lauf: Montag, 3. März 2026

**ClickUp Struktur pro Kunde:**
```
Delivery Space
├── 📁 [Kundenname]
│   ├── 📋 Cold Mail (6 Tasks)
│   ├── 📋 Email Marketing (7 Tasks)
│   ├── 📋 Project Management (15 Paid Ads Tasks)
│   ├── 📋 Creative Pipeline
│   ├── 📋 Archive
│   ├── 📋 Learnings
│   └── 📋 Creator Pool
```

---

### 2. Newsletter Automation (Montag 9:00 & 9:15 Uhr)

**Komponenten:**

| Komponente | Funktion | Zeit |
|------------|----------|------|
| `notion-weekly-newsletters.sh` | Notion → Klaviyo Campaign | 9:00 Uhr |
| `newsletter-weekly-task.sh` | ClickUp Task erstellen | 9:15 Uhr |

**Workflow:**
```
Notion (eCom Email Calendar KW10)
  ↓
Airtable (Razeco Brand Assets, API Key)
  ↓
HTML Template erstellen (Razeco Branding)
  ↓
Klaviyo Template upload
  ↓
Klaviyo Campaign erstellen (DRAFT)
  ↓
ClickUp Task mit Checklist
```

**Wichtig:** Campaigns sind DRAFT → müssen manuell in Klaviyo gescheduled werden

**Letzte Campaign:**
- Name: "Razeco | Internationaler Frauentag | 2026-03-08"
- Sende-Datum: 08.03.2026
- Status: DRAFT (wartet auf Schedule)

---

## 📋 AIRTABLE SCHEMA (Vollständig)

### Kunden-Tabelle (Pflichtfelder)

| Feld | Typ | Zweck |
|------|-----|-------|
| `Firmenname` | Text | Kunden-Name |
| `Status` | Single Select | Prospect → Onboarding → Aktiv |
| `Cold Mail` | Checkbox | Service aktivieren |
| `Email Marketing` | Checkbox | Service aktivieren |
| `Paid Ads` | Checkbox | Service aktivieren |
| `Newsletter Service` | Checkbox | Service aktivieren |
| `ClickUp Folder Created` | Checkbox | Cold Mail erledigt |
| `ClickUp Email Marketing Created` | Checkbox | Email erledigt |
| `ClickUp Paid Ads Created` | Checkbox | Paid Ads erledigt |
| `Newsletter Onboarding Done` | Checkbox | Newsletter erledigt |
| `Klaviyo API Key` | Text | Für Newsletter |
| `Klaviyo Newsletter List ID` | Text | Für Newsletter |
| `Meta BM ID` | Text | Für Paid Ads |
| `Meta Ad Account ID` | Text | Für Paid Ads |
| `Meta Pixel ID` | Text | Für Paid Ads |

---

## 🛠️ SCRIPTS & TOOLS

### Onboarding Scripts

| Script | Zweck | Usage |
|--------|-------|-------|
| `clickup-coldmail-setup.py` | 6 Cold Mail Tasks | `python3 script.py "Kunde"` |
| `clickup-emailmarketing-setup.py` | 7 Email Tasks | `python3 script.py "Kunde"` |
| `paid_ads_onboarding.py` | 15 Tasks + 5 Listen | `python3 script.py --name "Kunde"` |
| `clickup-services-cron.sh` | Alle Services (Cron) | Auto (Montag 9:00) |

### Newsletter Scripts

| Script | Zweck | Usage |
|--------|-------|-------|
| `newsletter_automation_v3.py` | Klaviyo Campaign erstellen | Auto (Montag 9:00) |
| `newsletter-weekly-task.sh` | ClickUp Task erstellen | Auto (Montag 9:15) |
| `newsletter-monthly-report.sh` | Monthly Report Task | Auto (1. des Monats) |
| `newsletter-flow-check.sh` | Flow-Überprüfung | Auto (1. & 15.) |

### Utility Scripts

| Script | Zweck |
|--------|-------|
| `check-airtable-fields.sh` | Prüft Airtable Schema |
| `meta-ads-pull.py` | Meta Ads Reporting |
| `meta-reporting-setup.sh` | Meta Reporting Setup |

---

## 📁 DATEISTRUKTUR

### Wichtige Verzeichnisse

```
~/.openclaw/workspace/
├── docs/                           # Dokumentation
│   ├── automation-status.md        # Status-Übersicht
│   ├── clickup-coldmail-automation.md
│   ├── newsletter-automation-final.md
│   └── clickup-konzept-adsdrop.md  # Ursprüngliches Konzept
├── scripts/                        # Automation Scripts
│   ├── clickup-services-cron.sh    # Haupt-Cronjob
│   ├── clickup-*-setup.py          # Setup-Scripts
│   ├── newsletter-*.sh             # Newsletter Scripts
│   └── paid_ads_onboarding.py      # Paid Ads Setup
├── logs/                           # Logs
│   ├── clickup-services-cron.log
│   └── newsletter-*.log
└── MEMORY.md                       # Langzeit-Gedächtnis
```

---

## 🔄 WORKFLOWS - Detailliert

### Workflow 1: Neuer Kunde Onboarding

```
1. Kunde unterschreibt Vertrag
   ↓
2. Manuelle Eingabe in Airtable:
   - Firmenname
   - Status = "Aktiv"
   - Services aktivieren (Checkboxen)
   ↓
3. MONTAG 9:00 UHR ( automatisch )
   Cronjob prüft Airtable
   ↓
4. Für jeden aktivierten Service:
   - Erstellt ClickUp Folder
   - Erstellt Listen
   - Kopiert Template-Tasks mit Checklisten
   - Setzt Due Dates
   ↓
5. Airtable wird aktualisiert
   (Checkboxen auf "erledigt")
   ↓
6. Team arbeitet Tasks in ClickUp ab
```

### Workflow 2: Weekly Newsletter

```
1. MONTAG 9:00 UHR ( automatisch )
   notion-weekly-newsletters.sh
   ↓
2. Liest Notion-Kalender (KW10)
   Thema: "Internationaler Frauentag"
   ↓
3. Liest Airtable (Razeco)
   - Brand Assets
   - Klaviyo API Key
   - Produkt-Daten
   ↓
4. Erstellt HTML Template
   (Razeco Branding)
   ↓
5. Upload zu Klaviyo
   - Template
   - Campaign (DRAFT)
   - Subject, Preview, From
   ↓
6. MONTAG 9:15 UHR ( automatisch )
   newsletter-weekly-task.sh
   ↓
7. Erstellt ClickUp Task
   "[Razeco] Newsletter KW10"
   + 9-Item Checklist
   ↓
8. MANUELL (vor Sende-Datum):
   - Review in Klaviyo
   - Schedule klicken
   - Senden
```

---

## ⚠️ WICHTIGE HINWEISE

### Sicherheit
- Campaigns werden als DRAFT erstellt (nie auto-send)
- Manuelles Review erforderlich vor Senden
- API Keys in `~/.config/` (nicht im Repo)

### Cronjobs
- Alle laufen Montag 9:00/9:15 Uhr
- Logs in `~/.openclaw/workspace/logs/`
- Lock-Files verhindern Doppelausführung

### Erweiterungen
Neue Services hinzufügen:
1. Airtable Feld erstellen (Checkbox)
2. Status-Feld erstellen (Checkbox)
3. Script erstellen (ähnlich Cold Mail)
4. `clickup-services-cron.sh` erweitern
5. Testen

---

## 🔗 WICHTIGE URLs

| System | URL |
|--------|-----|
| Airtable Base | https://airtable.com/appbGhxy9I18oIS8E |
| ClickUp Delivery | https://app.clickup.com/90040311585 |
| n8n Dashboard | https://n8n.adsdrop.de |
| Klaviyo Campaigns | https://www.klaviyo.com/campaigns |

---

## 📞 SUPPORT

Bei Problemen:
1. Logs prüfen: `tail -f ~/.openclaw/workspace/logs/*.log`
2. Airtable Felder prüfen: `scripts/check-airtable-fields.sh`
3. Manuelles Testen: Scripts haben `--dry-run` Modus

---

**Dokumentation erstellt:** 24.02.2026  
**Nächste Überprüfung:** Nach Research-Agent Fertigstellung
