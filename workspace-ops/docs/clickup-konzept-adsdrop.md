# ClickUp Konzept für adsdrop
## Performance Marketing Agentur - Creative Operations & Workflow Management

**Erstellt:** 18.02.2026  
**Status:** Konzeptphase - Bereit für Implementierung  
**Nächster Schritt:** Review & Implementierung

---

## 1. Executive Summary

### Ziel
Aufbau eines optimierten ClickUp-Systems für:
- **Creative Testing & Iteration** (VSL, UGC, Static, Reels)
- **Kunden-Onboarding Automatisierung**
- **Performance Tracking & Reporting**
- **Team-Kollaboration & SOPs**

### Aktueller Stand
- ✅ ClickUp Skill erstellt (API-Integration)
- ✅ API-Token eingerichtet & getestet
- ✅ Team-ID: 9006104573 (Adsdrop)
- ✅ Notion-Dokumente analysiert (Creative Ops Templates)
- ✅ Best Practices recherchiert
- ⏳ Konzept erstellt (dieses Dokument)
- ⏳ Implementierung ausstehend

---

## 2. Anforderungsanalyse

### 2.1 Creative Testing Workflow

**Content-Formate:**
1. VSL (Video Sales Letter)
2. UGC (User Generated Content)
3. Static Ads (Bildanzeigen)
4. Reels / Shorts

**Prozess-Schritte:**
1. **Ideation** - Konzept/Hook entwickeln
2. **Briefing** - Creative Brief erstellen
3. **Creation** - Asset produzieren (Video/Design)
4. **Review** - Interne Freigabe
5. **Adjustments** - Korrekturen/Optimierungen
6. **R2L** - Ready to Launch
7. **Live** - Campaign gestartet
8. **Testing** - Performance-Phase (3-7 Tage)
9. **Analysis** - Auswertung (Winner/Loser)
10. **Archive** - Dokumentation & Learnings

**Benötigte Felder pro Creative:**
- Client (Dropdown)
- Format (VSL/UGC/Static/Reel) - Single Select
- Batch Number (z.B. "007")
- Hook Type (Problem/Agitation/Solution/Story)
- Platform (Meta/Google/TikTok)
- Creator/Designer (Assignee)
- Drive Folder URL (Assets)
- Status (Workflow-Status)
- ROAS (Performance)
- CTR (Performance)
- CPA (Performance)
- Test Duration
- Result (Winner/Loser/Inconclusive)
- Iteration of (Verlinkung zum Parent)

### 2.2 Kundenstruktur

**Option A: Pro Kunde ein Space**
- Vorteil: Maximale Trennung, Kunde könnte Zugriff erhalten
- Nachteil: Viele Spaces, unübersichtlich

**Option B: Zentraler Space mit Kunden-Foldern** ⭐ EMPFOHLEN
```
Delivery Space
├── 📁 Creatives by Client
│   ├── 📁 Razeco
│   │   └── 📝 Creative Pipeline
│   ├── 📁 Green Cola
│   │   └── 📝 Creative Pipeline
│   └── 📁 Ferro Berlin
│       └── 📝 Creative Pipeline
```

**Entscheidung:** Option B - Kunden-Folder im Delivery Space

### 2.3 Onboarding Automatisierung

**Trigger:** Neuer Kunde in Airtable (Status = "Onboarding")

**Automatische Tasks:**
1. Vertrag & Rechnung
2. Account Setup (Meta, Google, etc.)
3. Creative Onboarding (Briefing, Assets)
4. Tooling & Zugriffe
5. Kickoff Call

**Integration:**
- Airtable → ClickUp (neuer Kunde)
- ClickUp → n8n (Automation)
- n8n → Email/Slack (Notifications)

### 2.4 Dashboards & Reporting

**Rollen-basierte Dashboards:**

**Für Deniz (Agency Owner):**
- Creative Performance Overview
- Kunden-Status Board
- Umsatz/Performance pro Kunde
- Team Workload

**Für Media Buyer:**
- Live Campaigns
- Creative Testing Queue
- Performance Alerts

