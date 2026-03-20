#!/bin/bash
# Send welcome email after closing
# Input: JSON via stdin with fields: firmenname, ansprechpartner, email
# Sends welcome mail with onboarding form link

set -e
ACCOUNT="deniz@adsdrop.de"
ONBOARDING_URL="https://n8n.adsdrop.de/form/0a71aaea-c66e-45df-a94c-bb7f0ff1e787"

INPUT=$(cat)
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
ANSPRECHPARTNER=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ansprechpartner',''))")
EMAIL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('email',''))")

if [ -z "$EMAIL" ]; then
  echo '{"error": "Missing email field"}' >&2
  exit 1
fi

# Use first name if available, otherwise Firmenname
GREETING="${ANSPRECHPARTNER:-Team $FIRMENNAME}"

SUBJECT="Willkommen bei adsdrop! 🚀 Nächste Schritte für $FIRMENNAME"

BODY_HTML=$(cat <<EOF
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1a1a1a;">
  <h2 style="color: #111;">Hey ${GREETING}! 👋</h2>
  
  <p>Freut mich, dass wir zusammenarbeiten! Damit wir schnell loslegen können, brauche ich ein paar Infos von dir.</p>
  
  <h3 style="color: #333;">📋 Onboarding-Formular ausfüllen</h3>
  <p>Klick auf den Link unten und füll das Formular aus — dauert ca. 10 Minuten. Je mehr Infos, desto besser kann ich direkt loslegen:</p>
  
  <p style="text-align: center; margin: 30px 0;">
    <a href="${ONBOARDING_URL}" style="background-color: #111; color: #fff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Onboarding starten →</a>
  </p>
  
  <h3 style="color: #333;">Was ich brauche:</h3>
  <ul style="line-height: 1.8;">
    <li>Infos zu deinem Unternehmen & Produkten</li>
    <li>Zielgruppe & bisherige Marketing-Aktivitäten</li>
    <li>Zugänge zu Werbekonten (Meta, Google, TikTok)</li>
    <li>Brand Assets (Logo, Farben, Fonts)</li>
    <li>Produktbilder & Videos für Creatives</li>
  </ul>
  
  <p>Sobald ich alles habe, erstelle ich dir einen Research Brief und wir starten mit der ersten Kampagne.</p>
  
  <p>Bei Fragen einfach auf diese Mail antworten!</p>
  
  <p style="margin-top: 30px;">Beste Grüße,<br><strong>Deniz</strong><br>adsdrop</p>
</div>
EOF
)

gog gmail send \
  --to "$EMAIL" \
  --subject "$SUBJECT" \
  --body-html "$BODY_HTML" \
  --account "$ACCOUNT" \
  --force \
  --json

echo "✅ Welcome email sent to $EMAIL" >&2
