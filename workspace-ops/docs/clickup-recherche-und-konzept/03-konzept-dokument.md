# Konzept: Optimiertes ClickUp-System für adsdrop

## 1. Space-Struktur (Ziel)

```
📁 Growth (bestehend, optimieren)
├── 📂 CRM ✅ (bleibt)
└── 📂 Marketing ✅ (bleibt)
    ├── 📋 Content
    ├── 📋 Outbound
    └── 📋 Newsletter

📁 Delivery (bestehend, umstrukturieren)
├── 📂 [Kunde 1: Green Cola Germany]
│   ├── 📋 Paid Social (Kampagnen, Reporting)
│   ├── 📋 Creative Production (Creatives für diesen Kunden)
│   └── 📋 Onboarding (Checkliste, einmalig)
├── 📂 [Kunde 2: schnelleinfachgesund]
│   ├── 📋 Paid Social
│   ├── 📋 Creative Production
│   └── 📋 Onboarding
├── 📂 [Kunde 3: Ferro Berlin]
│   └── ...
├── 📂 [Kunde N: ...]
│   └── ...
└── 📂 _Templates (versteckt/archived)
    └── 📋 Client Onboarding Template

📁 Creative Operations (NEU)
├── 📋 Creative Pipeline (Alle Creatives, alle Kunden)
├── 📋 Creative Ideas (Backlog)
├── 📋 Creative Learnings (Insights)
├── 📋 Creative Archive (Abgeschlossen)
├── 📋 Creator Pool (Datenbank)
├── 📋 Ads Menu (Referenz: Ad-Formate)
└── 📋 Shoot Schedule (Calendar View)

📁 Operations (NEU)
├── 📂 Admin
│   ├── 📋 Aufgaben (allgemein)
│   └── 📋 Inbox
├── 📂 Projekte
│   ├── 📋 Shopify Theme
│   └── 📋 Meta Ads Lead Magnet
└── 📂 SOPs & Docs
    └── (ClickUp Docs)
```

### Begründung

- **Creative Operations als eigener Space:** Creative Testing ist der Kernprozess. Ein eigener Space ermöglicht eigene Statuses, Custom Fields und Views ohne die Client-Delivery-Struktur zu belasten.
- **Kunden als Folder:** Best Practice nach ZenPilot. Ermöglicht Folder-Level Views, eigene Statuses pro Kunde wenn nötig, und klare Trennung.
- **Operations:** Interne Projekte raus aus Delivery. Clean Separation.

---

## 2. Creative Testing System

### 2.1 Status-Workflow (Creative Pipeline)

```
💭 Backlog → 📋 Strategy/Briefing → 🎬 Filming/Content → ✂️ Editing → 
👀 Internal Review → 🔄 Revisions → ✅ Approved → 🚀 Ready to Launch → 
📊 Launched/Testing → 🏆 Winner → 📦 Archive
```

Alternativ (vereinfacht, empfohlen):
```
Idea → Briefing → Content → Cutting → Review → Adjustments → R2L → Launched
```
→ Dies entspricht dem bestehenden schnelleinfachgesund-Workflow und ist praxiserprobt!

### 2.2 Custom Fields Spezifikation

| # | Field Name | Typ | Optionen | Pflicht? | Begründung |
|---|---|---|---|---|---|
| 1 | **Client** | Dropdown | Green Cola, schnelleinfachgesund, Ferro Berlin, RAZECO, ATB Bau | ✅ Ja | Filtern nach Kunde |
| 2 | **Concept Type** | Dropdown | Video Concept, Static Concept, Motion Graphics | ✅ Ja | Art des Creatives |
| 3 | **Creative Type** | Dropdown | Net New, Iteration | ✅ Ja | Neu vs. Iteration |
| 4 | **Hook Type** | Dropdown | Problem/Pain, Question, Bold Statement, Social Proof, Before/After, Shock/Pattern Interrupt | Nein | Hook-Testing & Learnings |
| 5 | **Ad Format** | Dropdown | UGC, Testimonial, Warehouse, Midjourney/AI, Humorous, Educational | Nein | Aus Notion Ads Menu |
| 6 | **Platform** | Dropdown | Meta, TikTok, Google, YouTube, Pinterest | Nein | Plattform-Zuordnung |
| 7 | **Batch No.** | Number | - | Nein | Batch-Gruppierung |
| 8 | **Creator Needed** | Checkbox | - | Nein | UGC-Bedarf |
| 9 | **In-Person Shoot** | Checkbox | - | Nein | Logistik-Planung |
| 10 | **Performance Score** | Number | - | Nein | Post-Launch KPI (z.B. ROAS) |
| 11 | **Spend** | Currency | - | Nein | Ad Spend für dieses Creative |
| 12 | **Result** | Dropdown | Winner 🏆, Loser ❌, Inconclusive 🤷, Not Tested | Nein | Test-Ergebnis |

### 2.3 Archiv-Strategie

- Creatives mit Status "Launched" + Result "Winner/Loser" → automatisch nach 30 Tagen in "Creative Archive" verschieben
- Archive behält alle Custom Fields für spätere Analyse
- Regelmäßiges Review der Learnings aus archivierten Winners

### 2.4 Views

