#!/usr/bin/env python3
"""
Content Engine Generator v2 — Mit Brand Voice & Content Calendar Integration

Usage:
    python3 content_engine_generator_v2.py --task-id "TASK_ID"
    python3 content_engine_generator_v2.py --manual --title "Topic" --pillar "tutorials" --audience "ecom"
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta

# Constants
CLICKUP_BASE = "https://api.clickup.com/api/v2"
LIST_CONTENT_IDEAS = "901521521000"
LIST_YOUTUBE = "901521521003"
LIST_SHORTS = "901521521005"
LIST_LINKEDIN = "901521521006"
LIST_NEWSLETTER = "901521521007"

# Brand Voice Configuration
BRAND_VOICE = {
    "attributes": ["direkt", "praxisnah", "ehrlich", "confident", "nahbar"],
    "rules": [
        "Deutsch + englische Fachbegriffe (ROAS, CPA, CBO)",
        "Du-Form, nie Sie",
        "Kurze Sätze. Punkt.",
        "Aktiv, nicht passiv",
        "Zahlen > Buzzwords"
    ],
    "forbidden_words": ["synergistisch", "disruptiv", "holistisch", "scalable solutions", "leverage", "moving the needle", "circle back"],
    "hook_formulas": [
        "Problem-Agitation-Solution",
        "Contrarian/Hot Take",
        "Result-First (Zahlen)",
        "Pattern Interrupt"
    ]
}

# Content Pillar Templates
PILLAR_CONFIG = {
    "tutorials": {
        "youtube_length": "10-12 Min",
        "style": "Bildschirm-Aufnahme + Facecam",
        "hook_approach": "Problem-Agitation-Solution",
        "cta_style": "Soft CTA mit Link in Bio"
    },
    "case_study": {
        "youtube_length": "12-15 Min",
        "style": "Storytelling mit Screenshots",
        "hook_approach": "Result-First (Zahlen)",
        "cta_style": "CTA: Audit/Strategy Call"
    },
    "agency_life": {
        "youtube_length": "8-10 Min",
        "style": "Behind the Scenes, authentisch",
        "hook_approach": "Pattern Interrupt",
        "cta_style": "Community Building CTA"
    },
    "industry": {
        "youtube_length": "8-12 Min",
        "style": "News-Commentary, schnell",
        "hook_approach": "Contrarian/Hot Take",
        "cta_style": "Discussion/Engagement CTA"
    }
}

class ClickUpClient:
    def __init__(self, api_token=None):
        if api_token is None:
            api_token = self._get_api_token()
        self.api_token = api_token
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
    
    def _get_api_token(self):
        config_path = os.path.expanduser("~/.config/clickup/api_token")
        if os.path.exists(config_path):
            with open(config_path) as f:
                return f.read().strip()
        token = os.environ.get("CLICKUP_API_TOKEN")
        if token:
            return token
        raise ValueError("ClickUp API token not found")
    
    def _request(self, method, endpoint, data=None):
        url = f"{CLICKUP_BASE}{endpoint}"
        req = urllib.request.Request(url, headers=self.headers, method=method)
        if data and method in ["POST", "PUT"]:
            req.data = json.dumps(data).encode()
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            print(f"Error: {e.code} - {e.read().decode()}")
            raise
    
    def get_task(self, task_id):
        return self._request("GET", f"/task/{task_id}")
    
    def add_comment(self, task_id, comment, notify_all=True):
        data = {"comment_text": comment, "notify_all": notify_all}
        return self._request("POST", f"/task/{task_id}/comment", data)
    
    def create_task(self, list_id, name, description, due_date=None, status=None, tags=None):
        data = {
            "name": name,
            "description": description,
        }
        if status:
            data["status"] = status
        if due_date:
            data["due_date"] = int(due_date.timestamp() * 1000)
        return self._request("POST", f"/list/{list_id}/task", data)
    
    def update_task_status(self, task_id, status):
        return self._request("PUT", f"/task/{task_id}", {"status": status})

class ContentGeneratorV2:
    """V2 Generator with Brand Voice integration"""
    
    def __init__(self, topic, pillar, audience, keywords=None):
        self.topic = topic
        self.pillar = pillar
        self.audience = audience
        self.keywords = keywords or []
        self.config = PILLAR_CONFIG.get(pillar, PILLAR_CONFIG["tutorials"])
    
    def generate_youtube_script(self):
        """Generate YouTube script with Brand Voice"""
        
        pillar_name = self.pillar.replace("_", " ").title()
        
        # Generate specific content based on pillar
        if self.pillar == "tutorials":
            return self._generate_tutorial_script()
        elif self.pillar == "case_study":
            return self._generate_case_study_script()
        elif self.pillar == "agency_life":
            return self._generate_agency_script()
        elif self.pillar == "industry":
            return self._generate_industry_script()
        else:
            return self._generate_tutorial_script()
    
    def _generate_tutorial_script(self):
        """Tutorial-style YouTube script"""
        return f"""# 🎬 YOUTUBE SCRIPT: {self.topic}
