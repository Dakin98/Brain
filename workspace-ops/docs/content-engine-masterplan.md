# 🎬 Content Engine Masterplan — adsdrop

> **Version:** 1.0 | **Stand:** 24.02.2026 | **Owner:** Deniz + Brain

---

## Executive Summary

adsdrop baut einen vollautomatisierten Content Engine, der aus **1 YouTube Video pro Woche** ein komplettes Multi-Channel Content-Ökosystem generiert. Ziel: **Thought Leadership im DACH Performance Marketing Space** bei minimalem Zeitaufwand (2-3h/Woche aktive Arbeit).

---

## 1. Ist-Analyse

### Was bereits steht ✅
- ClickUp Folder "🎬 Content Engine" mit 6 Listen
- Cronjob (5 Min Intervall) → `content_engine_generator.py`
- Automatische Generierung: YouTube Scripts, LinkedIn Posts, Newsletter, Shorts
- Custom Fields: Content Pillar, Target Audience, Keywords, Priority Score, Estimated Views
- SOP mit Publishing Rhythm und Review Checklisten

### Gaps & Optimierungspotenzial 🔧
| Bereich | Problem | Lösung |
|---------|---------|--------|
| **Content Qualität** | Templates sind generisch, kein Brand Voice | Brand Voice Guide + Custom Prompts |
| **Repurposing** | Shorts sind nur Timestamps, kein eigenständiger Content | Hook-Value-CTA Struktur für jeden Short |
| **Distribution** | Kein Cross-Posting Tracking | Distribution Tracker aktivieren |
| **Analytics** | Manuelle Eingabe, kein Feedback-Loop | Semi-automatisches Tracking + monatliche Reviews |
| **Ideation** | Keine systematische Pipeline | Competitor Monitoring + Audience Research |
| **SEO** | Keywords nicht datenbasiert | YouTube Search + Google Trends Integration |

---

## 2. Content Pillar Strategie

### Die 4 Säulen (überarbeitet)

| Pillar | Anteil | Ziel | Beispiel-Themen |
|--------|--------|------|-----------------|
| 🎯 **Meta Ads Mastery** | 40% | Authority & SEO | Campaign Setups, Creative Testing, Scaling Strategien, Audit Walkthroughs |
| 📊 **Case Studies & Results** | 25% | Social Proof & Trust | Client Transformations, ROAS Stories, Vorher/Nachher, Nischen-Breakdowns |
| 🏢 **Agency Building** | 20% | Relatability & Recruiting | Team Workflows, Tool Stack, Behind the Scenes, Lessons Learned |
| 🔥 **Hot Takes & Trends** | 15% | Virality & Engagement | Algorithm Updates, Industry News, Contrarian Opinions, Predictions |

### Pillar-Rotation im Monat
```
Woche 1: Meta Ads Mastery (Tutorial)
Woche 2: Case Study
Woche 3: Meta Ads Mastery (Advanced)
Woche 4: Agency Building ODER Hot Take
```

### Warum diese Verteilung?
- **40% Tutorials:** Evergreen SEO-Traffic, Hauptkanal für Discovery
- **25% Case Studies:** Conversion-stärkstes Format (→ Leads)
- **20% Agency Life:** Differenzierung, Recruiting, Community
- **15% Hot Takes:** Algorithmus liebt Engagement-Posts, bringt Reichweite

---

## 3. Weekly Publishing Rhythm

### Der "1 Video → 12 Assets" Workflow

```
1 YouTube Long-Form (SO)
├── 3 YouTube Shorts (MI, FR, SO)
├── 3 LinkedIn Posts (DI, DO, FR)
├── 1 Newsletter (DO)
├── 3 Instagram Reels (MI, FR, SO)
└── 1 Twitter/X Thread (DI)
```

### Detaillierter Wochenplan

