#!/usr/bin/env python3
import requests, json, time

API = "https://api.clickup.com/api/v2"
TOKEN = "pk_63066979_9BJKQ4PHNOE3AEJWRH3PFKEH04MFZZY1"
LIST_ID = "901507242261"
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}

created = []

def create_task(name, desc, tags):
    r = requests.post(f"{API}/list/{LIST_ID}/task", headers=HEADERS, json={
        "name": name,
        "description": desc,
        "tags": tags,
        "status": "to do"
    })
    data = r.json()
    if "id" not in data:
        print(f"ERROR creating '{name}': {data}")
        return None
    print(f"✅ Created: {name} ({data['id']})")
    created.append({"name": name, "id": data["id"]})
    return data["id"]

def add_checklist(task_id, name, items):
    r = requests.post(f"{API}/task/{task_id}/checklist", headers=HEADERS, json={"name": name})
    cl = r.json().get("checklist", {})
    cl_id = cl.get("id")
    if not cl_id:
        print(f"  ERROR checklist: {r.json()}")
        return
    for item in items:
        requests.post(f"{API}/checklist/{cl_id}/checklist_item", headers=HEADERS, json={"name": item})
    print(f"  📋 Checklist: {len(items)} items")

# ============================================================
# 1. EMAIL MARKETING TEMPLATE
# ============================================================
templates = {
    "email": [
        {
            "name": "[TEMPLATE] 📧 Kickoff & Zugänge sichern",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 1/7

Ziel: Alle Zugänge sichern und Onboarding abschließen.

⏱ Aufwand: 1-2h
👤 Verantwortlich: Deniz
📅 Due: Tag 1

✅ Quality Gate: Alle Zugänge funktionieren, Kunde ist eingewiesen.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Klaviyo API Key vom Kunden anfordern",
                "Shopify/WooCommerce Store-Zugang erhalten",
                "Klaviyo mit Shop verbinden & Sync prüfen",
                "Bestehende E-Mail-Daten exportieren/importieren",
                "Kickoff-Call durchführen (Ziele, Branding, Tone of Voice)",
                "Brand Assets sammeln (Logo, Farben, Fonts)",
                "Bestehende Flows & Campaigns dokumentieren",
                "Onboarding-Protokoll erstellen & teilen"
            ]
        },
        {
            "name": "[TEMPLATE] 🔧 Account Setup & Segmentierung",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 2/7

Ziel: Klaviyo Account vollständig einrichten und 15-20 Segmente erstellen.

⏱ Aufwand: 3-4h
👤 Verantwortlich: VA
📅 Due: Tag 2-3

✅ Quality Gate: Mindestens 15 Segmente aktiv, Tracking verifiziert.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Tracking-Setup prüfen (Klaviyo Pixel, Shopify Integration)",
                "Engagement-Segmente erstellen (30/60/90/180 Tage aktiv)",
                "Purchase-Segmente (VIP, Repeat, One-Time, Lapsed)",
                "Lifecycle-Segmente (New Subscriber, Active, At-Risk, Churned)",
                "Custom Segmente nach Produktkategorie/Interessen",
                "Suppression Lists einrichten (Bounces, Unsubscribes)",
                "UTM-Parameter & Attribution konfigurieren",
                "Segment-Dokumentation erstellen"
            ]
        },
        {
            "name": "[TEMPLATE] 🔄 Flow-Strategie & Setup",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 3/7

Ziel: Alle Core Flows aufsetzen und aktivieren.

⏱ Aufwand: 6-8h
👤 Verantwortlich: Deniz + VA
📅 Due: Tag 3-7

✅ Quality Gate: Alle 6+ Flows live, Test-Mails gesendet und geprüft.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Welcome Series (3-5 Mails) erstellen & aktivieren",
                "Abandoned Cart Flow (3 Mails + SMS optional)",
                "Browse Abandonment Flow einrichten",
                "Post-Purchase Flow (Thank You, Review Request, Cross-Sell)",
                "Win-Back Flow (60/90/120 Tage inaktiv)",
                "Sunset Flow für inaktive Subscriber",
                "Alle Flows mit Test-Profil durchlaufen lassen",
                "Flow-Performance Baseline dokumentieren"
            ]
        },
        {
            "name": "[TEMPLATE] 🎨 Template Design & Branding",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 4/7

Ziel: Brand-konforme E-Mail Templates erstellen.

⏱ Aufwand: 3-4h
👤 Verantwortlich: VA
📅 Due: Tag 5-7

✅ Quality Gate: 3+ Templates erstellt, Mobile-optimiert, Kunde approved.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Master Template mit Brand-Farben, Logo, Footer erstellen",
                "Campaign Template (Newsletter/Promo) designen",
                "Flow Template (minimalistisch, conversion-fokussiert)",
                "Mobile Responsiveness auf 3+ Geräten testen",
                "Dark Mode Kompatibilität prüfen",
                "A/B Test Template-Varianten vorbereiten",
                "Kunde Approval einholen"
            ]
        },
        {
            "name": "[TEMPLATE] 🚀 Erste Campaign Launch",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 5/7

Ziel: Erste Kampagne live senden und Baseline-Daten sammeln.

⏱ Aufwand: 2-3h
👤 Verantwortlich: Deniz
📅 Due: Tag 7-10

✅ Quality Gate: Campaign gesendet, Open Rate >20%, keine Spam-Issues.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Campaign-Strategie mit Kunde abstimmen (Angebot/Content)",
                "Subject Line + Preview Text (3 Varianten für A/B Test)",
                "E-Mail Content erstellen (Copy + Design)",
                "Segment auswählen (Engaged 90d als Start)",
                "Spam-Check durchführen (Litmus/Mail-Tester)",
                "Test-Mail an Team senden & prüfen",
                "Campaign schedulen (optimale Sendezeit)",
                "24h Post-Send Analyse dokumentieren"
            ]
        },
        {
            "name": "[TEMPLATE] 📅 Weekly Newsletter Prozess",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 6/7

Ziel: Wiederkehrenden Newsletter-Prozess etablieren.

⏱ Aufwand: 2h/Woche
👤 Verantwortlich: VA
📅 Due: Wöchentlich ab Tag 14

✅ Quality Gate: Newsletter geht pünktlich raus, Metriken werden getrackt.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Content-Plan für nächste 4 Wochen erstellen",
                "Wöchentliches Content-Briefing vom Kunden einholen",
                "Newsletter Copy + Design erstellen",
                "A/B Test Setup (Subject Line oder Content)",
                "QA: Links, Bilder, Mobile Check",
                "Senden & Performance nach 24h dokumentieren",
                "Monthly Content-Kalender updaten"
            ]
        },
        {
            "name": "[TEMPLATE] 📊 Monthly Reporting & Optimierung",
            "desc": """📋 EMAIL MARKETING TEMPLATE - Task 7/7

Ziel: Monatlichen Report erstellen und Optimierungen umsetzen.

⏱ Aufwand: 2-3h/Monat
👤 Verantwortlich: Deniz
📅 Due: Monatlich

✅ Quality Gate: Report an Kunde gesendet, 3+ Optimierungen identifiziert.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Flow-Performance Review (Open Rate, Click Rate, Revenue)",
                "Campaign-Performance Zusammenfassung",
                "List Growth & Health Analyse (Churn, Bounce Rate)",
                "Revenue Attribution Report (Klaviyo Dashboard)",
                "Top 3 Optimierungen identifizieren & priorisieren",
                "A/B Test Ergebnisse auswerten & Learnings dokumentieren",
                "Nächsten Monat planen (Campaigns, neue Flows)",
                "Report an Kunde senden & Call schedulen"
            ]
        }
    ],
    "website": [
        {
            "name": "[TEMPLATE] 📋 Projekt-Briefing & Requirements",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 1/8

Ziel: Vollständiges Briefing erstellen, Anforderungen definieren.

⏱ Aufwand: 2-3h
👤 Verantwortlich: Deniz
📅 Due: Tag 1

✅ Quality Gate: Briefing-Dokument vom Kunden freigegeben.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Kickoff-Call: Ziele, Zielgruppe, USPs besprechen",
                "Technische Anforderungen definieren (CMS, Hosting, Integrationen)",
                "Seitenstruktur & Sitemap erstellen",
                "Referenz-Websites sammeln (3-5 Beispiele)",
                "Brand Guidelines & Assets erhalten",
                "Content-Anforderungen klären (wer liefert was?)",
                "Timeline & Milestones festlegen",
                "Briefing-Dokument erstellen & Kunde Approval"
            ]
        },
        {
            "name": "[TEMPLATE] ✏️ Wireframe & UX Konzept",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 2/8

Ziel: Wireframes für alle Seiten erstellen.

⏱ Aufwand: 4-6h
👤 Verantwortlich: Deniz
📅 Due: Tag 2-4

✅ Quality Gate: Wireframes approved, User Flow logisch.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "User Journey & Conversion-Pfad definieren",
                "Wireframe Homepage erstellen",
                "Wireframe Unterseiten (About, Services, Kontakt)",
                "Wireframe Landingpage (Hero, Benefits, Social Proof, CTA)",
                "Mobile-First Wireframe erstellen",
                "CTA-Strategie & Platzierung definieren",
                "Feedback-Runde mit Kunde",
                "Wireframe finalisieren & freigeben"
            ]
        },
        {
            "name": "[TEMPLATE] 🎨 Design in Figma",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 3/8

Ziel: Pixel-perfektes Design basierend auf Wireframes.

⏱ Aufwand: 6-10h
👤 Verantwortlich: Designer/VA
📅 Due: Tag 5-10

✅ Quality Gate: Design approved, alle Breakpoints abgedeckt.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Design System aufsetzen (Farben, Typo, Spacing, Components)",
                "Desktop Design aller Seiten",
                "Tablet Breakpoint (768px)",
                "Mobile Breakpoint (375px)",
                "Hover States & Micro-Interactions definieren",
                "Bild-/Video-Platzhalter mit Specs versehen",
                "Kunde Feedback-Runde (max. 2 Revisionen)",
                "Final Design Export & Handoff an Development"
            ]
        },
        {
            "name": "[TEMPLATE] 💻 Development & Umsetzung",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 4/8

Ziel: Website/Landingpage technisch umsetzen.

⏱ Aufwand: 8-16h
👤 Verantwortlich: Developer/VA
📅 Due: Tag 10-17

✅ Quality Gate: Alle Seiten gebaut, responsive, funktional.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Staging-Umgebung aufsetzen",
                "Grundstruktur & Navigation implementieren",
                "Alle Sektionen nach Design umsetzen",
                "Responsive Anpassungen (Mobile, Tablet, Desktop)",
                "Formulare & Integrationen einrichten (CRM, E-Mail)",
                "Animationen & Interaktionen einbauen",
                "Performance-Optimierung (Bilder, Lazy Loading)",
                "Cross-Browser Testing (Chrome, Safari, Firefox)"
            ]
        },
        {
            "name": "[TEMPLATE] 📝 Content Integration",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 5/8

Ziel: Finalen Content einpflegen (Texte, Bilder, Videos).

⏱ Aufwand: 3-4h
👤 Verantwortlich: VA
📅 Due: Tag 17-19

✅ Quality Gate: Aller Content eingepflegt, keine Platzhalter mehr.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Finale Texte vom Kunden erhalten & einpflegen",
                "Bilder optimieren (WebP, richtige Größe) & einsetzen",
                "Videos einbetten (YouTube/Vimeo oder Self-Hosted)",
                "Meta-Titles & Descriptions für alle Seiten",
                "Alt-Tags für alle Bilder setzen",
                "Rechtschreibung & Grammatik-Check",
                "Legal Pages prüfen (Impressum, Datenschutz, AGB)"
            ]
        },
        {
            "name": "[TEMPLATE] 🧪 QA & Testing",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 6/8

Ziel: Vollständiger Quality Check vor Launch.

⏱ Aufwand: 2-3h
👤 Verantwortlich: Deniz
📅 Due: Tag 19-20

✅ Quality Gate: Alle Tests bestanden, PageSpeed >80, keine Bugs.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Mobile Testing auf echten Geräten (iOS + Android)",
                "PageSpeed Insights Check (Ziel: >80 Mobile, >90 Desktop)",
                "Alle Links & Buttons testen",
                "Formulare testen (Submission + E-Mail Empfang)",
                "Tracking Setup prüfen (GA4, Meta Pixel, GTM)",
                "SSL Zertifikat & HTTPS prüfen",
                "404-Seite & Redirects einrichten",
                "Browser-Kompatibilität final checken"
            ]
        },
        {
            "name": "[TEMPLATE] 🚀 Launch",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 7/8

Ziel: Website live schalten.

⏱ Aufwand: 1-2h
👤 Verantwortlich: Deniz
📅 Due: Tag 21

✅ Quality Gate: Seite live, DNS propagiert, Tracking feuert.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "DNS umstellen / Domain verbinden",
                "SSL Zertifikat aktivieren",
                "Redirects von alter Seite einrichten (301)",
                "Google Search Console einrichten & Sitemap einreichen",
                "Live-Check: Alle Seiten, Formulare, Tracking",
                "Kunde informieren & gemeinsamer Live-Check"
            ]
        },
        {
            "name": "[TEMPLATE] 📦 Handover & Dokumentation",
            "desc": """📋 WEBSITE/LANDINGPAGE TEMPLATE - Task 8/8

Ziel: Projekt sauber übergeben, Kunde befähigen.

⏱ Aufwand: 1-2h
👤 Verantwortlich: Deniz
📅 Due: Tag 22-23

✅ Quality Gate: Dokumentation vollständig, Kunde kann selbst editieren.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "CMS-Schulung für Kunde (Loom Video oder Call)",
                "Zugangsdaten-Dokument erstellen (Hosting, CMS, DNS)",
                "Backup-Strategie einrichten & dokumentieren",
                "Wartungsplan besprechen (Updates, Security)",
                "Projekt-Dokumentation finalisieren",
                "Feedback vom Kunden einholen",
                "Projekt in ClickUp als abgeschlossen markieren"
            ]
        }
    ],
    "cold-mail": [
        {
            "name": "[TEMPLATE] 🌐 Domain & Inbox Setup",
            "desc": """📋 COLD MAILING TEMPLATE - Task 1/6

Ziel: Domains kaufen, DNS konfigurieren, Inboxen aufwärmen.

⏱ Aufwand: 2-3h
👤 Verantwortlich: VA
📅 Due: Tag 1 (+ 14 Tage Warmup)

✅ Quality Gate: Domains live, SPF/DKIM/DMARC korrekt, Warmup gestartet.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "3-5 ähnliche Domains kaufen (z.B. firma-team.com, getfirma.com)",
                "Google Workspace Accounts einrichten (2 Inboxen pro Domain)",
                "SPF Record konfigurieren",
                "DKIM Record konfigurieren",
                "DMARC Record konfigurieren",
                "Custom Tracking Domain in Instantly einrichten",
                "Warmup in Instantly aktivieren (min. 14 Tage)",
                "Deliverability Test nach 7 Tagen Warmup"
            ]
        },
        {
            "name": "[TEMPLATE] 🔍 Lead List Preparation",
            "desc": """📋 COLD MAILING TEMPLATE - Task 2/6

Ziel: Qualifizierte Lead-Liste mit 500-1000 Kontakten erstellen.

⏱ Aufwand: 3-5h
👤 Verantwortlich: VA
📅 Due: Tag 1-5 (parallel zum Warmup)

✅ Quality Gate: 500+ verifizierte Leads, Bounce-Rate <3%.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "ICP (Ideal Customer Profile) mit Kunde definieren",
                "Apollo.io / LinkedIn Sales Nav Filter erstellen",
                "Lead-Liste exportieren (Name, Title, Company, Email)",
                "E-Mail Verification durchführen (ZeroBounce/NeverBounce)",
                "Catch-All & Risky Emails entfernen",
                "Liste in Instantly importieren & Tags setzen",
                "Duplikate & bestehende Kunden ausschließen"
            ]
        },
        {
            "name": "[TEMPLATE] ✍️ Sequenz & Copy Writing",
            "desc": """📋 COLD MAILING TEMPLATE - Task 3/6

Ziel: 3-4 E-Mail Sequenz mit personalisierten Varianten schreiben.

⏱ Aufwand: 3-4h
👤 Verantwortlich: Deniz
📅 Due: Tag 5-8

✅ Quality Gate: 3+ Sequenz-Varianten fertig, Spintax eingebaut, Kunde approved.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Value Proposition & Offer klar definieren",
                "E-Mail 1: Initial Outreach (Problem → Lösung → CTA)",
                "E-Mail 2: Follow-Up (Social Proof / Case Study)",
                "E-Mail 3: Breakup Mail (letzte Chance, FOMO)",
                "Spintax für Subject Lines einbauen (3+ Varianten)",
                "Personalisierung ({{firstName}}, {{company}}, {{custom}})",
                "Spam-Wörter Check & Compliance prüfen",
                "Kunde Approval für Copy einholen"
            ]
        },
        {
            "name": "[TEMPLATE] 🚀 Campaign Launch in Instantly",
            "desc": """📋 COLD MAILING TEMPLATE - Task 4/6

Ziel: Kampagne in Instantly live schalten.

⏱ Aufwand: 1-2h
👤 Verantwortlich: Deniz
📅 Due: Tag 14 (nach Warmup)

✅ Quality Gate: Campaign läuft, erste Mails gehen raus, keine Bounces.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Sequenz in Instantly anlegen & Leads zuweisen",
                "Sending Schedule konfigurieren (Mo-Fr, 8-17 Uhr)",
                "Daily Sending Limit setzen (30-50/Inbox/Tag)",
                "A/B Test für Subject Lines aktivieren",
                "Warmup-Status prüfen (Inbox Score >90)",
                "Test-Run mit 10-20 Leads starten",
                "24h Monitoring: Bounces, Opens, Replies checken"
            ]
        },
        {
            "name": "[TEMPLATE] 💬 Reply Management Setup",
            "desc": """📋 COLD MAILING TEMPLATE - Task 5/6

Ziel: Reply-Handling Prozess einrichten.

⏱ Aufwand: 1-2h
👤 Verantwortlich: Deniz
📅 Due: Tag 15-16

✅ Quality Gate: Reply-Prozess definiert, Templates für Antworten bereit.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Unified Inbox in Instantly einrichten",
                "Reply Templates erstellen (Interested, Meeting Book, Not Now)",
                "Calendly/Cal.com Link für Meeting-Buchung einrichten",
                "Positive Reply → CRM/Pipeline Workflow definieren",
                "Negative Reply → Auto-Unsubscribe einrichten",
                "SLA definieren: Max. 2h Reply-Zeit während Business Hours",
                "Tägliche Reply-Check Routine festlegen"
            ]
        },
        {
            "name": "[TEMPLATE] 📈 Weekly Optimization",
            "desc": """📋 COLD MAILING TEMPLATE - Task 6/6

Ziel: Wöchentliche Optimierung der Kampagne.

⏱ Aufwand: 1-2h/Woche
👤 Verantwortlich: Deniz
📅 Due: Wöchentlich ab Tag 21

✅ Quality Gate: KPIs getrackt, Optimierungen umgesetzt, Report an Kunde.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Open Rate analysieren (Ziel: >50%)",
                "Reply Rate analysieren (Ziel: >3-5%)",
                "Bounce Rate prüfen (<3%)",
                "Underperforming Sequenzen pausieren/optimieren",
                "Neue Lead-Listen nachfüllen (500+/Woche)",
                "A/B Test Ergebnisse auswerten & Winner skalieren",
                "Weekly Report an Kunde senden",
                "Neue Sequenz-Varianten testen"
            ]
        }
    ],
    "content-ugc": [
        {
            "name": "[TEMPLATE] 🎬 UGC Content Batch",
            "desc": """📋 CONTENT TEMPLATE - UGC Batch

Ziel: 5-10 UGC Videos produzieren lassen.

⏱ Aufwand: 4-6h (verteilt über 1-2 Wochen)
👤 Verantwortlich: Deniz + VA

✅ Quality Gate: Alle Videos in finaler Qualität, verschiedene Hooks, ready for upload.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Performance-Analyse: Top Hooks & Angles identifizieren",
                "5-10 Hook-Varianten schreiben (Pattern Interrupt, Question, Bold Claim)",
                "Creator-Briefing erstellen (Script, Do's & Don'ts, Brand Voice)",
                "Creator aus Pool auswählen & briefen",
                "Raw Footage erhalten & Quality Check",
                "Editing: Hooks, Captions, CTA, Sound",
                "Final Review & Kunde Approval",
                "In Creative Pipeline uploaden & taggen"
            ]
        },
        {
            "name": "[TEMPLATE] 🖼️ Static Content Batch",
            "desc": """📋 CONTENT TEMPLATE - Static Batch

Ziel: 8-12 Static Ad Creatives erstellen.

⏱ Aufwand: 3-4h
👤 Verantwortlich: VA

✅ Quality Gate: Alle Formate exportiert, verschiedene Angles getestet.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Performance-Analyse: Welche Angles/Designs performen?",
                "3-4 neue Angles/Konzepte definieren",
                "Design erstellen (Canva/Figma) in allen Formaten (1:1, 4:5, 9:16)",
                "Varianten pro Angle (verschiedene Headlines, CTAs)",
                "Brand Compliance Check",
                "Export in korrekten Formaten & Größen",
                "In Creative Pipeline uploaden & taggen"
            ]
        },
        {
            "name": "[TEMPLATE] 🎥 VSL Video Content",
            "desc": """📋 CONTENT TEMPLATE - VSL (Video Sales Letter)

Ziel: 1-2 VSL Videos produzieren.

⏱ Aufwand: 5-8h
👤 Verantwortlich: Deniz

✅ Quality Gate: VSL fertig, verschiedene Hook-Varianten geschnitten, ready for test.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "VSL Script schreiben (Problem → Agitate → Solution → Proof → CTA)",
                "Voiceover aufnehmen oder AI-Voice generieren",
                "B-Roll & Visual Assets sammeln",
                "Video Editing (Captions, Transitions, Branding)",
                "3-5 verschiedene Hook-Varianten schneiden",
                "Thumbnail/Preview Image erstellen",
                "Final Review & Export in allen Formaten",
                "In Creative Pipeline uploaden & taggen"
            ]
        },
        {
            "name": "[TEMPLATE] 🔄 Mix Content Sprint",
            "desc": """📋 CONTENT TEMPLATE - Mix Content Sprint

Ziel: Gemischtes Content-Paket erstellen (2-3 Static + 1-2 UGC + optional VSL).

⏱ Aufwand: 6-10h (über 1 Woche)
👤 Verantwortlich: Deniz + VA

✅ Quality Gate: Alle Creatives fertig, diverser Content-Mix für Testing.

💡 Nutzung: Diesen Task kopieren und in Kunden-Projekt verschieben.""",
            "checklist": [
                "Performance Check: Welche Creative Types performen am besten?",
                "Content-Mix festlegen (z.B. 3 Static, 2 UGC, 1 VSL)",
                "Static Creatives designen (siehe Static Batch Template)",
                "UGC Briefings erstellen & an Creator senden",
                "VSL Script & Produktion (falls im Mix)",
                "Alle Creatives in finaler Qualität sammeln",
                "Batch-Upload in Creative Pipeline mit korrektem Tagging",
                "Testing-Plan erstellen (welches Creative wann testen)"
            ]
        }
    ]
}

tag_map = {
    "email": ["template", "email-marketing", "workflow"],
    "website": ["template", "website", "workflow"],
    "cold-mail": ["template", "cold-mail", "workflow"],
    "content-ugc": ["template", "content", "workflow"]
}

for category, tasks in templates.items():
    print(f"\n{'='*50}")
    print(f"Creating {category.upper()} templates...")
    print(f"{'='*50}")
    for task in tasks:
        task_id = create_task(task["name"], task["desc"], tag_map[category])
        if task_id:
            add_checklist(task_id, "Checklist", task["checklist"])
        time.sleep(0.3)

print(f"\n\n✅ DONE! Created {len(created)} tasks total.")
for c in created:
    print(f"  - {c['name']} ({c['id']})")
