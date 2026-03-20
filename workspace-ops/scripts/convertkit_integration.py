#!/usr/bin/env python3
"""
ConvertKit Integration for Content Engine
Create and send newsletters from generated content

Usage:
    python3 convertkit_integration.py --create-broadcast --subject "Subject" --content "HTML Content"
    python3 convertkit_integration.py --list-subscribers
    python3 convertkit_integration.py --create-from-clickup --task-id "TASK_ID"
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta

CONVERTKIT_API_BASE = "https://api.kit.com/v4"

def get_api_key():
    """Get ConvertKit API key from config"""
    config_path = os.path.expanduser("~/.config/convertkit/api_key")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return f.read().strip()
    return os.environ.get("CONVERTKIT_API_KEY")

def convertkit_request(method, endpoint, data=None):
    """Make ConvertKit API request"""
    api_key = get_api_key()
    headers = {
        "X-Kit-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    url = f"{CONVERTKIT_API_BASE}{endpoint}"
    req = urllib.request.Request(url, headers=headers, method=method)
    
    if data and method in ["POST", "PUT"]:
        req.data = json.dumps(data).encode()
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Error {e.code}: {error_body[:500]}")
        return None

def get_account_info():
    """Get account information"""
    return convertkit_request("GET", "/account")

def list_broadcasts():
    """List all broadcasts"""
    return convertkit_request("GET", "/broadcasts")

def create_broadcast(subject, content, description=""):
    """Create a new broadcast (newsletter)"""
    data = {
        "subject": subject,
        "content": content,
        "description": description or subject,
        "public": False
    }
    return convertkit_request("POST", "/broadcasts", data)

def get_broadcast(broadcast_id):
    """Get broadcast details"""
    return convertkit_request("GET", f"/broadcasts/{broadcast_id}")

def publish_broadcast(broadcast_id):
    """Publish/send a broadcast"""
    return convertkit_request("POST", f"/broadcasts/{broadcast_id}/publish")

def list_subscribers():
    """List subscribers"""
    return convertkit_request("GET", "/subscribers")

def get_subscriber_count():
    """Get total subscriber count"""
    result = list_subscribers()
    if result:
        return result.get("pagination", {}).get("total", 0)
    return 0

def create_newsletter_from_content(topic, youtube_title, youtube_url="", linkedin_highlights=None, tool_rec=None):
    """Create a newsletter from content engine output"""
    
    linkedin_section = ""
    if linkedin_highlights:
        linkedin_section = "## 💼 LINKEDIN HIGHLIGHTS\n\n"
        for post in linkedin_highlights[:3]:
            linkedin_section += f"• {post}\n"
        linkedin_section += "\n"
    
    tool_section = ""
    if tool_rec:
        tool_section = f"""## 🛠️ TOOL EMPFEHLUNG

**{tool_rec['name']}**

{tool_rec['description']}

[Mehr erfahren →]({tool_rec['url']})

---

"""
    
    content = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">

<h2 style="color: #1a1a1a;">🎥 DIESES VIDEO</h2>

<p><strong>{youtube_title}</strong></p>

<p>Diese Woche habe ich ein neues Video zu <strong>{topic}</strong> veröffentlicht.</p>

<p>Hier sind die Key Takeaways:</p>

<ul>
<li>Main insight from video</li>
<li>Practical tip you can implement today</li>
<li>Common mistake to avoid</li>
</ul>

<p><a href="{youtube_url}" style="display: inline-block; background: #000; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 4px;">Video ansehen →</a></p>

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

{linkedin_section}

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

{tool_section}

<h2>🤔 FRAGE AN DICH</h2>

<p>Was ist dein größtes Meta Ads Problem gerade?</p>

<p>Reply auf diese Email — ich lese jede Antwort!</p>

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

<p>Talk next week,<br>
<strong>Deniz</strong></p>

<p style="font-size: 12px; color: #666; margin-top: 30px;">
P.S. Wir nehmen 2 neue Kunden im März auf. Wenn du skalieren willst: <a href="https://adsdrop.de">Hier bewerben</a>
</p>

</div>
</body>
</html>"""
    
    return content

def main():
    parser = argparse.ArgumentParser(description="ConvertKit Integration")
    parser.add_argument("--account", action="store_true", help="Get account info")
    parser.add_argument("--list-broadcasts", action="store_true", help="List broadcasts")
    parser.add_argument("--list-subscribers", action="store_true", help="List subscribers")
    parser.add_argument("--subscriber-count", action="store_true", help="Get subscriber count")
    parser.add_argument("--create-broadcast", action="store_true", help="Create broadcast")
    parser.add_argument("--subject", help="Broadcast subject")
    parser.add_argument("--content", help="Broadcast HTML content")
    parser.add_argument("--description", help="Broadcast description")
    parser.add_argument("--publish", help="Publish broadcast by ID")
    parser.add_argument("--create-from-clickup", action="store_true", help="Create from ClickUp task")
    parser.add_argument("--task-id", help="ClickUp task ID")
    
    args = parser.parse_args()
    
    if args.account:
        result = get_account_info()
        print(json.dumps(result, indent=2))
    
    elif args.list_broadcasts:
        result = list_broadcasts()
        print(json.dumps(result, indent=2))
    
    elif args.list_subscribers:
        result = list_subscribers()
        print(json.dumps(result, indent=2))
    
    elif args.subscriber_count:
        count = get_subscriber_count()
        print(f"Total subscribers: {count}")
    
    elif args.create_broadcast:
        if not args.subject or not args.content:
            print("❌ --subject and --content required")
            sys.exit(1)
        result = create_broadcast(args.subject, args.content, args.description)
        if result:
            print(f"✅ Broadcast created: {result.get('id')}")
            print(json.dumps(result, indent=2))
    
    elif args.publish:
        result = publish_broadcast(args.publish)
        if result:
            print(f"✅ Broadcast published: {args.publish}")
    
    elif args.create_from_clickup:
        print("🎬 Creating newsletter from ClickUp task...")
        # This would integrate with ClickUp to get content
        # For now, create a template newsletter
        content = create_newsletter_from_content(
            topic="Meta Ads Optimization",
            youtube_title="5 Meta Ads Fehler die dich Geld kosten",
            youtube_url="https://youtube.com/watch?v=..."
        )
        result = create_broadcast(
            subject="5 Meta Ads Fehler — Diese Woche im Video",
            content=content,
            description="Weekly newsletter with video highlights"
        )
        if result:
            print(f"✅ Newsletter created: {result.get('id')}")
    
    else:
        # Test connection
        print("🎬 ConvertKit Integration")
        print("=" * 50)
        account = get_account_info()
        if account:
            print(f"✅ Connected to: {account.get('name', 'Unknown')}")
            count = get_subscriber_count()
            print(f"📧 Subscribers: {count}")
        else:
            print("❌ Connection failed")
            sys.exit(1)

if __name__ == "__main__":
    main()
