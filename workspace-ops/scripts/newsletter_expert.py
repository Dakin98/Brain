#!/usr/bin/env python3
"""
Newsletter Engine v4 — EXPERT COPYWRITER EDITION

Premium copywriting for Razeco with:
- Story-driven hooks (not generic greetings)
- Emotional triggers (identity, belonging, impact)
- AIDA structure in every email
- Value-first approach (not product-first)
- Brand voice consistency (eco-conscious, confident, premium)
"""

import os
import sys
import json
import urllib.request
import urllib.error
import hashlib
from datetime import datetime
from typing import Dict, List
import argparse

BRIEFING_DIR = os.path.join(os.path.dirname(__file__), '..', 'newsletters', 'briefings')

def load_briefing(briefing_id: str) -> Dict:
    if not briefing_id.endswith('.json'):
        briefing_id += '.json'
    filepath = os.path.join(BRIEFING_DIR, briefing_id)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_briefing(briefing: Dict):
    filename = f"{briefing['briefing_id']}.json"
    filepath = os.path.join(BRIEFING_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(briefing, f, indent=2, ensure_ascii=False)

def klaviyo_api(api_key: str, method: str, endpoint: str, data: dict = None) -> dict:
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
        return {'error': e.read().decode()}

def fetch_klaviyo_images(api_key: str) -> Dict:
    print('  📸 Loading images...')
    result = klaviyo_api(api_key, 'GET', '/images?page%5Bsize%5D=100')
    
    images = {'logos': [], 'heroes': [], 'products': [], 'photos': [], 'grids': []}
    
    if 'error' in result:
        return images
    
    for img in result.get('data', []):
        attrs = img.get('attributes', {})
        name = attrs.get('name', '').lower()
        url = attrs.get('image_url', '')
        if not url:
            continue
        
        img_data = {'name': attrs.get('name'), 'url': url}
        
        if 'logo' in name or 'stacked' in name:
            images['logos'].append(img_data)
        elif 'hero' in name:
            images['heroes'].append(img_data)
        elif 'razor' in name:
            images['products'].append(img_data)
        elif 'grid' in name:
            images['grids'].append(img_data)
        elif 'photo' in name or 'picture' in name:
            images['photos'].append(img_data)
    
    print(f'     ✅ {len(images["heroes"])} heroes, {len(images["photos"])} photos')
    return images

def get_rotated_images(images: Dict, topic_name: str) -> Dict:
    topic_hash = int(hashlib.md5(topic_name.encode()).hexdigest(), 16)
    
    heroes = images.get('heroes', [])
    photos = images.get('photos', [])
    grids = images.get('grids', [])
    logos = images.get('logos', [])
    
    hero_index = topic_hash % len(heroes) if heroes else 0
    hero_url = heroes[hero_index]['url'] if heroes else ''
    
    grid_imgs = []
    all_products = grids + photos
    if all_products:
        start_idx = (topic_hash // 10) % len(all_products)
        for i in range(min(4, len(all_products))):
            idx = (start_idx + i) % len(all_products)
            grid_imgs.append(all_products[idx]['url'])
    
    logo_index = topic_hash % len(logos) if logos else 0
    logo_url = logos[logo_index]['url'] if logos else ''
    
    return {'hero_url': hero_url, 'logo_url': logo_url, 'grid_imgs': grid_imgs}

# ═══════════════════════════════════════════════════════════════════════════
# EXPERT COPYWRITING TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════

def generate_st_patricks_copy() -> Dict:
    """St. Patrick's Day - Theme: Luck meets sustainability"""
    return {
        'subject': 'Glück gehabt 🍀 Heute sparst du doppelt',
        'preview': 'Grün ist nicht nur die Farbe des Glücks...',
        'headline': 'Heute ist dein Glückstag',
        'body': [
            'St. Patrick\'s Day steht für Glück, Grün und gute Taten.',
            '',
            'Passend dazu: Unser **System Razor** — der erste biobasierte Rasierer mit schwedischen Premium-Stahlklingen.',
            '',
            'Denn Grün ist nicht nur die Farbe des Glücks — es ist auch die Farbe einer Zukunft ohne Plastikmüll im Badezimmer.',
            '',
            'Heute schenken wir dir 24h lang **doppeltes Glück**:',
            '✓ System Razor Face oder Body für €24.99 (statt €29.99)',
            '✓ Oder das System Bundle für €37.96 — du sparst €12',
            '✓ Gratis Versand für alle Bestellungen',
            '',
            'TÜV Austria 4-Sterne zertifiziert. Made in Germany.',
        ],
        'cta': 'Jetzt Glück machen →',
        'closing': 'Viel Glück!<br>Das Razeco Team',
        'full_text': 'St. Patrick\'s Day Special: System Razor für €24.99 oder Bundle für €37.96 (spare €12) + Gratis Versand. TÜV Austria zertifiziert.'
    }

def generate_bnpl_copy() -> Dict:
    """Buy Now Pay Later - Theme: Accessibility meets values"""
    return {
        'subject': 'Nachhaltigkeit sollte nicht teuer sein',
        'preview': 'Jetzt: Flexibel zahlen oder kostenlos geliefert',
        'headline': 'Gute Entscheidungen müssen nicht warten',
        'body': [
            'Du willst umsteigen auf plastikfreie Rasur — aber €24.99 für den System Razor auf einmal?',
            '',
            'Wir sagen: Der beste Zeitpunkt ist jetzt. Und der beste Preis auch.',
            '',
            'Deshalb gibt es ab sofort zwei neue Möglichkeiten:',
            '',
            '**1. Flexibel zahlen**\n',
            'System Razor Face oder Body in 3 Raten à €8.33 — ohne Zinsen, ohne Stress.',
            '',
            '**2. Kostenloser Versand**\n',
            'Auch für Refills (Face & Body) und das Oneway Rosé — immer kostenlos.',
            '',
            'Weil 99% biobasierte Qualität für alle erreichbar sein sollte.',
        ],
        'cta': 'Flexibel starten →',
        'closing': 'Für dich und den Planeten,<br>Razeco',
        'full_text': 'Neu bei Razeco: System Razor in 3 Raten à €8.33 oder kostenloser Versand für alle Produkte. 99% biobasiert, TÜV Austria zertifiziert.'
    }

def generate_bundle_copy() -> Dict:
    """Bundles - Theme: Smart choices, better together"""
    return {
        'subject': 'Die perfekte Kombination (spare €12)',
        'preview': 'Unser Bestseller-Bundle — limitiert verfügbar',
        'headline': 'Manche Dinge funktionieren einfach besser zusammen',
        'body': [
            'Wie Gesicht und Körper.',
            'Oder dein System Razor und die passenden Refills.',
            '',
            'Unsere Kunden haben gesprochen: Die meisten kaufen gleich beide Rasierer — einen fürs Gesicht, einen für den Körper.',
            '',
            'Deshalb gibt es jetzt das **System Bundle**:',
            '',
            '**System Razor Face + Body**\n',
            '• 2x System Razor (Wert: €49.98)',
            '• Je 2 Klingen vorinstalliert',
            '• Dein Preis: nur €37.96',
            '',
            'Du sparst €12 — und wir sparen zusammen Verpackung.',
            '',
            'Nur solange der Vorrat reicht.',
        ],
        'cta': 'Bundle sichern →',
        'closing': 'Smart kombiniert,<br>Dein Razeco Team',
        'full_text': 'Razeco System Bundle: Face + Body Rasierer für €37.96 (statt €49.98). Du sparst €12, wir sparen Verpackung. TÜV Austria zertifiziert.'
    }

def generate_womens_day_copy() -> Dict:
    """Women's Day - Theme: Empowerment meets sustainability"""
    return {
        'subject': 'Für alle, die jeden Tag etwas bewegen 💪',
        'preview': 'Heute feiern wir starke Frauen — und eine starke Zukunft',
        'headline': 'Starke Frauen. Starke Entscheidungen.',
        'body': [
            'Der Internationale Frauentag ist mehr als ein Datum.',
            '',
            'Er erinnert uns daran, dass echte Veränderung durch kleine, tägliche Entscheidungen entsteht.',
            '',
            'Durch Frauen, die Neues wagen.',
            'Durch Frauen, die sich nicht mit dem Status quo zufrieden geben.',
            'Durch Frauen, die wissen: Jede Entscheidung zählt.',
            '',
            'Genau das verbindet uns mit dir.',
            '',
            'Wenn du heute Razeco wählst, entscheidest du dich für 12.000+ zufriedene Kunden, die genau wie du jeden Tag etwas bewegen.',
            '',
            'Für dich. Für unsere Welt. Für die nächste Generation.',
        ],
        'cta': 'Mitmachen →',
        'closing': 'In Bewegung,<br>Das Razeco Team',
        'full_text': 'Internationaler Frauentag: Wir feiern starke Frauen und tägliche Entscheidungen, die die Welt verändern.'
    }

def generate_sale_copy(topic: str) -> Dict:
    """Generic sale - create urgency with value"""
    return {
        'subject': 'Nur für dich: Ein besonderes Angebot',
        'preview': 'Limitiert — nur die nächsten 24 Stunden',
        'headline': 'Einmal, nicht wiederholbar',
        'body': [
            'Dieses Angebot gibt es nur heute.',
            '',
            'Nicht nächste Woche. Nicht im nächsten Sale.',
            'Nur jetzt.',
            '',
            'Warum? Weil wir uns bei Razeco für Qualität statt Masse entschieden haben.',
            'Und Qualität hat ihren Preis — außer heute.',
            '',
            'Nutze die nächsten 24 Stunden und sichere dir Premium-Nachhaltigkeit zum Bestpreis.',
        ],
        'cta': 'Angebot sichern →',
        'closing': 'Nur für kurze Zeit,<br>Razeco',
        'full_text': 'Limitiertes Angebot — nur 24h. Premium-Nachhaltigkeit zum Bestpreis bei Razeco.'
    }

def generate_expert_copy(topic: str) -> Dict:
    """Generate expert-level copy based on topic"""
    topic_lower = topic.lower()
    
    if 'patrick' in topic_lower:
        return generate_st_patricks_copy()
    elif 'buy now' in topic_lower or 'pay later' in topic_lower or 'free shipping' in topic_lower:
        return generate_bnpl_copy()
    elif 'bundle' in topic_lower or 'combo' in topic_lower:
        return generate_bundle_copy()
    elif 'women' in topic_lower or 'frau' in topic_lower:
        return generate_womens_day_copy()
    elif 'sale' in topic_lower or 'deal' in topic_lower:
        return generate_sale_copy(topic)
    else:
        # Generic but better
        return {
            'subject': f'Neuigkeiten von Razeco ✨',
            'preview': f'Schau dir an, was wir für dich vorbereitet haben',
            'headline': f'{topic}',
            'body': [
                f'Wir haben etwas Neues für dich: {topic}.',
                '',
                'Bei Razeco stehen Nachhaltigkeit und Qualität im Mittelpunkt.',
                'Entdecke, was das für dich bedeutet.',
            ],
            'cta': 'Entdecken →',
            'closing': 'Mit besten Grüßen,<br>Razeco',
            'full_text': f'{topic} bei Razeco — Nachhaltigkeit trifft auf Qualität.'
        }

# ═══════════════════════════════════════════════════════════════════════════
# HTML GENERATION
# ═══════════════════════════════════════════════════════════════════════════

BRAND = {
    'primary': '#48413C',
    'secondary': '#696255', 
    'accent': '#0C5132',
    'cream': '#F5F4F0',
    'beige': '#ECEAE4',
    'font_heading': "'DM Serif Display',Georgia,serif",
    'font_body': "'DM Sans',Arial,sans-serif",
}

# Razeco Product Catalog
PRODUCTS = {
    'system_razor_face': {
        'name': 'System Razor · Face',
        'price': '24.99',
        'url': 'https://www.razeco.com/en-de/products/system-razor-face',
        'image': 'https://cdn.shopify.com/s/files/1/0892/0131/2077/files/face_razor_updated.png',
        'description': 'Biobasierter Rasierer für das Gesicht'
    },
    'system_razor_body': {
        'name': 'System Razor · Body',
        'price': '24.99',
        'url': 'https://www.razeco.com/en-de/products/system-razor-body',
        'image': 'https://cdn.shopify.com/s/files/1/0892/0131/2077/files/body_razor_updated.png',
        'description': 'Biobasierter Rasierer für den Körper'
    },
    'system_bundle': {
        'name': 'System Bundle',
        'price': '37.96',
        'original_price': '49.98',
        'url': 'https://www.razeco.com/en-de/products/system-bundle',
        'image': 'https://cdn.shopify.com/s/files/1/0892/0131/2077/files/Frame_8044.png',
        'description': 'Face + Body — Du sparst €12',
        'badge': 'BESTSELLER'
    },
    'oneway_rose': {
        'name': 'Oneway Rosé',
        'price': '9.99',
        'url': 'https://www.razeco.com/en-de/products/oneway-rose',
        'image': 'https://cdn.shopify.com/s/files/1/0892/0131/2077/files/oneway_rose.png',
        'description': 'Der nachhaltige Einwegrasierer'
    }
}

def generate_product_showcase(grid_imgs: List[str], briefing: Dict) -> str:
    """Generate product cards with prices and CTAs"""
    topic = briefing['topic']['name'].lower()
    lang = briefing['client']['language']
    
    # Determine which products to show based on topic
    if 'bundle' in topic or 'combo' in topic:
        products_to_show = ['system_bundle', 'system_razor_face', 'system_razor_body']
    elif 'patrick' in topic or 'sale' in topic:
        products_to_show = ['system_razor_face', 'system_razor_body', 'system_bundle']
    elif 'flexibel' in topic or 'pay later' in topic:
        products_to_show = ['system_razor_face', 'system_razor_body']
    else:
        products_to_show = ['system_bundle', 'system_razor_face']
    
    shop_btn = 'Jetzt shoppen' if lang == 'de' else 'Shop Now'
    
    html = f'''
          <!-- Products -->
          <tr>
            <td style="padding:40px 30px 20px 30px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'''
    
    for i, product_key in enumerate(products_to_show):
        if product_key not in PRODUCTS:
            continue
            
        product = PRODUCTS[product_key]
        
        # Alternate layout: full width product cards
        html += f'''
                <tr>
                  <td style="padding:15px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:linear-gradient(135deg, {BRAND['cream']} 0%, #FFFFFF 100%);border-radius:20px;overflow:hidden;border:1px solid {BRAND['beige']};">
                      <tr>
                        <td width="40%" style="padding:20px;">
                          <img src="{product['image']}" width="100%" style="display:block;border-radius:12px;" alt="{product['name']}">
                        </td>
                        <td width="60%" style="padding:25px 25px 25px 10px;" valign="middle">
                          {f'<span style="display:inline-block;background-color:{BRAND["accent"]};color:#FFFFFF;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;margin-bottom:10px;">{product["badge"]}</span>' if product.get('badge') else ''}
                          <h3 style="font-family:{BRAND['font_heading']};font-size:24px;color:{BRAND['primary']};margin:0 0 8px 0;font-weight:normal;">
                            {product['name']}
                          </h3>
                          <p style="font-size:14px;color:#666;margin:0 0 15px 0;line-height:1.5;">
                            {product['description']}
                          </p>
                          <p style="font-size:14px;color:#666;margin:0 0 10px 0;">
                            ✓ 99% biobasiert<br>
                            ✓ TÜV Austria zertifiziert
                          </p>
                          <p style="font-size:28px;color:{BRAND['accent']};margin:0 0 15px 0;font-weight:700;">
                            €{product['price']}
                            {f'<span style="font-size:16px;color:#999;text-decoration:line-through;margin-left:8px;">€{product["original_price"]}</span>' if product.get('original_price') else ''}
                          </p>
                          <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                              <td style="background-color:{BRAND['primary']};border-radius:50px;padding:0;">
                                <a href="{product['url']}" style="display:inline-block;padding:14px 32px;font-size:15px;color:#FFFFFF;text-decoration:none;font-weight:600;border-radius:50px;">
                                  {shop_btn} →
                                </a>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>'''
    
    html += '''
              </table>
            </td>
          </tr>'''
    
    return html

def generate_expert_html(copy: Dict, briefing: Dict, images: Dict) -> str:
    """Generate HTML with expert copy and design"""
    
    rotated = get_rotated_images(images, briefing['topic']['name'])
    logo_url = rotated['logo_url']
    hero_url = rotated['hero_url']
    grid_imgs = rotated['grid_imgs']
    
    client = briefing['client']
    lang = client['language']
    
    # Build body paragraphs
    body_html = ''
    for para in copy['body']:
        if para == '':
            body_html += '<tr><td style="padding:5px 40px;"></td></tr>'
        elif para.startswith('**') and para.endswith('**'):
            # Subheading
            text = para.replace('**', '')
            body_html += f'''
          <tr>
            <td style="padding:10px 40px 5px 40px;" class="mobile-padding">
              <p style="font-size:16px;font-weight:700;color:{BRAND['primary']};margin:0;line-height:1.5;">
                {text}
              </p>
            </td>
          </tr>'''
        elif para.startswith('✓'):
            # Bullet point
            body_html += f'''
          <tr>
            <td style="padding:5px 40px 5px 60px;" class="mobile-padding">
              <p style="font-size:16px;color:#333;margin:0;line-height:1.6;">
                {para}
              </p>
            </td>
          </tr>'''
        else:
            # Regular paragraph
            # Handle bold text
            para_formatted = para.replace('**', '<strong>').replace('**', '</strong>')
            body_html += f'''
          <tr>
            <td style="padding:8px 40px;" class="mobile-padding">
              <p style="font-size:17px;color:#333;margin:0;line-height:1.8;font-family:{BRAND['font_body']};">
                {para_formatted}
              </p>
            </td>
          </tr>'''
    
    # Product showcase with actual products
    products_html = generate_product_showcase(grid_imgs, briefing)
    
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{copy['subject']}</title>
  <style>
    @media only screen and (max-width: 600px) {{
      .mobile-full {{ width: 100% !important; max-width: 100% !important; }}
      .mobile-padding {{ padding: 24px !important; }}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background-color:{BRAND['cream']};font-family:{BRAND['font_body']};">
  
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{BRAND['cream']};">
    <tr>
      <td align="center" style="padding:30px 15px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:20px;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,0.06);" class="mobile-full">
          
          <!-- Logo -->
          <tr>
            <td align="center" style="padding:40px 20px 30px 20px;">
              {f'<img src="{logo_url}" alt="Razeco" width="140" style="display:block;">' if logo_url else '<h2 style="color:#48413C;margin:0;font-family:DM Serif Display,Georgia,serif;font-size:28px;">Razeco</h2>'}
            </td>
          </tr>
          
          <!-- Hero Image -->
          {f'''
          <tr>
            <td style="padding:0 30px;">
              <img src="{hero_url}" width="100%" style="display:block;border-radius:16px;" alt="Hero">
            </td>
          </tr>''' if hero_url else ''}
          
          <!-- Headline -->
          <tr>
            <td style="padding:50px 40px 20px 40px;" class="mobile-padding">
              <h1 style="font-family:{BRAND['font_heading']};font-size:42px;color:{BRAND['primary']};margin:0;font-weight:normal;line-height:1.2;text-align:center;">
                {copy['headline']}
              </h1>
            </td>
          </tr>
          
          <!-- Divider -->
          <tr>
            <td align="center" style="padding:10px 40px 30px 40px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="60" style="border-top:2px solid {BRAND['accent']};">
                <tr><td></td></tr>
              </table>
            </td>
          </tr>
          
          <!-- Body -->
          {body_html}
          
          <!-- Products -->
          {products_html}
          
          <!-- CTA -->
          <tr>
            <td align="center" style="padding:50px 40px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background-color:{BRAND['accent']};border-radius:50px;padding:0;box-shadow:0 8px 30px rgba(12,81,50,0.25);">
                    <a href="https://razeco.de" style="display:inline-block;padding:22px 70px;font-size:18px;color:#FFFFFF;text-decoration:none;font-weight:700;border-radius:50px;letter-spacing:0.5px;">
                      {copy['cta']}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- Closing -->
          <tr>
            <td style="padding:0 40px 40px 40px;" class="mobile-padding">
              <p style="font-size:17px;color:{BRAND['primary']};margin:0;line-height:1.7;text-align:center;">
                {copy['closing']}
              </p>
            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="background-color:{BRAND['beige']};padding:40px;text-align:center;">
              <p style="font-size:12px;color:#888;margin:0 0 8px 0;letter-spacing:1px;text-transform:uppercase;">
                shave the future.
              </p>
              <p style="font-size:11px;color:#AAA;margin:0;line-height:1.6;">
                Razeco UG · <a href="https://razeco.de" style="color:#AAA;text-decoration:none;">razeco.de</a><br>
                <a href="{{{{unsubscribe_url}}}}" style="color:#AAA;">Abmelden</a>
              </p>
            </td>
          </tr>
          
        </table>
      </td>
    </tr>
  </table>
</body>
</html>'''
    
    return html

def publish_to_klaviyo(briefing: Dict, copy: Dict, html: str) -> Dict:
    api_key = briefing['klaviyo']['api_key']
    list_id = briefing['klaviyo']['list_id']
    name = f"{briefing['client']['name']} | {briefing['topic']['name']} | {briefing['topic']['date']}"
    
    if not list_id:
        return {'error': 'no_list_id'}
    
    # Template
    template_result = klaviyo_api(api_key, 'POST', '/templates', {
        'data': {
            'type': 'template',
            'attributes': {
                'name': name,
                'editor_type': 'CODE',
                'html': html,
                'text': copy['full_text']
            }
        }
    })
    
    if 'error' in template_result:
        return {'error': 'template_failed'}
    
    template_id = template_result['data']['id']
    
    # Campaign
    send_datetime = f"{briefing['topic']['date']}T09:00:00+01:00"
    campaign_result = klaviyo_api(api_key, 'POST', '/campaigns', {
        'data': {
            'type': 'campaign',
            'attributes': {
                'name': name,
                'audiences': {'included': [list_id], 'excluded': []},
                'send_strategy': {'method': 'static', 'options_static': {'datetime': send_datetime}},
                'campaign-messages': {
                    'data': [{
                        'type': 'campaign-message',
                        'attributes': {
                            'channel': 'email',
                            'label': 'Default',
                            'content': {
                                'subject': copy['subject'],
                                'preview_text': copy['preview'],
                                'from_email': 'hello@razeco.de',
                                'from_label': 'Razeco'
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
    
    # Link
    klaviyo_api(api_key, 'POST', '/campaign-message-assign-template', {
        'data': {
            'type': 'campaign-message',
            'id': message_id,
            'relationships': {'template': {'data': {'type': 'template', 'id': template_id}}}
        }
    })
    
    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_id,
        'url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

def process_briefing(briefing_file: str):
    briefing = load_briefing(briefing_file)
    
    print(f'\n🎯 {briefing["client"]["name"]} | {briefing["topic"]["name"]}')
    print('=' * 55)
    
    # Generate expert copy
    copy = generate_expert_copy(briefing['topic']['name'])
    print(f'  ✍️  Subject: {copy["subject"]}')
    print(f'  📰 Headline: {copy["headline"]}')
    
    # Load images
    images = fetch_klaviyo_images(briefing['klaviyo']['api_key'])
    
    # Build HTML
    html = generate_expert_html(copy, briefing, images)
    
    # Save
    html_file = f"{briefing['briefing_id']}_expert.html"
    html_path = os.path.join(os.path.dirname(BRIEFING_DIR), html_file)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Publish
    result = publish_to_klaviyo(briefing, copy, html)
    
    if result.get('success'):
        print(f'  ✅ Campaign: {result["campaign_id"]}')
        print(f'  🔗 {result["url"]}')
        
        briefing['status'] = 'expert_done'
        briefing['output'] = {
            'subject': copy['subject'],
            'headline': copy['headline'],
            'klaviyo_url': result['url'],
        }
        save_briefing(briefing)
    else:
        print(f'  ❌ {result.get("error")}')
    
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--briefing', type=str, required=True)
    args = parser.parse_args()
    
    process_briefing(args.briefing)

if __name__ == '__main__':
    main()
