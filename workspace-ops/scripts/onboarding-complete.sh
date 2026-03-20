#!/bin/bash
# Called when onboarding form is submitted
# Input: JSON via stdin with firmenname, website, email, produktbeschreibung, zielgruppe, kundenId
# Does: 1. Create Google Drive folders  2. Update Airtable with Drive links

set -e

INPUT=$(cat)
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
WEBSITE=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('website',''))")
KUNDEN_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('kundenId',''))")

echo "🏗️ Creating Drive structure for: $FIRMENNAME" >&2

# Create Drive folders
DRIVE_RESULT=$(bash /Users/denizakin/.openclaw/workspace/scripts/create-client-drive.sh "$FIRMENNAME" 2>/dev/null)

ROOT_LINK=$(echo "$DRIVE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['rootLink'])")
CREATIVES_LINK=$(echo "$DRIVE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['creativesLink'])")

echo "✅ Drive: $ROOT_LINK" >&2
echo "✅ Creatives Upload: $CREATIVES_LINK" >&2

# Update Airtable Kunde with Drive links
MATON_KEY="t1xQq0wltj1AZvDRA23Qvm6c-mIy6P6j_HyCC-AmwdO9E0ks6BYxPpPtOD_lXKJXB6m2xp5wa0h4YAU0fslNEL7YnBzJqjtzB1JyhVemRA"

curl -g -s -X PATCH "https://gateway.maton.ai/airtable/v0/appbGhxy9I18oIS8E/Kunden" \
  -H "Authorization: Bearer $MATON_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"records\": [{\"id\": \"$KUNDEN_ID\", \"fields\": {\"Google Drive\": \"$ROOT_LINK\", \"Creatives Upload\": \"$CREATIVES_LINK\"}}]}" > /dev/null

echo "✅ Airtable updated with Drive links" >&2

# Output result
echo "$DRIVE_RESULT"
