#!/bin/bash
#
# Create Content Engine Drive Structure
# Usage: ./create-content-drive.sh "Video Title"
#

VIDEO_NAME="$1"

if [ -z "$VIDEO_NAME" ]; then
    echo "Usage: $0 \"Video Title\""
    echo "Example: $0 \"5_Meta_Ads_Fehler\""
    exit 1
fi

# Clean up video name for folder (replace spaces with underscores)
FOLDER_NAME=$(echo "$VIDEO_NAME" | tr ' ' '_' | tr -cd '[:alnum:]_-')

# Google Drive Base Path (2 Intern/Content Engine)
DRIVE_BASE="2 Intern/Content Engine"

echo "🎬 Creating Content Engine Drive Structure"
echo "=========================================="
echo "Video: $VIDEO_NAME"
echo "Folder: $FOLDER_NAME"
echo ""

# Function to create folder
create_folder() {
    local path="$1"
    echo "  📁 Creating: $path"
    # Note: This requires gdrive CLI or rclone to be set up
    # For now, we output the structure for manual creation
}

# Create structure
echo "Structure to create:"
echo ""

echo "${DRIVE_BASE}/"
echo "├── 01_RAW/"
echo "│   ├── YouTube_Recordings/"
echo "│   │   └── ${FOLDER_NAME}/"
echo "│   │       ├── Main_Take/"
echo "│   │       └── B_Roll/"
echo "│   └── B_Roll/"
echo "│       └── ${FOLDER_NAME}/"
echo "│           ├── Screen_Recordings/"
echo "│           └── Talking_Head/"
echo "├── 02_EDIT/"
echo "│   ├── Final_Videos/"
echo "│   │   └── ${FOLDER_NAME}/"
echo "│   │       ├── 4K_Master/"
echo "│   │       └── 1080p_Web/"
echo "│   └── Thumbnails/"
echo "│       └── ${FOLDER_NAME}/"
echo "│           ├── PSD_Source/"
echo "│           └── PNG_Export/"
echo "├── 03_ASSETS/"
echo "│   ├── Shorts/"
echo "│   │   └── ${FOLDER_NAME}/"
echo "│   │       ├── Short_1/"
echo "│   │       ├── Short_2/"
echo "│   │       └── Short_3/"
echo "│   ├── LinkedIn_Carousels/"
echo "│   │   └── ${FOLDER_NAME}/"
echo "│   └── Newsletter_Images/"
echo "│       └── ${FOLDER_NAME}/"
echo "└── 04_ARCHIVE/"
echo "    └── Published/"
echo "        └── ${FOLDER_NAME}/"
echo "            ├── YouTube_Link.txt"
echo "            ├── LinkedIn_Posts.txt"
echo "            └── Performance_Data/"
echo ""

# Create local folder structure for reference
LOCAL_BASE="/tmp/content_engine_template/${FOLDER_NAME}"
echo "Creating local template at: $LOCAL_BASE"

mkdir -p "${LOCAL_BASE}/01_RAW/YouTube_Recordings/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/01_RAW/B_Roll/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/02_EDIT/Final_Videos/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/02_EDIT/Thumbnails/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/03_ASSETS/Shorts/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/03_ASSETS/LinkedIn_Carousels/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/03_ASSETS/Newsletter_Images/${FOLDER_NAME}"
mkdir -p "${LOCAL_BASE}/04_ARCHIVE/Published/${FOLDER_NAME}"

# Create README file
cat > "${LOCAL_BASE}/README.txt" << EOF
CONTENT ENGINE: ${VIDEO_NAME}
================================

Recording Date: 
Publish Date: 
Status: 

QUICK LINKS:
- YouTube Script: See ClickUp Task
- LinkedIn Posts: See ClickUp Task  
- Newsletter: See ClickUp Task

FOLDER STRUCTURE:
01_RAW/         → Unkomprimierte Aufnahmen
02_EDIT/        → Finale Exports & Thumbnails
03_ASSETS/      → Shorts, Carousels, Newsletter Images
04_ARCHIVE/     → Veröffentlichter Content + Performance

NEXT STEPS:
1. [ ] RAW Aufnahmen in 01_RAW ablegen
2. [ ] Edit in 02_EDIT
3. [ ] Assets in 03_ASSETS
4. [ ] Nach Publish: Alles in 04_ARCHIVE
EOF

echo "✅ Local template created!"
echo ""
echo "📋 Next Steps:"
echo "   1. Copy this structure to Google Drive:"
echo "      ${DRIVE_BASE}/"
echo ""
echo "   2. Or use gdrive CLI to create automatically:"
echo "      gdrive mkdir \"${DRIVE_BASE}/01_RAW/YouTube_Recordings/${FOLDER_NAME}\""
echo ""

# Output the full path for automation
OUTPUT_PATH="${DRIVE_BASE}/02_EDIT/Final_Videos/${FOLDER_NAME}"
echo "OUTPUT_PATH: ${OUTPUT_PATH}"
