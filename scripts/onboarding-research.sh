#!/bin/bash
set -euo pipefail

ACCOUNT="deniz@adsdrop.de"
BASE_ID="appbGhxy9I18oIS8E"
TABLE="Kunden"
GATEWAY="https://gateway.maton.ai/airtable/v0/${BASE_ID}/${TABLE}"

echo "=== Onboarding Client Research ==="
echo "Time: $(date -u '+%Y-%m-%d %H:%M UTC')"

# Step 1: Fetch onboarding clients with Google Drive set
FILTER="AND({Status}='Onboarding',{Google Drive}!='')"
ENCODED_FILTER=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$FILTER'))")

resp=$(curl -gs -H "Authorization: Bearer $MATON_API_KEY" \
  "${GATEWAY}?filterByFormula=${ENCODED_FILTER}&maxRecords=100" 2>&1)

# Validate response
if ! echo "$resp" | jq -e '.records' > /dev/null 2>&1; then
  echo "ERROR: Airtable API returned unexpected response, skipping this run."
  echo "Raw response: $resp"
  exit 0
fi

RECORD_COUNT=$(echo "$resp" | jq '.records | length')
echo "Found $RECORD_COUNT clients with Status=Onboarding and Google Drive set."

if [ "$RECORD_COUNT" -eq 0 ]; then
  echo "No clients matched. Done."
  exit 0
fi

CREATED_DOCS=()
SKIPPED=()

# Process each client
echo "$resp" | jq -c '.records[]' | while IFS= read -r record; do
  REC_ID=$(echo "$record" | jq -r '.id')
  FIRMENNAME=$(echo "$record" | jq -r '.fields.Firmenname // empty')
  WEBSITE=$(echo "$record" | jq -r '.fields.Website // empty')
  PRODUKTBESCHREIBUNG=$(echo "$record" | jq -r '.fields.Produktbeschreibung // empty')
  ZIELGRUPPE=$(echo "$record" | jq -r '.fields.Zielgruppe // empty')
  GDRIVE_URL=$(echo "$record" | jq -r '.fields["Google Drive"] // empty')
  PRODUKT_INFO_IDS=$(echo "$record" | jq -r '.fields["Produkt-Info"] // [] | join(",")')

  if [ -z "$FIRMENNAME" ]; then
    echo "⚠️ Record $REC_ID has no Firmenname, skipping."
    continue
  fi

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Processing: $FIRMENNAME"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Extract folder ID from Google Drive URL
  FOLDER_ID=""
  if echo "$GDRIVE_URL" | grep -q "folders/"; then
    FOLDER_ID=$(echo "$GDRIVE_URL" | grep -oP 'folders/\K[^/?]+')
  elif echo "$GDRIVE_URL" | grep -q "id="; then
    FOLDER_ID=$(echo "$GDRIVE_URL" | grep -oP 'id=\K[^&]+')
  fi

  if [ -z "$FOLDER_ID" ]; then
    echo "⚠️ Could not extract folder ID from: $GDRIVE_URL"
    continue
  fi
  echo "Drive folder ID: $FOLDER_ID"

  # Find "Daten" subfolder, then "Research" inside it
  echo "Looking for Daten folder..."
  DATEN_ID=""
  DATEN_RESULT=$(gog drive ls --parent "$FOLDER_ID" --query "mimeType='application/vnd.google-apps.folder' and name='Daten'" --account "$ACCOUNT" -j --no-input 2>&1 || true)
  DATEN_ID=$(echo "$DATEN_RESULT" | jq -r '.files[0].id // empty' 2>/dev/null || true)
  
  if [ -z "$DATEN_ID" ]; then
    echo "No 'Daten' folder found. Looking for Research directly..."
    SEARCH_PARENT="$FOLDER_ID"
  else
    echo "Found Daten folder: $DATEN_ID"
    SEARCH_PARENT="$DATEN_ID"
  fi

  echo "Looking for Research folder..."
  RESEARCH_ID=""
  RESEARCH_RESULT=$(gog drive ls --parent "$SEARCH_PARENT" --query "mimeType='application/vnd.google-apps.folder' and name='Research'" --account "$ACCOUNT" -j --no-input 2>&1 || true)
  RESEARCH_ID=$(echo "$RESEARCH_RESULT" | jq -r '.files[0].id // empty' 2>/dev/null || true)

  if [ -z "$RESEARCH_ID" ]; then
    # Try searching in the main folder if we searched Daten first
    if [ "$SEARCH_PARENT" != "$FOLDER_ID" ]; then
      RESEARCH_RESULT=$(gog drive ls --parent "$FOLDER_ID" --query "mimeType='application/vnd.google-apps.folder' and name='Research'" --account "$ACCOUNT" -j --no-input 2>&1 || true)
      RESEARCH_ID=$(echo "$RESEARCH_RESULT" | jq -r '.files[0].id // empty' 2>/dev/null || true)
    fi
  fi

  if [ -z "$RESEARCH_ID" ]; then
    echo "⚠️ No Research folder found for $FIRMENNAME, skipping."
    continue
  fi
  echo "Research folder ID: $RESEARCH_ID"

  # Check if research brief already exists
  DOC_NAME="${FIRMENNAME} - Research Brief"
  echo "Checking for existing '$DOC_NAME'..."
  EXISTING=$(gog drive ls --parent "$RESEARCH_ID" --query "name='${DOC_NAME}' and trashed=false" --account "$ACCOUNT" -j --no-input 2>&1 || true)
  EXISTING_ID=$(echo "$EXISTING" | jq -r '.files[0].id // empty' 2>/dev/null || true)

  if [ -n "$EXISTING_ID" ]; then
    echo "✅ Research Brief already exists (ID: $EXISTING_ID). Skipping $FIRMENNAME."
    echo "SKIPPED:$FIRMENNAME" >> /tmp/onboarding-results.txt
    continue
  fi

  # Fetch Produkt-Info linked records if any
  PRODUKT_INFO_TEXT=""
  if [ -n "$PRODUKT_INFO_IDS" ]; then
    echo "Fetching Produkt-Info linked records..."
    IFS=',' read -ra PI_IDS <<< "$PRODUKT_INFO_IDS"
    for pi_id in "${PI_IDS[@]}"; do
      pi_resp=$(curl -gs -H "Authorization: Bearer $MATON_API_KEY" \
        "https://gateway.maton.ai/airtable/v0/${BASE_ID}/Produkt-Info/${pi_id}" 2>&1 || true)
      if echo "$pi_resp" | jq -e '.fields' > /dev/null 2>&1; then
        pi_name=$(echo "$pi_resp" | jq -r '.fields.Name // empty')
        pi_desc=$(echo "$pi_resp" | jq -r '.fields.Beschreibung // empty')
        if [ -n "$pi_name" ]; then
          PRODUKT_INFO_TEXT="${PRODUKT_INFO_TEXT}
