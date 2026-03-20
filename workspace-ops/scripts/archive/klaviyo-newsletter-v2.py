#!/usr/bin/env python3
"""
Klaviyo Newsletter Automation v2 — Clean Template System
4 structured email templates with brand design system.
"""

import urllib.request
import json
import os
import sys
import ssl
import re
import time
from datetime import datetime, timedelta

# ─── Config ──────────────────────────────────────────────────────────────────
NOTION_KEY = open(os.path.expanduser("~/.config/notion/api_key")).read().strip()
NOTION_DS_ID = "f973c96b-5659-4fd8-97c2-63984dbd89d9"
MATON_KEY = os.environ.get("MATON_API_KEY", "")
AIRTABLE_BASE = "appbGhxy9I18oIS8E"
TELEGRAM_BOT_TOKEN = "8586858553:AAEKHWk0ru9UHzhMAAWwlFyfqa2GAk16gxM"
TELEGRAM_CHAT_ID = "6607099798"
CACHE_DAYS = 30

# ─── Design System ──────────────────────────────────────────────────────────
# Default brand tokens (overridden per client from Airtable/website analysis)
DEFAULT_DESIGN = {
    "headingFont": "'DM Serif Display', Georgia, serif",
    "bodyFont": "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "colors": {
        "primary": "#48413C",
        "accent": "#0C5132",
        "background": "#F3F2EE",
        "surface": "#FFFFFF",
        "text": "#1A1A1A",
        "textLight": "#6B6B6B",
        "border": "#E5E2DD",
    },
}

# Razeco Shopify product images (known good URLs from successful run)
RAZECO_PRODUCTS = [
    {
        "name": "Schwarzkümmelöl Kapseln",
        "image": "https://cdn.shopify.com/s/files/1/0915/8563/5774/files/RAZECO_Schwarzkummelol_Kapseln_-_Naturliche_Nahrungserganzung.jpg",
        "url": "https://razeco.de/products/schwarzkummelol-kapseln",
        "price": "24,90 €",
    },
    {
        "name": "Vitamin D3 + K2 Tropfen",
        "image": "https://cdn.shopify.com/s/files/1/0915/8563/5774/files/RAZECO_Vitamin_D3_K2_Tropfen.jpg",
        "url": "https://razeco.de/products/vitamin-d3-k2-tropfen",
        "price": "19,90 €",
    },
    {
        "name": "Omega 3 Kapseln",
        "image": "https://cdn.shopify.com/s/files/1/0915/8563/5774/files/RAZECO_Omega_3_Kapseln.jpg",
        "url": "https://razeco.de/products/omega-3-kapseln",
        "price": "22,90 €",
    },
]

# ─── Template Type Mapping ───────────────────────────────────────────────────
# Maps Notion "Email Type" multi_select values → template function
TEMPLATE_MAP = {
    "Us vs Them": "us_vs_them",
    "Recommended Products": "recommended_products",
    "FAQ Email": "faq_email",
    "Show the Future": "show_the_future",
}


# ═══════════════════════════════════════════════════════════════════════════════
#  UTILITY
# ═══════════════════════════════════════════════════════════════════════════════

def log(msg):
    print(msg, file=sys.stderr)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        log(f"Telegram error: {e}")


def _ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def safe_request(url, method="GET", headers=None, data=None, retry=3, timeout=15):
    headers = headers or {}
    ctx = _ssl_ctx()
    for attempt in range(retry):
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            if data:
                req.data = json.dumps(data).encode() if isinstance(data, dict) else data
            resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            body = resp.read()
            return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="ignore")[:500]
            log(f"  HTTP {e.code} (attempt {attempt+1}): {err}")
            if attempt == retry - 1:
                raise
            time.sleep(2 ** attempt)
        except Exception as e:
            log(f"  Error (attempt {attempt+1}): {str(e)[:150]}")
            if attempt == retry - 1:
                raise
            time.sleep(2 ** attempt)


# ═══════════════════════════════════════════════════════════════════════════════
#  NOTION
# ═══════════════════════════════════════════════════════════════════════════════

def get_notion_topics(days=14, target_date=None):
    today = datetime.now()
    if target_date:
        try:
            d = datetime.strptime(target_date, "%Y-%m-%d")
            date_start, date_end = d, d
        except ValueError:
            date_start, date_end = today, today + timedelta(days=days)
    else:
        date_start, date_end = today, today + timedelta(days=days)

    log(f"📅 Topics window: {date_start:%d.%m.%Y} – {date_end:%d.%m.%Y}")

    headers = {
        "Authorization": f"Bearer {NOTION_KEY}",
        "Notion-Version": "2025-09-03",
        "Content-Type": "application/json",
    }

    all_entries, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = safe_request(
            f"https://api.notion.com/v1/data_sources/{NOTION_DS_ID}/query",
            method="POST", headers=headers, data=body,
        )
        all_entries.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")

    log(f"📊 {len(all_entries)} total Notion entries")

    topics = []
    for entry in all_entries:
        props = entry["properties"]
        dp = props.get("Date", {}).get("date")
        if not dp or not dp.get("start"):
            continue
        entry_date = datetime.strptime(dp["start"], "%Y-%m-%d")
        try:
            mapped = entry_date.replace(year=today.year)
        except ValueError:
            mapped = datetime(today.year, 3, 1)

        if date_start.date() <= mapped.date() <= date_end.date():
            name = "".join(t["plain_text"] for t in props.get("Name", {}).get("title", []))
            types = [s["name"] for s in props.get("Email Type", {}).get("multi_select", [])]
            content = _fetch_page_content(entry["id"])
            topics.append({"name": name, "date": mapped.strftime("%Y-%m-%d"), "types": types, "content": content, "pageId": entry["id"]})
            log(f"  ✅ {mapped:%d.%m}: {name} ({', '.join(types) or 'no type'})")

    topics.sort(key=lambda x: x["date"])
    return topics


