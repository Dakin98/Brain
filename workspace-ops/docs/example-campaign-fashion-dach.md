# 🎯 Beispiel: Erste Campaign "Fashion DACH Case Study"

## Komplettes Setup von A-Z

---

## 📋 ÜBERSICHT

**Campaign Name:** Fashion DACH - Case Study - März  
**Ziel:** 10 Quali Calls buchen  
**ICP:** Fashion E-Commerce Brands in DACH (500k-5M Umsatz)  
**Titel:** CEO, Founder, E-commerce Manager  
**Zeitraum:** 4 Wochen  
**Budget:** 4 Gmail Accounts × 40 Emails/Tag = 160/Tag

---

## PHASE 1: LEAD LIST (10 Min)

### Schritt 1: ClickUp Task erstellen

**Gehe zu:** Growth Space → 🚀 Outbound Engine → 👥 Lead Lists

**Klicke:** + Add Task

**Ausfüllen:**
```
Task Name: 🎯 Fashion DACH - März - Case Study
List Name: Fashion DACH Q1
ICP: Fashion DACH (Dropdown)
Source: Apollo (Dropdown)
Total Leads: [leer lassen]
Upload Date: [leer lassen]
Validated: ☐
```

**Speichern** → Task ID kopieren (z.B. `86c8e72xj`)

### Schritt 2: Apollo Search

**Terminal öffnen:**
```bash
cd ~/.openclaw/workspace/scripts
./apollo-lead-search.sh "86c8e72xj" "Fashion DACH" 500
```

**Was passiert:**
- Script sucht in Apollo
- Findet ~500 Leads
- Speichert als JSON
- Updated ClickUp automatisch

**Ergebnis in ClickUp:**
- Total Leads: 500
- Upload Date: Heute
- Attachment: leads.json

### Schritt 3: Validierung

**JSON öffnen und prüfen:**
```bash
# Leads anzeigen
cat /tmp/leads_86c8e72xj_*.json | jq '.leads[:5]'
```

**Prüfen auf:**
- ✅ Vollständige Namen
- ✅ Relevante Unternehmen
- ✅ Keine Duplikate

**In ClickUp:**
- Validated: ☑️

---

## PHASE 2: SEQUENCE (20 Min)

### Schritt 1: Sequence Task erstellen

**Gehe zu:** 🚀 Outbound Engine → 📝 Sequences

**Klicke:** + Add Task

**Ausfüllen:**
```
Task Name: Case Study Angle - Fashion DACH
Sequence Name: Case Study Angle - Fashion DACH
Steps: 5
Target ICP: Fashion (Dropdown)
Status: Draft (Dropdown)
```

### Schritt 2: Sequence schreiben

**In Task Beschreibung einfügen:**

```markdown
## Sequence: Case Study Angle - Fashion DACH

### Subject Line Variants
1. {{company}} + Meta Ads Question
2. Quick question about {{company}}
3. Idea for {{company}}

---

### Email 1 (Day 0) - Cold Intro

Hi {{first_name}},

Saw {{company}} is scaling fast in the DACH market.

Quick question: Are you currently testing any new creative angles for your Meta Ads?

Reason I ask: We just helped MADS NØRGAARD increase their ROAS by 43% in 60 days with a specific video hook that might work for {{company}} too.

Worth a 5-min chat?

Best,
Deniz

P.S. Here's the case study if you're curious: [LINK]

---

### Email 2 (Day 3) - Value Add

Hi {{first_name}},

Quick follow-up.

I put together a 2-min Loom showing exactly how we structured the winning creative for MADS NØRGAARD:

[VIDEO LINK]

The key insight: We stopped selling the clothes and started selling the confidence boost.

Want me to send over the full strategy doc?

Deniz

---

### Email 3 (Day 7) - Social Proof

Hi {{first_name}},

Still thinking about your Meta Ads strategy.

Here's the full case study: [LINK]

Key results for MADS NØRGAARD:
• 43% ROAS increase in 60 days
• 28% lower CAC
• 4 winning creatives identified

The best part: It worked without increasing ad spend.

Open to a quick call to see if this could work for {{company}}?

Deniz

---

### Email 4 (Day 12) - Soft Breakup

Hi {{first_name}},

I don't want to be that guy who keeps emailing if there's no interest.

Should I close your file or is Meta Ads optimization still on your radar for Q2?

Either way, all good.

Deniz

---

### Email 5 (Day 18) - Final Breakup

{{first_name}},

This is my last email.

If you're not interested in exploring how to scale {{company}}'s Meta Ads efficiently, I totally understand.

If you change your mind, just reply "interested" and I'll send over the case study link.

All the best,
Deniz
```

