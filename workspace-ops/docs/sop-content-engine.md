# 🎬 Content Engine SOP

**Ziel:** Einmal pro Woche 15 Min investieren → Komplette Content-Woche generiert

---

## 📅 WÖCHENTLICHER WORKFLOW

### Montag 9:00 Uhr — Content-Idee wählen (15 Min)

1. **Öffne ClickUp → Growth Space → Content Engine → 💡 Content Ideas**
2. **Wähle eine Idee** aus dem Backlog (nach Priority Score sortiert)
3. **Prüfe Custom Fields:**
   - Content Pillar gesetzt?
   - Target Audience definiert?
   - Keywords vorhanden?
4. **Status ändern:** `🤖 Claude Generate`
5. **Warte bis max. 9:05 Uhr** (Cron läuft alle 5 Min)
6. **Review generierten Content** in den Kommentaren

**ODER direkt ausführen:**
```bash
python3 scripts/content_engine_generator.py --task-id "TASK_ID"
```

### Output nach Generierung

Claude erstellt automatisch:
- ✅ YouTube Script (inkl. Hook, 3-Act-Struktur, CTA)
- ✅ 3 LinkedIn Posts (Long-form, Short, Poll)
- ✅ Newsletter Draft (mit Video-Embed)
- ✅ 3 Shorts Hooks mit Timestamps
- ✅ Follow-Up Tasks in allen Pipelines

---

## ✅ REVIEW CHECKLISTE

### YouTube Script
- [ ] Hook in ersten 30 Sekunden?
- [ ] Problem → Lösung → Ergebnis Struktur?
- [ ] Persönliche Story/Example enthalten?
- [ ] CTA klar (Subscribe, Comment, Link)?
- [ ] B-Roll Momente markiert?

### LinkedIn Posts
- [ ] Long-Form: 500-1300 Wörter, persönlicher Take?
- [ ] Short: Punchy One-Liner oder kurze Story?
- [ ] Poll: Einfache Frage mit Engagement-Potential?

### Newsletter
- [ ] Subject Line unter 50 Zeichen?
- [ ] Video-Embed prominent platziert?
- [ ] LinkedIn Highlights der Woche?
- [ ] Tool Recommendation enthalten?
- [ ] P.S. mit Fun Fact?

### Shorts
- [ ] Hook unter 5 Sekunden?
- [ ] Timestamp logisch aus YouTube extrahiert?
- [ ] Caption mit CTA?

---

## 📤 PUBLISHING RHYTHM

| Tag | Plattform | Content Type | Zeit |
|-----|-----------|--------------|------|
| **DI** | LinkedIn | Long-Form Post | 8:00 Uhr |
| **MI** | YouTube Shorts | Short #1 | 12:00 Uhr |
| **DO** | LinkedIn | Carousel | 8:00 Uhr |
| **DO** | Newsletter | Weekly Digest | 9:00 Uhr |
| **FR** | LinkedIn | Short Text / Poll | 8:00 Uhr |
| **FR** | Instagram/TikTok | Short #2 | 12:00 Uhr |
| **SO** | YouTube | Long-Form Video | 10:00 Uhr |
| **SO** | YouTube Shorts | Short #3 | 14:00 Uhr |

---

## 🛠️ TROUBLESHOOTING

### Problem: Status "Claude Generate" triggert nicht

**Lösung A (Schnell):**
```bash
python3 scripts/content_engine_generator.py --task-id "TASK_ID"
```

**Lösung B (Prüfe Cron):**
```bash
# Manuell auslösen
cd ~/.openclaw/workspace && python3 scripts/content_engine_check_status.py
```

**Lösung C (Direkt generieren):**
Sag mir einfach: "Claude, generiere Content für [Thema]" → Ich erstelle Tasks direkt

### Problem: Generierter Content passt nicht zum Brand

**Fix:**
1. Kommentiere am Task was angepasst werden soll
2. Tagge mich mit "@Brain regenerate [Section]"
3. Oder: Bearbeite SOP mit Brand Guidelines → Ich lerne dazu

### Problem: Keine Content-Ideen im Backlog

**Fix:**
1. Content Brainstorming Session (30 Min)
2. Themen aus YouTube Kommentaren/LinkedIn Engagement ableiten
3. Competitor Content analysieren

---

## 🎯 SUCCESS METRICS

Tracken in ClickUp Custom Fields:

| Metric | Ziel | Tracking |
|--------|------|----------|
| YouTube Views (7d) | 1.000+ | Manuelle Eingabe nach 7 Tagen |
| LinkedIn Engagement | >3% | Manuelle Eingabe |
| Shorts Views | 10.000+ | Manuelle Eingabe |
| Newsletter Open Rate | >35% | Klaviyo → Airtable Sync |

---

## 📝 CONTENT PILLARS

**Verteilung (40/30/20/10):**

1. **Meta Ads Tutorials (40%)**
   - Deep-dives, Campaign Setups, Creative Testing
   
2. **Case Studies (30%)**
   - Before/After, ROAS Stories, Learnings
   
3. **Agency Life (20%)**
   - Behind the Scenes, Workflows, Tool Stack
   
4. **Industry Commentary (10%)**
   - Algorithm Updates, Hot Takes, Trends

---

## 🔧 TECH STACK

| Tool | Zweck |
|------|-------|
| **ClickUp** | Project Management, SOPs |
| **Claude (Brain)** | Content Generierung |
| **Cron** | Automation (alle 5 Min) |
| **CapCut/Descript** | Video Editing |
| **Canva** | Thumbnails, Carousels |
| **Klaviyo** | Newsletter Sending |
| **YouTube** | Long-form Hosting |

---

## 🚀 QUICK START

**Heute:**
1. [ ] Custom Fields in Content Ideas konfigurieren
2. [ ] Erste Idee erstellen (z.B. "5 Meta Ads Mistakes")
3. [ ] Status auf "Claude Generate" setzen
4. [ ] Output reviewen

**Diese Woche:**
1. [ ] YouTube Video aufnehmen
2. [ ] LinkedIn Posts schedulen
3. [ ] Newsletter senden

---

*Letzte Aktualisierung: 2026-02-24*  
*Verantwortlich: Deniz + Brain*
