#!/usr/bin/env python3
"""
Newsletter Engine v6 — FULLY AUTOMATED, AI-POWERED

Runs every Friday for next week's newsletters.
Notion topics → Airtable clients → AI copy → HTML → Klaviyo draft campaigns.

Usage:
    python3 newsletter_engine_v6.py                    # Next week (default)
    python3 newsletter_engine_v6.py --week-offset 2    # 2 weeks ahead
    python3 newsletter_engine_v6.py --client "Razeco"  # Single client
    python3 newsletter_engine_v6.py --dry-run           # Preview without publishing
"""

import os
import sys
import json
import urllib.request
import urllib.error
import hashlib
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════

NOTION_API_KEY = open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
NOTION_DB_ID = '3465a32b-e5e0-4d52-bec3-c24ff39e1507'
AIRTABLE_TOKEN = os.environ.get('MATON_API_KEY', '')
AIRTABLE_BASE = 'appbGhxy9I18oIS8E'
AIRTABLE_GATEWAY = 'https://gateway.maton.ai/airtable/v0'
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
if not ANTHROPIC_API_KEY:
    _ak = os.path.expanduser('~/.config/anthropic/api_key')
    if os.path.exists(_ak):
        ANTHROPIC_API_KEY = open(_ak).read().strip()
WORKSPACE = Path(os.path.dirname(__file__)).parent
NEWSLETTERS_DIR = WORKSPACE / 'newsletters'
BRIEFINGS_DIR = NEWSLETTERS_DIR / 'briefings'
LOG_FILE = NEWSLETTERS_DIR / 'last_run.json'

# Razeco product catalog (fallback if not in Airtable)
KNOWN_PRODUCTS = {
    'Razeco UG': {
        'system_razor_face': {
            'name': 'System Razor · Face', 'price': '24.99',
            'url': 'https://www.razeco.com/en-de/products/system-razor-face',
            'image': 'https://www.razeco.com/cdn/shop/files/face_razor_updated.png',
            'desc': 'Biobasierter Rasierer für das Gesicht', 'badge': None
        },
        'system_razor_body': {
            'name': 'System Razor · Body', 'price': '24.99',
            'url': 'https://www.razeco.com/en-de/products/system-razor-body',
            'image': 'https://www.razeco.com/cdn/shop/files/body_Razor_for_website_e079db2b-5f45-4c5b-bbf0-55b65257099c.png',
            'desc': 'Biobasierter Rasierer für den Körper', 'badge': None
        },
        'system_bundle': {
            'name': 'System Bundle', 'price': '37.96', 'original_price': '49.98',
            'url': 'https://www.razeco.com/en-de/products/system-bundle',
            'image': 'https://www.razeco.com/cdn/shop/files/Frame1533211901.png',
            'desc': 'Face + Body — Du sparst €12', 'badge': 'BESTSELLER'
        },
        'oneway_rose': {
            'name': 'Oneway Rosé', 'price': '9.99',
            'url': 'https://www.razeco.com/en-de/products/oneway-rose',
            'image': 'https://www.razeco.com/cdn/shop/files/Razor_Single_Use2.png',
            'desc': 'Der nachhaltige Einwegrasierer', 'badge': None
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# API HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def notion_api(method: str, path: str, data: dict = None) -> dict:
    url = f'https://api.notion.com/v1{path}'
    headers = {'Authorization': f'Bearer {NOTION_API_KEY}', 'Notion-Version': '2022-06-28', 'Content-Type': 'application/json'}
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        print(f'  ❌ Notion error: {e}')
        return {}

def airtable_api(method: str, path: str, data: dict = None) -> dict:
    url = f'{AIRTABLE_GATEWAY}/{path}'
    headers = {'Authorization': f'Bearer {AIRTABLE_TOKEN}', 'Content-Type': 'application/json'}
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        print(f'  ❌ Airtable error: {e}')
        return {}

def klaviyo_api(api_key: str, method: str, endpoint: str, data: dict = None) -> dict:
    url = f'https://a.klaviyo.com/api{endpoint}'
    headers = {'Authorization': f'Klaviyo-API-Key {api_key}', 'revision': '2024-10-15', 'Content-Type': 'application/json'}
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  ❌ Klaviyo {e.code}: {body[:200]}')
        return {'error': body}

def openai_chat(system: str, user: str, model: str = 'gpt-4o', temperature: float = 0.7) -> str:
    """Call OpenAI Chat API and return assistant message content."""
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'temperature': temperature,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user}
        ]
    }
    req = urllib.request.Request(url, headers=headers, method='POST')
    req.data = json.dumps(payload).encode()
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        return resp['choices'][0]['message']['content']
    except Exception as e:
        print(f'  ❌ OpenAI error: {e}')
        return ''


