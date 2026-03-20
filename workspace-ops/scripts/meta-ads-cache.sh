#!/bin/bash
# meta-ads-cache.sh - Cache Verwaltung für Meta Ads
# Usage: meta-ads-cache [stats|clear|list|refresh]

COMMAND="${1:-stats}"
CACHE_DIR="$HOME/.openclaw/workspace/.cache/meta-ads"

mkdir -p "$CACHE_DIR"

case "$COMMAND" in
    stats)
        python3 ~/.openclaw/workspace/scripts/meta-ads-pull-cached.py cache-stats
        ;;
        
    clear)
        python3 ~/.openclaw/workspace/scripts/meta-ads-pull-cached.py cache-clear
        ;;
        
    list)
        echo "📋 Meta Ads Cache Einträge"
        echo "=========================="
        echo ""
        
        if [ -d "$CACHE_DIR" ]; then
            ls -lah "$CACHE_DIR" | tail -n +2 | awk '{print $9, $5, $6, $7, $8}'
        else
            echo "Cache-Verzeichnis leer"
        fi
        ;;
        
    refresh)
        echo "🔄 Cache-Refresh wird über die API-Calls ausgeführt"
        echo "   Nutze: meta-ads-pull-cached.py <command> --force"
        echo ""
        echo "Beispiele:"
        echo "   meta-ads-pull-cached.py campaigns --force"
        echo "   meta-ads-pull-cached.py insights --force"
        ;;
        
    *)
        echo "Meta Ads Cache Management"
        echo ""
        echo "Usage: meta-ads-cache <command>"
        echo ""
        echo "Commands:"
        echo "   stats    - Cache-Statistiken anzeigen"
        echo "   clear    - Alle gecachten Daten löschen"
        echo "   list     - Alle Cache-Dateien auflisten"
        echo "   refresh  - Hinweis für Force-Refresh"
        echo ""
        echo "Location: $CACHE_DIR"
        ;;
esac