def _fetch_page_content(page_id):
    headers = {"Authorization": f"Bearer {NOTION_KEY}", "Notion-Version": "2025-09-03"}
    try:
        resp = safe_request(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers)
        lines = []
        for b in resp.get("results", []):
            bt = b["type"]
            rich = b.get(bt, {}).get("rich_text", [])
            text = "".join(r["plain_text"] for r in rich)
            if not text.strip():
                continue
            if bt.startswith("heading"):
                lines.append(f"{'#' * int(bt[-1])} {text}")
            elif bt == "bulleted_list_item":
                lines.append(f"• {text}")
            elif bt == "numbered_list_item":
                lines.append(f"1. {text}")
            elif bt == "quote":
                lines.append(f"> {text}")
            elif bt == "callout":
                emoji = b.get("callout", {}).get("icon", {}).get("emoji", "💡")
                lines.append(f"{emoji} {text}")
            else:
                lines.append(text)
        return "\n".join(lines)
    except Exception as e:
        log(f"  ⚠️ Content fetch failed for {page_id}: {e}")
        return ""


# ═══════════════════════════════════════════════════════════════════════════════
#  AIRTABLE
# ═══════════════════════════════════════════════════════════════════════════════

def get_klaviyo_clients():
    filt = "AND(OR(Status='Aktiv',Status='Onboarding'),{Klaviyo API Key}!='')"
    url = f"https://gateway.maton.ai/airtable/v0/{AIRTABLE_BASE}/Kunden?filterByFormula={urllib.parse.quote(filt)}"
    resp = safe_request(url, headers={"Authorization": f"Bearer {MATON_KEY}"})
    clients = []
    for rec in resp.get("records", []):
        f = rec["fields"]
        clients.append({
            "id": rec["id"],
            "firmenname": f.get("Firmenname", ""),
            "klaviyoKey": f.get("Klaviyo API Key", ""),
            "website": f.get("Website", ""),
            "branche": f.get("Branche", ""),
            "tonalitaet": f.get("Brand Tone", ""),
            "emailFrom": f.get("E-Mail Rechnungen", "") or "hello@adsdrop.de",
            "websiteScanDate": f.get("Website Scan Date", ""),
            "brandColors": f.get("Brand Colors", ""),
            "brandFonts": f.get("Brand Fonts", ""),
            "usps": f.get("USPs", ""),
            "productsJson": f.get("Produkte JSON", ""),
            "klaviyoLogoUrl": f.get("Klaviyo Logo URL", ""),
            "klaviyoNewsletterListId": f.get("Klaviyo Newsletter List ID", ""),
            "brandTagline": f.get("Brand Tagline", ""),
            "socialProof": f.get("Social Proof", ""),
            "emailSprache": f.get("Email Sprache", "de"),
        })
    return clients