def anthropic_chat(system: str, user: str, model: str = 'claude-sonnet-4-20250514', temperature: float = 0.7) -> str:
    """Call Anthropic Messages API and return assistant message content."""
    url = 'https://api.anthropic.com/v1/messages'
    headers = {
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'max_tokens': 2000,
        'temperature': temperature,
        'system': system,
        'messages': [{'role': 'user', 'content': user}]
    }
    req = urllib.request.Request(url, headers=headers, method='POST')
    req.data = json.dumps(payload).encode()
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        return resp['content'][0]['text']
    except Exception as e:
        print(f'  ❌ Claude error: {e}')
        return ''


def ai_chat(system: str, user: str, temperature: float = 0.7) -> str:
    """Try Claude first, fall back to OpenAI if it fails."""
    result = anthropic_chat(system, user, temperature=temperature)
    if result:
        return result
    print(f'  🔄 Fallback → OpenAI GPT-4o...')
    result = openai_chat(system, user, temperature=temperature)
    return result

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 1: DATA COLLECTION
# ═══════════════════════════════════════════════════════════════════════════

def get_weekly_topics(week_offset: int = 1, weeks: int = 1, until_date: str = None) -> List[Dict]:
    """Fetch newsletter topics for target period from Notion."""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    if until_date:
        end_dt = datetime.strptime(until_date, '%Y-%m-%d')
    else:
        end_dt = monday + timedelta(weeks=weeks) - timedelta(days=1)
    start_date = monday.strftime('%Y-%m-%d')
    end_date = end_dt.strftime('%Y-%m-%d')

    print(f'📅 Notion: Themen {start_date} → {end_date}')

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

        # Fetch briefing content from page blocks
        content_data = notion_api('GET', f'/blocks/{page["id"]}/children?page_size=100')
        briefing_parts = []
        for block in content_data.get('results', []):
            btype = block['type']
            if btype in ['paragraph', 'heading_1', 'heading_2', 'heading_3',
                         'bulleted_list_item', 'callout', 'quote', 'numbered_list_item']:
                text = ''.join([t.get('plain_text', '') for t in block[btype].get('rich_text', [])])
                if text:
                    briefing_parts.append(text)

        topics.append({
            'page_id': page['id'],
            'name': name.strip(),
            'date': date,
            'briefing': '\n'.join(briefing_parts),
        })

    print(f'  ✅ {len(topics)} Themen gefunden')
    for t in topics:
        print(f'     • {t["date"]} — {t["name"]}')
    return topics


