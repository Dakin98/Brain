# Implementation Plan – Cold Email Workflow

**Datum:** 2026-02-24

---

## Workflow-Übersicht

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  1. LEADS   │ ──→ │ 2. CAMPAIGN  │ ──→ │ 3. GO LIVE  │ ──→ │ 4. MANAGE    │
│   Upload    │     │   Plan       │     │   Launch     │     │   Replies    │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
```

---

## Schritt-für-Schritt Workflow

### Step 1: Lead Upload

**User Action:** CSV-Datei mit Leads hochladen (oder Apollo-Suche starten)

**System Response:**
1. CSV wird validiert (Email-Format, Pflichtfelder vorhanden)
2. Deduplizierung gegen bestehende Leads in ClickUp
3. Leads werden in ClickUp "Leads"-Liste erstellt (Status: New)
4. Leads werden via Instantly API als Leads importiert

**Technischer Flow:**
```
User uploaded CSV
    → n8n/Make Webhook empfängt Datei
    → Validierung (Email-Regex, Pflichtfelder)
    → Dedup-Check gegen ClickUp (Email-Suche)
    → Neue Leads → ClickUp Tasks erstellen
    → Leads → Instantly API: POST /api/v2/leads
    → Confirmation an User
```

**Alternative: Apollo-Import**
```
User gibt Suchkriterien ein (Industry, Title, Location)
    → Apollo API: People Search
    → Ergebnisse anzeigen
    → User wählt aus
    → Weiter wie bei CSV
```

---

### Step 2: Campaign planen

**User Action:** Neue Campaign erstellen, Template auswählen/schreiben, Follow-ups definieren

**System Response:**
1. ClickUp Task in "Campaigns" erstellt (Status: Draft)
2. Template wird in ClickUp Docs gespeichert
3. Campaign wird in Instantly erstellt via API
4. Leads werden der Campaign zugewiesen

**Technischer Flow:**
```
User erstellt Campaign in ClickUp (oder via Chat-Command)
    → Campaign-Details erfassen (Name, Audience, Schedule)
    → Template in ClickUp Doc schreiben/auswählen
    → Instantly API: POST /api/v2/campaigns
      {
        name: "Campaign Name",
        campaign_schedule: { schedules: [{ timing, days, timezone }] },
        sequences: [{ steps: [
          { subject: "...", body: "...", delay_days: 0 },
          { subject: "...", body: "...", delay_days: 3 },
          { subject: "...", body: "...", delay_days: 7 }
        ]}]
      }
    → Instantly Campaign ID → ClickUp Custom Field speichern
    → Leads zuweisen: POST /api/v2/leads (mit campaign_id)
    → Status → "Ready for Review"
```

**Preview/Test:**
- Test-Email an eigene Adresse senden (Instantly API)
- Template-Preview in ClickUp Doc
- Checkliste vor Go-Live (siehe Step 3)

---

### Step 3: Go Live

**User Action:** Campaign freigeben (One-Click)

**System Response:**
1. Safety Checks ausführen
2. Campaign in Instantly aktivieren
3. Status-Update in ClickUp

**Safety Checks (automatisch):**
```
☐ Sending-Domain aufgewärmt? (> 2 Wochen)
☐ Daily Limit gesetzt? (≤ 50/Account)
☐ Leads > 0?
☐ Email-Accounts verbunden & healthy?
☐ Template enthält {{unsubscribe}}?
☐ Keine Duplikate in aktiven Campaigns?
☐ Test-Email gesendet & geprüft?
```

**Technischer Flow:**
```
User klickt "Launch" in ClickUp (Status → Active)
    → Automation triggered
    → Safety Checks laufen
    → Alle bestanden? 
        → Instantly API: PATCH /api/v2/campaigns/{id} { status: 1 }
        → ClickUp Status → "Active"
        → Notification: "Campaign XYZ ist live!"
    → Check failed?
        → Status bleibt "Ready for Review"
        → Notification: "Campaign blocked: [Grund]"
```

---

### Step 4: Reports & Monitoring

**Automatisch (alle 4h via Cron/Scheduled Task):**
```
Instantly API: GET /api/v2/analytics
    → Metrics abrufen (Sent, Opens, Clicks, Replies, Bounces)
    → ClickUp Custom Fields updaten (Open Rate, Reply Rate etc.)
    → Bei Anomalien: Alert
        - Bounce Rate > 5% → Campaign pausieren!
        - Open Rate < 10% → Warnung
        - Reply Rate > 15% → 🎉 Notification
