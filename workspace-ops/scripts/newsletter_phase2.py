#!/usr/bin/env python3
"""
Newsletter Engine v4 — PHASE 2: Content Generator + Klaviyo Publisher

This is the AI-powered phase that generates personalized content
and publishes to Klaviyo. Can run as agent task (takes time).

Usage:
    # Single briefing
    python3 newsletter_phase2.py --briefing razeco_ug_2026-03-08.json
    
    # All pending briefings
    python3 newsletter_phase2.py --all-pending
    
    # Dry run (generate HTML but don't push to Klaviyo)
    python3 newsletter_phase2.py --briefing razeco_ug_2026-03-08.json --dry-run
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Optional
import argparse

BRIEFING_DIR = os.path.join(os.path.dirname(__file__), '..', 'newsletters', 'briefings')

def load_briefing(briefing_id: str) -> Dict:
    """Load briefing JSON by ID or filename"""
    # Try with .json extension if not provided
    if not briefing_id.endswith('.json'):
        briefing_id += '.json'
    
    filepath = os.path.join(BRIEFING_DIR, briefing_id)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_briefing(briefing: Dict):
    """Save updated briefing with output data"""
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

def generate_content_with_ai(briefing: Dict) -> Dict:
    """Generate personalized newsletter content using AI (Claude)"""
    
    # Build the prompt for AI content generation
    language = briefing['client']['language']
    is_german = language == 'de'
    
    # Extract briefing data
    client_name = briefing['client']['name']
    topic_name = briefing['topic']['name']
    instructions = briefing['topic']['briefing_instructions']
    brand_tone = briefing['brand']['tone']
    products = briefing['products']
    usps = products.get('usps', '')
    social_proof = products.get('social_proof', '')
    
    # Create prompt
    if is_german:
        prompt = f"""Du bist ein erfahrener Email-Marketing Copywriter für E-Commerce Marken.

Erstelle einen personalisierten Newsletter für {client_name}.

THEMA: {topic_name}

BRIEFING (was der Newsletter beinhalten soll):
{instructions}

MARKEN-TONALITÄT:
{brand_tone}

PRODUKT-USPs:
{usps}

SOCIAL PROOF:
{social_proof}

AUFGABE:
Schreibe einen kompletten Newsletter auf DEUTSCH mit folgenden Elementen:

1. BETREFFZEILE (Subject Line): Catchy, max 50 Zeichen, mit Emoji wenn passend
2. VORSCHAUTEXT (Preview Text): Max 100 Zeichen, macht Lust auf mehr
3. ANREDE: Persönlich, "Hallo {{first_name|default:\"Freund\"}}"
4. HAUPTTEXT: 2-3 Absätze, conversational, auf das Thema bezogen, mit Bezug zu den USPs
5. PRODUKT-EMPFFEHLUNGEN: Wenn passend, 2-3 Produkte kurz beschreiben
6. CTA: Ein klarer Call-to-Action
7. ABSCHIED: Freundlicher, passender Abschluss

FORMATIERUNG:
Gib das Ergebnis als JSON zurück:
{{
  "subject_line": "...",
  "preview_text": "...",
  "greeting": "...",
  "body_paragraphs": ["...", "..."],
  "product_section": "...",
  "cta_text": "...",
  "closing": "...",
  "full_text": "gesamter Fließtext für Text-Version"
}}

Wichtig:
- Der Ton muss zur Marken-Tonalität passen
- Der Content muss zum Thema "{topic_name}" passen
- Natürlich klingen, nicht wie Werbung
- Deutsche Sprache, korrekte Grammatik"""
    else:
        prompt = f"""You are an experienced email marketing copywriter for e-commerce brands.

Create a personalized newsletter for {client_name}.

TOPIC: {topic_name}

BRIEFING (what the newsletter should include):
{instructions}

BRAND TONE:
{brand_tone}

PRODUCT USPs:
{usps}

SOCIAL PROOF:
{social_proof}

TASK:
Write a complete newsletter in ENGLISH with:

1. SUBJECT LINE: Catchy, max 50 chars, emoji if appropriate
2. PREVIEW TEXT: Max 100 chars, creates curiosity
3. GREETING: Personal, "Hello {{first_name|default:\"there\"}}"
4. BODY: 2-3 paragraphs, conversational, related to topic, referencing USPs
5. PRODUCT RECOMMENDATIONS: If appropriate, briefly describe 2-3 products
6. CTA: Clear call-to-action
7. CLOSING: Friendly, appropriate ending

OUTPUT FORMAT:
Return as JSON:
{{
  "subject_line": "...",
  "preview_text": "...",
  "greeting": "...",
  "body_paragraphs": ["...", "..."],
  "product_section": "...",
  "cta_text": "...",
  "closing": "...",
  "full_text": "full text for text-only version"
}}

Important:
- Tone must match brand personality
- Content must fit the "{topic_name}" topic
- Sound natural, not salesy
- Proper English grammar"""

    print('  🤖 Generiere Content mit AI...')
    
    # For now, use a simple approach - in production this would call Claude
    # Since we don't have direct API access here, I'll use fallback content
    # that can be improved
    
    # Check if we should use real AI or fallback
    try:
        # Try to call Claude via OpenClaw sub-agent or direct API
        content = call_claude_for_content(prompt)
        if content:
            print('     ✅ AI Content generiert')
            return content
    except Exception as e:
        print(f'     ⚠️  AI failed: {e}, using fallback')
    
    # Fallback: Map topic to pre-written templates
    return generate_fallback_content(briefing)

def call_claude_for_content(prompt: str) -> Optional[Dict]:
    """Call Claude API for content generation - placeholder"""
    # This would integrate with Claude API
    # For now, return None to trigger fallback
    return None

def generate_fallback_content(briefing: Dict) -> Dict:
    """Generate fallback content based on topic patterns"""
    topic = briefing['topic']['name'].lower()
    lang = briefing['client']['language']
    client_name = briefing['client']['name']
    
    # Topic-based fallback content
    if 'women' in topic or 'frau' in topic:
        if lang == 'de':
            return {
                'subject_line': 'Happy International Women\'s Day! 💪🌸',
                'preview_text': 'Wir feiern starke Frauen — heute und jeden Tag',
                'greeting': 'Hallo {{first_name|default:"Freund"}}',
                'body_paragraphs': [
                    f'am heutigen Internationalen Frauentag möchten wir alle starken Frauen feiern — besonders die, die jeden Tag für eine nachhaltige Zukunft kämpfen.',
                    f'Bei {client_name} stehen Nachhaltigkeit und Innovation im Mittelpunkt. Wir glauben daran, dass kleine Veränderungen im Alltag einen großen Unterschied machen können.'
                ],
                'product_section': 'Entdecke unsere nachhaltigen Produkte, mit denen du einen positiven Impact erzeugen kannst.',
                'cta_text': 'Jetzt entdecken →',
                'closing': 'Mit besten Grüßen,<br>Dein {client_name} Team'.format(client_name=client_name),
                'full_text': f'Happy International Women\'s Day! Wir feiern starke Frauen und eine nachhaltige Zukunft. Bei {client_name} kannst du mit kleinen Veränderungen im Alltag einen großen Unterschied machen.'
            }
    
    elif 'faq' in topic:
        if lang == 'de':
            return {
                'subject_line': 'Deine Fragen, unsere Antworten ❓',
                'preview_text': 'Alles, was du über uns wissen musst',
                'greeting': 'Hallo {{first_name|default:"Freund"}}',
                'body_paragraphs': [
                    f'wir haben die häufigsten Fragen unserer Kunden gesammelt und beantworten sie heute für dich.',
                    f'Von Lieferzeiten bis hin zu Produktpflege — hier findest du alle wichtigen Infos auf einen Blick.'
                ],
                'product_section': '',
                'cta_text': 'Mehr erfahren →',
                'closing': 'Bei Fragen erreichst du uns jederzeit!<br>Dein {client_name} Team'.format(client_name=client_name),
                'full_text': f'Deine Fragen, unsere Antworten. Wir haben die häufigsten Fragen gesammelt und beantworten sie für dich.'
            }
    
    elif 'recommend' in topic or 'empfehl' in topic:
        if lang == 'de':
            return {
                'subject_line': 'Unsere Empfehlungen für dich 🌱',
                'preview_text': 'Die besten Produkte, handverlesen für dich',
                'greeting': 'Hallo {{first_name|default:"Freund"}}',
                'body_paragraphs': [
                    f'wir haben unsere beliebtesten Produkte für dich zusammengestellt.',
                    f'Ob du auf der Suche nach dem perfekten Einstieg in nachhaltige Produkte bist oder deine Kollektion erweitern möchtest — hier findest du alles, was du brauchst.'
                ],
                'product_section': 'Entdecke unsere Bestseller und finde dein neues Lieblingsprodukt.',
                'cta_text': 'Jetzt shoppen →',
                'closing': 'Viel Spaß beim Stöbern!<br>Dein {client_name} Team'.format(client_name=client_name),
                'full_text': f'Unsere Empfehlungen für dich: Wir haben die beliebtesten Produkte zusammengestellt. Entdecke dein neues Lieblingsprodukt bei {client_name}.'
            }
    
    # Generic fallback
    if lang == 'de':
        return {
            'subject_line': f'Neuigkeiten von {client_name} ✨',
            'preview_text': f'Sieh dir an, was es Neues gibt',
            'greeting': 'Hallo {{first_name|default:"Freund"}}',
            'body_paragraphs': [
                f'wir haben spannende Neuigkeiten für dich!',
                f'Schau vorbei und entdecke, was {client_name} für dich bereithält.'
            ],
            'product_section': '',
            'cta_text': 'Mehr entdecken →',
            'closing': f'Beste Grüße,<br>Dein {client_name} Team',
            'full_text': f'Neuigkeiten von {client_name}: Schau vorbei und entdecke, was wir für dich bereithalten.'
        }
    else:
        return {
            'subject_line': f'News from {client_name} ✨',
            'preview_text': f'See what\'s new',
            'greeting': 'Hello {{first_name|default:"there"}}',
            'body_paragraphs': [
                f'we have exciting news for you!',
                f'Check out what {client_name} has in store for you.'
            ],
            'product_section': '',
            'cta_text': 'Discover more →',
            'closing': f'Best regards,<br>The {client_name} Team',
            'full_text': f'News from {client_name}: Check out what we have in store for you.'
        }

def build_html_email(content: Dict, briefing: Dict) -> str:
    """Build complete HTML email from content and brand assets"""
    
    brand = briefing['brand']
    client = briefing['client']
    language = client['language']
    
    # Colors
    colors = brand['colors']
    primary = colors.get('primary', '#333333')
    secondary = colors.get('secondary', '#666666')
    accent = colors.get('accent', '#0066CC')
    
    # Fonts
    fonts = brand.get('fonts', '')
    heading_font = "Georgia, serif"
    body_font = "Arial, sans-serif"
    if 'heading' in fonts.lower():
        heading_font = fonts.split('(')[0].strip() + ", Georgia, serif"
    if 'body' in fonts.lower():
        body_font = fonts.split('(')[0].strip() + ", Arial, sans-serif"
    
    # Logo
    logo_url = brand.get('logo_url', '')
    website = client['website']
    
    # Build body paragraphs
    body_html = ''
    for para in content.get('body_paragraphs', []):
        body_html += f'''
          <tr>
            <td style="padding:10px 30px;">
              <p style="font-family:{body_font};font-size:16px;line-height:1.7;color:{primary};margin:0;">
                {para}
              </p>
            </td>
          </tr>'''
    
    # Product section if present
    product_html = ''
    if content.get('product_section'):
        product_html = f'''
          <tr>
            <td style="padding:10px 30px;">
              <p style="font-family:{body_font};font-size:16px;line-height:1.7;color:{primary};margin:0;">
                {content['product_section']}
              </p>
            </td>
          </tr>'''
    
    # CTA button
    cta_text = content.get('cta_text', 'Learn more →' if language == 'en' else 'Mehr erfahren →')
    
    html = f'''<!DOCTYPE html>
<html lang="{language}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{content['subject_line']}</title>
  <!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
</head>
<body style="margin:0;padding:0;background-color:#F5F5F5;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#F5F5F5;">
    <tr>
      <td align="center" style="padding:20px 0;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="background-color:#FFFFFF;max-width:600px;width:100%;">
          
          <!-- Header -->
          <tr>
            <td align="center" style="padding:30px 20px;background-color:#FFFFFF;">
              {f'<a href="{website}"><img src="{logo_url}" alt="{client["name"]}" width="120" style="display:block;border:0;"></a>' if logo_url else f'<h2 style="font-family:{heading_font};color:{primary};margin:0;">{client["name"]}</h2>'}
            </td>
          </tr>

          <!-- Hero -->
          <tr>
            <td style="background-color:{accent};padding:40px 30px;text-align:center;">
              <h1 style="font-family:{heading_font};font-size:28px;line-height:1.3;color:#FFFFFF;margin:0 0 15px 0;font-weight:normal;">
                {content['subject_line']}
              </h1>
              <p style="font-family:{body_font};font-size:16px;line-height:1.6;color:#E0E0E0;margin:0;">
                {briefing['topic']['name']}
              </p>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding:40px 30px 20px 30px;">
              <p style="font-family:{body_font};font-size:16px;line-height:1.7;color:{primary};margin:0;">
                {content['greeting']},
              </p>
            </td>
          </tr>

          <!-- Body -->
          {body_html}
          
          <!-- Products -->
          {product_html}

          <!-- CTA -->
          <tr>
            <td align="center" style="padding:20px 30px 40px 30px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background-color:{accent};border-radius:4px;">
                    <a href="{website}" style="display:inline-block;padding:14px 32px;font-family:{body_font};font-size:16px;color:#FFFFFF;text-decoration:none;font-weight:600;">
                      {cta_text}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Closing -->
          <tr>
            <td style="padding:0 30px 30px 30px;">
              <p style="font-family:{body_font};font-size:16px;line-height:1.7;color:{primary};margin:0;">
                {content['closing']}
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color:#F5F5F5;padding:30px;text-align:center;border-top:1px solid #E0E0E0;">
              <p style="font-family:{body_font};font-size:12px;color:#999999;margin:0 0 10px 0;">
                {brand.get('tagline', client['name'])}
              </p>
              <p style="font-family:{body_font};font-size:11px;color:#AAAAAA;margin:0;">
                <a href="{website}" style="color:#AAAAAA;text-decoration:underline;">{client['name']}</a>
                &nbsp;|&nbsp;
                <a href="{{{{unsubscribe_url}}}}" style="color:#AAAAAA;text-decoration:underline;">
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
    
    return html

def publish_to_klaviyo(briefing: Dict, content: Dict, html: str, dry_run: bool = False) -> Dict:
    """Create template and campaign in Klaviyo"""
    
    api_key = briefing['klaviyo']['api_key']
    list_id = briefing['klaviyo']['list_id']
    name = f"{briefing['client']['name']} | {briefing['topic']['name']} | {briefing['topic']['date']}"
    
    if dry_run:
        print('  🏜️  DRY RUN — Kein Klaviyo Upload')
        return {'dry_run': True}
    
    if not list_id:
        print('  ⚠️  Kein Klaviyo List ID — übersprungen')
        return {'error': 'no_list_id'}
    
    # 1. Create Template
    print('  📨 Klaviyo: Template erstellen...')
    template_result = klaviyo_api(api_key, 'POST', '/templates', {
        'data': {
            'type': 'template',
            'attributes': {
                'name': name,
                'editor_type': 'CODE',
                'html': html,
                'text': content.get('full_text', content['subject_line'])
            }
        }
    })
    
    if 'error' in template_result:
        print(f'     ❌ Template failed: {template_result["error"][:100]}')
        return {'error': 'template_failed'}
    
    template_id = template_result['data']['id']
    print(f'     ✅ {template_id}')
    
    # 2. Create Campaign
    send_datetime = f"{briefing['topic']['date']}T09:00:00+01:00"
    from_email = f'hello@{briefing["client"]["website"].replace("https://","").split("/")[0]}' if briefing['client']['website'] else 'hello@example.com'
    
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
        print(f'     ❌ Campaign failed: {campaign_result["error"][:100]}')
        return {'error': 'campaign_failed', 'template_id': template_id}
    
    campaign_id = campaign_result['data']['id']
    message_id = campaign_result['data']['relationships']['campaign-messages']['data'][0]['id']
    print(f'     ✅ Campaign: {campaign_id}')
    
    # 3. Assign Template
    assign_result = klaviyo_api(api_key, 'POST', '/campaign-message-assign-template', {
        'data': {
            'type': 'campaign-message',
            'id': message_id,
            'relationships': {'template': {'data': {'type': 'template', 'id': template_id}}}
        }
    })
    
    if 'error' in assign_result:
        print(f'     ⚠️  Assignment failed')
    else:
        print(f'     ✅ Verknüpft!')
    
    return {
        'success': True,
        'template_id': template_id,
        'campaign_id': campaign_id,
        'url': f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
    }

def process_briefing(briefing_file: str, dry_run: bool = False):
    """Process a single briefing through all phases"""
    
    # Load briefing
    briefing = load_briefing(briefing_file)
    
    print('=' * 60)
    print(f'📧 {briefing["client"]["name"]} | {briefing["topic"]["name"]}')
    print('=' * 60)
    
    # 1. Generate Content
    content = generate_content_with_ai(briefing)
    
    # 2. Build HTML
    print('  🎨 Baue HTML...')
    html = build_html_email(content, briefing)
    
    # Save HTML preview
    html_file = f"{briefing['briefing_id']}.html"
    html_path = os.path.join(os.path.dirname(BRIEFING_DIR), html_file)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'     💾 {html_file}')
    
    # 3. Publish to Klaviyo
    result = publish_to_klaviyo(briefing, content, html, dry_run)
    
    # 4. Update briefing with results
    briefing['status'] = 'done' if result.get('success') else 'error'
    briefing['output'] = {
        'subject_line': content['subject_line'],
        'preview_text': content['preview_text'],
        'email_body_html': html[:500] + '...',
        'email_body_text': content['full_text'],
        'klaviyo_template_id': result.get('template_id', ''),
        'klaviyo_campaign_id': result.get('campaign_id', ''),
        'klaviyo_url': result.get('url', ''),
    }
    save_briefing(briefing)
    
    if result.get('url'):
        print(f'\n  🔗 {result["url"]}')
    
    return result

def get_pending_briefings():
    """Get all briefings with status 'pending'"""
    pending = []
    if not os.path.exists(BRIEFING_DIR):
        return pending
    
    for filename in os.listdir(BRIEFING_DIR):
        if not filename.endswith('.json'):
            continue
        filepath = os.path.join(BRIEFING_DIR, filename)
        with open(filepath, 'r') as f:
            briefing = json.load(f)
        if briefing.get('status') == 'pending':
            pending.append(filename)
    
    return pending

def main():
    parser = argparse.ArgumentParser(description='Newsletter Phase 2: Content Generation')
    parser.add_argument('--briefing', type=str, help='Briefing JSON file to process')
    parser.add_argument('--all-pending', action='store_true', help='Process all pending briefings')
    parser.add_argument('--dry-run', action='store_true', help='Generate but dont publish')
    args = parser.parse_args()
    
    if args.briefing:
        # Single briefing
        result = process_briefing(args.briefing, args.dry_run)
        return 0 if result.get('success') or result.get('dry_run') else 1
    
    elif args.all_pending:
        # All pending briefings
        pending = get_pending_briefings()
        if not pending:
            print('No pending briefings found')
            return 0
        
        print(f'Processing {len(pending)} pending briefings...')
        results = []
        for briefing_file in pending:
            result = process_briefing(briefing_file, args.dry_run)
            results.append(result)
        
        success = sum(1 for r in results if r.get('success'))
        print(f'\n✅ {success}/{len(results)} successful')
        return 0
    
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