def get_newsletter_clients(client_filter: str = None) -> List[Dict]:
    """Fetch active newsletter clients from Airtable with brand + product data."""
    print(f'\n📊 Airtable: Newsletter-Kunden')
    import urllib.parse
    path = urllib.parse.quote(f'{AIRTABLE_BASE}/Kunden?maxRecords=100', safe='/?=&')
    data = airtable_api('GET', path)

    clients = []
    for record in data.get('records', []):
        f = record['fields']
        if f.get('Status') != 'Aktiv':
            continue
        if not f.get('Newsletter Service'):
            continue
        if not f.get('Klaviyo API Key'):
            continue

        client_name = f.get('Firmenname', '')
        if client_filter and client_filter.lower() not in client_name.lower():
            continue

        client = {
            'id': record['id'],
            'name': client_name,
            'website': f.get('Website', ''),
            'klaviyo_api_key': f.get('Klaviyo API Key', ''),
            'klaviyo_list_id': f.get('Klaviyo List ID', ''),
            'language': f.get('Email Sprache', 'de'),
            'brand_assets_ids': f.get('Brand Assets', []),
            'product_info_ids': f.get('Produkt-Info', []),
            'branche': f.get('Branche', ''),
        }

        # Enrich: Brand Assets
        for asset_id in client.get('brand_assets_ids', []):
            asset = airtable_api('GET', f'{AIRTABLE_BASE}/Brand%20Assets/{asset_id}')
            if asset:
                af = asset.get('fields', {})
                colors = [c.strip() for c in af.get('Farbcodes', '').split(',') if c.strip().startswith('#')]
                client['brand'] = {
                    'primary': colors[0] if len(colors) > 0 else '#333333',
                    'secondary': colors[1] if len(colors) > 1 else '#666666',
                    'accent': colors[2] if len(colors) > 2 else '#0066CC',
                    'cream': colors[3] if len(colors) > 3 else '#F5F4F0',
                    'fonts_heading': af.get('Schriftarten', 'Georgia, serif').split(',')[0].strip(),
                    'fonts_body': af.get('Schriftarten', 'Arial, sans-serif').split(',')[-1].strip() if ',' in af.get('Schriftarten', '') else 'Arial, sans-serif',
                    'tone': af.get('Tonalität', ''),
                    'tagline': af.get('Brand Tagline', ''),
                    'logo_url': af.get('Logo URL', ''),
                }
                break
        if 'brand' not in client:
            client['brand'] = {
                'primary': '#333333', 'secondary': '#666666', 'accent': '#0066CC',
                'cream': '#F5F4F0', 'fonts_heading': 'Georgia, serif',
                'fonts_body': 'Arial, sans-serif', 'tone': '', 'tagline': '', 'logo_url': ''
            }

        # Enrich: Product Info
        for prod_id in client.get('product_info_ids', []):
            prod = airtable_api('GET', f'{AIRTABLE_BASE}/Produkt-Info/{prod_id}')
            if prod:
                pf = prod.get('fields', {})
                client['product_info'] = {
                    'description': pf.get('Produktbeschreibung', ''),
                    'target_audience': pf.get('Zielgruppe', ''),
                    'usps': pf.get('USPs / Vorteile', ''),
                    'top_products': pf.get('Top-Produkte', ''),
                    'social_proof': pf.get('Social Proof', ''),
                }
                try:
                    pj = pf.get('Produkte JSON', '')
                    if pj:
                        client['product_info']['json'] = json.loads(pj)
                except:
                    pass
                break
        if 'product_info' not in client:
            client['product_info'] = {}

        # Known product catalog for HTML product cards
        client['products'] = KNOWN_PRODUCTS.get(client_name, {})

        clients.append(client)

    print(f'  ✅ {len(clients)} Kunden')
    for c in clients:
        print(f'     • {c["name"]} (Klaviyo ✓, {len(c["products"])} Produkte)')
    return clients

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 2: AI COPY GENERATION
# ═══════════════════════════════════════════════════════════════════════════

