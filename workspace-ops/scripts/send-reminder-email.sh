#!/bin/bash
# Send reminder email to clients who haven't completed onboarding
# Input: JSON via stdin with fields: firmenname, ansprechpartner, email, tage (days since closing)
# Gentle reminder to fill out the onboarding form

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

GREETING="${ANSPRECHPARTNER:-Team $FIRMENNAME}"

SUBJECT="Kurze Erinnerung: Onboarding für $FIRMENNAME"

BODY_HTML=$(cat <<EOF
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1a1a1a;">
  <h2 style="color: #111;">Hey ${GREETING}! 👋</h2>
  
  <p>Kurze Erinnerung — damit ich mit eurer Kampagne loslegen kann, brauche ich noch ein paar Infos von dir.</p>
  
  <p>Das Onboarding-Formular dauert nur ca. 10 Minuten:</p>
  
  <p style="text-align: center; margin: 30px 0;">
    <a href="${ONBOARDING_URL}" style="background-color: #111; color: #fff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Jetzt ausfüllen →</a>
  </p>
  
  <p>Je schneller ich die Infos habe, desto schneller können wir starten. 🚀</p>
  
  <p>Falls du Fragen hast oder Hilfe beim Ausfüllen brauchst — einfach antworten!</p>
  
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

echo "✅ Reminder email sent to $EMAIL" >&2
