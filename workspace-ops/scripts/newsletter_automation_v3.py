#!/usr/bin/env python3
"""
Newsletter Automation v3 - COMPLETE

Erstellt automatisch Newsletter Campaigns für Razeco aus Notion-Themen.
Vollständig automatisiert inkl. Template-Verknüpfung!

Usage:
    python newsletter_automation_v3.py
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
KLAVIYO_API_KEY = os.getenv('KLAVIYO_API_KEY', 'pk_dfc4dd8deb22827d0244a251f315db13c3')
LIST_ID = 'ThKApp'
BASE_DIR = '/Users/denizakin/.openclaw/workspace'

def load_html_template(filename: str) -> str:
    """Load HTML from newsletters directory"""
    filepath = os.path.join(BASE_DIR, 'newsletters', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def api_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """Make Klaviyo API request"""
    url = f'https://a.klaviyo.com/api{endpoint}'
    headers = {
        'Authorization': f'Klaviyo-API-Key {KLAVIYO_API_KEY}',
        'revision': '2024-10-15',
        'Content-Type': 'application/json'
    }
    
    req_data = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ API Error {e.code}: {error_body[:200]}")
        return {'error': error_body}

def create_template(name: str, html: str, text: str) -> Optional[str]:
    """Create email template"""
    result = api_request('POST', '/templates', {
        'data': {
            'type': 'template',
            'attributes': {
                'name': name,
                'editor_type': 'CODE',
                'html': html,
                'text': text
            }
        }
    })
    if 'error' in result:
        return None
    return result['data']['id']

def create_campaign(name: str, subject: str, preview: str, send_datetime: str) -> Optional[Dict]:
    """Create campaign with message"""
    result = api_request('POST', '/campaigns', {
        'data': {
            'type': 'campaign',
            'attributes': {
                'name': name,
                'audiences': {'included': [LIST_ID], 'excluded': []},
                'send_strategy': {
                    'method': 'static',
                    'options_static': {'datetime': send_datetime}
                },
                'campaign-messages': {
                    'data': [{
                        'type': 'campaign-message',
                        'attributes': {
                            'channel': 'email',
                            'label': 'Default',
                            'content': {
                                'subject': subject,
                                'preview_text': preview,
                                'from_email': 'hello@razeco.de',
                                'from_label': 'Razeco'
                            }
                        }
                    }]
                }
            }
        }
    })
    if 'error' in result:
        return None
    
    return {
        'campaign_id': result['data']['id'],
        'message_id': result['data']['relationships']['campaign-messages']['data'][0]['id']
    }

def assign_template_to_campaign(message_id: str, template_id: str) -> Optional[str]:
    """Assign template to campaign message"""
    result = api_request('POST', '/campaign-message-assign-template', {
        'data': {
            'type': 'campaign-message',
            'id': message_id,
            'relationships': {
                'template': {
                    'data': {
                        'type': 'template',
                        'id': template_id
                    }
                }
            }
        }
    })
    if 'error' in result:
        return None
    return result['data']['relationships']['template']['data']['id']

def create_newsletter(newsletter_config: Dict) -> Dict:
    """Complete workflow: Template → Campaign → Link"""
    name = newsletter_config['name']
    date = newsletter_config['date']
    
    print(f"\n{'='*60}")
    print(f"📧 Creating: {name}")
    print(f"{'='*60}")
    
    # Step 1: Create Template
    print("1️⃣ Creating template...")
    template_id = create_template(
        name=f"{name} | {date}",
        html=newsletter_config['html'],
        text=newsletter_config['text']
    )
    if not template_id:
        return {'error': 'template_creation_failed'}
    print(f"   ✅ Template: {template_id}")
    
    # Step 2: Create Campaign
    print("2️⃣ Creating campaign...")
    campaign_result = create_campaign(
        name=f"{name} | {date}",
        subject=newsletter_config['subject'],
        preview=newsletter_config['preview'],
        send_datetime=f"{date}T{newsletter_config['time']}:00Z"
    )
    if not campaign_result:
        return {'error': 'campaign_creation_failed', 'template_id': template_id}
    print(f"   ✅ Campaign: {campaign_result['campaign_id']}")
    print(f"   ✅ Message: {campaign_result['message_id']}")
    
    # Step 3: Assign Template
    print("3️⃣ Linking template...")
    assigned_id = assign_template_to_campaign(
        campaign_result['message_id'],
        template_id
    )
    if not assigned_id:
        return {
            'error': 'assignment_failed',
            'template_id': template_id,
            'campaign_id': campaign_result['campaign_id']
        }
    print(f"   ✅ Linked: {assigned_id}")
    
    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_result['campaign_id'],
        'message_id': campaign_result['message_id'],
        'assigned_template_id': assigned_id,
        'url': f"https://www.klaviyo.com/campaign/{campaign_result['campaign_id']}/edit"
    }

def main():
    """Main automation workflow"""
    print("\n" + "="*60)
    print("🚀 NEWSLETTER AUTOMATION v3 - COMPLETE")
    print("="*60)
    
    # Newsletter configurations for this week
    newsletters = [
        {
            'name': 'Razeco | Unsere Empfehlungen',
            'subject': 'Unsere Empfehlungen für dich 🌱',
            'preview': 'Die besten Produkte für deine perfekte Rasur',
            'date': '2026-02-26',
            'time': '10:00',
            'html': load_html_template('razeco_recommended_products.html'),
            'text': 'Unsere Empfehlungen für dich\n\nEntdecke unsere besten Produkte!'
        },
        {
            'name': 'Razeco | Häufig gestellte Fragen',
            'subject': 'Deine Fragen, unsere Antworten ❓',
            'preview': 'Alles, was du über Razeco wissen musst',
            'date': '2026-02-27',
            'time': '10:00',
            'html': load_html_template('razeco_faq.html'),
            'text': 'Häufig gestellte Fragen\n\nHier beantworten wir deine Fragen!'
        },
        {
            'name': 'Razeco | Die Zukunft der Rasur',
            'subject': 'Stell dir eine Welt ohne Plastikmüll vor 🌍',
            'preview': 'Die Zukunft der Rasur beginnt jetzt',
            'date': '2026-02-28',
            'time': '10:00',
            'html': load_html_template('razeco_show_the_future.html'),
            'text': 'Die Zukunft der Rasur\n\nGemeinsam für eine nachhaltige Welt!'
        }
    ]
    
    # Process each newsletter
    results = []
    for newsletter in newsletters:
        result = create_newsletter(newsletter)
        results.append({
            'name': newsletter['name'],
            'date': newsletter['date'],
            **result
        })
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    success_count = sum(1 for r in results if r.get('success'))
    print(f"✅ Successfully created: {success_count}/{len(newsletters)}\n")
    
    for result in results:
        status = "✅" if result.get('success') else "❌"
        print(f"{status} {result['name']} | {result['date']}")
        if result.get('success'):
            print(f"   Campaign: {result['campaign_id']}")
            print(f"   URL: {result['url']}")
        elif 'error' in result:
            print(f"   Error: {result['error']}")
        print()
    
    print("⚠️  Remember: Campaigns are created as DRAFTS.")
    print("   Please review and schedule in Klaviyo UI before send date.")
    print("="*60)
    
    return results

if __name__ == '__main__':
    main()