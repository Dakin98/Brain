#!/usr/bin/env python3
"""
Newsletter Engine v4 — PHASE 2: Advanced Content Generator

Features:
- Analyzes Notion example images for design patterns
- Fetches Klaviyo brand images (logos, products)
- Email-type specific templates (Tips, Reviews, Sale, etc.)
- High-quality HTML based on reference designs
"""

import os
import sys
import json
import urllib.request
import urllib.error
import base64
from datetime import datetime
from typing import Dict, List, Optional, Tuple
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
        return {'error': e.read().decode()}

def fetch_klaviyo_images(api_key: str) -> Dict:
    """Fetch brand images from Klaviyo"""
    print('  📸 Klaviyo: Brand Images laden...')
    
    images = {
        'logos': [],
        'heroes': [],
        'products': [],
        'lifestyle': [],
        'social_icons': []
    }
    
    # Get images from Klaviyo
    result = klaviyo_api(api_key, 'GET', '/images?page%5Bsize%5D=100')
    
    if 'error' in result:
        print(f'     ⚠️  Konnte Images nicht laden: {result["error"][:100]}')
        return images
    
    for img in result.get('data', []):
        attrs = img.get('attributes', {})
        name = attrs.get('name', '').lower()
        url = attrs.get('image_url', '')
        
        if not url:
            continue
        
        # Categorize by name
        if any(kw in name for kw in ['logo', 'brand', 'header']):
            images['logos'].append({'name': attrs.get('name'), 'url': url})
        elif any(kw in name for kw in ['hero', 'banner', 'welcome']):
            images['heroes'].append({'name': attrs.get('name'), 'url': url})
        elif any(kw in name for kw in ['product', 'razor', 'item']):
            images['products'].append({'name': attrs.get('name'), 'url': url})
        elif any(kw in name for kw in ['lifestyle', 'photo', 'scene']):
            images['lifestyle'].append({'name': attrs.get('name'), 'url': url})
        elif any(kw in name for kw in ['social', 'instagram', 'facebook']):
            images['social_icons'].append({'name': attrs.get('name'), 'url': url})
    
    print(f'     ✅ Logos: {len(images["logos"])}, Heroes: {len(images["heroes"])}, Products: {len(images["products"])}')
    return images

def analyze_email_type(topic_name: str) -> str:
    """Determine email type from topic name"""
    topic_lower = topic_name.lower()
    
    if any(kw in topic_lower for kw in ['sale', 'flash', 'deal', 'discount', 'black friday', 'cyber', 'promo']):
        return 'sale'
    elif any(kw in topic_lower for kw in ['review', 'testimonial', 'social proof', 'before & after', 'ugc']):
        return 'social_proof'
    elif any(kw in topic_lower for kw in ['tip', 'trick', 'how to', 'guide', 'faq', 'education', 'myth']):
        return 'education'
    elif any(kw in topic_lower for kw in ['product', 'feature', 'best-seller', 'recommended', 'new arrival']):
        return 'product_showcase'
    elif any(kw in topic_lower for kw in ['brand', 'mission', 'story', 'founder', 'behind']):
        return 'brand_story'
    elif any(kw in topic_lower for kw in ['giveaway', 'contest', 'win']):
        return 'giveaway'
    elif any(kw in topic_lower for kw in ['survey', 'feedback', 'quiz']):
        return 'survey'
    elif any(kw in topic_lower for kw in ['holiday', 'christmas', 'valentine', 'mother', 'father', 'halloween', 'easter']):
        return 'holiday'
    elif any(kw in topic_lower for kw in ['refer', 'friend', 'invite']):
        return 'referral'
    else:
        return 'newsletter'

def get_email_template(email_type: str, colors: Dict, fonts: Dict) -> Dict:
    """Get layout template based on email type"""
    
    templates = {
        'sale': {
            'hero_style': 'full_width_gradient',
            'product_grid': '3_column',
            'cta_style': 'large_button_center',
            'urgency_banner': True,
            'social_proof_placement': 'below_products',
        },
        'social_proof': {
            'hero_style': 'testimonial_focus',
            'product_grid': 'none',
            'cta_style': 'text_link',
            'testimonial_grid': '2_column',
            'star_rating': True,
        },
        'education': {
            'hero_style': 'clean_text',
            'product_grid': 'none',
            'cta_style': 'button_inline',
            'tip_box': True,
            'step_by_step': True,
        },
        'product_showcase': {
            'hero_style': 'hero_product',
            'product_grid': '2_column_large',
            'cta_style': 'product_buttons',
            'price_highlight': True,
        },
        'brand_story': {
            'hero_style': 'lifestyle_image',
            'product_grid': 'minimal',
            'cta_style': 'story_cta',
            'mission_quote': True,
        },
        'giveaway': {
            'hero_style': 'celebration',
            'product_grid': 'prize_display',
            'cta_style': 'enter_now',
            'countdown': True,
        },
        'survey': {
            'hero_style': 'clean_ask',
            'product_grid': 'none',
            'cta_style': 'take_survey',
            'progress_bar': False,
        },
        'newsletter': {
            'hero_style': 'standard',
            'product_grid': '2_column',
            'cta_style': 'standard_button',
            'content_blocks': True,
        }
    }
    
    return templates.get(email_type, templates['newsletter'])

