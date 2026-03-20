#!/usr/bin/env python3
"""
Create ClickUp Docs and Template Tasks for Content Engine SOPs
"""

import os
import json
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta

CLICKUP_BASE = "https://api.clickup.com/api/v2"

# IDs
WORKSPACE_ID = "9006104573"
SPACE_ID = "90040244466"
FOLDER_CONTENT_ENGINE = "901514665491"
LIST_CONTENT_IDEAS = "901521521000"
LIST_YOUTUBE = "901521521003"
LIST_SHORTS = "901521521005"
LIST_LINKEDIN = "901521521006"
LIST_NEWSLETTER = "901521521007"
LIST_DISTRIBUTION = "901521521009"

def get_api_token():
    config_path = os.path.expanduser("~/.config/clickup/api_token")
    with open(config_path) as f:
        return f.read().strip()

def clickup_request(method, endpoint, data=None):
    headers = {
        "Authorization": get_api_token(),
        "Content-Type": "application/json"
    }
    url = f"{CLICKUP_BASE}{endpoint}"
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  ⚠️ Error {e.code}: {e.read().decode()[:200]}")
        return None

def create_doc(workspace_id, name, content, parent_id=None):
    """Create a ClickUp Doc"""
    data = {
        "name": name,
        "content": content,
        "parent": {"id": parent_id, "type": 5} if parent_id else None  # 5 = folder
    }
    return clickup_request("POST", f"/workspaces/{workspace_id}/docs", data)

def create_task(list_id, name, description, due_date=None, tags=None, checklist=None):
    """Create a task with optional checklist"""
    data = {
        "name": name,
        "description": description,
        "status": "to do"
    }
    if due_date:
        data["due_date"] = int(due_date.timestamp() * 1000)
    if tags:
        data["tags"] = tags
    
    result = clickup_request("POST", f"/list/{list_id}/task", data)
    
    # Add checklist if provided
    if result and checklist:
        task_id = result["id"]
        checklist_data = {
            "name": "SOP Checklist",
            "items": [{"name": item, "assignee": None} for item in checklist]
        }
        clickup_request("POST", f"/task/{task_id}/checklist", checklist_data)
    
    return result

def update_list_content(list_id, content):
    """Update list description"""
    return clickup_request("PUT", f"/list/{list_id}", {"content": content})

print("=" * 70)
print("🎬 Content Engine SOPs → ClickUp")
print("=" * 70)

# 1. Update List Descriptions with SOPs
print("\n📋 Updating List Descriptions...")

# Content Ideas List
content_ideas_desc = """# 💡 Content Ideas — SOP

## 🎯 Ziel
Sammlung und Priorisierung aller Content-Ideen für die Content Engine.

## 🔄 Workflow
1. **Idea** → Idee eintragen (Thema, Pillar, Audience)
2. **Researching** → Keywords recherchieren, Competitor checken
3. **Ready** → Alle Felder ausgefüllt, wartet auf Montag
4. **🤖 Claude Generate** → Automation triggered
5. **Content Generated** → Review & Anpassung
6. **Scheduled** → Genehmigt, Publishing läuft
7. **Archived** → Published oder verworfen

## 📊 Custom Fields ausfüllen
- **Content Pillar:** Meta Ads Tutorials / Case Study / Agency Life / Industry
- **Target Audience:** E-Com Brands / SaaS / Agencies / Beginners
- **Keywords:** Komma-getrennt, für SEO
- **Priority Score:** 1-10 (Impact × Machbarkeit)
- **Estimated Views:** Geschätzte Reichweite

## ⚡ Quick Actions
- Neue Idee: `+ Task` drücken
- Direkte Generierung: Status auf "🤖 Claude Generate" setzen
- Manuelle Generierung: `@Brain generiere Content für [Thema]`

---
📚 Vollständige Doku: `docs/sop-content-engine.md`
"""

update_list_content(LIST_CONTENT_IDEAS, content_ideas_desc)
print("  ✅ Content Ideas List updated")

