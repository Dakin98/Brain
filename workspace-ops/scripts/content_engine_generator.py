#!/usr/bin/env python3
"""
Content Engine Generator
Generiert YouTube Scripts, LinkedIn Posts, Newsletter & Shorts basierend auf ClickUp Tasks

Usage:
    python3 content_engine_generator.py --task-id "TASK_ID"
    python3 content_engine_generator.py --manual --title "5 Meta Ads Mistakes" --pillar "tutorials" --audience "ecom"

Environment:
    CLICKUP_API_TOKEN - ClickUp API Token
    CLAUDE_API_KEY - Optional, für direkte API Calls
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
CONTENT_ENGINE_FOLDER = "901514665491"

# List IDs
LIST_CONTENT_IDEAS = "901521521000"
LIST_YOUTUBE = "901521521003"
LIST_SHORTS = "901521521005"
LIST_LINKEDIN = "901521521006"
LIST_NEWSLETTER = "901521521007"

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
    
    def create_task(self, list_id, name, description, due_date=None, tags=None, status=None):
        data = {
            "name": name,
            "description": description
        }
        if status:
            data["status"] = status
        if due_date:
            data["due_date"] = int(due_date.timestamp() * 1000)
        if tags:
            data["tags"] = tags
        return self._request("POST", f"/list/{list_id}/task", data)
    
    def attach_file(self, task_id, filename, content):
        # For text attachments, we'll add as comment with markdown
        pass

class ContentGenerator:
    """Generates content based on templates and topic"""
    
    def __init__(self, topic, pillar, audience, keywords=None):
        self.topic = topic
        self.pillar = pillar
        self.audience = audience
        self.keywords = keywords or []
    
    def generate_youtube_script(self):
        """Generate YouTube video script with hook, structure, CTA"""
        
        scripts = {
            "tutorials": self._youtube_tutorial_template(),
            "case_study": self._youtube_case_study_template(),
            "agency_life": self._youtube_agency_template(),
            "industry": self._youtube_industry_template()
        }
        
        return scripts.get(self.pillar, scripts["tutorials"])
    
    def _youtube_tutorial_template(self):
        return f"""# 🎬 YouTube Script: {self.topic}

## HOOK (0:00 - 0:30)
[Direct to Camera, high energy]

"Most e-commerce brands are burning money on Meta Ads right now. 
Not because the algorithm changed—because they're making these 5 mistakes 
that are completely avoidable. In the next 10 minutes, I'll show you 
exactly what to fix."

[B-Roll: Screen recording of Ads Manager with wasted spend highlighted]

---

## INTRO (0:30 - 1:00)
[Direct to Camera]

"Hey, Deniz hier von adsdrop. Wir managen Meta Ads für D2C Brands 
und sehen diese Fehler Woche für Woche. Heute: {self.topic}."

[Lower Third: Name + Title]
[B-Roll: Quick office shots, team working]

---

## MAIN CONTENT (1:00 - 8:00)

### Mistake #1: [Specific Mistake]
[Screen Share: Show example in Ads Manager]
- Was ist das Problem?
- Warum kostet es Geld?
- Wie fixt man es?

[B-Roll: Close-up of clicking through interface]

### Mistake #2: [Specific Mistake]
...

### Mistake #3: [Specific Mistake]
...

### Mistake #4: [Specific Mistake]
...

### Mistake #5: [Specific Mistake]
...

---

## RECAP (8:00 - 9:00)
[Direct to Camera]

"Fassen wir zusammen:"
- [Quick bullet points on screen]
- "Fix diese 5 Dinge und du siehst Ergebnisse in 7-14 Tagen."

---

## CTA (9:00 - 10:00)
[Direct to Camera, energy up]

"Wenn dir das Video geholfen hat, drop einen Kommentar mit deinem 
größten Learning. Und falls du das Ganze nicht alleine machen willst—
wir nehmen nur 3 neue Kunden pro Monat auf. Link in der Beschreibung, 
Bewerbung über das Formular."

[End Screen: Subscribe button + Next video]

---

