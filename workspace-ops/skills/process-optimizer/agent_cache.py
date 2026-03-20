#!/usr/bin/env python3
# agent_cache.py - SQLite-basiertes Caching für Agent-Prozesse
# Usage: python3 agent_cache.py <command> [args]

import sqlite3
import json
import hashlib
import time
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Cache DB location
CACHE_DIR = Path.home() / ".openclaw" / "workspace" / ".cache"
CACHE_DB = CACHE_DIR / "agent_cache.db"

def init_db():
    """Initialisiert die Cache-Datenbank"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            ttl_hours INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            access_count INTEGER DEFAULT 1,
            source TEXT,
            data_size INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS token_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workflow TEXT NOT NULL,
            tokens_in INTEGER,
            tokens_out INTEGER,
            cached BOOLEAN DEFAULT FALSE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_cache_key ON cache(key)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_token_workflow ON token_usage(workflow)
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Cache-Datenbank initialisiert: {CACHE_DB}")

def get(key):
    """Holt Daten aus dem Cache wenn gültig"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT data, ttl_hours, created_at, access_count 
        FROM cache 
        WHERE key = ?
    ''', (key,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    data, ttl_hours, created_at, access_count = row
    
    # Check TTL
    created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    expires = created + timedelta(hours=ttl_hours)
    
    if datetime.now() > expires:
        return None  # Expired
    
    # Update access stats
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cache 
        SET last_accessed = CURRENT_TIMESTAMP, access_count = access_count + 1
        WHERE key = ?
    ''', (key,))
    conn.commit()
    conn.close()
    
    return data

def set_key(key, data, ttl_hours=24, source="api"):
    """Speichert Daten im Cache"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    data_size = len(data.encode('utf-8')) if isinstance(data, str) else len(str(data))
    
    cursor.execute('''
        INSERT OR REPLACE INTO cache 
        (key, data, ttl_hours, source, data_size, created_at, last_accessed, access_count)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
    ''', (key, data, ttl_hours, source, data_size))
    
    conn.commit()
    conn.close()
    print(f"💾 Cached: {key} (TTL: {ttl_hours}h, Size: {data_size} bytes)", file=sys.stderr)

def delete(key):
    """Löscht einen Cache-Eintrag"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cache WHERE key = ?', (key,))
    conn.commit()
    conn.close()
    print(f"🗑️ Deleted: {key}", file=sys.stderr)

def clear_expired():
    """Löscht abgelaufene Einträge"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM cache 
        WHERE datetime(created_at, '+' || ttl_hours || ' hours') < datetime('now')
    ''')
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"🧹 Cleared {deleted} expired entries", file=sys.stderr)
    return deleted

def stats():
    """Zeigt Cache-Statistiken"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    # Total entries
    cursor.execute('SELECT COUNT(*), SUM(data_size) FROM cache')
    total_count, total_size = cursor.fetchone()
    total_count = total_count or 0
    total_size = total_size or 0
    
    # Expired entries
    cursor.execute('''
        SELECT COUNT(*) FROM cache 
        WHERE datetime(created_at, '+' || ttl_hours || ' hours') < datetime('now')
    ''')
    expired_count = cursor.fetchone()[0] or 0
    
    # Most accessed
    cursor.execute('''
        SELECT key, access_count, source 
        FROM cache 
        ORDER BY access_count DESC 
        LIMIT 5
    ''')
    top_keys = cursor.fetchall()
    
    # Token usage stats
    cursor.execute('''
        SELECT workflow, SUM(tokens_in), SUM(tokens_out), COUNT(*)
        FROM token_usage
        GROUP BY workflow
        ORDER BY SUM(tokens_in) DESC
    ''')
    token_stats = cursor.fetchall()
    
    conn.close()
    
    print("📊 Cache Statistiken")
    print("=" * 50)
    print(f"Gesamt-Einträge: {total_count}")
    print(f"Gesamt-Größe: {total_size / 1024:.2f} KB")
    print(f"Abgelaufen: {expired_count}")
    print(f"Aktiv: {total_count - expired_count}")
    print()
    
    if top_keys:
        print("🔥 Meist genutzt:")
        for key, count, source in top_keys:
            print(f"  {key[:40]:40} | {count:5}x | {source}")
        print()
    
    if token_stats:
        print("🤖 Token Usage:")
        print(f"  {'Workflow':<30} | {'In':>8} | {'Out':>8} | Runs")
        print("  " + "-" * 60)
        for workflow, tin, tout, runs in token_stats:
            print(f"  {workflow[:30]:<30} | {tin or 0:>8} | {tout or 0:>8} | {runs}")
    
    # Calculate savings
    cursor = sqlite3.connect(CACHE_DB).cursor()
    cursor.execute('SELECT SUM(access_count - 1) FROM cache')
    hits = cursor.fetchone()[0] or 0
    print(f"\n💰 Cache Hits: {hits} (API-Calls gespart)")

