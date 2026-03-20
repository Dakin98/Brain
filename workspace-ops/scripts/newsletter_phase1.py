#!/usr/bin/env python3
"""
Newsletter Engine v4 — PHASE 1: Briefing Generator

Fast, lightweight script that runs as cronjob.
Creates briefing JSONs for AI content generation.

Output: ~/.openclaw/workspace/newsletters/briefings/*.json
Each briefing contains all data needed for content generation.
"""

import os
import sys
import json
import urllib.request
from datetime import datetime, timedelta
from typing import Dict, List

# ─── Config ─────────────────────────────────────────────────────────────────
NOTION_API_KEY = open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
NOTION_DB_ID = '3465a32b-e5e0-4d52-bec3-c24ff39e1507'
AIRTABLE_TOKEN = os.environ.get('MATON_API_KEY', '')
AIRTABLE_BASE = 'appbGhxy9I18oIS8E'
AIRTABLE_GATEWAY = 'https://gateway.maton.ai/airtable/v0'
BRIEFING_DIR = os.path.join(os.path.dirname(__file__), '..', 'newsletters', 'briefings')

def notion_api(method: str, path: str, data: dict = None) -> dict:
    url = f'https://api.notion.com/v1{path}'
    headers = {'Authorization': f'Bearer {NOTION_API_KEY}', 'Notion-Version': '2022-06-28', 'Content-Type': 'application/json'}
    req = urllib.request.Request(url, headers=headers, method=method)
    if data: req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        print(f'  ❌ Notion error: {e}')
        return {}

def airtable_api(method: str, path: str, data: dict = None) -> dict:
    url = f'{AIRTABLE_GATEWAY}/{path}'
    headers = {'Authorization': f'Bearer {AIRTABLE_TOKEN}', 'Content-Type': 'application/json'}
    req = urllib.request.Request(url, headers=headers, method=method)
    if data: req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        print(f'  ❌ Airtable error: {e}')
        return {}

def get_weekly_topics(week_offset: int = 0) -> List[Dict]:
    """Fetch newsletter topics for target week"""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    sunday = monday + timedelta(days=6)
    start_date = monday.strftime('%Y-%m-%d')
    end_date = sunday.strftime('%Y-%m-%d')
    
    print(f'📅 Notion: Themen für {start_date} bis {end_date}')
    
    data = notion_api('POST', f'/databases/{NOTION_DB_ID}/query', {
        'filter': {
            'and': [
                {'property': 'Date', 'date': {'on_or_after': start_date}},
                {'property': 'Date', 'date': {'on_or_before': end_date}}
            ]
        },
        'sorts': [{'property': 'Date', 'direction': 'ascending'}]
    })
    
    topics = []
    for page in data.get('results', []):
        props = page['properties']
        name = ''.join([t.get('plain_text', '') for t in props.get('Name', {}).get('title', [])])
        date_prop = props.get('Date', {}).get('date', {})
        date = date_prop.get('start', '') if date_prop else ''
        topics.append({'page_id': page['id'], 'name': name.strip(), 'date': date})
    
    print(f'  ✅ {len(topics)} Themen')
    return topics

def enrich_topic_content(topic: Dict) -> Dict:
    """Fetch briefing text and example images from Notion page"""
    data = notion_api('GET', f'/blocks/{topic["page_id"]}/children?page_size=100')
    
    briefing_parts = []
    images = []
    
    for block in data.get('results', []):
        btype = block['type']
        
        if btype in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 
                      'bulleted_list_item', 'callout', 'quote', 'numbered_list_item']:
            rich_text = block[btype].get('rich_text', [])
            text = ''.join([t.get('plain_text', '') for t in rich_text])
            if text:
                if btype == 'callout':
                    briefing_parts.append(f'CALLOUT: {text}')
                elif btype.startswith('heading'):
                    briefing_parts.append(f'HEADING: {text}')
                elif btype == 'bulleted_list_item':
                    briefing_parts.append(f'BULLET: {text}')
                else:
                    briefing_parts.append(text)
        
        elif btype == 'image':
            img = block['image']
            url = img.get('file', {}).get('url') or img.get('external', {}).get('url', '')
            if url:
                images.append({'url': url, 'type': 'example_email_design'})
    
    topic['briefing_instructions'] = '\n'.join(briefing_parts)
    topic['example_images'] = images
    return topic