## B-ROLL SHOT LIST
- [ ] Office establishing shot
- [ ] Screen recordings (Ads Manager)
- [ ] Close-ups of clicking/typing
- [ ] Team working (authentic, not staged)
- [ ] Client results (anonymized dashboards)

## SEO
**Title:** {self.topic} | Meta Ads Tutorial 2026
**Description:** [Hook sentence] Timestamps below...
**Tags:** meta ads, facebook ads, ecommerce marketing, {', '.join(self.keywords)}
"""
    
    def _youtube_case_study_template(self):
        return f"""# 🎬 YouTube Script: {self.topic}

## HOOK (0:00 - 0:30)
"Wie wir einem Fashion Brand geholfen haben, von 50k auf 200k 
Monatsumsatz mit Meta Ads zu skalieren—ohne Budget zu erhöhen. 
Hier ist die komplette Strategie."

## STRUCTURE
1. Before State (Problem)
2. Strategy Overview  
3. Tactics & Execution
4. Results
5. Key Learnings

[Case Study specific script template...]
"""
    
    def _youtube_agency_template(self):
        return f"""# 🎬 YouTube Script: {self.topic}

## HOOK (0:00 - 0:30)
"Ein Tag im Leben eines Performance Marketing Teams. 
Spoiler: Es ist nicht so glamourös wie auf LinkedIn."

[Behind the scenes, authentic style]
"""
    
    def _youtube_industry_template(self):
        return f"""# 🎬 YouTube Script: {self.topic}

## HOOK (0:00 - 0:30)
"Meta hat gerade wieder den Algorithmus geändert. 
Hier ist was das für deine Ads bedeutet—und wie du davon profitierst."

[Timely, news-commentary style]
"""
    
    def generate_linkedin_posts(self):
        """Generate 3 LinkedIn posts"""
        
        long_form = f"""# 💼 LINKEDIN POST 1: Long-Form (Dienstag)

Most brands are overcomplicating Meta Ads.

Last week I posted a video about {self.topic}.

The response was wild—here's what I learned from 50+ comments:

1️⃣ **The #1 mistake:** [Key insight from video]

Most people focus on [wrong thing] when they should focus on [right thing].

It's not about [tactic A].
It's about [tactic B].

2️⃣ **The counter-intuitive truth:**

[Surprising insight that challenges conventional wisdom]

I see this with every new client:
- They think they need [complex solution]
- Reality: They need [simple solution]

3️⃣ **The 80/20:**

If I had to pick ONE thing to fix:

[Actionable, specific recommendation]

Everything else is optimization.
This is transformation.

---

**Personal Story:**

[Relatable anecdote about learning this lesson the hard way]

We spent [timeframe] figuring this out.
Now our clients see [result] consistently.

---

**Want the full breakdown?**

I recorded a 10-minute deep-dive covering all 5 mistakes:

[Link to YouTube video]

Drop a 🔥 if you want me to audit your current setup.

#MetaAds #Ecommerce #PerformanceMarketing #{self.keywords[0] if self.keywords else 'D2C'}
"""
        
        short = f"""# 💼 LINKEDIN POST 2: Short (Freitag)

"{self.topic}.

Most e-commerce brands waste 70% of their ad budget on the wrong creative.

Here's how to identify winners in 48h: [Link to video]"

---

**Alternative Short Formats:**

"3 signs your Meta Ads need help:

→ ROAS below 3.0
→ CAC increasing monthly  
→ No creative testing in 30 days

If you check 2/3, we should talk."

---

"Hot take: CBO is overrated.

Most brands should manual placements for 90 days before touching CBO.

Change my mind. 👇"
"""
        
        poll = f"""# 💼 LINKEDIN POST 3: Poll (optional)

"What's your biggest Meta Ads challenge right now?

🎯 Creative fatigue
📊 Attribution gaps  
💰 Rising CPMs
🔄 Landing page conversion

Comment with your situation—I'll reply with specific tactics."
"""
        
        return {"long_form": long_form, "short": short, "poll": poll}
    
    def generate_newsletter(self):
        """Generate weekly newsletter"""
        
        return f"""# 📧 NEWSLETTER: Weekly Digest

