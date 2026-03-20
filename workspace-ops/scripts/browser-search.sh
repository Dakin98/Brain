#!/bin/bash
# browser-search.sh - Google Search via headless Chrome
# Usage: browser-search.sh "query"

QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: browser-search.sh <query>"
    exit 1
fi

echo "🔍 Browser Search: $QUERY"
echo ""

# Note: Dies ist ein Wrapper der das browser tool nutzt
# Da browser tool nicht direkt aus bash callable ist, 
# outputten wir die URL für manuelle Nutzung

SEARCH_URL="https://www.google.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')"
echo "URL: $SEARCH_URL"
echo ""
echo "Nutze: openclaw browser open '$SEARCH_URL'"
