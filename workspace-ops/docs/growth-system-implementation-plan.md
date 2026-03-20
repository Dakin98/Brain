# Growth System Implementierungs-Plan – adsdrop

> Stand: 24.02.2026 | ClickUp Space: Growth (90040244466)

---

## 1. IST-Analyse

### Growth Space Struktur

```
Growth Space (90040244466)
├── Marketing Folder (90153490386) — 8 Tasks
│   ├── Content (901505427933) — 5 Tasks
│   │   └── Custom Fields: Content Idee (checkbox)
│   │   └── Status: Open → In Bearbeitung → Review → Closed
│   ├── Outbound (901505427931) — 2 Tasks
│   │   └── Custom Fields: keine
│   │   └── Status: Open → In Bearbeitung → Review → Closed
│   └── Newsletter (901505427932) — 1 Task
│       └── Custom Fields: keine
│       └── Status: Open → In Bearbeitung → Review → Closed
│
└── CRM Folder (90153948883) — 16 Tasks
    └── CRM (901506196069) — 16 Tasks
        └── Custom Fields: E-Mail, Quelle, Tags, Firma, Deal Value,
            Paket, Radar-Status, Telefon, Website, Nächste Aufgabe,
            Setter, Cash Collected
        └── Status: Prospect → Quali Call Terminiert → Quali Call No-Show →
            Quali Call Follow-Up → Strategie Call Terminiert →
            Strategie Call No-Show → Strategie Call No Offer →
            Angebot gemacht → Won 🏆 → Lost ❌
```

### Bewertung

| Bereich | Status | Gaps |
|---------|--------|------|
| Content | ⚠️ Rudimentär | Nur 1 Custom Field, kein Pipeline-Workflow, keine Plattform-Trennung |
| Outbound | ⚠️ Fast leer | Keine Fields, keine Struktur für Campaigns/Sequences |
| Newsletter | ⚠️ Minimal | Keine Fields für Tracking |
| CRM | ✅ Solide | Guter Sales-Funnel, 12 Custom Fields, klarer Workflow |

---

## 2. Content Engine — SOLL-Struktur

### Folder-Hierarchie

```
Marketing Folder (90153490386)
└── Content Engine (NEUER Sub-Folder oder bestehende Listen umbauen)
    ├── Content Ideas (List)        — Ideen-Backlog
    ├── YouTube Pipeline (List)     — Video-Produktion
    ├── Reels Pipeline (List)       — Short-Form Repurposing
    ├── LinkedIn Pipeline (List)    — LinkedIn Posts
    ├── Newsletter Pipeline (List)  — Newsletter-Ausgaben
    └── Distribution Tracker (List) — Cross-Platform Verteilung
```

> **Empfehlung:** Bestehende Listen (Content, Newsletter) in die neue Struktur migrieren statt parallel zu führen.

---

### 2.1 Content Ideas

**Status-Workflow:**
| Status | Typ | Farbe |
|--------|-----|-------|
| 💡 Idea | open | grau |
| 🔍 Researching | custom | lila |
| ✅ Approved | custom | grün |
| 🗓️ Scheduled | custom | blau |
| ❌ Rejected | closed | rot |

**Custom Fields:**

| Field | Typ | Optionen / Details |
|-------|-----|--------------------|
| Content Pillar | Dropdown | Ads Education, Case Studies, Behind the Scenes, Industry News, How-To |
| Format | Dropdown | YouTube Long, YouTube Short, Reel, LinkedIn Post, Newsletter, Carousel |
| Priority Score | Number | 1-10 (Impact × Machbarkeit) |
| Effort | Dropdown | Low (< 2h), Medium (2-5h), High (5h+) |
| Target Audience | Dropdown | E-Com Brands, SaaS, Agencies, Beginner, Advanced |
| Source / Inspiration | URL | Link zur Quelle |
| Keyword / Hook | Short Text | SEO Keyword oder Hook-Idee |
| Estimated Reach | Number | Geschätzte Views/Impressions |