| Tag | Content | Plattform | Zeit | Dauer Erstellung |
|-----|---------|-----------|------|-------------------|
| **MO** | Content-Idee wählen + "Claude Generate" | ClickUp | 09:00 | 15 Min |
| **MO** | Review + Anpassung aller Outputs | ClickUp | 09:15 | 30 Min |
| **DI** | LinkedIn Long-Form Post | LinkedIn | 08:00 | Scheduled |
| **DI** | Twitter Thread (Video Teaser) | X | 12:00 | Scheduled |
| **MI** | YouTube Short #1 | YT/IG/TT | 12:00 | 15 Min Edit |
| **DO** | LinkedIn Carousel / Insight Post | LinkedIn | 08:00 | Scheduled |
| **DO** | Newsletter versenden | Klaviyo | 09:00 | 10 Min Review |
| **FR** | LinkedIn Short Post / Poll | LinkedIn | 08:00 | Scheduled |
| **FR** | YouTube Short #2 + Reel | YT/IG/TT | 12:00 | 15 Min Edit |
| **SA** | YouTube Video aufnehmen + editieren | Studio | Flexibel | 2-3h |
| **SO** | YouTube Long-Form veröffentlichen | YouTube | 10:00 | 15 Min |
| **SO** | YouTube Short #3 | YT/IG/TT | 14:00 | 10 Min Edit |

**Gesamt aktive Zeit: ~4-5h/Woche** (davon 2-3h Video Production)

---

## 4. Automation Workflow

### Aktueller Flow (v1)
```
ClickUp Task (Status: "Claude Generate")
    → Cron (5 Min) erkennt Status
    → content_engine_generator.py
    → Kommentare am Task + Follow-Up Tasks
    → Manueller Review + Publish
```

### Optimierter Flow (v2 — Empfehlung)

```
Phase 1: IDEATION (automatisiert)
┌─────────────────────────────────────────┐
│ Wöchentlicher Cron (Sonntag 20:00)      │
│ → Analysiert Top-Performer der Woche    │
│ → Schlägt 3 Themen für nächste Woche vor│
│ → Erstellt Draft-Tasks in Content Ideas  │
└─────────────────────────────────────────┘

Phase 2: GENERATION (semi-automatisiert)
┌─────────────────────────────────────────┐
│ Deniz wählt Thema → "Claude Generate"   │
│ → Script mit Brand Voice Prompts        │
│ → Alle Derivate werden erstellt          │
│ → Follow-Up Tasks mit Due Dates         │
└─────────────────────────────────────────┘

Phase 3: PRODUCTION (manuell)
┌─────────────────────────────────────────┐
│ Video aufnehmen nach Script             │
│ → CapCut/Descript Edit                  │
│ → Shorts extrahieren (OpusClip/manuell) │
│ → Thumbnail in Canva                    │
└─────────────────────────────────────────┘

Phase 4: DISTRIBUTION (semi-automatisiert)
┌─────────────────────────────────────────┐
│ YouTube Upload → Schedule               │
│ → LinkedIn Posts scheduled (Buffer/nativ)│
│ → Newsletter in Klaviyo loaded          │
│ → Shorts cross-posted                   │
│ → Distribution Tracker aktualisiert     │
└─────────────────────────────────────────┘

Phase 5: ANALYTICS (wöchentlich)
┌─────────────────────────────────────────┐
│ Freitag: Wöchentlicher Performance Check│
│ → Views, Engagement, Subs, Leads       │
│ → Custom Fields in ClickUp updaten     │
│ → Learnings → nächste Woche anpassen   │
└─────────────────────────────────────────┘
```

### Script-Verbesserungen für v2

**`content_engine_generator.py` — Empfohlene Upgrades:**

1. **Brand Voice Integration:** Lade `brand-voice.md` als System-Prompt statt generischer Templates
2. **Keyword Research:** YouTube Search Suggest API einbinden für datenbasierte Titles
3. **Competitor-Aware:** Top 5 Videos zum Thema analysieren, Differentiation einbauen
4. **Performance Feedback:** Letzte 5 Videos als Context mitgeben ("mehr davon / weniger davon")
5. **Multi-Format Output:** Statt nur Text auch Canva-Template-Links und Thumbnail-Prompts

---

## 5. Plattform-Strategien

### 📺 YouTube Long-Form

**Ziel:** 1.000 Subscriber in 90 Tagen, 10.000 Views/Video in 12 Monaten