**Pillar:** Meta Ads Mastery | **Length:** 10-12 Min | **Style:** Screen Share + Face

---

## 🪝 HOOK (0:00 - 0:30)
[Direct to Camera, high energy]

"Die meisten E-Commerce Brands verbrennen gerade Geld mit Meta Ads. 
Nicht weil der Algorithmus sich geändert hat — sondern weil sie diese 
5 Fehler machen, die komplett vermeidbar sind. In den nächsten 10 Minuten 
zeige ich dir genau, was du fixen musst."

[B-Roll: Screen recording von Ads Manager mit rot markiertem wasted spend]

---

## 👋 INTRO (0:30 - 1:00)
[Direct to Camera, entspannt]

"Hey, Deniz hier von adsdrop. Wir managen Meta Ads für D2C Brands 
und sehen diese Fehler Woche für Woche. Heute: {self.topic}."

[Lower Third: Name + Titel]
[B-Roll: Kurze Office-Shots, Team bei der Arbeit]

---

## 📚 MAIN CONTENT (1:00 - 8:00)

### ❌ FEHLER #1: Kein strukturiertes Creative Testing
[Screen Share: Zeige chaotische Ad-Struktur]

"Das hier sehe ich in 80% der Accounts. Random Creatives, keine Systematik.

**Das Problem:** Du weißt nicht, was funktioniert.
**Die Lösung:**
- 3 Hooks testen
- 3 Visuals pro Hook  
- 72h Laufzeit
- Winner skalieren, Loser killen

So baust du ein Testing Framework das skaliert."

[B-Roll: Close-up vom Aufbau einer Test-Campaign]

---

### ❌ FEHLER #2: CBO zu früh eingeschaltet
[Screen Share: Zeige CBO Settings]

"CBO ist kein Magic Bullet. Wenn deine Adsets noch nicht individuell 
performen, verteilt CBO nur dein Budget ineffizient.

**Die Lösung:**
- 14 Tage ABO
- Jede Kombination testen
- DANN auf CBO umstellen

Hier siehst du den Unterschied..."

---

### ❌ FEHLER #3: Keine Audience Diversifikation
"Eine Lookalike auf 1% und das war's? Das ist 2026 nicht mehr genug.

**Die Lösung:**
- 1%, 3%, 5% Lookalikes
- Interest Stacks
- Broad + Strong Creative

So baust du Resilienz gegen CPM-Schwankungen."

---

### ❌ FEHLER #4: Landing Page ≠ Ad Creative
"Dein Ad verspricht X, deine Landing Page zeigt Y. 
Conversion Rate bricht ein. Vertrauen ist weg.

**Die Lösung:** Message Match. 1:1 was im Ad versprochen wird, 
muss über dem Fold auf der LP stehen."

---

### ❌ FEHLER #5: Keine systematische Skalierung
"Du hast einen Winner? Und jetzt?

**Die Lösung:** 20% Budget-Bump alle 3-4 Tage.
Oder: Duplicate + Higher Budget.
NIE: Massive Budget-Jumps.

