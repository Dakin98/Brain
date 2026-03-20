# 🚀 Lean Outbound Workflow: ClickUp + Instantly

## Nur heiße Leads in ClickUp - Rest bleibt in Instantly

**Philosophie:** 
- Cold Leads = In Instantly (einfache CSV Liste)
- Hot Leads (Replies) = In ClickUp (detailliertes Tracking)

---

## 🎯 WORKFLOW

```
PHASE 1: LEAD GENERIERUNG
├── Quelle: LinkedIn, Listen, manuelle Recherche
├── Format: Einfache CSV oder Google Sheet
└── Speicherort: Temporär (nicht ClickUp)

PHASE 2: OUTREACH (Instantly)
├── CSV importieren
├── Campaign erstellen
├── Sequences einrichten
└── Launch

PHASE 3: REPLIES (ClickUp)
├── Instantly Inbox checken
├── Bei Antwort: ClickUp Task erstellen
├── Nur für Leads die antworten!
└── CRM & Follow-up in ClickUp
```

---

## 📋 CLICKUP STRUKTUR (Lean)

### Nur 3 Listen statt 5:

```
🚀 Outbound Engine (Folder)
├── 📊 Campaign Overview      ← Campaign Tracking (Meta)
├── 🔥 Hot Leads              ← NUR Leads die geantwortet haben!
└── 💬 Reply Management       ← Konversationen
```

---

## 1️⃣ CAMPAIGN OVERVIEW

**Zweck:** Übersicht aller laufenden/beendeten Campaigns

### Custom Fields:

| Field | Type | Zweck |
|-------|------|-------|
| **Campaign Name** | Text | Name |
| **ICP** | Dropdown | Zielgruppe |
| **Status** | Dropdown | Draft/Active/Completed |
| **Start Date** | Date | Launch |
| **Total Leads** | Number | Wie viele gesendet |
| **Sent Count** | Number | Wie viele Emails |
| **Replies** | Number | Anzahl Antworten |
| **Interested** | Number | Positive Replies |
| **Meetings** | Number | Gebuchte Termine |
| **Reply Rate %** | Formula | (Replies/Sent)×100 |
| **Instantly Link** | URL | Link zu Campaign |

### Keine individuellen Lead Tasks hier!

Nur **eine Task pro Campaign** als Dashboard.

---

## 2️⃣ HOT LEADS (Nur Replies!)

**Zweck:** Nur Leads die geantwortet haben

### Wann wird ein Lead hier erstellt?

**Nur wenn:**
- ✅ Antwort in Instantly eingegangen
- ✅ Lead ist relevant (nicht "unsubscribe")
- ✅ Potenzial für Deal

### Custom Fields:

| Field | Type | Zweck |
|-------|------|-------|
| **Lead Name** | Text | Name |
| **Email** | Email | Kontakt |
| **Company** | Text | Firma |
| **Title** | Text | Position |
| **Phone** | Phone | Falls bekannt |
| **LinkedIn** | URL | Profil |
| **Website** | URL | Company |
| **Source Campaign** | Text | Welche Campaign |
| **Reply Type** | Dropdown | Interested/Question/Referral |
| **Status** | Dropdown | Workflow Status |
| **Priority** | Dropdown | Hot/Warm/Cold |
| **Next Action** | Text | Was ist nächster Schritt |
| **Assigned To** | Text | Wer kümmert sich |
| **Est. Deal Value** | Number | Potenzial |
| **Notes** | Text | Komplette History |
| **Meeting Date** | Date | Falls gebucht |

### Status Workflow:

```
New Reply → Qualified → Contacted → Meeting Booked → Proposal Sent → Negotiation → Closed (Won/Lost)
```

**Status Details:**
- **New Reply:** Gerade reingekommen
- **Qualified:** Geprüft & relevant
- **Contacted:** Wir haben zurückgeschrieben
- **Meeting Booked:** Termin steht
- **Proposal Sent:** Angebot raus
- **Negotiation:** Verhandlung
- **Closed Won:** Deal! 🎉
- **Closed Lost:** Kein Deal
- **Nurture:** Später relevant

---

## 3️⃣ REPLY MANAGEMENT

**Zweck:** Temporäre Inbox für Replies

### Workflow:

1. **Reply kommt in Instantly**
2. **Schnell kategorisieren:**
   - 🔥 Interested → Hot Leads (detailliert)
   - ❓ Question → Hot Leads (detailliert)
   - ❌ Not Interested → Löschen/Archive
   - 🏖️ OOO → Wiedervorlage
   - 🔗 Referral → Hot Leads

3. **Bei Hot:** Alle Daten kopieren nach "Hot Leads"
4. **In Reply Management:** Nur als erledigt markieren

### ODER: Reply Management komplett weglassen!

**Alternative:** Direkt in "Hot Leads" erstellen, kein Zwischenschritt.

---

## 🔄 DETAIL WORKFLOW

### Phase 1: Campaign Setup (15 Min)

**In ClickUp:**
1. Campaign Overview → + Add Task
2. **Campaign Name:** "Fashion DACH - März"
3. **ICP:** Fashion DACH
4. **Status:** Draft
5. **Total Leads:** [Anzahl aus CSV]

**In Instantly:**
1. Campaign erstellen
2. Leads importieren (CSV)
3. Sequences einrichten
4. Launch

**Zurück in ClickUp:**
- Status: Active
- Start Date: Heute
- Instantly Link: [URL]

### Phase 2: Daily Monitoring (10 Min)

**In Instantly:**
1. Inbox checken
2. Neue Replies durchgehen
3. Kategorisieren

**Für jede HOT Reply:**

