#!/bin/bash
# setup.sh - Einmaliges Setup für Video Automation Agent
# Läuft auf: 82.165.169.97 (Dein Server)

echo "🎬 Video Automation Agent Setup"
echo "================================"
echo ""

# 1. System-Updates
echo "📦 System Updates..."
sudo apt update && sudo apt upgrade -y

# 2. Python 3.10+ installieren
echo "🐍 Python Setup..."
sudo apt install -y python3.10 python3.10-pip python3.10-venv

# 3. Node.js 18+ installieren (für Remotion)
echo "⬢ Node.js Setup..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 4. FFmpeg installieren
echo "🎥 FFmpeg Setup..."
sudo apt install -y ffmpeg

# 5. Projekt-Verzeichnis erstellen
echo "📁 Projektstruktur erstellen..."
mkdir -p ~/video-automation-agent
cd ~/video-automation-agent

mkdir -p {analyzer,assets/broll,assets/output,remotion/src,remotion/public/videos,agent,logs}

# 6. Python Virtual Environment
echo "🐍 Python venv..."
python3.10 -m venv venv
source venv/bin/activate

# 7. Python Dependencies
echo "📚 Python Packages installieren..."
pip install --upgrade pip
pip install whisperx
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install requests python-dotenv pyairtable

# 8. Remotion Setup
echo "⚛️ Remotion init..."
cd remotion
npx create-remotion@latest . --template ts --skip-install
npm install
npm install @remotion/transitions @remotion/media-utils

# 9. Environment Template
cd ~
cat > ~/video-automation-agent/.env.example << 'EOF'
# Pexels API (kostenlos: pexels.com/api)
PEXELS_API_KEY=your_pexels_key_here

# Pixabay API (kostenlos: pixabay.com/api/docs)
PIXABAY_API_KEY=your_pixabay_key_here

# Airtable
AIRTABLE_API_KEY=your_airtable_key
AIRTABLE_BASE_ID=appbGhxy9I18oIS8E

# OpenAI (für GPT-4 Vision, optional)
OPENAI_API_KEY=your_openai_key
EOF

echo ""
echo "✅ Setup abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "1. API Keys in .env eintragen:"
echo "   cd ~/video-automation-agent"
echo "   cp .env.example .env"
echo "   nano .env"
echo ""
echo "2. Test laufen lassen:"
echo "   source venv/bin/activate"
echo "   python analyzer/test_whisper.py"
echo ""
echo "3. Remotion dev starten:"
echo "   cd remotion"
echo "   npm run dev"