### Schritt 3: Testen

**Test-Email an dich selbst:**
1. Erste Email kopieren
2. In Gmail → Compose
3. An deine eigene Email
4. {{first_name}} = Dein Name
5. {{company}} = Deine Firma

**Lesen als ob du der Empfänger bist:**
- Würdest du antworten?
- Ist es zu verkaufsorientiert?
- Ist der CTA klar?

**Anpassen wenn nötig**

---

## PHASE 3: CAMPAIGN (10 Min)

### Schritt 1: Campaign Task erstellen

**Gehe zu:** 🚀 Outbound Engine → 📊 Campaigns

**Klicke:** + Add Task

**Ausfüllen:**
```
Task Name: Fashion DACH - Case Study - März
Campaign Name: Fashion DACH - Case Study - März
ICP Segment: Fashion DACH (Dropdown)
Sequence: Case Study Angle - Fashion DACH (verlinken)
Lead Count: 500
Daily Send Limit: 40
Launch Date: [Morgen]
Campaign Status: Draft
```

**In Beschreibung:**
```markdown
## Campaign Setup

**Objective:** Book 10 Quali Calls
**Duration:** 4 weeks (500 Leads / 40 per day)
**Target:** Fashion E-Commerce in DACH

### Links
- Lead List: [LINK]
- Sequence: [LINK]

### Tracking
- [ ] Test emails sent
- [ ] Apollo/Gmail campaign created
- [ ] Tracking active
- [ ] Reply management ready

### Metrics
- Target Reply Rate: > 5%
- Target Meeting Rate: > 1%
```

### Schritt 2: In Apollo importieren

**Apollo.io öffnen:**

1. **Sequenzen erstellen:**
   - Sequences → Create New
   - Name: `Fashion DACH - Case Study - März`
   - Type: Email
   - Schedule: Manual

2. **Steps hinzufügen:**
   - Step 1: Copy-Paste Email 1
   - Step 2: Copy-Paste Email 2 (Day 3)
   - Step 3: Copy-Paste Email 3 (Day 7)
   - Step 4: Copy-Paste Email 4 (Day 12)
   - Step 5: Copy-Paste Email 5 (Day 18)

3. **Subject Lines:**
   - A/B Test aktivieren
   - Varianten: V1, V2, V3

4. **Leads importieren:**
   - Leads aus JSON extrahieren
   - Contacts → Import
   - CSV hochladen

5. **Zuordnen:**
   - Leads auswählen
   - "Add to Sequence"
   - Schedule: 40/Tag
   - Time: 9-10 Uhr (DE Zeit)

### Schritt 3: Launch

**In Apollo:**
- Review & Launch

**In ClickUp:**
- Campaign Status: Active
- Launch Date: Heute

---

## PHASE 4: REPLY MANAGEMENT (Ongoing)

### Scenario 1: "Interested" Reply

**Email kommt:**
```
Hi Deniz,

Thanks for reaching out! This sounds interesting.

Can we chat next week? I'm free Tuesday or Thursday afternoon.

Best,
Max
```

**In ClickUp:**
1. 💬 Reply Management → + Add Task
2. **Task Name:** `🔥 Reply: Max Mustermann`
3. **Custom Fields:**
   - Lead Name: Max Mustermann
   - Email: max@company.de
   - Company: Fashion Brand GmbH
   - Campaign: Fashion DACH - Case Study - März
   - Reply Type: Interested
   - Reply Snippet: "Thanks for reaching out! This sounds interesting..."
4. **Priority:** 🔴 High
5. **Due Date:** +4 Stunden
6. **Assign:** You

**Antwort schreiben:**
```
Hi Max,

Great to hear from you!

Tuesday 2pm or Thursday 3pm works for me. Here's my calendar:
[CALENDAR LINK]

Pick a slot that works best.

Talk soon!
Deniz
```

