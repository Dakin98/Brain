#!/usr/bin/env python3
"""
Klaviyo Flow Email Creator - Mit HTML Content
Flows erlauben Template-Zuweisung via API!
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict

def create_flow_with_email(
    api_key: str,
    name: str,
    list_id: str,
    subject: str,
    preview_text: str,
    html_content: str,
    from_email: str = "hello@razeco.de",
    from_label: str = "Razeco"
) -> Dict:
    """
    Erstellt einen Flow mit Email Action die direkt HTML enthält
    """
    
    # Step 1: Create Template
    template_data = {
        "data": {
            "type": "template",
            "attributes": {
                "name": name,
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
    
    # Step 2: Create Flow
    flow_data = {
        "data": {
            "type": "flow",
            "attributes": {
                "name": name,
                "status": "draft",
                "trigger_type": "schedule"  # Oder "list", "segment"
            }
        }
    }
    
    req = urllib.request.Request(
        'https://a.klaviyo.com/api/flows',
        data=json.dumps(flow_data).encode('utf-8'),
        headers={
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'revision': '2024-10-15',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            flow_result = json.loads(resp.read().decode('utf-8'))
            flow_id = flow_result['data']['id']
            print(f"✅ Flow created: {flow_id}")
    except urllib.error.HTTPError as e:
        print(f"❌ Flow error: {e.read().decode()}")
        return {'error': 'flow_creation_failed'}
    
    # Step 3: Create Flow Action (Email)
    action_data = {
        "data": {
            "type": "flow-action",
            "attributes": {
                "action_type": "EMAIL",
                "action": {
                    "template_id": template_id,  # Template wird hier zugewiesen!
                    "subject": subject,
                    "preview_text": preview_text,
                    "from_email": from_email,
                    "from_label": from_label
                }
            },
            "relationships": {
                "flow": {
                    "data": {
                        "type": "flow",
                        "id": flow_id
                    }
                }
            }
        }
    }
    
    req = urllib.request.Request(
        'https://a.klaviyo.com/api/flow-actions',
        data=json.dumps(action_data).encode('utf-8'),
        headers={
            'Authorization': f'Klaviyo-API-Key {api_key}',
            'revision': '2024-10-15',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            action_result = json.loads(resp.read().decode('utf-8'))
            action_id = action_result['data']['id']
            print(f"✅ Flow Action created: {action_id}")
            print(f"✅ Template successfully linked!")
    except urllib.error.HTTPError as e:
        error = e.read().decode()
        print(f"⚠️  Flow Action error: {error}")
        # Trotzdem erfolgreich - Template wurde erstellt
        return {
            'flow_id': flow_id,
            'template_id': template_id,
            'link_method': 'template_in_action',
            'status': 'partial'
        }
    
    return {
        'flow_id': flow_id,
        'template_id': template_id,
        'action_id': action_id,
        'link_method': 'template_in_action',
        'status': 'complete'
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Create Klaviyo Flow with Email')
    parser.add_argument('--api-key', default=os.getenv('KLAVIYO_API_KEY'))
    parser.add_argument('--name', required=True)
    parser.add_argument('--subject', required=True)
    parser.add_argument('--preview', required=True)
    parser.add_argument('--html-file', required=True)
    parser.add_argument('--list-id', required=True)
    parser.add_argument('--from-email', default='hello@razeco.de')
    parser.add_argument('--from-label', default='Razeco')
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("❌ API key required")
        return
    
    with open(args.html_file, 'r') as f:
        html = f.read()
    
    print(f"📧 Creating Flow: {args.name}")
    
    result = create_flow_with_email(
        api_key=args.api_key,
        name=args.name,
        list_id=args.list_id,
        subject=args.subject,
        preview_text=args.preview,
        html_content=html,
        from_email=args.from_email,
        from_label=args.from_label
    )
    
    if 'error' in result:
        print(f"\n❌ Failed: {result['error']}")
    else:
        print(f"\n{'='*50}")
        print(f"✅ SUCCESS!")
        print(f"{'='*50}")
        print(f"Flow ID: {result['flow_id']}")
        print(f"Template ID: {result['template_id']}")
        print(f"Status: {result['status']}")
        print(f"\n🔗 Open: https://www.klaviyo.com/flows/{result['flow_id']}")

if __name__ == '__main__':
    main()