# YouTube Pipeline
youtube_desc = """# 📺 YouTube Pipeline — SOP

## 🎯 Ziel
Long-Form Video Production (1x/Woche, Sonntag 10:00)

## ✅ Checklist pro Video

### Pre-Production
- [ ] Script aus Content Ideas reviewen
- [ ] Thumbnail skizzieren (3 Varianten)
- [ ] B-Roll planen (Shot List)
- [ ] Equipment checken (Licht, Kamera, Audio)

### Recording (Samstag)
- [ ] Setup aufbauen
- [ ] Main Take aufnehmen
- [ ] B-Roll Shots
- [ ] Backup auf NAS

### Post-Production
- [ ] Rough Cut
- [ ] B-Roll einfügen
- [ ] Grafiken/Animationen
- [ ] Color Grade
- [ ] Sound Design
- [ ] Export (4K)

### Upload & SEO
- [ ] Thumbnail finalisieren
- [ ] Title (SEO + Clickbait)
- [ ] Description mit Timestamps
- [ ] Tags recherchieren
- [ ] Endscreens
- [ ] Cards
- [ ] Schedule (Sonntag 10:00)

### Post-Publish
- [ ] Community Post
- [ ] Stories
- [ ] Erste 30 Min aktiv antworten

**Ziel:** 10-15 Min Video, 50k+ Views in 12 Monaten
"""

update_list_content(LIST_YOUTUBE, youtube_desc)
print("  ✅ YouTube Pipeline List updated")

# LinkedIn Pipeline
linkedin_desc = """# 💼 LinkedIn Pipeline — SOP

## 🎯 Ziel
3-4 Posts/Woche — Thought Leadership aufbauen

## 📅 Publishing Rhythm

### Dienstag 08:00 — Long-Form Post
**Format:** 500-1300 Wörter
**Template:** Hook → Story → Insights → CTA
**Ziel:** Engagement + Video-Drive

### Donnerstag 08:00 — Carousel/Insight
**Format:** 5-10 Slides (Canva)
**Template:** Problem → Lösung → Steps → CTA
**Ziel:** Shares + Saves

### Freitag 08:00 — Short/Poll
**Format:** Ein Absatz oder Poll
**Template:** Hot Take oder Frage
**Ziel:** Schnelles Engagement

## ✅ Checklist pro Post
- [ ] Hook in ersten 2 Zeilen?
- [ ] Persönliche Story enthalten?
- [ ] Konkrete Insights (nicht nur Buzzwords)?
- [ ] CTA klar (Comment, Link, Follow)?
- [ ] Hashtags: #MetaAds #Ecommerce #PerformanceMarketing
- [ ] Getaggt: @Brain für Review (optional)

**Ziel:** 5k+ Views/Post, 3%+ Engagement
"""

update_list_content(LIST_LINKEDIN, linkedin_desc)
print("  ✅ LinkedIn Pipeline List updated")

# Newsletter Pipeline
newsletter_desc = """# 📧 Newsletter Pipeline — SOP

## 🎯 Ziel
Weekly Digest (Donnerstag 09:00) — 35%+ Open Rate

## 📋 Template Struktur

**Subject Line:** [Video Title] + This Week's Insights

**1. 🎥 This Week's Video**
- Thumbnail + Link
- 3 Key Takeaways
- CTA: Watch here

**2. 💼 LinkedIn Highlights**
- Best performing post
- Most engaged comment
- Link zu Profil

**3. 🛠️ Tool Recommendation**
- Tool Name
- One-sentence why
- Link

**4. 🤔 Question for You**
- Engagement Frage
- Hit reply CTA

**P.S.** Fun fact or bonus tip

## ✅ Pre-Send Checklist
- [ ] Subject Line unter 50 Zeichen?
- [ ] Preview Text gesetzt?
- [ ] Video Link funktioniert?
- [ ] Mobile Preview gecheckt?
- [ ] Send Test an dich selbst?
- [ ] Send Time: Do 09:00?

**Ziel:** 35%+ Open Rate, 5%+ Click Rate
"""

update_list_content(LIST_NEWSLETTER, newsletter_desc)
print("  ✅ Newsletter Pipeline List updated")