- ${pi_name}: ${pi_desc}"
        fi
      fi
    done
  fi

  # Web research
  echo "Researching $FIRMENNAME online..."
  SEARCH_RESULTS=""
  
  # Search company
  SEARCH1=$(curl -gs "https://api.search.brave.com/res/v1/web/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${FIRMENNAME} company'))")&count=5" \
    -H "Accept: application/json" \
    -H "X-Subscription-Token: ${BRAVE_API_KEY:-}" 2>&1 || true)
  RESULTS1=$(echo "$SEARCH1" | jq -r '.web.results[]? | "- \(.title): \(.url) — \(.description // "")"' 2>/dev/null || true)

  # Search competitors
  SEARCH2=$(curl -gs "https://api.search.brave.com/res/v1/web/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${FIRMENNAME} competitors alternatives'))")&count=5" \
    -H "Accept: application/json" \
    -H "X-Subscription-Token: ${BRAVE_API_KEY:-}" 2>&1 || true)
  RESULTS2=$(echo "$SEARCH2" | jq -r '.web.results[]? | "- \(.title): \(.url) — \(.description // "")"' 2>/dev/null || true)

  # Analyze website if available
  WEBSITE_ANALYSIS=""
  if [ -n "$WEBSITE" ]; then
    echo "Analyzing website: $WEBSITE..."
    WEBSITE_CONTENT=$(curl -gs -L "$WEBSITE" -o /tmp/website.html --max-time 10 && \
      python3 -c "
import html.parser, sys
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'): self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript'): self.skip = False
    def handle_data(self, data):
        if not self.skip: self.text.append(data.strip())