| View | Typ | Filter/Gruppierung | Für wen |
|---|---|---|---|
| **Pipeline Board** | Board | Gruppiert nach Status | Alle |
| **By Client** | Board | Gruppiert nach Client CF | Account Manager |
| **My Tasks** | List | Assignee = Me | Jeder |
| **This Week** | List | Due Date = This Week | Jeder |
| **Winners Gallery** | Board | Result = Winner | Strategist |
| **Batch View** | Table | Gruppiert nach Batch No. | Strategist |
| **Calendar** | Calendar | - | Alle |

---

## 3. Kunden-Onboarding System

### 3.1 Onboarding-Checkliste (Template)

Wenn ein neuer Kunde gewonnen wird (CRM → Won 🏆), folgende Tasks:

```
📋 Onboarding [Kundenname]
├── ✅ Vertrag & Payment Setup
│   ├── Vertrag unterschrieben
│   ├── Stripe Subscription eingerichtet
│   └── Erste Rechnung versendet
├── ✅ Account Setup
│   ├── Meta Business Manager Zugang erhalten
│   ├── Ad Accounts eingerichtet
│   ├── Pixel/CAPI verifiziert
│   ├── Google Analytics Zugang
│   └── TikTok Business Center (wenn relevant)
├── ✅ Creative Onboarding
│   ├── Brand Guidelines erhalten
│   ├── Produktfotos & Assets erhalten
│   ├── Zielgruppen-Brief ausgefüllt
│   ├── Wettbewerbs-Analyse durchgeführt
│   └── Erste Creative-Strategie erstellt
├── ✅ Tooling
│   ├── ClickUp Folder erstellt
│   ├── Google Drive Ordner erstellt
│   ├── Airtable Record angelegt
│   └── Kommunikationskanal eingerichtet (Slack/WhatsApp)
└── ✅ Kickoff
    ├── Kickoff-Call durchgeführt
    ├── Reporting-Rhythmus vereinbart
    └── Erste Kampagne geplant
```

### 3.2 Automatisierung via n8n

```
Trigger: CRM Task → Status "Won 🏆"
  ↓
1. Erstelle Folder in Delivery Space mit Kunden-Name
2. Erstelle Listen: "Paid Social", "Creative Production", "Onboarding"
3. Wende Onboarding-Template auf "Onboarding"-Liste an
4. Erstelle Google Drive Ordner
5. Sende Notification an Team (Slack/WhatsApp)
6. Erstelle Airtable Record
```

---

## 4. Dashboard & Reporting Konzept

### 4.1 Agency Owner Dashboard

| Widget | Typ | Daten |
|---|---|---|
| Active Clients | Number | Anzahl offener Kunden-Folders |
| Pipeline Value | Number | Summe CRM Deal Values |
| Creative Output This Month | Number | Tasks mit Status "Launched" diesen Monat |
| Team Workload | Bar Chart | Tasks pro Person |
| Overdue Tasks | List | Alle überfälligen Tasks |
| Creative Win Rate | Pie Chart | Winners vs. Losers |

### 4.2 Creative Operations Dashboard

| Widget | Typ | Daten |
|---|---|---|
| Pipeline Status | Status Board | Creative Pipeline nach Status |
| By Client | Bar Chart | Creatives pro Kunde |
| Batch Progress | Progress Bar | Aktueller Batch % complete |
| Ideas Backlog | Number | Anzahl Ideas |
| Time to Launch | Line Chart | Durchschnittliche Tage Idea → Launch |

### 4.3 Client Report (Template)

Wöchentlich/Monatlich per n8n generierbar:
- Anzahl neue Creatives
- Creatives in Testing
- Winners/Losers mit Performance-Daten
- Nächste geplante Creatives
- Budget-Übersicht

---

## 5. Automatisierungen-Plan

### 5.1 ClickUp-native Automationen

| # | Trigger | Aktion | Space |
|---|---|---|---|
| 1 | Task → "Review" | Assign Final Reviewer | Creative Ops |
| 2 | Task → "R2L" | Notify Account Manager | Creative Ops |
| 3 | Task → "Launched" | Add Due Date +7 Tage (für Ergebnis-Check) | Creative Ops |
| 4 | Alle Subtasks Complete | Parent → "Complete" | Delivery |
| 5 | Priority → Urgent | Notify via Email | Alle |

### 5.2 n8n Automationen

| # | Flow | Trigger | Actions |
|---|---|---|---|
| 1 | **Client Onboarding** | CRM → Won | Folder + Lists + Template + Drive + Airtable |
| 2 | **Weekly Report** | Cron (Montag 9:00) | Aggregate Tasks → Generate Report → Email |
| 3 | **Creative Result Check** | Task "Launched" + 7 Tage | Reminder: "Performance eintragen!" |
| 4 | **Airtable → ClickUp Sync** | Airtable Webhook | Update Performance Score CF |
| 5 | **Overdue Alert** | Cron (täglich 9:00) | Check Overdue → Slack/WhatsApp |

### 5.3 Airtable Integration

Airtable (appbGhxy9I18oIS8E) kann als Performance-Daten-Hub dienen:
- Ad Performance Daten (ROAS, CPA, CTR) werden in Airtable getrackt
- n8n synct relevante KPIs zurück in ClickUp Custom Fields
- Dashboards in ClickUp zeigen aggregierte Performance
