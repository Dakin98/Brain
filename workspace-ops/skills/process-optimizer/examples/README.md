# Process Optimizer - Beispiele

## Übersicht

Dieser Ordner enthält praktische Beispiele für die Nutzung des Process Optimizers mit **SQLite**.

## Scripts

### cached-meta-ads.sh
Zeigt, wie Meta Ads Daten mit 24h SQLite Cache abgerufen werden.

```bash
./cached-meta-ads.sh <kunde_id>
```

### cached-shopify.sh
Zeigt, wie Shopify Revenue mit 24h SQLite Cache abgerufen wird.

```bash
./cached-shopify.sh <kunde_id>
```

## Integration in eigene Scripts

### Vorher (ohne Cache):
```bash
RESULT=$(curl -s "https://api.meta.com/ads/campaigns")
```

### Nachher (mit SQLite Cache):
```bash
CACHE_PY="~/.openclaw/workspace/skills/process-optimizer/agent_cache.py"
RESULT=$(python3 $CACHE_PY fetch "meta_ads_campaigns" 24 \
    "curl -s https://api.meta.com/ads/campaigns")
```

## Token-Einsparung

| Script | Ohne Cache | Mit Cache | Einsparung |
|--------|-----------|-----------|------------|
| Meta Ads | ~12k tokens | ~3.6k tokens | 70% |
| Shopify | ~3k tokens | ~300 tokens | 90% |
| Klaviyo | ~8k tokens | ~1.2k tokens | 85% |

## SQLite Datenbank

**Location:** `~/.openclaw/workspace/.cache/agent_cache.db`

```sql
-- Cache-Tabelle
CREATE TABLE cache (
    key TEXT PRIMARY KEY,
    data TEXT NOT NULL,
    ttl_hours INTEGER,
    access_count INTEGER DEFAULT 1,
    created_at TIMESTAMP,
    last_accessed TIMESTAMP
);

-- Token Usage-Tabelle
CREATE TABLE token_usage (
    workflow TEXT,
    tokens_in INTEGER,
    tokens_out INTEGER,
    cached BOOLEAN,
    timestamp TIMESTAMP
);
```
