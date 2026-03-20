#!/usr/bin/env python3
"""
Newsletter Engine v4 — PHASE 2: Razeco Optimized

- Uses correct brand colors (#48413C brown primary, #0C5132 green accent)
- Uses Klaviyo images (Hero, Products, Logos)
- Better HTML with images
"""

import os
import sys
import json
import urllib.request
import urllib.error
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
    """Fetch all images from Klaviyo and categorize them"""
    print('  📸 Klaviyo: Images laden...')
    
    result = klaviyo_api(api_key, 'GET', '/images?page%5Bsize%5D=100')
    
    images = {
        'logos': [],
        'heroes': [],
        'products': [],
        'photos': [],
        'grids': [],
        'social': []
    }
    
    if 'error' in result:
        print(f'     ⚠️  Fehler: {result["error"][:100]}')
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
        elif 'social' in name or 'icon' in name:
            images['social'].append(img_data)
    
    print(f'     ✅ Logos: {len(images["logos"])}, Heroes: {len(images["heroes"])}, Products: {len(images["products"])}, Photos: {len(images["photos"])}')
    return images

def get_rotated_images(images: Dict, topic_name: str) -> Dict:
    """Rotate images based on topic to ensure variety"""
    import hashlib
    
    # Create a hash from topic name to get consistent but varied selection
    topic_hash = int(hashlib.md5(topic_name.encode()).hexdigest(), 16)
    
    heroes = images.get('heroes', [])
    photos = images.get('photos', [])
    grids = images.get('grids', [])
    logos = images.get('logos', [])
    
    # Rotate hero image based on topic
    hero_index = topic_hash % len(heroes) if heroes else 0
    hero_url = heroes[hero_index]['url'] if heroes else ''
    
    # Get 2-4 product/grid images, rotated
    grid_imgs = []
    all_products = grids + photos
    if all_products:
        start_idx = (topic_hash // 10) % len(all_products)
        for i in range(min(4, len(all_products))):
            idx = (start_idx + i) % len(all_products)
            grid_imgs.append(all_products[idx]['url'])
    
    # Rotate logo too
    logo_index = topic_hash % len(logos) if logos else 0
    logo_url = logos[logo_index]['url'] if logos else ''
    
    return {
        'hero_url': hero_url,
        'logo_url': logo_url,
        'grid_imgs': grid_imgs
    }

def generate_sale_email_v2(content: Dict, briefing: Dict, images: Dict) -> str:
    """Generate sale email with Razeco branding and rotated images"""
    
    # Razeco Brand Colors
    PRIMARY = '#48413C'      # Dark brown (main brand)
    SECONDARY = '#696255'    # Medium brown
    ACCENT = '#0C5132'       # Green (eco)
    BG_LIGHT = '#F5F4F0'     # Cream
    BG_BEIGE = '#ECEAE4'     # Light beige
    
    client = briefing['client']
    lang = client['language']
    topic = briefing['topic']['name']
    
    # Get rotated images based on topic
    rotated = get_rotated_images(images, topic)
    logo_url = rotated['logo_url']
    hero_url = rotated['hero_url']
    grid_imgs = rotated['grid_imgs']
    
    # Text content
    cta_text = 'Jetzt sparen →' if lang == 'de' else 'Shop Now →'
    shop_btn = 'Zum Shop →' if lang == 'de' else 'Shop Now →'
    
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{content['subject_line']}</title>
  <!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
  <style>
    @media only screen and (max-width: 600px) {{
      .mobile-full {{ width: 100% !important; max-width: 100% !important; }}
      .mobile-padding {{ padding: 20px !important; }}
      .mobile-stack {{ display: block !important; width: 100% !important; }}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background-color:{BG_LIGHT};font-family:'DM Sans',Arial,sans-serif;">
  
  <!-- Urgency Bar -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{ACCENT};">
    <tr>
      <td align="center" style="padding:12px 20px;">
        <p style="margin:0;font-size:13px;color:#FFFFFF;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">
          🔥 {'Nur für kurze Zeit!' if lang == 'de' else 'Limited Time Only!'}
        </p>
      </td>
    </tr>
  </table>
  
  <!-- Main -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{BG_LIGHT};">
    <tr>
      <td align="center" style="padding:20px 10px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);" class="mobile-full">
          
          <!-- Logo Header -->
          <tr>
            <td align="center" style="padding:30px 20px 20px 20px;">
              {f'<img src="{logo_url}" alt="Razeco" width="130" style="display:block;">' if logo_url else '<h2 style="color:#48413C;margin:0;font-family:DM Serif Display,Georgia,serif;">Razeco</h2>'}
            </td>
          </tr>
          
          <!-- Hero Image -->
          {f'''
          <tr>
            <td>
              <img src="{hero_url}" width="100%" style="display:block;" alt="Hero">
            </td>
          </tr>''' if hero_url else ''}
          
          <!-- Hero Text -->
          <tr>
            <td style="background:linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);padding:50px 40px;text-align:center;" class="mobile-padding">
              <h1 style="font-family:'DM Serif Display',Georgia,serif;font-size:38px;color:#FFFFFF;margin:0 0 15px 0;font-weight:normal;line-height:1.2;">
                {content['subject_line'].replace('🔥', '').strip()}
              </h1>
              <p style="font-size:18px;color:rgba(255,255,255,0.9);margin:0 0 30px 0;line-height:1.5;">
                {content.get('preview_text', '')}
              </p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                <tr>
                  <td style="background-color:#FFFFFF;border-radius:50px;padding:0;">
                    <a href="{client['website']}" style="display:inline-block;padding:16px 40px;font-size:16px;color:{PRIMARY};text-decoration:none;font-weight:700;border-radius:50px;">
                      {cta_text}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- Greeting -->
          <tr>
            <td style="padding:40px 40px 10px 40px;" class="mobile-padding">
              <p style="font-size:17px;color:{PRIMARY};margin:0;line-height:1.6;">
                {content['greeting']},
              </p>
            </td>
          </tr>
          
          <!-- Body -->
          <tr>
            <td style="padding:10px 40px;" class="mobile-padding">
              {''.join([f'<p style="font-size:16px;color:#333;margin:0 0 18px 0;line-height:1.8;">{p}</p>' for p in content.get('body_paragraphs', [])])}
            </td>
          </tr>
          
          <!-- Product Grid with Images -->
          {generate_product_grid_v2(grid_imgs or product_imgs, PRIMARY, lang) if (grid_imgs or product_imgs) else ''}
          
          <!-- Big CTA -->
          <tr>
            <td align="center" style="padding:40px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background-color:{ACCENT};border-radius:50px;padding:0;box-shadow:0 6px 20px rgba(12,81,50,0.3);">
                    <a href="{client['website']}" style="display:inline-block;padding:20px 60px;font-size:18px;color:#FFFFFF;text-decoration:none;font-weight:700;border-radius:50px;">
                      {shop_btn}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- Social Proof -->
          {generate_social_proof_v2(briefing['products'].get('social_proof', ''), PRIMARY, lang) if briefing['products'].get('social_proof') else ''}
          
          <!-- Footer -->
          <tr>
            <td style="background-color:{BG_BEIGE};padding:40px;text-align:center;">
              {f'<img src="{logo_url}" alt="Razeco" width="100" style="display:block;margin:0 auto 20px auto;opacity:0.8;">' if logo_url else ''}
              <p style="font-size:13px;color:{SECONDARY};margin:0 0 10px 0;font-style:italic;">
                shave the future.
              </p>
              <p style="font-size:12px;color:#999;margin:0;line-height:1.6;">
                Razeco UG · <a href="{client['website']}" style="color:#999;text-decoration:underline;">razeco.de</a><br>
                <a href="{{{{unsubscribe_url}}}}" style="color:#999;">{'Abmelden' if lang == 'de' else 'Unsubscribe'}</a>
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

def generate_product_grid_v2(image_urls: List[str], primary_color: str, lang: str) -> str:
    """Generate product grid with actual images"""
    if not image_urls:
        return ''
    
    html = '''
          <!-- Products -->
          <tr>
            <td style="padding:20px 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'''
    
    for i in range(0, len(image_urls[:4]), 2):
        html += '<tr>'
        
        # First product
        if i < len(image_urls):
            html += f'''
                <td width="50%" style="padding:10px;" valign="top">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F9F9F9;border-radius:12px;overflow:hidden;">
                    <tr>
                      <td>
                        <img src="{image_urls[i]}" width="100%" style="display:block;" alt="Product">
                      </td>
                    </tr>
                  </table>
                </td>'''
        
        # Second product
        if i + 1 < len(image_urls):
            html += f'''
                <td width="50%" style="padding:10px;" valign="top">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F9F9F9;border-radius:12px;overflow:hidden;">
                    <tr>
                      <td>
                        <img src="{image_urls[i+1]}" width="100%" style="display:block;" alt="Product">
                      </td>
                    </tr>
                  </table>
                </td>'''
        else:
            html += '<td width="50%"></td>'
        
        html += '</tr>'
    
    html += '''
              </table>
            </td>
          </tr>'''
    
    return html

def generate_social_proof_v2(social_proof: str, primary_color: str, lang: str) -> str:
    """Generate social proof section"""
    if not social_proof:
        return ''
    
    lines = [l.strip() for l in social_proof.split('\n') if l.strip()][:2]
    
    html = '''
          <!-- Trust -->
          <tr>
            <td style="padding:30px 40px;background-color:#F9F9F9;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'''
    
    for line in lines:
        html += f'''
                <tr>
                  <td style="padding:8px 0;text-align:center;">
                    <p style="font-size:15px;color:#666;margin:0;font-style:italic;">
                      "{line}"
                    </p>
                  </td>
                </tr>'''
    
    html += '''
              </table>
            </td>
          </tr>'''
    
    return html

def generate_content(briefing: Dict) -> Dict:
    """Generate email content"""
    lang = briefing['client']['language']
    topic = briefing['topic']['name']
    
    # Determine content based on topic
    topic_lower = topic.lower()
    
    if 'sale' in topic_lower or 'patrick' in topic_lower:
        if lang == 'de':
            return {
                'subject_line': f'🍀 {topic} — Nur heute!',
                'preview_text': 'Sichere dir die besten Deals',
                'greeting': 'Hallo {{first_name|default:"Freund"}}',
                'body_paragraphs': [
                    f'wir feiern St. Patrick\'s Day mit einem besonderen Angebot! 🎉',
                    f'Nutze die Chance und sichere dir unsere nachhaltigen Produkte zu tollen Preisen.',
                    'Das Angebot gilt nur für kurze Zeit — also sei schnell!'
                ],
                'cta_text': 'Jetzt sparen',
                'full_text': f'{topic} — Nur heute! Sichere dir die besten Deals auf nachhaltige Produkte.'
            }
    
    elif 'buy now' in topic_lower or 'pay later' in topic_lower:
        if lang == 'de':
            return {
                'subject_line': '💳 Flexibel zahlen bei Razeco',
                'preview_text': 'Buy now, pay later — oder mit kostenlosem Versand',
                'greeting': 'Hallo {{first_name|default:"Freund"}}',
                'body_paragraphs': [
                    'gute Neuigkeiten! Wir haben unsere Zahlungsoptionen erweitert.',
                    'Jetzt kannst du bequem in Raten zahlen oder von kostenlosem Versand profitieren.',
                    'Nachhaltigkeit sollte für alle erreichbar sein!'
                ],
                'cta_text': 'Mehr erfahren',
                'full_text': 'Flexibel zahlen bei Razeco — Buy now, pay later oder kostenloser Versand.'
            }
    
    elif 'bundle' in topic_lower or 'combo' in topic_lower:
        if lang == 'de':
            return {
                'subject_line': '📦 Spare mit unseren Bundles',
                'preview_text': 'Mehr kaufen, mehr sparen',
                'greeting': 'Hallo {{first_name|default:"Freund"}}',
                'body_paragraphs': [
                    'unsere beliebtesten Produkte jetzt als Bundle!',
                    'Perfekt kombiniert für dich — und dabei auch noch Geld gespart.',
                    'Entdecke unsere Sets und finde deine perfekte Kombination.'
                ],
                'cta_text': 'Bundles entdecken',
                'full_text': 'Spare mit unseren Bundles — Mehr kaufen, mehr sparen auf nachhaltige Produkte.'
            }
    
    # Default
    if lang == 'de':
        return {
            'subject_line': f'✨ {topic}',
            'preview_text': 'Neuigkeiten von Razeco',
            'greeting': 'Hallo {{first_name|default:"Freund"}}',
            'body_paragraphs': [f'wir haben Neuigkeiten für dich: {topic}!', 'Schau vorbei und entdecke mehr.'],
            'cta_text': 'Entdecken',
            'full_text': f'{topic} — Neuigkeiten von Razeco'
        }

def publish_to_klaviyo(briefing: Dict, content: Dict, html: str) -> Dict:
    """Publish to Klaviyo"""
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
                'text': content['full_text']
            }
        }
    })
    
    if 'error' in template_result:
        return {'error': 'template_failed', 'details': template_result['error']}
    
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
                                'subject': content['subject_line'],
                                'preview_text': content['preview_text'],
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
    
    # Link template
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
    
    print(f'\n📧 {briefing["client"]["name"]} | {briefing["topic"]["name"]}')
    print('=' * 50)
    
    # Load images
    images = fetch_klaviyo_images(briefing['klaviyo']['api_key'])
    
    # Generate content
    content = generate_content(briefing)
    print(f'  📝 Subject: {content["subject_line"]}')
    
    # Build HTML
    html = generate_sale_email_v2(content, briefing, images)
    
    # Save HTML
    html_file = f"{briefing['briefing_id']}_v3.html"
    html_path = os.path.join(os.path.dirname(BRIEFING_DIR), html_file)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  💾 HTML saved')
    
    # Publish
    result = publish_to_klaviyo(briefing, content, html)
    
    if result.get('success'):
        print(f'  ✅ Campaign: {result["campaign_id"]}')
        print(f'  🔗 {result["url"]}')
        
        # Update briefing
        briefing['status'] = 'done_v3'
        briefing['output'] = {
            'subject_line': content['subject_line'],
            'klaviyo_template_id': result['template_id'],
            'klaviyo_campaign_id': result['campaign_id'],
            'klaviyo_url': result['url'],
        }
        save_briefing(briefing)
    else:
        print(f'  ❌ Error: {result.get("error")}')
    
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--briefing', type=str, required=True)
    args = parser.parse_args()
    
    process_briefing(args.briefing)

if __name__ == '__main__':
    main()
