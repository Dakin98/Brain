# Cold Email Workflow – Recherche Summary

**Datum:** 2026-02-24

---

## 1. Apollo.io API – Möglichkeiten & Limits

### Verfügbare Sequence-Endpunkte
| Endpunkt | Methode | Funktion |
|----------|---------|----------|
| `/emailer_campaigns/search` | POST | Alle Sequences durchsuchen |
| `/emailer_campaigns/{id}/add_contact_ids` | POST | Contacts zu Sequence hinzufügen |
| `/emailer_campaigns/{id}/update_contact_status` | POST | Contact-Status in Sequence ändern |
| `/outreach_emails/search` | GET | Gesendete Emails durchsuchen |
| `/email_stats` | GET | Email-Statistiken abrufen |

### Contacts API
| Endpunkt | Methode | Funktion |
|----------|---------|----------|
| `/contacts` | POST | Einzelnen Contact erstellen |
| `/contacts/bulk_create` | POST | Bulk-Import von Contacts |
| `/contacts/bulk_update` | POST | Bulk-Update |
| `/contacts/search` | POST | Contacts durchsuchen |

### Wichtige Einschränkungen Apollo API
- **Keine programmatische Sequence-Erstellung!** Man kann Sequences nur suchen und Contacts hinzufügen, aber NICHT per API erstellen oder die Email-Templates definieren
- Sequences müssen in der Apollo UI erstellt werden
- Benötigt **Master API Key** für Sequence-Endpunkte (403 ohne)
- **Keine nativen Webhooks** für Replies – muss per Polling (`/outreach_emails/search`) gelöst werden
- Rate Limits gelten (Details in Apollo Docs)

### Was Apollo gut kann
- Lead-Datenbank & Enrichment (People/Organization)
- Contact Management (CRUD + Bulk)
- Contacts in bestehende Sequences pushen
- Email-Statistiken abrufen

### Was Apollo NICHT kann (per API)
- Sequences/Campaigns erstellen oder bearbeiten
- Email-Templates per API definieren
- Webhooks für Reply-Benachrichtigungen
- Granulare Campaign-Konfiguration (Timing, Throttling etc.)

---

## 2. Tool-Stack Vergleich

### Instantly.ai ⭐ EMPFEHLUNG
**API V2 (aktuell, sehr vollständig):**
- ✅ Campaigns programmatisch erstellen (Name, Schedule, Sequences/Steps)
- ✅ Leads zu Campaigns hinzufügen per API
- ✅ Campaign starten/pausieren/stoppen per API
- ✅ Webhooks für Events (Replies, Opens, Clicks etc.)
- ✅ Analytics-Endpunkte
- ✅ Subsequences für Reply-basierte Flows
- ✅ OAuth + Bearer Token Auth
- ✅ CRM-Integration (eigenes CRM-Modul)
- ✅ Unified Inbox ("Master Inbox") für alle Replies
- ✅ Zapier/Make Integration

**Preise:** Günstig, unlimited Email-Accounts ab Growth Plan

### Smartlead
**API:**
- ✅ Campaigns erstellen per API
- ✅ Webhooks (LEAD_CATEGORY_CHANGE, REPLY etc.)
- ✅ Lead Management per API
- Gut für hohe Sendevolumen
- Stärker bei technischen/API-heavy Usern
- Besseres Warmup als Instantly (laut Community)

**Nachteile:**
- UI weniger intuitiv
- Weniger polished als Instantly
- Community kleiner

### Apollo.io
**Als Sending-Tool:**
- ❌ API zu limitiert für vollautomatisierten Workflow
- ❌ Kein programmatisches Sequence-Erstellen
- ❌ Keine Webhooks

**Als Lead-Quelle:**
- ✅ Hervorragend! Beste B2B-Datenbank
- ✅ Enrichment API sehr gut
- ✅ Scraping von Leads empfohlen → dann in Instantly/Smartlead senden

### 🏆 Empfohlener Stack
```
Apollo.io (Lead-Sourcing & Enrichment)
    ↓
Instantly.ai (Sending & Campaign Management)
    ↓
ClickUp (CRM/Workflow/Reply Management)
```

**Begründung:**
- Apollo hat die besten Lead-Daten, aber schlechte Sending-API
- Instantly hat die vollständigste API für Campaigns + Webhooks
- Community-Konsens: "Apollo für Leads, dediziertes Tool zum Senden"
- Trennung schützt auch Apollo-Account (Deliverability-Risiko bei Cold Email)

---

## 3. Cold Email Best Practices

### Sequence-Struktur
- **3-5 Emails** pro Sequence (Initial + 2-4 Follow-ups)
- **Mehr als 5 Follow-ups** → diminishing returns, Spam-Risiko

### Timing-Strategie
| Step | Timing | Typ |
|------|--------|-----|
| Email 1 | Tag 1 | Initial Outreach |
| Email 2 | Tag 3-4 | Soft Follow-up |
| Email 3 | Tag 7-8 | Value Add / Case Study |
| Email 4 | Tag 14 | Break-up Email |

### Sende-Fenster
- **Mo-Fr, 10:00-18:00** Empfänger-Zeitzone
- Dienstag-Donnerstag tendenziell beste Open Rates
- Montag morgen & Freitag nachmittag vermeiden

### Personalisierung
- **Erste Zeile IMMER personalisiert** (nicht automatisiert)
- Rest kann Template sein
- Variablen: {{first_name}}, {{company}}, {{pain_point}}

### Deliverability
- Neue Domains 2-3 Wochen warmen vor dem Senden
- Max 30-50 Emails/Tag pro Account zu Beginn
- Mehrere Sending-Accounts rotieren
- Plain Text > HTML (bessere Deliverability)
- Kurze Emails (50-125 Wörter optimal)
- NICHT von der Haupt-Domain senden → Secondary Domains nutzen

### Reply-Management
- **< 2h Response Time** für positive Replies (sonst Lead kalt)
- Reply-Kategorien: Interested / Not Interested / Out of Office / Wrong Person / Unsubscribe
- Auto-Pause der Sequence bei Reply (Standard in Instantly)

### Typische Pitfalls
1. Zu viele Emails pro Tag → Domain burnt
2. Keine Warmup-Phase → Spam-Folder
3. HTML-lastige Emails → schlechte Deliverability
4. Kein Tracking wer geantwortet hat → doppelte Kontaktierung
5. Keine Deduplizierung → gleiche Person, mehrere Campaigns
6. Replies zu spät bearbeitet → Conversion sinkt drastisch

---

## 4. Webhook-Strategie (Instantly → ClickUp)

Instantly bietet Webhooks für:
- `reply` → Neuer Reply eingegangen
- `email_opened` → Email geöffnet
- `link_clicked` → Link geklickt
- `lead_status_change` → Lead-Status geändert
- `bounce` → Email gebounced
- `unsubscribe` → Abmeldung

**Flow:**
```
Instantly Webhook (Reply) 
    → Make.com/n8n Middleware 
    → ClickUp Task erstellen (Reply-List)
    → Auto-Kategorisierung (via AI oder Keywords)
    → Notification an Team
```