**Views:**
- **Board View** (Default) — Kanban nach Status
- **Table View** — Alle Ideen mit Fields sortierbar
- **Grouped by Pillar** — Table gruppiert nach Content Pillar

---

### 2.2 YouTube Pipeline

**Status-Workflow:**
| Status | Typ | Farbe |
|--------|-----|-------|
| 📝 Scripting | open | grau |
| 🎬 Recording | custom | orange |
| ✂️ Editing | custom | lila |
| 👀 Review | custom | blau |
| 📅 Scheduled | custom | gelb |
| 🟢 Published | custom | grün |
| 📊 Analyzing | done | dunkelgrün |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Video Title | Short Text | Finaler Titel |
| Thumbnail Status | Dropdown | Not Started, Draft, Final |
| Content Pillar | Dropdown | (gleiche wie Ideas) |
| Publish Date | Date | Geplantes Veröffentlichungsdatum |
| YouTube URL | URL | Link nach Upload |
| Views (7 Tage) | Number | Manuell oder via API |
| Watch Time (h) | Number | Aus YouTube Analytics |
| CTR (%) | Number | Click-Through-Rate Thumbnail |
| Avg. View Duration | Short Text | z.B. "4:32" |
| Subscriber Delta | Number | Neue Subs durch dieses Video |
| Script Doc | URL | Link zu Google Doc |
| B-Roll Needed | Checkbox | |
| Reels Created | Number | Anzahl erstellter Reels |

**Standard-Checkliste (Template):**
```
□ Topic Research & Outline
□ Script schreiben
□ Script Review
□ Thumbnail Konzept
□ Recording Setup
□ A-Roll aufnehmen
□ B-Roll aufnehmen
□ Editing
□ Thumbnail finalisieren
□ Titel & Description optimieren
□ Tags & End Screens
□ Upload & Schedule
□ Community Post erstellen
□ Distribution Tasks erstellen (Reels, LinkedIn, Newsletter)
```

**Views:**
- **Board View** — Kanban Pipeline
- **Calendar View** — Publish-Dates auf einen Blick
- **Table View** — Performance-Übersicht aller Videos

---

### 2.3 Reels Pipeline

**Status-Workflow:**
| Status | Typ | Farbe |
|--------|-----|-------|
| 🎯 Identified | open | grau |
| ✂️ Clipping | custom | orange |
| 📝 Caption & Hook | custom | lila |
| 👀 Review | custom | blau |
| 📅 Scheduled | custom | gelb |
| 🟢 Published | done | grün |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Source Video | Relationship | Link zum YouTube Task |
| Hook Timestamp | Short Text | z.B. "02:15 - 02:45" |
| Platform | Dropdown | Instagram, TikTok, YouTube Shorts, Alle |
| Caption | Long Text | Post-Caption |
| Views | Number | Nach 7 Tagen |
| Saves | Number | |
| Shares | Number | |
| Profile Visits | Number | |
| Hashtags | Short Text | |
| Trending Audio | Checkbox | Trending Sound verwendet? |

**Views:**
- **Board View** — Pipeline
- **Table View** — Performance-Vergleich
- **Grouped by Source Video** — Welche Reels pro YouTube Video

---

### 2.4 LinkedIn Pipeline

**Status-Workflow:**
| Status | Typ | Farbe |
|--------|-----|-------|
| 💡 Draft | open | grau |
| ✍️ Writing | custom | orange |
| 👀 Review | custom | blau |
| 📅 Scheduled | custom | gelb |
| 🟢 Published | done | grün |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Post Type | Dropdown | Text, Carousel, Video, Poll, Article |
| Content Pillar | Dropdown | (gleiche wie Ideas) |
| Source Content | Relationship | Link zum YouTube Task |
| LinkedIn URL | URL | Link zum Post |
| Impressions | Number | |
| Engagement Rate (%) | Number | |
| Comments | Number | |
| Reposts | Number | |
| Profile Views Delta | Number | |
| Publish Date | Date | |

**Views:**
- **Board View** — Pipeline
- **Calendar View** — Posting-Schedule
- **Table View** — Engagement Tracker

---

### 2.5 Newsletter Pipeline

