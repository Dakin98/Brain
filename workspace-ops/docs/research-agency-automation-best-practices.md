# Agentur Automatisierung - Best Practices Research

**Recherche-Datum:** Februar 2025  
**Fokus:** Performance Marketing Agentur - Skalierung & Automatisierung  
**Tech-Stack Berücksichtigung:** ClickUp, Airtable, n8n, Klaviyo, Meta Ads

---

## 1. Überblick: Was wir gelernt haben

### Die wichtigsten Erkenntnisse

Die Recherche hat gezeigt, dass erfolgreiche Agentur-Skalierung auf **vier Säulen** basiert:

1. **Systematisierung durch SOPs** - Standardisierte Prozesse als Fundament
2. **Workflow-Automatisierung** - Wiederholende Aufgaben automatisieren
3. **Passende Tech-Stack Auswahl** - Tools, die zusammenspielen
4. **Klare Handoffs & Kommunikation** - Nahtlose Übergaben zwischen Teams

### Der Unterschied: Agency Automation vs. Marketing Automation

| Agency Automation | Marketing Automation |
|-------------------|---------------------|
| Interne Prozesse (Onboarding, PM, Billing) | Externe Kampagnen (Email, Social, Ads) |
| Fokus: Effizienz & Skalierung | Fokus: Kundenbindung & Conversions |
| Tools: ClickUp, n8n, Airtable | Tools: Klaviyo, Meta Ads, Zapier |

**Kerninsicht:** Agenturen brauchen BEIDE Automatisierungstypen für nachhaltiges Wachstum.

### Die 80/20 Regel der Agentur-Automatisierung

Basierend auf der Recherche sollten Agenturen zuerst diese Prozesse automatisieren:

1. **Client Onboarding** (höchster Impact auf Kundenretention)
2. **Reporting & Analytics** (zeitaufwendig, repetitiv)
3. **Content/Asset Pipeline** (kreative Engpässe reduzieren)
4. **Campaign Management** (Fehler reduzieren, Speed erhöhen)

---

## 2. Best Practice Workflows

### 2.1 Client Onboarding Automation

#### Warum automatisieren?
- Durchschnittliche Onboarding-Zeit: 3-10 Tage manuell
- Mit Automation: 1-3 Tage
- **87% der Kunden** sagen, dass Onboarding ihre Loyalität beeinflusst

#### Der 5-Schritte Onboarding Workflow

```
SCHRITT 1: Vertragsabschluss (Automatisch)
├── Trigger: Vertrag unterzeichnet (DocuSign/PandaDoc)
├── Aktion: CRM-Status → "Contract Signed"
├── Aktion: Slack-Benachrichtigung an Account Manager
└── Aktion: Onboarding-Sequenz starten

SCHRITT 2: Daten-Erfassung (Automatisch)
├── Versand Intake-Formular (Typeform/Airtable Forms)
├── Automatische Erinnerungen nach 24h/48h
├── Daten-Validierung
└── CRM-Aktualisierung (Airtable/HubSpot)

SCHRITT 3: Account Setup (Teil-automatisch)
├── Tech-Stack Zugriffe anfordern (Leadsie/Automated)
├── Projekt in ClickUp erstellen (mit Template)
├── Kanäle/Accounts verbinden
└── Kickoff-Call scheduling (Calendly)

SCHRITT 4: Willkommens-Sequenz (Automatisch)
├── Willkommens-Email mit nächsten Schritten
├── Brand Guidelines anfordern
├── Zugang zu Client-Portal
└── Team-Vorstellungen

SCHRITT 5: Projekt-Initiierung (Manuell + Auto)
├── Internes Briefing-Meeting
├── Erste Tasks zuweisen
└── Status: "Active" in CRM
```

#### Empfohlene Tools für Onboarding

