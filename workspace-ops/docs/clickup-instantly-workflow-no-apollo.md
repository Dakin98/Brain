# 🚀 ClickUp + Instantly Workflow (Ohne Apollo)

## Stack: ClickUp → Instantly → ClickUp

**Kein Apollo mehr!** Stattdessen: Manuelle Lead-Generierung oder andere Quellen.

---

## 🎯 WORKFLOW ÜBERSICHT

```
PHASE 1: LEADS
├── Quelle: LinkedIn, manuelle Recherche, oder gekaufte Listen
├── Import nach ClickUp (CSV oder manuell)
├── Qualifizierung in ClickUp
└── Status: Ready

PHASE 2: EXPORT
├── CSV Export aus ClickUp
├── Instantly-kompatibles Format
└── Upload zu Instantly

PHASE 3: CAMPAIGN
├── Campaign in Instantly erstellen
├── Sequences einrichten
├── Starten
└── ClickUp: Campaign Status = Active

PHASE 4: REPLIES
├── Instantly Inbox checken
├── Manuell in ClickUp eintragen
└── Reply Management & CRM
```

---

## 📋 CLICKUP STRUKTUR (Optimiert)

### 🚀 Outbound Engine

```
Growth Space
└── 📁 Marketing
    └── 📁 Outbound Engine
        ├── 📊 Campaigns
        ├── 👥 Lead Lists  
        ├── 💬 Reply Management
        └── 📝 Sequences (Templates)
```

---

## 1️⃣ LEAD LISTS

### Custom Fields (Minimalistisch):

| Field | Type | Zweck |
|-------|------|-------|
| **Lead Name** | Text | Voller Name |
| **First Name** | Text | Für Personalisierung |
| **Last Name** | Text | Nachname |
| **Email** | Email | Kontakt |
| **Title** | Text | Job Titel |
| **Company** | Text | Firma |
| **LinkedIn URL** | URL | Profil |
| **Source** | Dropdown | Woher der Lead kommt |
| **ICP Segment** | Dropdown | Fashion/Beauty/etc. |
| **Lead Status** | Dropdown | Workflow Status |
| **Notes** | Text | Freie Notizen |

### Lead Status Workflow:

```
New → Qualified → Ready → Exported → Contacted → Replied → Meeting → Closed
```

**Status Bedeutungen:**
- **New:** Neu importiert
- **Qualified:** Geprüft (LinkedIn, Website)
- **Ready:** Bereit für Export
- **Exported:** In Instantly hochgeladen
- **Contacted:** Erste Email gesendet
- **Replied:** Hat geantwortet
- **Meeting:** Termin gebucht
- **Closed:** Abgeschlossen (Won/Lost)
- **Bounce:** Ungültige Email

---

## 2️⃣ CAMPAIGNS

### Custom Fields:

| Field | Type | Zweck |
|-------|------|-------|
| **Campaign Name** | Text | Name |
| **ICP Segment** | Dropdown | Zielgruppe |
| **Lead Count** | Number | Anzahl Leads |
| **Daily Send Limit** | Number | z.B. 40 |
| **Launch Date** | Date | Startdatum |
| **Campaign Status** | Dropdown | Draft/Active/Paused |
| **Instantly Campaign ID** | Text | Für Tracking |
| **Reply Rate %** | Number | Performance |
| **Meeting Rate %** | Number | Performance |

### Campaign Status:
- **Draft:** In Planung
- **Ready:** Bereit zum Start
- **Active:** Läuft gerade
- **Paused:** Pausiert
- **Completed:** Beendet

---

## 3️⃣ REPLY MANAGEMENT

### Custom Fields:

| Field | Type | Zweck |
|-------|------|-------|
| **Lead Name** | Text | Name |
| **Email** | Email | Kontakt |
| **Company** | Text | Firma |
| **Campaign** | Text | Zuordnung |
| **Reply Type** | Dropdown | Kategorie |
| **Reply Snippet** | Text | Ausschnitt |
| **Meeting Date** | Date | Falls gebucht |
| **Status** | Dropdown | Bearbeitungsstatus |

### Reply Types:
- 🔥 **Interested** - Will Termin
- ❓ **Question** - Hat Fragen
- ❌ **Not Interested** - Absage
- 🏖️ **OOO** - Out of Office
- 🔗 **Referral** - Weiterleitung

### Reply Status:
- **New:** Neue Antwort
- **In Review:** Wird bearbeitet
- **Responded:** Geantwortet
- **Meeting Booked:** Termin gebucht
- **Closed:** Erledigt

---

## 🔄 KOMPLETTER WORKFLOW

### Phase 1: Lead-Generierung (Ohne Apollo)

**Option A: LinkedIn Sales Navigator**
1. LinkedIn Suche: "CEO E-Commerce Germany"
2. Profile durchgehen
3. Relevante Leads in ClickUp manuell eintragen

**Option B: Gekaufte Listen**
1. Anbieter: Lusha, ZoomInfo, etc.
2. CSV kaufen
3. In ClickUp importieren

**Option C: Manuelle Recherche**
1. Google: "Top 100 Fashion Brands Germany"
2. Websites durchgehen
3. Kontaktdaten finden

### Phase 2: Lead Import

**CSV Import zu ClickUp:**

