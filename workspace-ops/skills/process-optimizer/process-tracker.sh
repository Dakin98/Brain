#!/bin/bash
# process-tracker.sh - Zeigt Token-Usage Dashboard
# Usage: process-tracker

CACHE_PY="$HOME/.openclaw/workspace/skills/process-optimizer/agent_cache.py"

echo "📊 Token Usage Dashboard"
echo "========================"
echo ""

# Check if cache DB exists
if [ ! -f "$HOME/.openclaw/workspace/.cache/agent_cache.db" ]; then
    echo "⚠️  Cache-Datenbank nicht initialisiert"
    echo "    Führe aus: init-cache-table"
    exit 1
fi

# Show estimated current usage
echo "Geschätzte Token-Usage pro Workflow:"
echo ""
printf "%-30s | %10s | %10s | %8s\n" "Workflow" "Tokens In" "Tokens Out" "Cached?"
printf "%-30s-+-%-10s-+-%-10s-+-%-8s\n" "------------------------------" "----------" "----------" "--------"
printf "%-30s | %10s | %10s | %8s\n" "Meta Ads Reporting" "~8k" "~4k" "❌"
printf "%-30s | %10s | %10s | %8s\n" "Shopify Monthly Revenue" "~2k" "~1k" "❌"
printf "%-30s | %10s | %10s | %8s\n" "Klaviyo Newsletter" "~5k" "~3k" "❌"
printf "%-30s | %10s | %10s | %8s\n" "Platform Access Check" "~1.5k" "~500" "❌"
printf "%-30s-+-%-10s-+-%-10s-+-%-8s\n" "------------------------------" "----------" "----------" "--------"
printf "%-30s | %10s | %10s | %8s\n" "TOTAL (pro Run)" "~16.5k" "~8.5k" ""
printf "%-30s | %10s | %10s | %8s\n" "TOTAL (monatlich)" "~495k" "~255k" ""
echo ""

echo "Mit Caching:"
echo ""
printf "%-30s | %10s | %10s | %8s\n" "Workflow" "Tokens In" "Tokens Out" "Cached?"
printf "%-30s-+-%-10s-+-%-10s-+-%-8s\n" "------------------------------" "----------" "----------" "--------"
printf "%-30s | %10s | %10s | %8s\n" "Meta Ads Reporting" "~2.4k" "~1.2k" "✅ 70%"
printf "%-30s | %10s | %10s | %8s\n" "Shopify Monthly Revenue" "~200" "~100" "✅ 90%"
printf "%-30s | %10s | %10s | %8s\n" "Klaviyo Newsletter" "~750" "~450" "✅ 85%"
printf "%-30s | %10s | %10s | %8s\n" "Platform Access Check" "~150" "~50" "✅ 90%"
printf "%-30s-+-%-10s-+-%-10s-+-%-8s\n" "------------------------------" "----------" "----------" "--------"
printf "%-30s | %10s | %10s | %8s\n" "TOTAL (pro Run)" "~3.5k" "~1.8k" ""
printf "%-30s | %10s | %10s | %8s\n" "TOTAL (monatlich)" "~105k" "~54k" ""
echo ""

echo "💰 Kosteneinsparung (geschätzt):"
echo "   Ohne Caching: ~$75/Monat (bei 750k tokens)"
echo "   Mit Caching:  ~$24/Monat (bei 240k tokens)"
echo "   Einsparung:   ~$51/Monat (68%)"
echo ""

# Show actual stats from SQLite
echo "📈 Aktuelle Cache-Statistiken:"
python3 "$CACHE_PY" stats 2>/dev/null || echo "  (Keine Daten verfügbar)"

echo ""
echo "🚀 Nächste Schritte:"
echo "   1. Führe 'process-audit' aus für Detail-Analyse"
echo "   2. Starte Cache-Warming: 'cache-warm.sh'"
echo "   3. Token-Usage tracken: agent_cache.py track <workflow> <in> <out>"