def build_copy_prompt(topic: Dict, client: Dict) -> list:
    """Build OpenAI messages for newsletter copy generation."""
    brand = client['brand']
    pi = client.get('product_info', {})
    products = client.get('products', {})

    # Build product list for context
    product_lines = []
    for key, p in products.items():
        line = f"- {p['name']}: €{p['price']}"
        if p.get('original_price'):
            line += f" (statt €{p['original_price']})"
        if p.get('desc'):
            line += f" — {p['desc']}"
        product_lines.append(line)

    system = f"""Du bist ein Expert Email Copywriter für E-Commerce Newsletter.
Schreibe im Stil der Brand: {brand.get('tone', 'professional, warm, engaging')}.

REGELN:
- AIDA-Struktur (Attention → Interest → Desire → Action)
- Hook in der ersten Zeile — keine generischen Begrüßungen ("Liebe Kunden...")
- Emotional, nicht generisch. Storytelling statt Produktliste.
- Kurze Absätze, max 2-3 Sätze pro Block
- Sprache: {client['language'].upper()}
- USPs natürlich einbauen, nicht als Bulletpoints runterbeten
- Dringlichkeit wenn passend (limitiert, nur heute, etc.)
- Brand Tagline: "{brand.get('tagline', '')}"

PRODUKTE:
{chr(10).join(product_lines) if product_lines else 'Keine spezifischen Produkte.'}

USPs: {pi.get('usps', 'N/A')}
Social Proof: {pi.get('social_proof', 'N/A')}

ANTWORT als JSON (kein Markdown, nur raw JSON):
{{
  "subject": "Betreffzeile (max 50 Zeichen, mit Emoji)",
  "preview": "Preview-Text (max 80 Zeichen)",
  "headline": "Headline (kurz, emotional, max 6 Worte)",
  "body": ["Absatz 1", "", "Absatz 2", "✓ Bulletpoint", ...],
  "cta": "CTA-Text →",
  "closing": "Abschluss<br>Team Name",
  "products_to_show": ["system_bundle", "system_razor_face"]
}}

products_to_show: Wähle 2-3 passende Produkt-Keys aus: {', '.join(products.keys()) if products else 'keine'}"""

    user = f"""Newsletter für: {client['name']}
Thema: {topic['name']}
Datum: {topic['date']}

Briefing aus dem Content-Kalender:
{topic.get('briefing', 'Kein Briefing vorhanden — generiere basierend auf dem Thema.')}"""

    return [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user}
    ]


def generate_ai_copy(topic: Dict, client: Dict) -> Dict:
    """Generate newsletter copy using OpenAI."""
    print(f'  🤖 AI Copy generieren...')

    messages = build_copy_prompt(topic, client)
    raw = ai_chat(system=messages[0]['content'], user=messages[1]['content'], temperature=0.7)

    if not raw:
        print(f'  ⚠️  AI-Fallback: generischer Text')
        return fallback_copy(topic, client)

    # Parse JSON from response (handle markdown code blocks, smart quotes, etc.)
    raw = raw.strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1] if '\n' in raw else raw[3:]
        if raw.endswith('```'):
            raw = raw[:-3]
        raw = raw.strip()

    # Fix common JSON issues from LLMs
    # Replace smart/curly quotes with straight quotes
    raw = raw.replace('\u201c', '\\"').replace('\u201d', '\\"')  # " "
    raw = raw.replace('\u201e', '\\"').replace('\u201f', '\\"')  # „ ‟
    raw = raw.replace('\u2018', "'").replace('\u2019', "'")      # ' '
    raw = raw.replace('\u00ab', '\\"').replace('\u00bb', '\\"')  # « »

    try:
        copy = json.loads(raw)
        print(f'  ✅ Subject: {copy.get("subject", "?")}')
        return copy
    except json.JSONDecodeError as e:
        print(f'  ⚠️  JSON parse error (attempt 1): {e}')
        # Retry: ask AI to fix the JSON
        fix_raw = ai_chat(
            system='Fix this broken JSON. Return ONLY valid JSON, nothing else. Escape all quotes inside string values.',
            user=raw,
            temperature=0.0
        )
        fix_raw = fix_raw.strip()
        if fix_raw.startswith('```'):
            fix_raw = fix_raw.split('\n', 1)[1] if '\n' in fix_raw else fix_raw[3:]
            if fix_raw.endswith('```'):
                fix_raw = fix_raw[:-3]
            fix_raw = fix_raw.strip()
        try:
            copy = json.loads(fix_raw)
            print(f'  ✅ Subject (fixed): {copy.get("subject", "?")}')
            return copy
        except json.JSONDecodeError:
            print(f'  ⚠️  JSON fix failed, using fallback')
            return fallback_copy(topic, client)


def fallback_copy(topic: Dict, client: Dict) -> Dict:
    """Fallback copy when AI fails."""
    return {
        'subject': f'{topic["name"]} ✨',
        'preview': f'Neuigkeiten von {client["name"]}',
        'headline': topic['name'],
        'body': [
            f'Wir haben Neuigkeiten: {topic["name"]}.',
            '',
            f'Entdecke jetzt, was {client["name"]} für dich vorbereitet hat.',
        ],
        'cta': 'Jetzt entdecken →',
        'closing': f'Beste Grüße,<br>Dein {client["name"]} Team',
        'products_to_show': list(client.get('products', {}).keys())[:2]
    }

