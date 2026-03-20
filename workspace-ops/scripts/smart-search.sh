#!/bin/bash
# smart-search.sh - Web search mit Fallback auf Browser
# Usage: smart-search.sh "query"

QUERY="$1"

echo "🔍 Suche: $QUERY"
echo ""

# Versuche zuerst web_search (schneller, günstiger)
if RESULT=$(openclaw web search "$QUERY" 2>/dev/null); then
    echo "$RESULT"
    exit 0
fi

# Fallback: Browser automation
echo "⚠️ API Rate Limit → nutze Browser Fallback..."
echo ""

# Google Search via Browser
openclaw browser open "https://www.google.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')"
openclaw browser snapshot --format text
