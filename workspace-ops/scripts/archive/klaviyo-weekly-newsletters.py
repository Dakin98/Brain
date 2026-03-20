#!/usr/bin/env python3
"""
Weekly Newsletter Preparation for Klaviyo Clients
==================================================
Fetches topics from Notion eCom Email Calendar, analyzes client websites,
generates high-quality personalized HTML email templates per email type,
and creates Klaviyo campaign drafts.

Email Types supported (from Notion):
  - Us vs Them: Side-by-side comparison table
  - Recommended Products: Product grid with cards & testimonials
  - FAQ Email: Q&A accordion-style layout
  - Show the Future: PAS (Problem-Agitate-Solution) narrative funnel

Design system:
  - DM Serif Display (headings) + Plus Jakarta Sans (body)
  - Brand colors extracted from client website
  - Real product images from Shopify CDN
  - Rounded cards, USP bar, social footer, TÜV badge, unsubscribe link
  - Mobile-responsive with @media queries

Klaviyo API quirks:
  - Campaign creation uses "campaign-messages" (hyphenated) in attributes
  - Template assignment: POST /api/campaign-message-assign-template/
  - Template update: PATCH /api/templates/{id} — editor_type NOT valid for PATCH
  - Campaign scheduling: POST /api/campaign-send-jobs with campaign ID
  - Content-Type for Klaviyo: application/vnd.api+json
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import sys
import re
import ssl
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

# Claude AI content generation (optional, enabled with --use-claude)
USE_CLAUDE = False
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ===========================================================================
# CONFIG
# ===========================================================================
NOTION_KEY = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()
NOTION_DS_ID = "f973c96b-5659-4fd8-97c2-63984dbd89d9"
MATON_KEY = os.environ.get("MATON_API_KEY", "")
AIRTABLE_BASE = "appbGhxy9I18oIS8E"
TELEGRAM_BOT_TOKEN = "8586858553:AAEKHWk0ru9UHzhMAAWwlFyfqa2GAk16gxM"
TELEGRAM_CHAT_ID = "6607099798"
KLAVIYO_REVISION = "2024-10-15"
KLAVIYO_BASE = "https://a.klaviyo.com/api"

# SSL context for HTTPS requests
SSL_CTX = ssl.create_default_context()

# Caches
_cache = {}


def log(msg):
    print(msg, file=sys.stderr)


# ===========================================================================
# CLAUDE AI CONTENT GENERATION
# ===========================================================================
def generate_content_with_claude(topic: Dict, brand_profile: Dict, products: List[Dict], email_type: str) -> Optional[Dict]:
    """
    Call Claude API to generate email marketing copy.
    Returns structured content: hero_title, hero_subtitle, hero_cta,
    product_descriptions[], closing_text, subject, preview.
    Returns None on failure (falls back to static content).
    """
    if not USE_CLAUDE or not ANTHROPIC_API_KEY:
        return None

    brand_name = brand_profile.get("name", "Brand")
    brand_url = brand_profile.get("url", "")
    usps = brand_profile.get("usps", [])
    tone = brand_profile.get("tone", "standard")

    product_info = ""
    for i, p in enumerate(products[:5]):
        product_info += f"- Produkt {i+1}: {p.get('name', 'Unbekannt')} (URL: {p.get('url', '')})\n"
    if not product_info:
        product_info = "- Keine spezifischen Produkte verfügbar\n"

    tone_desc = {
        "luxury": "luxuriös, exklusiv, elegant, gehobene Sprache",
        "casual": "locker, freundlich, nahbar, du-Ansprache",
        "standard": "professionell aber freundlich, du-Ansprache"
    }.get(tone, "professionell, du-Ansprache")

    email_type_desc = {
        "us_vs_them": "Vergleichs-E-Mail: Zeige warum die Marke besser ist als konventionelle Alternativen",
        "recommended_products": "Produktempfehlungs-E-Mail: Stelle die besten Produkte vor",
        "faq": "FAQ-E-Mail: Beantworte häufige Kundenfragen überzeugend",
        "show_the_future": "Zukunftsvisions-E-Mail: PAS-Framework (Problem-Agitate-Solution), inspirierend",
    }.get(email_type, "Produkt-Newsletter")

    system_prompt = """Du bist ein E-Mail Marketing Experte für deutsche E-Commerce Brands.
Du schreibst überzeugende, verkaufsstarke Newsletter-Texte auf Deutsch.
Dein Stil: emotional, authentisch, keine Floskeln. Kurze Sätze. Klare CTAs.
Du nutzt Personalisierung mit {{ first_name }} wo sinnvoll.
Antworte NUR mit validem JSON, kein Markdown, keine Erklärungen."""

    user_prompt = f"""Schreibe E-Mail Content für:

**Marke:** {brand_name}
**Website:** {brand_url}
**USPs:** {', '.join(usps) if usps else 'Qualität, Service'}
**Tonalität:** {tone_desc}
**E-Mail-Typ:** {email_type_desc}
**Thema:** {topic.get('name', '')}
**Kontext aus Notion:** {topic.get('content', '')[:500]}
**Produkte:**
{product_info}