def generate_sale_email(content: Dict, briefing: Dict, template: Dict, klaviyo_images: Dict) -> str:
    """Generate sale/promotion email with urgency elements"""
    
    brand = briefing['brand']
    client = briefing['client']
    colors = brand['colors']
    
    # Colors
    primary = colors.get('primary', '#333')
    accent = colors.get('accent', '#FF6B35')  # Sale accent color
    
    # Get hero image
    hero_img = klaviyo_images['heroes'][0]['url'] if klaviyo_images['heroes'] else ''
    logo_url = brand.get('logo_url') or (klaviyo_images['logos'][0]['url'] if klaviyo_images['logos'] else '')
    
    # Product images (up to 3)
    product_imgs = [p['url'] for p in klaviyo_images['products'][:3]]
    
    html = f'''<!DOCTYPE html>
<html lang="{client['language']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{content['subject_line']}</title>
  <!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
  <style>
    @media only screen and (max-width: 600px) {{
      .mobile-full {{ width: 100% !important; max-width: 100% !important; }}
      .mobile-padding {{ padding: 20px !important; }}
      .mobile-hide {{ display: none !important; }}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background-color:#F5F5F5;font-family:Arial,sans-serif;">
  
  <!-- Urgency Banner -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{accent};">
    <tr>
      <td align="center" style="padding:10px 20px;">
        <p style="margin:0;font-size:13px;color:#FFFFFF;font-weight:bold;letter-spacing:1px;text-transform:uppercase;">
          🔥 {'Nur für kurze Zeit!' if client['language'] == 'de' else 'Limited Time Only!'}
        </p>
      </td>
    </tr>
  </table>
  
  <!-- Main Container -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F5F5F5;">
    <tr>
      <td align="center" style="padding:20px 10px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;border-radius:8px;overflow:hidden;" class="mobile-full">
          
          <!-- Header -->
          <tr>
            <td align="center" style="padding:25px 20px;">
              {f'<img src="{logo_url}" alt="{client["name"]}" width="140" style="display:block;">' if logo_url else f'<h2 style="color:{primary};margin:0;">{client["name"]}</h2>'}
            </td>
          </tr>
          
          <!-- Hero -->
          <tr>
            <td style="background:linear-gradient(135deg, {accent} 0%, {primary} 100%);padding:50px 30px;text-align:center;" class="mobile-padding">
              <h1 style="font-size:36px;color:#FFFFFF;margin:0 0 15px 0;font-weight:bold;line-height:1.2;">
                {content['subject_line'].replace('🔥', '').strip()}
              </h1>
              <p style="font-size:18px;color:rgba(255,255,255,0.9);margin:0 0 25px 0;">
                {content.get('preview_text', '')}
              </p>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
                <tr>
                  <td style="background-color:#FFFFFF;border-radius:50px;padding:0;">
                    <a href="{client['website']}" style="display:inline-block;padding:16px 40px;font-size:16px;color:{accent};text-decoration:none;font-weight:bold;border-radius:50px;">
                      {content.get('cta_text', 'Jetzt sparen!' if client['language'] == 'de' else 'Shop Now')}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- Greeting -->
          <tr>
            <td style="padding:30px 30px 10px 30px;" class="mobile-padding">
              <p style="font-size:16px;color:{primary};margin:0;line-height:1.6;">
                {content['greeting']},
              </p>
            </td>
          </tr>
          
          <!-- Body -->
          <tr>
            <td style="padding:10px 30px;" class="mobile-padding">
              {''.join([f'<p style="font-size:16px;color:#333;margin:0 0 15px 0;line-height:1.7;">{p}</p>' for p in content.get('body_paragraphs', [])])}
            </td>
          </tr>
          
          <!-- Products Grid -->
          {generate_product_grid(product_imgs, accent, client['language']) if product_imgs else ''}
          
          <!-- Main CTA -->
          <tr>
            <td align="center" style="padding:30px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background-color:{accent};border-radius:50px;padding:0;box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                    <a href="{client['website']}" style="display:inline-block;padding:18px 50px;font-size:18px;color:#FFFFFF;text-decoration:none;font-weight:bold;border-radius:50px;">
                      {'Zum Sale →' if client['language'] == 'de' else 'Shop Sale →'}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- Social Proof -->
          {generate_social_proof(briefing['products'].get('social_proof', ''), client['language']) if briefing['products'].get('social_proof') else ''}
          
          <!-- Footer -->
          <tr>
            <td style="background-color:#F8F8F8;padding:30px;text-align:center;border-top:1px solid #EEEEEE;">
              <p style="font-size:12px;color:#999;margin:0 0 10px 0;">
                {client['name']} | {brand.get('tagline', '')}
              </p>
              <p style="font-size:11px;color:#AAA;margin:0;">
                <a href="{client['website']}" style="color:#AAA;">{client['website'].replace('https://', '')}</a> | 
                <a href="{{{{unsubscribe_url}}}}" style="color:#AAA;">{'Abmelden' if client['language'] == 'de' else 'Unsubscribe'}</a>
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

def generate_product_grid(image_urls: List[str], accent_color: str, lang: str) -> str:
    """Generate 3-column product grid"""
    if not image_urls:
        return ''
    
    html = '''
          <!-- Products -->
          <tr>
            <td style="padding:20px 30px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'''
    
    for i, url in enumerate(image_urls[:3]):
        if i % 3 == 0:
            html += '<tr>'
        
        html += f'''
                <td width="33%" style="padding:10px;" valign="top">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F9F9F9;border-radius:8px;overflow:hidden;">
                    <tr>
                      <td style="padding:15px;text-align:center;">
                        <img src="{url}" width="100%" style="display:block;border-radius:4px;" alt="Product">
                      </td>
                    </tr>
                  </table>
                </td>'''
        
        if i % 3 == 2 or i == len(image_urls) - 1:
            html += '</tr>'
    
    html += '''
              </table>
            </td>
          </tr>'''
    
    return html

