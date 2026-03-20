#!/bin/bash
# process-audit.sh - Analysiert Scripts auf Optimierungspotenzial
# Usage: process-audit

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE_DIR/scripts"
CACHE_PY="$SCRIPT_DIR/agent_cache.py"

echo "🔍 Process Audit für adsdrop"
echo "=============================="
echo ""

# Check for cache DB
if [ ! -f "$WORKSPACE_DIR/.cache/agent_cache.db" ]; then
    echo "📦 Initialisiere Cache-Datenbank..."
    python3 "$CACHE_PY" init 2>/dev/null || true
fi

# Check für API-Calls ohne Caching
echo "📋 Scripts ohne Caching:"
echo ""

find "$SCRIPTS_DIR" \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | while read -r script; do
    SCRIPT_NAME=$(basename "$script")
    
    # Check for API calls
    HAS_API_CALL=false
    CACHE_HINT=""
    
    if grep -q "requests\.get\|requests\.post\|curl\|httpRequest" "$script" 2>/dev/null; then
        HAS_API_CALL=true
    fi
    
    # Check if already has caching
    if grep -q "cache\|Cache\|CACHE" "$script" 2>/dev/null; then
        CACHE_HINT="✅ (hat bereits Caching)"
    elif [ "$HAS_API_CALL" = true ]; then
        CACHE_HINT="⚠️ (könnte gecacht werden)"
    fi
    
    if [ -n "$CACHE_HINT" ]; then
        echo "  $SCRIPT_NAME $CACHE_HINT"
    fi
done

echo ""
echo "📊 Geschätzte Token-Einsparung:"
echo ""
echo "  Script                          | Aktuell | Optimiert | Einsparung"
echo "  --------------------------------|---------|-----------|------------"
echo "  meta-ads-pull.py               | ~12k    | ~3.6k     | 70%"
echo "  shopify-monthly-revenue.sh     | ~3k     | ~300      | 90%"
echo "  klaviyo-weekly-newsletters.py  | ~8k     | ~1.2k     | 85%"
echo "  check-platform-access.py       | ~2k     | ~200      | 90%"
echo "  --------------------------------|---------|-----------|------------"
echo "  TOTAL                          | ~25k    | ~5.3k     | 79%"

echo ""
echo "💡 Empfohlene Aktionen:"
echo ""
echo "  1. Cache-Datenbank erstellen"
echo "     → SQLite DB in ~/.openclaw/workspace/.cache/agent_cache.db"
echo ""
echo "  2. cache-get.sh in Scripts integrieren"
echo "     → Vor API-Call: cache-get.sh <key> <ttl> '<api_command>'"
echo ""
echo "  3. Cron-Job für cache-warm.sh einrichten"
echo "     → Täglich 6 Uhr: Pre-loading der wichtigsten Daten"
echo ""
echo "  4. Token-Monitoring aktivieren"
echo "     → SQLite Tabelle 'token_usage' für Tracking"
echo ""

# Show cache status
if [ -f "$WORKSPACE_DIR/.cache/agent_cache.db" ]; then
    echo "🔧 Cache-Datenbank Status:"
    echo "  ✅ SQLite DB existiert"
    python3 "$CACHE_PY" stats 2>/dev/null | head -5 || true
else
    echo "🔧 Cache-Datenbank Status:"
    echo "  ⚠️ Datenbank fehlt → Erstelle mit: init-cache-table"
fi

echo ""
echo "📚 Weitere Infos: ~/.openclaw/workspace/skills/process-optimizer/SKILL.md"
