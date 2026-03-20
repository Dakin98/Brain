#!/bin/bash
# Usage: create-client-drive.sh "Firmenname"
# Creates full folder structure under 1_CLIENTS and outputs JSON with folder IDs

set -e
ACCOUNT="deniz@adsdrop.de"
CLIENTS_FOLDER="1_8oRxRfP1PHXEsGhdsfsGPLOjCopxMee"
CLIENT_NAME="$1"

if [ -z "$CLIENT_NAME" ]; then
  echo '{"error": "Usage: create-client-drive.sh \"Firmenname\""}' 
  exit 1
fi

create_folder() {
  local name="$1"
  local parent="$2"
  local result=$(gog drive mkdir "$name" --parent "$parent" --account "$ACCOUNT" --json 2>/dev/null)
  echo "$result" | python3 -c "import sys,json; print(json.load(sys.stdin)['folder']['id'])"
}

share_folder() {
  local folder_id="$1"
  # Share with "anyone with link" as writer
  gog drive share "$folder_id" --role writer --type anyone --account "$ACCOUNT" 2>/dev/null || true
}

echo "Creating folder structure for: $CLIENT_NAME" >&2

# Main client folder
ROOT_ID=$(create_folder "$CLIENT_NAME" "$CLIENTS_FOLDER")
echo "  ✅ $CLIENT_NAME ($ROOT_ID)" >&2

# Level 1
PROJEKTE_ID=$(create_folder "Projekte" "$ROOT_ID")
REPORTS_ID=$(create_folder "Reports" "$ROOT_ID")
DATEN_ID=$(create_folder "Daten" "$ROOT_ID")
KAMPAGNEN_ID=$(create_folder "Kampagnen" "$ROOT_ID")
CREATIVES_ID=$(create_folder "Creatives" "$ROOT_ID")
VSL_ID=$(create_folder "VSL" "$ROOT_ID")
echo "  ✅ Subfolders created" >&2

# Daten subfolders
RESEARCH_ID=$(create_folder "Research" "$DATEN_ID")
TARGETING_ID=$(create_folder "Targeting" "$DATEN_ID")
ANALYTICS_ID=$(create_folder "Analytics" "$DATEN_ID")
echo "  ✅ Daten subfolders" >&2

# Kampagnen subfolders
FB_ID=$(create_folder "Facebook" "$KAMPAGNEN_ID")
GOOGLE_ID=$(create_folder "Google" "$KAMPAGNEN_ID")
TIKTOK_ID=$(create_folder "TikTok" "$KAMPAGNEN_ID")
echo "  ✅ Kampagnen subfolders" >&2

# Share Creatives folder for client uploads
share_folder "$CREATIVES_ID"
echo "  ✅ Creatives shared" >&2

# Output JSON
cat << EOF
{
  "clientName": "$CLIENT_NAME",
  "rootFolder": "$ROOT_ID",
  "rootLink": "https://drive.google.com/drive/folders/$ROOT_ID",
  "creativesFolder": "$CREATIVES_ID",
  "creativesLink": "https://drive.google.com/drive/folders/$CREATIVES_ID",
  "folders": {
    "projekte": "$PROJEKTE_ID",
    "reports": "$REPORTS_ID",
    "daten": "$DATEN_ID",
    "kampagnen": "$KAMPAGNEN_ID",
    "creatives": "$CREATIVES_ID",
    "vsl": "$VSL_ID",
    "research": "$RESEARCH_ID",
    "targeting": "$TARGETING_ID",
    "analytics": "$ANALYTICS_ID",
    "facebook": "$FB_ID",
    "google": "$GOOGLE_ID",
    "tiktok": "$TIKTOK_ID"
  }
}
EOF
