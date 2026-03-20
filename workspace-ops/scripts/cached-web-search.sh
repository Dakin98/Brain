#!/bin/bash
# cached-web-search.sh - Web search mit Airtable Caching
# Reduziert API-Calls um ~80% bei wiederholten Queries
# Usage: cached-web-search.sh "query" [ttl_hours]

set -e

QUERY="$1"
TTL="${2:-168}"  # Default: 7 Tage
AIRTABLE_BASE="appbGhxy9I18oIS8E"
CACHE_TABLE="Web Cache"

if [ -z "$QUERY" ]; then
    echo "Usage: cached-web-search.sh <query> [ttl_hours]"
    exit 1
fi

# Generate cache key from query
CACHE_KEY=$(echo "$QUERY" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g' | cut -c1-50)

echo "🔍 Query: $QUERY" >&2
echo "🗝️  Cache Key: $CACHE_KEY" >&2

# Check Airtable Cache
if command -v gog &> /dev/null; then
    CACHED=$(gog airtable list-records "$AIRTABLE_BASE" "$CACHE_TABLE" \
        --filter="{Key}='$CACHE_KEY'" 2>/dev/null | jq -r '.[0] // empty')
    
    if [ -n "$CACHED" ]; then
        LAST_UPDATED=$(echo "$CACHED" | jq -r '.fields["Last Updated"] // empty')
        DATA=$(echo "$CACHED" | jq -r '.fields.Data // empty')
        
        if [ -n "$LAST_UPDATED" ] && [ -n "$DATA" ]; then
            # Check TTL
            LAST_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M:%S.000Z" "$LAST_UPDATED" "+%s" 2>/dev/null || date -d "$LAST_UPDATED" "+%s" 2>/dev/null || echo "0")
            NOW_EPOCH=$(date "+%s")
            TTL_SECONDS=$((TTL * 3600))
            
            if [ $((NOW_EPOCH - LAST_EPOCH)) -lt $TTL_SECONDS ]; then
                echo "✅ Cache HIT (TTL: $TTL h)" >&2
                echo "$DATA" | jq -r '.results[]? | "\(.title)\n\(.url)\n\(.description)\n---"' 2>/dev/null || echo "$DATA"
                exit 0
            else
                echo "⏰ Cache EXPIRED (update needed)" >&2
            fi
        fi
    fi
fi

echo "🌐 Cache MISS → API Call..." >&2

# API Call mit Retry-Logik
for i in 1 2 3; do
    if RESULT=$(openclaw web search "$QUERY" 2>/dev/null); then
        # Save to cache
        if command -v gog &> /dev/null; then
            RECORD_ID=$(echo "$CACHED" | jq -r '.id // empty')
            TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
            
            if [ -n "$RECORD_ID" ] && [ "$RECORD_ID" != "null" ]; then
                gog airtable update-record "$AIRTABLE_BASE" "$CACHE_TABLE" "$RECORD_ID" \
                    --data="{\"fields\":{\"Query\":\"$QUERY\",\"Data\":$(echo "$RESULT" | jq -Rs .),\"Last Updated\":\"$TIMESTAMP\",\"TTL Hours\":$TTL}}" 2>/dev/null || true
            else
                gog airtable create-record "$AIRTABLE_BASE" "$CACHE_TABLE" \
                    --data="{\"fields\":{\"Key\":\"$CACHE_KEY\",\"Query\":\"$QUERY\",\"Data\":$(echo "$RESULT" | jq -Rs .),\"Last Updated\":\"$TIMESTAMP\",\"TTL Hours\":$TTL,\"Source\":\"Brave API\"}}" 2>/dev/null || true
            fi
        fi
        
        echo "$RESULT"
        exit 0
    fi
    
    echo "⚠️ Attempt $i failed, waiting..." >&2
    sleep $((i * 2))
done

# Alle Retries failed → Browser Fallback
echo "❌ API failed → Browser Fallback..." >&2

SEARCH_URL="https://www.google.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')"
echo "🌐 Using: $SEARCH_URL" >&2
echo ""

# Output für Browser-Nutzung
echo "BROWSER_FALLBACK: $SEARCH_URL"
exit 1
