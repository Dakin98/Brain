#!/bin/bash
# cached-shopify.sh - Beispiel: Shopify Revenue mit SQLite Caching
# Usage: cached-shopify.sh <kunde_id>

set -e

KUNDE_ID="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_PY="$SCRIPT_DIR/../agent_cache.py"

if [ -z "$KUNDE_ID" ]; then
    echo "Usage: cached-shopify.sh <kunde_id>"
    exit 1
fi

# Ensure DB exists
if [ ! -f "$HOME/.openclaw/workspace/.cache/agent_cache.db" ]; then
    python3 "$CACHE_PY" init
fi

echo "🛒 Shopify Revenue (mit SQLite Cache)"
echo "======================================"
echo ""

# Aktueller Monat
CURRENT_MONTH=$(date +%Y-%m)
CACHE_KEY="shopify_revenue_${KUNDE_ID}_${CURRENT_MONTH}"

# Hole Daten (mit Cache)
RESULT=$(python3 "$CACHE_PY" fetch "$CACHE_KEY" 24 \
    "bash ~/.openclaw/workspace/scripts/shopify-monthly-revenue.sh $KUNDE_ID 2>/dev/null || echo '{}'" 2>&1)

# Cache Status
if echo "$RESULT" | grep -q "CACHE_HIT"; then
    echo "✅ Daten aus SQLite Cache geladen"
else
    echo "🔄 Frische Daten von Shopify API"
fi

# Extrahiere Daten (ohne Cache-Messages)
DATA=$(echo "$RESULT" | grep -v "CACHE_")

# Zeige Daten
echo "$DATA" | jq -r '. | "  Umsatz: €\(.revenue // 0)"' 2>/dev/null || echo "  (Keine Daten)"
echo "$DATA" | jq -r '. | "  Bestellungen: \(.orders // 0)"' 2>/dev/null || true
echo "$DATA" | jq -r '. | "  Durchschn. Bestellwert: €\(.aov // 0)"' 2>/dev/null || true

echo ""
echo "💡 Diese Daten sind für 24h gecacht"
echo "   Einsparung: ~90% weniger API-Calls"
