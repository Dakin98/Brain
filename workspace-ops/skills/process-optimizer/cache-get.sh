#!/bin/bash
# cache-get.sh - Holt Daten aus SQLite Cache oder API
# Usage: cache-get.sh <key> <ttl_hours> <api_command>

set -e

KEY="$1"
TTL="$2"
API_CMD="$3"
CACHE_PY="$HOME/.openclaw/workspace/skills/process-optimizer/agent_cache.py"

if [ -z "$KEY" ] || [ -z "$TTL" ] || [ -z "$API_CMD" ]; then
    echo "Usage: cache-get.sh <key> <ttl_hours> <api_command>"
    exit 1
fi

# Ensure cache DB exists
if [ ! -f "$HOME/.openclaw/workspace/.cache/agent_cache.db" ]; then
    echo "Initializing cache database..." >&2
    python3 "$CACHE_PY" init >/dev/null 2>&1
fi

# Check Cache in SQLite
CACHED=$(python3 "$CACHE_PY" get "$KEY" 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$CACHED" ]; then
    echo "CACHE_HIT: $KEY" >&2
    echo "$CACHED"
    exit 0
fi

# Cache miss → API call
echo "CACHE_MISS: $KEY - calling API..." >&2
RESULT=$(eval "$API_CMD")

# Save to cache
if [ -n "$RESULT" ]; then
    python3 "$CACHE_PY" set "$KEY" "$RESULT" "$TTL" 2>/dev/null || true
fi

echo "$RESULT"