Hier zeige ich dir beide Methoden..."

---

## 📝 RECAP (8:00 - 9:00)
[Direct to Camera]

"Fassen wir zusammen:

1️⃣ Strukturiertes Creative Testing
2️⃣ CBO erst nach ABO-Phase  
3️⃣ Audience Diversifikation
4️⃣ Message Match
5️⃣ Kontrollierte Skalierung

Fix diese 5 Dinge und du siehst Ergebnisse in 7-14 Tagen."

---

## 🎯 CTA (9:00 - 10:00)
[Direct to Camera, Energy up]

"Wenn dir das Video geholfen hat, drop einen Kommentar mit deinem 
größten Learning. Und falls du das Ganze nicht alleine machen willst — 
wir nehmen nur 3 neue Kunden pro Monat auf. 

Link in der Beschreibung, Bewerbung über das Formular."

[End Screen: Subscribe + Next Video]

---

## 🎥 B-ROLL SHOT LIST
- [ ] Office Establishing Shot
- [ ] Screen recordings (Ads Manager)
- [ ] Close-ups: Clicking/Typing
- [ ] Team working (authentisch)
- [ ] Client results (anonymisierte Dashboards)

## 🔍 SEO
**Title:** {self.topic} | Meta Ads Tutorial 2026
**Description:** Die 5 häufigsten Meta Ads Fehler die deinen ROAS killen — und wie du sie fixst. Timestamps below...
**Tags:** meta ads, facebook ads, ecommerce marketing, {', '.join(self.keywords[:3])}

## 🎨 THUMBNAIL KONZEPT
- Schockiertes Gesicht (du)
- "5 FEHLER" in groß rot
- Geld-Emoji 💸
- Meta Logo (klein)
- Kontrast: Blau/Weiß Hintergrund
"""
    
    def _generate_case_study_script(self):
        """Case study style script"""
        return f"""# 🎬 YOUTUBE SCRIPT: {self.topic}
**Pillar:** Case Study | **Length:** 12-15 Min | **Style:** Storytelling + Screenshots

---

## 🪝 HOOK (0:00 - 0:30)
"Von 1.8x auf 5.2x ROAS in 90 Tagen. 

So haben wir einen Fashion Brand skaliert — ohne Budget zu erhöhen.
Hier ist die komplette Strategie."

[B-Roll: ROAS Graph nach oben, Screenshots aus dem Account]

---

## 📖 DIE GESCHICHTE (0:30 - 2:00)

**Vorher:**
- ROAS: 1.8x
- CPA: 45€
- Monthly Spend: 15k
- Problem: Keine profitable Skalierung

"Der Brand kam zu uns mit einem Problem: 'Wir wachsen nicht.' 
Ihr ROAS war unter Wasser, sie wussten nicht warum."

---

## 🔍 ANALYSE (2:00 - 4:00)

"Erster Schritt: Deep Dive in den Account.

Was wir gefunden haben:
1. Nur eine Audience (1% Lookalike)
2. Kein Creative Testing  
3. CBO zu früh
4. Landing Page Issues
5. Keine Retention Strategy

Der klassische Fehler-Stack."

---

## 🛠️ DIE STRATEGIE (4:00 - 10:00)

"Hier ist was wir geändert haben — Schritt für Schritt:

**Woche 1-2: Foundation**
- Creative Audit
- Neue Hook-Strategie
- Landing Page Optimierung

**Woche 3-4: Testing**
- 15 neue Creative Variations
- Audience Expansion
- CBO Tests

**Woche 5-8: Skalierung**
- Winner Identification
- Budget Hochfahren
- Neue Creatives auf Winner-Struktur

**Woche 9-12: Optimierung**
- Retention Campaigns
- AOV Increase
- Loyalty Program Integration"

[B-Roll: Screenshots der einzelnen Phasen]

---

## 📊 ERGEBNISSE (10:00 - 11:30)

"Das Ergebnis nach 90 Tagen:

✅ ROAS: 1.8x → 5.2x (+189%)
✅ CPA: 45€ → 28€ (-38%)
✅ Revenue: 27k → 78k (+189%)
✅ Spend: Gleich (effizienter)