# ═══════════════════════════════════════════════════════════════════════════
# PHASE 3: HTML + KLAVIYO
# ═══════════════════════════════════════════════════════════════════════════

def fetch_klaviyo_images(api_key: str) -> Dict:
    """Fetch images from Klaviyo for email templates."""
    result = klaviyo_api(api_key, 'GET', '/images?page%5Bsize%5D=100')
    images = {'logos': [], 'heroes': [], 'products': []}
    if 'error' in result:
        return images
    for img in result.get('data', []):
        attrs = img.get('attributes', {})
        url = attrs.get('image_url', '')
        if not url:
            continue
        name = attrs.get('name', '').lower()
        img_data = {'name': attrs.get('name'), 'url': url}
        if 'logo' in name or 'stacked' in name:
            images['logos'].append(img_data)
        elif 'hero' in name:
            images['heroes'].append(img_data)
        else:
            images['products'].append(img_data)
    return images


def get_rotated_image(images: list, topic_name: str) -> Optional[str]:
    """Pick a rotated image based on topic hash."""
    if not images:
        return None
    h = int(hashlib.md5(topic_name.encode()).hexdigest(), 16)
    return images[h % len(images)]['url']


def generate_product_card_html(product: Dict, brand: Dict, lang: str) -> str:
    """Generate a single product card HTML."""
    if not product:
        return ''
    btn = 'Jetzt shoppen' if lang == 'de' else 'Shop Now'
    badge_html = ''
    if product.get('badge'):
        badge_html = f'<span style="display:inline-block;background-color:{brand["accent"]};color:#FFFFFF;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;margin-bottom:10px;">{product["badge"]}</span><br>'
    original_html = ''
    if product.get('original_price'):
        original_html = f'<span style="font-size:16px;color:#999;text-decoration:line-through;margin-left:8px;">€{product["original_price"]}</span>'

    return f'''<tr><td style="padding:12px 15px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:linear-gradient(135deg,{brand['cream']} 0%,#FFFFFF 100%);border-radius:20px;overflow:hidden;border:1px solid {brand.get('cream','#eee')};">
<tr>
<td width="40%" style="padding:20px;"><img src="{product.get('image','')}" width="100%" style="display:block;border-radius:12px;" alt="{product.get('name','')}"></td>
<td width="60%" style="padding:25px 25px 25px 10px;" valign="middle">
{badge_html}
<h3 style="font-family:{brand.get('fonts_heading','Georgia,serif')};font-size:22px;color:{brand['primary']};margin:0 0 8px 0;font-weight:normal;">{product.get('name','')}</h3>
<p style="font-size:14px;color:#666;margin:0 0 12px 0;line-height:1.5;">{product.get('desc','')}</p>
<p style="font-size:26px;color:{brand['accent']};margin:0 0 15px 0;font-weight:700;">€{product.get('price','')}{original_html}</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background-color:{brand['primary']};border-radius:50px;padding:0;"><a href="{product.get('url','#')}" style="display:inline-block;padding:12px 28px;font-size:14px;color:#FFFFFF;text-decoration:none;font-weight:600;border-radius:50px;">{btn} →</a></td></tr></table>
</td>
</tr>
</table>
</td></tr>'''


