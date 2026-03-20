# 📧 Newsletter-Automatisierung: Überblick

Die Newsletter-Automatisierung ermöglicht es, personalisierte Newsletter-Kampagnen für alle aktiven Kunden basierend auf Themen aus dem Notion-Kalender zu erstellen.

## 📋 Was wurde umgesetzt

1. **Neues Python-Script `klaviyo-weekly-newsletters-improved.py`**
   - Robustere Website-Analyse mit besserer Fehlerbehandlung
   - Intelligentes Timing für Kampagnen-Versand
   - Verbesserte Template-Personalisierung
   - Admin-Links zu Klaviyo-Kampagnen
   - Command-Line-Optionen für Flexibilität

2. **Aktualisierter Cron-Job**
   - Läuft jeden Montag um 9:00 Uhr
   - Nutzt das verbesserte Script
   - Alter Job wurde deaktiviert

3. **Dokumentation**
   - `newsletter-automation-konzept.md` - Vollständiges Konzept
   - `newsletter-templates.md` - Wie Templates in Notion erstellt werden sollten
   - `airtable-fields.md` - Empfohlene Airtable-Felder
   - `airtable-setup.md` - Einrichtungsanleitung

## 🚀 Nächste Schritte

1. **Airtable-Felder erstellen**
   - `Brand Colors` (Text): HEX-Code der Primärfarbe
   - `Hauptprodukte` (Text): Komma-separierte Liste
   - `Marketing Focus` (Text): USP/Hauptbotschaft

2. **Templates testen**
   - Notion-Themen auf optimale Formatierung prüfen
   - Test-Run mit Razeco UG

3. **Erweiterungen (optional)**
   - Themen-Relevanz nach Branche (z.B. Mode vs. Food)
   - A/B-Testing von Betreffzeilen
   - Automationen für Follow-up-Kampagnen

## 💡 Verbesserungen gegenüber der Vorversion

- **Zuverlässigkeit:** Bessere Fehlerbehandlung, Cache für API-Aufrufe
- **Qualität:** Verbesserte Templates, mehr Personalisierung
- **Effizienz:** Intelligentes Timing, Parallelisierung
- **Kontrolle:** Mehr Optionen, detaillierte Logs
- **Links:** Direkte URLs zu Klaviyo-Kampagnen

## 🛠️ Verwendung

### Regulärer Automatisierungs-Prozess

Der Cron-Job läuft automatisch jeden Montag um 9:00 Uhr und führt folgende Schritte aus:
1. Themen für die kommende Woche aus Notion abrufen
2. Aktive Kunden mit Klaviyo-API-Keys aus Airtable abrufen
3. Websites analysieren und personalisierte Newsletters erstellen
4. Drafts in Klaviyo erstellen mit optimaler Zeitplanung
5. Bericht per Telegram senden

### Manuelle Ausführung

```bash
# Alle Kunden, alle Themen
python3 scripts/klaviyo-weekly-newsletters-improved.py

# Nur für einen bestimmten Kunden
python3 scripts/klaviyo-weekly-newsletters-improved.py --client "Razeco"

# Nur als Draft (keine Zeitplanung)
python3 scripts/klaviyo-weekly-newsletters-improved.py --draft-only

# Nur für bestimmtes Thema
python3 scripts/klaviyo-weekly-newsletters-improved.py --topic "FAQ"

# Nur für bestimmtes Datum
python3 scripts/klaviyo-weekly-newsletters-improved.py --date "2026-03-01"

# Kombinationen
python3 scripts/klaviyo-weekly-newsletters-improved.py --client "Razeco" --topic "FAQ" --draft-only
```

## 📊 Erfolgsmetriken

- **Volumen:** 8 Themen × Anzahl Kunden = Kampagnen pro Woche
- **Personalisierung:** Templates nutzen Kunde-spezifische Daten
- **Effizienz:** ~1 Minute pro Kunde für volle Automatisierung
- **Fehlerrate:** Website-Analyse nutzt Fallbacks bei SSL-Problemen

## 📅 Wartungsplan

- **Wöchentlich:** Themen im Notion-Kalender prüfen/ergänzen
- **Monatlich:** Airtable-Felder für neue Kunden ausfüllen
- **Vierteljährlich:** Template-Variationen und Designs aktualisieren
- **Jährlich:** Klaviyo-API-Version und Kompatibilität prüfen

---

Mit dieser Automatisierung sparst du ~4-5 Stunden pro Woche für das manuelle Erstellen von Newsletters und steigerst gleichzeitig die Qualität und Konsistenz.