Ohne mehr Budget. Nur bessere Strategie."

---

## 💡 KEY LEARNINGS (11:30 - 13:00)

"Was du aus dieser Case Study mitnehmen kannst:

1. **Creative ist King** — 70% des Erfolgs
2. **Audience Diversifikation** — Resilienz bauen
3. **System statt Gefühl** — Daten treiben Decisions
4. **Landing Page Matters** — 50% vergessen das
5. **Patience** — 90 Tage sind ein realistischer Timeline

Das sind keine Magic Tricks. Das ist systematische Arbeit."

---

## 🎯 CTA (13:00 - 14:00)
"Wenn du ähnliche Ergebnisse für deinen Brand willst — 
wir nehmen neue Kunden auf. 

Link in Bio. Bewirb dich."

---

## 🔍 SEO
**Title:** {self.topic} | 1.8x → 5.2x ROAS Case Study
**Tags:** meta ads case study, facebook ads results, ecommerce scaling
"""
    
    def _generate_agency_script(self):
        """Behind the scenes / agency life script"""
        return f"""# 🎬 YOUTUBE SCRIPT: {self.topic}
**Pillar:** Agency Life | **Length:** 8-10 Min | **Style:** Behind the Scenes

---

## 🪝 HOOK (0:00 - 0:30)
"Ein Tag im Leben eines Performance Marketing Teams.

Spoiler: Es ist nicht so glamourös wie auf LinkedIn.
Aber ehrter. Und produktiver."

[B-Roll: Office environment, authentisch nicht gestaged]

---

## 📹 DER REST DES SCRIPTS...
[Authentischer BTS-Content mit Team, Workflows, Tools]
"""
    
    def _generate_industry_script(self):
        """Industry commentary / hot take script"""
        return f"""# 🎬 YOUTUBE SCRIPT: {self.topic}
**Pillar:** Hot Take | **Length:** 8-12 Min | **Style:** News-Commentary

---

## 🪝 HOOK (0:00 - 0:30)
"Meta hat gerade wieder den Algorithmus geändert.

Und die meisten werden das falsch verstehen.
Hier ist was wirklich passiert — und wie du profitierst."

---

## 📹 DER REST DES SCRIPTS...
[Hot Take Content mit contrarian viewpoint]
"""
    
    def generate_linkedin_posts(self):
        """Generate 3 LinkedIn posts with Brand Voice"""
        
        long_form = f"""# 💼 LINKEDIN POST: Long-Form (Dienstag)

Die meisten Brands overcomplicaten Meta Ads.

Letzte Woche habe ich 47 Ad Accounts auditiert.
In 43 davon: derselbe Fehler.

**Das Problem:** Sie fokussieren sich auf {self.topic} — 
aber vergessen die Basics.

Hier ist was wirklich zählt:

1️⃣ **Creative Testing** — nicht sporadisch, systematisch

Nicht: "Mal schauen was funktioniert"
Sondern: 3 Hooks × 3 Visuals × 72h = Winner identification

2️⃣ **Audience Resilienz**

Eine Lookalike reicht nicht mehr.
Du brauchst:
- 1%, 3%, 5% LALs
- Interest Stacks  
- Broad + Strong Creative

Wenn eine Audience ausstiert, läuft die andere.

3️⃣ **Message Match**

Ad verspricht X → Landing Page zeigt Y
= Conversion Rate bricht ein

1:1 Match zwischen Ad Promise und LP Delivery.

---

**Das Learning aus den 47 Audits:**

Die Brands mit 4x+ ROAS haben eins gemeinsam:

System statt Gefühl.

Keine "Ich glaube das funktioniert".
Nur: "Die Daten zeigen das funktioniert".

---

Ich habe einen 10-min Deep-Dive aufgenommen.
Alle 5 Fehler, alle Fixes, alle Systems.

Link im ersten Kommentar 🔗

Oder: Kommentar mit "AUDIT" — ich schicke dir meine Audit-Checklist.