# Shorts Pipeline
shorts_desc = """# 📱 Shorts/Reels Pipeline — SOP

## 🎯 Ziel
3 Shorts/Woche aus jedem YouTube Video

## 🔄 Repurposing Workflow

### Aus YouTube Video extrahieren:
1. **Hook** (0:00-0:45) → Beste 30-45 Sek
2. **Mistake** (Timestamp aus Script) → Konkreter Fehler
3. **Framework** (Später im Video) → Taktik/Tip

## 🎬 Edit Workflow (CapCut)

### Jeder Short braucht:
- [ ] Hook in ersten 3 Sekunden
- [ ] Untertitel/Captions
- [ ] Zoom/Pan auf wichtige Momente
- [ ] Musik (Trending Sounds)
- [ ] CTA: "Full Video in Bio"

### Export Settings:
- Format: 9:16 (1080x1920)
- 30fps
- Mit Captions (burn-in)

## 📤 Cross-Posting

| Plattform | Zeit | Besonderheit |
|-----------|------|--------------|
| YouTube Shorts | MI/FR/SO 12:00 | Hashtags in Description |
| Instagram Reels | MI/FR/SO 12:00 | Trending Audio nutzen |
| TikTok | MI/FR/SO 12:00 | Native Upload, nicht Crosspost |

## ✅ Checklist pro Short
- [ ] Hook unter 5 Sekunden?
- [ ] Captions lesbar?
- [ ] Timestamp aus YouTube notiert?
- [ ] Caption mit CTA?
- [ ] Hashtags: #metaads #facebookads #ecommerce

**Ziel:** 10k+ Views/Short
"""

update_list_content(LIST_SHORTS, shorts_desc)
print("  ✅ Shorts Pipeline List updated")

# Distribution Tracker
distribution_desc = """# 📊 Distribution Tracker — SOP

## 🎯 Ziel
Übersicht über alle Published Content & Performance

## 📋 Tracking Pro Video

| Content | Status | Publish Date | Views | Engagement | Link |
|---------|--------|--------------|-------|------------|------|
| YouTube | ⬜ | | | | |
| Short 1 | ⬜ | | | | |
| Short 2 | ⬜ | | | | |
| Short 3 | ⬜ | | | | |
| LinkedIn Long | ⬜ | | | | |
| LinkedIn Carousel | ⬜ | | | | |
| LinkedIn Short | ⬜ | | | | |
| Newsletter | ⬜ | | | | |

## 🔄 Weekly Review (Freitag)

### Metrics aktualisieren:
- [ ] YouTube: Views, Watch Time, Subs
- [ ] LinkedIn: Views, Engagement Rate
- [ ] Shorts: Views pro Plattform
- [ ] Newsletter: Open Rate, Click Rate

### Learnings dokumentieren:
- Was hat funktioniert?
- Was nicht?
- Anpassungen für nächste Woche?

## 📊 Monthly Report
Erstelle am Monatsende:
- Total Views (alle Plattformen)
- Best performing Content
- Audience Growth
- Lead Generation
"""

update_list_content(LIST_DISTRIBUTION, distribution_desc)
print("  ✅ Distribution Tracker List updated")

# 2. Create Template Tasks
print("\n📋 Creating Template Tasks...")

# Master SOP Task
today = datetime.now()
master_task = create_task(
    LIST_CONTENT_IDEAS,
    "📚 SOP: Content Engine Quick Reference",
    """# 🎬 Content Engine — Quick Reference

## 🚀 Weekly Workflow (Montag 09:00)

1. **Content Ideas öffnen**
2. **Idee auswählen** (nach Priority Score)
3. **Custom Fields checken:**
   - Content Pillar ✓
   - Target Audience ✓
   - Keywords ✓
   - Priority Score ✓
4. **Status → "🤖 Claude Generate"**
5. **Warte max 5 Min**
6. **Review generierten Content** in Kommentaren
7. **Anpassen & Approven**

## 📅 Publishing Rhythm

| Tag | Zeit | Plattform | Content |
|-----|------|-----------|---------|
| DI | 08:00 | LinkedIn | Long-Form Post |
| MI | 12:00 | YT/IG/TT | Short #1 |
| DO | 08:00 | LinkedIn | Carousel |
| DO | 09:00 | Newsletter | Weekly Digest |
| FR | 08:00 | LinkedIn | Short/Poll |
| FR | 12:00 | YT/IG/TT | Short #2 |
| SO | 10:00 | YouTube | Long-Form Video |
| SO | 14:00 | YT/IG/TT | Short #3 |

## 🛠️ Troubleshooting

**Automation nicht getriggert?**
→ Manuelles Generieren:
   `python3 scripts/content_engine_generator_v2.py --task-id "TASK_ID"`

**Content passt nicht?**
→ Kommentar mit "@Brain regenerate [Section]"

**Keine Ideen?**
→ Schau in `docs/content-engine-content-calendar.md`

## 📚 Links
- SOP: `docs/sop-content-engine.md`
- Masterplan: `docs/content-engine-masterplan.md`
- Content Calendar: `docs/content-engine-content-calendar.md`
- Brand Voice: `docs/content-engine-brand-voice.md`
""",
    tags=["sop", "reference"]
)
if master_task:
    print("  ✅ Master SOP Task created")