**Best Practices 2026:**
- **Qualität > Quantität:** 1 exzellentes Video/Woche schlägt 3 mittelmäßige
- **Hook in 5 Sekunden:** Pattern Interrupt, kontroverse Aussage, oder Ergebnis vorwegnehmen
- **Retention-Optimierung:** Kapitel, visuelle Wechsel alle 30s, "Coming up next"-Teaser
- **CTAs mit Mehrwert:** Statt "Subscribe" → "Ich poste jeden Sonntag neue Ads-Strategien"
- **SEO-First Titles:** Keyword vorne, Neugier hinten ("Meta Ads Creative Testing | So findest du Winner in 48h")
- **Thumbnails:** Gesicht + Emotion + max. 3 Wörter + Kontrast

**Video-Länge nach Pillar:**
- Tutorials: 8-15 Min
- Case Studies: 10-20 Min
- Agency Life: 5-10 Min (authentisch, weniger polished)
- Hot Takes: 5-8 Min

### 📱 YouTube Shorts / Reels / TikTok

**Ziel:** 10.000+ Views pro Short, Funnel zu Long-Form

**Repurposing-Strategie (Hook-Value-CTA):**
1. **Hook (0-3s):** Stärkste Aussage aus dem Video, visuell unterstützt
2. **Value Bomb (3-45s):** Ein konkreter Insight, nicht das ganze Video komprimiert
3. **CTA (45-60s):** "Full breakdown on my channel" oder "Comment [Keyword]"

**Produktions-Tipps:**
- OpusClip für automatisches Clipping, dann manuell nachbessern
- Eigene Shorts zusätzlich zu Clips (Talking Head, direkt in die Kamera)
- Dynamic Captions (CapCut Auto-Captions)
- 3 Shorts pro Video: Best Hook, Controversial Take, Quick Tip

### 💼 LinkedIn

**Ziel:** 5.000 Follower in 6 Monaten, 3%+ Engagement Rate, 5 Inbound Leads/Monat

**Algorithmus 2025/2026:**
- **Expertise > Virality:** LinkedIn belohnt Fach-Content über Entertainment
- **2-3 Posts/Woche > tägliches Posten:** Qualität wird belohnt
- **Erste 90 Minuten entscheidend:** Engagement in der Golden Hour pusht Reichweite
- **Kommentare > Likes:** Aktiv auf Kommentare antworten, selbst kommentieren

**Post-Formate (Rotation):**
1. **Long-Form Story (DI):** 800-1500 Zeichen, persönlicher Take, Learnings
2. **Carousel/Visual (DO):** Framework, Step-by-Step, Vorher/Nachher
3. **Short/Poll (FR):** Engagement-Trigger, Hot Take, Community-Frage