| Prozess | Tool | Integration |
|---------|------|-------------|
| Verträge | PandaDoc / DocuSign | n8n → Airtable |
| Formulare | Airtable Forms / Typeform | Direkt in Airtable |
| Zugriffsverwaltung | Leadsie | Manuelle Trigger |
| Projekt-Setup | ClickUp Templates | n8n Automation |
| Kommunikation | Slack + Email | n8n Workflows |

#### Best Practices

1. **„Manual Override" Optionen** - Bei Sonderfällen menschliche Intervention ermöglichen
2. **Personalisierte Touchpoints** - Automation sollte nicht robotisch wirken
3. **Klare Deadlines** - Jeder Schritt hat Zeitlimits (SLAs)
4. **Progress Tracking** - Kunden sehen ihren Onboarding-Status

---

### 2.2 Campaign Management Workflow

#### Der Performance Marketing Campaign Lifecycle

```
PHASE 1: Strategie & Planung (Woche 1)
├── Kickoff-Meeting mit Client
├── Zieldefinition (KPIs, Budget, Timeline)
├── Audience Research
├── Competitive Analysis
└── Deliverable: Campaign Brief

PHASE 2: Creative Production (Woche 2-3)
├── Creative Briefing
├── Asset-Erstellung
├── Review & Approval (max. 2 Runden!)
├── Asset-Datenbank aktualisieren
└── Deliverable: Creative Set

PHASE 3: Setup & Launch (Woche 3-4)
├── Account-Struktur aufsetzen
├── Kampagnen bauen
├── Tracking implementieren
├── QA & Testing
└── Go-Live

PHASE 4: Optimierung & Scale (Woche 4+)
├── Daily Monitoring (erste 7 Tage)
├── A/B Testing
├── Budget-Reallocation
├── Creative Refresh
└── Weekly Client Updates
```

#### Campaign Management Automation

**Automatisierte Checks & Alerts:**
```
IF Campaign.spend > Budget.daily * 1.2 THEN
    → Alert an Media Buyer
    → Auto-pause Option
    → Slack Notification

IF CTR < Benchmark.CTR THEN
    → Flag für Creative Review
    → Email an Creative Team
    → Task in ClickUp erstellen

IF ROAS < Target.ROAS * 0.8 THEN
    → Alert an Account Manager
    → Performance Report generieren
    → Meeting-Invite vorschlagen
```

**Meta Ads spezifisch:**
- n8n Workflow: Täglicher Daten-Pull aus Meta Ads API
- Automatische Berechnung von ROAS, CPA, Frequency
- Alert bei Anomalien (Spike/Drop)
- Auto-Report Generation

---

### 2.3 Creative Pipeline Management

#### Der „Creative Factory" Ansatz

Erfolgreiche Agenturen behandeln Content wie eine **Produktions-Pipeline**, nicht als Einzelaufgaben.

```
INTAKE → BRIEFING → PRODUCTION → REVIEW → APPROVAL → DELIVERY
```

#### Creative Workflow Stages

| Stage | Owner | Duration | Automation |
|-------|-------|----------|------------|
| Intake | Account Manager | 1 Tag | Formular → ClickUp Task |
| Briefing | Strategist | 2 Tage | Template-basiert |
| Production | Creative Team | 5-10 Tage | Status-Updates |
| Internal Review | Creative Director | 2 Tage | Approval Workflow |
| Client Review | Client | 3-5 Tage | Reminder-Sequenz |
| Revisions | Creative Team | 2-3 Tage | Task-Zuweisung |
| Final Approval | Client | 1-2 Tage | E-Signature |
| Delivery | AM/Operations | 1 Tag | Asset-Organisation |

#### Creative Pipeline Best Practices

1. **Limit Review Rounds auf 2** - Mehr kreatives Chaos, keine besseren Ergebnisse
2. **Status-Visibility** - Jeder sieht, wo Assets stehen
3. **Asset Library** - Zentralisierte Datenbank für alle Creatives
4. **Version Control** - Keine „final_final_v2" Dateien

