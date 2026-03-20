#!/bin/bash
# process-cache.sh - SQLite Cache für Process Optimizer
# Usage: process-cache [stats|clear|get <key> <ttl>|set <key> <data> <source> <ttl>]

COMMAND="${1:-stats}"
DB_PATH="$HOME/.openclaw/workspace/.db/brain.db"

case "$COMMAND" in
    get)
        KEY="$2"
        TTL="${3:-24}"
        
        if [ -z "$KEY" ]; then
            echo "Usage: process-cache get <key> [ttl_hours]"
            exit 1
        fi
        
        RESULT=$(sqlite3 "$DB_PATH" "SELECT data FROM cache WHERE key = '$KEY' AND (ttl_hours IS NULL OR datetime(created_at, '+' || ttl_hours || ' hours') > datetime('now'));" 2>/dev/null)
        
        if [ -n "$RESULT" ]; then
            echo "$RESULT"
        else
            exit 1
        fi
        ;;
        
    set)
        KEY="$2"
        DATA="$3"
        SOURCE="${4:-process}"
        TTL="${5:-24}"
        
        if [ -z "$KEY" ] || [ -z "$DATA" ]; then
            echo "Usage: process-cache set <key> <data> [source] [ttl_hours]"
            exit 1
        fi
        
        DATA_ESCAPED=$(echo "$DATA" | sed "s/'/''/g")
        sqlite3 "$DB_PATH" "INSERT OR REPLACE INTO cache (key, data, source, ttl_hours) VALUES ('$KEY', '$DATA_ESCAPED', '$SOURCE', $TTL);"
        ;;
        
    stats)
        echo "⚙️  Process Cache Stats (SQLite)"
        echo "================================"
        echo ""
        
        TOTAL=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cache;" 2>/dev/null || echo "0")
        VALID=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cache WHERE ttl_hours IS NULL OR datetime(created_at, '+' || ttl_hours || ' hours') > datetime('now');" 2>/dev/null || echo "0")
        
        echo "   Total:  $TOTAL"
        echo "   Valid:  $VALID"
        echo "   Expired: $((TOTAL - VALID))"
        echo ""
        
        sqlite3 "$DB_PATH" "SELECT source, COUNT(*) FROM cache GROUP BY source;" 2>/dev/null
        ;;
        
    clear)
        sqlite3 "$DB_PATH" "DELETE FROM cache;"
        echo "🗑️  Process Cache geleert"
        ;;
        
    list)
        sqlite3 "$DB_PATH" "SELECT key, source, created_at FROM cache ORDER BY created_at DESC LIMIT 20;" 2>/dev/null | column -t -s'|'
        ;;
        
    *)
        echo "Process Cache (SQLite)"
        echo ""
        echo "Usage: process-cache <command>"
        echo ""
        echo "   get <key> [ttl]              - Daten holen"
        echo "   set <key> <data> [src] [ttl] - Daten speichern"
        echo "   stats                        - Statistiken"
        echo "   clear                        - Cache leeren"
        echo "   list                         - Einträge auflisten"
        ;;
esac