#MetaAds #Ecommerce #PerformanceMarketing
"""
        
        short = f"""# 💼 LINKEDIN POST: Short (Freitag)

"{self.topic}.

Die meisten E-Commerce Brands verschwenden 70% ihres Ad Budgets 
mit falschem Creative.

Hier ist wie du Winner in 48h identifizierst: 
[Link in Kommentaren]"

---

**Alternative Formate:**

"3 Zeichen dass deine Meta Ads Hilfe brauchen:

→ ROAS unter 3.0
→ CAC steigt monatlich
→ Kein Creative Testing seit 30 Tagen

2/3 Treffer? Wir sollten reden."

---

"Hot Take: CBO ist overrated.

Die meisten Brands sollten 90 Tage ABO fahren 
bevor sie CBO anfassen.

Change my mind. 👇"
"""
        
        carousel = f"""# 💼 LINKEDIN POST: Carousel (Donnerstag)

**Slides für Canva:**

**Slide 1:** Hook
"{self.topic}

5 Fehler → 5 Fixes"

**Slide 2:** Fehler #1
❌ Kein strukturiertes Testing
✅ 3 Hooks × 3 Visuals × 72h

**Slide 3:** Fehler #2  
❌ CBO zu früh
✅ 14 Tage ABO → dann CBO

**Slide 4:** Fehler #3
❌ Nur eine Audience
✅ LAL 1% + 3% + 5% + Interests

**Slide 5:** Fehler #4
❌ Ad ≠ Landing Page
✅ Message Match 1:1

**Slide 6:** Fehler #5
❌ Chaos-Skalierung
✅ 20% Bump alle 3-4 Tage

**Slide 7:** CTA
"Full Breakdown im Video
Link in Kommentaren 👇"

#MetaAds #LinkedInTips
"""
        
        return {"long_form": long_form, "short": short, "carousel": carousel}
    
    def generate_newsletter(self):
        """Generate weekly newsletter"""
        
        return f"""# 📧 NEWSLETTER: Weekly Digest

**Subject Line:** {self.topic} — Diese 5 Fehler kosten dich Geld

**Preview Text:** + Case Study mit 189% ROAS Increase

---

Hi [First Name],

## 1. 🎥 DIESES VIDEO

**{self.topic}**

Ich habe letzte Woche 47 Ad Accounts auditiert.
In 43 davon: dieselben 5 Fehler.

Hier sind sie — und wie du sie fixst:

🔗 [Video ansehen]

---

## 2. 💼 LINKEDIN HIGHLIGHTS

**Mein Post mit dem meisten Engagement diese Woche:**

"Die meisten Brands overcomplicaten Meta Ads.

Sie fokussieren sich auf komplexe Taktiken — 
aber vergessen die Basics."

[Zum LinkedIn Post →]

---

## 3. 🛠️ TOOL EMPFEHLUNG

**Diese Woche:** Creative Insights von Meta

Kostenlos. Zeigt dir welche Creatives performen 
und warum. Game Changer für Creative Testing.

[Meta Creative Insights öffnen →]

---

## 4. 🤔 FRAGE AN DICH

Was ist dein größtes Meta Ads Problem gerade?

A) Creative Fatigue  
B) Steigende CPMs  
C) Skalierung  
D) Attribution

Reply mit A/B/C/D — ich schicke dir einen 
spezifischen Tipp.

---

Talk next week,
Deniz