def list_all():
    """Listet alle Cache-Einträge"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT key, ttl_hours, created_at, access_count, source,
               CASE 
                   WHEN datetime(created_at, '+' || ttl_hours || ' hours') < datetime('now') 
                   THEN 'EXPIRED'
                   ELSE 'ACTIVE'
               END as status
        FROM cache
        ORDER BY created_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    print(f"{'Key':<40} | {'TTL':>5} | {'Status':<8} | {'Access':>6}")
    print("-" * 70)
    for key, ttl, created, access, source, status in rows:
        print(f"{key[:40]:<40} | {ttl:>5}h | {status:<8} | {access:>6}x")

def track_tokens(workflow, tokens_in, tokens_out, cached=False):
    """Trackt Token-Usage"""
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO token_usage (workflow, tokens_in, tokens_out, cached)
        VALUES (?, ?, ?, ?)
    ''', (workflow, tokens_in, tokens_out, cached))
    
    conn.commit()
    conn.close()

def get_with_fallback(key, ttl_hours, command):
    """Holt aus Cache oder führt Command aus"""
    cached = get(key)
    
    if cached:
        print(f"CACHE_HIT: {key}", file=sys.stderr)
        return cached
    
    print(f"CACHE_MISS: {key}", file=sys.stderr)
    
    # Execute command
    import subprocess
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    data = result.stdout if result.returncode == 0 else result.stderr
    
    # Cache the result
    set_key(key, data, ttl_hours)
    
    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: agent_cache.py <command> [args]")
        print("")
        print("Commands:")
        print("  init                          - Initialize cache database")
        print("  get <key>                     - Get cached data")
        print("  set <key> <data> <ttl_hours>  - Set cache entry")
        print("  delete <key>                  - Delete cache entry")
        print("  clear-expired                 - Remove expired entries")
        print("  stats                         - Show cache statistics")
        print("  list                          - List all entries")
        print("  track <workflow> <in> <out>   - Track token usage")
        print("  fetch <key> <ttl> <command>   - Get or fetch and cache")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_db()
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: agent_cache.py get <key>")
            sys.exit(1)
        result = get(sys.argv[2])
        if result:
            print(result)
        else:
            sys.exit(1)
    elif command == "set":
        if len(sys.argv) < 5:
            print("Usage: agent_cache.py set <key> <data> <ttl_hours>")
            sys.exit(1)
        set_key(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: agent_cache.py delete <key>")
            sys.exit(1)
        delete(sys.argv[2])
    elif command == "clear-expired":
        clear_expired()
    elif command == "stats":
        stats()
    elif command == "list":
        list_all()
    elif command == "track":
        if len(sys.argv) < 5:
            print("Usage: agent_cache.py track <workflow> <tokens_in> <tokens_out>")
            sys.exit(1)
        track_tokens(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    elif command == "fetch":
        if len(sys.argv) < 5:
            print("Usage: agent_cache.py fetch <key> <ttl_hours> <command>")
            sys.exit(1)
        result = get_with_fallback(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        print(result)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
