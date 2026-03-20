# Klaviyo Newsletter Automation v2

## Neue Features & Verbesserungen

Die Version 2 der Newsletter-Automatisierung bringt wichtige Verbesserungen und nutzt alle verfügbaren Airtable-Felder für optimale Personalisierung.

### 1. Intelligentes Caching

- **Website-Analyse wird in Airtable gespeichert**
  - Feld `Website Scan Date` trackt, wann die letzte Analyse durchgeführt wurde
  - Website-Analysen sind 30 Tage gültig (konfigurierbar)
  - Spart API-Kosten und beschleunigt den Prozess erheblich

### 2. Verbesserte Branding-Integration

Nutzt alle verfügbaren Branding-Felder aus Airtable:

- **`Brand Colors`** - Primär- und Sekundärfarben für Header, Buttons und Akzente
- **`Brand Fonts`** - Typografie für die gesamte Email
- **`Brand Tone`** - Kommunikationsstil (luxury, casual, standard)
- **`USPs`** - Hervorhebung von Verkaufsargumenten
- **`Brand Tagline`** - Für Vorschau-Texte und Einleitungen
- **`Klaviyo Logo URL`** - Logo im Header
- **`Klaviyo Newsletter List ID`** - Vorausgewählte Liste
- **`Social Proof`** - Für Testimonials (kann in Templates eingebunden werden)

### 3. Produktpersonalisierung

- **`Produkte JSON`** - Array von Produktkategorien
- Dynamische Ersetzung von "Produkt" mit der Hauptprodukt-Kategorie
- Angepasste CTAs basierend auf Produktkategorien

### 4. Verbesserte Notion-Integration

- Bessere Formatierung von Notion-Inhalten:
  - Überschriften (H1, H2, H3)
  - Listen (Bullets, Nummeriert)
  - Zitate
  - Callouts mit Emojis
- Smartere Personalisierung des Contents

### 5. Erweiterte Kampagnen-Optionen

- **Draft-Modus** (`--draft`): Erstellt Kampagnen ohne automatisches Scheduling
- **Kundenfilter** (`--client`): Erstellt Newsletter nur für bestimmte Kunden
- **Datum-Filter** (`--date`): Verarbeitet Themen für ein bestimmtes Datum
- **Zeitraum-Einstellung** (`--days`): Wie viele Tage voraus sollen Themen geholt werden

### 6. Robustere Fehlerbehandlung

- **Retry-Mechanismen** für alle API-Aufrufe
- **Ausführliche Logs** für bessere Diagnose
- **Fallback-Werte** bei fehlenden Daten

### 7. Verbesserte Reporting-Tools

- **Detailliertere Telegram-Nachrichten**
- **Admin-URLs** zu erstellten Kampagnen
- **JSON-Output** für Weiterverarbeitung

### 8. Responsives Email-Design

- **Mobile-optimiertes Layout**
- **Dynamische Farbanpassungen** basierend auf Brand Colors
- **Konsistente Typografie** durch Verwendung von Brand Fonts

## Nutzung

```bash
# Standard-Ausführung (alle Kunden, nächste 14 Tage)
python3 klaviyo-newsletter-v2.py

# Nur für einen bestimmten Kunden
python3 klaviyo-newsletter-v2.py --client "Razeco UG"

# Nur Drafts erstellen (kein Scheduling)
python3 klaviyo-newsletter-v2.py --draft

# Nur für ein bestimmtes Datum
python3 klaviyo-newsletter-v2.py --date "2026-03-15"

# Kombination von Optionen
python3 klaviyo-newsletter-v2.py --client "Razeco UG" --draft --days 30
```

## Erforderliche Airtable-Felder

Für optimale Nutzung sollten folgende Felder in Airtable vorhanden sein:

| Feldname | Typ | Beschreibung |
|----------|-----|-------------|
| `Website Scan Date` | Date | Datum der letzten Website-Analyse |
| `Brand Colors` | Text | Primär- und Sekundärfarben (HEX-Codes) |
| `Brand Fonts` | Text | Typografie-Einstellungen |
| `Brand Tone` | Single Select | Kommunikationsstil (luxury/casual/standard) |
| `USPs` | Text | Unique Selling Propositions |
| `Produkte JSON` | Long Text | JSON-Array der Produktkategorien |
| `Brand Tagline` | Text | Slogan/Kurzbeschreibung |
| `Klaviyo Logo URL` | URL | URL zum Firmenlogo |
| `Klaviyo Newsletter List ID` | Text | ID der Newsletter-Liste |
| `Email Sprache` | Single Select | Sprache des Newsletters |

## Integration mit Cron

Für automatische Ausführung jeden Montag um 9:00 Uhr:

```json
{
  "name": "Klaviyo: Wöchentliche Newsletter-Automation V2",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "Europe/Berlin"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Erstelle wöchentliche Newsletter für alle Kunden.\n\nFühre aus:\ncd /Users/denizakin/.openclaw/workspace && python3 scripts/klaviyo-newsletter-v2.py\n\nBerichte die Ergebnisse detailliert.",
    "timeoutSeconds": 900
  },
  "delivery": {
    "mode": "announce"
  }
}
```