# Next Week Prep Task
next_monday = today + timedelta(days=(7 - today.weekday()))
prep_task = create_task(
    LIST_CONTENT_IDEAS,
    f"🎯 Woche {next_monday.isocalendar()[1]}: Content auswählen & generieren",
    f"""# Content für Woche {next_monday.isocalendar()[1]} vorbereiten

**Fällig:** {next_monday.strftime('%A, %d.%m.%Y')} 09:00

## ✅ To-Do

1. [ ] Content Ideas öffnen
2. [ ] Idee mit höchstem Priority Score wählen
3. [ ] Custom Fields verifizieren
4. [ ] Status auf "🤖 Claude Generate" setzen
5. [ ] Warten (max 5 Min)
6. [ ] Generierten Content reviewen
7. [ ] YouTube Script anpassen
8. [ ] LinkedIn Posts finalisieren
9. [ ] Newsletter Draft reviewen
10. [ ] Shorts Hooks checken

## 📋 Output
Nach diesem Task hast du:
- 🎬 YouTube Script (für Samstag Recording)
- 💼 3 LinkedIn Posts (für DI/DO/FR)
- 📧 Newsletter Draft (für DO)
- 📱 3 Shorts Strategie (für MI/FR/SO)

**Nächster Schritt:** Samstag Video aufnehmen
""",
    due_date=next_monday,
    tags=["weekly-task"],
    checklist=[
        "Content Idea auswählen",
        "Custom Fields checken",
        "Status auf 'Claude Generate' setzen",
        "Content reviewen",
        "YouTube Script finalisieren",
        "LinkedIn Posts reviewen",
        "Newsletter Draft checken",
        "Shorts Strategie durchgehen"
    ]
)
if prep_task:
    print("  ✅ Next Week Prep Task created")

# Content Examples Task
examples_task = create_task(
    LIST_CONTENT_IDEAS,
    "💡 Content Ideen Beispiele (Monat 1)",
    """# Content Ideen für den ersten Monat

## Woche 1: Meta Ads Mastery
**Thema:** 5 Meta Ads Fehler die dich Geld kosten
**Pillar:** Tutorials
**Keywords:** meta ads fehler, facebook ads 2026, roas
**Priority:** 9/10

## Woche 2: Case Study
**Thema:** Von 2x auf 5x ROAS: Fashion Brand Case Study
**Pillar:** Case Study
**Keywords:** meta ads case study, fashion ecommerce, scaling
**Priority:** 9/10

## Woche 3: Meta Ads Mastery (Advanced)
**Thema:** Creative Testing Framework (48h Winner System)
**Pillar:** Tutorials
**Keywords:** creative testing, facebook ads creative, winner identification
**Priority:** 8/10

## Woche 4: Hot Take
**Thema:** Warum Advantage+ Shopping overrated ist
**Pillar:** Industry Commentary
**Keywords:** advantage+ shopping, meta ads 2026, contrarian
**Priority:** 7/10

---

**Mehr Ideen:** Siehe `docs/content-engine-content-calendar.md`
""",
    tags=["examples", "backlog"]
)
if examples_task:
    print("  ✅ Content Examples Task created")

print("\n" + "=" * 70)
print("✅ Content Engine SOPs erfolgreich in ClickUp erstellt!")
print("=" * 70)
print("\n📋 Summary:")
print("  • 6 List Descriptions mit SOPs aktualisiert")
print("  • 3 Template Tasks erstellt:")
print("    - Master SOP Reference")
print("    - Weekly Prep Task (mit Checklist)")
print("    - Content Examples (Monat 1)")
print("\n🎬 Bereit für den ersten Content-Durchlauf!")