def get_newsletter_clients() -> List[Dict]:
    """Fetch active clients with newsletter service enabled"""
    print(f'\n📊 Airtable: Newsletter-Kunden')
    
    # Get all Kunden (simpler, filter client-side)
    data = airtable_api('GET', f'{AIRTABLE_BASE}/Kunden?maxRecords=50')
    
    clients = []
    for record in data.get('records', []):
        f = record['fields']
        # Check criteria
        status = f.get('Status', '')
        newsletter_service = f.get('Newsletter Service', False)
        klaviyo_key = f.get('Klaviyo API Key', '')
        
        if status != 'Aktiv' or not newsletter_service or not klaviyo_key:
            continue
        
        client = {
            'id': record['id'],
            'name': f.get('Firmenname', ''),
            'website': f.get('Website', ''),
            'klaviyo_api_key': klaviyo_key,
            'klaviyo_list_id': f.get('Klaviyo List ID', ''),
            'email_language': f.get('Email Sprache', 'de'),
            'brand_assets_ids': f.get('Brand Assets', []),
            'product_info_ids': f.get('Produkt-Info', []),
            'target_audience': f.get('Branche', ''),
        }
        clients.append(client)
    
    # Enrich with Brand Assets
    for client in clients:
        for asset_id in client.get('brand_assets_ids', []):
            asset = airtable_api('GET', f'{AIRTABLE_BASE}/Brand%20Assets/{asset_id}')
            if asset:
                af = asset.get('fields', {})
                client['brand'] = {
                    'colors_hex': af.get('Farbcodes', ''),
                    'colors_list': [c.strip() for c in af.get('Farbcodes', '').split(',') if c.strip().startswith('#')],
                    'fonts': af.get('Schriftarten', ''),
                    'tone': af.get('Tonalität', ''),
                    'tagline': af.get('Brand Tagline', ''),
                    'logo_url': af.get('Logo URL', ''),
                }
                break
        if 'brand' not in client:
            client['brand'] = {'colors_hex': '', 'colors_list': [], 'fonts': '', 'tone': '', 'tagline': '', 'logo_url': ''}
    
    # Enrich with Product Info
    for client in clients:
        for prod_id in client.get('product_info_ids', []):
            prod = airtable_api('GET', f'{AIRTABLE_BASE}/Produkt-Info/{prod_id}')
            if prod:
                pf = prod.get('fields', {})
                client['products'] = {
                    'description': pf.get('Produktbeschreibung', ''),
                    'target_audience': pf.get('Zielgruppe', ''),
                    'usps': pf.get('USPs / Vorteile', ''),
                    'top_products': pf.get('Top-Produkte', ''),
                    'social_proof': pf.get('Social Proof', ''),
                }
                # Try to parse products_json if exists
                try:
                    pj = pf.get('Produkte JSON', '')
                    if pj:
                        client['products']['json'] = json.loads(pj)
                except:
                    client['products']['json'] = {}
                break
        if 'products' not in client:
            client['products'] = {'description': '', 'target_audience': '', 'usps': '', 'top_products': '', 'social_proof': '', 'json': {}}
    
    print(f'  ✅ {len(clients)} Kunden bereit')
    return clients

