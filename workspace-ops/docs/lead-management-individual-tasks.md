# 🎯 Lead Management in ClickUp (Individual Tasks)

## Jeder Lead = Ein Task = Maximale Kontrolle

---

## 📋 WAS IST NEU?

### Vorher (JSON Attachment)
- ❌ Alle Leads in einer JSON-Datei
- ❌ Schwer zu durchsuchen
- ❌ Kein Status-Tracking pro Lead
- ❌ Keine Notizen möglich

### Jetzt (Individual Tasks)
- ✅ Jeder Lead = eigener Task
- ✅ Status pro Lead tracken
- ✅ Notizen & Kommentare
- ✅ Einfaches Filtern & Sortieren
- ✅ Direkt aus ClickUp in Apollo öffnen

---

## 🚀 WORKFLOW

### Phase 1: Lead Import (Automatisch)

```
1. Lead List Task erstellen
2. Script ausführen
3. Leads werden als einzelne Tasks importiert
```

**Schritt-für-Schritt:**

#### 1. Lead List Task erstellen

**Gehe zu:** Growth Space → 🚀 Outbound Engine → 👥 Lead Lists

**Klicke:** + Add Task

**Ausfüllen:**
```
Task Name: 🎯 Fashion DACH - März 2024
List Name: Fashion DACH Q1
ICP: Fashion DACH
Source: Apollo
Total Leads: [leer]
Validated: ☐
```

**Speichern** → Task ID kopieren (z.B. `901600000001`)

#### 2. Import Script ausführen

```bash
cd ~/.openclaw/workspace/scripts
./apollo-lead-import.sh "901600000001" "Fashion DACH" 500
```

**Was passiert:**
1. Script sucht 500 Leads in Apollo
2. Erstellt einen Folder in Lead Lists
3. Für JEDEN Lead einen Task:
   - 👤 Max Mustermann
   - 👤 Laura Schmidt
   - 👤 Jannis Weber
   - ... (500x)
4. Custom Fields gefüllt:
   - Lead Name, First Name, Last Name
   - Title, Company
   - LinkedIn URL
   - Apollo ID
   - ICP Segment
   - Email Status (available/unknown)
   - Lead Status (New)

**Dauer:** ~5-10 Minuten für 500 Leads

#### 3. Ergebnis in ClickUp

**Du siehst:**
```
👥 Lead Lists
├── 📂 Fashion DACH - 24.02.2024 (Folder)
│   ├── 👤 Max Mustermann (CEO @ Fashion Brand)
│   ├── 👤 Laura Schmidt (Founder @ Beauty Co)
│   ├── 👤 Jannis Weber (E-commerce Manager @ Home Living)
│   └── ... (497 weitere Leads)
└── 🎯 Fashion DACH - März 2024 (Parent Task)
    └── Total Leads: 500 ✓
```

---

### Phase 2: Email Enrichment

Nicht alle Leads haben sofort eine Email. Die mit `Email Status: available` können angereichert werden.

**Schritt 1: Leads mit verfügbaren Emails identifizieren**

In ClickUp:
- Filter: `Email Status` = `available`
- Oder: Board View nach Email Status gruppieren

**Schritt 2: Emails abrufen**

```bash
./apollo-enrich-leads.sh 901521519130 50
```

**Was passiert:**
- Script holt Emails von Apollo
- Updated jeden Lead Task
- Email Status: `enriched`

**Ergebnis:**
```
👤 Max Mustermann
├── Email: max@fashionbrand.de ✓
├── Email Status: enriched
└── Lead Status: New
```

---

### Phase 3: Lead Qualifizierung (Manuell)

**Jeden Lead kurz prüfen:**

1. **LinkedIn öffnen**
   - Custom Field: `LinkedIn URL` → Klicken
   - Profil prüfen

2. **Entscheiden:**
   - ✅ Gut: Lead Status → `Ready`
   - ❌ Schlecht: Lead Status → `Bounce` (oder löschen)
   - 🤔 Unsicher: Notizen hinzufügen

