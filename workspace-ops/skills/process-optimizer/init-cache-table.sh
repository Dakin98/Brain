#!/bin/bash
# init-cache-table.sh - Initialisiert SQLite Cache-Datenbank
# Usage: init-cache-table

set -e

CACHE_PY="$HOME/.openclaw/workspace/skills/process-optimizer/agent_cache.py"
CACHE_DIR="$HOME/.openclaw/workspace/.cache"
CACHE_DB="$CACHE_DIR/agent_cache.db"

echo "🗄️ Initialisiere SQLite Cache-Datenbank..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nicht gefunden"
    exit 1
fi

# Initialize database
python3 "$CACHE_PY" init

echo ""
echo "✅ Cache-Datenbank bereit!"
echo ""
echo "📁 Location: $CACHE_DB"
echo ""
echo "Tabellen:"
echo "  • cache         - Cache-Einträge (key, data, ttl, access_count)"
echo "  • token_usage   - Token-Usage Tracking (workflow, tokens, timestamp)"
echo ""
echo "🚀 Nächste Schritte:"
echo "  1. Führe 'cache-warm.sh' aus"
echo "  2. Teste mit: agent_cache.py stats"
echo ""
echo "💡 CLI Commands:"
echo "  agent_cache.py get <key>              - Daten holen"
echo "  agent_cache.py set <key> <data> <ttl> - Daten speichern"
echo "  agent_cache.py fetch <key> <ttl> <cmd> - Holen oder fetchen"
echo "  agent_cache.py stats                  - Statistiken"
echo "  agent_cache.py list                   - Alle Einträge"
echo "  agent_cache.py clear-expired          - Aufräumen"
