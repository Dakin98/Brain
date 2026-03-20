# MEMORY.md - Brain's Long-Term Memory

## Deniz
- Performance Marketing Agentur
- Locker, duzen
- Timezone: Europe/Berlin

## Agentur-Prozesse
- Video-Schnitt
- Bildererstellung (Templates mit austauschbaren Texten + Produktfotos)
- Meta Ads Datenanalyse
- Shop-Analyse
- Kunden-Research

## Projekte
- **Bild-Template-Automatisierung** — Deniz hat viele Templates, will Text + Produktfotos automatisch austauschen
- **Agentur-Automatisierung (Feb 2026)** — Airtable als zentrales System, Onboarding-Prozess automatisieren
  - Jotform: https://form.jotform.com/230483733940356 (Onboarding-Formular, 7 Sektionen)
  - Airtable Base: `appbGhxy9I18oIS8E` (ehemals "Untitled Base" → "adsdrop Hub" umbenennen!)
  - Tabellen: Kunden, Produkt-Info, Brand Assets, Plattform-Zugänge, Projekte, Onboarding Checklist, Rechnungen, Stripe Kunden, Klaviyo Accounts
  - Alle Tabellen mit Link-Feld "Kunde" → Kunden-Tabelle verknüpft
  - E-Mail Agentur: Deniz@adsdrop.de
  - **n8n Workflows (n8n.adsdrop.de):**
    - Closing Formular (829fR1eGNdQ7QDHw): Deal erfassen → Airtable (Kunde + Rechnung + Projekt)
    - Onboarding Formular (1DyOnFYcS6uwvZs6): Kunde füllt aus → Airtable + Stripe Kunde
    - Onboarding Form URL: https://n8n.adsdrop.de/form/0a71aaea-c66e-45df-a94c-bb7f0ff1e787
    - ⚠️ n8n Webhooks: Müssen IMMER im UI Active-Toggle aus/an gemacht werden (API reicht nicht)
  - **Stripe Sandbox:** rk_test_51T1RxpFRPwAXPToL... (Test-Key, direkt via api.stripe.com)
  - **Google Drive Struktur** pro Kunde unter 1_CLIENTS (ID: 1_8oRxRfP1PHXEsGhdsfsGPLOjCopxMee):
    - [Kunde]/ → Projekte, Reports, Daten (Research/Targeting/Analytics), Kampagnen (Facebook/Google/TikTok), Creatives, VSL
    - Script: scripts/create-client-drive.sh "Firmenname"
    - Creatives-Ordner wird mit "anyone with link = writer" geteilt
  - **Cron-Job "Onboarding: Drive + Research"**: Alle 5 Min prüft neue Kunden → erstellt Drive-Ordner + Research
  - **DocuSeal** (Vertragsunterschrift): http://82.165.169.97:38694, Template ID: 1 (Agenturvertrag)
  - **E-Mail Scripts** (Gmail via gog CLI, deniz@adsdrop.de):
    - send-welcome-email.sh — Willkommen + Onboarding-Link (nach Vertragsunterschrift)
    - send-onboarding-complete-email.sh — Bestätigung + Creatives-Link (nach Formular)
    - send-reminder-email.sh — Erinnerung ans Onboarding-Formular
  - **Cron "Contract Signed Check"**: Alle 10 Min, prüft DocuSeal auf neue Unterschriften → Status Onboarding + Welcome Mail (pausiert)
  - **Cron "Onboarding: Reminder Check"**: Täglich 9 Uhr, erinnert Kunden die Formular nicht ausgefüllt haben (pausiert)
  - **Closing Flow (n8n, aktualisiert)**: Formular → Airtable → DocuSeal Vertrag senden (statt direkt Welcome Mail)
  - **Stripe Integration**: Test-Key rk_test_51T1RxpFRPwAXPToL..., Script stripe-setup-invoice.sh (Kunde anlegen + Setup-Rechnung senden)
  - **Stripe Subscription**: stripe-create-subscription.sh (Monatlicher Retainer, auto-cancel nach Laufzeit)
  - **Cron "Contract Signed Check"**: Alle 10 Min, prüft DocuSeal → Stripe Kunde + Setup-Rechnung + Subscription + Welcome Mail (pausiert)
  - **Cron "Contract Reminder Check"**: Täglich 9 Uhr, erinnert an fehlende Vertragsunterschrift (pausiert)
  - **Cron "Onboarding: Reminder Check"**: Täglich 9 Uhr, erinnert Kunden die Formular nicht ausgefüllt haben (pausiert)
  - **Cron "Stripe: Zahlungsstatus Check"**: Täglich 10 Uhr, prüft offene/überfällige Rechnungen (pausiert)
  - **Closing Flow (n8n, aktualisiert)**: Formular → Airtable (inkl. Vertragsfelder) → DocuSeal Vertrag senden + Error Handling
  - **Onboarding Flow (n8n, aktualisiert)**: Formular → Airtable + Drive + Bestätigungsmail + Status Active (Stripe entfernt, kommt via Cron)
  - **Airtable Kunden Felder**: Retainer, Provisionsmodell, Provision Wert, Vertragslaufzeit, Startdatum, Setup-Gebühr, Zahlungsweise, Stripe Customer ID, Google Drive, Creatives Upload
  - **Shopify Integration**: Kein OAuth — Token wird manuell im Onboarding-Call erstellt (Custom App im Shopify Admin). Anleitung: docs/shopify-token-anleitung.md
  - **Klaviyo Segment Automatisierung**: Script `scripts/klaviyo-setup-segments.sh` erstellt 20 Standard-Segmente (Essential + Exclusion + Advanced). Idempotent, URL-Encoding + Variable-Passing gefixt. Cron "Klaviyo: Segment Setup" (täglich 9 Uhr). Airtable-Felder: "Klaviyo API Key", "Klaviyo Segments Done"
  - **Notion Integration**: API Key in `~/.config/notion/api_key`, Page "eCom Email Calendar Kit" (DB `3465a32b`, DataSource `f973c96b`), 177 Newsletter-Themen als Jahreskalender
  - **Newsletter-Automatisierung**: Cron `dbcb229e` (Montag 9 Uhr) — Notion-Themen der Woche → Website-Analyse pro Kunde → personalisierter Newsletter-Draft → Klaviyo Campaign Draft. Script: `scripts/notion-weekly-newsletters.sh`
  - **Plattform-Onboarding**: Airtable-Felder für Meta BM/Ad Account/Pixel, Google Ads CID, GA4 Property, GTM Container + Zugangs-OK Checkboxen. Docs in `docs/onboarding-zugang-*.md`. Script: `check-platform-access.py`. Cron "Plattform-Zugangs Check" (täglich 10 Uhr)
  - **Airtable Refactor (Feb 2026)**: Kunden-Tabelle bereinigt — Stripe Subscription ID, Abo-Status, Monatlicher Betrag direkt in Kunden. Tabellen "Stripe Kunden" und "Klaviyo Accounts" entfernt (waren leer). 49 → 37 Felder.
  - **Meta Ads Reporting (Feb 2026)**: Automatisches Reporting wenn Kunde Meta Zugang gibt. Erstellt Google Sheet, pulled Campaign/Adset/Ad-Daten, monatliches Update. Scripts: `meta-ads-pull.py`, `meta-reporting-setup.sh`. Crons: Auto-Setup (stündlich), Monthly Update (1. des Monats).
  - **Klaviyo Newsletter Automatisierung (Feb 2026)**: Jeden Montag 9 Uhr — Pullt Themen aus Notion-Kalender, analysiert Client-Websites, erstellt personalisierte Newsletter-Drafts in Klaviyo für alle aktiven Kunden. 1 Woche Vorlauf zum Review. Script: `klaviyo-weekly-newsletters.py`.
  - **Telegram Bot**: @adsdrop_brainbot (Token in Config), chat_id: 6607099798
  - **ClickUp Onboarding Automatisierung (Feb 2026)**: Wenn neuer Kunde mit Services (Cold Mail/Email Marketing/Paid Ads) geonboarded wird → automatisch Folder + Listen + Tasks in ClickUp Delivery Space. Scripts: `clickup-coldmail-setup.py` (6 Tasks), `clickup-emailmarketing-setup.py` (7 Tasks), `paid_ads_onboarding.py` (15 Tasks + 5 Listen). Cronjob: **wöchentlich Montag 9:00 Uhr** (`clickup-services-cron.sh`). Airtable-Felder: `Cold Mail`, `Email Marketing`, `Paid Ads` + Status-Felder. Doku: `docs/clickup-coldmail-automation.md`
  - **Newsletter/Klaviyo Automatisierung (Feb 2026)**: Wöchentliche Newsletter-Erstellung für aktive Kunden. Ablauf: Notion-Kalender → HTML-Template → Klaviyo Campaign + ClickUp Task. Razeco: Campaign "Internationaler Frauentag" erstellt (Sende-Datum 08.03.2026). Cronjobs: Montag 9:00 (Klaviyo Campaign), Montag 9:15 (ClickUp Tasks). Benötigt Airtable-Felder: `Newsletter Service`, `Newsletter Onboarding Done`. Doku: `docs/newsletter-automation-final.md`
  - **Test-Daten aufgeräumt (Feb 2026)**: Alle Test-Kunden (3) und Test-Folder in ClickUp (6) gelöscht. Verbleibende echte Daten: Razeco UG + Intern. Logs bereinigt.
  - **System-Audit & Cleanup (25.02.2026)**:
    - Airtable bereinigt: Kontakt → Victor Haisch (victor.haisch@razeco.com), 8 Plattform-Testrecords gelöscht, Onboarding Checklist Duplikate entfernt (20→9)
    - ClickUp Onboarding für Razeco ausgeführt: Cold Mail (6), Email Marketing (7), Paid Ads (15+5+3) — Folder ID: 901514709837
    - n8n: Läuft aber 0 Workflows, wird nicht genutzt (API Key erhalten)
    - 3 Cronjobs reaktiviert: Onboarding Reminder, Plattform-Check, Stripe Check (7/19 aktiv)
    - Newsletter Engine gefixt: bestEffort delivery, Pfad korrigiert, Agent=ops
    - Content Engine: Pfad gefixt, aber Follow-Up Tasks failed (Listen-IDs prüfen)
    - paid_ads_onboarding.py Bug: braucht PYTHONPATH="/Users/denizakin/.openclaw/workspace-ops/skills/clickup/scripts"
    - clickup-services-cron.sh Bug: SCRIPT_DIR zeigt auf workspace statt workspace-ops
  - **Wissensdatenbank erstellt (Feb 2026)**: Umfassende Dokumentation aller Automatisierungen in `docs/wissensdatenbank-2026-02-24.md`. Enthält: Architektur, Workflows, Airtable Schema, Script-Übersicht, Troubleshooting.
  - **Research-Agent gestartet (Feb 2026)**: Agent recherchiert Best Practices für Agentur-Automatisierung & Project Management (4h+ Recherche). Ergebnis wird in `docs/research-agency-automation-best-practices.md` dokumentiert.
  - **Server SSH**: akin@82.165.169.97 (Plesk), kein sudo/docker-Zugang für akin User
  - **n8n Webhooks**: Production webhooks registrieren sich nicht zuverlässig über API, nur formTrigger funktioniert. Workaround: eigenständige Services statt n8n Webhooks
  - **Plattform-Onboarding** (Feb 2026): Airtable-Felder + Onboarding-Formular erweitert für Meta BM/Ad Account/Pixel, Google Ads CID, GA4 Property, GTM Container. Zugangs-Anleitungen in docs/. Check-Script: scripts/check-platform-access.py. Cron "Plattform-Zugangs Check" (täglich 10 Uhr). E-Mail Script: send-access-guide-email.sh
  - **Abrechnungsmodell**: MAX(Retainer, Provision) — keine Subscription, monatliche Einzelrechnung basierend auf Shopify-Umsatz
  - **Cron "Monatliche Abrechnung"**: Am 1. jeden Monats 8 Uhr, zieht Shopify-Umsätze, berechnet Provision vs Retainer, erstellt Stripe-Rechnung
  - **Scripts**: shopify-monthly-revenue.sh, calculate-invoice.sh
  - Nächste Schritte: n8n Webhooks im UI aktivieren, Shopify OAuth testen, Testdaten aufräumen, Live Stripe Key
  - **Content Engine (Feb 2026)** — YouTube → Shorts → LinkedIn → Newsletter Workflow mit Claude-Generierung
    - ClickUp Folder: `🎬 Content Engine` (ID: 901514665491) mit 6 Listen + SOPs in jeder Liste
      - 💡 Content Ideas (Backlog + Ideation)
      - 📺 YouTube Pipeline (Long-Form Videos)
      - 📱 Shorts/Reels Pipeline (YouTube Shorts, IG Reels, TikTok)
      - 💼 LinkedIn Pipeline (Posts + Carousels)
      - 📧 Newsletter Pipeline (Weekly Digest)
      - 📊 Distribution Tracker (Cross-Platform Publishing)
    - **SOPs direkt in ClickUp List Descriptions:** Alle 6 Listen haben detaillierte Workflows + Checklisten
    - **Template Tasks in ClickUp:**
      - 📚 SOP: Content Engine Quick Reference (Master Guide)
      - 🎯 Jede Woche: Content auswählen & generieren (mit Checklist)
      - 💡 Content Ideen Beispiele (Monat 1-2)
      - 🎬 [TEMPLATE] YouTube Video aufnehmen
      - 💼 [TEMPLATE] LinkedIn Post erstellen
    - Dokumente im Workspace:
      - SOP: `docs/sop-content-engine.md` — wöchentlicher Workflow
      - Masterplan: `docs/content-engine-masterplan.md` — Komplette Strategie
      - Content Calendar: `docs/content-engine-content-calendar.md` — 4-Wochen Plan
      - Brand Voice: `docs/content-engine-brand-voice.md` — Style Guide
    - Scripts: `scripts/content_engine_generator_v2.py` (Brand Voice), `content_engine_generator_v3.py` (+Drive), `content_engine_check_status.py`, `create-content-drive.sh`
    - **Drive Integration:** Automatische Ordnerstruktur unter `2 Intern/Content Engine/`
      - 01_RAW/ → Unkomprimierte Aufnahmen
      - 02_EDIT/ → Finale Videos & Thumbnails
      - 03_ASSETS/ → Shorts, Carousels, Newsletter Images
      - 04_ARCHIVE/ → Veröffentlichter Content
    - **Status-Workflow (Content Ideas) — Planung:**
      1. **Idea** (Grau) → Rohe Idee, Backlog
      2. **Claude Generate** (Lila) → ⭐ Automation Trigger
      3. **Done** (Grün) → Content generiert, wartet auf Recording
    - **Status-Workflow (YouTube Pipeline) — Produktion:**
      1. **To Do** → Script vorhanden, wartet
      2. **🎬 Recording Prep** (Blau) → ⭐ **Drive-Ordner wird automatisch erstellt**
      3. **Recording** (Gelb) → Du nimmst auf
      4. **Editing** (Orange) → Post-Production
      5. **Ready to Publish** (Hellgrün) → Fertig, wartet auf Sonntag
      6. **Published** (Grün) → Live
    - **Custom Fields:** Content Pillar, Target Audience, Keywords, Priority Score, Estimated Views
    - **Workflow:** Task Status "Claude Generate" → Cron (alle 5 Min) → Claude generiert mit Brand Voice → Kommentare + Follow-Up Tasks → Manuelles Review
    - **Content Pillar Strategie (40/25/20/15):**
      - Meta Ads Mastery (40%) — Tutorials, Deep-Dives
      - Case Studies (25%) — ROAS Stories, Before/After
      - Agency Life (20%) — Behind the Scenes, Workflows
      - Hot Takes (15%) — Industry Commentary, Contrarian Views
    - **Publishing Rhythm:**
      - DI 08:00 — LinkedIn Long-Form
      - MI 12:00 — Short #1
      - DO 08:00 — LinkedIn Carousel
      - DO 09:00 — Newsletter
      - FR 08:00 — LinkedIn Short/Poll
      - FR 12:00 — Short #2
      - SO 10:00 — YouTube Long-Form
      - SO 14:00 — Short #3
    - **Cronjobs:**
      - `*/5 * * * *` → `content_engine_check_status.py` (checkt Content Ideas auf "Claude Generate")
      - `*/5 * * * *` → `youtube_pipeline_monitor.py` (checkt YouTube Pipeline auf "Recording Prep" → erstellt Drive-Ordner)
    - **Generated Output pro Task:**
      - 🎬 YouTube Script (10-15 Min, mit Hook, B-Roll Plan, SEO)
      - 💼 3 LinkedIn Posts (Long-Form, Short, Carousel)
      - 📧 Newsletter Draft (Subject, Preview, Content)
      - 📱 3 Shorts Strategie (Hooks, Captions, Timestamps)
      - ✅ Follow-Up Tasks in allen Pipelines mit Due Dates
    - **Ziele (12 Monate):** 50k Views/Video, 200+ LinkedIn Follower/Monat, 35%+ Newsletter Open Rate
    - **Newsletter Tool:** ConvertKit (kit.com) — API Key: `kit_b10646280a161577ae74c62141a1faab`
    - **Integration:** Content → ConvertKit API → Newsletter senden

