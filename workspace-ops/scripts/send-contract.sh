#!/bin/bash
# Send contract via DocuSeal after closing
# Input: JSON via stdin with fields: firmenname, ansprechpartner, email
# Creates a submission (signing request) from the Agenturvertrag template

set -e
DOCUSEAL_URL="http://82.165.169.97:38694"
DOCUSEAL_TOKEN="XFpkE1c59eGyGejPzDCo1iLhN7Yh77e8Y3ovUfj2CbW"
TEMPLATE_ID=3

INPUT=$(cat)
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
ANSPRECHPARTNER=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ansprechpartner',''))")
EMAIL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('email',''))")

if [ -z "$EMAIL" ] || [ -z "$FIRMENNAME" ]; then
  echo '{"error": "Missing email or firmenname"}' >&2
  exit 1
fi

# Create submission (signing request)
RESPONSE=$(curl -s -X POST "${DOCUSEAL_URL}/api/submissions" \
  -H "X-Auth-Token: ${DOCUSEAL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"template_id\": ${TEMPLATE_ID},
    \"send_email\": true,
    \"submitters\": [
      {
        \"role\": \"Erste Partei\",
        \"email\": \"${EMAIL}\",
        \"name\": \"${ANSPRECHPARTNER:-$FIRMENNAME}\",
        \"send_email\": true
      }
    ]
  }")

# Validate response
echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list) and len(data) > 0:
        print(json.dumps(data, indent=2))
        print('✅ Contract sent to ${EMAIL}', file=sys.stderr)
    elif 'error' in str(data):
        print(json.dumps(data, indent=2))
        print('❌ Error sending contract', file=sys.stderr)
        sys.exit(1)
    else:
        print(json.dumps(data, indent=2))
except:
    print(sys.stdin.read(), file=sys.stderr)
    sys.exit(1)
"
