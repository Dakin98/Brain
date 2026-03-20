#!/bin/bash
# cache-warm.sh - Pre-load häufig genutzte Daten in SQLite
# Usage: cache-warm.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_PY="$SCRIPT_DIR/agent_cache.py"

echo "🔄 Warming cache for adsdrop workflows..."
echo ""

# Ensure cache DB exists
if [ ! -f "$HOME/.openclaw/workspace/.cache/agent_cache.db" ]; then
    echo "📦 Initializing cache database..."
    python3 "$CACHE_PY" init
    echo ""
fi

# Meta Ads Daten (24h TTL)
echo "📊 Caching Meta Ads campaigns..."
if [ -f ~/.openclaw/workspace/scripts/meta-ads-pull.py ]; then
    python3 "$CACHE_PY" fetch "meta_ads_campaigns_$(date +%Y-%m-%d)" 24 \
        "cd ~/.openclaw/workspace && python3 scripts/meta-ads-pull.py campaigns 2>/dev/null || echo '{}'" \
        2>/dev/null || echo "  ⚠️ Meta Ads cache failed"
fi

# Shopify Umsätze aktueller Monat (24h TTL)
echo "🛒 Caching Shopify revenue..."
if [ -f ~/.openclaw/workspace/scripts/shopify-monthly-revenue.sh ]; then
    CURRENT_MONTH=$(date +%Y-%m)
    python3 "$CACHE_PY" fetch "shopify_revenue_$CURRENT_MONTH" 24 \
        "cd ~/.openclaw/workspace && bash scripts/shopify-monthly-revenue.sh 2>/dev/null || echo '{}'" \
        2>/dev/null || echo "  ⚠️ Shopify cache failed"
fi

# Klaviyo Segmente (7 Tage = 168h TTL)
echo "📧 Caching Klaviyo segments..."
python3 "$CACHE_PY" fetch "klaviyo_segments" 168 \
    "echo '[]'" 2>/dev/null || echo "  ⚠️ Klaviyo cache failed"

# Platform Access Status (12h TTL)
echo "🔑 Caching platform access status..."
if [ -f ~/.openclaw/workspace/scripts/check-platform-access.py ]; then
    python3 "$CACHE_PY" fetch "platform_access_$(date +%Y-%m-%d)" 12 \
        "cd ~/.openclaw/workspace && python3 scripts/check-platform-access.py 2>/dev/null || echo '{}'" \
        2>/dev/null || echo "  ⚠️ Platform access cache failed"
fi

echo ""
echo "✅ Cache warming complete!"
echo ""

# Show stats
echo "📊 Current cache stats:"
python3 "$CACHE_PY" stats 2>/dev/null || true
echo ""
echo "Next steps:"
echo "  - Scripts können jetzt auf Cache zugreifen"
echo "  - Cron-Job: 0 6 * * * $(realpath "$0")"
