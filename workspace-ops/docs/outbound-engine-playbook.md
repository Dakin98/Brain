# 📚 Outbound Engine Playbook

## Complete Guide: Apollo + ClickUp Campaign Management

**Version:** 1.0  
**Last Updated:** 24.02.2026  
**For:** adsdrop Growth Team

---

## 🎯 QUICK START (5 Minuten)

### Dein erster Campaign in 3 Schritten:

```
1. Lead List erstellen → Apollo Search → 500 Leads
2. Sequence schreiben → 5-Step Email Flow  
3. Campaign starten → 40 Emails/Tag → Replies tracken
```

**Time to first email:** ~30 Minuten

---

## 📋 SYSTEM ÜBERSICHT

### Was wurde aufgebaut?

```
ClickUp Outbound Engine
├── 📊 Campaigns → Campaign Management & Performance
├── 👥 Lead Lists → Apollo Lead Import & Segmente  
├── 📝 Sequences → Email Templates & A/B Tests
├── 💬 Reply Management → Antworten kategorisieren
└── 🔍 Domain Health → 4 Gmail Accounts monitoren
```

### Apollo Integration

- **91.947+ CEOs/Founder** in DACH verfügbar
- **API Zugriff:** Direkte Suche nach ICP
- **Enrichment:** Emails & Firmendaten
- **Filter:** Branche, Titel, Standort, Unternehmensgröße

---

## 🚀 WORKFLOW: KOMPLETTE CAMPAIGN

### Phase 1: Lead Suche (10 Min)

#### Schritt 1.1: Lead List in ClickUp erstellen

1. Gehe zu: **Growth Space → 🚀 Outbound Engine → 👥 Lead Lists**
2. Klicke **"+ Add Task"**
3. Fülle aus:
   - **Task Name:** `🎯 [ICP] - [Monat] - [Kampagne]`
     - Beispiel: `🎯 Fashion DACH - März - Case Study`
   - **List Name:** `Fashion DACH Q1`
   - **ICP:** `Fashion DACH` (Dropdown)
   - **Source:** `Apollo`
   - **Total Leads:** (leer lassen, wird automatisch gefüllt)

#### Schritt 1.2: Apollo Lead Search ausführen

**Option A: Automatisch (Script)**

```bash
# Terminal öffnen
cd ~/.openclaw/workspace/scripts

# Lead Search starten
./apollo-lead-search.sh "[CLICKUP_TASK_ID]" "[ICP]" [ANZAHL]

# Beispiel:
./apollo-lead-search.sh "86c8e72xj" "Fashion DACH" 500
```

**Was passiert:**
- Script sucht in Apollo nach deinem ICP
- Speichert Leads als JSON
- Updated ClickUp Task mit Anzahl
- Upload Date automatisch gesetzt

**Option B: Manuell (Apollo UI)**

1. Apollo.io öffnen
2. Search → People
3. Filter setzen:
   - **Titles:** CEO, Founder, E-commerce Manager
   - **Locations:** Germany, Austria, Switzerland
   - **Industries:** Apparel & Fashion
4. "Export to CSV"
5. In ClickUp unter Lead List als Attachment hochladen

#### Schritt 1.3: Leads validieren

**Manuelle Prüfung:**

1. Öffne die JSON/CSV Datei
2. Prüfe auf:
   - ✅ Vollständige Namen
   - ✅ Gültige Unternehmen
   - ✅ Keine Duplikate
   - ✅ Relevante Titel

3. In ClickUp:
   - **Validated:** ☑️ (Checkbox)
   - **Total Leads:** [aktualisierte Anzahl]

---

### Phase 2: Sequence erstellen (20 Min)

#### Schritt 2.1: Sequence Task in ClickUp erstellen

1. Gehe zu: **🚀 Outbound Engine → 📝 Sequences**
2. Klicke **"+ Add Task"**
3. Fülle aus:
   - **Task Name:** `[Angle] - [ICP]`
     - Beispiel: `Case Study Angle - Fashion DACH`
   - **Sequence Name:** Gleich wie Task Name
   - **Steps:** `5`
   - **Target ICP:** `Fashion` (Dropdown)
   - **Status:** `Draft` → später `Testing` oder `Winner`

#### Schritt 2.2: Email Sequenz schreiben

**Template: 5-Step Sequence**