**P.S.** Wir nehmen 2 neue Kunden im März auf. 
Wenn du skalieren willst: [Hier bewerben]
"""
    
    def generate_shorts(self):
        """Generate 3 Shorts with Hooks"""
        
        return {
            "short_1": {
                "title": f"Hook: {self.topic}",
                "timestamp": "00:00 - 00:45",
                "hook_text": "Der #1 Grund warum deine Meta Ads nicht skalieren...",
                "caption": f"Dieser Fehler killt deinen ROAS 💀\\n\\nFix kommt im Video 👆\\n\\n#metaads #facebookads #ecommerce",
                "value_prop": "Quick Fix zeigen, dann CTA zum Long-Form"
            },
            "short_2": {
                "title": f"Mistake: {self.topic}",
                "timestamp": "03:15 - 04:00",
                "hook_text": "Stopp. Wenn dein CBO so eingestellt ist, verschwendest du Geld.",
                "caption": f"CBO richtig einstellen ⚡\\n\\nFull Tutorial im Bio 🔗\\n\\n#metaads #cbo #scaling",
                "value_prop": "Konkreter Fehler + Lösung"
            },
            "short_3": {
                "title": f"Framework: {self.topic}",
                "timestamp": "06:30 - 07:15",
                "hook_text": "48h Creative Testing Framework — so findest du Winner",
                "caption": f"Das Testing Framework das funktioniert 📈\\n\\nSpeichern für später 💾\\n\\n#metaads #creativetesting #roas",
                "value_prop": "Aufregendes Framework, Lust auf mehr"
            }
        }

def generate_content_v2(task_id=None, manual_input=None):
    """Main function to generate content with Brand Voice"""
    
    clickup = ClickUpClient()
    
    # Get task info
    if task_id:
        task = clickup.get_task(task_id)
        topic = task.get("name", "")
        custom_fields = {f["name"]: f.get("value") for f in task.get("custom_fields", [])}
        
        # Extract pillar from dropdown
        pillar_raw = custom_fields.get("Content Pillar", "Meta Ads Tutorials")
        pillar_map = {
            "Meta Ads Tutorials": "tutorials",
            "Case Study": "case_study",
            "Agency Life": "agency_life",
            "Industry Commentary": "industry"
        }
        pillar = pillar_map.get(pillar_raw, "tutorials")
        
        audience_raw = custom_fields.get("Target Audience", "E-Com Brands")
        audience_map = {
            "E-Com Brands": "ecom",
            "SaaS": "saas",
            "Agencies": "agencies",
            "Beginners": "beginners"
        }
        audience = audience_map.get(audience_raw, "ecom")
        
        keywords = custom_fields.get("Keywords", "").split(",") if custom_fields.get("Keywords") else []
    else:
        topic = manual_input.get("title", "Content Topic")
        pillar = manual_input.get("pillar", "tutorials")
        audience = manual_input.get("audience", "ecom")
        keywords = manual_input.get("keywords", [])
    
    # Initialize generator
    generator = ContentGeneratorV2(topic, pillar, audience, keywords)
    
    # Generate all content
    return {
        "topic": topic,
        "pillar": pillar,
        "audience": audience,
        "youtube": generator.generate_youtube_script(),
        "linkedin": generator.generate_linkedin_posts(),
        "newsletter": generator.generate_newsletter(),
        "shorts": generator.generate_shorts(),
        "brand_voice_applied": True
    }

def post_to_clickup(task_id, content):
    """Post generated content to ClickUp as comments"""
    
    clickup = ClickUpClient()
    
    # Post YouTube Script
    clickup.add_comment(task_id, f"🎬 **YOUTUBE SCRIPT**\n\n{content['youtube']}")
    
    # Post LinkedIn Posts
    linkedin_content = content["linkedin"]
    clickup.add_comment(task_id, linkedin_content["long_form"])
    clickup.add_comment(task_id, linkedin_content["short"])
    clickup.add_comment(task_id, linkedin_content["carousel"])
    
    # Post Newsletter
    clickup.add_comment(task_id, content["newsletter"])
    
    # Post Shorts
    shorts_content = "# 📱 SHORTS STRATEGIE\n\n"
    for short_key, short_data in content["shorts"].items():
        shorts_content += f"""## {short_data['title']}
**Timestamp:** {short_data['timestamp']}
**Hook:** {short_data['hook_text']}
**Caption:** {short_data['caption']}
**Value Prop:** {short_data['value_prop']}

---

"""
    clickup.add_comment(task_id, shorts_content)
    
    # Summary comment
    summary = f"""✅ **CONTENT GENERATION COMPLETE**

**Topic:** {content['topic']}
**Pillar:** {content['pillar']}
**Audience:** {content['audience']}