**Für Creative Team:**
- Active Productions
- Review Queue
- Creator Assignments

**Für Kunden (optional):**
- Creative Performance Report
- Testing Results

---

## 3. Optimierte Struktur

### 3.1 Space-Architektur

**Haupt-Spaces:**

1. **🎯 Delivery** (Haupt-Workspace)
   - Creative Production
   - Campaign Management
   - Client Work

2. **👥 Internal** (Interne Prozesse)
   - SOPs & Dokumentation
   - Team Management
   - Finanzen & Admin

3. **📊 Strategy** (Planung)
   - Research & Insights
   - Creative Strategy
   - Testing Roadmap

### 3.2 Delivery Space - Detaillierte Struktur

```
📦 Delivery
├── 📁 Creatives by Client
│   ├── 📁 Razeco
│   │   ├── 📝 Creative Pipeline (aktive Produktionen)
│   │   └── 📝 Creative Archive (abgeschlossen)
│   ├── 📁 Green Cola
│   │   ├── 📝 Creative Pipeline
│   │   └── 📝 Creative Archive
│   └── 📁 Ferro Berlin
│       ├── 📝 Creative Pipeline
│       └── 📝 Creative Archive
├── 📁 Campaigns
│   ├── 📝 Live Campaigns
│   └── 📝 Campaign Planning
└── 📁 Resources
    ├── 📝 Creator Pool
    ├── 📝 Winning Concepts
    └── 📝 Hook Database
```

### 3.3 Custom Fields Spezifikation

**Für Creative Pipeline:**

| Feld | Typ | Optionen / Format | Beschreibung |
|------|-----|-------------------|--------------|
| Client | Dropdown | Razeco, Green Cola, Ferro Berlin, ... | Kunde |
| Format | Single Select | VSL, UGC, Static, Reel | Content-Typ |
| Batch Number | Text | z.B. "007", "008" | Batch-ID |
| Hook Type | Single Select | Problem, Agitation, Solution, Story | Hook-Kategorie |
| Platform | Multi Select | Meta, Google, TikTok | Kanäle |
| Creator | People | Team-Mitglieder | Zuständig |
| Drive URL | URL | Google Drive Link | Asset-Ordner |
| Status | Single Select | Idea → Live → Archive | Workflow-Status |
| Priority | Single Select | Urgent, High, Normal, Low | Priorität |
| ROAS | Number | Dezimal | Return on Ad Spend |
| CTR | Percent | Prozent | Click-Through-Rate |
| CPA | Currency | Euro | Cost per Acquisition |
| Test Duration | Duration | Tage | Test-Phase |
| Result | Single Select | Winner, Loser, Inconclusive | Test-Ergebnis |
| Iteration Of | Relationship | Link zu anderem Task | Abgeleitet von |
| Due Date | Date | Datum | Deadline |
| Launch Date | Date | Datum | Go-Live |

---

## 4. Workflow-Design

### 4.1 Creative Production Workflow

```mermaid
Idea → Briefing → Creation → Review → Adjustments → R2L → Live → Testing → Analysis → Archive
```

**Status-Beschreibungen:**

- **💡 Idea** - Konzeptphase, Hook-Ideen sammeln
- **📝 Briefing** - Creative Brief erstellen, Assets sammeln
- **🎨 Creation** - Video/Design wird produziert
- **👀 Review** - Interne Qualitätskontrolle
- **🔧 Adjustments** - Korrekturen nach Feedback
- **✅ R2L** - Ready to Launch, finale Freigabe
- **🚀 Live** - Campaign ist gestartet
- **📊 Testing** - Performance-Phase (3-7 Tage)
- **📈 Analysis** - Auswertung, Winner/Loser Bestimmung
- **📦 Archive** - Dokumentation, Learnings extrahieren

### 4.2 Automationen

**Automation 1: Status-Updates**
- Wenn Status = "Live" → Setze Launch Date = heute
- Wenn Status = "Testing" → Erinnere nach 3 Tagen zur Analyse
- Wenn Status = "Analysis" & Result = "Winner" → Move to "Winner Archive"