3. **Notizen hinzufügen:**
   ```
   Task: 👤 Max Mustermann
   Kommentar: "Aktiv auf LinkedIn, postet über E-Commerce. 
              Firmenwebsite zeigt Shopify-Store. 
              Guter Lead!"
   ```

**Filter für Ready Leads:**
```
Filter: Lead Status = Ready
Result: 350 von 500 Leads
```

---

### Phase 4: Campaign Erstellen

**Option A: Alle "Ready" Leads**

1. Filter: `Lead Status` = `Ready`
2. Alle auswählen
3. In Campaign verschieben oder exportieren

**Option B: Nur bestimmte ICPs**

1. Filter: `ICP Segment` = `Fashion DACH` + `Lead Status` = `Ready`
2. Ergebnis: Nur Fashion Leads

**Export für Apollo/Gmail:**

```bash
# CSV Export (manuell in ClickUp)
# Oder: Script-basiert
```

---

## 📊 LEAD STATUS WORKFLOW

```
New → Enriching → Ready → Contacted → Replied → Meeting → Closed
 │        │          │          │          │          │        │
 │        │          │          │          │          │        └── Deal gewonnen/verloren
 │        │          │          │          │          └── Termin gebucht
 │        │          │          │          └── Antwort erhalten
 │        │          │          └── Erste Email gesendet
 │        │          └── Qualifiziert & bereit
 │        └── Email wird abgerufen
 └── Frisch importiert
```

**Status Farben:**
- 🔘 **New** - Grau (neu importiert)
- 🟡 **Enriching** - Orange (Email wird geholt)
- 🟢 **Ready** - Grün (bereit für Outreach)
- 🔵 **Contacted** - Blau (Email gesendet)
- 🟣 **Replied** - Lila (Antwort erhalten)
- 🔴 **Meeting** - Rot (Termin gebucht)
- 🟢 **Closed** - Dunkelgrün (abgeschlossen)
- 🔴 **Bounce** - Rot (ungültige Email)

---

## 🎯 CUSTOM FIELDS REFERENZ

### Für jeden Lead verfügbar:

| Field | Type | Beschreibung |
|-------|------|--------------|
| **Lead Name** | Text | Voller Name |
| **First Name** | Text | Vorname (für Personalisierung) |
| **Last Name** | Text | Nachname |
| **Title** | Text | Job Titel |
| **Company** | Text | Firmenname |
| **Email** | Email | Email Adresse |
| **LinkedIn URL** | URL | LinkedIn Profil |
| **Apollo ID** | Text | Apollo.io ID |
| **ICP Segment** | Dropdown | Fashion/Beauty/Home/Food |
| **Email Status** | Dropdown | unknown/available/enriched/verified/bounce |
| **Lead Status** | Dropdown | New/Enriching/Ready/Contacted/Replied/Meeting/Closed/Bounce |
| **Notes** | Text | Freie Notizen |

---

## 🔍 FILTER & VIEWS

### Nützliche Filter:

**1. Bereit für Outreach:**
```
Lead Status = Ready
Email Status = enriched
```

**2. Hohe Priorität (C-Level):**
```
Title contains: CEO OR Founder OR Geschäftsführer
Lead Status = Ready
```

**3. Nur Fashion:**
```
ICP Segment = Fashion DACH
Lead Status = Ready
```

**4. Mit LinkedIn:**
```
LinkedIn URL is not empty
```

**5. Keine Email:**
```
Email Status = unknown
```

### Empfohlene Views:

**Board View (nach Status):**
```
Spalten: New | Ready | Contacted | Replied | Meeting | Closed
```

**Table View (alle Details):**
```
Spalten: Name | Company | Title | Email | Status | ICP | Actions
```

**List View (einfach):**
```
Nur: Name | Company | Status
```

---

## 🛠️ COMMANDS