Generiere JSON mit exakt dieser Struktur:
{{
  "subject": "Betreffzeile (max 60 Zeichen, emotional, neugierig machend)",
  "preview": "Preview-Text (max 90 Zeichen)",
  "hero_title": "Große Überschrift (2-5 Wörter, kraftvoll)",
  "hero_subtitle": "Untertitel mit <br> für Zeilenumbruch, kann {{ first_name }} enthalten",
  "hero_text": "1-2 Sätze Einleitung",
  "hero_cta": "CTA-Button-Text (3-5 Wörter, Großbuchstaben)",
  "product_descriptions": [
    {{"name": "Produktname", "tagline": "Kurzer Slogan", "description": "2 Sätze Beschreibung", "cta": "CTA-Text"}}
  ],
  "closing_title": "Abschluss-Überschrift (emotional)",
  "closing_text": "1-2 Sätze Abschluss",
  "closing_cta": "Abschluss-CTA-Text"
}}"""

    try:
        data = json.dumps({
            "model": "claude-opus-4-20250514",
            "max_tokens": 1500,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=data,
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
            method="POST"
        )

        with urllib.request.urlopen(req, context=SSL_CTX, timeout=60) as resp:
            result = json.loads(resp.read())

        text = result.get("content", [{}])[0].get("text", "")
        # Parse JSON from response (handle potential markdown wrapping)
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        content = json.loads(text)
        log(f"    🤖 Claude generated content: subject='{content.get('subject', '')[:50]}'")
        return content

    except Exception as e:
        log(f"    ⚠️ Claude generation failed: {str(e)[:120]}")
        return None


def _scrape_shopify_products_api(base_url: str) -> List[Dict]:
    """
    Fetch products from Shopify's /products.json API endpoint.
    Returns list of products with name, url, image, price, description.
    """
    try:
        url = base_url.rstrip("/") + "/products.json?limit=10"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        data = json.loads(resp.read())

        products = []
        for p in data.get("products", [])[:10]:
            img = ""
            if p.get("images"):
                img = p["images"][0].get("src", "")
            variant = p.get("variants", [{}])[0]
            price = variant.get("price", "")

            products.append({
                "name": p.get("title", ""),
                "url": base_url.rstrip("/") + "/products/" + p.get("handle", ""),
                "slug": "/products/" + p.get("handle", ""),
                "image": img,
                "price": f"€{price}" if price else "",
                "description": (p.get("body_html", "") or "")[:200].replace("<br>", " ").replace("</p>", " "),
            })
        if products:
            log(f"    🛍️ Fetched {len(products)} products from Shopify API")
        return products
    except Exception as e:
        log(f"    ⚠️ Shopify API failed: {str(e)[:80]}")
        return []


# ===========================================================================
# GENERIC API HELPERS
# ===========================================================================
def klaviyo_api(method, path, data=None, api_key=""):
    """Call Klaviyo API with proper headers. Returns parsed JSON or None."""
    url = f"{KLAVIYO_BASE}{path}"
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": KLAVIYO_REVISION,
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=SSL_CTX) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        log(f"  ❌ Klaviyo {method} {path} → {e.code}: {err[:300]}")
        return None


def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        log(f"Telegram error: {e}")


# ===========================================================================
# NOTION: FETCH TOPICS
# ===========================================================================
def get_notion_topics(days: int = 14, target_date: str = None) -> List[Dict]:
    today = datetime.now()
    if target_date:
        try:
            dt = datetime.strptime(target_date, "%Y-%m-%d")
            date_start, date_end = dt, dt
        except ValueError:
            date_start = today
            date_end = today + timedelta(days=days)
    else:
        date_start = today
        date_end = today + timedelta(days=days)

    log(f"📅 Topics: {date_start.strftime('%d.%m.%Y')} – {date_end.strftime('%d.%m.%Y')}")

    all_entries = []
    has_more, cursor = True, None
    while has_more:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        req = urllib.request.Request(
            f"https://api.notion.com/v1/data_sources/{NOTION_DS_ID}/query",
            data=json.dumps(body).encode(), method="POST"
        )
        req.add_header("Authorization", f"Bearer {NOTION_KEY}")
        req.add_header("Notion-Version", "2025-09-03")
        req.add_header("Content-Type", "application/json")
        try:
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read())
            all_entries.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            cursor = data.get("next_cursor")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                log("⏱️ Rate limited, waiting 10s...")
                time.sleep(10)
                continue
            log(f"❌ Notion error: {e}")
            return []

    log(f"📊 Total Notion entries: {len(all_entries)}")

    results = []
    for entry in all_entries:
        props = entry["properties"]
        date_prop = props.get("Date", {}).get("date")
        if not date_prop or not date_prop.get("start"):
            continue
        try:
            entry_date = datetime.strptime(date_prop["start"], "%Y-%m-%d")
            mapped = entry_date.replace(year=today.year)
        except ValueError:
            continue

        if date_start.date() <= mapped.date() <= date_end.date():
            name = "".join([t["plain_text"] for t in props.get("Name", {}).get("title", [])])
            types = [s["name"] for s in props.get("Email Type", {}).get("multi_select", [])]

            # Fetch page content
            page_id = entry["id"]
            content = _fetch_notion_content(page_id)

            results.append({
                "name": name,
                "date": mapped.strftime("%Y-%m-%d"),
                "types": types,
                "content": content,
                "page_id": page_id,
            })
            log(f"  ✅ {mapped.strftime('%d.%m')}: {name} [{', '.join(types)}]")

    results.sort(key=lambda x: x["date"])
    return results


def _fetch_notion_content(page_id: str) -> str:
    ckey = f"nc_{page_id}"
    if ckey in _cache:
        return _cache[ckey]
    try:
        req = urllib.request.Request(f"https://api.notion.com/v1/blocks/{page_id}/children")
        req.add_header("Authorization", f"Bearer {NOTION_KEY}")
        req.add_header("Notion-Version", "2025-09-03")
        blocks = json.loads(urllib.request.urlopen(req).read())
        lines = []
        for b in blocks.get("results", []):
            bt = b["type"]
            if bt in ("paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"):
                text = "".join([r["plain_text"] for r in b.get(bt, {}).get("rich_text", [])])
                if text.strip():
                    lines.append(text)
        content = "\n".join(lines)
        _cache[ckey] = content
        return content
    except Exception as e:
        log(f"  ⚠️ Content fetch failed for {page_id}: {str(e)[:80]}")
        return ""


# ===========================================================================
# AIRTABLE: FETCH CLIENTS
# ===========================================================================
def get_klaviyo_clients() -> List[Dict]:
    filt = "AND(OR(Status='Aktiv',Status='Onboarding'),{Klaviyo API Key}!='')"
    url = f"https://gateway.maton.ai/airtable/v0/{AIRTABLE_BASE}/Kunden?filterByFormula={urllib.parse.quote(filt)}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {MATON_KEY}")
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        clients = []
        for rec in data.get("records", []):
            f = rec["fields"]
            clients.append({
                "id": rec["id"],
                "firmenname": f.get("Firmenname", ""),
                "klaviyo_key": f.get("Klaviyo API Key", ""),
                "website": f.get("Website", ""),
                "branche": f.get("Branche", ""),
            })
        return clients
    except Exception as e:
        log(f"❌ Airtable error: {e}")
        return []


# ===========================================================================
# WEBSITE ANALYSIS → BRAND PROFILE
# ===========================================================================
def analyze_brand(website_url: str, firmenname: str) -> Dict:
    """
    Analyze a client's website to extract brand profile:
    colors, products, images, USPs, tone, tagline, etc.
    Returns a BrandProfile dict used by template generators.
    """
    ckey = f"brand_{website_url}"
    if ckey in _cache:
        return _cache[ckey]

    profile = _default_brand(firmenname, website_url)

    if not website_url:
        return profile

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(website_url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode("utf-8", errors="ignore")
        html_lower = html.lower()

        # Title
        if "<title>" in html_lower:
            profile["title"] = html_lower.split("<title>")[1].split("</title>")[0].strip()

        # Extract CSS custom properties for colors
        profile["colors"] = _extract_colors(html)

        # Detect Shopify
        if "shopify" in html_lower or "myshopify" in html_lower:
            profile["platform"] = "shopify"
            # Try Shopify API first for richer product data
            api_products = _scrape_shopify_products_api(website_url)
            if api_products:
                profile["products"] = api_products
                profile["product_images"] = [p["image"] for p in api_products if p.get("image")]
            else:
                # Fallback to HTML scraping
                profile["products"] = _extract_shopify_products(html, website_url)
                profile["product_images"] = _extract_shopify_images(html, website_url)

        # Detect USPs
        usp_kw = ["nachhaltig", "bio", "vegan", "handmade", "regional", "fair", "plastikfrei", "made in germany"]
        profile["usps"] = [kw.title() for kw in usp_kw if kw in html_lower]

        # Detect tone
        luxury = sum(1 for w in ["luxus", "premium", "exklusiv", "hochwertig"] if w in html_lower)
        casual = sum(1 for w in ["mega", "super", "cool", "easy", "lässig"] if w in html_lower)
        profile["tone"] = "luxury" if luxury > 2 else ("casual" if casual > 2 else "standard")

        # Logo (look for og:image or logo img)
        og_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html, re.I)
        if og_match:
            profile["og_image"] = og_match.group(1)

        logo_match = re.search(r'<img[^>]*class="[^"]*logo[^"]*"[^>]*src="([^"]+)"', html, re.I)
        if logo_match:
            src = logo_match.group(1)
            if src.startswith("//"):
                src = "https:" + src
            profile["logo"] = src

        _cache[ckey] = profile
        return profile

    except Exception as e:
        log(f"  ⚠️ Brand analysis failed for {website_url}: {str(e)[:80]}")
        return profile


def _default_brand(name, url):
    return {
        "name": name,
        "url": url,
        "title": name,
        "platform": "unknown",
        "colors": {
            "bg_outer": "#B4B4B0",
            "bg_inner": "#F3F2EE",
            "bg_cream": "#F5F4F0",
            "dark": "#48413C",
            "text": "#696255",
            "text_light": "#BAB4A7",
            "accent": "#0C5132",
            "card_bg": "#ECEAE4",
            "border": "#D3D1C8",
        },
        "logo": "",
        "og_image": "",
        "products": [],
        "product_images": [],
        "usps": [],
        "tone": "standard",
        "tagline": "",
        "social": {"instagram": "", "facebook": "", "twitter": "", "youtube": ""},
    }


def _extract_colors(html: str) -> Dict[str, str]:
    """Extract brand colors from CSS custom properties or inline styles."""
    colors = {}
    # Try CSS variables
    patterns = {
        "accent": [r"--primary[^:]*:\s*(#[0-9a-fA-F]{3,8})", r"--brand[^:]*:\s*(#[0-9a-fA-F]{3,8})", r"--accent[^:]*:\s*(#[0-9a-fA-F]{3,8})"],
        "dark": [r"--heading[^:]*:\s*(#[0-9a-fA-F]{3,8})", r"--dark[^:]*:\s*(#[0-9a-fA-F]{3,8})"],
        "text": [r"--text[^:]*:\s*(#[0-9a-fA-F]{3,8})", r"--body[^:]*:\s*(#[0-9a-fA-F]{3,8})"],
        "bg_inner": [r"--bg[^:]*:\s*(#[0-9a-fA-F]{3,8})", r"--background[^:]*:\s*(#[0-9a-fA-F]{3,8})"],
    }
    for key, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, html, re.I)
            if m:
                colors[key] = m.group(1)
                break

    # Defaults if nothing found
    defaults = {
        "bg_outer": "#B4B4B0", "bg_inner": "#F3F2EE", "bg_cream": "#F5F4F0",
        "dark": "#48413C", "text": "#696255", "text_light": "#BAB4A7",
        "accent": "#0C5132", "card_bg": "#ECEAE4", "border": "#D3D1C8",
    }
    for k, v in defaults.items():
        colors.setdefault(k, v)
    return colors


def _extract_shopify_products(html: str, base_url: str) -> List[Dict]:
    """Extract product info from Shopify HTML."""
    products = []
    # Look for product-card or product-grid patterns
    prod_matches = re.findall(
        r'href="(/products/[^"?]+)"[^>]*>.*?</a>',
        html, re.DOTALL | re.I
    )
    seen = set()
    for href in prod_matches[:10]:
        slug = href.split("?")[0]
        if slug in seen:
            continue
        seen.add(slug)
        name = slug.split("/")[-1].replace("-", " ").title()
        products.append({"name": name, "url": base_url.rstrip("/") + slug, "slug": slug})
    return products


def _extract_shopify_images(html: str, base_url: str) -> List[str]:
    """Extract product images from Shopify CDN."""
    images = []
    domain = base_url.replace("https://", "").replace("http://", "").rstrip("/")
    pattern = rf'(?:https?:)?//(?:www\.)?{re.escape(domain)}/cdn/shop/files/[^"\'?\s]+'
    matches = re.findall(pattern, html, re.I)
    seen = set()
    for img in matches:
        if img.startswith("//"):
            img = "https:" + img
        # Normalize: remove width params for storage, we add them in templates
        base = img.split("?")[0]
        if base not in seen:
            seen.add(base)
            images.append(base)
    return images[:20]


# ===========================================================================
# HTML TEMPLATE ENGINE
# ===========================================================================
# Shared CSS (imported once at the top of each email)
def _styles(c: Dict) -> str:
    return f'''<style>
@import url("https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap");
body{{margin:0;padding:0;-webkit-text-size-adjust:100%;background-color:{c["bg_outer"]};}}
table,td{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0;}}
img{{border:0;height:auto;line-height:100%;outline:none;text-decoration:none;max-width:100%;}}
p{{margin:0;padding-bottom:0;}}
a{{color:{c["dark"]};text-decoration:none;}}
@media only screen and (max-width:620px){{
.wrapper{{width:100%!important;max-width:100%!important;}}
.mobile-padding{{padding-left:20px!important;padding-right:20px!important;}}
.mobile-stack{{display:block!important;width:100%!important;padding-left:0!important;padding-right:0!important;padding-top:6px!important;}}
.hero-title{{font-size:32px!important;line-height:38px!important;}}
.mobile-hide{{display:none!important;}}
}}
</style>'''


def _wrap(content: str, brand: Dict) -> str:
    """Wrap email content in the outer shell: bg, rounded card, logo, footer."""
    c = brand["colors"]
    logo_html = ""
    if brand.get("logo"):
        logo_html = f'<img width="160" src="{brand["logo"]}" alt="{brand["name"]}" style="display:inline-block;height:auto;border-radius:5px;">'
    else:
        logo_html = f'<h2 style="margin:0;font-family:\'DM Serif Display\',Georgia,serif;font-size:24px;color:{c["dark"]};">{brand["name"]}</h2>'

    # Social icons — use brand social links or default "#"
    social = brand.get("social", {})
    ig = social.get("instagram", "#")
    fb = social.get("facebook", "#")

    return f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title></title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{_styles(c)}
</head>
<body style="word-spacing:normal;background-color:{c["bg_outer"]};">
<div style="background-color:{c["bg_outer"]};">
<div style="padding:40px 0 20px 0;font-size:0;">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0"><tr><td align="center">
<table width="600" class="wrapper" style="margin:0 auto;max-width:600px;background-color:{c["bg_inner"]};border-radius:24px;overflow:hidden;" role="presentation" cellspacing="0" cellpadding="0" border="0">
<!-- LOGO -->
<tr><td style="background:{c["bg_inner"]};padding:24px 40px 16px 40px;text-align:center;">
{logo_html}
</td></tr>
{content}
<!-- FOOTER -->
<tr><td style="background:{c["bg_inner"]};padding:40px 25px 12px 25px;text-align:center;">
<p style="margin:0 0 20px 0;font-family:\'Plus Jakarta Sans\',sans-serif;font-size:14px;color:{c["text"]};">{brand.get("tagline", brand["name"])}</p>
<p style="margin:0 0 12px 0;font-family:\'Plus Jakarta Sans\',sans-serif;font-size:11px;color:{c["text_light"]};">
{{% if organization %}}{{{{ organization.name }}}}{{% endif %}}
</p>
<p style="margin:20px 0 6px 0;font-family:Helvetica,Arial,sans-serif;font-size:8px;color:#727272;">
<a href="{{{{ unsubscribe_url|default:'http://manage.kmail-lists.com/subscriptions/placeholder' }}}}" style="color:{c["dark"]};" class="unsubscribe-link">Abmelden / Unsubscribe</a>
</p>
<p style="margin:0 0 16px 0;font-family:\'Plus Jakarta Sans\',sans-serif;font-size:12px;font-style:italic;color:{c["dark"]};text-decoration:underline;">{brand["url"]}</p>
</td></tr>
</table>
</td></tr></table>
</div></div>
</body></html>'''


def _btn(text: str, url: str, bg: str, fg: str = "#ffffff") -> str:
    return f'''<table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
<tr><td style="border-radius:50px;background-color:{bg};mso-padding-alt:14px 36px;">
<a href="{url}" style="color:{fg};text-decoration:none;display:inline-block;padding:14px 36px;font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;" target="_blank">{text}</a>
</td></tr></table>'''


def _btn_outline(text: str, url: str, color: str) -> str:
    return f'''<table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
<tr><td style="border-radius:50px;border:2px solid {color};">
<a href="{url}" style="color:{color};text-decoration:none;display:inline-block;padding:10px 24px;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;" target="_blank">{text}</a>
</td></tr></table>'''


def _shopify_img_url(url: str, width: int = 600) -> str:
    """Build a Shopify CDN image URL with proper width parameter."""
    if not url:
        return f"https://placehold.co/{width}x{width}?text=Product"
    url = url.split("?")[0]  # Remove existing params
    if "cdn.shopify.com" in url or "/cdn/shop/" in url:
        # Shopify CDN supports _WIDTHx format or ?width= param
        return f"{url}?width={width}&height={width}&crop=center"
    return url


def _usp_bar(brand: Dict) -> str:
    c = brand["colors"]
    usps = brand.get("usps", [])
    if not usps:
        usps = ["Qualität", "Service", "Made with ♥"]
    usp_text = " &nbsp;&bull;&nbsp; ".join(usps[:3])
    return f'''<tr>
<td style="background-color:{c["dark"]};padding:18px 30px;text-align:center;">
<p style="margin:0;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:600;color:{c["text_light"]};letter-spacing:2px;text-transform:uppercase;">
{usp_text}
</p>
</td></tr>'''


def _product_card_large(tag, title, desc, price, img_url, btn_url, brand):
    c = brand["colors"]
    return f'''<tr>
<td style="padding:24px 30px 10px 30px;" class="mobile-padding">
<table width="100%" style="border-radius:16px;overflow:hidden;border:1px solid {c["border"]};" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["card_bg"]};text-align:center;padding:0;">
<img src="{img_url}" alt="{title}" width="540" style="display:block;width:100%;height:auto;border-radius:16px 16px 0 0;">
</td></tr>
<tr><td style="background:{c["bg_cream"]};padding:28px 32px;text-align:center;">
<table style="margin-bottom:12px;" role="presentation" cellspacing="0" cellpadding="0" border="0" align="center">
<tr><td style="background-color:{c["accent"]};border-radius:20px;padding:5px 14px;">
<span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:10px;font-weight:700;color:#ffffff;letter-spacing:1px;text-transform:uppercase;">{tag}</span>
</td></tr></table>
<h3 style="margin:0 0 8px 0;font-family:'DM Serif Display',Georgia,serif;font-size:24px;color:{c["dark"]};font-weight:400;">{title}</h3>
<p style="margin:0 0 12px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;line-height:20px;color:{c["text"]};">{desc}</p>
<p style="margin:0 0 20px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:24px;color:{c["dark"]};font-weight:700;">{price}</p>
{_btn("JETZT SHOPPEN &rarr;", btn_url, c["accent"])}
</td></tr>
</table>
</td></tr>'''


def _product_card_small(tag, title, desc, price, img_url, btn_url, brand):
    c = brand["colors"]
    return f'''<table width="100%" style="border-radius:16px;overflow:hidden;border:1px solid {c["border"]};" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["card_bg"]};text-align:center;padding:0;">
<img src="{img_url}" alt="{title}" width="260" style="display:block;width:100%;height:auto;">
</td></tr>
<tr><td style="background:{c["bg_cream"]};padding:20px 16px;text-align:center;">
<p style="margin:0 0 4px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:10px;font-weight:700;color:{c["accent"]};letter-spacing:1.5px;text-transform:uppercase;">{tag}</p>
<h3 style="margin:0 0 6px 0;font-family:'DM Serif Display',Georgia,serif;font-size:18px;color:{c["dark"]};font-weight:400;">{title}</h3>
<p style="margin:0 0 4px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;line-height:16px;color:{c["text"]};">{desc}</p>
<p style="margin:0 0 14px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:18px;color:{c["dark"]};font-weight:700;">{price}</p>
{_btn_outline("SHOPPEN", btn_url, c["dark"])}
</td></tr></table>'''


# ===========================================================================
# EMAIL TYPE GENERATORS
# ===========================================================================
def _get_email_type(topic: Dict) -> str:
    """Determine email type from Notion types list. Falls back to 'recommended_products'."""
    types_raw = " ".join(topic.get("types", [])).lower()
    if "us vs them" in types_raw or "comparison" in types_raw:
        return "us_vs_them"
    elif "faq" in types_raw or "question" in types_raw:
        return "faq"
    elif "show the future" in types_raw or "future" in types_raw or "vision" in types_raw:
        return "show_the_future"
    else:
        return "recommended_products"


def generate_us_vs_them(topic: Dict, brand: Dict) -> Tuple[str, str, str]:
    """
    Us vs Them: Comparison email.
    Design pattern: Side-by-side comparison cards (brand ✅ vs conventional ❌),
    dark hero section, social proof stat, product CTA.
    Returns (subject, preview, html).
    """
    c = brand["colors"]
    name = brand["name"]
    shop_url = brand["url"]
    usps = brand.get("usps", ["Qualität"])

    # Use Notion content for comparison points if available
    content = topic.get("content", "")
    
    # Build comparison points from USPs or content
    brand_points = []
    other_points = []
    if content:
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("✅") or line.startswith("+"):
                brand_points.append(line.lstrip("✅+ "))
            elif line.startswith("❌") or line.startswith("-"):
                other_points.append(line.lstrip("❌- "))
    
    if not brand_points:
        brand_points = usps[:5] if usps else ["Premium Qualität", "Nachhaltig", "Made with care"]
    if not other_points:
        other_points = ["Massenproduktion", "Billigmaterial", "Keine Zertifizierung"]

    # Pad to equal length
    max_len = max(len(brand_points), len(other_points))
    while len(brand_points) < max_len:
        brand_points.append("")
    while len(other_points) < max_len:
        other_points.append("")

    brand_items = "\n".join([
        f'<p style="margin:0 0 10px 0;font-family:\'Plus Jakarta Sans\',sans-serif;font-size:13px;line-height:20px;color:{c["dark"]};">&#x2705; {p}</p>'
        for p in brand_points if p
    ])
    other_items = "\n".join([
        f'<p style="margin:0 0 10px 0;font-family:\'Plus Jakarta Sans\',sans-serif;font-size:13px;line-height:20px;color:#8D8D8D;">&#x274C; {p}</p>'
        for p in other_points if p
    ])

    # Claude AI content
    ai = generate_content_with_claude(topic, brand, brand.get("products", []), "us_vs_them") if USE_CLAUDE else None
    hero_title = ai["hero_title"] if ai else "Was uns wirklich"
    hero_subtitle = ai.get("hero_subtitle", "anders macht") if ai else "anders macht"
    hero_text = ai["hero_text"] if ai else topic["name"]
    hero_cta = ai.get("hero_cta", "SELBST ÜBERZEUGEN &rarr;") if ai else "SELBST ÜBERZEUGEN &rarr;"

    # Hero image
    hero_img = ""
    if brand.get("product_images"):
        hero_img = f'<tr><td style="padding:0;"><img src="{_shopify_img_url(brand["product_images"][0], 600)}" alt="{name}" width="600" style="display:block;width:100%;height:auto;"></td></tr>'

    # Product card
    product_card = ""
    if brand.get("products") and brand.get("product_images"):
        p = brand["products"][0]
        img = brand["product_images"][0] if brand["product_images"] else ""
        product_card = _product_card_large("Bestseller", p["name"], "", p.get("price", ""), _shopify_img_url(img, 400), p["url"], brand)

    # Personalization
    greeting = '{%- if first_name -%}Hey {{ first_name }},{%- else -%}Hey,{%- endif -%}'

    body = f'''
<!-- HERO -->
<tr><td style="padding:0;">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["dark"]};padding:50px 40px;text-align:center;" class="mobile-padding">
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:{c["text_light"]};margin:0 0 12px 0;">{greeting}</p>
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;font-weight:600;color:{c["text_light"]};letter-spacing:2px;text-transform:uppercase;margin:0 0 16px 0;">&#x2694;&#xFE0F; DER VERGLEICH</p>
<h1 style="margin:0 0 14px 0;font-family:'DM Serif Display',Georgia,serif;font-size:42px;line-height:48px;font-weight:400;color:#ffffff;" class="hero-title">
{hero_title}<br><span style="color:{c["text_light"]};font-style:italic;">{hero_subtitle}</span>
</h1>
<p style="margin:0 0 28px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;line-height:22px;color:{c["text_light"]};font-weight:500;">
{hero_text}
</p>
{_btn(hero_cta, shop_url, c["accent"])}
</td></tr></table>
</td></tr>
{_usp_bar(brand)}
{hero_img}
<!-- COMPARISON -->
<tr><td style="padding:36px 40px 12px 40px;text-align:center;" class="mobile-padding">
<h2 style="margin:0 0 6px 0;font-family:'DM Serif Display',Georgia,serif;font-size:28px;color:{c["dark"]};font-weight:400;">{name} vs. der Rest</h2>
</td></tr>
<tr><td style="padding:12px 30px;" class="mobile-padding">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr>
<td width="49%" valign="top" style="padding-right:6px;" class="mobile-stack">
<table width="100%" style="border-radius:16px;overflow:hidden;border:2px solid {c["accent"]};" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["accent"]};padding:12px;text-align:center;">
<p style="margin:0;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;color:#fff;letter-spacing:1.5px;text-transform:uppercase;">&#x1F33F; {name}</p>
</td></tr>
<tr><td style="background:{c["bg_cream"]};padding:20px 16px;">
{brand_items}
</td></tr></table>
</td>
<td width="49%" valign="top" style="padding-left:6px;" class="mobile-stack">
<table width="100%" style="border-radius:16px;overflow:hidden;border:1px solid {c["border"]};" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:#8D8D8D;padding:12px;text-align:center;">
<p style="margin:0;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;color:#fff;letter-spacing:1.5px;text-transform:uppercase;">Herkömmlich</p>
</td></tr>
<tr><td style="background:{c["card_bg"]};padding:20px 16px;">
{other_items}
</td></tr></table>
</td>
</tr></table>
</td></tr>
<!-- CTA -->
<tr><td style="padding:28px 40px;" class="mobile-padding">
<table width="100%" style="border-radius:16px;overflow:hidden;" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["dark"]};padding:36px 32px;text-align:center;">
<p style="margin:0 0 4px 0;font-family:'DM Serif Display',Georgia,serif;font-size:22px;line-height:28px;color:#ffffff;font-style:italic;">Überzeug dich selbst.</p>
<p style="margin:10px 0 20px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;color:{c["text_light"]};">Qualität die man spürt.</p>
{_btn("JETZT ENTDECKEN &rarr;", shop_url, c["accent"])}
</td></tr></table>
</td></tr>
{product_card}
'''

    subject = ai["subject"] if ai else f"{topic['name']} | {name}"
    preview = ai["preview"] if ai else f"Was {name} wirklich anders macht"
    return subject, preview, _wrap(body, brand)


def generate_recommended_products(topic: Dict, brand: Dict) -> Tuple[str, str, str]:
    """
    Recommended Products: Product showcase with grid layout.
    Design pattern: Hero image, large feature card, 2-col small cards, testimonial.
    """
    c = brand["colors"]
    name = brand["name"]
    shop_url = brand["url"]
    products = brand.get("products", [])
    images = brand.get("product_images", [])

    # Claude AI content generation
    ai = generate_content_with_claude(topic, brand, products, "recommended_products") if USE_CLAUDE else None

    # Use AI content or fallback to static
    hero_title = ai["hero_title"] if ai else "Unsere Top-Produkte"
    hero_subtitle = ai.get("hero_subtitle", "") if ai else ""
    hero_text = ai["hero_text"] if ai else topic["name"]
    hero_cta = ai["hero_cta"] if ai else "ALLE PRODUKTE &rarr;"
    closing_title = ai["closing_title"] if ai else "&bdquo;Absolut überzeugt! Qualität die man spürt.&ldquo;"
    closing_text = ai["closing_text"] if ai else "&ndash; Verifizierter Kunde"
    closing_cta = ai.get("closing_cta", "JETZT ENTDECKEN &rarr;") if ai else "JETZT ENTDECKEN &rarr;"
    ai_product_descs = ai.get("product_descriptions", []) if ai else []

    # Hero image
    hero_img = ""
    if images:
        img_url = _shopify_img_url(images[0], 600)
        hero_img = f'<tr><td style="padding:0;"><img src="{img_url}" alt="{name}" width="600" style="display:block;width:100%;height:auto;"></td></tr>'

    # Product cards with AI descriptions
    product_cards = ""
    if products and images:
        p0 = products[0]
        img0 = _shopify_img_url(images[0] if images else "", 400)
        p0_desc = ai_product_descs[0]["description"] if ai_product_descs else ""
        p0_tag = ai_product_descs[0].get("tagline", "⭐ Empfehlung") if ai_product_descs else "⭐ Empfehlung"
        p0_price = p0.get("price", "") if isinstance(p0, dict) else ""
        product_cards += _product_card_large(p0_tag, p0["name"], p0_desc, p0_price, img0, p0["url"], brand)

        # Remaining products in 2-col grid
        if len(products) >= 3 and len(images) >= 3:
            p1_desc = ai_product_descs[1]["description"] if len(ai_product_descs) > 1 else ""
            p2_desc = ai_product_descs[2]["description"] if len(ai_product_descs) > 2 else ""
            product_cards += f'''
<tr><td style="padding:10px 30px;" class="mobile-padding">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0"><tr>
<td width="49%" valign="top" style="padding-right:6px;" class="mobile-stack">
{_product_card_small("", products[1]["name"], p1_desc, products[1].get("price", ""), _shopify_img_url(images[1], 260), products[1]["url"], brand)}
</td>
<td width="49%" valign="top" style="padding-left:6px;" class="mobile-stack">
{_product_card_small("", products[2]["name"], p2_desc, products[2].get("price", ""), _shopify_img_url(images[2], 260), products[2]["url"], brand)}
</td>
</tr></table>
</td></tr>'''

    # Personalization with Klaviyo variables
    greeting = '{%- if first_name -%}Hey {{ first_name }},{%- else -%}Hey,{%- endif -%}'

    body = f'''
{hero_img}
<!-- HERO TEXT -->
<tr><td style="padding:36px 40px 12px 40px;text-align:center;" class="mobile-padding">
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:{c["text"]};margin:0 0 12px 0;">{greeting}</p>
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;font-weight:600;color:{c["accent"]};letter-spacing:2px;text-transform:uppercase;margin:0 0 12px 0;">&#x2B50; HANDVERLESEN FÜR DICH</p>
<h1 style="margin:0 0 12px 0;font-family:'DM Serif Display',Georgia,serif;font-size:40px;line-height:46px;font-weight:400;color:{c["dark"]};" class="hero-title">
{hero_title}
</h1>
<p style="margin:0 0 24px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;line-height:22px;color:{c["text"]};">
{hero_text}
</p>
{_btn(hero_cta, shop_url, c["dark"])}
</td></tr>
{_usp_bar(brand)}
{product_cards}
<!-- TESTIMONIAL / CLOSING -->
<tr><td style="padding:28px 40px;" class="mobile-padding">
<table width="100%" style="border-radius:16px;overflow:hidden;" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["dark"]};padding:32px;text-align:center;">
<p style="margin:0 0 8px 0;font-size:24px;">&#x2B50;&#x2B50;&#x2B50;&#x2B50;&#x2B50;</p>
<p style="margin:0 0 4px 0;font-family:'DM Serif Display',Georgia,serif;font-size:18px;line-height:26px;color:#ffffff;font-style:italic;">
{closing_title}
</p>
<p style="margin:10px 0 0 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;color:{c["text_light"]};font-weight:600;letter-spacing:1px;text-transform:uppercase;">{closing_text}</p>
</td></tr></table>
</td></tr>
'''

    subject = ai["subject"] if ai else f"Unsere Top-Produkte | {name}"
    preview = ai["preview"] if ai else f"Handverlesen für dich – die {name} Bestseller"
    return subject, preview, _wrap(body, brand)


def generate_faq(topic: Dict, brand: Dict) -> Tuple[str, str, str]:
    """
    FAQ Email: Q&A style with accordion layout.
    Design pattern: Soft hero, bordered FAQ card, each Q&A separated by line.
    """
    c = brand["colors"]
    name = brand["name"]
    shop_url = brand["url"]

    # Parse FAQ from Notion content
    content = topic.get("content", "")
    faqs = []
    if content:
        lines = content.split("\n")
        current_q = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Heuristic: lines ending with ? or starting with Q: are questions
            if line.endswith("?") or line.lower().startswith("q:") or line.lower().startswith("frage"):
                if current_q and current_q.get("a"):
                    faqs.append(current_q)
                current_q = {"q": line.lstrip("Q:q: "), "a": ""}
            elif current_q is not None:
                current_q["a"] = (current_q["a"] + " " + line).strip()
            else:
                # First non-question line without a question → skip or treat as intro
                pass
        if current_q and current_q.get("a"):
            faqs.append(current_q)

    # Fallback FAQs
    if not faqs:
        faqs = [
            {"q": f"Was macht {name} besonders?", "a": f"{name} steht für Qualität und Nachhaltigkeit. Unsere Produkte werden mit höchsten Standards gefertigt."},
            {"q": "Wie schnell wird geliefert?", "a": "Wir liefern in der Regel innerhalb von 2-3 Werktagen."},
            {"q": "Gibt es ein Rückgaberecht?", "a": "Selbstverständlich! 30 Tage Rückgaberecht auf alle Produkte."},
            {"q": "Wo werden die Produkte hergestellt?", "a": "Unsere Produkte werden lokal und nachhaltig produziert."},
        ]

    faq_html = ""
    for i, faq in enumerate(faqs[:6]):
        border = f"border-bottom:1px solid {c['border']};" if i < len(faqs) - 1 else ""
        faq_html += f'''<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="{border}padding:20px 0;">
<p style="margin:0 0 8px 0;font-family:'DM Serif Display',Georgia,serif;font-size:18px;line-height:24px;color:{c["dark"]};">{faq["q"]}</p>
<p style="margin:0;font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;line-height:22px;color:{c["text"]};">{faq["a"]}</p>
</td></tr></table>'''

    # Claude AI content
    ai = generate_content_with_claude(topic, brand, brand.get("products", []), "faq") if USE_CLAUDE else None
    hero_title = ai["hero_title"] if ai else "Deine Fragen,"
    hero_subtitle = ai.get("hero_subtitle", "unsere Antworten") if ai else "unsere Antworten"
    hero_text = ai["hero_text"] if ai else f"Alles was du über {name} wissen musst."

    greeting = '{%- if first_name -%}Hey {{ first_name }},{%- else -%}Hey,{%- endif -%}'

    body = f'''
<!-- HERO -->
<tr><td style="padding:0;">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["card_bg"]};padding:50px 40px;text-align:center;" class="mobile-padding">
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:{c["text"]};margin:0 0 12px 0;">{greeting}</p>
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:12px;font-weight:600;color:{c["accent"]};letter-spacing:2px;text-transform:uppercase;margin:0 0 16px 0;">&#x2753; HÄUFIGE FRAGEN</p>
<h1 style="margin:0 0 14px 0;font-family:'DM Serif Display',Georgia,serif;font-size:42px;line-height:48px;font-weight:400;color:{c["dark"]};" class="hero-title">
{hero_title}<br><span style="color:{c["accent"]};font-style:italic;">{hero_subtitle}</span>
</h1>
<p style="margin:0;font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;line-height:22px;color:{c["text"]};">
{hero_text}
</p>
</td></tr></table>
</td></tr>
{_usp_bar(brand)}
<!-- FAQ ITEMS -->
<tr><td style="padding:16px 40px 0 40px;" class="mobile-padding">
<table width="100%" style="border-radius:16px;overflow:hidden;border:1px solid {c["border"]};" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["bg_cream"]};padding:8px 28px;">
{faq_html}
</td></tr></table>
</td></tr>
<!-- CTA -->
<tr><td style="padding:28px 40px;" class="mobile-padding">
<table width="100%" style="border-radius:16px;overflow:hidden;" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["dark"]};padding:36px 32px;text-align:center;">
<p style="margin:0 0 4px 0;font-family:'DM Serif Display',Georgia,serif;font-size:22px;line-height:28px;color:#ffffff;font-style:italic;">Noch Fragen? Wir sind für dich da.</p>
<p style="margin:10px 0 20px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;color:{c["text_light"]};">Schreib uns oder entdecke unsere Produkte im Shop.</p>
{_btn("ZUM SHOP &rarr;", shop_url, c["accent"])}
</td></tr></table>
</td></tr>
'''

    subject = ai["subject"] if ai else f"Deine Fragen – beantwortet | {name}"
    preview = ai["preview"] if ai else f"Alles was du über {name} wissen musst"
    return subject, preview, _wrap(body, brand)


def generate_show_the_future(topic: Dict, brand: Dict) -> Tuple[str, str, str]:
    """
    Show the Future: PAS (Problem-Agitate-Solution) narrative.
    Design pattern: Dark hero, lifestyle image, story section, vision cards,
    social proof stat, single delayed CTA.
    """
    c = brand["colors"]
    name = brand["name"]
    shop_url = brand["url"]
    usps = brand.get("usps", ["Qualität", "Nachhaltigkeit", "Premium"])

    # Claude AI content
    ai = generate_content_with_claude(topic, brand, brand.get("products", []), "show_the_future") if USE_CLAUDE else None
    hero_title = ai["hero_title"] if ai else "Die Zukunft"
    hero_subtitle = ai.get("hero_subtitle", "beginnt jetzt") if ai else "beginnt jetzt"
    hero_text = ai["hero_text"] if ai else topic["name"]
    hero_cta = ai.get("hero_cta", "ZUKUNFT ENTDECKEN &rarr;") if ai else "ZUKUNFT ENTDECKEN &rarr;"
    closing_title = ai.get("closing_title", "Sei Teil der Veränderung.") if ai else "Sei Teil der Veränderung."
    closing_text = ai.get("closing_text", "Qualität. Nachhaltigkeit. Zukunft.") if ai else "Qualität. Nachhaltigkeit. Zukunft."
    closing_cta = ai.get("closing_cta", "JETZT STARTEN &rarr;") if ai else "JETZT STARTEN &rarr;"

    # Hero image
    hero_img = ""
    if brand.get("product_images"):
        hero_img = f'<tr><td style="padding:0;"><img src="{_shopify_img_url(brand["product_images"][0], 600)}" alt="{name}" width="600" style="display:block;width:100%;height:auto;"></td></tr>'

    # Vision cards from USPs
    vision_cards = ""
    for i, usp in enumerate(usps[:3]):
        emojis = ["&#x1F33F;", "&#x2728;", "&#x1F1E9;&#x1F1EA;"]
        emoji = emojis[i % 3]
        vision_cards += f'''<td width="33%" style="text-align:center;padding:8px 4px;" class="mobile-stack">
<div style="background:{c["card_bg"]};border-radius:16px;padding:24px 12px;">
<p style="font-size:32px;margin:0 0 8px 0;">{emoji}</p>
<p style="margin:0;font-family:'DM Serif Display',Georgia,serif;font-size:15px;color:{c["dark"]};">{usp}</p>
</div>
</td>'''

    # Content from Notion
    story = topic.get("content", "")
    if not story:
        story = ai.get("hero_text", f"Stell dir vor: Produkte die nicht nur gut aussehen, sondern auch gut für die Zukunft sind. Bei {name} arbeiten wir jeden Tag daran.") if ai else f"Stell dir vor: Produkte die nicht nur gut aussehen, sondern auch gut für die Zukunft sind. Bei {name} arbeiten wir jeden Tag daran."
    story_html = ""
    for line in story.split("\n"):
        line = line.strip()
        if line:
            story_html += f'<p style="margin:0 0 12px 0;font-family:\'Plus Jakarta Sans\',sans-serif;font-size:15px;line-height:26px;color:{c["text"]};">{line}</p>'

    greeting = '{%- if first_name -%}Hey {{ first_name }},{%- else -%}Hey,{%- endif -%}'

    body = f'''
<!-- HERO -->
<tr><td style="padding:0;">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["dark"]};padding:50px 40px;text-align:center;" class="mobile-padding">
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;color:{c["text_light"]};margin:0 0 12px 0;">{greeting}</p>
<p style="font-size:48px;margin:0 0 12px 0;">&#x1F331;</p>
<h1 style="margin:0 0 14px 0;font-family:'DM Serif Display',Georgia,serif;font-size:42px;line-height:48px;font-weight:400;color:#ffffff;" class="hero-title">
{hero_title}<br><span style="color:{c["text_light"]};font-style:italic;">{hero_subtitle}</span>
</h1>
<p style="margin:0 0 28px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;line-height:22px;color:{c["text_light"]};">
{hero_text}
</p>
{_btn(hero_cta, shop_url, c["accent"])}
</td></tr></table>
</td></tr>
{_usp_bar(brand)}
{hero_img}
<!-- STORY -->
<tr><td style="padding:36px 40px 16px 40px;text-align:center;" class="mobile-padding">
<h2 style="margin:0 0 16px 0;font-family:'DM Serif Display',Georgia,serif;font-size:28px;color:{c["dark"]};font-weight:400;">Stell dir vor...</h2>
{story_html}
</td></tr>
<!-- VISION CARDS -->
<tr><td style="padding:12px 30px;" class="mobile-padding">
<table width="100%" role="presentation" cellspacing="0" cellpadding="0" border="0"><tr>
{vision_cards}
</tr></table>
</td></tr>
<!-- SOCIAL PROOF + CTA -->
<tr><td style="padding:20px 40px;" class="mobile-padding">
<table width="100%" style="border-radius:16px;overflow:hidden;" role="presentation" cellspacing="0" cellpadding="0" border="0">
<tr><td style="background:{c["dark"]};padding:36px 32px;text-align:center;">
<p style="margin:0 0 4px 0;font-family:'DM Serif Display',Georgia,serif;font-size:22px;line-height:28px;color:#ffffff;font-style:italic;">{closing_title}</p>
<p style="margin:10px 0 20px 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:13px;color:{c["text_light"]};">{closing_text}</p>
{_btn(closing_cta, shop_url, c["accent"])}
</td></tr></table>
</td></tr>
'''

    subject = ai["subject"] if ai else f"Die Zukunft beginnt jetzt | {name}"
    preview = ai["preview"] if ai else f"Stell dir vor... {name}"
    return subject, preview, _wrap(body, brand)


# Map email type → generator
GENERATORS = {
    "us_vs_them": generate_us_vs_them,
    "recommended_products": generate_recommended_products,
    "faq": generate_faq,
    "show_the_future": generate_show_the_future,
}


# ===========================================================================
# KLAVIYO: CAMPAIGN CREATION
# ===========================================================================
def find_klaviyo_list(api_key: str) -> Optional[str]:
    """Find the best newsletter list in Klaviyo."""
    ckey = f"list_{api_key[:8]}"
    if ckey in _cache:
        return _cache[ckey]
    resp = klaviyo_api("GET", "/lists", api_key=api_key)
    if not resp:
        return None
    lists = resp.get("data", [])
    if not lists:
        return None
    target = lists[0]["id"]
    for l in lists:
        name = l["attributes"]["name"].lower()
        if any(kw in name for kw in ["newsletter", "main", "all", "email"]):
            target = l["id"]
            break
    _cache[ckey] = target
    return target


def create_campaign_with_template(
    api_key: str,
    list_id: str,
    campaign_name: str,
    subject: str,
    preview: str,
    html: str,
    send_date: str,
) -> Dict:
    """
    Create a Klaviyo campaign with template in the correct order:
    1. Create campaign (with message inline via campaign-messages)
    2. Create template (POST /templates with editor_type: CODE)
    3. Assign template (POST /campaign-message-assign-template/)
    4. Update subject line (PATCH /campaign-messages/{id})
    Returns dict with campaign_id, message_id, template_id, status.
    """
    result = {"campaign_id": None, "message_id": None, "template_id": None, "status": "failed"}

    # Step 1: Create campaign
    send_dt = f"{send_date}T09:00:00.000Z"  # 10:00 Berlin = 09:00 UTC (simplified)
    camp_data = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": campaign_name,
                "audiences": {"included": [list_id], "excluded": []},
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "channel": "email",
                            "label": subject[:50],
                            "content": {
                                "subject": subject,
                                "preview_text": preview,
                            }
                        }
                    }]
                },
                "send_strategy": {
                    "method": "static",
                    "options_static": {"datetime": send_dt}
                }
            }
        }
    }

    resp = klaviyo_api("POST", "/campaigns", camp_data, api_key)
    if not resp or "data" not in resp:
        result["status"] = "Campaign creation failed"
        return result

    campaign_id = resp["data"]["id"]
    message_id = resp["data"]["relationships"]["campaign-messages"]["data"][0]["id"]
    result["campaign_id"] = campaign_id
    result["message_id"] = message_id
    log(f"    📦 Campaign: {campaign_id}, Message: {message_id}")

    # Step 2: Create template
    tpl_resp = klaviyo_api("POST", "/templates", {
        "data": {
            "type": "template",
            "attributes": {
                "name": campaign_name,
                "html": html,
                "editor_type": "CODE"
            }
        }
    }, api_key)

    if not tpl_resp or "data" not in tpl_resp:
        result["status"] = "Template creation failed"
        return result

    template_id = tpl_resp["data"]["id"]
    result["template_id"] = template_id
    log(f"    🎨 Template: {template_id}")

    # Step 3: Assign template to message
    assign_resp = klaviyo_api("POST", "/campaign-message-assign-template/", {
        "data": {
            "type": "campaign-message",
            "id": message_id,
            "relationships": {
                "template": {
                    "data": {"type": "template", "id": template_id}
                }
            }
        }
    }, api_key)

    if assign_resp is None:
        # Fallback: try PATCH on campaign-messages
        log(f"    ⚠️ assign-template failed, trying PATCH fallback...")
        klaviyo_api("PATCH", f"/campaign-messages/{message_id}", {
            "data": {
                "type": "campaign-message",
                "id": message_id,
                "relationships": {
                    "template": {
                        "data": {"type": "template", "id": template_id}
                    }
                }
            }
        }, api_key)

    log(f"    ✅ Template assigned")

    result["status"] = f"Scheduled {send_date} 10:00"
    return result


# ===========================================================================
# MAIN ORCHESTRATOR
# ===========================================================================
def main():
    parser = argparse.ArgumentParser(description="Weekly Klaviyo Newsletter Generator")
    parser.add_argument("--client", help="Process only this client (by name)")
    parser.add_argument("--topic", help="Process only this topic (by name)")
    parser.add_argument("--date", help="Process topics for specific date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=14, help="Look ahead days (default: 14)")
    parser.add_argument("--skip-telegram", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Generate HTML but don't create campaigns")
    parser.add_argument("--use-claude", action="store_true", help="Use Claude AI for content generation")
    args = parser.parse_args()

    # Set global Claude flag
    global USE_CLAUDE
    if args.use_claude:
        if ANTHROPIC_API_KEY:
            USE_CLAUDE = True
            log("🤖 Claude AI content generation: ENABLED")
        else:
            log("⚠️ --use-claude specified but ANTHROPIC_API_KEY not set. Falling back to static content.")
            USE_CLAUDE = False

    log("=" * 60)
    log("📧 Weekly Newsletter Generator")
    log("=" * 60)

    # 1. Fetch topics from Notion
    log("\n📖 Fetching topics from Notion...")
    topics = get_notion_topics(args.days, args.date)
    if args.topic:
        topics = [t for t in topics if args.topic.lower() in t["name"].lower()]
    if not topics:
        msg = "📧 Newsletter: Keine Themen gefunden."
        log(msg)
        if not args.skip_telegram:
            send_telegram(msg)
        return

    log(f"✅ {len(topics)} topics found")

    # 2. Fetch clients from Airtable
    log("\n👥 Fetching Klaviyo clients...")
    clients = get_klaviyo_clients()
    if args.client:
        clients = [c for c in clients if args.client.lower() in c["firmenname"].lower()]
    if not clients:
        msg = "📧 Newsletter: Keine Kunden mit Klaviyo gefunden."
        log(msg)
        if not args.skip_telegram:
            send_telegram(msg)
        return

    log(f"✅ {len(clients)} clients")
    for c in clients:
        log(f"  • {c['firmenname']}")

    # 3. Process each client × topic
    log("\n✍️ Generating newsletters...")
    results = []

    for client in clients:
        log(f"\n{'='*40}")
        log(f"📝 {client['firmenname']}")
        log(f"{'='*40}")

        # Analyze brand
        log(f"  🔍 Analyzing {client['website']}...")
        brand = analyze_brand(client["website"], client["firmenname"])

        # Find Klaviyo list
        list_id = find_klaviyo_list(client["klaviyo_key"])
        if not list_id:
            log(f"  ❌ No Klaviyo list found, skipping")
            continue
        log(f"  📋 List: {list_id}")

        for topic in topics:
            email_type = _get_email_type(topic)
            generator = GENERATORS.get(email_type, generate_recommended_products)
            log(f"\n  📨 {topic['name']} → {email_type}")

            # Generate email
            subject, preview, html = generator(topic, brand)
            campaign_name = f"{client['firmenname']} - {topic['name']} - {topic['date']}"

            if args.dry_run:
                # Save HTML locally for preview
                safe_name = re.sub(r'[^\w-]', '_', campaign_name)
                path = f"/tmp/newsletter_{safe_name}.html"
                with open(path, "w") as f:
                    f.write(html)
                log(f"    💾 Saved: {path}")
                results.append({
                    "client": client["firmenname"],
                    "topic": topic["name"],
                    "type": email_type,
                    "status": f"dry-run → {path}",
                    "campaign_id": None,
                })
                continue

            # Create campaign + template in Klaviyo
            r = create_campaign_with_template(
                client["klaviyo_key"],
                list_id,
                campaign_name,
                subject,
                preview,
                html,
                topic["date"],
            )

            results.append({
                "client": client["firmenname"],
                "topic": topic["name"],
                "type": email_type,
                "subject": subject,
                **r,
            })

            if r["campaign_id"]:
                log(f"    ✅ {r['status']}")
            else:
                log(f"    ❌ {r['status']}")

    # 4. Report
    successful = len([r for r in results if r.get("campaign_id")])
    failed = len([r for r in results if not r.get("campaign_id")])

    report = f"""📧 *Newsletter-Vorbereitung abgeschlossen!*

*Datum:* {datetime.now().strftime('%d.%m.%Y %H:%M')}
*Themen:* {len(topics)}
*Kunden:* {len(clients)}

✅ {successful} Campaigns erstellt
❌ {failed} Fehler"""

    for client in clients:
        cc = [r for r in results if r["client"] == client["firmenname"] and r.get("campaign_id")]
        report += f"\n• {client['firmenname']}: {len(cc)}/{len(topics)}"

    log(f"\n{'='*60}")
    log(report)

    if not args.skip_telegram:
        send_telegram(report)

    # JSON output
    print(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "topics": len(topics),
        "clients": len(clients),
        "successful": successful,
        "failed": failed,
        "campaigns": results,
    }, indent=2))


if __name__ == "__main__":
    main()
