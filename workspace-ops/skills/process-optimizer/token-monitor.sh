#!/bin/bash
# token-monitor.sh - Trackt Token-Usage in SQLite
# Usage: token-monitor.sh <workflow> <tokens_in> <tokens_out>

set -e

WORKFLOW="$1"
TOKENS_IN="$2"
TOKENS_OUT="$3"
CACHE_PY="$HOME/.openclaw/workspace/skills/process-optimizer/agent_cache.py"

if [ -z "$WORKFLOW" ] || [ -z "$TOKENS_IN" ] || [ -z "$TOKENS_OUT" ]; then
    echo "Usage: token-monitor.sh <workflow> <tokens_in> <tokens_out>"
    echo "Example: token-monitor.sh 'Meta Ads Report' 8500 4200"
    exit 1
fi

# Ensure DB exists
if [ ! -f "$HOME/.openclaw/workspace/.cache/agent_cache.db" ]; then
    python3 "$CACHE_PY" init 2>/dev/null || true
fi

# Save to SQLite
python3 "$CACHE_PY" track "$WORKFLOW" "$TOKENS_IN" "$TOKENS_OUT"

echo "✅ Token-Usage gespeichert: $WORKFLOW ($TOKENS_IN in / $TOKENS_OUT out)"