**Automation 2: Notifications**
- Neue Task in Pipeline → Notify Creative Team
- Status = "Review" → Notify Media Buyer
- Status = "R2L" → Notify Deniz
- Result = "Winner" → Post in Slack Channel

**Automation 3: Time Tracking**
- Status = "Creation" → Start Timer
- Status = "Review" → Stop Timer (Creation)

**Automation 4: Kunden-Onboarding**
- Neuer Eintrag in Airtable (Kunden-Tabelle)
→ Create Folder in ClickUp
→ Create Onboarding Tasks
→ Send Email to Client
→ Notify Team

---

## 5. Integrationen

### 5.1 Airtable ↔ ClickUp

**Sync-Richtung Airtable → ClickUp:**
- Neue Kunden (Trigger: Onboarding-Status)
- Kunden-Updates (Status-Änderungen)
- Creative Performance Daten (nach Testing)

**Sync-Richtung ClickUp → Airtable:**
- Creative Status-Updates
- Task-Completion (Onboarding)
- Zeit-Tracking Daten

### 5.2 Google Drive Integration

**Struktur:**
```
📁 1_CLIENTS
├── 📁 Razeco
│   └── 📁 Creatives
│       ├── 📁 Batch-007
│       ├── 📁 Batch-008
│       └── 📁 Archive
```

**Integration:**
- ClickUp Task hat Feld "Drive URL"
- Automatisch verlinkt zum passenden Batch-Ordner

### 5.3 Slack / Notifications

**Channel:** #creatives oder #campaigns

**Notifications:**
- Winner Creative identified
- Campaign launched
- Review needed
- Onboarding completed

### 5.4 n8n Workflows

**Workflow 1: Kunden-Onboarding**
```
Airtable (Neuer Kunde) 
→ n8n 
→ ClickUp (Create Folder + Tasks)
→ Email (Client)
→ Slack (Team)
→ Airtable (Update Status)
```

**Workflow 2: Creative Testing Complete**
```
ClickUp (Status = Analysis)
→ n8n
→ Meta Ads API (Pull Performance Data)
→ ClickUp (Update ROAS/CTR/CPA)
→ Airtable (Sync Data)
→ Slack (Report Results)
```

---

## 6. Dashboards & Views

### 6.1 Board View (Kanban)

**Gruppierung:** Status
**Filter:** Client, Format, Priority
**Spalten:** Workflow-Status (Idea → Archive)

### 6.2 List View

**Gruppierung:** Client → Format
**Spalten:** Name, Status, Assignee, Due Date, ROAS
**Filter:** Active (nicht Archive)

### 6.3 Calendar View

**Anzeige:** Due Dates, Launch Dates
**Filter:** By Client, By Team Member

### 6.4 Dashboard: Creative Performance

**Widgets:**
- Active Creatives (Zahl)
- Testing Queue (Zahl)
- Winners this Month (Zahl)
- Average ROAS (Graph)
- Creative by Status (Pie Chart)
- Top Performing Hooks (Table)

### 6.5 Dashboard: Kunden-Übersicht

**Widgets:**
- Kunden-Status (List)
- Active Campaigns per Client
- Creative Pipeline per Client
- Onboarding Progress

---

## 7. Templates

### 7.1 Creative Task Template

**Titel:** [Client] Batch-[XXX] - [Hook Type] [Format]
**Beispiel:** Razeco Batch-007 - Problem Hook VSL

**Beschreibung:**
```
## Brief
[Beschreibung des Creatives]

## Assets
- Drive Folder: [URL]
- Script: [Link]
- References: [Links]

## Targeting
- Platform: [Meta/Google/TikTok]
- Audience: [Beschreibung]
- Budget: [€]

## Success Criteria
- ROAS Target: [X.X]
- CTR Target: [X%]
- Test Duration: [X days]
```

**Checkliste:**
- [ ] Brief approved
- [ ] Assets collected
- [ ] Script written
- [ ] Video recorded / Design created
- [ ] Edited & post-produced
- [ ] Reviewed & approved
- [ ] Uploaded to ad platform
- [ ] Campaign launched
- [ ] Testing phase complete
- [ ] Results analyzed

