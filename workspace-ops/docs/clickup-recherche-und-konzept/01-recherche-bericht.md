# Recherche-Bericht: ClickUp für Performance Marketing Agenturen

## Zusammenfassung

Basierend auf umfangreicher Online-Recherche, Analyse bestehender Systeme und Branchenstandards.

---

## 1. Best Practices: ClickUp für Marketing-Agenturen

### 1.1 Empfohlene Space-Struktur (Industrie-Standard)

Zwei führende Frameworks haben sich etabliert:

**Framework A: Drei-Säulen-Modell** (ZenPilot / UpSys)
- **Growth** – Sales, Marketing, CRM
- **Delivery** – Kunden-Projekte
- **Operations** – HR, Finance, Admin

**Framework B: Hybrid-Modell** (für Performance-Agenturen optimiert)
- **Growth** – CRM, Marketing, Outbound
- **Delivery** – Kunden-Ordner mit Service-Listen
- **Creative Operations** – Eigener Space für Creative Testing
- **Operations** – Admin, Finance

**Empfehlung für adsdrop:** Framework B – Creative Testing verdient einen eigenen Fokus, da es der Kern-Wertschöpfungsprozess ist.

### 1.2 Kunden-Organisation

Best Practice ist **Folder = Kunde** im Delivery Space:
- Jeder Kunde bekommt einen eigenen Folder
- Listen im Folder = Service-Linien oder Phasen
- Beispiel: `Delivery > Green Cola > Paid Social`, `Delivery > Green Cola > Creative Production`

Quelle: ZenPilot (https://www.zenpilot.com/blog/clickup-for-agencies-guide)

### 1.3 Status-Workflows

**Standard Agency Statuses** (ZenPilot):
1. To-Do → In Progress → Internal Review → In Revision → Client Review → Blocked → Deliver & Close → Complete

**Creative Production Statuses** (Best Practice):
1. Idea → Briefing → Content/Filming → Cutting/Editing → Review → Adjustments → Ready to Launch → Launched

→ adsdrop hat bei "schnelleinfachgesund" bereits einen sehr guten Creative Workflow: Idea → Briefing → Content → Cutting → Review → Adjustments → R2L → Launched

### 1.4 Automatisierungen (Standard)

| Automation | Trigger | Aktion |
|---|---|---|
| Task-Zuweisung | Status → "Review" | Assign → Reviewer |
| Template-Apply | Neuer Folder erstellt | Template anwenden |
| Cross-List | Tag "design" | Task auch in Design-Liste |
| Deadline-Warning | 48h vor Due Date | Priority → Urgent |
| Onboarding | CRM → "Won" | Folder + Tasks erstellen (via n8n) |

### 1.5 Custom Fields (Must-Haves für Agenturen)

| Field | Typ | Zweck |
|---|---|---|
| Role | Label/Dropdown | Wer ist zuständig (Strategist, Editor, etc.) |
| Client | Dropdown | Kunden-Zuordnung |
| Service Line | Dropdown | Paid Social, Creative, etc. |
| Sprint/Batch | Number/Label | Batch-Zuordnung |
| Billable | Checkbox | Abrechenbar? |

---

## 2. Creative Testing Workflows

### 2.1 Der ideale Creative Testing Workflow

Basierend auf der Notion "Master Creative Database" und Branchenstandards:

```
Idee/Backlog → Strategy/Briefing → Filming/Content → Editing → Review → Adjustments → Ready to Launch → Launched → Testing → Winner/Loser → Archive
```

### 2.2 Custom Fields für Creatives (aus Notion-Analyse)

| Field | Typ | Optionen | Zweck |
|---|---|---|---|
| Concept Type | Dropdown | Video, Static, Motion Graphics | Art des Creatives |
| Type | Dropdown | Net New, Iteration | Neu oder Iteration |
| Priority | Dropdown | Urgent, High, Medium, Low | Priorisierung |
| Product | Dropdown | Pro Kunde konfigurierbar | Produkt-Zuordnung |
| Client | Dropdown | Alle Kunden | Kunden-Zuordnung |
| Batch No. | Number | - | Batch-Nummer |
| Creator Needed | Checkbox | - | UGC erforderlich? |
| In-Person Shoot | Checkbox | - | Vor-Ort-Dreh? |
| Strategist | People | - | Verantwortlicher Stratege |
| Editor | People | - | Verantwortlicher Editor |
| Strategy Due | Date | - | Deadline Strategie |
| Editing Start | Date | - | Editing-Beginn |
| Delivery Due | Date | - | Finale Deadline |
| Performance Score | Number | - | ROAS/CPA nach Launch |
| Hook Type | Dropdown | Problem, Question, Statement, Social Proof | Für Hook-Testing |

### 2.3 Creative Learnings System

Best Practice: Separate "Learnings" Liste/Datenbank wo gewonnene Insights dokumentiert werden:
- Was hat funktioniert? (Hook, Angle, Format)
- Was hat NICHT funktioniert?
- Quantitative Daten (CTR, ROAS, CPA)
- Qualitative Insights

→ adsdrop hat dies bereits als "Creative Learnings" Liste angelegt ✅

---

## 3. Dashboard & Reporting Best Practices

### 3.1 Dashboards pro Rolle

| Rolle | Dashboard-Inhalte |
|---|---|
| **Agency Owner** | Pipeline-Wert, Active Clients, Team Workload, Revenue KPIs |
| **Account Manager** | Client Status, Offene Tasks pro Client, Deadlines |
| **Creative Strategist** | Creative Pipeline Status, Batch Progress, Ideas Backlog |
| **Editor/Creator** | Meine Tasks, Deadlines, Review-Status |

### 3.2 KPIs für Performance Marketing Agenturen

- Anzahl aktive Creatives pro Kunde pro Monat
- Time-to-Launch (Idee bis Live)
- Win-Rate (% Creatives die skalieren)
- Creative Output pro Editor
- Client Satisfaction/Retention

### 3.3 n8n Integration Patterns

Bewährte ClickUp + n8n Automationen:
1. **Onboarding:** CRM-Won → n8n → Folder + Tasks + Google Drive erstellen
2. **Reporting:** Wöchentlich Tasks aggregieren → Report generieren → per Mail/Slack senden
3. **Airtable Sync:** Creative Performance Daten aus Airtable → ClickUp Custom Fields updaten
4. **Deadline Alerts:** Überfällige Tasks → Slack/WhatsApp Notification

---

## 4. Quellen

- ZenPilot: "ClickUp for Agencies: The Definitive Guide" – https://www.zenpilot.com/blog/clickup-for-agencies-guide
- UpSys: "Ultimate Guide to Setting Up Agency Workspace in ClickUp" – https://www.upsys-consulting.com/en/blog/clickup-agency-workspace
- ZenPilot: "The Best ClickUp Hierarchy for Agencies" – https://www.zenpilot.com/blog/the-best-clickup-hierarchy-for-agencies
- ClickUp Help: "Organize your Workspace Hierarchy for marketing teams" – https://help.clickup.com/hc/en-us/articles/9907965431191
- n8n: "ClickUp integrations" – https://n8n.io/integrations/clickup/
- Reddit r/clickup: Diverse Agentur-Strukturen und Erfahrungsberichte
- Reddit r/n8n: "Onboarding Automation with n8n and ClickUp"