```

**Dashboard in ClickUp:**
- Live-Übersicht aller aktiven Campaigns
- Weekly Digest per Automation (Montag morgens)

---

### Step 5: Reply Management

**Automatisch (via Webhook):**
```
Instantly Webhook: "reply" Event fired
    → n8n/Make empfängt Webhook
    → Reply-Text extrahieren
    → Auto-Kategorisierung:
        Keywords "interested/yes/tell me more" → Interested
        Keywords "not interested/remove/stop" → Not Interested
        Keywords "out of office/OOO/vacation" → OOO
        Keywords "wrong person/not the right" → Wrong Person
        (Optional: AI-Klassifizierung via OpenAI)
    → ClickUp Task in "Replies" erstellen
        - Lead-Relationship setzen
        - Campaign-Relationship setzen
        - Category setzen
        - Priority basierend auf Category
    → Lead-Status in ClickUp updaten
    → Notification an zuständige Person
```

**User Action bei Reply:**
1. Reply-Task öffnen
2. Reply-Text lesen
3. Category bestätigen/korrigieren
4. Antwort schreiben (direkt oder via Instantly)
5. Task → "Responded"
6. Bei Interest: Lead → "Meeting Booked"

---

## Implementierungs-Reihenfolge

### Phase 1: Foundation (1 Woche)
| # | Task | Aufwand | Abhängigkeit |
|---|------|---------|--------------|
| 1.1 | ClickUp Folder/Lists/Custom Fields anlegen | 2h | - |
| 1.2 | Instantly Account einrichten + API Key | 1h | - |
| 1.3 | n8n/Make Account einrichten | 1h | - |
| 1.4 | Sending-Domains kaufen + DNS Setup | 2h | - |
| 1.5 | Email-Accounts erstellen + Warmup starten | 2h | 1.4 |
| 1.6 | Apollo API Key einrichten | 30min | - |

### Phase 2: Core Automations (1 Woche)
| # | Task | Aufwand | Abhängigkeit |
|---|------|---------|--------------|
| 2.1 | Lead-Import Flow (CSV → ClickUp + Instantly) | 4h | Phase 1 |
| 2.2 | Campaign-Erstellung Flow (ClickUp → Instantly) | 4h | Phase 1 |
| 2.3 | Campaign-Launch Flow + Safety Checks | 3h | 2.2 |
| 2.4 | Instantly Webhooks einrichten | 2h | Phase 1 |
| 2.5 | Reply → ClickUp Automation | 4h | 2.4 |

### Phase 3: Reporting & Polish (1 Woche)
| # | Task | Aufwand | Abhängigkeit |
|---|------|---------|--------------|
| 3.1 | Metrics-Sync (Instantly → ClickUp, scheduled) | 3h | Phase 2 |
| 3.2 | ClickUp Dashboard bauen | 2h | 3.1 |
| 3.3 | Auto-Kategorisierung verfeinern (Keywords/AI) | 3h | 2.5 |
| 3.4 | Notification-Rules definieren | 1h | Phase 2 |
| 3.5 | End-to-End Test mit echten Leads | 2h | Alles |
| 3.6 | Dokumentation & Team-Training | 2h | Alles |

### Phase 4: Optimization (ongoing)
- A/B Testing von Templates
- Apollo-Integration für Lead-Sourcing direkt im Workflow
- AI-basierte Reply-Kategorisierung
- Erweiterte Analytics

---

## Aufwandsschätzung Gesamt

| Phase | Aufwand | Zeitraum |
|-------|---------|----------|
| Phase 1: Foundation | ~8h | Woche 1 |
| Phase 2: Core Automations | ~17h | Woche 1-2 |
| Phase 3: Reporting & Polish | ~13h | Woche 2-3 |
| **Gesamt** | **~38h** | **~3 Wochen** |

*Note: Warmup der Sending-Domains dauert 2-3 Wochen parallel. Erste Campaigns können in Woche 4 live gehen.*

---

## Tech Stack Zusammenfassung

```
┌─────────────┐
│   ClickUp   │ ← Workflow, CRM, Dashboard, Team-Management
└──────┬──────┘
       │ (n8n/Make)
       │
┌──────┴──────┐
│  Instantly  │ ← Email Sending, Sequences, Warmup, Deliverability
└──────┬──────┘
       │
┌──────┴──────┐
│  Apollo.io  │ ← Lead Database, Enrichment, People Search
└─────────────┘
```

**Middleware:** n8n (self-hosted, kostenlos) oder Make.com (cloud, einfacher)
**Empfehlung:** n8n für volle Kontrolle, Make für schnellen Start