**EMAIL 1 (Tag 0) - Cold Intro:**
```
Subject: {{company}} + Meta Ads Question

Hi {{first_name}},

Saw {{company}} is scaling fast in the DACH market. 

Quick question: Are you currently testing any new creative angles for your Meta Ads?

Reason I ask: We just helped [Similar Company] increase their ROAS by 40% with a specific video hook that might work for {{company}} too.

Worth a 5-min chat?

Best,
Deniz
```

**EMAIL 2 (Tag 3) - Value Add:**
```
Subject: Re: {{company}} + Meta Ads Question

Hi {{first_name}},

Quick follow-up. 

I put together a 2-min Loom showing exactly how [Similar Company] structured their winning creative:

[VIDEO LINK]

The key insight: They stopped selling the product and started selling the transformation.

Want me to send over the full case study?

Deniz
```

**EMAIL 3 (Tag 7) - Social Proof:**
```
Subject: Case study: 40% ROAS increase

Hi {{first_name}},

Still thinking about your Meta Ads strategy.

Here's the case study I mentioned: [LINK]

Key results:
• 40% ROAS increase in 30 days
• 25% lower CAC
• 3 winning creatives identified

The best part: It worked without increasing ad spend.

Open to a quick call to see if this could work for {{company}}?

Deniz
```

**EMAIL 4 (Tag 12) - Breakup Soft:**
```
Subject: Should I close your file?

Hi {{first_name}},

I don't want to be that guy who keeps emailing if there's no interest.

Should I close your file or is Meta Ads optimization still on your radar for Q2?

Either way, all good.

Deniz
```

**EMAIL 5 (Tag 18) - Final Breakup:**
```
Subject: Last try → {{company}} growth

{{first_name}},

This is my last email.

If you're not interested in exploring how to scale {{company}}'s Meta Ads efficiently, I totally understand.

If you change your mind, just reply "interested" and I'll send over the case study.

All the best,
Deniz
```

#### Schritt 2.3: Subject Line Variants

Erstelle 3 Varianten pro Email für A/B Testing:

| Email | Variant A | Variant B | Variant C |
|-------|-----------|-----------|-----------|
| 1 | `{{company}} + Meta Ads Question` | `Quick question about {{company}}` | `Idea for {{company}}` |
| 2 | `Re: {{company}} + Meta Ads Question` | `2-min video for {{company}}` | `Creative that worked` |
| 3 | `Case study: 40% ROAS increase` | `How [Similar] scaled with Meta` | `Results from Q4` |

**In ClickUp speichern:**
- Beschreibung der Task = Vollständige Sequenz
- ODER: Link zu Google Doc mit Sequenz

---

### Phase 3: Campaign Launch (10 Min)

#### Schritt 3.1: Campaign in ClickUp erstellen

1. Gehe zu: **🚀 Outbound Engine → 📊 Campaigns**
2. Klicke **"+ Add Task"**
3. Fülle aus:
   - **Task Name:** `[ICP] - [Angle] - [Monat]`
     - Beispiel: `Fashion DACH - Case Study - März`
   - **Campaign Name:** Gleich wie Task Name
   - **ICP Segment:** `Fashion DACH` (Dropdown)
   - **Sequence:** `Case Study Angle - Fashion DACH` (verlinken)
   - **Lead Count:** [aus Lead List übernehmen]
   - **Daily Send Limit:** `40`
   - **Launch Date:** [heute + 1 Tag]
   - **Campaign Status:** `Draft`

#### Schritt 3.2: Lead List zuordnen

In der Campaign Task Beschreibung:
```
## Campaign Setup

**Lead List:** [Link zu Lead List Task]
**Sequence:** [Link zu Sequence Task]
**Target:** 500 Leads

### Schedule
- Start: [Datum]
- Daily Volume: 40 Emails
- Duration: ~13 Tage

### Notes
- [ ] Test emails sent
- [ ] Subject lines A/B tested
- [ ] Tracking pixels active
```

#### Schritt 3.3: In Apollo/Gmail importieren

**Option A: Apollo Sequences (empfohlen)**

1. Apollo.io → Sequences → Create New
2. Name: `Fashion DACH - Case Study - März`
3. Steps einfügen (Copy-Paste aus ClickUp)
4. Leads importieren:
   - Leads aus JSON/CSV kopieren
   - In Apollo → Contacts → Bulk Import
5. Sequence zu Contacts zuordnen
6. Schedule: 40/Tag
7. Launch

**Option B: Gmail + Sheets**

1. Google Sheet erstellen mit Spalten:
   - Email, First Name, Company, Sent Date, Status