**Wenn Meeting gebucht:**
- Reply Task: Status → ✅ Handled
- Meeting Date: [Datum]
- CRM: Neuen Lead erstellen (Status: Quali Call Terminiert)

### Scenario 2: "Question" Reply

**Email kommt:**
```
Hi Deniz,

What exactly do you mean by "video hook"? Is this something we'd need to produce ourselves?

Max
```

**In ClickUp:**
1. Task erstellen
2. **Reply Type:** Question
3. **Priority:** 🟡 Normal
4. **Due Date:** +24 Stunden

**Antwort:**
```
Hi Max,

Great question!

By "video hook" I mean the first 3 seconds of the ad that stops the scroll. 

We can either:
1. Guide your internal team on what to produce
2. Connect you with our creative partners
3. Audit your existing creatives and identify quick wins

Happy to explain more on a quick call:
[CALENDAR LINK]

Deniz
```

### Scenario 3: "Not Interested" Reply

**Email kommt:**
```
Hi Deniz,

Thanks but we're not interested at this time.

Max
```

**In ClickUp:**
1. Task erstellen
2. **Reply Type:** Not Interested
3. **Priority:** 🟢 Low
4. **Status:** ❌ Handled

**Keine Antwort nötig** (außer bei Bedarf: "Thanks for letting me know!")

---

## 📊 EXPECTED RESULTS

### Week 1 (Launch)
- **200 Emails sent** (40/Tag × 5 Tage)
- **10 Replies** erwartet (5% Reply Rate)
- **4 Interested** (40% der Replies)
- **1-2 Meetings** gebucht

### Week 2-4 (Scale)
- **300 weitere Emails** (Rest der 500 Leads)
- **15 weitere Replies**
- **6 weitere Interested**
- **2-3 weitere Meetings**

### Total (4 Wochen)
- **500 Emails sent**
- **25 Replies** (5%)
- **10 Interested** (40%)
- **3-5 Meetings** gebucht (1-2% Meeting Rate)

**Ziel erreicht:** 10 Quali Calls ✓

---

## 🎯 OPTIMIZATION

### Wenn Reply Rate < 3%

**Am Subject Line arbeiten:**
```
❌ Schlecht: "Meta Ads Services for {{company}}"
✅ Besser: "{{company}} + Meta Ads Question"
✅ Besser: "Quick question"
✅ Besser: "Idea for {{company}}"
```

**Am Opening arbeiten:**
```
❌ Schlecht: "I'm Deniz from adsdrop..."
✅ Besser: "Saw {{company}} is scaling fast..."
```

### Wenn Meeting Rate < 0.5%

**Stärkeren CTA:**
```
❌ Schlecht: "Let me know if you're interested"
✅ Besser: "Worth a 5-min chat?"
✅ Besser: "How's Tuesday 2pm?"
```

**Mehr Social Proof:**
- Zahlen nennen (43% ROAS increase)
- Spezifische Ergebnisse
- Case Study Link

### Wenn Viele "Not Interested"

**ICP strenger filtern:**
- Min. 10 Mitarbeiter
- Max. 200 Mitarbeiter
- Nur E-Commerce (nicht Retail)
- Nur mit Online-Shop

---

## ✅ SUCCESS CHECKLIST

### Pre-Launch
- [ ] Lead List mit 500 validierten Leads
- [ ] Sequence mit 5 Steps geschrieben
- [ ] 3 Subject Line Varianten
- [ ] Test Email an mich selbst geschickt
- [ ] Apollo Campaign eingerichtet

### Launch Day
- [ ] Campaign Status: Active
- [ ] Daily Limit: 40
- [ ] Schedule: 9-10 Uhr
- [ ] Reply Management bereit

### Week 1 Review
- [ ] Open Rate > 50%?
- [ ] Reply Rate > 3%?
- [ ] Erste Replies kategorisiert?
- [ ] Meetings gebucht?

### Week 4 Review
- [ ] 500 Emails sent?
- [ ] 25+ Replies?
- [ ] 10+ Interested?
- [ ] 3-5 Meetings gebucht?
- [ ] Ziel erreicht?

---

**Ready to launch?** 🚀

Copy this example and adapt it to your first campaign!