#### Tools für Creative Pipeline

- **Figma** - Design-Kollaboration
- **Frame.io** - Video Review
- **Airtable** - Asset Management
- **ClickUp** - Task Management
- **Slack** - Schnelle Kommunikation

---

### 2.4 Reporting & Analytics Automation

#### Das Problem mit manuellem Reporting
- 5-10 Stunden pro Woche pro Client
- Fehleranfällig
- Nicht Echtzeit
- Schlechte Skalierbarkeit

#### Die Lösung: Automated Dashboards

**Self-Service Client Dashboard:**
```
┌─────────────────────────────────────────────────┐
│  Client: Brand XYZ                              │
│  Period: Last 30 Days                           │
├─────────────────────────────────────────────────┤
│                                                 │
│  KEY METRICS           │  CHANNEL BREAKDOWN    │
│  ┌──────────────┐      │  ┌─────────────────┐  │
│  │ ROAS: 4.2x   │      │  Meta Ads: 65%    │  │
│  │ ↑ 12%        │      │  Google: 25%      │  │
│  └──────────────┘      │  TikTok: 10%      │  │
│  ┌──────────────┐      │  └─────────────────┘  │
│  │ CPA: €28     │      │                       │
│  │ ↓ 8%         │      │  TREND CHART          │
│  └──────────────┘      │  [📈]                 │
│                        │                       │
├─────────────────────────────────────────────────┤
│  Auto-Update: Daily │ PDF Export │ Custom Date │
└─────────────────────────────────────────────────┘
```

#### Reporting Stack Empfehlungen

| Tool | Use Case | Preis |
|------|----------|-------|
| AgencyAnalytics | All-in-One Dashboard | ab $59/Monat |
| Swydo | Automated Reports | ab $39/Monat |
| DashThis | Multi-Channel Reports | ab $33/Monat |
| Google Looker Studio | Custom Dashboards | Kostenlos |
| n8n + Google Sheets | DIY Lösung | Kostenlos (Self-hosted) |

#### Automation Workflows für Reporting

**Wöchentlicher Report:**
```
Jeden Montag 8:00 Uhr:
├── Meta Ads API → Daten abrufen
├── Google Ads API → Daten abrufen
├── Klaviyo API → Email-Daten
├── Daten aggregieren & berechnen
├── Google Sheets aktualisieren
├── PDF Report generieren
├── Email an Client senden
└── Slack Summary an Team
```

---

## 3. Empfohlene Tools & Integrationen

### 3.1 Project Management: ClickUp vs. Monday vs. Asana

| Feature | ClickUp | Monday | Asana |
|---------|---------|--------|-------|
| **Best for** | Große Teams, komplexe Hierarchien | Visual Teams, Marketing | Einfache Prozesse, schneller Start |
| **Lernkurve** | Hoch | Mittel | Niedrig |
| **Automation** | Sehr stark | Stark | Mittel |
| **Preis** | $7-19/User | $8-16/User | $10.99-24.99/User |
| **Templates** | 1000+ | 200+ | 50+ |
| **Custom Fields** | Unbegrenzt | Stark | Limitiert |
| **Zeiterfassung** | Nativ | Integration | Integration |
| **Kundenansicht** | Gut | Sehr gut | Gut |

#### Empfehlung für Deniz

**ClickUp** ist die beste Wahl für eine Performance Marketing Agentur weil:
- Native Zeit-Tracking für Stundenabrechnung
- Starke Automation (ersetzt Zapier für viele Use-Cases)
- Tief verschachtelte Strukturen (Client → Campaign → Adsets → Ads)
- White-Label Optionen für Client-Portale
- Gute n8n-Integration

#### ClickUp Setup für Agenturen