**Status-Workflow:**
| Status | Typ | Farbe |
|--------|-----|-------|
| 📋 Planning | open | grau |
| ✍️ Writing | custom | orange |
| 🎨 Design | custom | lila |
| 👀 Review | custom | blau |
| 📅 Scheduled | custom | gelb |
| 📨 Sent | done | grün |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Subject Line | Short Text | |
| Preview Text | Short Text | |
| Content Pillar | Dropdown | |
| Source Content | Relationship | Link zum YouTube Task |
| Klaviyo Campaign ID | Short Text | |
| Send Date | Date | |
| Subscriber Count | Number | Zum Zeitpunkt des Sends |
| Open Rate (%) | Number | |
| Click Rate (%) | Number | |
| Unsubscribes | Number | |
| Revenue Attributed | Currency | Falls E-Com relevant |

**Standard-Checkliste (Template):**
```
□ Thema festlegen (basierend auf YouTube dieser Woche)
□ Subject Line + Preview Text
□ Newsletter Text schreiben
□ CTA definieren
□ Design in Klaviyo
□ Test-Mail senden
□ Review & Freigabe
□ Schedule in Klaviyo
□ Performance nach 48h eintragen
```

**Views:**
- **Board View** — Pipeline
- **Calendar View** — Send-Dates
- **Table View** — Performance-Übersicht

---

### 2.6 Distribution Tracker

**Status-Workflow:**
| Status | Typ | Farbe |
|--------|-----|-------|
| ⏳ Pending | open | grau |
| ✅ Distributed | done | grün |
| ⏭️ Skipped | closed | rot |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Source Content | Relationship | Original YouTube Task |
| Channel | Dropdown | Reels, LinkedIn, Newsletter, Twitter, Community |
| Distribution Date | Date | |
| Distributed By | Users | |

> **Zweck:** Pro YouTube-Video sieht man auf einen Blick, welche Kanäle schon bespielt wurden. Wird automatisch per Automation befüllt.

---

## 3. Outbound Engine — SOLL-Struktur

> **Info:** Techstack ist bereits aktiv: Apollo.io, Gmail, 4 Email-Accounts, Domains gekauft & gewarmt. Kein Domain/Inbox-Setup nötig. Fokus = Campaign Management & Tracking.

### Folder-Hierarchie

```
Marketing Folder (90153490386)
└── Outbound Engine (NEUER Sub-Folder oder bestehende "Outbound" Liste umbauen)
    ├── Lead Lists (List)           — Segmentierte Lead-Listen
    ├── Campaigns (List)            — Aktive & geplante Campaigns
    ├── Sequences (List)            — E-Mail Sequenz-Templates
    ├── Reply Management (List)     — Antworten bearbeiten
    └── Inbox & Domain Health (List)— Monitoring (4 Accounts)
```

---

### 3.1 Lead Lists

**Status-Workflow:**
| Status | Typ |
|--------|-----|
| 🔍 Sourcing | open |
| 📋 Ready | custom |
| 🚀 In Campaign | custom |
| ✅ Exhausted | done |
| ❌ Bad Quality | closed |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| ICP Segment | Dropdown | E-Com 1-5M, E-Com 5-20M, SaaS, Agency, etc. |
| Lead Count | Number | Anzahl Kontakte |
| Source | Dropdown | Apollo, LinkedIn, Manual, Referral |
| Apollo List URL | URL | Link zur Apollo-Liste |
| Upload Date | Date | |
| Quality Score | Dropdown | A, B, C |
| Vertical | Short Text | z.B. "Fashion E-Com", "B2B SaaS" |
| Geography | Dropdown | DACH, EU, US, Global |

**Views:**
- **Table View** (Default) — Übersicht aller Listen
- **Grouped by ICP Segment** — Listen nach Segment

---

### 3.2 Campaigns