**LinkedIn-spezifische Regeln:**
- Erste Zeile = Hook (sichtbar im Feed)
- Leerzeilen für Lesbarkeit
- Maximal 3 Hashtags (branded: #adsdrop + 2 Nischen)
- Kein externer Link im Post (→ Kommentar)
- Persönliche Perspektive > Unternehmenssprache

### 📧 Newsletter

**Ziel:** 35%+ Open Rate, 5%+ Click Rate, 1.000 Subscriber in 6 Monaten

**Struktur (Weekly, Donnerstag 09:00):**
1. **Video der Woche** mit Key Takeaways (nicht den ganzen Content wiederholen)
2. **LinkedIn Highlight** (Best Post + Diskussion)
3. **Tool/Resource** der Woche
4. **Quick Tip** (exklusiv für Newsletter)
5. **P.S.** mit persönlicher Note oder Fun Fact

**Engagement-Taktiken:**
- Subject Line: Neugier + Nutzen, <50 Zeichen
- Preview Text optimieren
- Reply-Trigger ("Hit reply with your biggest challenge")
- Segmentierung nach Interesse (E-Com vs. Lead Gen vs. Agency Owners)

---

## 6. Success Metrics & Tracking

### KPI Dashboard (monatlich)

| Metrik | Monat 1 | Monat 3 | Monat 6 | Monat 12 |
|--------|---------|---------|---------|----------|
| **YouTube Subscribers** | 100 | 500 | 1.500 | 5.000 |
| **YouTube Views/Video** | 200 | 1.000 | 3.000 | 10.000 |
| **Shorts Views/Short** | 1.000 | 5.000 | 15.000 | 50.000 |
| **LinkedIn Followers** | 500 | 1.500 | 5.000 | 15.000 |
| **LinkedIn Engagement** | 2% | 3% | 4% | 5% |
| **Newsletter Subscribers** | 100 | 300 | 1.000 | 3.000 |
| **Newsletter Open Rate** | 40% | 38% | 35% | 35% |
| **Inbound Leads/Monat** | 1 | 3 | 8 | 20 |

### Tracking-Setup

**Wöchentlich (Freitag, 15 Min):**
- YouTube Studio → Views, Watch Time, CTR, Retention
- LinkedIn Analytics → Impressions, Engagement, Follower Growth
- Klaviyo → Open Rate, Click Rate, Unsubscribes
- → Update ClickUp Custom Fields

**Monatlich (1. des Monats, 30 Min):**
- Content Performance Review (Top 3 / Bottom 3)
- Pillar-Performance vergleichen
- Audience Feedback auswerten
- Nächsten Monat planen

**ClickUp Custom Fields für Tracking:**
- `Views (7d)` — Number
- `Engagement Rate` — Percentage
- `Lead Score` — 1-10
- `Performance` — Dropdown: 🟢 Hit / 🟡 OK / 🔴 Flop
- `Learning` — Text (was haben wir gelernt?)

---

## 7. Tool Stack (optimiert)

| Kategorie | Tool | Zweck | Kosten/Monat |
|-----------|------|-------|--------------|
| **Project Management** | ClickUp | Content Pipeline, SOPs, Tracking | Bereits vorhanden |
| **Content Generation** | Claude (Brain) | Scripts, Posts, Newsletter | Bereits vorhanden |
| **Video Recording** | OBS / iPhone | Aufnahme | Kostenlos |
| **Video Editing** | CapCut Pro | Long-Form + Shorts Edit | ~10€ |
| **Auto-Clipping** | OpusClip | Long-Form → Shorts | ~15€ |
| **Thumbnails** | Canva Pro | Thumbnails, Carousels | ~12€ |
| **Newsletter** | Klaviyo | Email Marketing | Free bis 500 |
| **Scheduling** | YouTube Studio + LinkedIn nativ | Publishing | Kostenlos |
| **Analytics** | Native Analytics + ClickUp | Tracking | Kostenlos |
| **Captions** | CapCut Auto-Captions | Shorts Untertitel | Inkl. CapCut |
| | | **Gesamt** | **~37€/Monat** |

### Nice-to-Have (später)
- **Descript** — Transkription + Text-basiertes Video Editing
- **TubeBuddy/vidIQ** — YouTube SEO & Keyword Research
- **Taplio** — LinkedIn Scheduling & Analytics
- **Beehiiv** — Newsletter Alternative mit Referral-System

---

## 8. 30-Tage Launch Plan

### Woche 1: Foundation (24.02. – 02.03.)

| Tag | Aufgabe | Verantwortlich | Status |
|-----|---------|----------------|--------|
| MO 24 | ✅ Content Engine Masterplan finalisieren | Brain | ✅ |
| MO 24 | Brand Voice Guide erstellen | Brain | ✅ |
| DI 25 | Content Calendar (4 Wochen) aufsetzen | Brain | ✅ |
| DI 25 | ClickUp Custom Fields prüfen & ergänzen | Deniz | ⬜ |
| MI 26 | Erste 4 Content Ideas in ClickUp anlegen | Deniz | ⬜ |
| DO 27 | content_engine_generator.py mit Brand Voice upgraden | Brain | ⬜ |
| FR 28 | Canva Thumbnail Templates erstellen (3 Varianten) | Deniz | ⬜ |
| SA 01 | Erstes YouTube Video aufnehmen | Deniz | ⬜ |
| SO 02 | Video editieren + Upload schedulen | Deniz | ⬜ |

### Woche 2: First Content (03.03. – 09.03.)

| Tag | Aufgabe |
|-----|---------|
| MO | Claude Generate für Woche 2 Thema triggern |
| DI | Erster LinkedIn Long-Form Post live |
| MI | Erster YouTube Short live |
| DO | Erster Newsletter versenden (auch an 10 Kontakte = OK) |
| FR | LinkedIn Poll/Short Post |
| SO | **Erstes YouTube Video live!** 🎉 |

### Woche 3: Optimize (10.03. – 16.03.)

| Tag | Aufgabe |
|-----|---------|
| MO | Woche 1 Performance reviewen, Learnings dokumentieren |
| MO | Thema Woche 3 generieren lassen |
| DI-SO | Publishing Rhythm wie Woche 2 |
| FR | LinkedIn Engagement-Strategie: 30 Min Kommentare schreiben |
| SO | YouTube Video #2 live |

### Woche 4: Scale & Systematize (17.03. – 23.03.)

| Tag | Aufgabe |
|-----|---------|
| MO | Monat 1 Recap: Was funktioniert, was nicht? |
| MO | Content Ideas für Monat 2 brainstormen (10 Themen) |
| DI-SO | Publishing Rhythm beibehalten |
| FR | Automation-Check: Läuft alles? Wo sind Bottlenecks? |
| SO | YouTube Video #3 live |
| SO | **Monat 1 KPIs dokumentieren** |

### Erfolgskriterien nach 30 Tagen
- [ ] 4 YouTube Videos veröffentlicht
- [ ] 12 LinkedIn Posts veröffentlicht
- [ ] 4 Newsletter versendet
- [ ] 9+ Shorts veröffentlicht
- [ ] Workflow läuft in <1h/Woche (ohne Video Production)
- [ ] Erste Engagement-Daten in ClickUp dokumentiert

---

## 9. Content Ideation System

### Quellen für Content Ideas (wöchentlich 15 Min scannen)

1. **YouTube Kommentare** — Fragen = Content-Ideen
2. **LinkedIn DMs & Kommentare** — Pain Points der Zielgruppe
3. **Client Conversations** — Häufige Fragen → Tutorial
4. **Competitor Channels** — Was performt? Wie können wir es besser machen?
5. **Google Trends + YouTube Search** — Suchvolumen-basierte Themen
6. **Reddit r/PPC, r/FacebookAds** — Community-Probleme
7. **Meta/Google Changelog** — Plattform-Updates als Content

### Bewertungs-Framework (Priority Score)

```
Priority Score = (Search Volume × 0.3) + (Uniqueness × 0.3) + (Lead Potential × 0.2) + (Production Ease × 0.2)

Jeder Faktor: 1-10
```

| Faktor | 1-3 (Low) | 4-6 (Medium) | 7-10 (High) |
|--------|-----------|--------------|--------------|
| Search Volume | Nischenthema | Moderate Suche | Hohes Suchvolumen |
| Uniqueness | Jeder macht es | Eigener Twist | Niemand hat es |
| Lead Potential | Awareness only | Interest | Decision-Stage |
| Production Ease | Aufwändig | Normal | Schnell machbar |

---

## 10. Skalierungs-Roadmap

### Phase 1: Solo Creator (Monat 1-3)
- Deniz macht alles + Brain automatisiert
- 1 Video/Woche
- Focus: Workflow etablieren, Qualität finden

### Phase 2: Mit Freelancer (Monat 4-6)
- Video Editor (Freelance, ~500€/Monat)
- Deniz fokussiert auf Aufnahme + LinkedIn
- 1-2 Videos/Woche möglich

### Phase 3: Mini-Team (Monat 7-12)
- Editor + Social Media Manager (Teilzeit)
- Deniz nur noch Aufnahme + Strategy
- 2 Videos/Woche, tägliches LinkedIn

### Phase 4: Content Machine (Jahr 2)
- Podcast-Format hinzufügen
- Gastbeiträge / Collaborations
- Paid Amplification der Top-Performer
- Community (Discord/Skool)

---

*Dieses Dokument wird monatlich reviewed und aktualisiert.*
