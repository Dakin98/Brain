#!/bin/bash
# brain-cache.sh - SQLite-basiertes Caching für alle Brain-Skills
# Keine Airtable-Abhängigkeit mehr!
# DB: ~/.openclaw/workspace/.db/brain.db

DB_PATH="$HOME/.openclaw/workspace/.db/brain.db"
COMMAND="${1:-stats}"

# Ensure DB exists
mkdir -p "$(dirname "$DB_PATH")"
if [ ! -f "$DB_PATH" ]; then
    sqlite3 "$DB_PATH" "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, data TEXT, source TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ttl_hours INTEGER);"
fi

case "$COMMAND" in
    get)
        KEY="$2"
        TTL="${3:-24}"
        
        if [ -z "$KEY" ]; then
            echo "Usage: brain-cache get <key> [ttl_hours]"
            exit 1
        fi
        
        # Check if exists and not expired
        RESULT=$(sqlite3 "$DB_PATH" "SELECT data, created_at, ttl_hours FROM cache WHERE key = '$KEY' AND (ttl_hours IS NULL OR datetime(created_at, '+' || ttl_hours || ' hours') > datetime('now'));" 2>/dev/null)
        
        if [ -n "$RESULT" ]; then
            echo "$RESULT" | cut -d'|' -f1
        else
            exit 1
        fi
        ;;
        
    set)
        KEY="$2"
        DATA="$3"
        SOURCE="${4:-unknown}"
        TTL="${5:-24}"
        
        if [ -z "$KEY" ] || [ -z "$DATA" ]; then
            echo "Usage: brain-cache set <key> <data> [source] [ttl_hours]"
            exit 1
        fi
        
        # Escape single quotes
        DATA_ESCAPED=$(echo "$DATA" | sed "s/'/''/g")
        
        sqlite3 "$DB_PATH" "INSERT OR REPLACE INTO cache (key, data, source, ttl_hours) VALUES ('$KEY', '$DATA_ESCAPED', '$SOURCE', $TTL);"
        echo "✅ Cached: $KEY"
        ;;
        
    delete)
        KEY="$2"
        if [ -z "$KEY" ]; then
            echo "Usage: brain-cache delete <key>"
            exit 1
        fi
        sqlite3 "$DB_PATH" "DELETE FROM cache WHERE key = '$KEY';"
        echo "🗑️  Deleted: $KEY"
        ;;
        
    stats)
        echo "🧠 Brain Cache Stats (SQLite)"
        echo "============================="
        echo ""
        
        TOTAL=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cache;" 2>/dev/null || echo "0")
        VALID=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cache WHERE ttl_hours IS NULL OR datetime(created_at, '+' || ttl_hours || ' hours') > datetime('now');" 2>/dev/null || echo "0")
        EXPIRED=$((TOTAL - VALID))
        
        echo "📊 Einträge:"
        echo "   Total:    $TOTAL"
        echo "   Valid:    $VALID"
        echo "   Expired:  $EXPIRED"
        echo ""
        
        # Show by source
        echo "📦 Nach Source:"
        sqlite3 "$DB_PATH" "SELECT source, COUNT(*) FROM cache GROUP BY source;" 2>/dev/null | while read line; do
            echo "   $line"
        done
        echo ""
        
        # Recent entries
        echo "🕐 Letzte 5 Einträge:"
        sqlite3 "$DB_PATH" "SELECT key, source, created_at FROM cache ORDER BY created_at DESC LIMIT 5;" 2>/dev/null | while read line; do
            echo "   $line"
        done
        echo ""
        echo "📁 DB: $DB_PATH"
        ;;
        
    list)
        sqlite3 "$DB_PATH" "SELECT key, source, created_at, ttl_hours FROM cache ORDER BY created_at DESC;" 2>/dev/null | column -t -s'|'
        ;;
        
    clear)
        read -p "⚠️  Wirklich ALLE Einträge löschen? (ja/nein): " CONFIRM
        if [ "$CONFIRM" = "ja" ]; then
            sqlite3 "$DB_PATH" "DELETE FROM cache;"
            echo "🗑️  Cache geleert"
        else
            echo "Abgebrochen"
        fi
        ;;
        
    clear-expired)
        BEFORE=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cache;")
        sqlite3 "$DB_PATH" "DELETE FROM cache WHERE ttl_hours IS NOT NULL AND datetime(created_at, '+' || ttl_hours || ' hours') <= datetime('now');"
        AFTER=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cache;")
        DELETED=$((BEFORE - AFTER))
        echo "🗑️  $DELETED expired Einträge gelöscht"
        ;;
        
    *)
        echo "Brain Cache (SQLite)"
        echo ""
        echo "Usage: brain-cache <command>"
        echo ""
        echo "Commands:"
        echo "   get <key> [ttl]       - Daten holen (fails if expired)"
        echo "   set <key> <data> [src] [ttl]  - Daten speichern"
        echo "   delete <key>          - Eintrag löschen"
        echo "   stats                 - Statistiken"
        echo "   list                  - Alle Einträge"
        echo "   clear                 - Alles löschen"
        echo "   clear-expired         - Nur abgelaufene löschen"
        echo ""
        echo "DB: $DB_PATH"
        ;;
esac
