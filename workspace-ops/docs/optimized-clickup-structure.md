# Optimierte ClickUp Struktur – Cold Email Workflow

**Datum:** 2026-02-24

---

## Folder-Struktur

```
📁 Cold Email Operations
├── 📋 Campaigns          (Campaign-Management)
├── 📋 Leads              (Lead-Datenbank)
├── 📋 Replies            (Reply-Management)
└── 📋 Templates          (Email-Templates als Docs)
```

---

## 1. List: Campaigns

### Status-Flow
```
Draft → Ready for Review → Active → Paused → Completed
```

### Custom Fields (nur was nötig ist)

| Feld | Typ | Pflicht | Zweck |
|------|-----|---------|-------|
| Campaign Name | Task Name | ✅ | Identifikation |
| Instantly Campaign ID | Short Text | ✅ | Verknüpfung mit Instantly |
| Target Audience | Short Text | ✅ | z.B. "SaaS CTOs DACH" |
| Sending Domain | Dropdown | ✅ | Welche Domain wird genutzt |
| Daily Send Limit | Number | ✅ | Max Emails/Tag |
| Start Date | Date | ✅ | Geplanter Start |
| End Date | Date | ❌ | Geplantes Ende |
| Total Leads | Number | Auto | Anzahl Leads (auto-update) |
| Emails Sent | Number | Auto | Via Instantly API |
| Open Rate | Number (%) | Auto | Via Instantly API |
| Reply Rate | Number (%) | Auto | Via Instantly API |
| Positive Replies | Number | Auto | Via Kategorisierung |
| Bounce Rate | Number (%) | Auto | Via Instantly API |
| Owner | People | ✅ | Verantwortlicher |
| Notes | Long Text | ❌ | Kontext/Notizen |

### Was NICHT als Feld (im Vergleich zu typischen Over-Engineered Setups)
- ❌ Email-Templates als Custom Field → gehören in Instantly + ClickUp Docs
- ❌ Einzelne Step-Metriken → zu granular, Instantly Dashboard reicht
- ❌ Sender-Email-Adressen → werden in Instantly verwaltet
- ❌ Warmup-Status → Instantly managed das

---

## 2. List: Leads

### Status-Flow
```
New → In Sequence → Replied → Qualified → Meeting Booked → Won / Lost
```

### Custom Fields

| Feld | Typ | Pflicht | Zweck |
|------|-----|---------|-------|
| Lead Name | Task Name | ✅ | Vor- & Nachname |
| Email | Email | ✅ | Kontakt-Email |
| Company | Short Text | ✅ | Firmenname |
| Title/Role | Short Text | ✅ | Position |
| LinkedIn URL | URL | ❌ | Profil-Link |
| Campaign | Relationship | ✅ | Verknüpfung zu Campaign |
| Instantly Lead ID | Short Text | Auto | Für API-Sync |
| Source | Dropdown | ✅ | Apollo / CSV / Manual / Referral |
| Reply Category | Dropdown | Auto | Interested / Not Interested / OOO / Wrong Person |
| Last Contact Date | Date | Auto | Letzter Kontakt |
| Notes | Long Text | ❌ | Kontext zur Person |
| Phone | Phone | ❌ | Optional für Multichannel |
| Country | Short Text | ❌ | Für Segmentierung |
| Industry | Dropdown | ❌ | Branche |

### Was NICHT als Feld
- ❌ Alle Apollo-Enrichment-Daten → zu viel Noise, nur was für Outreach relevant
- ❌ Social Media Links (außer LinkedIn) → selten genutzt
- ❌ Revenue/Company Size → nur relevant wenn für Targeting, dann in Campaign-Beschreibung

---

## 3. List: Replies

### Status-Flow
```
New → In Progress → Responded → Meeting Booked → Closed
```

### Custom Fields

| Feld | Typ | Pflicht | Zweck |
|------|-----|---------|-------|
| Reply Subject | Task Name | Auto | Email-Subject |
| Lead | Relationship | ✅ | Verknüpfung zum Lead |
| Campaign | Relationship | ✅ | Aus welcher Campaign |
| Category | Dropdown | ✅ | Interested / Not Interested / OOO / Wrong Person / Unsubscribe / Question |
| Sentiment | Dropdown | Auto | Positive / Neutral / Negative (AI) |
| Reply Text | Long Text | Auto | Inhalt der Reply |
| Received At | Date | Auto | Zeitstempel |
| Response Time | Number (min) | Auto | Wie schnell geantwortet |
| Assigned To | People | ✅ | Wer bearbeitet |
| Priority | Priority | Auto | Basierend auf Category |

### Automatisierungen

1. **Neuer Reply (via Webhook):**
   - Task in Replies erstellen
   - Auto-Category setzen (Keyword-basiert oder AI)
   - Priority: Interested → Urgent, Rest → Normal
   - Notification an Owner

2. **Category = Interested:**
   - Lead-Status → "Replied"
   - Assignee bekommt Notification
   - SLA: Antwort innerhalb 2h

3. **Category = Not Interested / Unsubscribe:**
   - Lead-Status → "Lost"
   - Auto-Close nach 24h wenn keine Aktion

4. **Category = OOO:**
   - Task wird auf Wiedervorlage gesetzt (Follow-up nach OOO-Datum)

---

## 4. Templates (ClickUp Docs)

Statt Custom Fields für Templates → **ClickUp Docs** in der Templates-List:

```
📄 [Campaign-Name] - Sequence
  ├── Step 1: Initial Email
  ├── Step 2: Follow-up 1 (Tag +3)
  ├── Step 3: Follow-up 2 (Tag +7)
  └── Step 4: Break-up (Tag +14)
```

**Vorteile:**
- Versionierung
- Kollaboration (Team kann kommentieren)
- Vorschau vor dem Import in Instantly
- Templates können wiederverwendet werden

---

## 5. Dashboard (ClickUp Dashboard)

### Widgets
1. **Campaign Overview** – Tabelle aller aktiven Campaigns mit Key Metrics
2. **Reply Pipeline** – Funnel: New → In Progress → Meeting Booked
3. **Response Time Tracker** – Durchschnittliche Antwortzeit
4. **Weekly Metrics** – Sent / Opens / Replies / Meetings diese Woche
5. **Unhandled Replies** – Replies im Status "New" > 2h (Alert)

---

## Zusammenfassung: Was sich ändert

### Felder die WEG können (typische Überflüssige)
- Detaillierte Enrichment-Daten (gehören in Apollo)
- Sending-Account Details (gehören in Instantly)
- Warmup-Metriken (gehören in Instantly)
- Schritt-für-Schritt Sequence-Inhalte als Felder

### Neue sinnvolle Felder
- Instantly Campaign ID / Lead ID (für API-Sync)
- Reply Category & Sentiment (für schnelle Triage)
- Response Time (SLA-Tracking)
- Relationships zwischen Leads ↔ Campaigns ↔ Replies
- Source-Tracking (woher kam der Lead)

### Prinzip
> **ClickUp = Workflow & People Management**
> **Instantly = Email Execution & Deliverability**
> **Apollo = Lead Database & Enrichment**
> 
> Jedes Tool macht was es am besten kann. Kein Daten-Duplizieren.