p = P()
with open('/tmp/website.html') as f: p.feed(f.read())
print(' '.join(t for t in p.text if t)[:3000])
" 2>/dev/null || true)
    if [ -n "$WEBSITE_CONTENT" ]; then
      WEBSITE_ANALYSIS="$WEBSITE_CONTENT"
    fi
  fi

  # Build the research brief markdown
  echo "Creating Research Brief..."
  
  cat > /tmp/research-brief.md << DOCEOF
# ${FIRMENNAME} - Research Brief

*Erstellt am: $(date -u '+%d.%m.%Y') | Automatisch generiert*

---

## 🏢 Company Overview

**Firmenname:** ${FIRMENNAME}
**Website:** ${WEBSITE:-Nicht angegeben}

**Produktbeschreibung:**
${PRODUKTBESCHREIBUNG:-Keine Beschreibung verfügbar.}

**Zielgruppe:**
${ZIELGRUPPE:-Nicht definiert.}

${PRODUKT_INFO_TEXT:+**Produkt-Informationen:**
${PRODUKT_INFO_TEXT}
}

---

## 🎯 Market Position & USPs

*Basierend auf Web-Recherche:*

${RESULTS1:-Keine Suchergebnisse gefunden.}

${WEBSITE_ANALYSIS:+**Website-Analyse:**
${WEBSITE_ANALYSIS}
}

---

## 🏆 Competitors & Wettbewerb

*Recherche zu Wettbewerbern und Alternativen:*

${RESULTS2:-Keine Wettbewerber-Daten gefunden.}

---

## 👥 Target Audience Insights

**Definierte Zielgruppe:** ${ZIELGRUPPE:-Nicht spezifiziert}

*Empfehlung: Zielgruppe über Meta Audience Insights und Google Analytics weiter verfeinern.*

---

## 📊 Ad Strategy Recommendations

### Meta (Facebook/Instagram)
- Produktfokussierte Creatives mit klaren USPs
- Lookalike Audiences basierend auf bestehenden Kunden
- Retargeting für Website-Besucher
- A/B Testing verschiedener Ad Formate (Carousel, Video, Static)

### Google
- Brand-Keywords absichern
- Shopping Ads für Produkte (falls E-Commerce)
- Display Retargeting
- Performance Max Kampagnen testen

### TikTok
- UGC-Style Content für authentische Wirkung
- Trend-basierte Creatives
- Spark Ads mit Creator-Content
- Fokus auf jüngere Zielgruppen-Segmente

---

## 🔗 Quellen & Links

**Website:** ${WEBSITE:-N/A}
**Google Drive:** ${GDRIVE_URL}

*Dieses Dokument wird im Rahmen des Onboarding-Prozesses automatisch erstellt und sollte vom Account Manager ergänzt werden.*
DOCEOF

  # Create the doc
  CREATE_RESULT=$(gog docs create "$DOC_NAME" --parent "$RESEARCH_ID" --account "$ACCOUNT" -j --no-input 2>&1)
  DOC_ID=$(echo "$CREATE_RESULT" | jq -r '.documentId // .id // empty' 2>/dev/null || true)

  if [ -z "$DOC_ID" ]; then
    echo "⚠️ Failed to create doc for $FIRMENNAME"
    echo "Create result: $CREATE_RESULT"
    continue
  fi
  echo "Created doc: $DOC_ID"

  # Write content
  gog docs write "$DOC_ID" --file /tmp/research-brief.md --account "$ACCOUNT" --no-input 2>&1 || true
  echo "✅ Research Brief created for $FIRMENNAME (Doc ID: $DOC_ID)"
  echo "CREATED:$FIRMENNAME:$DOC_ID" >> /tmp/onboarding-results.txt

  # Small delay to avoid rate limits
  sleep 2
done

echo ""
echo "=== Summary ==="
if [ -f /tmp/onboarding-results.txt ]; then
  cat /tmp/onboarding-results.txt
  rm -f /tmp/onboarding-results.txt
else
  echo "No actions taken."
fi
echo "=== Done ==="
