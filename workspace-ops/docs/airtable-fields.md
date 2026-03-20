# Airtable-Felder für Newsletter-Automatisierung

Für eine optimale Personalisierung der automatischen Newsletter-Erstellung benötigen wir folgende Felder in der Airtable-Basis `appbGhxy9I18oIS8E`, Tabelle `Kunden`.

## Bestehende Felder

Diese Felder werden bereits genutzt:

| Feldname | Typ | Beschreibung | Verwendung |
|----------|-----|--------------|------------|
| `Firmenname` | Text | Name des Unternehmens | Absender, Branding |
| `Klaviyo API Key` | Text | API-Schlüssel für Klaviyo | Authentifizierung |
| `Website` | URL | Unternehmenswebsite | Analyse, Links |
| `Branche` | Single Select | Branchenkategorie | Themenrelevanz |
| `Tonalität` | Single Select | Kommunikationsstil | Ansprache-Stil |
| `E-Mail Rechnungen` | Email | Absender-Email | From-Adresse |
| `Status` | Single Select | Kundenstatus | Filter (Aktiv/Onboarding) |

## Neue Felder

Für die verbesserte Personalisierung empfehlen wir folgende zusätzliche Felder:

| Feldname | Typ | Beschreibung | Beispielwerte |
|----------|-----|--------------|---------------|
| `Brand Colors` | Text | Primärfarbe als HEX | `#FF5733`, `#4A90E2` |
| `Hauptprodukte` | Text | Comma-separated Liste | `T-Shirts, Hoodies, Caps` |
| `Marketing Focus` | Text | USP/Hauptbotschaft | `Nachhaltigkeit`, `Handarbeit` |
| `Newsletter Tonalität` | Single Select | Spezifisch für Newsletter | `casual`, `formal`, `premium` |
| `Newsletter Frequenz` | Single Select | Gewünschte Häufigkeit | `wöchentlich`, `alle 2 Wochen` |
| `Newsletter Tags` | Multiple Select | Themen-Kategorien | `Produkte`, `Lifestyle`, `How-To` |

## Implementierungsplan

1. **Feldtypen in Airtable anlegen**:
   - Öffne die Basis `appbGhxy9I18oIS8E`
   - Navigiere zur Tabelle `Kunden`
   - Füge die neuen Felder hinzu (rechts auf "+" klicken)

2. **Daten für bestehende Kunden hinzufügen**:
   - Ergänze mindestens für alle aktiven Kunden die Felder
   - Brand Colors können von der Website extrahiert werden
   - Hauptprodukte aus Website-Kategorien ableiten

3. **Onboarding-Formular erweitern**:
   - Jotform-Formular um entsprechende Felder erweitern
   - Alternativ: Daten im Onboarding-Call erfragen

## Nutzung im Script

Das verbesserte Script `klaviyo-weekly-newsletters-improved.py` nutzt diese Felder wie folgt:

```python
# Airtable-Daten werden in client_info gespeichert
website_analysis = analyze_website_detailed(client["website"], client_info)

# Brand Colors werden priorisiert aus Airtable genommen
primary_color = client_info.get('brand_colors', '#000000')

# Hauptprodukte werden aus Airtable gelesen oder von Website abgeleitet
products = client_info.get('hauptprodukte', '').split(',') or detected_products

# Marketing Focus überschreibt erkannten USP
usp = client_info.get('marketing_focus') or detected_usp
```

## Fallbacks

Wenn die neuen Felder nicht ausgefüllt sind, nutzt das System folgende Fallbacks:

1. **Brand Colors**:
   - Versuch, Farben aus Website-CSS zu extrahieren
   - Fallback: `#000000` (Schwarz)

2. **Hauptprodukte**:
   - Analyse der Website nach Produkt-Keywords
   - Fallback: `['Produkte', 'Angebote']`

3. **Marketing Focus**:
   - Analyse der Website nach USP-Keywords
   - Fallback: `'Qualität und Service'`

## Beispiel-Airtable-Export

So könnte ein Eintrag mit allen Feldern aussehen:

```json
{
  "id": "rec123abc",
  "fields": {
    "Firmenname": "Razeco UG",
    "Klaviyo API Key": "pk_abcd1234...",
    "Website": "https://razeco.de",
    "Branche": "Mode",
    "Tonalität": "casual",
    "E-Mail Rechnungen": "hello@razeco.de",
    "Status": "Aktiv",
    "Brand Colors": "#3A7BD5",
    "Hauptprodukte": "Shirts, Hoodies, Accessoires",
    "Marketing Focus": "Nachhaltige Produktion",
    "Newsletter Tonalität": "casual",
    "Newsletter Frequenz": "wöchentlich",
    "Newsletter Tags": ["Produkte", "Lifestyle"]
  }
}
```

Diese erweiterten Felder ermöglichen eine deutlich präzisere Personalisierung, reduzieren Fehleranfälligkeit bei der Website-Analyse und verbessern die Qualität der automatisch generierten Newsletter.