## Content Engine — Nächste Schritte (Offen)

### 🔧 In ClickUp manuell einrichten (vor erstem Test):
1. [ ] Status "Claude Generate" in Content Ideas erstellen (Lila)
2. [ ] Status "Done" in Content Ideas erstellen (Grün)
3. [ ] Status "🎬 Recording Prep" in YouTube Pipeline erstellen (Blau)
4. [ ] Status "Recording" in YouTube Pipeline erstellen (Gelb)
5. [ ] Status "Editing" in YouTube Pipeline erstellen (Orange)
6. [ ] Status "Ready to Publish" in YouTube Pipeline erstellen (Hellgrün)
7. [ ] Status "Published" in YouTube Pipeline erstellen (Grün)

### 🧪 Erster Test:
1. [ ] Task in Content Ideas erstellen: "5 Meta Ads Fehler die dich Geld kosten"
2. [ ] Custom Fields ausfüllen (Pillar: Meta Ads Tutorials, Audience: E-Com Brands)
3. [ ] Status auf "Claude Generate" setzen
4. [ ] 5 Minuten warten
5. [ ] Kommentare checken → Content reviewen

### 🚀 Danach:
- LinkedIn Posting Automation (Buffer API?)
- YouTube Upload Automation
- ConvertKit Newsletter Automation
- Performance Tracking Dashboard