def generate_html(copy: Dict, client: Dict, topic: Dict, images: Dict) -> str:
    """Generate complete email HTML."""
    brand = client['brand']
    lang = client['language']
    products = client.get('products', {})

    logo_url = get_rotated_image(images['logos'], topic['name']) or brand.get('logo_url', '')
    hero_url = get_rotated_image(images['heroes'], topic['name']) or ''

    # Body paragraphs
    body_html = ''
    for para in copy.get('body', []):
        if para == '':
            body_html += '<tr><td style="padding:5px 40px;"></td></tr>\n'
        elif para.startswith('✓') or para.startswith('•'):
            body_html += f'<tr><td style="padding:4px 40px 4px 60px;"><p style="font-size:16px;color:#333;margin:0;line-height:1.6;">{para}</p></td></tr>\n'
        elif para.startswith('**') or para.isupper():
            clean = para.replace('**', '')
            body_html += f'<tr><td style="padding:10px 40px 5px 40px;"><p style="font-size:16px;font-weight:700;color:{brand["primary"]};margin:0;">{clean}</p></td></tr>\n'
        else:
            # Handle inline bold
            formatted = para
            while '**' in formatted:
                formatted = formatted.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
            body_html += f'<tr><td style="padding:8px 40px;"><p style="font-size:17px;color:#333;margin:0;line-height:1.8;font-family:{brand.get("fonts_body","Arial,sans-serif")};">{formatted}</p></td></tr>\n'

    # Product cards
    products_html = ''
    products_to_show = copy.get('products_to_show', list(products.keys())[:2])
    if products_to_show and products:
        products_html = '<tr><td style="padding:30px 15px 10px 15px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">\n'
        for pk in products_to_show[:3]:
            if pk in products:
                products_html += generate_product_card_html(products[pk], brand, lang)
        products_html += '</table></td></tr>\n'

    # Hero section
    hero_html = ''
    if hero_url:
        hero_html = f'<tr><td style="padding:0 30px;"><img src="{hero_url}" width="100%" style="display:block;border-radius:16px;" alt="Hero"></td></tr>'

    # Logo
    if logo_url:
        logo_html = f'<img src="{logo_url}" alt="{client["name"]}" width="140" style="display:block;">'
    else:
        logo_html = f'<h2 style="color:{brand["primary"]};margin:0;font-family:{brand.get("fonts_heading","Georgia,serif")};font-size:28px;">{client["name"]}</h2>'

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{copy.get('subject','')}</title>
<style>@media only screen and (max-width:600px){{.mp{{padding:20px!important;}}}}</style>
</head>
<body style="margin:0;padding:0;background-color:{brand['cream']};font-family:{brand.get('fonts_body','Arial,sans-serif')};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{brand['cream']};">
<tr><td align="center" style="padding:30px 15px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:20px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,0.06);">

<!-- Logo -->
<tr><td align="center" style="padding:40px 20px 30px 20px;">{logo_html}</td></tr>

<!-- Hero -->
{hero_html}

<!-- Headline -->
<tr><td style="padding:50px 40px 20px 40px;" class="mp">
<h1 style="font-family:{brand.get('fonts_heading','Georgia,serif')};font-size:38px;color:{brand['primary']};margin:0;font-weight:normal;line-height:1.2;text-align:center;">
{copy.get('headline', topic['name'])}
</h1></td></tr>

<!-- Divider -->
<tr><td align="center" style="padding:10px 40px 30px 40px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="60" style="border-top:2px solid {brand['accent']};"><tr><td></td></tr></table>
</td></tr>

<!-- Body -->
{body_html}

<!-- Products -->
{products_html}

<!-- CTA -->
<tr><td align="center" style="padding:40px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="background-color:{brand['accent']};border-radius:50px;padding:0;box-shadow:0 8px 30px rgba(0,0,0,0.15);">
<a href="{client.get('website','#')}" style="display:inline-block;padding:20px 60px;font-size:17px;color:#FFFFFF;text-decoration:none;font-weight:700;border-radius:50px;letter-spacing:0.5px;">
{copy.get('cta', 'Jetzt entdecken →')}
</a></td></tr></table>
</td></tr>

<!-- Closing -->
<tr><td style="padding:0 40px 40px 40px;" class="mp">
<p style="font-size:16px;color:{brand['primary']};margin:0;line-height:1.7;text-align:center;">
{copy.get('closing', f'Dein {client["name"]} Team')}
</p></td></tr>

<!-- Footer -->
<tr><td style="background-color:{brand.get('cream','#F5F4F0')};padding:35px;text-align:center;">
<p style="font-size:12px;color:#888;margin:0 0 8px 0;letter-spacing:1px;text-transform:uppercase;">{brand.get('tagline','')}</p>
<p style="font-size:11px;color:#AAA;margin:0;line-height:1.6;">
{client['name']} · <a href="{client.get('website','#')}" style="color:#AAA;text-decoration:none;">{client.get('website','').replace('https://','').rstrip('/')}</a><br>
<a href="{{{{unsubscribe_url}}}}" style="color:#AAA;">Abmelden</a>
</p></td></tr>