def create_briefing(client: Dict, topic: Dict) -> Dict:
    """Create comprehensive briefing for AI content generation"""
    
    briefing = {
        # Metadata
        'briefing_id': f"{client['name'].lower().replace(' ', '_')}_{topic['date']}",
        'created_at': datetime.now().isoformat(),
        'status': 'pending',  # pending → generating → done
        
        # Client Info
        'client': {
            'name': client['name'],
            'website': client['website'],
            'target_audience': client.get('target_audience', '') or client['products'].get('target_audience', ''),
            'language': client['email_language'],
        },
        
        # Newsletter Topic
        'topic': {
            'name': topic['name'],
            'date': topic['date'],
            'briefing_instructions': topic['briefing_instructions'],
            'example_images': topic['example_images'],
        },
        
        # Brand Assets
        'brand': {
            'colors': {
                'hex_string': client['brand']['colors_hex'],
                'primary': client['brand']['colors_list'][0] if client['brand']['colors_list'] else '#333333',
                'secondary': client['brand']['colors_list'][1] if len(client['brand']['colors_list']) > 1 else '#666666',
                'accent': client['brand']['colors_list'][2] if len(client['brand']['colors_list']) > 2 else '#0066CC',
            },
            'fonts': client['brand']['fonts'],
            'tone': client['brand']['tone'],
            'tagline': client['brand']['tagline'],
            'logo_url': client['brand']['logo_url'],
        },
        
        # Products
        'products': {
            'description': client['products']['description'],
            'usps': client['products']['usps'],
            'top_products': client['products']['top_products'],
            'social_proof': client['products']['social_proof'],
            'product_data': client['products'].get('json', {}),
        },
        
        # Klaviyo
        'klaviyo': {
            'api_key': client['klaviyo_api_key'],
            'list_id': client['klaviyo_list_id'],
        },
        
        # Output placeholders (to be filled by Phase 2)
        'output': {
            'subject_line': '',
            'preview_text': '',
            'email_body_html': '',
            'email_body_text': '',
            'klaviyo_template_id': '',
            'klaviyo_campaign_id': '',
            'klaviyo_url': '',
        }
    }
    
    return briefing

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--week-offset', type=int, default=0)
    args = parser.parse_args()
    
    print('=' * 60)
    print('📧 NEWSLETTER ENGINE — Phase 1: Briefing Generator')
    print(f'   {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print('=' * 60)
    
    # Ensure briefing directory exists
    os.makedirs(BRIEFING_DIR, exist_ok=True)
    
    # Step 1: Get topics from Notion
    topics = get_weekly_topics(args.week_offset)
    if not topics:
        print('\n⚠️  Keine Themen für diese Woche')
        return
    
    # Enrich topics with content
    print(f'\n📖 Lade Briefings...')
    for topic in topics:
        enrich_topic_content(topic)
    
    # Step 2: Get clients from Airtable
    clients = get_newsletter_clients()
    if not clients:
        print('\n⚠️  Keine Newsletter-Kunden')
        return
    
    # Step 3: Create briefings
    print(f'\n🔨 Erstelle Briefings...')
    created = []
    
    for client in clients:
        for topic in topics:
            briefing = create_briefing(client, topic)
            
            # Save to file
            filename = f"{briefing['briefing_id']}.json"
            filepath = os.path.join(BRIEFING_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(briefing, f, indent=2, ensure_ascii=False)
            
            created.append({
                'client': client['name'],
                'topic': topic['name'],
                'date': topic['date'],
                'file': filename,
                'path': filepath,
            })
            
            print(f'  ✅ {filename}')
    
    # Summary
    print('\n' + '=' * 60)
    print(f'📊 {len(created)} Briefings erstellt')
    print('=' * 60)
    
    for c in created:
        print(f'  📄 {c["client"]} | {c["date"]} | {c["topic"]}')
    
    print(f'\n📁 Gespeichert in: {BRIEFING_DIR}')
    print('\nNächster Schritt: Phase 2 — Content Generation')
    print('  python3 newsletter_phase2.py --briefing BRIEFING_ID.json')
    print('=' * 60)

if __name__ == '__main__':
    main()