**In ClickUp - Hot Leads:**
1. + Add Task
2. **Task Name:** "🔥 [Name] - [Company]"
3. **Felder ausfüllen:**
   - Lead Name, Email, Company
   - Title, LinkedIn
   - Source Campaign: "Fashion DACH - März"
   - Reply Type: "Interested"
   - Status: "New Reply"
   - Priority: "Hot"
   - Notes: [Kompletter Reply-Text]

4. **Speichern**

### Phase 3: Follow-up (Ongoing)

**In ClickUp - Hot Leads:**
1. **Filter:** Status = "New Reply"
2. **Bearbeiten:**
   - LinkedIn checken
   - Antwort schreiben (in Instantly oder direkt)
   - Status: "Contacted"
   - Next Action: "Send case study"

3. **Kalender:**
   - Bei Interesse → Termin buchen
   - Status: "Meeting Booked"
   - Meeting Date: [Datum]

4. **CRM:**
   - Bei Meeting → In Haupt-CRM übertragen
   - Status: "Proposal Sent" etc.

### Phase 4: Campaign Update (Wöchentlich)

**In ClickUp - Campaign Overview:**
- Replies: [Anzahl aus Instantly]
- Interested: [Anzahl Hot Leads]
- Meetings: [Anzahl Termine]
- Reply Rate %: (Replies/Sent)×100

---

## 📊 BEISPIEL

### Tag 1: Campaign Launch

**Instantly:**
- 300 Leads importiert
- Campaign gestartet
- 40 Emails/Tag

**ClickUp - Campaign Overview:**
- Task: "📊 Fashion DACH - März"
- Status: Active
- Total Leads: 300
- Sent Count: 0
- Replies: 0

### Tag 3: Erste Replies

**Instantly Inbox:**
- 3 neue Replies
  1. Max Mustermann: "Interested!" 🔥
  2. Laura Schmidt: "How much?" ❓
  3. Hans Müller: "Not now" ❌

**ClickUp - Hot Leads:**
- Task 1: "🔥 Max Mustermann - Fashion Brand GmbH"
  - Reply Type: Interested
  - Status: New Reply
  - Priority: Hot
  
- Task 2: "🔥 Laura Schmidt - Beauty Co"
  - Reply Type: Question
  - Status: New Reply
  - Priority: Hot

**Hans Müller:** Nicht in ClickUp (nur in Instantly archiviert)

**ClickUp - Campaign Overview:**
- Sent Count: 120
- Replies: 3
- Interested: 2
- Reply Rate %: 2.5%

### Tag 5: Follow-up

**Max Mustermann:**
- Status: Contacted
- Next Action: "Send calendar link"
- Notes: "Hot lead, wants to start Q2"

**Laura Schmidt:**
- Status: Meeting Booked
- Meeting Date: 15.03.2024
- Priority: Hot

**Campaign Overview Update:**
- Meetings: 1

---

## ✅ VORTEILE dieses Workflows

### vs. Vollständiger Import (alle Leads in ClickUp)

| Aspekt | Lean (Nur Replies) | Vollständig (Alle Leads) |
|--------|-------------------|-------------------------|
| **ClickUp Tasks** | 10-50 (nur Hot) | 300-500 (alle) |
| **Übersichtlichkeit** | ⭐⭐⭐ Sehr hoch | ⭐⭐ Mittel |
| **Setup Zeit** | 5 Min | 60+ Min |
| **Qualifizierung** | Nur Hot Leads | Alle manuell |
| **Datenqualität** | Hoch (nur relevante) | Gemischt |
| **Kosten** | Niedrig | Höher (API Calls) |

### Wann Lean Workflow?
- ✅ High-volume Outreach (1000+ Leads/Monat)
- ✅ Kleines Team (nur Du)
- ✅ Fokus auf Conversion, nicht Daten
- ✅ Schneller Start wichtig

### Wann Vollständiger Import?
- Niedriges Volumen (<100 Leads/Monat)
- Großes Team (mehrere Setter)
- Lange Sales Cycles (mehr Touchpoints nötig)
- Compliance/Tracking Anforderungen

---

## 🛠️ TOOLS

### Scripts:

**Nicht mehr nötig:**
- ❌ `apollo-lead-import.sh` (kein Massen-Import)
- ❌ `export-leads-instantly.sh` (manueller Export reicht)

**Noch nützlich:**
- ✅ `weekly-outbound-report.sh` (Campaign Performance)

### Einfacher Workflow:

```
1. Leads in Excel/Google Sheet sammeln
2. CSV Export
3. In Instantly importieren
4. Campaign starten
5. Bei Replies: Manuell in ClickUp - Hot Leads eintragen
```

---

## 📋 CHECKLISTEN

### Campaign Launch
- [ ] Leads gesammelt (Excel/Sheet)
- [ ] CSV erstellt
- [ ] In Instantly importiert
- [ ] Campaign in Instantly erstellt
- [ ] ClickUp - Campaign Overview Task erstellt
- [ ] Sequences getestet
- [ ] Launch!

### Daily (10 Min)
- [ ] Instantly Inbox checken
- [ ] Neue Hot Replies in ClickUp eintragen
- [ ] Hot Leads Status aktualisieren
- [ ] Termine buchen

### Weekly
- [ ] Campaign Performance updaten
- [ ] Reply Rate berechnen
- [ ] Sequences optimieren
- [ ] Neue Leads sammeln

---

## 🚀 NÄCHSTE SCHRITTE

### Sofort:
1. ClickUp Listen anpassen (Hot Leads statt Lead Lists)
2. Erste Campaign planen
3. 50 Leads sammeln (Excel)
4. In Instantly testen

### Diese Woche:
5. Erste Campaign launch
6. Replies tracken
7. Hot Leads Workflow testen

**Ready für den Lean Workflow?** 🎯

Weniger Setup, mehr Fokus auf Conversion! 🚀