def get_products_from_airtable(client_id=None):
    url = f"https://gateway.maton.ai/airtable/v0/{AIRTABLE_BASE}/Produkt-Info"
    if client_id:
        filt = f"{{Kunde}}='{client_id}'"
        url += f"?filterByFormula={urllib.parse.quote(filt)}"
    try:
        resp = safe_request(url, headers={"Authorization": f"Bearer {MATON_KEY}"})
        products = []
        for rec in resp.get("records", []):
            f = rec["fields"]
            products.append({
                "name": f.get("Titel", ""),
                "desc": f.get("Produktbeschreibung", ""),
                "price": f.get("Preis", ""),
                "image": f.get("Bild URL", "") or (f.get("Bild", [{}])[0].get("url", "") if isinstance(f.get("Bild"), list) else ""),
                "url": f.get("URL", ""),
            })
        log(f"    📦 {len(products)} products from Airtable")
        return products
    except Exception as e:
        log(f"    ⚠️ Airtable products failed: {e}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
#  WEBSITE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def get_website_analysis(client):
    if _is_cache_valid(client):
        log(f"    📋 Cached analysis for {client['firmenname']}")
        return _build_analysis(client)
    log(f"    🔍 New analysis for {client['firmenname']}")
    return _analyze_website(client)


def _is_cache_valid(client):
    if not client.get("websiteScanDate"):
        return False
    try:
        d = datetime.fromisoformat(client["websiteScanDate"])
        return (datetime.now() - d).days <= CACHE_DAYS
    except:
        return False


def _build_analysis(client):
    colors = client.get("brandColors", "#000000").split(",")
    return {
        "mainColor": colors[0].strip(),
        "secondaryColor": colors[1].strip() if len(colors) > 1 else "#CCCCCC",
        "fontFamily": client.get("brandFonts", "Arial, sans-serif"),
        "tone": client.get("tonalitaet", "standard"),
        "usp": client.get("usps", ""),
        "products": json.loads(client["productsJson"]) if client.get("productsJson") else [],
    }


def _analyze_website(client):
    url = client.get("website", "")
    html = ""
    if url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=15, context=_ssl_ctx()).read().decode("utf-8", errors="ignore")[:30000]
        except Exception as e:
            log(f"    ⚠️ Fetch failed: {str(e)[:100]}")

    prompt = f"""Analyze this website HTML for newsletter personalization:

{html}

Company: {client['firmenname']}, Industry: {client.get('branche','')}

Return ONLY valid JSON:
{{"products":["..."],"tone":"luxury|casual|standard","usp":"...","mainColor":"#hex","secondaryColor":"#hex","fontFamily":"..."}}"""

    try:
        resp = safe_request("https://api.anthropic.com/v1/messages", method="POST", headers={
            "anthropic-version": "2023-06-01", "content-type": "application/json",
            "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
        }, data={"model": "claude-3-sonnet-20240229", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]})
        content = resp["content"][0]["text"]
        m = re.search(r'\{.*\}', content, re.DOTALL)
        if m:
            analysis = json.loads(m.group())
            # Cache to Airtable
            update_fields = {
                "Website Scan Date": datetime.now().strftime("%Y-%m-%d"),
                "Brand Colors": f"{analysis.get('mainColor','#000')}, {analysis.get('secondaryColor','#CCC')}",
                "Brand Tone": analysis.get("tone", "standard"),
                "USPs": analysis.get("usp", ""),
                "Produkte JSON": json.dumps(analysis.get("products", [])),
            }
            if analysis.get("fontFamily"):
                update_fields["Brand Fonts"] = analysis["fontFamily"]
            _update_airtable("Kunden", client["id"], update_fields)
            return analysis
    except Exception as e:
        log(f"    ❌ Analysis failed: {str(e)[:200]}")

    return _build_analysis(client)


