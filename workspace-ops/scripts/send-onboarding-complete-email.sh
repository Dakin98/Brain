#!/bin/bash
# Send confirmation email after onboarding form is submitted
# Input: JSON via stdin with fields: firmenname, ansprechpartner, email, creativesLink
# Confirms receipt and shares Creatives upload folder

set -e
ACCOUNT="deniz@adsdrop.de"

INPUT=$(cat)
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
ANSPRECHPARTNER=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ansprechpartner',''))")
EMAIL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('email',''))")
CREATIVES_LINK=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('creativesLink',''))")

if [ -z "$EMAIL" ]; then
  echo '{"error": "Missing email field"}' >&2
  exit 1
fi

GREETING="${ANSPRECHPARTNER:-Team $FIRMENNAME}"

SUBJECT="Alles erhalten ✅ Wir starten, $FIRMENNAME!"

# Build creatives section if link available
CREATIVES_SECTION=""
if [ -n "$CREATIVES_LINK" ]; then
  CREATIVES_SECTION=$(cat <<CEOF
  <h3 style="color: #333;">📁 Creatives & Assets hochladen</h3>
  <p>Lade deine Produktbilder, Videos, Logos und alles was wir für die Creatives brauchen hier hoch:</p>
  <p style="text-align: center; margin: 25px 0;">
    <a href="${CREATIVES_LINK}" style="background-color: #111; color: #fff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">Creatives-Ordner öffnen →</a>
  </p>
CEOF
)
fi

BODY_HTML=$(cat <<EOF
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1a1a1a;">
  <h2 style="color: #111;">Perfekt, ${GREETING}! 🎉</h2>
  
  <p>Ich habe deine Infos erhalten und alles sieht gut aus. Hier ist was jetzt passiert:</p>
  
  <h3 style="color: #333;">📊 Nächste Schritte</h3>
  <ol style="line-height: 2;">
    <li><strong>Research & Analyse</strong> — Ich analysiere deinen Markt, Wettbewerber und Zielgruppe</li>
    <li><strong>Strategie</strong> — Basierend darauf erstelle ich einen Kampagnen-Plan</li>
    <li><strong>Creatives</strong> — Erste Anzeigen-Entwürfe zur Freigabe</li>
    <li><strong>Launch</strong> — Kampagnen gehen live 🚀</li>
  </ol>
  
  ${CREATIVES_SECTION}
  
  <p>Ich melde mich in den nächsten Tagen mit dem Research Brief und ersten Vorschlägen.</p>
  
  <p>Bei Fragen jederzeit antworten!</p>
  
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

echo "✅ Onboarding complete email sent to $EMAIL" >&2
