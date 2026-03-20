#!/usr/bin/env python3
"""
Klaviyo Campaign Manager v2 - Mit Content-Workaround

Dieses Script nutzt einen alternativen Ansatz um Campaigns mit HTML Content zu erstellen.
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, Dict, List

def load_html_file(filepath: str) -> str:
    """Load HTML from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def create_campaign_with_html(
    api_key: str,
    name: str,
    list_id: str,
    subject: str,
    preview_text: str,
    html_content: str,
    send_datetime: str,
    from_email: str = "hello@razeco.de",
    from_label: str = "Razeco"
) -> Dict:
    """
    Create campaign and return IDs for manual linking instructions
    """
    
    # Step 1: Create Template
    template_data = {
        "data": {
            "type": "template",
            "attributes": {
                "name": f"{name} | {send_datetime[:10]}",
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
            print(f"✅ Template created: {template_id}")
    except urllib.error.HTTPError as e:
        print(f"❌ Template error: {e.read().decode()}")
        return {'error': 'template_creation_failed'}
    
    # Step 2: Create Campaign
    campaign_data = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": f"{name} | {send_datetime[:10]}",
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
            print(f"✅ Campaign created: {campaign_id}")
            print(f"✅ Message ID: {message_id}")
    except urllib.error.HTTPError as e:
        print(f"❌ Campaign error: {e.read().decode()}")
        return {'error': 'campaign_creation_failed'}
    
    # Step 3: Try to link via alternative methods
    print("\n🔗 Attempting to link template to campaign...")
    
    # Method A: Try to use render_options with template reference
    render_patch = {
        "data": {
            "type": "campaign-message",
            "id": message_id,
            "attributes": {
                "render_options": {
                    "template_id": template_id
                }
            }
        }
    }
    
    req = urllib.request.Request(
        f'https://a.klaviyo.com/api/campaign-messages/{message_id}',
        data=json.dumps(render_patch).encode('utf-8'),
        headers={
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'revision': '2024-10-15',
            'Content-Type': 'application/json'
        },
        method='PATCH'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"✅ Linked via render_options!")
            link_method = "render_options"
    except urllib.error.HTTPError:
        print(f"⚠️  Could not auto-link (expected)")
        link_method = "manual"
    
    return {
        'template_id': template_id,
        'campaign_id': campaign_id,
        'message_id': message_id,
        'link_method': link_method,
        'manual_link_url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

def main():
    """CLI for creating campaigns with content"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create Klaviyo Campaign with HTML')
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
    parser.add_argument('--auto-open', action='store_true', help='Try to open browser for manual linking')
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ Error: API key required")
        sys.exit(1)
    
    # Load HTML
    print(f"📄 Loading HTML from: {args.html_file}")
    try:
        html = load_html_file(args.html_file)
    except FileNotFoundError:
        print(f"❌ File not found: {args.html_file}")
        sys.exit(1)
    
    # Create campaign
    print(f"\n📧 Creating campaign: {args.name}")
    print(f"📅 Send date: {args.date} {args.time}")
    
    send_datetime = f"{args.date}T{args.time}:00Z"
    
    result = create_campaign_with_html(
        api_key=args.api_key,
        name=args.name,
        list_id=args.list_id,
        subject=args.subject,
        preview_text=args.preview,
        html_content=html,
        send_datetime=send_datetime,
        from_email=args.from_email,
        from_label=args.from_label
    )
    
    if 'error' in result:
        print(f"\n❌ Failed: {result['error']}")
        sys.exit(1)
    
    # Output result
    print(f"\n{'='*50}")
    print(f"✅ SUCCESS!")
    print(f"{'='*50}")
    print(f"Template ID: {result['template_id']}")
    print(f"Campaign ID: {result['campaign_id']}")
    print(f"Message ID:  {result['message_id']}")
    print(f"Link Method: {result['link_method']}")
    print(f"\n🔗 Link URL: {result['manual_link_url']}")
    
    if result['link_method'] == 'manual':
        print(f"\n⚠️  MANUAL STEP REQUIRED:")
        print(f"   1. Visit: {result['manual_link_url']}")
        print(f"   2. Click 'Edit Content'")
        print(f"   3. Select template: '{args.name} | {args.date}'")
        print(f"   4. Save & Schedule")
    
    # Try to open browser
    if args.auto_open and result['link_method'] == 'manual':
        print(f"\n🌐 Opening browser...")
        import webbrowser
        webbrowser.open(result['manual_link_url'])
    
    # Save result to file
    result_file = f"/tmp/klaviyo_campaign_{result['campaign_id']}.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Result saved to: {result_file}")

if __name__ == '__main__':
    main()