**Subject Line:** {self.topic} + This Week's Insights

---

Hi [First Name],

## 1. 🎥 THIS WEEK'S VIDEO

**{self.topic}**

[Video Thumbnail + Link]

Key takeaways:
• [Main point 1 from video]
• [Main point 2 from video]  
• [Main point 3 from video]

[Watch here →]

---

## 2. 💼 LINKEDIN HIGHLIGHTS

This week on LinkedIn:
• [Post 1 summary - 2 sentences]
• [Post 2 summary - 2 sentences]
• Most engaged comment: "[Quote]"

[Follow me on LinkedIn →]

---

## 3. 🛠️ TOOL RECOMMENDATION

**This week's tool:** [Tool Name]

Why: [One sentence value prop]

[Check it out →]

---

## 4. 🤔 QUESTION FOR YOU

[Engagement question related to video topic]

Hit reply and let me know!

---

Talk next week,
Deniz

P.S. [Fun fact or bonus tip related to topic]
"""
    
    def generate_shorts(self):
        """Generate 3 Shorts with timestamps"""
        
        return {
            "short_1": {
                "title": f"Best Hook: {self.topic}",
                "timestamp": "00:00 - 00:45",
                "caption": f"The #1 mistake killing your Meta Ads performance 💀\\n\\nFull video in bio 👆\\n\\n#metaads #facebookads #ecommerce #{self.keywords[0] if self.keywords else 'marketing'}",
                "hook": "Most brands burn money on Meta Ads because of this ONE mistake..."
            },
            "short_2": {
                "title": f"Key Insight: {self.topic}",
                "timestamp": "03:15 - 04:00", 
                "caption": f"This counter-intuitive Meta Ads strategy changed everything 📈\\n\\nFull breakdown in bio 👆\\n\\n#metaads #scaling #roas",
                "hook": "Stop doing this. Start doing THAT. Results in 7 days."
            },
            "short_3": {
                "title": f"Quick Tip: {self.topic}",
                "timestamp": "06:30 - 07:15",
                "caption": f"Meta Ads hack that took me 2 years to learn ⚡\\n\\nSave this for later ↗️\\n\\n#metaads #marketingtips #ecommerce",
                "hook": "Meta Ads pro-tip you won't find in courses..."
            }
        }

def generate_content(task_id=None, manual_input=None):
    """Main function to generate content"""
    
    clickup = ClickUpClient()
    
    # Get task info
    if task_id:
        task = clickup.get_task(task_id)
        topic = task.get("name", "")
        # Extract custom fields if available
        custom_fields = {f["name"]: f.get("value") for f in task.get("custom_fields", [])}
        pillar = custom_fields.get("Content Pillar", "tutorials")
        audience = custom_fields.get("Target Audience", "ecom")
        keywords = custom_fields.get("Keywords", "").split(",") if custom_fields.get("Keywords") else []
    else:
        topic = manual_input.get("title", "Content Topic")
        pillar = manual_input.get("pillar", "tutorials")
        audience = manual_input.get("audience", "ecom")
        keywords = manual_input.get("keywords", [])
    
    # Initialize generator
    generator = ContentGenerator(topic, pillar, audience, keywords)
    
    # Generate all content
    youtube_script = generator.generate_youtube_script()
    linkedin_posts = generator.generate_linkedin_posts()
    newsletter = generator.generate_newsletter()
    shorts = generator.generate_shorts()
    
    return {
        "youtube": youtube_script,
        "linkedin": linkedin_posts,
        "newsletter": newsletter,
        "shorts": shorts
    }

def post_to_clickup(task_id, content):
    """Post generated content to ClickUp as comments"""
    
    clickup = ClickUpClient()
    
    # Post YouTube Script
    clickup.add_comment(task_id, content["youtube"])
    
    # Post LinkedIn Posts
    for post_type, post_content in content["linkedin"].items():
        clickup.add_comment(task_id, post_content)
    
    # Post Newsletter
    clickup.add_comment(task_id, content["newsletter"])
    
    # Post Shorts
    shorts_content = "# 📱 SHORTS HOOKS\n\n"
    for short_key, short_data in content["shorts"].items():
        shorts_content += f"""## {short_data['title']}