2. Leads einfügen
3. Gmail → Drafts → Sequenz als Templates speichern
4. Manuell oder mit Tool (GMass, Yet Another Mail Merge) senden

#### Schritt 3.4: Campaign auf "Active" setzen

In ClickUp:
- **Campaign Status:** `Active`
- **Launch Date:** [heute]

---

### Phase 4: Reply Management (laufend)

#### Schritt 4.1: Replies kategorisieren

**Wenn Antwort kommt:**

1. Neue Task in **💬 Reply Management** erstellen:
   - **Task Name:** `📩 Reply: [Lead Name]`
   - **Lead Name:** [Name]
   - **Email:** [Email]
   - **Company:** [Firma]
   - **Campaign:** [Campaign Name]
   - **Reply Type:** (Dropdown wählen)
     - 🔥 Interested
     - ❓ Question
     - ❌ Not Interested
     - 🏖️ OOO
     - 🔗 Referral
   - **Reply Snippet:** [Erste 200 Zeichen]

2. **Wenn "Interested":**
   - Priority: 🔴 High
   - Due Date: +4 Stunden (schnelle Antwort!)
   - Kommentar: Antwortstrategie

3. **Wenn "Question":**
   - Priority: 🟡 Normal
   - Due Date: +24 Stunden
   - Kommentar: Beantworten + CTA

#### Schritt 4.2: Antworten schreiben

**Template: Interested Reply**
```
Hi {{first_name}},

Thanks for getting back to me!

I'd love to show you exactly how we achieved those results.

How's [Day] at [Time] for a quick 15-min call?
[CALENDAR LINK]

Best,
Deniz
```

**Template: Question Reply**
```
Hi {{first_name}},

Great question!

[Answer the question specifically]

Does that help? Happy to jump on a quick call to walk through it.

[CALENDAR LINK]

Deniz
```

#### Schritt 4.3: Meeting buchen

Wenn Meeting gebucht:
1. **Reply Management Task:**
   - Status: ✅ Handled
   - Meeting Date: [Datum]

2. **CRM Task erstellen** (falls nicht automatisch):
   - Gehe zu: **CRM Folder → CRM List**
   - Neuen Lead erstellen
   - Status: `Quali Call Terminiert`

---

## 📊 TRACKING & OPTIMIZATION

### Daily Check (5 Min)

Jeden Morgen:
1. **Replies checken** → Neue Antworten kategorisieren
2. **Campaign Health** → Sende-Limit erreicht?
3. **Domain Health** → Alle Accounts grün?

### Weekly Review (30 Min) - Montag 9 Uhr

**Report generieren:**
```bash
cd ~/.openclaw/workspace/scripts
./weekly-outbound-report.sh
```

**Prüfen:**
- 📊 Reply Rate pro Campaign (> 5% ist gut)
- 🔥 Anzahl "Interested" Replies
- 📅 Gebuchte Meetings
- 📉 Unterperformende Campaigns

**Actions:**
- [ ] Winner Campaigns skalieren
- [ ] Loser Campaigns pausieren/optimieren
- [ ] Neue Sequences testen

### Monthly Deep Dive (1 Stunde)

1. **Performance Analysis:**
   - Beste ICP-Segmente
   - Beste Sequences/Angles
   - Beste Subject Lines

2. **Strategic Decisions:**
   - Neue ICPs testen?
   - Neue Märkte (AT/CH)?
   - Budget-Shift?

---

## 🎯 BEST PRACTICES

### Do's ✅

- **Personalization:** Immer {{first_name}} und {{company}} nutzen
- **Subject Lines:** Curiosity > Promotion (kein "Offer", "Discount")
- **Follow-up:** Mindestens 5 Touchpoints
- **Reply Time:** < 4h für "Interested", < 24h für rest
- **A/B Testing:** Immer mindestens 2 Subject Lines testen
- **Segmentation:** Je spezifischer der ICP, desto besser die Replies

### Don'ts ❌

- **Keine Attachments** in Cold Emails (Spam-Filter)
- **Keine Links** im ersten Email (außer Calendar im Signature)
- **Keine All-Caps** oder zu viele Ausrufezeichen!!!
- **Keine Lügen** ("I saw your profile" wenn nicht wahr)
- **Keine Buchung** ohne Qualifikation

### Reply Rate Benchmarks