### Lead Import
```bash
# Neue Leads suchen & importieren
./apollo-lead-import.sh "[PARENT_TASK_ID]" "[ICP]" [COUNT]

# Beispiel
./apollo-lead-import.sh "901600000001" "Fashion DACH" 500
```

### Email Enrichment
```bash
# Emails für "available" Leads abrufen
./apollo-enrich-leads.sh [LIST_ID] [LIMIT]

# Beispiel: Max 50 Leads
./apollo-enrich-leads.sh 901521519130 50
```

### Quick Test
```bash
# Apollo API testen
./apollo-quick-test.sh
```

---

## 💡 BEST PRACTICES

### Import
- **Max 500 Leads** pro Import (Rate Limiting)
- **Ein ICP** pro Import (besser organisiert)
- **Sofort validieren** (Nach Import 30 Min Review)

### Enrichment
- **Batchweise** (50 Leads pro Run)
- **Nur "available"** (nicht alle Leads haben Emails)
- **Status checken** (nicht alle Enrichments funktionieren)

### Qualifizierung
- **LinkedIn checken** (immer!)
- **Firmenwebsite prüfen** (E-Commerce? Shopify?)
- **Notizen machen** (für spätere Referenz)
- **Schlechte Leads löschen** (nicht auf "Bounce" lassen)

### Organization
- **Folder pro Import** (gut für Overview)
- **Parent Task** behalten (für Summary)
- **Tags nutzen** (z.B. "High Priority", "Follow Up")

---

## 🚨 TROUBLESHOOTING

### Zu viele Leads ohne Email

**Problem:** 80% haben `Email Status: unknown`

**Lösung:**
- Apollo Credits prüfen
- Anderer ICP testen (größere Firmen haben mehr Daten)
- Manuelle Recherche (LinkedIn → Website → Email)

### Import ist langsam

**Normal:** ~10 Sekunden pro Lead (API Rate Limits)

**500 Leads = ~5-10 Minuten**

**Nicht unterbrechen!**

### Leads sind nicht relevant

**Lösung:**
- ICP strenger definieren
- Apollo Filter anpassen
- Nach Import filtern & löschen

### Duplikate

**Prävention:**
- Importiert in neuen Folder
- Vorher prüfen: "Max Mustermann" existiert bereits?

**Lösung:**
- Manuelle Duplikate löschen
- Oder: Script anpassen für Deduplication

---

## 📈 WORKFLOW ZUSAMMENFASSUNG

```
1. LEAD LIST TASK erstellen (2 Min)
   ↓
2. IMPORT SCRIPT ausführen (5-10 Min)
   → 500 individuelle Lead Tasks
   ↓
3. EMAIL ENRICHMENT (3-5 Min)
   → Emails abrufen
   ↓
4. QUALIFIZIERUNG (30 Min)
   → LinkedIn checken
   → Status: Ready setzen
   → Notizen hinzufügen
   ↓
5. CAMPAIGN erstellen
   → "Ready" Leads exportieren
   → In Apollo/Gmail importieren
   → Outreach starten
   ↓
6. TRACKING
   → Lead Status aktualisieren (Contacted → Replied → Meeting)
   → Notizen zu Antworten
   → Meetings in CRM übertragen
```

**Gesamtzeit für Setup:** ~45 Minuten  
**Ergebnis:** 500 qualifizierte Leads als individuelle Tasks

---

## 🎯 NÄCHSTE SCHRITTE

**Bereit für deinen ersten Import?**

1. Lead List Task in ClickUp erstellen
2. Script ausführen:
   ```bash
   ./apollo-lead-import.sh "[TASK_ID]" "Fashion DACH" 100
   ```
3. Ergebnis in ClickUp prüfen
4. Emails enrich:
   ```bash
   ./apollo-enrich-leads.sh
   ```
5. Leads qualifizieren (Status: Ready)
6. Campaign erstellen!

---

**Fragen?** Check das Outbound Engine Playbook oder frage mich! 🚀
