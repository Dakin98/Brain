#!/bin/bash
# setup-macos.sh - Lokale Entwicklung auf MacBook

set -e

echo "🍎 Video Automation Agent - macOS Setup"
echo "========================================="
echo ""

# Check if Homebrew installed
if ! command -v brew &> /dev/null; then
    echo "🍺 Homebrew wird installiert..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew ist installiert"
fi

# 1. Python 3.10+ via Homebrew
echo ""
echo "🐍 Python 3.11 wird installiert..."
brew install python@3.11

# 2. Node.js 18+
echo ""
echo "⬢ Node.js 18 wird installiert..."
brew install node@18

# 3. FFmpeg
echo ""
echo "🎥 FFmpeg wird installiert..."
brew install ffmpeg

# 4. Projekt-Verzeichnis erstellen
echo ""
echo "📁 Projekt wird erstellt..."
PROJECT_DIR="$HOME/Developer/video-automation-agent"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

mkdir -p {analyzer,assets/broll,assets/output,remotion/src/components,remotion/public/videos,agent,logs,scripts}

# 5. Python Virtual Environment
echo ""
echo "🐍 Python Virtual Environment..."
python3.11 -m venv venv
source venv/bin/activate

# 6. Python Dependencies
echo ""
echo "📚 Python Packages werden installiert (das dauert)..."
pip install --upgrade pip

# Installiere WhisperX und Dependencies
echo "   → Installing WhisperX..."
pip install whisperx

# PyTorch für Mac (Metal GPU Support)
echo "   → Installing PyTorch (Mac Metal)..."
pip install torch torchvision torchaudio

# Weitere Dependencies
echo "   → Installing utilities..."
pip install requests python-dotenv pyairtable rich typer

echo "✅ Python Packages installiert!"

# 7. Remotion Setup
echo ""
echo "⚛️ Remotion wird initialisiert..."
cd "$PROJECT_DIR/remotion"

# package.json erstellen
cat > package.json << 'EOF'
{
  "name": "video-automation",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "remotion preview",
    "build": "remotion render src/index.tsx Video out/video.mp4",
    "upgrade": "remotion upgrade",
    "test": "tsc"
  },
  "dependencies": {
    "@remotion/cli": "latest",
    "@remotion/media-utils": "latest",
    "@remotion/transitions": "latest",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "remotion": "latest",
    "zod": "^3.21.4"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/web": "^0.0.61",
    "typescript": "^4.9.4"
  }
}
EOF

# Installiere Dependencies
echo "   → Installing npm packages..."
npm install

echo "✅ Remotion installiert!"

# 8. TypeScript Config
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020", "DOM"],
    "jsx": "react",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node"
  },
  "include": ["src/**/*"]
}
EOF

# 9. Environment Template
cd "$PROJECT_DIR"
cat > .env.example << 'EOF'
# Pexels API (kostenlos: https://www.pexels.com/api/)
PEXELS_API_KEY=your_pexels_key_here

# Pixabay API (kostenlos: https://pixabay.com/api/docs/)
PIXABAY_API_KEY=your_pixabay_key_here

# Airtable
AIRTABLE_API_KEY=your_airtable_key
AIRTABLE_BASE_ID=appbGhxy9I18oIS8E

# OpenAI (optional, für GPT-4 Vision)
OPENAI_API_KEY=your_openai_key

# Output Path
OUTPUT_DIR=./assets/output
EOF

cp .env.example .env

# 10. Kopiere Code-Dateien
echo ""
echo "📄 Kopiere Projekt-Dateien..."

# Kopiere analyzer.py
if [ -f "$HOME/.openclaw/workspace/video-automation/analyzer/analyzer.py" ]; then
    cp "$HOME/.openclaw/workspace/video-automation/analyzer/analyzer.py" "$PROJECT_DIR/analyzer/"
fi

# Kopiere Remotion files
if [ -f "$HOME/.openclaw/workspace/video-automation/remotion/src/Video.tsx" ]; then
    cp "$HOME/.openclaw/workspace/video-automation/remotion/src/"*.tsx "$PROJECT_DIR/remotion/src/"
    cp "$HOME/.openclaw/workspace/video-automation/remotion/src/components/"*.tsx "$PROJECT_DIR/remotion/src/components/"
fi

echo ""
echo "========================================="
echo "✅ Setup abgeschlossen!"
echo "========================================="
echo ""
echo "📍 Projekt-Ordner: $PROJECT_DIR"
echo ""
echo "Nächste Schritte:"
echo "1. Terminal öffnen:"
echo "   cd $PROJECT_DIR"
echo ""
echo "2. Python aktivieren:"
echo "   source venv/bin/activate"
echo ""
echo "3. API Keys eintragen:"
echo "   open .env"
echo ""
echo "4. Test-Video vorbereiten:"
echo "   Kopiere ein UGC-Video nach: $PROJECT_DIR/assets/"
echo ""
echo "5. Analyse starten:"
echo "   python analyzer/analyzer.py assets/dein-video.mp4"
echo ""
echo "6. Remotion Dev Server starten:"
echo "   cd remotion"
echo "   npm run dev"
echo ""
echo "🎉 Fertig!"
