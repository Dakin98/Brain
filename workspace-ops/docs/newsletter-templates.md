# Newsletter-Templates und Personalisierung

Diese Dokumentation zeigt, wie du die Newsletter-Vorlagen in der Notion-Datenbank gestaltest, damit sie optimal vom Automatisierungssystem verarbeitet werden können.

## Grundstruktur in Notion

Das System erkennt folgende Formatierungen in Notion-Seiten:

| Notion-Element | Unterstützung | HTML-Ausgabe |
|----------------|---------------|--------------|
| Überschriften (H1-H3) | ✅ | `<h1>`, `<h2>`, `<h3>` |
| Aufzählungen | ✅ | `<li>` in `<ul>` |
| Nummerierte Listen | ✅ | `<li>` in `<ol>` |
| Zitate | ✅ | `<blockquote>` |
| Callouts (mit Emoji) | ✅ | `<div>` mit Styling |
| Tabellen | ❌ | Nicht unterstützt |
| Bilder | ❌ | Nicht unterstützt |
| Code-Blöcke | ❌ | Nicht unterstützt |

## Best Practices für Newsletter-Themen

1. **Aussagekräftige Titel**: Der Seitenname wird als Newsletter-Betreff verwendet
   - Gut: "Sommertrends 2026"
   - Vermeiden: "Newsletter Idee #5"

2. **Strukturierung**:
   - Beginne mit einer H1-Überschrift (Hauptthema)
   - Nutze H2 für Abschnitte
   - Füge 3-5 Bullet-Points ein (werden als Vorteile personalisiert)
   - Verwende Callouts für Tipps (beginnen mit 💡)

3. **Personalisierungsmarker**:
   - `Produkt` wird durch die Hauptprodukte des Kunden ersetzt
   - `deine Marke` wird durch den Firmennamen ersetzt

## Beispiel-Template

Ein optimales Notion-Template für "Sommertrends 2026" könnte so aussehen:

```
# Sommertrends 2026

Diese Saison bringt frische Styles für deine Marke. Die neuesten Trends passen perfekt zu unseren Produkt-Kollektionen.

## Warum Trends wichtig sind

• Kunden suchen ständig nach Neuheiten
• Trends steigern die Relevanz deiner Marke
• Sie bieten Anlass für zusätzliche Marketing-Kampagnen
• Produkt wirkt innovativer mit saisonalen Updates

💡 Tipp: Verbinde Trends mit deinen Bestsellern für maximalen Erfolg!

## Umsetzungs-Ideen

1. Integriere 2-3 Trendfarben in deine Produkt-Fotos
2. Erstelle einen Trend-Guide für deine Kunden
3. Nutze Trend-Keywords in deiner Produktsuche
```

Dieses Format wird automatisch personalisiert, wobei "deine Marke" und "Produkt" durch die entsprechenden Werte des Kunden ersetzt werden.

## Thementypen und Timing

Die Newsletter-Automatisierung verarbeitet folgende Thementypen:

| Thementyp | Beispiele | Optimaler Versandzeitpunkt |
|-----------|-----------|----------------------------|
| Produkt-Focus | Neuheiten, Bestseller, Kollektionen | 10:00 Uhr |
| Lehrreich/Informativ | Anleitungen, FAQs, Tipps | 15:00 Uhr |
| Marketing/Branding | Markengeschichte, Team, Werte | 19:00 Uhr |

Du kannst die Thementypen in Notion als Multi-Select-Tags hinzufügen. Das System berücksichtigt diese bei der Planung optimaler Sendezeiten.

## Saisonalität

Datum-basierte Newsletter werden automatisch auf das aktuelle Jahr angepasst. So kannst du z.B. "Valentinstag" im Kalender eintragen, und das System sendet es jährlich rechtzeitig vor dem 14. Februar.

## Branchen-Anpassung

Diverse Newsletter-Themen funktionieren besser für bestimmte Branchen. Empfehlungen:

- **Mode/Fashion**: Trend-Guides, Styling-Tipps, Saisonwechsel
- **Beauty**: Anwendungstipps, Ingredient-Spotlight, Hautpflege-Routinen
- **Food**: Rezepte, Zutatenkunde, Anlass-bezogene Menüs
- **Home/Deko**: Styling-Ideen, DIY-Projekte, Saisonale Wohndeko
- **Technik**: How-Tos, Vergleiche, Nutzungsszenarien

## Personalisierungs-Tiefe

Das System nutzt folgende Datenquellen für die Personalisierung:

1. **Airtable-Daten**:
   - Firmenname
   - Website-URL
   - Branche
   - Tonalität
   - Brand Colors (Primary)
   - Hauptprodukte
   - Marketing-Focus

2. **Website-Analyse**:
   - Produkt-Kategorien
   - Tonalität (casual/standard/luxury)
   - USP-Hinweise
   - Garantien/Versprechen

Fülle diese Felder in Airtable aus, um die Personalisierung zu verbessern und weniger abhängig von der Website-Analyse zu sein.

## Support für Klaviyo-Variablen

Das Template unterstützt folgende Klaviyo-Variablen:

- `$web_version_url` - Link zur Web-Version
- `$unsubscribe_url` - Abmelde-Link

Diese werden in die HTML-Templates eingesetzt und von Klaviyo beim Versand ersetzt.