| Metric | Gut | Okay | Schlecht |
|--------|-----|------|----------|
| **Open Rate** | > 50% | 35-50% | < 35% |
| **Reply Rate** | > 5% | 3-5% | < 3% |
| **Meeting Rate** | > 1% | 0.5-1% | < 0.5% |
| **Positive Replies** | > 60% | 40-60% | < 40% |

**Wenn Reply Rate < 3%:**
- Subject Lines testen
- ICP überprüfen
- Timing ändern
- Angle pivoten

---

## 🛠️ TROUBLESHOOTING

### Problem: Keine Replies

**Checkliste:**
1. Subject Line zu verkaufsorientiert? → Mehr Curiosity
2. ICP zu breit? → Spezifischer filtern
3. Email zu lang? → Kürzen (< 100 Wörter)
4. Kein CTA? → Klaren nächsten Schritt definieren

### Problem: Hohe Bounce Rate

**Lösung:**
1. Leads validieren (ZeroBounce, NeverBounce)
2. Nur Apollo-verifizierte Emails nutzen
3. Domain Health checken

### Problem: Emails landen im Spam

**Checkliste:**
1. SPF/DKIM/DMARC korrekt? → Domain Health prüfen
2. Zu viele Emails/Tag? → Limit auf 40 senken
3. Trigger Words? → "Free", "Offer", "Discount" vermeiden
4. Kein Plain Text? → HTML minimieren

### Problem: Viele "Not Interested"

**Lösung:**
1. Früher Qualifizieren (Pre-qualify in Email)
2. ICP strenger definieren
3. Angle ändern (Problem → Value → Social Proof)

---

## 📋 TEMPLATES

### Campaign Setup Checklist

```
## Pre-Launch
- [ ] Lead List erstellt & validiert
- [ ] Sequence geschrieben & getestet
- [ ] Subject Lines (3 Varianten)
- [ ] Test Emails an eigene Adressen geschickt
- [ ] Tracking aktiv (Open, Click, Reply)

## Launch
- [ ] Campaign in Apollo/Gmail aktiv
- [ ] ClickUp Campaign Status: Active
- [ ] Daily Limit gesetzt (40/Tag)
- [ ] Reply Management bereit

## Post-Launch
- [ ] Daily Monitoring (erste 3 Tage)
- [ ] Weekly Report aktiviert
- [ ] CRM Integration geprüft
```

### Reply Type Decision Tree

```
Reply kommt ein
    ↓
Kategorisieren:
    ↓
🔥 Interested → Kalender-Link → Meeting buchen
    ↓
❓ Question → Antworten → CTA → Follow-up
    ↓
❌ Not Interested → Archive → 3-Monats-Nurture?
    ↓
🏖️ OOO → Warten → Reschedule in 1 Woche
    ↓
🔗 Referral → Danke sagen → Kontakt anfragen
```

---

## 🔗 WICHTIGE LINKS

### ClickUp
- **Outbound Engine:** https://app.clickup.com/901514663975
- **Campaigns:** https://app.clickup.com/901521519128
- **Lead Lists:** https://app.clickup.com/901521519130
- **Reply Management:** https://app.clickup.com/901521519132

### Tools
- **Apollo:** https://app.apollo.io
- **Gmail:** https://mail.google.com

### Scripts (lokal)
```bash
cd ~/.openclaw/workspace/scripts
./apollo-lead-search.sh      # Lead Suche
./apollo-reply-sync.sh       # Reply Import
./campaign-analytics.sh      # Performance Update
./weekly-outbound-report.sh  # Weekly Report
```

---

## ❓ FAQ

**Q: Wie viele Leads soll ich pro Woche suchen?**
A: Ziel: 200-400 neue Leads/Woche für 1 aktive Campaign

**Q: Wie lange läuft eine Campaign?**
A: 2-4 Wochen (abhängig von Lead-Anzahl & Daily Limit)

**Q: Kann ich mehrere Campaigns parallel laufen lassen?**
A: Ja, aber max. 1 pro ICP-Segment um Overlap zu vermeiden

**Q: Was ist der beste Sende-Zeitpunkt?**
A: Dienstag-Donnerstag, 8-10 Uhr (DE Zeit)

**Q: Wie handle ich "Out of Office"?**
A: In 1 Woche wieder kontaktieren, nicht sofort

**Q: Soll ich Telefonnummern anrufen?**
A: Nur nach positivem Email-Exchange oder bei Referrals

---

**Ready to launch your first campaign?** 🚀

Start with: **Lead List → Apollo Search → Sequence → Launch**

Questions? Check the troubleshooting section or iterate based on data!