**Status-Workflow:**
| Status | Typ |
|--------|-----|
| 📋 Planning | open |
| ⚙️ Setup | custom |
| 🟢 Active | custom |
| ⏸️ Paused | custom |
| ✅ Completed | done |
| ❌ Cancelled | closed |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| ICP Segment | Dropdown | (gleich wie Lead Lists) |
| Sequence Used | Relationship | Link zur Sequence |
| Lead List | Relationship | Link zur Lead List |
| Lead Count | Number | |
| Emails Sent | Number | |
| Open Rate (%) | Number | |
| Reply Rate (%) | Number | |
| Positive Reply Rate (%) | Number | |
| Meetings Booked | Number | |
| Meeting Rate (%) | Number | |
| Start Date | Date | |
| End Date | Date | |
| Apollo/Instantly Campaign ID | Short Text | |
| Revenue Generated | Currency | Aus gewonnenen Deals |

**Standard-Checkliste (Template):**
```
□ ICP & Segment definieren
□ Lead-Liste in Apollo erstellen / filtern
□ Lead-Liste exportieren & prüfen
□ Sequence auswählen / anpassen
□ Campaign in Tool aufsetzen
□ Test-Mails senden
□ Campaign starten
□ Tag 3: Erste Metrics checken
□ Tag 7: Reply-Handling
□ Woche 2: Performance Review
□ Campaign abschließen & Learnings dokumentieren
```

**Views:**
- **Board View** — Pipeline nach Status
- **Table View** — Performance Dashboard
- **Calendar View** — Start/End Dates

---

### 3.3 Sequences

**Status-Workflow:**
| Status | Typ |
|--------|-----|
| ✍️ Drafting | open |
| 🧪 Testing | custom |
| ✅ Active | custom |
| 📦 Archived | closed |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Sequence Name | Short Text | |
| Step Count | Number | Anzahl E-Mails |
| ICP Segment | Dropdown | |
| Tone | Dropdown | Formal, Casual, Direct, Storytelling |
| Avg. Open Rate (%) | Number | Über alle Campaigns |
| Avg. Reply Rate (%) | Number | |
| Times Used | Number | In wie vielen Campaigns |
| Step 1 Subject | Short Text | |
| Step 1 Preview | Long Text | Erster Absatz |
| Google Doc URL | URL | Volle Sequence |

**Views:**
- **Table View** (Default) — Alle Sequences mit Performance
- **Grouped by ICP** — Sequences pro Segment

---

### 3.4 Reply Management

**Status-Workflow:**
| Status | Typ |
|--------|-----|
| 📩 New Reply | open |
| 🔍 Reviewing | custom |
| 🗓️ Meeting Booked | custom |
| 🔁 Follow-Up | custom |
| ✅ Handled | done |
| ❌ Not Interested | closed |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Lead Name | Short Text | |
| Lead Email | Email | |
| Company | Short Text | |
| Campaign | Relationship | Link zur Campaign |
| Reply Type | Dropdown | Interested, Not Interested, OOO, Referral, Bounce, Unsubscribe |
| Reply Snippet | Long Text | Kopie der Antwort |
| Meeting Date | Date | Falls gebucht |
| CRM Task | Relationship | Link zum CRM-Eintrag |
| Response Time (h) | Number | Zeit bis zur Antwort |
| Follow-Up Count | Number | |

**Views:**
- **Board View** (Default) — Kanban nach Reply Type
- **Table View** — Alle Replies
- **Filtered: Interested Only** — Fokus auf heiße Leads

---

### 3.5 Inbox & Domain Health

**Status-Workflow:**
| Status | Typ |
|--------|-----|
| 🟢 Healthy | open |
| ⚠️ Warning | custom |
| 🔴 Issues | custom |
| ❌ Deactivated | closed |

**Custom Fields:**

| Field | Typ | Details |
|-------|-----|---------|
| Domain | Short Text | z.B. adsdrop.io |
| Provider | Dropdown | Gmail, Google Workspace |
| Inbox Email | Email | |
| Daily Send Limit | Number | |
| Current Daily Volume | Number | |
| Health Score (%) | Number | Deliverability |
| SPF | Checkbox | Konfiguriert? |
| DKIM | Checkbox | |
| DMARC | Checkbox | |
| Last Check Date | Date | |
| Notes | Long Text | |