**Empfohlene Spaces:**
```
🏢 OPERATIONS
├── HR & Recruiting
├── Finance & Billing
└── Internal Projects

👥 CLIENT DELIVERY
├── [Client A]
│   ├── Campaigns
│   ├── Reporting
│   └── Communication
├── [Client B]
│   └── ...

📊 SALES
├── Pipeline
├── Proposals
└── Onboarding

🎨 CREATIVE
├── Asset Library
├── Production Pipeline
└── Brand Guidelines
```

### 3.2 Automation: n8n vs. Zapier vs. Make

| Feature | n8n | Zapier | Make |
|---------|-----|--------|------|
| **Preis** | Kostenlos (Self-hosted) / ab $20 | ab $19.99 | ab $9 |
| **Integrationen** | 400+ (wachsend) | 8000+ | 2000+ |
| **Self-hosted** | ✅ Ja | ❌ Nein | ❌ Nein |
| **Code-Logik** | JavaScript/Python | Limitiert | Gut |
| **Data-Residency** | ✅ EU möglich | ❌ US-only | ❌ US-only |
| **Visueller Builder** | Gut | Sehr gut | Gut |
| **Error-Handling** | Stark | Mittel | Gut |

#### Warum n8n für Agenturen?

1. **Kostenlos bei Self-hosting** - Skaliert ohne Kostenexplosion
2. **Data Privacy** - GDPR-konform für EU-Kunden
3. **Für Deniz' Stack ideal:**
   - Meta Ads API direkt ansprechbar
   - ClickUp nativ integriert
   - Airtable perfekt verbunden
   - Klaviyo über API

#### Must-Have n8n Workflows für Agenturen

```yaml
# Workflow 1: Meta Ads Daten-Sync
Trigger: Schedule (Daily 6:00 AM)
Actions:
  - Meta Ads API: Get campaign insights
  - Transform: Calculate ROAS, CPA
  - Google Sheets: Append data
  - ClickUp: Update campaign status
  - Condition: IF ROAS < 2 THEN Alert

# Workflow 2: Client Onboarding
Trigger: Airtable (New Client)
Actions:
  - ClickUp: Create project structure
  - Slack: Notify team
  - Email: Send welcome sequence
  - Calendar: Schedule kickoff

# Workflow 3: Reporting
Trigger: Schedule (Weekly Monday 8:00)
Actions:
  - Collect data from all platforms
  - Generate PDF report
  - Email to client
  - Slack summary
```

### 3.3 CRM & Datenbank: Airtable

#### Warum Airtable für Agenturen?

**Relationale Datenbank-Struktur:**
```
CLIENTS
├── ID, Name, Industry, Status
├── LINKED → CAMPAIGNS
├── LINKED → CONTACTS
└── LINKED → INVOICES

CAMPAIGNS
├── ID, Client_ID, Name, Budget
├── LINKED → ADSETS
├── LINKED → CREATIVE_ASSETS
└── Rollup: Total Spend, ROAS

CREATIVE_ASSETS
├── ID, Name, Type, Status
├── LINKED → CAMPAIGNS
├── Attachments: Files
└── Review Status
```

#### Airtable für Performance Marketing

| Base | Use Case |
|------|----------|
| **Client CRM** | Kundenbeziehungen, Verträge, Kommunikation |
| **Campaign Tracker** | Alle Kampagnen, Budgets, Performance |
| **Asset Library** | Creatives, Versions, Usage Rights |
| **Content Calendar** | Social Media, Email Content |
| **Team Management** | Urlaub, Skills, Kapazitäten |

#### Airtable Automations

```
Automation 1: Status-Updates
WHEN Campaign.Status = "Live"
THEN Create ClickUp Task (Monitoring)
AND Post Slack Message
AND Update Client Record

Automation 2: Erinnerungen
WHEN Due Date = TODAY + 3 Days
THEN Send Email Reminder
AND Update Status = "Due Soon"

Automation 3: Approval Workflow
WHEN Asset.Status = "Ready for Review"
THEN Create Frame.io Review
AND Email Client
AND Set Due Date (+5 Days)
```

