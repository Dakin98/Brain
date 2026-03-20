#!/bin/bash
# cached-meta-ads.sh - Beispiel: Meta Ads mit SQLite Caching
# Usage: cached-meta-ads.sh <kunde_id>

set -e

KUNDE_ID="${1:-all}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_PY="$SCRIPT_DIR/../agent_cache.py"

echo "📊 Meta Ads Reporting (mit SQLite Cache)"
echo "========================================="
echo ""

# Ensure DB exists
if [ ! -f "$HOME/.openclaw/workspace/.cache/agent_cache.db" ]; then
    python3 "$CACHE_PY" init
fi

# Cache Key basierend auf Datum und Kunde
CACHE_KEY="meta_ads_${KUNDE_ID}_$(date +%Y-%m-%d)"

# Hole Daten (mit Cache)
RESULT=$(python3 "$CACHE_PY" fetch "$CACHE_KEY" 24 \
    "python3 ~/.openclaw/workspace/scripts/meta-ads-pull.py $KUNDE_ID 2>/dev/null || echo '{}'" 2>&1)

# Check ob aus Cache
if echo "$RESULT" | grep -q "CACHE_HIT"; then
    echo "✅ Daten aus SQLite Cache geladen"
else
    echo "🔄 Frische Daten von Meta API"
fi

# Parse und zeige Daten
echo "$RESULT" | grep -v "CACHE_" | jq -r '.campaigns[]? | "  \(.name): €\(.spend) Spend, \(.conversions) Conversions"' 2>/dev/null || echo "  (Keine Kampagnen gefunden)"

echo ""
echo "💡 Diese Daten sind für 24h gecacht"
echo "   Nächster API-Call spart ~8k Tokens!"
