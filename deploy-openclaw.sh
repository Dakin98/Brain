#!/bin/bash
# Deploy OpenClaw auf clawd.adsdrop.de
# Ausführen auf dem Server: ./deploy-openclaw.sh

set -e

echo "🚀 Deploying OpenClaw..."

# 1. Ordner erstellen
mkdir -p /opt/openclaw
cd /opt/openclaw

# 2. Config kopieren (Token muss angepasst sein!)
if [ ! -f config.yaml ]; then
    echo "⚠️  Bitte config.yaml erstellen und Token einfügen!"
    echo "   Template: config.yaml.example"
    exit 1
fi

# 3. Data-Verzeichnis erstellen
mkdir -p data/memory data/skills

# 4. Alten Container stoppen (falls vorhanden)
docker stop openclaw 2>/dev/null || true
docker rm openclaw 2>/dev/null || true

# 5. Neuestes Image pullen
docker pull clawd/openclaw:latest

# 6. Container starten
docker run -d \
  --name openclaw \
  --restart unless-stopped \
  -p 3000:3000 \
  -v /opt/openclaw/data:/data \
  -v /opt/openclaw/config.yaml:/app/config.yaml:ro \
  -e OPENCLAW_DATA_DIR=/data \
  -e NODE_ENV=production \
  clawd/openclaw:latest

echo "✅ OpenClaw läuft!"
echo "   Status: docker logs -f openclaw"
echo "   Web: https://clawd.adsdrop.de"
