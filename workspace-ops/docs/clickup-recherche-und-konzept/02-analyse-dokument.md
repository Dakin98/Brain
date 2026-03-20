# Analyse: Aktueller Stand & Optimierungspotenzial

## 1. ClickUp – Aktueller Stand

### 1.1 Aktuelle Struktur

```
Team: 9006104573 (adsdrop)
Members: Deniz Akin (63066979), Richard Lingath (84109837)

📁 Space: Growth (90040244466)
├── 📂 Marketing (90153490386) [8 Tasks]
│   ├── 📋 Content [5 Tasks]
│   ├── 📋 Outbound [2 Tasks]
│   └── 📋 Newsletter [1 Task]
└── 📂 CRM (90153948883) [16 Tasks]
    └── 📋 CRM [16 Tasks]
        Statuses: Prospect → Quali Call terminiert → Quali Call No-Show →
        Quali Call Follow-Up → Strategie Call terminiert → Strategie Call No-Show →
        Strategie Call No Offer → Angebot gemacht → Won 🏆 → Lost ❌

📁 Space: Delivery (90040311585)
├── 📂 Clients (90040881723) [8 Tasks]
│   ├── 📋 Green Cola Germany [1 Task]
│   ├── 📋 schnelleinfachgesund [0 Tasks] ⭐ Eigene Creative Statuses!
│   ├── 📋 Ferro Berlin [0 Tasks]
│   ├── 📋 Client Work [6 Tasks]
│   ├── 📋 RAZECO [1 Task]
│   └── 📋 ATB Bau [0 Tasks]
├── 📂 Intern (90154036937) [13 Tasks]
│   ├── 📋 Shopify Theme [5 Tasks]
│   ├── 📋 Inbox [1 Task]
│   ├── 📋 Aufgaben [2 Tasks]
│   └── 📋 Meta Ads Lead Magnet [5 Tasks]
└── 📂 Creative Testing (901514520867) [7 Tasks]
    ├── 📋 Creative Pipeline [3 Tasks] ⚠️ Keine Custom Fields!
    ├── 📋 Creative Archive [0 Tasks]
    ├── 📋 💡 Creative Ideas [3 Tasks]
    ├── 📋 📝 Creative Learnings [1 Task]
    └── 📋 👤 Creator Pool [0 Tasks]
```

### 1.2 Was funktioniert gut ✅

1. **CRM-Workflow** – Sehr granularer Sales-Pipeline mit 10 Statuses, ideal für Agentur-Vertrieb
2. **Growth/Delivery Trennung** – Grundsätzlich richtige Aufteilung nach Best Practices
3. **Creative Testing Folder** – Gute Grundstruktur mit Pipeline, Archive, Ideas, Learnings, Creator Pool
4. **schnelleinfachgesund Statuses** – Idea → Briefing → Content → Cutting → Review → Adjustments → R2L → Launched – ausgezeichneter Creative Workflow!

### 1.3 Probleme & Lücken ❌

| Problem | Details | Schwere |
|---|---|---|
| **Keine Custom Fields** | Creative Pipeline hat 0 Custom Fields – keine Filterung, kein Reporting möglich | 🔴 Kritisch |
| **Inkonsistente Statuses** | Delivery Space Default ist nur Open → In Bearbeitung → Review → Closed. Nur schnelleinfachgesund hat kreative Statuses | 🔴 Kritisch |
| **"Client Work" Catch-All** | Generische Liste mit 6 Tasks statt pro-Kunde-Struktur | 🟡 Mittel |
| **Kein Operations Space** | Finance, HR, Admin fehlt komplett | 🟡 Mittel |
| **Intern im Delivery Space** | Interne Projekte (Shopify Theme, Lead Magnet) sind unter Delivery – gehören in Operations | 🟡 Mittel |
| **Keine Templates** | Kein Onboarding-Template, kein Creative-Template | 🟡 Mittel |
| **Keine Dashboards** | Kein Überblick-Dashboard vorhanden | 🟡 Mittel |
| **Keine Automatisierungen** | Keine ClickUp-nativen oder n8n-Automationen | 🟠 Niedrig (erstmal) |

---

## 2. Notion – Analyse des "Brand Creative Ops Template"

### 2.1 Vorhandene Datenbanken