### 7.2 Onboarding Task Template

**Titel:** Onboarding - [Client Name]

**Checkliste (27 Items):**
- [ ] Vertrag unterschrieben
- [ ] Setup-Rechnung bezahlt
- [ ] Airtable Entry created
- [ ] Google Drive Folder created
- [ ] ClickUp Folder created
- [ ] Meta Business Manager access
- [ ] Google Ads access
- [ ] Shopify access (if applicable)
- [ ] Brand Assets collected
- [ ] Brand Guidelines documented
- [ ] Creative Brief Template customized
- [ ] First Kickoff Call scheduled
- [ ] ... (weitere Items)

---

## 8. SOPs (Standard Operating Procedures)

### SOP 1: Creative Testing Prozess

1. **Idee generieren** (Hook Database checken)
2. **Briefing erstellen** (Template nutzen)
3. **Assets sammeln** (Drive-Ordner anlegen)
4. **Produktion** (Creator/Designer assignen)
5. **Review** (Media Buyer + Creative Lead)
6. **Launch** (Campaign aufsetzen)
7. **Testing** (3-7 Tage laufen lassen)
8. **Analysis** (Performance checken)
9. **Archivierung** (Winner/Loser dokumentieren)

### SOP 2: Winner Creative Iteration

1. Winner identifizieren (ROAS > Target)
2. Neue Variante planen (neuer Hook/neue Angle)
3. Als "Iteration of" verlinken
4. Schnell produzieren (while hot)
5. Testen

### SOP 3: Kunden-Onboarding

1. Vertrag & Payment
2. Tech Setup (Zugriffe)
3. Brand Onboarding (Assets, Guidelines)
4. Creative Onboarding (erste Briefings)
5. Kickoff Call
6. First Campaign Launch

---

## 9. Implementierungs-Plan

### Phase 1: Struktur (30 Min)
- [ ] Spaces erstellen/optimieren
- [ ] Folder-Struktur aufbauen
- [ ] Listen erstellen
- [ ] Custom Fields anlegen

### Phase 2: Workflows (30 Min)
- [ ] Status-Workflow definieren
- [ ] Automationen einrichten
- [ ] Views konfigurieren
- [ ] Templates erstellen

### Phase 3: Integrationen (30 Min)
- [ ] n8n Workflows bauen
- [ ] Airtable-Sync testen
- [ ] Slack Notifications
- [ ] Drive-Integration

### Phase 4: Test & Dokumentation (30 Min)
- [ ] Test-Tasks erstellen
- [ ] Workflows testen
- [ ] Team einweisen
- [ ] SOPs finalisieren

**Gesamtaufwand:** ~2 Stunden

---

## 10. Nächste Schritte

### Sofort (heute)
- [ ] Dieses Konzept reviewen
- [ ] Feedback geben / Anpassungen wünschen
- [ ] Go/No-Go Entscheidung

### Morgen (Implementierung)
- [ ] Phase 1: Struktur bauen
- [ ] Phase 2: Workflows einrichten
- [ ] Phase 3: Integrationen verbinden
- [ ] Phase 4: Testen & Launch

### Danach (Optimierung)
- [ ] 1 Woche: Daily Usage, Feedback sammeln
- [ ] 2 Wochen: Erste Optimierungen
- [ ] 1 Monat: Full Review & Adjustments

---

## Anhänge

### A: Aktuelle ClickUp-Struktur (Vorher)
- 2 Spaces
- 3 Folder
- ~45 Tasks
- Probleme: Keine Custom Fields, unklare Struktur

### B: Notion-Analyse (Übernommen)
- Master Creative Database
- Creator Pool
- Hook Database
- Launch Systems
- SOPs

### C: Best Practices (Recherche)
- ZenPilot Agency Framework
- UpSys Creative Operations
- ClickUp Community Templates

---

**Dokument erstellt von:** AI Agent (Brain)  
**Zur Fortsetzung:** Dieses Konzept im Workspace speichern und morgen damit weiterarbeiten.