def generate_social_proof(social_proof: str, lang: str) -> str:
    """Generate social proof section"""
    if not social_proof:
        return ''
    
    lines = [l.strip() for l in social_proof.split('\n') if l.strip()][:2]
    
    html = '''
          <!-- Social Proof -->
          <tr>
            <td style="padding:20px 30px;background-color:#F9F9F9;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'''
    
    for line in lines:
        html += f'''
                <tr>
                  <td style="padding:10px;text-align:center;">
                    <p style="font-size:14px;color:#666;margin:0;font-style:italic;">
                      ⭐ "{line}"
                    </p>
                  </td>
                </tr>'''
    
    html += '''
              </table>
            </td>
          </tr>'''
    
    return html

def generate_content_with_ai_advanced(briefing: Dict, email_type: str) -> Dict:
    """Generate personalized content based on email type"""
    
    lang = briefing['client']['language']
    topic = briefing['topic']['name']
    instructions = briefing['topic']['briefing_instructions']
    brand_tone = briefing['brand']['tone']
    usps = briefing['products'].get('usps', '')
    
    # Email-type specific content generation
    content_templates = {
        'sale': {
            'de': {
                'subject': f'🔥 {topic} — Nur für kurze Zeit!',
                'preview': 'Sichere dir jetzt die besten Deals',
                'cta': 'Jetzt shoppen →',
            },
            'en': {
                'subject': f'🔥 {topic} — Limited Time!',
                'preview': 'Get the best deals now',
                'cta': 'Shop Now →',
            }
        },
        'social_proof': {
            'de': {
                'subject': f'⭐ Das sagen unsere Kunden über {briefing["client"]["name"]}',
                'preview': 'Echte Bewertungen von echten Menschen',
                'cta': 'Mehr erfahren →',
            },
            'en': {
                'subject': f'⭐ What customers say about {briefing["client"]["name"]}',
                'preview': 'Real reviews from real people',
                'cta': 'Learn More →',
            }
        },
        'education': {
            'de': {
                'subject': f'💡 {topic}',
                'preview': 'Unsere besten Tipps für dich',
                'cta': 'Tipps ansehen →',
            },
            'en': {
                'subject': f'💡 {topic}',
                'preview': 'Our best tips for you',
                'cta': 'View Tips →',
            }
        }
    }
    
    template = content_templates.get(email_type, content_templates['sale'])
    lang_template = template.get(lang, template['en'])
    
    # Build paragraphs based on briefing
    paragraphs = []
    
    if 'de' in lang:
        paragraphs = [
            f'wir haben etwas Besonderes für dich: {topic}!',
            f'{instructions[:200] if instructions else "Entdecke unsere neuesten Angebote und finde genau das, was du suchst."}'
        ]
        greeting = 'Hallo {{first_name|default:"Freund"}}'
        closing = f'Viele Grüße,<br>Dein {briefing["client"]["name"]} Team'
        full_text = f'{lang_template["subject"]}\n\n{paragraphs[0]}\n{paragraphs[1]}\n\n{lang_template["cta"]}'
    else:
        paragraphs = [
            f'we have something special for you: {topic}!',
            f'{instructions[:200] if instructions else "Discover our latest offers and find exactly what you're looking for."}'
        ]
        greeting = 'Hello {{first_name|default:"there"}}'
        closing = f'Best regards,<br>The {briefing["client"]["name"]} Team'
        full_text = f'{lang_template["subject"]}\n\n{paragraphs[0]}\n{paragraphs[1]}\n\n{lang_template["cta"]}'
    
    return {
        'subject_line': lang_template['subject'],
        'preview_text': lang_template['preview'],
        'greeting': greeting,
        'body_paragraphs': paragraphs,
        'cta_text': lang_template['cta'],
        'closing': closing,
        'full_text': full_text
    }