| Datenbank | Inhalt | In ClickUp übernehmen? |
|---|---|---|
| **Master Creative Database** | Kern-DB für Creatives mit Status, Type, Priority, Creator, Dates | ✅ JA – Als Creative Pipeline |
| **Content Creator Pool** | Creator mit Niche, Country, Portfolio, Contact | ✅ JA – Als Creator Pool |
| **Creator Database** | Verknüpfung Creator ↔ Concepts, Payment, Status | ✅ JA – Merge mit Creator Pool |
| **Ads Menu** | Ad-Formate (UGC, Warehouse, Midjourney, etc.) mit Industry-Tags | ✅ JA – Als Reference/Doc |
| **SOPs** | Prompt Cheatsheet, Project Handbook, AI Scriptwriting | ✅ JA – Als ClickUp Docs |
| **Shoot Schedule** | Shoot-Planung mit Creator, Type, Time | ✅ JA – Als Calendar View |
| **Storyboard** | Shot-by-Shot Planung | 🟡 Optional – eher als Task-Checkliste |
| **eCom Email Calendar** | Email-Marketing-Planung | ✅ JA – Unter Client Delivery |
| **Font Style Inspiration** | Design-Referenzen | 🟡 Optional |
| **DTC Landing Page Inspiration** | Lander-Referenzen | 🟡 Optional |
| **TikTok Organic Inspiration** | Content-Referenzen | 🟡 Optional |
| **Actor Outreach** (3x dupliziert) | Casting-Tracking | ✅ Merge zu einer Liste |

### 2.2 Master Creative Database – Detailanalyse

Die wichtigste Datenbank mit folgenden Feldern:

| Feld | Typ | Optionen | → ClickUp Custom Field |
|---|---|---|---|
| Name | Title | - | Task Name |
| Status | Status | Not started, In progress, In Review, Final Review, Pending, Approved, Cancelled | → Status-Workflow |
| Status Type | Status | Backlog, Strategy, Filming, Editing, Approved, Disapproved, Cancelled | → Separates Dropdown oder Merge |
| Concept Type | Select | Video, Static, Motion Graphics | → Dropdown CF |
| Type | Select | Net New, Iteration | → Dropdown CF |
| Priority | Select | Urgent, High, Medium, Low, None | → ClickUp Priority |
| Product | Select | Krispy, Krunch Bar, Koko, Kreme Bru | → Dropdown CF (pro Kunde) |
| Batch no. | Number | - | → Number CF |
| Concept no. | Number | - | → Number CF |
| Creator Needed? | Checkbox | - | → Checkbox CF |
| In-Person Shoot | Checkbox | - | → Checkbox CF |
| Creator(s) | Relation | → Creator DB | → Relation oder Text CF |
| Strategist | People | - | → ClickUp Assignee + Role CF |
| Editor | People | - | → ClickUp Assignee + Role CF |
| Edit Reviewer | People | - | → Reviewer CF |
| Final Reviewer | People | - | → Reviewer CF |
| Strategy Due | Date | - | → Date CF |
| Editing Start Date | Date | - | → Date CF |
| Delivery Due | Date | - | → Due Date |

**Erkenntnis:** Es gibt ZWEI Status-Felder (Status + Status Type) – das ist verwirrend. In ClickUp sollte das in EINEN Workflow konsolidiert werden.

### 2.3 SOPs (3 Dokumente)

1. **Prompt Cheatsheet** (Creative Strategy) – AI-Prompts für Scriptwriting
2. **Project Workflow & Handbook** (All) – Gesamt-Workflow-Dokumentation
3. **Using AI for Scriptwriting** (Creative Strategy) – SOP für AI-gestütztes Scripting

→ Diese sollten als ClickUp Docs im entsprechenden Space verfügbar sein.

---

## 3. Chancen & Empfehlungen

### Sofort umsetzbar (Quick Wins)
1. ✅ Custom Fields für Creative Pipeline erstellen
2. ✅ Creative Status-Workflow von schnelleinfachgesund auf Creative Testing Folder übertragen
3. ✅ "Client Work" Tasks auf individuelle Kunden-Listen verteilen
4. ✅ Notion Master Creative Database Felder als Custom Fields anlegen

### Mittelfristig
1. 📋 Operations Space für interne Projekte erstellen
2. 📋 Onboarding-Template entwickeln
3. 📋 Dashboards einrichten
4. 📋 SOPs als ClickUp Docs migrieren

### Langfristig
1. 🔄 n8n Automationen (CRM → Onboarding, Reporting)
2. 🔄 Airtable ↔ ClickUp Sync für Performance-Daten
3. 🔄 Client-facing Views/Reports