### 3.4 Email Marketing: Klaviyo

#### Klaviyo Flows für E-Commerce Kunden

**Must-Have Flows:**

1. **Welcome Series** (5-7 Emails)
   - Trigger: List Subscribe
   - Ziel: Onboarding, First Purchase
   - Timing: Tag 0, 1, 3, 5, 7, 14

2. **Abandoned Cart** (3 Emails)
   - Trigger: Checkout Started
   - Ziel: Conversion
   - Timing: 1h, 4h, 24h

3. **Post-Purchase** (3-5 Emails)
   - Trigger: Order Placed
   - Ziel: Loyalty, Reviews, Cross-sell
   - Timing: Immediate, 7d, 30d

4. **Win-Back** (3 Emails)
   - Trigger: 60 Days No Purchase
   - Ziel: Re-activation
   - Timing: Tag 60, 75, 90

5. **Browse Abandonment** (2 Emails)
   - Trigger: Viewed Product
   - Ziel: Conversion
   - Timing: 30min, 24h

#### Klaviyo Best Practices

- **Segmentierung:** RFM-Analyse (Recency, Frequency, Monetary)
- **Personalization:** Produkt-Recommendations
- **Testing:** A/B Testing für Subject Lines, Send-Zeiten
- **Integration:** Mit Meta Ads für Custom Audiences syncen

### 3.5 Meta Ads Management

#### Native Automation in Meta Ads Manager

**Automated Rules:**
```
Rule 1: Underperforming Ads
IF Frequency > 3 AND CTR < 1%
THEN Pause Ad
AND Notify Team

Rule 2: Budget Scaling
IF ROAS > 4 AND Spend > €500
THEN Increase Budget by 20%

Rule 3: Night Mode
IF Time = 23:00
THEN Pause All Campaigns
AND Resume at 07:00
```

#### Meta Ads + n8n Integration

**API-Use-Cases:**
- Täglicher Daten-Pull (Insights API)
- Automatische Campaign-Creation
- Asset-Upload Automation
- Audience-Sync mit CRM

---

## 4. Skalierungs-Frameworks

### 4.1 Das SOP-Framework

#### Warum SOPs kritisch sind

> „SOPs are your agency's playbook. They turn chaos into consistency." - Seven Figure Agency

**Vorteile:**
- Konsistente Qualität unabhängig vom Mitarbeiter
- Schnelleres Onboarding neuer Team-Mitglieder
- Ermöglicht Delegation ohne Qualitätsverlust
- Reduziert Fehler und Nacharbeit

#### SOP-Struktur Template

```markdown
# SOP: [Prozess-Name]

## Meta
- **Version:** 1.0
- **Owner:** [Name]
- **Last Updated:** [Datum]
- **Review Cycle:** Quartalsweise

## Ziel
[Kurze Beschreibung des Prozessziels]

## Trigger
[Wann startet dieser Prozess?]

## Schritte

### Schritt 1: [Name]
**Zeit:** X Minuten
**Owner:** [Rolle]

1. [Detaillierte Anweisung]
2. [Detaillierte Anweisung]
3. [Detaillierte Anweisung]

**Expected Output:** [Was ist das Ergebnis?]

### Schritt 2: [Name]
...

## Tools
- [Tool 1] - [Zweck]
- [Tool 2] - [Zweck]

## Templates
- [Link zu Template]

## Quality Checklist
- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

## Fehlerbehebung
| Problem | Lösung |
|---------|--------|
| X passiert | Y machen |

## Related SOPs
- [Link zu verwandtem SOP]
```

#### Top 10 SOPs für Agenturen

1. Client Onboarding
2. Campaign Setup (Meta Ads)
3. Campaign Setup (Google Ads)
4. Creative Briefing
5. Creative Review Process
6. Weekly Reporting
7. Monthly Business Review
8. Client Offboarding
9. New Employee Onboarding
10. Crisis Management (Ads Account banned, etc.)