```csv
Lead Name,First Name,Last Name,Email,Title,Company,LinkedIn URL,Source,ICP Segment
Max Mustermann,Max,Mustermann,max@company.de,CEO,Fashion Brand,https://linkedin.com/in/max,LinkedIn,Fashion DACH
```

**In ClickUp:**
- Import → CSV
- Felder mappen
- Status = "New"

### Phase 3: Qualifizierung

**Pro Lead (2 Min):**
1. LinkedIn öffnen
2. Profil prüfen
3. Website checken
4. Entscheiden:
   - ✅ Gut → Status: "Ready"
   - ❌ Schlecht → Status: "Bounce" (oder löschen)

**Ziel:** 300-500 "Ready" Leads

### Phase 4: Export zu Instantly

```bash
cd ~/.openclaw/workspace/scripts
./export-leads-instantly.sh "901521519130" "Ready"
```

**Ergebnis:** CSV Datei mit:
```csv
email,first_name,last_name,company,title,linkedin_url,lead_status,icp_segment
max@company.de,Max,Mustermann,Fashion Brand,CEO,https://...,Ready,Fashion DACH
```

### Phase 5: Instantly Upload

1. **Instantly.ai öffnen**
2. **Campaigns → Import Leads**
3. **CSV hochladen**
4. **Felder mappen:**
   - email → Email
   - first_name → First Name
   - last_name → Last Name
   - company → Company
   - title → Title

### Phase 6: Campaign erstellen

**In Instantly:**

1. **Neue Campaign:**
   - Name: "Fashion DACH - März"
   
2. **Sequences einrichten:**
   
   **Email 1:**
   ```
   Subject: {{company}} + Meta Ads Question
   
   Hi {{first_name}},
   
   Saw {{company}} is scaling fast...
   [Rest der Email]
   ```
   
   **Email 2-5:** Follow-ups

3. **Schedule:**
   - Daily Limit: 40
   - Sendezeit: 9-11 Uhr (DE Zeit)

4. **Launch!**

### Phase 7: Tracking in ClickUp

**Campaign Task aktualisieren:**
- Status: "Active"
- Launch Date: Heute
- Instantly Campaign ID: [aus Instantly kopieren]

**Leads aktualisieren:**
- Status: "Exported" → "Contacted"

### Phase 8: Reply Management

**Täglich (9 Uhr):**
1. Instantly Inbox checken
2. Neue Replies in ClickUp eintragen:
   - Task Name: "📩 Reply: [Name]"
   - Reply Type: [Kategorie]
   - Reply Snippet: [Text]

3. Antworten:
   - Interested → Kalender-Link
   - Question → Beantworten + CTA
   - Not Interested → Archive

4. **Wenn Meeting gebucht:**
   - Reply Task: Status "Meeting Booked"
   - CRM Task erstellen

---

## 🛠️ TOOLS & SCRIPTS

### Scripts:

| Script | Funktion |
|--------|----------|
| `export-leads-instantly.sh` | Exportiert "Ready" Leads als CSV |
| `weekly-outbound-report.sh` | Generiert Performance Report |

### Verwendung:

```bash
# Leads exportieren
./export-leads-instantly.sh "[LIST_ID]" "Ready"

# Oder: Alle qualifizierten
./export-leads-instantly.sh "[LIST_ID]" "Qualified"
```

---

## 📊 SUCCESS METRICS

### Campaign Level:
- **Open Rate:** > 50%
- **Reply Rate:** > 5%
- **Meeting Rate:** > 1%

### Lead Level:
- **Qualifizierungsrate:** 60-80% (von Import zu Ready)
- **Bounce Rate:** < 5%

### Operational:
- **Leads/Woche:** 200-400 neue
- **Campaigns parallel:** Max 2-3
- **Replies/Tag:** Durchschnitt 2-5

---

## ✅ CHECKLISTEN

### Pre-Launch
- [ ] 300-500 "Ready" Leads in ClickUp
- [ ] CSV Export erstellt
- [ ] Instantly Campaign eingerichtet
- [ ] Sequences geschrieben & getestet
- [ ] Test-Email an mich selbst geschickt

### Launch
- [ ] Leads in Instantly importiert
- [ ] Campaign gestartet
- [ ] ClickUp Campaign Status: Active
- [ ] Daily Limit: 40

### Post-Launch (Täglich)
- [ ] Instantly Inbox checken
- [ ] Replies in ClickUp eintragen
- [ ] Auf "Interested" antworten (< 4h)
- [ ] Meetings buchen

### Weekly Review
- [ ] Performance checken (Open/Reply Rate)
- [ ] Sequences optimieren
- [ ] Neue Leads suchen
- [ ] Report generieren

---

## 🎯 NÄCHSTE SCHRITTE

**Sofort:**
1. Lead List in ClickUp erstellen
2. Erste 10 Leads manuell eintragen (Test)
3. CSV Export testen
4. Instantly Campaign erstellen

**Diese Woche:**
5. 100 Leads qualifizieren
6. Erste Campaign launch
7. Reply Workflow testen

**Nächste Woche:**
8. Scale auf 300-500 Leads
9. Mehrere Campaigns parallel
10. Optimization basierend auf Daten

---

**Ready to launch without Apollo?** 🚀

Starte mit manueller Lead-Generierung - das gibt dir mehr Kontrolle und bessere Qualität!