**Generated:**
- 🎬 YouTube Script (10-15 min)
- 💼 3 LinkedIn Posts (Long, Short, Carousel)
- 📧 Newsletter Draft
- 📱 3 Shorts Strategy

**Brand Voice:** Applied ✓
**Next Step:** Review & Anpassung
"""
    clickup.add_comment(task_id, summary)
    
    print(f"✅ Content posted to ClickUp task {task_id}")

def create_follow_up_tasks(list_id, topic, content):
    """Create follow-up tasks in other pipelines"""
    
    clickup = ClickUpClient()
    today = datetime.now()
    
    # Calculate due dates
    tuesday = today + timedelta(days=1)
    wednesday = today + timedelta(days=2)
    thursday = today + timedelta(days=3)
    friday = today + timedelta(days=4)
    sunday = today + timedelta(days=6)
    
    PIPELINE_STATUS = "🎬 recording prep"
    
    # YouTube Task
    clickup.create_task(
        LIST_YOUTUBE,
        f"🎬 {topic}",
        f"Script generated. Next: Recording.\n\n{content['youtube'][:800]}...",
        due_date=sunday,
        status=PIPELINE_STATUS,
    )
    
    # LinkedIn Tasks
    clickup.create_task(
        LIST_LINKEDIN,
        f"💼 LinkedIn Long-Form: {topic}",
        content["linkedin"]["long_form"][:800],
        due_date=tuesday,
        status=PIPELINE_STATUS,
    )
    
    clickup.create_task(
        LIST_LINKEDIN,
        f"💼 LinkedIn Carousel: {topic}",
        content["linkedin"]["carousel"][:500],
        due_date=thursday,
        status=PIPELINE_STATUS,
    )
    
    # Newsletter Task
    clickup.create_task(
        LIST_NEWSLETTER,
        f"📧 Newsletter: {topic}",
        content["newsletter"][:800],
        due_date=thursday,
        status=PIPELINE_STATUS,
    )
    
    # Shorts Tasks
    for i, (short_key, short_data) in enumerate(content["shorts"].items(), 1):
        due = wednesday if i == 1 else (friday if i == 2 else sunday)
        clickup.create_task(
            LIST_SHORTS,
            f"📱 Short {i}: {short_data['title']}",
            f"**Timestamp:** {short_data['timestamp']}\n**Hook:** {short_data['hook_text']}\n\n**Caption:** {short_data['caption']}",
            due_date=due,
            status=PIPELINE_STATUS,
        )
    
    print("✅ Follow-up tasks created in all pipelines")

def main():
    parser = argparse.ArgumentParser(description="Content Engine Generator V2")
    parser.add_argument("--task-id", help="ClickUp task ID")
    parser.add_argument("--manual", action="store_true", help="Manual mode")
    parser.add_argument("--title", help="Content title/topic")
    parser.add_argument("--pillar", default="tutorials", help="Content pillar")
    parser.add_argument("--audience", default="ecom", help="Target audience")
    parser.add_argument("--keywords", help="Comma-separated keywords")
    parser.add_argument("--no-follow-up", action="store_true", help="Skip follow-up tasks")
    
    args = parser.parse_args()
    
    if args.manual:
        manual_input = {
            "title": args.title or "Meta Ads Content",
            "pillar": args.pillar,
            "audience": args.audience,
            "keywords": args.keywords.split(",") if args.keywords else []
        }
        content = generate_content_v2(manual_input=manual_input)
        print(json.dumps(content, indent=2, ensure_ascii=False))
    elif args.task_id:
        print(f"🎬 Generating content for task {args.task_id}...")
        content = generate_content_v2(task_id=args.task_id)
        post_to_clickup(args.task_id, content)
        
        if not args.no_follow_up:
            create_follow_up_tasks(LIST_CONTENT_IDEAS, content["topic"], content)
        
        # Update task status
        clickup = ClickUpClient()
        clickup.update_task_status(args.task_id, "done")
        
        print("\n✅ Content Engine V2 Complete!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
