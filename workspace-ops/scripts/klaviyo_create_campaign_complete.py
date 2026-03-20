#!/usr/bin/env python3
"""
Klaviyo Campaign Creator - VOLLSTÄNDIG AUTOMATISIERT
Erstellt Campaign + Template + Verknüpfung in einem Schritt!
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict

def create_complete_campaign(
    api_key: str,
    name: str,
    list_id: str,
    subject: str,
    preview_text: str,
    html_content: str,
    send_date: str,
    send_time: str = "09:00",
    from_email: str = "hello@razeco.de",
    from_label: str = "Razeco"
) -> Dict:
    """
    Vollständiger Workflow:
    1. Template erstellen
    2. Campaign erstellen
    3. Template zuweisen
    """
    
    send_datetime = f"{send_date}T{send_time}:00Z"
    
    # Step 1: Create Template
    print("📝 Erstelle Template...")
    template_data = {
        "data": {
            "type": "template",
            "attributes": {
                "name": f"{name} | {send_date}",
                "editor_type": "CODE",
                "html": html_content,
                "text": f"{subject}\n\nView in browser: https://razeco.de"
            }
        }
    }
    
    req = urllib.request.Request(
        'https://a.klaviyo.com/api/templates',
        data=json.dumps(template_data).encode('utf-8'),
        headers={
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'revision': '2024-10-15',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            template_result = json.loads(resp.read().decode('utf-8'))
            template_id = template_result['data']['id']
            print(f"   ✅ Template: {template_id}")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Fehler: {e.read().decode()}")
        return {'error': 'template_creation_failed'}
    
    # Step 2: Create Campaign
    print("📨 Erstelle Campaign...")
    campaign_data = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": f"{name} | {send_date}",
                "audiences": {"included": [list_id], "excluded": []},
                "send_strategy": {
                    "method": "static",
                    "options_static": {"datetime": send_datetime}
                },
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "channel": "email",
                            "label": "Default",
                            "content": {
                                "subject": subject,
                                "preview_text": preview_text,
                                "from_email": from_email,
                                "from_label": from_label
                            }
                        }
                    }]
                }
            }
        }
    }
    
    req = urllib.request.Request(
        'https://a.klaviyo.com/api/campaigns',
        data=json.dumps(campaign_data).encode('utf-8'),
        headers={
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'revision': '2024-10-15',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            campaign_result = json.loads(resp.read().decode('utf-8'))
            campaign_id = campaign_result['data']['id']
            message_id = campaign_result['data']['relationships']['campaign-messages']['data'][0]['id']
            print(f"   ✅ Campaign: {campaign_id}")
            print(f"   ✅ Message: {message_id}")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Fehler: {e.read().decode()}")
        return {'error': 'campaign_creation_failed', 'template_id': template_id}
    
    # Step 3: Assign Template to Campaign Message
    print("🔗 Verknüpfe Template mit Campaign...")
    assign_data = {
        "data": {
            "type": "campaign-message",
            "id": message_id,
            "relationships": {
                "template": {
                    "data": {
                        "type": "template",
                        "id": template_id
                    }
                }
            }
        }
    }
    
    req = urllib.request.Request(
        'https://a.klaviyo.com/api/campaign-message-assign-template',
        data=json.dumps(assign_data).encode('utf-8'),
        headers={
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'revision': '2024-10-15',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            assign_result = json.loads(resp.read().decode('utf-8'))
            assigned_template_id = assign_result['data']['relationships']['template']['data']['id']
            print(f"   ✅ Verknüpft: {assigned_template_id}")
    except urllib.error.HTTPError as e:
        print(f"   ❌ Fehler: {e.read().decode()}")
        return {
            'error': 'template_assignment_failed',
            'template_id': template_id,
            'campaign_id': campaign_id,
            'message_id': message_id
        }
    
    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_id,
        'message_id': message_id,
        'assigned_template_id': assigned_template_id,
        'url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Klaviyo Campaign Creator - Vollständig')
    parser.add_argument('--api-key', default=os.getenv('KLAVIYO_API_KEY'))
    parser.add_argument('--name', required=True)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--preview', required=True)
    parser.add_argument('--date', required=True, help='YYYY-MM-DD')
    parser.add_argument('--time', default='09:00')
    parser.add_argument('--html-file', required=True)
    parser.add_argument('--list-id', required=True)
    parser.add_argument('--from-email', default='hello@razeco.de')
    parser.add_argument('--from-label', default='Razeco')
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ API Key erforderlich")
        return
    
    print(f"\n{'='*60}")
    print(f"📧 Erstelle Newsletter: {args.name}")
    print(f"📅 Sendetermin: {args.date} {args.time}")
    print(f"{'='*60}\n")
    
    with open(args.html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    result = create_complete_campaign(
        api_key=args.api_key,
        name=args.name,
        list_id=args.list_id,
        subject=args.subject,
        preview_text=args.preview,
        html_content=html,
        send_date=args.date,
        send_time=args.time,
        from_email=args.from_email,
        from_label=args.from_label
    )
    
    if result.get('success'):
        print(f"\n{'='*60}")
        print("✅ ERFOLG! Campaign ist bereit!")
        print(f"{'='*60}")
        print(f"Template ID: {result['template_id']}")
        print(f"Campaign ID: {result['campaign_id']}")
        print(f"Message ID:  {result['message_id']}")
        print(f"\n🔗 Vorschau: {result['url']}")
        print(f"\n⚠️  WICHTIG: Campaign ist als DRAFT erstellt.")
        print(f"   Bitte in Klaviyo öffnen und auf 'Schedule' klicken.")
    else:
        print(f"\n❌ Fehler: {result.get('error')}")
        if 'campaign_id' in result:
            print(f"   Campaign wurde erstellt: {result['campaign_id']}")
            print(f"   Bitte Template manuell verknüpfen.")

if __name__ == '__main__':
    main()