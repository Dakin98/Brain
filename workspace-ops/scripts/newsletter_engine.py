#!/usr/bin/env python3
"""
Newsletter Engine v4 — Multi-Client, Notion-driven, Skalierbar

Flow:
1. Notion: Themen dieser Woche holen (inkl. Briefing + Beispielbilder)
2. Airtable: Aktive Newsletter-Kunden + Brand Assets
3. Pro Kunde × Thema: Personalisiertes HTML generieren
4. Klaviyo: Template + Campaign als Draft
5. Output: JSON Report

Usage:
    python3 newsletter_engine.py                    # Diese Woche
    python3 newsletter_engine.py --week-offset 1    # Nächste Woche
    python3 newsletter_engine.py --dry-run           # Nur Report, kein Klaviyo
    python3 newsletter_engine.py --client "Razeco"   # Nur für einen Kunden
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import argparse

# ─── Configuration ───────────────────────────────────────────────────────────

NOTION_API_KEY = open(os.path.expanduser('~/.config/notion/api_key')).read().strip()
NOTION_DB_ID = '3465a32b-e5e0-4d52-bec3-c24ff39e1507'
AIRTABLE_TOKEN = os.environ.get('MATON_API_KEY', '')
AIRTABLE_BASE = 'appbGhxy9I18oIS8E'
AIRTABLE_GATEWAY = 'https://gateway.maton.ai/airtable/v0'

# ─── API Helpers ─────────────────────────────────────────────────────────────

def notion_api(method: str, path: str, data: dict = None) -> dict:
    """Call Notion API"""
    url = f'https://api.notion.com/v1{path}'
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        print(f'  ❌ Notion {e.code}: {e.read().decode()[:200]}')
        return {}

def airtable_api(method: str, path: str, data: dict = None) -> dict:
    """Call Airtable via Maton Gateway"""
    url = f'{AIRTABLE_GATEWAY}/{path}'
    headers = {
        'Authorization': f'Bearer {AIRTABLE_TOKEN}',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        print(f'  ❌ Airtable {e.code}: {e.read().decode()[:200]}')
        return {}

def klaviyo_api(api_key: str, method: str, endpoint: str, data: dict = None) -> dict:
    """Call Klaviyo API"""
    url = f'https://a.klaviyo.com/api{endpoint}'
    headers = {
        'Authorization': f'Klaviyo-API-Key {api_key}',
        'revision': '2024-10-15',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        print(f'  ❌ Klaviyo {e.code}: {e.read().decode()[:200]}')
        return {'error': e.read().decode() if hasattr(e, 'read') else str(e)}

# ─── Step 1: Notion — Themen dieser Woche ───────────────────────────────────

def get_weekly_topics(week_offset: int = 0) -> List[Dict]:
    """Fetch newsletter topics for a given week from Notion"""
    today = datetime.now()
    # Monday of target week
    monday = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    sunday = monday + timedelta(days=6)
    
    start_date = monday.strftime('%Y-%m-%d')
    end_date = sunday.strftime('%Y-%m-%d')
    
    print(f'\n📅 Notion: Themen für {start_date} bis {end_date}')
    
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
        
        topic = {
            'page_id': page['id'],
            'name': name.strip(),
            'date': date,
            'briefing': '',
            'example_images': [],
        }
        topics.append(topic)
    
    print(f'  ✅ {len(topics)} Themen gefunden')
    for t in topics:
        print(f'     • {t["date"]} — {t["name"]}')
    
    return topics

def enrich_topic_with_content(topic: Dict) -> Dict:
    """Fetch page blocks (briefing text + example images) from Notion"""
    page_id = topic['page_id']
    data = notion_api('GET', f'/blocks/{page_id}/children?page_size=100')
    
    briefing_parts = []
    images = []
    
    for block in data.get('results', []):
        btype = block['type']
        
        # Extract text content
        if btype in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 
                      'bulleted_list_item', 'callout', 'quote', 'numbered_list_item']:
            rich_text = block[btype].get('rich_text', [])
            text = ''.join([t.get('plain_text', '') for t in rich_text])
            if text:
                if btype == 'callout':
                    briefing_parts.append(f'📌 {text}')
                elif btype.startswith('heading'):
                    briefing_parts.append(f'\n## {text}')
                elif btype == 'bulleted_list_item':
                    briefing_parts.append(f'• {text}')
                else:
                    briefing_parts.append(text)
        
        # Extract images
        elif btype == 'image':
            img = block['image']
            url = img.get('file', {}).get('url') or img.get('external', {}).get('url', '')
            caption = ''.join([t.get('plain_text', '') for t in img.get('caption', [])])
            if url:
                images.append({'url': url, 'caption': caption})
    
    topic['briefing'] = '\n'.join(briefing_parts)
    topic['example_images'] = images
    
    print(f'  📝 {topic["name"]}: {len(briefing_parts)} Textblöcke, {len(images)} Beispielbilder')
    return topic

# ─── Step 2: Airtable — Aktive Newsletter-Kunden ────────────────────────────

def get_newsletter_clients(client_filter: str = None) -> List[Dict]:
    """Fetch active clients with Newsletter Service from Airtable"""
    print(f'\n📊 Airtable: Newsletter-Kunden laden...')
    
    # Get clients
    formula = "AND({Status}='Aktiv',{Newsletter Service}=TRUE(),{Klaviyo API Key}!='')"
    import urllib.parse
    encoded_formula = urllib.parse.quote(formula, safe='')
    
    data = airtable_api('GET', f'{AIRTABLE_BASE}/Kunden?filterByFormula={encoded_formula}')
    
    clients = []
    for record in data.get('records', []):
        f = record['fields']
        client = {
            'id': record['id'],
            'name': f.get('Firmenname', ''),
            'website': f.get('Website', ''),
            'klaviyo_api_key': f.get('Klaviyo API Key', ''),
            'klaviyo_list_id': f.get('Klaviyo List ID', ''),
            'email_language': f.get('Email Sprache', 'de'),
            'brand_assets_ids': f.get('Brand Assets', []),
        }
        
        if client_filter and client_filter.lower() not in client['name'].lower():
            continue
            
        clients.append(client)
    
    # Enrich with Brand Assets
    for client in clients:
        if client['brand_assets_ids']:
            for asset_id in client['brand_assets_ids']:
                asset_data = airtable_api('GET', f'{AIRTABLE_BASE}/tbl7MJdMfOfrMYsd6/{asset_id}')
                if asset_data:
                    af = asset_data.get('fields', {})
                    client['brand'] = {
                        'colors': af.get('Farbcodes', ''),
                        'fonts': af.get('Schriftarten', ''),
                        'tone': af.get('Tonalität', ''),
                        'tagline': af.get('Brand Tagline', ''),
                        'logo_url': af.get('Logo URL', ''),
                    }
                    break
        
        if 'brand' not in client:
            client['brand'] = {'colors': '', 'fonts': '', 'tone': '', 'tagline': '', 'logo_url': ''}
    
    # Enrich with Produkt-Info
    for client in clients:
        formula_prod = f"FIND('{client['name']}', ARRAYJOIN({{Kunde}}))"
        # Simpler: just get all and filter
        prod_data = airtable_api('GET', f'{AIRTABLE_BASE}/Produkt-Info?maxRecords=10')
        for rec in prod_data.get('records', []):
            linked = rec['fields'].get('Kunde', [])
            if client['id'] in linked:
                client['products'] = {
                    'usps': rec['fields'].get('USPs / Vorteile', ''),
                    'products_json': rec['fields'].get('Produkte JSON', ''),
                    'social_proof': rec['fields'].get('Social Proof', ''),
                }
                break
        if 'products' not in client:
            client['products'] = {'usps': '', 'products_json': '', 'social_proof': ''}
    
    print(f'  ✅ {len(clients)} Kunden gefunden')
    for c in clients:
        has_brand = '🎨' if c['brand']['colors'] else '⬜'
        has_products = '📦' if c['products']['usps'] else '⬜'
        print(f'     {has_brand}{has_products} {c["name"]} (Klaviyo: {"✅" if c["klaviyo_api_key"] else "❌"})')
    
    return clients

# ─── Step 3: HTML Generation ────────────────────────────────────────────────

def parse_brand_colors(color_string: str) -> Dict:
    """Parse brand colors from comma-separated hex string"""
    colors = [c.strip() for c in color_string.split(',') if c.strip().startswith('#')]
    return {
        'primary': colors[0] if len(colors) > 0 else '#333333',
        'secondary': colors[1] if len(colors) > 1 else '#666666',
        'accent': colors[2] if len(colors) > 2 else '#0066CC',
        'bg_light': colors[3] if len(colors) > 3 else '#F5F5F5',
        'bg_medium': colors[4] if len(colors) > 4 else '#ECECEC',
        'text_light': colors[5] if len(colors) > 5 else '#999999',
        'text_muted': colors[6] if len(colors) > 6 else '#AAAAAA',
    }

def parse_fonts(font_string: str) -> Dict:
    """Parse font families from string"""
    # Expects format like: "DM Serif Display (headings), Plus Jakarta Sans (body)"
    heading_font = "Georgia, serif"
    body_font = "Arial, sans-serif"
    
    if font_string:
        parts = font_string.split(',')
        for part in parts:
            p = part.strip()
            if 'heading' in p.lower() or 'serif' in p.lower():
                font_name = p.split('(')[0].strip()
                heading_font = f"'{font_name}', Georgia, serif"
            elif 'body' in p.lower() or 'sans' in p.lower():
                font_name = p.split('(')[0].strip()
                body_font = f"'{font_name}', Arial, sans-serif"
    
    return {'heading': heading_font, 'body': body_font}

def generate_newsletter_html(client: Dict, topic: Dict) -> str:
    """Generate branded newsletter HTML based on topic briefing and client brand"""
    
    colors = parse_brand_colors(client['brand']['colors'])
    fonts = parse_fonts(client['brand']['fonts'])
    logo_url = client['brand']['logo_url'] or ''
    tagline = client['brand']['tagline'] or client['name']
    website = client['website'] or '#'
    language = client.get('email_language', 'de')
    
    # Determine CTA text based on language
    cta_text = 'Jetzt entdecken →' if language == 'de' else 'Discover now →'
    greeting = 'Hallo' if language == 'de' else 'Hello'
    
    # Build content sections based on briefing
    briefing = topic.get('briefing', '')
    topic_name = topic['name']
    
    # Generate subject line and preview based on topic
    subject_line = generate_subject_line(topic_name, client['name'], language)
    preview_text = generate_preview_text(topic_name, language)
    
    # Build body content from briefing
    content_html = briefing_to_html(briefing, colors, fonts)
    
    # Products section if we have product data
    products_html = ''
    if client['products']['products_json']:
        try:
            products = json.loads(client['products']['products_json'])
            if isinstance(products, dict):
                products_html = products_to_html(products, colors, fonts, language)
        except json.JSONDecodeError:
            pass
    
    # Social proof section
    social_proof_html = ''
    if client['products']['social_proof']:
        social_proof_html = social_proof_to_html(client['products']['social_proof'], colors, fonts)
    
    html = f'''<!DOCTYPE html>
<html lang="{language}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject_line}</title>
  <!--[if mso]>
  <noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
  <![endif]-->
</head>
<body style="margin:0;padding:0;background-color:{colors['bg_light']};">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:{colors['bg_light']};">
    <tr>
      <td align="center" style="padding:20px 0;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="background-color:#FFFFFF;max-width:600px;width:100%;">
          
          <!-- Header -->
          <tr>
            <td align="center" style="padding:30px 20px;background-color:#FFFFFF;">
              {f'<a href="{website}"><img src="{logo_url}" alt="{client["name"]}" width="120" style="display:block;border:0;"></a>' if logo_url else f'<h2 style="font-family:{fonts["heading"]};color:{colors["primary"]};margin:0;">{client["name"]}</h2>'}
            </td>
          </tr>

          <!-- Hero Section -->
          <tr>
            <td style="background-color:{colors['accent']};padding:40px 30px;text-align:center;">
              <h1 style="font-family:{fonts['heading']};font-size:28px;line-height:1.3;color:{colors['bg_light']};margin:0 0 15px 0;font-weight:normal;">
                {subject_line}
              </h1>
              <p style="font-family:{fonts['body']};font-size:16px;line-height:1.6;color:{colors['bg_medium']};margin:0;">
                {preview_text}
              </p>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding:40px 30px 20px 30px;">
              <p style="font-family:{fonts['body']};font-size:16px;line-height:1.7;color:{colors['primary']};margin:0;">
                {greeting} {{{{first_name|default:"there"}}}},
              </p>
            </td>
          </tr>

          <!-- Content from Briefing -->
          {content_html}

          <!-- Products (if available) -->
          {products_html}

          <!-- Social Proof (if available) -->
          {social_proof_html}

          <!-- CTA -->
          <tr>
            <td align="center" style="padding:20px 30px 40px 30px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background-color:{colors['accent']};border-radius:4px;">
                    <a href="{website}" style="display:inline-block;padding:14px 32px;font-family:{fonts['body']};font-size:16px;color:#FFFFFF;text-decoration:none;font-weight:600;">
                      {cta_text}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color:{colors['bg_light']};padding:30px;text-align:center;border-top:1px solid {colors['bg_medium']};">
              <p style="font-family:{fonts['body']};font-size:12px;color:{colors['text_light']};margin:0 0 10px 0;">
                {tagline}
              </p>
              <p style="font-family:{fonts['body']};font-size:11px;color:{colors['text_muted']};margin:0;">
                <a href="{website}" style="color:{colors['text_muted']};text-decoration:underline;">{client['name']}</a>
                &nbsp;|&nbsp;
                <a href="{{{{unsubscribe_url}}}}" style="color:{colors['text_muted']};text-decoration:underline;">
                  {"Abmelden" if language == "de" else "Unsubscribe"}
                </a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>'''
    
    return html, subject_line, preview_text

def generate_subject_line(topic_name: str, client_name: str, lang: str) -> str:
    """Generate subject line from topic name"""
    # Map common topic patterns to German subject lines
    topic_lower = topic_name.lower()
    
    subject_map_de = {
        'recommended products': 'Unsere Empfehlungen für dich 🌱',
        'product recommendation': 'Unsere Empfehlungen für dich 🌱',
        'faq': 'Deine Fragen, unsere Antworten ❓',
        'show the future': 'Stell dir eine Welt ohne Plastikmüll vor 🌍',
        'product feature': 'Entdecke unser Highlight-Produkt ✨',
        'behind the scenes': 'Ein Blick hinter die Kulissen 👀',
        'tips': 'Unsere besten Tipps für dich 💡',
        'review': 'Das sagen unsere Kunden ⭐',
        'testimonial': 'Das sagen unsere Kunden ⭐',
        'before & after': 'Vorher & Nachher — Der Unterschied 🔄',
        'social proof': 'Warum uns tausende Kunden vertrauen ⭐',
        'sale': f'Sale bei {client_name} — Jetzt sparen! 🔥',
        'flash sale': f'Flash Sale — Nur für kurze Zeit! ⚡',
        'free shipping': 'Kostenloser Versand — Nur heute! 📦',
        'giveaway': f'Gewinnspiel bei {client_name} 🎁',
        'refer a friend': 'Empfiehl uns weiter & spare 🤝',
        'survey': 'Deine Meinung ist uns wichtig 📝',
        'founder': 'Eine persönliche Nachricht von uns 💌',
        'thank you': 'Danke, dass du dabei bist 🙏',
        'mission': 'Unsere Mission — Warum wir das tun 🌍',
        'new arrival': 'Neu eingetroffen! Entdecke jetzt ✨',
        'bestseller': 'Unsere Bestseller — Jetzt entdecken 🏆',
        'bundle': 'Mehr sparen mit unseren Bundles 📦',
        'black friday': 'Black Friday — Die besten Deals! 🖤',
        'cyber monday': 'Cyber Monday — Letzte Chance! 💻',
        'gift guide': 'Der perfekte Geschenke-Guide 🎁',
        'birthday': 'Alles Gute zum Geburtstag! 🎂',
        'loyalty': 'Danke für deine Treue ❤️',
    }
    
    subject_map_en = {
        'recommended products': 'Our Top Picks for You 🌱',
        'product recommendation': 'Our Top Picks for You 🌱',
        'faq': 'Your Questions, Answered ❓',
        'show the future': 'Imagine a World Without Plastic Waste 🌍',
        'product feature': 'Discover Our Featured Product ✨',
        'behind the scenes': 'Behind the Scenes 👀',
        'tips': 'Our Best Tips for You 💡',
        'review': 'What Our Customers Say ⭐',
        'testimonial': 'What Our Customers Say ⭐',
        'sale': f'Sale at {client_name} — Save Now! 🔥',
        'giveaway': f'Giveaway at {client_name} 🎁',
    }
    
    subject_map = subject_map_de if lang == 'de' else subject_map_en
    
    for pattern, subject in subject_map.items():
        if pattern in topic_lower:
            return subject
    
    # Fallback: use topic name directly
    return topic_name

def generate_preview_text(topic_name: str, lang: str) -> str:
    """Generate preview text"""
    topic_lower = topic_name.lower()
    
    previews_de = {
        'recommended': 'Die besten Produkte für dich zusammengestellt',
        'faq': 'Alles, was du wissen musst',
        'future': 'Gemeinsam für eine nachhaltige Zukunft',
        'review': 'Echte Erfahrungen unserer Community',
        'sale': 'Sichere dir jetzt die besten Angebote',
        'tips': 'Einfache Tricks für bessere Ergebnisse',
        'behind': 'So entsteht dein Lieblingsprodukt',
        'giveaway': 'Mitmachen und gewinnen',
    }
    
    for pattern, preview in previews_de.items():
        if pattern in topic_lower:
            return preview
    
    return f'Neuigkeiten von uns — Jetzt entdecken'

def briefing_to_html(briefing: str, colors: Dict, fonts: Dict) -> str:
    """Convert briefing text to email-safe HTML sections"""
    if not briefing:
        return ''
    
    lines = briefing.split('\n')
    html_parts = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('## '):
            html_parts.append(f'''
          <tr>
            <td style="padding:10px 30px;">
              <h2 style="font-family:{fonts['heading']};font-size:22px;color:{colors['primary']};margin:0;font-weight:normal;">
                {line[3:]}
              </h2>
            </td>
          </tr>''')
        elif line.startswith('📌 '):
            html_parts.append(f'''
          <tr>
            <td style="padding:10px 30px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="background-color:{colors['bg_light']};border-left:4px solid {colors['accent']};padding:15px 20px;border-radius:4px;">
                    <p style="font-family:{fonts['body']};font-size:15px;line-height:1.6;color:{colors['secondary']};margin:0;font-style:italic;">
                      {line[2:]}
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>''')
        elif line.startswith('• '):
            html_parts.append(f'''
          <tr>
            <td style="padding:3px 30px 3px 50px;">
              <p style="font-family:{fonts['body']};font-size:15px;line-height:1.6;color:{colors['primary']};margin:0;">
                • {line[2:]}
              </p>
            </td>
          </tr>''')
        else:
            html_parts.append(f'''
          <tr>
            <td style="padding:10px 30px;">
              <p style="font-family:{fonts['body']};font-size:16px;line-height:1.7;color:{colors['primary']};margin:0;">
                {line}
              </p>
            </td>
          </tr>''')
    
    return '\n'.join(html_parts)

def products_to_html(products: Dict, colors: Dict, fonts: Dict, lang: str) -> str:
    """Generate product showcase HTML from products JSON"""
    cta = 'Jetzt shoppen →' if lang == 'de' else 'Shop now →'
    html_parts = [f'''
          <tr>
            <td style="padding:20px 30px 10px 30px;">
              <h2 style="font-family:{fonts['heading']};font-size:22px;color:{colors['primary']};margin:0;font-weight:normal;text-align:center;">
                {"Unsere Produkte" if lang == "de" else "Our Products"}
              </h2>
            </td>
          </tr>''']
    
    count = 0
    for key, product in products.items():
        if count >= 3:  # Max 3 products in email
            break
        if not isinstance(product, dict):
            continue
            
        title = product.get('title', key)
        price = product.get('price', '')
        currency = product.get('currency', '€')
        url = product.get('url', '#')
        image = product.get('image', '')
        
        html_parts.append(f'''
          <tr>
            <td style="padding:10px 30px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border:1px solid {colors['bg_medium']};border-radius:8px;overflow:hidden;">
                <tr>
                  <td style="padding:20px;text-align:center;">
                    <h3 style="font-family:{fonts['heading']};font-size:18px;color:{colors['primary']};margin:0 0 8px 0;font-weight:normal;">{title}</h3>
                    <p style="font-family:{fonts['body']};font-size:18px;color:{colors['accent']};margin:0 0 12px 0;font-weight:bold;">{price} {currency}</p>
                    <a href="{url}" style="font-family:{fonts['body']};font-size:14px;color:{colors['accent']};text-decoration:none;font-weight:600;">{cta}</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>''')
        count += 1
    
    return '\n'.join(html_parts) if count > 0 else ''

def social_proof_to_html(social_proof: str, colors: Dict, fonts: Dict) -> str:
    """Generate social proof section"""
    if not social_proof:
        return ''
    
    lines = [l.strip() for l in social_proof.split('\n') if l.strip()][:3]
    
    html = f'''
          <tr>
            <td style="padding:20px 30px;background-color:{colors['bg_light']};">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">'''
    
    for line in lines:
        html += f'''
                <tr>
                  <td style="padding:8px 0;">
                    <p style="font-family:{fonts['body']};font-size:14px;color:{colors['secondary']};margin:0;text-align:center;">
                      ⭐ {line}
                    </p>
                  </td>
                </tr>'''
    
    html += '''
              </table>
            </td>
          </tr>'''
    
    return html

# ─── Step 4: Klaviyo — Template + Campaign ───────────────────────────────────

def create_klaviyo_campaign(client: Dict, topic: Dict, html: str, subject: str, preview: str, dry_run: bool = False) -> Dict:
    """Create template + campaign in Klaviyo"""
    api_key = client['klaviyo_api_key']
    list_id = client.get('klaviyo_list_id', '')
    name = f"{client['name']} | {topic['name']} | {topic['date']}"
    
    if dry_run:
        print(f'  🏜️  DRY RUN: Would create "{name}"')
        return {'dry_run': True, 'name': name}
    
    if not list_id:
        print(f'  ⚠️  Kein Klaviyo List ID für {client["name"]} — übersprungen')
        return {'error': 'no_list_id'}
    
    # Step 1: Create Template
    print(f'  📝 Template: {name}')
    template_result = klaviyo_api(api_key, 'POST', '/templates', {
        'data': {
            'type': 'template',
            'attributes': {
                'name': name,
                'editor_type': 'CODE',
                'html': html,
                'text': f'{subject}\n\n{preview}'
            }
        }
    })
    
    if 'error' in template_result:
        return {'error': 'template_failed'}
    
    template_id = template_result['data']['id']
    print(f'     ✅ Template: {template_id}')
    
    # Step 2: Create Campaign
    send_datetime = f"{topic['date']}T09:00:00+00:00"
    
    campaign_result = klaviyo_api(api_key, 'POST', '/campaigns', {
        'data': {
            'type': 'campaign',
            'attributes': {
                'name': name,
                'audiences': {'included': [list_id], 'excluded': []},
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
                                'from_email': f'hello@{client["website"].replace("https://","").replace("http://","").split("/")[0]}' if client['website'] else 'hello@example.com',
                                'from_label': client['name']
                            }
                        }
                    }]
                }
            }
        }
    })
    
    if 'error' in campaign_result:
        return {'error': 'campaign_failed', 'template_id': template_id}
    
    campaign_id = campaign_result['data']['id']
    message_id = campaign_result['data']['relationships']['campaign-messages']['data'][0]['id']
    print(f'     ✅ Campaign: {campaign_id}')
    
    # Step 3: Assign Template
    assign_result = klaviyo_api(api_key, 'POST', '/campaign-message-assign-template', {
        'data': {
            'type': 'campaign-message',
            'id': message_id,
            'relationships': {
                'template': {
                    'data': {'type': 'template', 'id': template_id}
                }
            }
        }
    })
    
    if 'error' in assign_result:
        print(f'     ⚠️  Template-Verknüpfung fehlgeschlagen')
    else:
        print(f'     ✅ Verknüpft!')
    
    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_id,
        'url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Newsletter Engine v4')
    parser.add_argument('--week-offset', type=int, default=0, help='0=diese Woche, 1=nächste')
    parser.add_argument('--dry-run', action='store_true', help='Kein Klaviyo, nur Report')
    parser.add_argument('--client', type=str, default=None, help='Nur für einen Kunden')
    parser.add_argument('--skip-klaviyo', action='store_true', help='HTML generieren aber nicht hochladen')
    args = parser.parse_args()
    
    print('=' * 60)
    print('📧 NEWSLETTER ENGINE v4')
    print(f'   {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    print('=' * 60)
    
    # Step 1: Get topics from Notion
    topics = get_weekly_topics(args.week_offset)
    if not topics:
        print('\n⚠️  Keine Themen für diese Woche gefunden.')
        return
    
    # Enrich topics with briefing content
    print(f'\n📖 Notion: Briefings laden...')
    for topic in topics:
        enrich_topic_with_content(topic)
    
    # Step 2: Get clients from Airtable
    clients = get_newsletter_clients(args.client)
    if not clients:
        print('\n⚠️  Keine Newsletter-Kunden gefunden.')
        return
    
    # Step 3 + 4: Generate HTML and create Klaviyo campaigns
    results = []
    total = len(topics) * len(clients)
    current = 0
    
    print(f'\n🔨 Generiere {total} Newsletter ({len(topics)} Themen × {len(clients)} Kunden)')
    print('=' * 60)
    
    for client in clients:
        for topic in topics:
            current += 1
            print(f'\n[{current}/{total}] {client["name"]} × {topic["name"]}')
            
            # Generate HTML
            html, subject, preview = generate_newsletter_html(client, topic)
            
            # Save HTML locally
            safe_name = f'{client["name"].lower().replace(" ", "_")}_{topic["date"]}_{topic["name"][:30].lower().replace(" ", "_")}'
            html_path = os.path.join(os.path.dirname(__file__), '..', 'newsletters', f'{safe_name}.html')
            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  💾 HTML: {os.path.basename(html_path)}')
            
            # Create in Klaviyo
            if args.dry_run or args.skip_klaviyo:
                result = {'dry_run': True, 'subject': subject}
                print(f'  🏜️  DRY RUN — Subject: {subject}')
            else:
                result = create_klaviyo_campaign(client, topic, html, subject, preview)
            
            results.append({
                'client': client['name'],
                'topic': topic['name'],
                'date': topic['date'],
                'subject': subject,
                'html_file': os.path.basename(html_path),
                **result
            })
    
    # Summary
    print('\n' + '=' * 60)
    print('📊 ZUSAMMENFASSUNG')
    print('=' * 60)
    
    success = sum(1 for r in results if r.get('success') or r.get('dry_run'))
    print(f'\n✅ {success}/{len(results)} Newsletter erstellt\n')
    
    for r in results:
        status = '✅' if r.get('success') else '🏜️' if r.get('dry_run') else '❌'
        print(f'{status} {r["client"]} | {r["date"]} | {r["topic"]}')
        if r.get('url'):
            print(f'   🔗 {r["url"]}')
        if r.get('error'):
            print(f'   ❌ {r["error"]}')
    
    print(f'\n⚠️  Alle Campaigns als DRAFT erstellt — bitte in Klaviyo reviewen!')
    print('=' * 60)
    
    # Write JSON report
    report_path = os.path.join(os.path.dirname(__file__), '..', 'newsletters', 'last_run.json')
    with open(report_path, 'w') as f:
        json.dump({
            'run_date': datetime.now().isoformat(),
            'week_offset': args.week_offset,
            'topics_count': len(topics),
            'clients_count': len(clients),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    return results

if __name__ == '__main__':
    main()