</table></td></tr></table>
</body></html>'''


def publish_to_klaviyo(client: Dict, topic: Dict, copy: Dict, html: str) -> Dict:
    """Create Klaviyo template + campaign draft."""
    api_key = client['klaviyo_api_key']
    list_id = client.get('klaviyo_list_id', '')
    if not list_id:
        return {'error': 'no_list_id', 'detail': f'{client["name"]} hat keine Klaviyo List ID'}

    name = f'{client["name"]} | {topic["name"]} | {topic["date"]}'

    # Create template
    tmpl = klaviyo_api(api_key, 'POST', '/templates', {
        'data': {'type': 'template', 'attributes': {
            'name': name, 'editor_type': 'CODE', 'html': html,
            'text': copy.get('subject', topic['name'])
        }}
    })
    if 'error' in tmpl:
        return {'error': 'template_failed', 'detail': str(tmpl['error'])[:200]}
    template_id = tmpl['data']['id']

    # Create campaign
    send_dt = f'{topic["date"]}T09:00:00+01:00'
    website = client.get('website', '').replace('https://', '').split('/')[0]
    from_email = f'hello@{website}' if website else 'hello@example.com'

    camp = klaviyo_api(api_key, 'POST', '/campaigns', {
        'data': {'type': 'campaign', 'attributes': {
            'name': name,
            'audiences': {'included': [list_id], 'excluded': []},
            'send_strategy': {'method': 'static', 'options_static': {'datetime': send_dt}},
            'campaign-messages': {'data': [{'type': 'campaign-message', 'attributes': {
                'channel': 'email', 'label': 'Default',
                'content': {
                    'subject': copy.get('subject', topic['name']),
                    'preview_text': copy.get('preview', ''),
                    'from_email': from_email,
                    'from_label': client['name']
                }
            }}]}
        }}
    })
    if 'error' in camp:
        return {'error': 'campaign_failed', 'template_id': template_id, 'detail': str(camp['error'])[:200]}

    campaign_id = camp['data']['id']
    message_id = camp['data']['relationships']['campaign-messages']['data'][0]['id']

    # Assign template to campaign message
    klaviyo_api(api_key, 'POST', '/campaign-message-assign-template', {
        'data': {'type': 'campaign-message', 'id': message_id,
                 'relationships': {'template': {'data': {'type': 'template', 'id': template_id}}}}
    })

    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_id,
        'url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

# ═══════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

def process_newsletter(client: Dict, topic: Dict, images: Dict, dry_run: bool = False) -> Dict:
    """Process a single newsletter: AI copy → HTML → Klaviyo."""
    print(f'\n{"─"*60}')
    print(f'📧 {client["name"]} | {topic["name"]} ({topic["date"]})')
    print(f'{"─"*60}')

    # Step 1: AI Copy
    copy = generate_ai_copy(topic, client)

    # Step 2: HTML
    html = generate_html(copy, client, topic, images)

    # Save HTML locally
    safe_name = f'{client["name"].lower().replace(" ", "_")}_{topic["date"]}_{topic["name"][:30].lower().replace(" ", "_")}.html'
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '._-')
    html_path = NEWSLETTERS_DIR / safe_name
    html_path.write_text(html, encoding='utf-8')
    print(f'  💾 Saved: {safe_name}')

    # Save briefing
    briefing_id = f'{client["name"].lower().replace(" ", "_")}_{topic["date"]}'
    briefing = {
        'briefing_id': briefing_id,
        'created_at': datetime.now().isoformat(),
        'status': 'done',
        'client': {'name': client['name'], 'website': client['website'], 'language': client['language']},
        'topic': {'name': topic['name'], 'date': topic['date'], 'briefing': topic.get('briefing', '')},
        'copy': copy,
    }
    briefing_path = BRIEFINGS_DIR / f'{briefing_id}.json'
    briefing_path.write_text(json.dumps(briefing, indent=2, ensure_ascii=False), encoding='utf-8')

    # Step 3: Publish to Klaviyo
    if dry_run:
        print(f'  🏜️  Dry run — nicht veröffentlicht')
        return {'success': True, 'dry_run': True, 'html_file': safe_name, 'subject': copy.get('subject', '')}

    result = publish_to_klaviyo(client, topic, copy, html)
    if result.get('success'):
        print(f'  ✅ Campaign: {result["campaign_id"]}')
        print(f'  🔗 {result["url"]}')
        briefing['klaviyo'] = result
        briefing_path.write_text(json.dumps(briefing, indent=2, ensure_ascii=False), encoding='utf-8')
    else:
        print(f'  ❌ {result.get("error")}: {result.get("detail", "")}')

    return {
        'success': result.get('success', False),
        'client': client['name'],
        'topic': topic['name'],
        'date': topic['date'],
        'subject': copy.get('subject', ''),
        'html_file': safe_name,
        **{k: v for k, v in result.items() if k != 'success'}
    }


def main():
    parser = argparse.ArgumentParser(description='Newsletter Engine v6 — AI-Powered, Fully Automated')
    parser.add_argument('--week-offset', type=int, default=1, help='Week offset (default: 1 = next week)')
    parser.add_argument('--weeks', type=int, default=1, help='Number of weeks to process (default: 1)')
    parser.add_argument('--until', type=str, default=None, help='Process all topics until this date (YYYY-MM-DD)')
    parser.add_argument('--client', type=str, default=None, help='Filter by client name')
    parser.add_argument('--dry-run', action='store_true', help='Generate without publishing to Klaviyo')
    args = parser.parse_args()

    NEWSLETTERS_DIR.mkdir(parents=True, exist_ok=True)
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)

    weeks_label = f'Week +{args.week_offset}' if args.weeks == 1 and not args.until else f'Weeks +{args.week_offset} ({args.weeks}w)' if not args.until else f'Until {args.until}'
    print('=' * 60)
    print('📧 NEWSLETTER ENGINE v6 — AI-Powered')
    print(f'   {datetime.now().strftime("%Y-%m-%d %H:%M")} | {weeks_label}')
    if args.dry_run:
        print('   🏜️  DRY RUN MODE')
    print('=' * 60)

    # Phase 1: Collect data
    topics = get_weekly_topics(args.week_offset, weeks=args.weeks, until_date=args.until)
    if not topics:
        print('\n⚠️  Keine Themen für diese Woche. Fertig.')
        return

    clients = get_newsletter_clients(args.client)
    if not clients:
        print('\n⚠️  Keine Newsletter-Kunden gefunden. Fertig.')
        return

    total = len(topics) * len(clients)
    print(f'\n🎯 {total} Newsletter zu erstellen ({len(clients)} Kunden × {len(topics)} Themen)')
    print('=' * 60)

    # Pre-fetch Klaviyo images per client (once)
    client_images = {}
    for client in clients:
        print(f'\n📸 Bilder laden: {client["name"]}...')
        client_images[client['name']] = fetch_klaviyo_images(client['klaviyo_api_key'])

    # Phase 2+3: Generate + Publish
    results = []
    for client in clients:
        images = client_images[client['name']]
        for topic in topics:
            result = process_newsletter(client, topic, images, dry_run=args.dry_run)
            results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get('success'))
    print('\n' + '=' * 60)
    print(f'📊 ERGEBNIS: {successful}/{len(results)} Newsletter erstellt')
    print('=' * 60)
    for r in results:
        status = '✅' if r.get('success') else '❌'
        print(f'  {status} {r.get("client", "?")} | {r.get("date", "?")} | {r.get("subject", r.get("topic", "?"))}')
        if r.get('url'):
            print(f'     🔗 {r["url"]}')
    print('=' * 60)

    # Save run log
    log = {
        'run_date': datetime.now().isoformat(),
        'week_offset': args.week_offset,
        'dry_run': args.dry_run,
        'topics_count': len(topics),
        'clients_count': len(clients),
        'successful': successful,
        'total': len(results),
        'results': results
    }
    LOG_FILE.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'\n📝 Log: {LOG_FILE}')


if __name__ == '__main__':
    main()