### 4.2 Das „Systems First" Mindset

#### Die Drei Ebenen der Skalierung

```
EBENE 1: DOER (1-3 Mitarbeiter)
├── Du machst alles selbst
├── Ad-hoc Prozesse
└── Maximum: €20k/Monat

EBENE 2: MANAGER (3-10 Mitarbeiter)
├── Erste SOPs
├── Einzelne Spezialisten
├── Basic Tools
└── Maximum: €100k/Monat

EBENE 3: CEO (10+ Mitarbeiter)
├── Vollständige Systematisierung
├── Self-managing Teams
├── Integrierte Tech-Stack
└── Unlimited Scale
```

### 4.3 Die „3-3-3 Rule" für Agenturen

Von Erik Huberman (Hawke Media):

- **3 Services** - Focus auf wenige, skalierbare Services
- **3 Pricing Tiers** - Clear Packages (Starter/Growth/Enterprise)
- **3 Process Iterations** - Kontinuierliche Verbesserung

---

## 5. Konkrete Implementierungs-Tipps für Deniz

### 5.1 Priorisierung: Was zuerst?

#### Phase 1: Foundation (Monat 1-2)
- [ ] ClickUp Struktur aufbauen
- [ ] Airtable CRM einrichten
- [ ] n8n Self-hosted installieren
- [ ] Erste 5 SOPs dokumentieren

#### Phase 2: Core Automation (Monat 3-4)
- [ ] Client Onboarding automatisieren
- [ ] Meta Ads Daten-Pipeline bauen
- [ ] Reporting Automation
- [ ] Klaviyo Integration

#### Phase 3: Scale (Monat 5-6)
- [ ] Creative Pipeline optimieren
- [ ] Client Self-Service Dashboards
- [ ] Advanced n8n Workflows
- [ ] Team Handoffs automatisieren

### 5.2 Der „Quick Win" Workflow

**Sofort implementierbar (1 Tag Aufwand):**

```
Meta Ads Daily Report
├── Trigger: n8n Schedule (Daily 8:00)
├── Action: Meta Ads API → Daten abrufen
├── Action: Google Sheets → Tabelle aktualisieren
├── Action: Slack → Summary posten
└── Result: Täglicher Überblick ohne manuellen Aufwand
```

### 5.3 Tech-Stack Empfehlung für Deniz

| Kategorie | Tool | Begründung |
|-----------|------|------------|
| **Project Management** | ClickUp | Bestes Preis/Leistung, starkes Automation |
| **CRM** | Airtable | Flexibel, relational, gute PM-Integration |
| **Automation** | n8n (Self-hosted) | Kostenlos, GDPR-konform, mächtig |
| **Email Marketing** | Klaviyo | E-Commerce Standard, gute Automation |
| **Ad Management** | Meta Business Manager + n8n | Native + Custom Automation |
| **Reporting** | Google Looker Studio + n8n | Kostenlos, custom dashboards |
| **Creative** | Figma + Frame.io | Industry Standard |
| **Communication** | Slack | Integration mit allen Tools |
| **Storage** | Google Drive | Nahtlose Integration |

### 5.4 Budget-Schätzung

| Tool | Monatlich (10 User) | Jährlich |
|------|---------------------|----------|
| ClickUp Business | €119 | €1,428 |
| Airtable Pro | €179 | €2,148 |
| n8n (Self-hosted) | €0 | €0 |
| Klaviyo | €100-500* | €1,200-6,000 |
| Slack Pro | €71 | €852 |
| Figma Pro | €135 | €1,620 |
| **Total** | **€604-1,004** | **€7,248-12,048** |

*abhängig von Kontakt-Anzahl

### 5.5 Erfolgsmetriken

**Track diese KPIs für Automation-Erfolg:**

