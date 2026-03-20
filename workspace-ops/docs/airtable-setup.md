# Airtable Setup für Newsletter-Automatisierung

## Schritt 1: Erstelle neue Felder in Airtable

Folgende Felder müssen in der Tabelle `Kunden` in der Basis `appbGhxy9I18oIS8E` hinzugefügt werden:

1. **Brand Colors**
   - Feldtyp: `Text`
   - Beschreibung: HEX-Code der Hauptfarbe des Kunden (z.B. `#1E90FF`)

2. **Hauptprodukte**
   - Feldtyp: `Text`
   - Beschreibung: Komma-separierte Liste der Hauptprodukte (z.B. `Shirts, Hoodies, Caps`)

3. **Marketing Focus**
   - Feldtyp: `Text`
   - Beschreibung: Hauptbotschaft/USP des Kunden (z.B. `Nachhaltige Mode`)

## Schritt 2: Update für Razeco UG

Nach dem Erstellen der Felder, aktualisiere die Daten für Razeco UG:

```bash
curl -s -X PATCH "https://gateway.maton.ai/airtable/v0/appbGhxy9I18oIS8E/Kunden" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "id": "recCVSA0tx8kwKwgI", 
        "fields": {
          "Brand Colors": "#1E90FF",
          "Hauptprodukte": "Shirts, Hoodies, Caps",
          "Marketing Focus": "Nachhaltige Mode"
        }
      }
    ]
  }'
```

## Schritt 3: Testen des Skripts mit Airtable-Daten

Nach der Aktualisierung der Felder, teste das Skript erneut:

```bash
cd ~/.openclaw/workspace && python3 scripts/klaviyo-weekly-newsletters-improved.py --client "Razeco" --draft-only
```

## Schritt 4: Manuelle Übersicht der Templates in Klaviyo

Überprüfe die in Klaviyo erstellten Drafts unter:

- [Kampagne 1](https://www.klaviyo.com/campaign/01KHREX1S5GHN74QAVRY06H10E/edit)
- [Kampagne 2](https://www.klaviyo.com/campaign/01KHREX2H3E94D5FSD3R9Z0R3Z/edit)
- [Kampagne 3](https://www.klaviyo.com/campaign/01KHREX39118AWSF6GEERENNWP/edit)

## Häufige Fehlermeldungen und Lösungen

| Fehlermeldung | Bedeutung | Lösung |
|---------------|-----------|--------|
| `UNKNOWN_FIELD_NAME` | Feld existiert nicht in Airtable | Feld zuerst in Airtable-UI erstellen |
| `ROW_DOES_NOT_EXIST` | Record ID nicht gefunden | Record ID mit GET-Request prüfen |
| `PERMISSION_DENIED` | Keine Berechtigung für Änderungen | API-Key prüfen oder Admin-Rechte einholen |

---

Diese Konfiguration ermöglicht eine deutlich verbesserte Newsletter-Personalisierung und reduziert die Abhängigkeit von der Website-Analyse, die bei SSL-Problemen fehlschlägt.