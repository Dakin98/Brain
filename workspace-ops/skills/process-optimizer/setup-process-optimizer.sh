#!/bin/bash
# setup-process-optimizer.sh - Richtet den Process Optimizer Skill ein
# Usage: setup-process-optimizer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$HOME/.openclaw/workspace/skills/process-optimizer"
BIN_DIR="$HOME/.local/bin"
CACHE_DIR="$HOME/.openclaw/workspace/.cache"

echo "🚀 Setup Process Optimizer Skill"
echo "================================="
echo ""

# Create directories
mkdir -p "$BIN_DIR"
mkdir -p "$CACHE_DIR"
mkdir -p "$HOME/.openclaw/workspace/logs"

# Initialize SQLite DB
echo "📦 Initialisiere SQLite Cache-Datenbank..."
python3 "$SKILL_DIR/agent_cache.py" init

# Add symlinks for CLI commands
echo "📎 Erstelle CLI-Kommandos..."

for script in "$SKILL_DIR"/*.sh; do
    SCRIPT_NAME=$(basename "$script" .sh)
    TARGET="$BIN_DIR/$SCRIPT_NAME"
    
    # Remove existing symlink if present
    if [ -L "$TARGET" ]; then
        rm "$TARGET"
    fi
    
    # Create new symlink
    ln -sf "$script" "$TARGET"
    chmod +x "$script"
    echo "  ✅ $SCRIPT_NAME"
done

# Add agent_cache.py symlink
ln -sf "$SKILL_DIR/agent_cache.py" "$BIN_DIR/agent_cache"
chmod +x "$SKILL_DIR/agent_cache.py"
echo "  ✅ agent_cache"

# Add to PATH if needed
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    echo ""
    echo "⚠️  $BIN_DIR ist nicht im PATH"
    echo "   Füge folgende Zeile zu ~/.zshrc hinzu:"
    echo "   export PATH=\"$BIN_DIR:\$PATH\""
fi

echo ""
echo "🧪 Teste Installation..."
echo ""

# Test commands
test_cmd() {
    if command -v "$1" &> /dev/null || [ -f "$BIN_DIR/$1" ]; then
        echo "  ✅ $1 verfügbar"
    else
        echo "  ⚠️  $1 nicht im PATH"
    fi
}

test_cmd "process-audit"
test_cmd "cache-get"
test_cmd "process-tracker"
test_cmd "agent_cache"

echo ""
echo "📊 SQLite Datenbank:"
python3 "$SKILL_DIR/agent_cache.py" stats 2>/dev/null | head -5 || true

echo ""
echo "📚 Verfügbare Kommandos:"
echo "  process-audit      - Analysiert Scripts auf Optimierungspotenzial"
echo "  process-tracker    - Zeigt Token-Usage Dashboard"
echo "  cache-get          - Holt gecachte Daten oder ruft API ab"
echo "  cache-warm         - Pre-load wichtige Daten in den Cache"
echo "  init-cache-table   - Erstellt SQLite Cache-Datenbank"
echo "  agent_cache        - Python CLI für Cache-Operationen"
echo ""
echo "🎯 Schnellstart:"
echo "  1. Führe 'process-audit' aus"
echo "  2. Teste Caching: 'cache-warm'"
echo "  3. Cache-Status: agent_cache stats"
echo ""
echo "📖 Dokumentation: $SKILL_DIR/SKILL.md"