| Metrik | Vorher | Ziel (6 Monate) |
|--------|--------|-----------------|
| Client Onboarding Zeit | 7 Tage | 3 Tage |
| Reporting Zeit/Woche | 10h | 2h |
| Neue Kampagne Setup | 5h | 2h |
| Manual Data Entry | 8h/Woche | 1h/Woche |
| Client Satisfaction | 7/10 | 9/10 |
| Team Produktivität | Baseline | +40% |

---

## 6. Quellen & Referenzen

### Artikel & Guides

1. **DashClicks** - Top 11 Marketing Agency Automation Processes  
   https://www.dashclicks.com/blog/marketing-agency-automation-processes

2. **Seven Figure Agency** - How to Scale a Marketing Agency  
   https://sevenfigureagency.com/how-to-scale-a-marketing-agency-a-comprehensive-guide/

3. **Vendasta** - 15 Essential Processes Every Agency Should Automate  
   https://www.vendasta.com/blog/agency-automation/

4. **Trainual** - Creating SOPs for Your Marketing Agency  
   https://trainual.com/manual/marketing-agency-standard-operating-procedures-sops

5. **n8n** - Marketing Automation Workflows  
   https://n8n.io/workflows/categories/marketing/

6. **ClickUp** - Agency Management Templates  
   https://clickup.com/templates/agency-management-t-90100000747

7. **Leadsie** - 6 Ways Agencies Can Automate Client Onboarding  
   https://www.leadsie.com/blog/best-ways-to-automate-agency-client-onboarding

8. **Wrike** - Creative Workflow Management Guide  
   https://www.wrike.com/workflow-guide/creative-workflow-management/

9. **AgencyAnalytics** - Automated Client Reporting  
   https://agencyanalytics.com

10. **Productive.io** - Agency Workflows 101  
    https://productive.io/blog/agency-workflows/

### Tools

| Tool | URL |
|------|-----|
| ClickUp | https://clickup.com |
| n8n | https://n8n.io |
| Airtable | https://airtable.com |
| Klaviyo | https://klaviyo.com |
| AgencyAnalytics | https://agencyanalytics.com |
| PandaDoc | https://pandadoc.com |
| Leadsie | https://leadsie.com |

### Community Ressourcen

- **r/n8n** - Reddit Community für n8n Workflows
- **r/marketing** - Marketing Best Practices
- **r/agency** - Agentur-Betrieb
- **ClickUp Community** - Templates & Best Practices
- **Airtable Community** - Base Templates

---

## Appendix: Nützliche Templates & Checklisten

### Checklist: Client Onboarding Setup

- [ ] Vertrags-Automation eingerichtet
- [ ] Intake-Formular erstellt
- [ ] ClickUp Projekt-Template bereit
- [ ] Willkommens-Email-Sequenz aktiv
- [ ] Kickoff-Call Kalender verknüpft
- [ ] Zugriffs-Anforderungen definiert
- [ ] Team-Benachrichtigungen konfiguriert
- [ ] Client-Portal eingerichtet

### Checklist: Campaign Launch

- [ ] Campaign Brief vollständig
- [ ] Ziele & KPIs definiert
- [ ] Budget genehmigt
- [ ] Creatives fertig & approved
- [ ] Tracking implementiert (Pixel, UTM)
- [ ] Landing Page live & getestet
- [ ] QA durchgeführt
- [ ] Monitoring eingerichtet
- [ ] Client informiert

### Checklist: Neue Automation

- [ ] Prozess dokumentiert
- [ ] Tools & API-Zugriff geprüft
- [ ] Workflow gebaut
- [ ] Error-Handling implementiert
- [ ] Testing durchgeführt
- [ ] Fallback-Prozess definiert
- [ ] Dokumentation erstellt
- [ ] Team geschult

---

*Diese Dokumentation wurde im Februar 2025 erstellt und sollte quartalsweise auf Aktualität geprüft werden.*
