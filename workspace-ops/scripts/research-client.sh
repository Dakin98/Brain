#!/bin/bash
# Usage: research-client.sh "Firmenname" "Website" "Produktbeschreibung" "Zielgruppe"
# Recherchiert den Kunden und gibt ein Research-Brief als JSON aus

FIRMENNAME="$1"
WEBSITE="$2"
PRODUKT="$3"
ZIELGRUPPE="$4"

if [ -z "$FIRMENNAME" ]; then
  echo '{"error": "Usage: research-client.sh \"Firmenname\" \"Website\" \"Produkt\" \"Zielgruppe\""}'
  exit 1
fi

# Use web_search via curl to Brave API (if available) or fallback
# For now, output structured research brief template
cat << EOF
{
  "firmenname": "$FIRMENNAME",
  "website": "$WEBSITE",
  "research": {
    "status": "pending",
    "note": "Research wird von OpenClaw Agent durchgeführt"
  }
}
EOF
