#!/bin/bash
# Send platform access guide email to a client
# Input: JSON via stdin with: firmenname, ansprechpartner, email

set -e
INPUT=$(cat)
FIRMA=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
AP=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ansprechpartner',''))")
EMAIL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('email',''))")

SUBJECT="Zugänge einrichten — ${FIRMA} x adsdrop"

BODY="<div style='font-family:sans-serif;max-width:600px;margin:0 auto;color:#333'>
<h2>Hey ${AP}! 👋</h2>

<p>Damit wir direkt für euch loslegen können, brauchen wir Zugang zu ein paar Plattformen. Dauert nur wenige Minuten pro Plattform:</p>

<h3>1️⃣ Meta (Facebook) Ads</h3>
<p>Gehe zu <b>business.facebook.com</b> → Einstellungen → Partner → Hinzufügen<br>
Wir brauchen: <b>Business Manager ID, Ad Account ID, Pixel ID</b></p>

<h3>2️⃣ Google Ads</h3>
<p>Gehe zu <b>ads.google.com</b> → Tools → Zugriff und Sicherheit → Nutzer hinzufügen: <b>deniz@adsdrop.de</b><br>
Wir brauchen: <b>Kundennummer (CID, Format: 123-456-7890)</b></p>

<h3>3️⃣ Google Analytics 4</h3>
<p>Gehe zu <b>analytics.google.com</b> → Verwaltung → Property-Zugriffssteuerung → Nutzer hinzufügen: <b>deniz@adsdrop.de</b><br>
Wir brauchen: <b>GA4 Property ID</b></p>

<h3>4️⃣ Google Tag Manager</h3>
<p>Gehe zu <b>tagmanager.google.com</b> → Verwaltung → Nutzerverwaltung → Hinzufügen: <b>deniz@adsdrop.de</b><br>
Wir brauchen: <b>Container ID (GTM-XXXXXXX)</b></p>

<h3>5️⃣ Klaviyo (falls vorhanden)</h3>
<p>Settings → API Keys → Create Private Key (Full Access)<br>
Wir brauchen: <b>Private API Key</b></p>

<hr style='border:none;border-top:1px solid #eee;margin:24px 0'>

<p>Du kannst alle Infos direkt im <b>Onboarding-Formular</b> eintragen oder uns einfach per Mail schicken.</p>

<p>Falls du Hilfe brauchst oder Fragen hast — einfach antworten! 💪</p>

<p>Beste Grüße,<br><b>Deniz</b><br>adsdrop</p>
</div>"

gog gmail send \
  --to "$EMAIL" \
  --subject "$SUBJECT" \
  --body-html "$BODY" \
  --account deniz@adsdrop.de \
  --force

echo "✅ Access guide email sent to $EMAIL"