#!/usr/bin/env python3
"""
Klaviyo Campaign Linker - Browser Automation
Nutzt Playwright um Template automatisch mit Campaign zu verknüpfen
"""

import os
import sys
import json
import time
import asyncio
from typing import Optional

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright nicht installiert")
    print("📦 Installiere mit: pip install playwright")
    print("🔧 Dann: playwright install chromium")
    sys.exit(1)

async def link_template_to_campaign(
    campaign_id: str,
    template_name: str,
    klaviyo_email: Optional[str] = None,
    klaviyo_password: Optional[str] = None
):
    """
    Automatisiert das Template-Linking in Klaviyo
    
    Achtung: Erfordert Klaviyo Login-Credentials oder manuelles Login
    """
    
    async with async_playwright() as p:
        # Browser starten
        browser = await p.chromium.launch(headless=False)  # headless=True für unsichtbar
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        try:
            # 1. Login (falls credentials vorhanden)
            if klaviyo_email and klaviyo_password:
                print("🔐 Logging in...")
                await page.goto('https://www.klaviyo.com/login')
                await page.fill('input[name="email"]', klaviyo_email)
                await page.fill('input[name="password"]', klaviyo_password)
                await page.click('button[type="submit"]')
                await page.wait_for_load_state('networkidle')
                time.sleep(2)
            else:
                print("⚠️  Bitte manuell einloggen...")
                await page.goto('https://www.klaviyo.com/login')
                input("⏸️  Drücke ENTER nach dem Login...")
            
            # 2. Campaign Editor öffnen
            edit_url = f'https://www.klaviyo.com/campaign/{campaign_id}/edit'
            print(f"🌐 Öffne: {edit_url}")
            await page.goto(edit_url)
            await page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # 3. Auf "Edit Content" klicken
            print("🖱️  Klicke 'Edit Content'...")
            try:
                # Versuche verschiedene Selektoren
                selectors = [
                    'button:has-text("Edit Content")',
                    'a:has-text("Edit Content")',
                    '[data-testid="edit-content-button"]',
                    '.edit-content-btn'
                ]
                
                for selector in selectors:
                    try:
                        await page.click(selector, timeout=3000)
                        print(f"✅ Gefunden: {selector}")
                        break
                    except:
                        continue
            except Exception as e:
                print(f"⚠️  Konnte 'Edit Content' nicht finden: {e}")
                print("💡 Bitte manuell klicken")
                input("⏸️  Drücke ENTER nachdem du 'Edit Content' geklickt hast...")
            
            time.sleep(3)
            
            # 4. Template Browser öffnen
            print("📄 Suche 'Browse Templates'...")
            try:
                await page.click('button:has-text("Browse Templates")', timeout=5000)
                print("✅ 'Browse Templates' geklickt")
            except:
                print("⚠️  Suche alternative...")
                # Versuche anderen Weg
                try:
                    await page.click('button:has-text("Templates")')
                except:
                    pass
            
            time.sleep(2)
            
            # 5. Template suchen und auswählen
            print(f"🔍 Suche Template: '{template_name}'...")
            try:
                # Sucheingabe füllen
                await page.fill('input[placeholder*="Search"], input[placeholder*="Suchen"]', template_name)
                time.sleep(1)
                
                # Template klicken
                template_selector = f'div:has-text("{template_name}")'
                await page.click(template_selector)
                print(f"✅ Template ausgewählt")
                
                time.sleep(1)
                
                # "Use This Template" klicken
                await page.click('button:has-text("Use This Template"), button:has-text("Template verwenden")')
                print("✅ Template angewendet")
                
            except Exception as e:
                print(f"⚠️  Konnte Template nicht automatisch auswählen: {e}")
                print(f"💡 Bitte manuell das Template '{template_name}' auswählen")
                input("⏸️  Drücke ENTER wenn fertig...")
            
            time.sleep(2)
            
            # 6. Speichern
            print("💾 Speichere...")
            try:
                await page.click('button:has-text("Save"), button:has-text("Speichern")')
                print("✅ Gespeichert!")
            except:
                print("⚠️  Konnte nicht automatisch speichern")
            
            time.sleep(2)
            
            print("\n✅ FERTIG! Campaign ist jetzt mit Template verknüpft.")
            print(f"🔗 URL: {edit_url}")
            
            # Screenshot für Verifikation
            screenshot_path = f"/tmp/klaviyo_campaign_{campaign_id}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot: {screenshot_path}")
            
        except Exception as e:
            print(f"❌ Fehler: {e}")
            # Screenshot bei Fehler
            await page.screenshot(path=f"/tmp/klaviyo_error_{campaign_id}.png")
            raise
        
        finally:
            # Browser nicht schließen damit Nutzer prüfen kann
            print("\n⏳ Browser bleibt 10 Sekunden offen...")
            time.sleep(10)
            await browser.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Link Klaviyo Template to Campaign')
    parser.add_argument('--campaign-id', required=True)
    parser.add_argument('--template-name', required=True)
    parser.add_argument('--email', help='Klaviyo email (optional)')
    parser.add_argument('--password', help='Klaviyo password (optional)')
    parser.add_argument('--json-file', help='JSON file from klaviyo_campaign_creator.py')
    
    args = parser.parse_args()
    
    # Load from JSON if provided
    if args.json_file:
        with open(args.json_file) as f:
            data = json.load(f)
        campaign_id = data.get('campaign_id', args.campaign_id)
        template_name = data.get('template_name', args.template_name)
    else:
        campaign_id = args.campaign_id
        template_name = args.template_name
    
    print(f"🔗 Linking Template to Campaign")
    print(f"   Campaign: {campaign_id}")
    print(f"   Template: {template_name}")
    print()
    
    # Run async
    asyncio.run(link_template_to_campaign(
        campaign_id=campaign_id,
        template_name=template_name,
        klaviyo_email=args.email,
        klaviyo_password=args.password
    ))

if __name__ == '__main__':
    main()