> **Hinweis:** Da Domains & Inboxen schon laufen, dient diese Liste nur dem Monitoring. Kein Setup nötig — einfach die 4 bestehenden Accounts eintragen.

---

## 4. Implementierungs-Roadmap

### Phase 1: Content Engine (Woche 1)

| Tag | Aufgabe | Dauer |
|-----|---------|-------|
| Mo | Content Engine Folder erstellen, 6 Listen anlegen | 2h |
| Mo | Status-Workflows für alle Listen konfigurieren | 1h |
| Di | Custom Fields für Content Ideas + YouTube erstellen | 2h |
| Di | Custom Fields für Reels + LinkedIn + Newsletter erstellen | 2h |
| Mi | Task-Templates mit Checklisten für YouTube + Newsletter | 2h |
| Mi | Views einrichten (Board, Table, Calendar pro Liste) | 1h |
| Do | Bestehende Tasks aus "Content" Liste migrieren | 1h |
| Do-Fr | Test: Erstes YouTube-Video durch die komplette Pipeline | 3h |

### Phase 2: Outbound Engine (Woche 2)

| Tag | Aufgabe | Dauer |
|-----|---------|-------|
| Mo | Outbound Engine Folder erstellen, 5 Listen anlegen | 1.5h |
| Mo | Status-Workflows konfigurieren | 1h |
| Di | Custom Fields für alle 5 Listen erstellen | 3h |
| Di | 4 bestehende Inboxen in Domain Health eintragen | 0.5h |
| Mi | Task-Templates für Campaigns erstellen | 1.5h |
| Mi | Views einrichten | 1h |
| Do | Bestehende Outbound-Tasks migrieren | 1h |
| Do-Fr | Test: Erste Campaign durch die Pipeline | 2h |

### Phase 3: Automatisierungen (Woche 3-4)

| Woche | Script | Dauer |
|-------|--------|-------|
| W3 Mo-Di | YouTube → Reels Auto-Tasks | 4h |
| W3 Mi-Do | YouTube → LinkedIn + Newsletter Reminder | 4h |
| W3 Fr | Reply Alert → CRM Integration | 3h |
| W4 Mo-Mi | Weekly Reporting Automation | 6h |
| W4 Do-Fr | Testing & Bugfixing aller Automations | 4h |

### Phase 4: Launch & Optimize (Woche 5+)

| Zeitraum | Aufgabe |
|----------|---------|
| W5 | Erste volle Woche mit beiden Engines |
| W5 | Erster automatischer Weekly Report |
| W6 | Review: Was funktioniert, was nicht? |
| W6 | Custom Fields anpassen basierend auf Erfahrung |
| W7+ | Dashboard-Optimierung, weitere Automations |

---

## 5. Offene Fragen an Deniz

1. **Reihenfolge:** Content Engine oder Outbound Engine zuerst? → Empfehlung: Content Engine zuerst, da YouTube-Produktion regelmäßig läuft und sofort Struktur braucht.
2. **Content-Zeit:** Wie viele Stunden pro Woche für Content Creation verfügbar? → Beeinflusst Publish-Frequenz.
3. **Reporting-Tool:** ClickUp Dashboards reichen für den Start. Airtable nur wenn ClickUp-Limits erreicht werden (z.B. komplexe Formeln, Cross-List-Berechnungen).
4. **Cold-Mail-Tool:** Wird Apollo auch zum Senden genutzt, oder läuft der Versand über ein anderes Tool (Instantly, Smartlead)? → Beeinflusst welche API integriert wird.
5. **Team:** Wer arbeitet noch im System? Nur Deniz, oder auch VAs / Editoren? → Beeinflusst Permissions & Assignee-Fields.

---

## 6. IDs & Referenzen

| Ressource | ID |
|-----------|-----|
| Team | 9006104573 |
| Growth Space | 90040244466 |
| Marketing Folder | 90153490386 |
| CRM Folder | 90153948883 |
| Content List (alt) | 901505427933 |
| Outbound List (alt) | 901505427931 |
| Newsletter List (alt) | 901505427932 |
| CRM List | 901506196069 |