def process_briefing_advanced(briefing_file: str, dry_run: bool = False):
    """Process briefing with full feature set"""
    
    briefing = load_briefing(briefing_file)
    
    print('=' * 60)
    print(f'📧 {briefing["client"]["name"]} | {briefing["topic"]["name"]}')
    print('=' * 60)
    
    # 1. Determine email type
    email_type = analyze_email_type(briefing['topic']['name'])
    print(f'  📧 Email Type: {email_type}')
    
    # 2. Get Klaviyo images
    klaviyo_images = fetch_klaviyo_images(briefing['klaviyo']['api_key'])
    
    # 3. Get template config
    template_config = get_email_template(email_type, briefing['brand']['colors'], {})
    
    # 4. Generate content
    print('  🤖 Generiere Content...')
    content = generate_content_with_ai_advanced(briefing, email_type)
    
    # 5. Build HTML based on email type
    print(f'  🎨 Baue {email_type} HTML...')
    
    if email_type == 'sale':
        html = generate_sale_email(content, briefing, template_config, klaviyo_images)
    else:
        # Fallback to standard template for now
        html = generate_sale_email(content, briefing, template_config, klaviyo_images)
    
    # Save HTML
    html_file = f"{briefing['briefing_id']}_v2.html"
    html_path = os.path.join(os.path.dirname(BRIEFING_DIR), html_file)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'     💾 {html_file}')
    
    # 6. Publish to Klaviyo
    if not dry_run:
        result = publish_to_klaviyo(briefing, content, html)
        if result.get('url'):
            print(f'  🔗 {result["url"]}')
        
        # Update briefing
        briefing['status'] = 'done'
        briefing['output'] = {
            'subject_line': content['subject_line'],
            'preview_text': content['preview_text'],
            'email_body_html': html[:500] + '...',
            'klaviyo_template_id': result.get('template_id', ''),
            'klaviyo_campaign_id': result.get('campaign_id', ''),
            'klaviyo_url': result.get('url', ''),
            'email_type': email_type,
        }
        save_briefing(briefing)
    else:
        print('  🏜️  DRY RUN — Kein Klaviyo Upload')
    
    return True

def publish_to_klaviyo(briefing: Dict, content: Dict, html: str) -> Dict:
    """Publish to Klaviyo"""
    api_key = briefing['klaviyo']['api_key']
    list_id = briefing['klaviyo']['list_id']
    name = f"{briefing['client']['name']} | {briefing['topic']['name']} | {briefing['topic']['date']}"
    
    if not list_id:
        print('  ⚠️  Kein List ID')
        return {'error': 'no_list_id'}
    
    # Create Template
    print('  📨 Klaviyo: Template...')
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
        return {'error': 'template_failed'}
    
    template_id = template_result['data']['id']
    print(f'     ✅ {template_id}')
    
    # Create Campaign
    send_datetime = f"{briefing['topic']['date']}T09:00:00+01:00"
    website = briefing['client']['website']
    from_email = f'hello@{website.replace("https://","").split("/")[0]}' if website else 'hello@example.com'
    
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
                                'from_email': from_email,
                                'from_label': briefing['client']['name']
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
    
    # Assign Template
    klaviyo_api(api_key, 'POST', '/campaign-message-assign-template', {
        'data': {
            'type': 'campaign-message',
            'id': message_id,
            'relationships': {'template': {'data': {'type': 'template', 'id': template_id}}}
        }
    })
    print(f'     ✅ Verknüpft!')
    
    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_id,
        'url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--briefing', type=str, required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    
    process_briefing_advanced(args.briefing, args.dry_run)

if __name__ == '__main__':
    main()