**Timestamp:** {short_data['timestamp']}
**Hook:** {short_data['hook']}
**Caption:** {short_data['caption']}

---

"""
    clickup.add_comment(task_id, shorts_content)
    
    print(f"✅ Content posted to ClickUp task {task_id}")

def create_follow_up_tasks(list_id, topic, content):
    """Create follow-up tasks in other pipelines"""
    
    clickup = ClickUpClient()
    
    # Calculate due dates (assuming Monday start)
    today = datetime.now()
    tuesday = today + timedelta(days=1)
    wednesday = today + timedelta(days=2)
    thursday = today + timedelta(days=3)
    friday = today + timedelta(days=4)
    sunday = today + timedelta(days=6)
    
    # YouTube Task (no status - uses list default)
    clickup.create_task(
        LIST_YOUTUBE,
        f"🎬 {topic}",
        f"Script generated. Next: Recording.\n\n{content['youtube'][:500]}...",
        due_date=sunday,
        tags=["content-engine"]
    )
    
    # LinkedIn Tasks
    clickup.create_task(
        LIST_LINKEDIN,
        f"💼 LinkedIn Long-Form: {topic}",
        content["linkedin"]["long_form"][:500],
        due_date=tuesday,
        tags=["content-engine", "linkedin"]
    )
    
    clickup.create_task(
        LIST_LINKEDIN,
        f"💼 LinkedIn Short: {topic}",
        content["linkedin"]["short"][:500],
        due_date=friday,
        tags=["content-engine", "linkedin"]
    )
    
    # Newsletter Task
    clickup.create_task(
        LIST_NEWSLETTER,
        f"📧 Newsletter: {topic}",
        content["newsletter"][:500],
        due_date=thursday,
        tags=["content-engine", "newsletter"]
    )
    
    # Shorts Tasks
    for i, (short_key, short_data) in enumerate(content["shorts"].items(), 1):
        due = wednesday if i == 1 else (friday if i == 2 else sunday)
        clickup.create_task(
            LIST_SHORTS,
            f"📱 Short {i}: {short_data['title']}",
            f"Timestamp: {short_data['timestamp']}\nHook: {short_data['hook']}\n\nCaption: {short_data['caption']}",
            due_date=due,
            tags=["content-engine", "shorts"]
        )
    
    print("✅ Follow-up tasks created")

def main():
    parser = argparse.ArgumentParser(description="Content Engine Generator")
    parser.add_argument("--task-id", help="ClickUp task ID")
    parser.add_argument("--manual", action="store_true", help="Manual mode (no ClickUp)")
    parser.add_argument("--title", help="Content title/topic")
    parser.add_argument("--pillar", default="tutorials", help="Content pillar")
    parser.add_argument("--audience", default="ecom", help="Target audience")
    parser.add_argument("--keywords", help="Comma-separated keywords")
    parser.add_argument("--no-follow-up", action="store_true", help="Skip creating follow-up tasks")
    
    args = parser.parse_args()
    
    if args.manual:
        # Manual mode - just generate and print
        manual_input = {
            "title": args.title or "Meta Ads Content",
            "pillar": args.pillar,
            "audience": args.audience,
            "keywords": args.keywords.split(",") if args.keywords else []
        }
        content = generate_content(manual_input=manual_input)
        print(json.dumps(content, indent=2))
    elif args.task_id:
        # ClickUp mode
        print(f"🎬 Generating content for task {args.task_id}...")
        content = generate_content(task_id=args.task_id)
        post_to_clickup(args.task_id, content)
        
        if not args.no_follow_up:
            task = ClickUpClient().get_task(args.task_id)
            create_follow_up_tasks(LIST_CONTENT_IDEAS, task["name"], content)
        
        print("\n✅ Content Engine Complete!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