def _update_airtable(table, record_id, fields):
    try:
        safe_request(
            f"https://gateway.maton.ai/airtable/v0/{AIRTABLE_BASE}/{table}/{record_id}",
            method="PATCH",
            headers={"Authorization": f"Bearer {MATON_KEY}", "Content-Type": "application/json"},
            data={"fields": fields},
        )
    except Exception as e:
        log(f"    ⚠️ Airtable update failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
#  EMAIL TEMPLATE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

def _get_design(client, analysis):
    """Build design tokens from client data, falling back to defaults."""
    colors = DEFAULT_DESIGN["colors"].copy()
    if analysis.get("mainColor"):
        colors["primary"] = analysis["mainColor"]
    if analysis.get("secondaryColor"):
        colors["accent"] = analysis["secondaryColor"]

    return {
        "headingFont": DEFAULT_DESIGN["headingFont"],
        "bodyFont": analysis.get("fontFamily", DEFAULT_DESIGN["bodyFont"]),
        "colors": colors,
        "logo": client.get("klaviyoLogoUrl", ""),
        "company": client["firmenname"],
        "website": client.get("website", ""),
        "tagline": client.get("brandTagline", ""),
    }


def _get_products(client, analysis):
    """Get product list — Airtable first, then Razeco defaults, then generic."""
    products = get_products_from_airtable(client.get("id"))
    if products and any(p.get("image") for p in products):
        return products[:3]

    # Razeco fallback
    if "razeco" in client["firmenname"].lower():
        return RAZECO_PRODUCTS

    # Generic from analysis
    product_names = analysis.get("products", [])
    if isinstance(product_names, dict):
        product_names = list(product_names.values())
    return [{"name": str(p) if not isinstance(p, dict) else p.get("name", "Produkt"), "image": "", "url": client.get("website", ""), "price": ""} for p in product_names[:3]]


def _base_wrapper(design, subject, preview_text, body_html):
    """Wraps body content in the standard email shell: preheader, header, body, footer."""
    c = design["colors"]
    logo_html = f'<img src="{design["logo"]}" alt="{design["company"]}" style="max-width:180px;max-height:60px;margin-bottom:12px;display:block;margin-left:auto;margin-right:auto;" />' if design["logo"] else ""

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{subject}</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:0;background:{c['background']};font-family:{design['bodyFont']};color:{c['text']};line-height:1.7;-webkit-font-smoothing:antialiased;">

<!-- Preheader -->
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{preview_text}</div>

<!-- Container -->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{c['background']};">
<tr><td align="center" style="padding:20px 10px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:{c['surface']};border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">

<!-- Header -->
<tr><td style="background:{c['primary']};padding:36px 40px;text-align:center;">
{logo_html}
<h1 style="font-family:{design['headingFont']};font-size:26px;color:#FFFFFF;margin:0;font-weight:400;letter-spacing:-0.3px;">{design['company']}</h1>
{f'<p style="font-size:13px;color:rgba(255,255,255,0.7);margin:6px 0 0;letter-spacing:1.5px;text-transform:uppercase;">{design["tagline"]}</p>' if design["tagline"] else ''}
</td></tr>

<!-- Body -->
<tr><td style="padding:0;">
{body_html}
</td></tr>

<!-- Footer -->
<tr><td style="padding:32px 40px;text-align:center;border-top:1px solid {c['border']};">
<p style="font-family:{design['headingFont']};font-size:18px;color:{c['primary']};margin:0 0 8px;">{design['company']}</p>
<p style="font-size:13px;color:{c['textLight']};margin:0 0 16px;">
<a href="{design['website']}" style="color:{c['textLight']};text-decoration:underline;">{design['website']}</a>
</p>
<p style="font-size:11px;color:#AAAAAA;margin:0;">
Du erhältst diese E-Mail, weil du dich für {design['company']} angemeldet hast.<br/>
<a href="$unsubscribe_url" style="color:#AAAAAA;text-decoration:underline;">Abmelden</a>
</p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""


def _product_grid_html(products, design):
    """Renders a 3-column product grid with Klaviyo variables."""
    c = design["colors"]
    
    # Use Klaviyo template variables for dynamic product data
    # These variables pull from Klaviyo catalog or event data
    cells = ""
    for i in range(3):
        # Klaviyo variables: catalog_item or event data
        name_var = f"{{{{ catalog_item.title | default: event.Items.{i}.Name | default: 'Produkt {i+1}' }}}}"
        image_var = f"{{{{ catalog_item.image_url | default: event.Items.{i}.Image | default: '' }}}}"
        price_var = f"{{{{ catalog_item.price | default: event.Items.{i}.Price | default: '' }}}}"
        url_var = f"{{{{ catalog_item.url | default: event.Items.{i}.URL | default: '{design['website']}' }}}}"
        
        img_html = f'''<img src="{image_var}" alt="{name_var}" style="width:100%;max-width:160px;height:160px;object-fit:cover;border-radius:8px;display:block;margin:0 auto 12px;" onerror="this.style.display='none';this.nextElementSibling.style.display='block';" />
<div style="width:160px;height:160px;background:{c['background']};border-radius:8px;margin:0 auto 12px;display:none;align-items:center;justify-content:center;color:{c['textLight']};font-size:12px;">Bild<br>folgt</div>'''
        
        cells += f"""<td style="width:33.33%;padding:8px;text-align:center;vertical-align:top;">
<a href="{url_var}" style="text-decoration:none;color:inherit;">
{img_html}
<p style="font-family:{design['headingFont']};font-size:15px;color:{c['text']};margin:0 0 4px;line-height:1.3;">{name_var}</p>
<p style="font-size:13px;color:{c['accent']};font-weight:600;margin:0;">{price_var}</p>
</a>
</td>"""

    return f"""<!-- Product Grid -->
<div style="padding:32px 40px;">
<h2 style="font-family:{design['headingFont']};font-size:22px;color:{c['primary']};margin:0 0 20px;text-align:center;">Unsere Empfehlungen</h2>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>{cells}</tr></table>
</div>"""


def _cta_button(text, url, design):
    c = design["colors"]
    return f"""<div style="text-align:center;padding:8px 40px 32px;">
<a href="{url}" style="display:inline-block;background:{c['accent']};color:#FFFFFF;padding:14px 36px;text-decoration:none;border-radius:6px;font-weight:600;font-size:15px;letter-spacing:0.3px;">{text} →</a>
</div>"""


def _section_divider(design):
    return f'<div style="height:1px;background:{design["colors"]["border"]};margin:0 40px;"></div>'


# ─── Template 1: Us vs Them ─────────────────────────────────────────────────

def _template_us_vs_them(topic, client, analysis, design, products):
    """Comparison template: brand vs. generic alternatives."""
    c = design["colors"]
    company = design["company"]
    topic_name = topic["name"]
    content = topic.get("content", "")

    # Build comparison rows from content or generic
    them_points = ["Massenproduktion ohne Transparenz", "Künstliche Zusatzstoffe", "Keine nachhaltige Herkunft"]
    us_points = [f"Handverlesene Qualität bei {company}", "100% natürliche Inhaltsstoffe", "Nachhaltig & transparent"]

    # Try to extract from Notion content
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    if len(lines) >= 6:
        them_points = lines[:3]
        us_points = lines[3:6]

    rows = ""
    for them, us in zip(them_points, us_points):
        rows += f"""<tr>
<td style="padding:12px 16px;border-bottom:1px solid {c['border']};color:{c['textLight']};font-size:14px;width:50%;">❌ {them}</td>
<td style="padding:12px 16px;border-bottom:1px solid {c['border']};color:{c['accent']};font-size:14px;font-weight:600;width:50%;">✅ {us}</td>
</tr>"""

    body = f"""
<!-- Hero -->
<div style="padding:40px 40px 24px;">
<h2 style="font-family:{design['headingFont']};font-size:28px;color:{c['primary']};margin:0 0 16px;line-height:1.2;">{topic_name}</h2>
<p style="font-size:16px;color:{c['textLight']};margin:0 0 24px;line-height:1.7;">Warum immer mehr Menschen auf {company} vertrauen — und was uns von anderen unterscheidet.</p>
</div>

<!-- Comparison Table -->
<div style="padding:0 40px 32px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid {c['border']};border-radius:8px;overflow:hidden;">
<tr style="background:{c['background']};">
<th style="padding:14px 16px;text-align:left;font-size:13px;text-transform:uppercase;letter-spacing:1px;color:{c['textLight']};">Andere</th>
<th style="padding:14px 16px;text-align:left;font-size:13px;text-transform:uppercase;letter-spacing:1px;color:{c['accent']};">{company}</th>
</tr>
{rows}
</table>
</div>

{_section_divider(design)}
{_product_grid_html(products, design)}
{_cta_button("Jetzt selbst überzeugen", design['website'], design)}
"""
    subject = f"{topic_name} | {company}"
    preview = f"Was macht {company} anders? Der ehrliche Vergleich."
    return subject, preview, _base_wrapper(design, subject, preview, body)


# ─── Template 2: Recommended Products ───────────────────────────────────────

def _template_recommended_products(topic, client, analysis, design, products):
    c = design["colors"]
    company = design["company"]
    topic_name = topic["name"]
    content = topic.get("content", "")

    # Featured product with Klaviyo variables
    feat_name = "{{ catalog_item.title | default: event.Items.0.Name | default: 'Unser Bestseller' }}"
    feat_image = "{{ catalog_item.image_url | default: event.Items.0.Image | default: '' }}"
    feat_price = "{{ catalog_item.price | default: event.Items.0.Price | default: '' }}"
    feat_url = "{{ catalog_item.url | default: event.Items.0.URL | default: '" + design["website"] + "' }}"
    
    feat_img = f'<img src="{feat_image}" alt="{feat_name}" style="width:100%;max-width:400px;border-radius:10px;display:block;margin:0 auto;" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'block\';" /><div style="width:400px;height:300px;background:{c["background"]};border-radius:10px;margin:0 auto;display:none;align-items:center;justify-content:center;color:{c["textLight"]};font-size:14px;">Produktbild<br>wird geladen</div>'

    body = f"""
<!-- Hero -->
<div style="padding:40px 40px 24px;">
<h2 style="font-family:{design['headingFont']};font-size:28px;color:{c['primary']};margin:0 0 12px;line-height:1.2;">{topic_name}</h2>
<p style="font-size:16px;color:{c['textLight']};margin:0;line-height:1.7;">Unsere handverlesenen Empfehlungen für dich — passend zum Thema der Woche.</p>
</div>

<!-- Featured Product -->
<div style="padding:16px 40px 32px;text-align:center;">
{feat_img}
<h3 style="font-family:{design['headingFont']};font-size:22px;color:{c['text']};margin:20px 0 8px;">{feat_name}</h3>
<p style="font-size:18px;color:{c["accent"]};font-weight:700;margin:0 0 16px;">{feat_price}</p>
{_cta_button("Jetzt entdecken", feat_url, design)}
</div>

{_section_divider(design)}

<!-- Content -->
{f'<div style="padding:24px 40px;"><p style="font-size:15px;color:{c["textLight"]};line-height:1.7;">{content[:500]}</p></div>' if content else ''}

{_product_grid_html([], design)}
"""
    subject = f"Empfohlen für dich: {topic_name} | {company}"
    preview = f"Unsere Top-Empfehlungen passend zu {topic_name}"
    return subject, preview, _base_wrapper(design, subject, preview, body)


# ─── Template 3: FAQ Email ──────────────────────────────────────────────────

def _template_faq_email(topic, client, analysis, design, products):
    c = design["colors"]
    company = design["company"]
    topic_name = topic["name"]
    content = topic.get("content", "")

    # Parse Q&A from content
    faqs = []
    lines = [l.strip() for l in content.split("\n") if l.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#") or line.endswith("?"):
            q = line.lstrip("#").strip()
            a = lines[i + 1] if i + 1 < len(lines) and not lines[i + 1].startswith("#") and not lines[i + 1].endswith("?") else ""
            faqs.append((q, a))
            i += 2 if a else 1
        else:
            i += 1

    if not faqs:
        faqs = [
            (f"Was macht {company} besonders?", analysis.get("usp", f"Höchste Qualität und persönlicher Service.")),
            ("Wie schnell liefert ihr?", "In der Regel 2-3 Werktage innerhalb Deutschlands."),
            ("Kann ich Produkte zurückgeben?", "Ja, 30 Tage Rückgaberecht — unkompliziert und kostenlos."),
        ]

    faq_html = ""
    for q, a in faqs[:5]:
        faq_html += f"""<div style="margin-bottom:20px;padding:20px;background:{c['background']};border-radius:8px;">
<h3 style="font-family:{design['headingFont']};font-size:17px;color:{c['primary']};margin:0 0 8px;">{q}</h3>
<p style="font-size:14px;color:{c['textLight']};margin:0;line-height:1.7;">{a}</p>
</div>"""

    body = f"""
<!-- Hero -->
<div style="padding:40px 40px 16px;">
<p style="font-size:13px;text-transform:uppercase;letter-spacing:2px;color:{c['accent']};margin:0 0 8px;font-weight:600;">Häufige Fragen</p>
<h2 style="font-family:{design['headingFont']};font-size:28px;color:{c['primary']};margin:0 0 16px;line-height:1.2;">{topic_name}</h2>
<p style="font-size:16px;color:{c['textLight']};margin:0;line-height:1.7;">Die wichtigsten Antworten auf einen Blick.</p>
</div>

<!-- FAQ Items -->
<div style="padding:16px 40px 32px;">
{faq_html}
</div>

<div style="padding:0 40px 8px;text-align:center;">
<p style="font-size:15px;color:{c['text']};">Noch Fragen? Schreib uns jederzeit!</p>
</div>
{_cta_button("Kontakt aufnehmen", design['website'], design)}

{_section_divider(design)}
{_product_grid_html(products, design)}
"""
    subject = f"Deine Fragen beantwortet: {topic_name} | {company}"
    preview = f"Die häufigsten Fragen rund um {topic_name}"
    return subject, preview, _base_wrapper(design, subject, preview, body)


# ─── Template 4: Show the Future ────────────────────────────────────────────

def _template_show_the_future(topic, client, analysis, design, products):
    c = design["colors"]
    company = design["company"]
    topic_name = topic["name"]
    content = topic.get("content", "")

    # Vision content
    vision_text = content[:600] if content else f"Stell dir vor, du startest jeden Tag mit dem guten Gefühl, die richtige Wahl getroffen zu haben. Mit {company} ist das keine Zukunftsmusik — sondern Realität."

    # Build timeline / steps
    steps = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith(("1.", "2.", "3.", "•")):
            steps.append(line.lstrip("0123456789.•").strip())
    if not steps:
        steps = ["Entdecke Produkte, die wirklich zu dir passen", "Erlebe den Unterschied in deinem Alltag", "Werde Teil einer Community, die Wert auf Qualität legt"]

    steps_html = ""
    for i, step in enumerate(steps[:4], 1):
        steps_html += f"""<tr>
<td style="width:48px;padding:12px 0;vertical-align:top;text-align:center;">
<div style="width:36px;height:36px;background:{c['accent']};color:#FFF;border-radius:50%;font-family:{design['headingFont']};font-size:18px;line-height:36px;text-align:center;display:inline-block;">{i}</div>
</td>
<td style="padding:12px 0 12px 12px;font-size:15px;color:{c['text']};line-height:1.6;">{step}</td>
</tr>"""

    body = f"""
<!-- Hero with gradient feel -->
<div style="padding:48px 40px 24px;background:linear-gradient(180deg,{c['background']} 0%,{c['surface']} 100%);">
<p style="font-size:13px;text-transform:uppercase;letter-spacing:2px;color:{c['accent']};margin:0 0 8px;font-weight:600;">Deine Zukunft mit {company}</p>
<h2 style="font-family:{design['headingFont']};font-size:30px;color:{c['primary']};margin:0 0 20px;line-height:1.2;">{topic_name}</h2>
<p style="font-size:16px;color:{c['textLight']};margin:0;line-height:1.8;">{vision_text[:300]}</p>
</div>

<!-- Steps -->
<div style="padding:24px 40px 32px;">
<h3 style="font-family:{design['headingFont']};font-size:20px;color:{c['primary']};margin:0 0 16px;">So sieht dein Weg aus:</h3>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
{steps_html}
</table>
</div>

{_cta_button("Zukunft starten", design['website'], design)}
{_section_divider(design)}
{_product_grid_html(products, design)}
"""
    subject = f"Stell dir vor: {topic_name} | {company}"
    preview = f"So sieht deine Zukunft mit {company} aus"
    return subject, preview, _base_wrapper(design, subject, preview, body)


# ─── Template Router ─────────────────────────────────────────────────────────

TEMPLATE_FUNCTIONS = {
    "us_vs_them": _template_us_vs_them,
    "recommended_products": _template_recommended_products,
    "faq_email": _template_faq_email,
    "show_the_future": _template_show_the_future,
}

# Ordered fallback cycle for topics without explicit type
TEMPLATE_CYCLE = ["us_vs_them", "recommended_products", "faq_email", "show_the_future"]


def _resolve_template(topic, index=0):
    """Determine which template to use based on Notion Email Type or cycle."""
    for t in topic.get("types", []):
        key = TEMPLATE_MAP.get(t)
        if key:
            return key
    return TEMPLATE_CYCLE[index % len(TEMPLATE_CYCLE)]


def generate_email(topic, client, analysis, index=0):
    """Main entry point: generates subject, preview, and full HTML for a topic."""
    design = _get_design(client, analysis)
    products = _get_products(client, analysis)
    template_key = _resolve_template(topic, index)
    fn = TEMPLATE_FUNCTIONS[template_key]

    log(f"    🎨 Template: {template_key}")
    subject, preview, html = fn(topic, client, analysis, design, products)
    return {"subject": subject, "preview": preview, "html": html, "template": template_key}


# ═══════════════════════════════════════════════════════════════════════════════
#  KLAVIYO CAMPAIGN CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def _klaviyo_headers(key):
    return {
        "Authorization": f"Klaviyo-API-Key {key}",
        "revision": "2024-10-15",
        "Content-Type": "application/json",
    }


def _get_list_id(klaviyo_key, client):
    """Resolve the target list ID."""
    explicit = client.get("klaviyoNewsletterListId", "")
    if explicit:
        return explicit
    headers = _klaviyo_headers(klaviyo_key)
    try:
        resp = safe_request("https://a.klaviyo.com/api/lists", headers=headers)
        for l in resp.get("data", []):
            name = l["attributes"]["name"].lower()
            if any(k in name for k in ("newsletter", "main", "all")):
                return l["id"]
        if resp.get("data"):
            return resp["data"][0]["id"]
    except Exception as e:
        log(f"    ❌ List fetch failed: {e}")
    return None


def create_klaviyo_campaign(klaviyo_key, email_data, client, topic, draft_only=False):
    """Create campaign → create template → assign template to message."""
    headers = _klaviyo_headers(klaviyo_key)
    list_id = _get_list_id(klaviyo_key, client)
    if not list_id:
        return {"campaign_id": None, "status": "No list found"}

    subject = email_data["subject"]
    preview = email_data["preview"]
    html = email_data["html"]

    # Send date
    topic_date = topic.get("date", "")
    today = datetime.now().date()
    if topic_date:
        td = datetime.strptime(topic_date, "%Y-%m-%d").date()
        send_date = td if td >= today else today + timedelta(days=1)
    else:
        send_date = today + timedelta(days=1)
    send_dt = f"{send_date:%Y-%m-%d}T09:00:00.000Z"

    # Step 1: Create campaign
    campaign_data = {
        "data": {
            "type": "campaign",
            "attributes": {
                "name": subject,
                "audiences": {"included": [list_id]},
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "channel": "email",
                            "label": subject[:50],
                            "content": {
                                "subject": subject,
                                "preview_text": preview,
                                "from_email": client.get("emailFrom", "hello@adsdrop.de"),
                                "from_label": client["firmenname"],
                            },
                        },
                    }],
                },
            },
        }
    }
    if not draft_only:
        campaign_data["data"]["attributes"]["send_strategy"] = {
            "method": "static",
            "options_static": {"datetime": send_dt},
        }

    try:
        resp = safe_request("https://a.klaviyo.com/api/campaigns", method="POST", headers=headers, data=campaign_data)
        campaign_id = resp["data"]["id"]
        log(f"    ✅ Campaign: {campaign_id}")
    except Exception as e:
        log(f"    ❌ Campaign creation failed: {str(e)[:200]}")
        return {"campaign_id": None, "status": f"Error: {str(e)[:100]}"}

    # Step 2: Get message ID
    message_id = None
    try:
        rels = resp["data"].get("relationships", {}).get("campaign-messages", {}).get("data", [])
        if rels:
            message_id = rels[0]["id"]
    except:
        pass
    if not message_id:
        try:
            mr = safe_request(f"https://a.klaviyo.com/api/campaigns/{campaign_id}/relationships/campaign-messages/", headers=headers)
            if mr.get("data"):
                message_id = mr["data"][0]["id"]
        except Exception as e:
            log(f"    ⚠️ Message ID fetch failed: {e}")

    if not message_id:
        return {"campaign_id": campaign_id, "status": "No message ID", "admin_url": f"https://www.klaviyo.com/campaign/{campaign_id}/edit"}

    log(f"    📝 Message: {message_id}")

    # Step 3: Create template
    try:
        tresp = safe_request("https://a.klaviyo.com/api/templates/", method="POST", headers=headers, data={
            "data": {"type": "template", "attributes": {"name": f"{subject[:80]} - Template", "html": html, "editor_type": "CODE"}}
        })
        template_id = tresp["data"]["id"]
        log(f"    ✅ Template: {template_id}")
    except Exception as e:
        log(f"    ❌ Template creation failed: {str(e)[:200]}")
        return {"campaign_id": campaign_id, "status": "Template creation failed", "admin_url": f"https://www.klaviyo.com/campaign/{campaign_id}/edit"}

    # Step 4: Assign template to message (JSON:API format — proven working)
    try:
        safe_request("https://a.klaviyo.com/api/campaign-message-assign-template/", method="POST", headers=headers, data={
            "data": {
                "type": "campaign-message",
                "id": message_id,
                "relationships": {
                    "template": {"data": {"type": "template", "id": template_id}}
                },
            }
        })
        log(f"    ✅ Template assigned!")
    except Exception as e:
        log(f"    ⚠️ Assign with ID failed, trying without: {str(e)[:150]}")
        try:
            safe_request("https://a.klaviyo.com/api/campaign-message-assign-template/", method="POST", headers=headers, data={
                "data": {
                    "type": "campaign-message",
                    "relationships": {
                        "template": {"data": {"type": "template", "id": template_id}}
                    },
                }
            })
            log(f"    ✅ Template assigned (fallback)!")
        except Exception as e2:
            log(f"    ❌ All assign methods failed: {str(e2)[:150]}")

    status = "Draft" if draft_only else f"Scheduled {send_date} 10:00 UTC"
    return {
        "campaign_id": campaign_id,
        "template_id": template_id,
        "admin_url": f"https://www.klaviyo.com/campaign/{campaign_id}/edit",
        "status": status,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Klaviyo Newsletter v2 — Clean Templates")
    parser.add_argument("--client", help="Filter to specific client name")
    parser.add_argument("--date", help="Target date YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=14, help="Look-ahead days")
    parser.add_argument("--draft", action="store_true", help="Create drafts only")
    parser.add_argument("--no-telegram", action="store_true", help="Skip Telegram notifications")
    parser.add_argument("--dry-run", action="store_true", help="Generate HTML but don't create campaigns")
    args = parser.parse_args()

    log("=" * 60)
    log("Klaviyo Newsletter v2 — Clean Template System")
    log("=" * 60)

    # 1. Topics
    log("\n📖 Fetching topics from Notion...")
    topics = get_notion_topics(days=args.days, target_date=args.date)
    if not topics:
        msg = "📧 No topics found for the selected period."
        log(msg)
        if not args.no_telegram:
            send_telegram(msg)
        return

    log(f"\n✅ {len(topics)} topics found")

    # 2. Clients
    log("\n👥 Fetching Klaviyo clients...")
    clients = get_klaviyo_clients()
    if args.client:
        clients = [c for c in clients if args.client.lower() in c["firmenname"].lower()]
    if not clients:
        msg = f"📧 No clients found{' matching ' + args.client if args.client else ''}."
        log(msg)
        if not args.no_telegram:
            send_telegram(msg)
        return

    log(f"✅ {len(clients)} clients")
    for c in clients:
        log(f"  • {c['firmenname']}")

    # 3. Generate & Create
    log("\n✍️ Generating newsletters...")
    results = []

    for client in clients:
        log(f"\n📝 {client['firmenname']}...")
        analysis = get_website_analysis(client)

        for i, topic in enumerate(topics):
            email_data = generate_email(topic, client, analysis, index=i)
            log(f"    📧 {email_data['subject'][:60]}...")

            if args.dry_run:
                # Save HTML to file for review
                fname = f"/tmp/newsletter-{client['firmenname'].lower().replace(' ', '-')}-{i}.html"
                with open(fname, "w") as f:
                    f.write(email_data["html"])
                log(f"    💾 Saved to {fname}")
                results.append({
                    "client": client["firmenname"], "topic": topic["name"],
                    "subject": email_data["subject"], "template": email_data["template"],
                    "campaignId": None, "status": f"Dry run — saved to {fname}",
                })
                continue

            result = create_klaviyo_campaign(client["klaviyoKey"], email_data, client, topic, draft_only=args.draft)
            results.append({
                "client": client["firmenname"], "topic": topic["name"],
                "subject": email_data["subject"], "template": email_data["template"],
                "campaignId": result.get("campaign_id"),
                "templateId": result.get("template_id"),
                "status": result.get("status", "Unknown"),
                "adminUrl": result.get("admin_url"),
            })
            if result.get("campaign_id"):
                log(f"    ✅ {result['status']}")
            else:
                log(f"    ❌ {result['status']}")

    # 4. Report
    ok = len([r for r in results if r.get("campaignId")])
    fail = len([r for r in results if not r.get("campaignId") and "Dry" not in r.get("status", "")])

    report = f"""📧 *Newsletter v2 — Ergebnis*

*Themen:* {len(topics)} | *Kunden:* {len(clients)}
✅ {ok} Campaigns | ❌ {fail} Fehler"""

    for r in results:
        icon = "✅" if r.get("campaignId") else "📄" if "Dry" in r.get("status", "") else "❌"
        report += f"\n{icon} {r['client']}: {r['topic']} ({r['template']})"

    log("\n" + "=" * 60)
    log(report)
    log("=" * 60)

    if not args.no_telegram and not args.dry_run:
        send_telegram(report)

    print(json.dumps({
        "topics": len(topics), "clients": len(clients),
        "successful": ok, "failed": fail, "campaigns": results,
    }, indent=2))


if __name__ == "__main__":
    main()
