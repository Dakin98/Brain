# Airtable Felder für ClickUp Automatisierung

## Benötigte Felder (bitte manuell hinzufügen)

Geh zu: https://airtable.com/appbGhxy9I18oIS8E/tblvKELPk6GFf0jG4/viwHblEkmZYNueSSO

### Schritt 1: Service-Checkboxen (Input)

Füge diese 2 Checkbox-Felder hinzu:

| Feldname | Typ | Farbe/Icon |
|----------|-----|-----------|
| `Cold Mail` | Checkbox | 🟢 Grün |
| `Email Marketing` | Checkbox | 🔵 Blau |

**So geht's:**
1. Rechts auf "+" neben dem letzten Feld klicken
2. "Checkbox" auswählen
3. Namen eingeben
4. Farbe wählen (optional)

### Schritt 2: Status-Checkboxen (Output)

Füge diese 2 Checkbox-Felder hinzu:

| Feldname | Typ | Farbe/Icon |
|----------|-----|-----------|
| `ClickUp Folder Created` | Checkbox | ⚫ Grau |
| `ClickUp Email Marketing Created` | Checkbox | ⚫ Grau |

### Schritt 3: Test-Dummy erstellen

1. Neue Zeile in Airtable hinzufügen
2. **Firmenname:** `🧪 TEST Automatisierung`
3. **Status:** `Active`
4. **Cold Mail:** ☑️ (ankreuzen)
5. **Email Marketing:** ☑️ (ankreuzen)
6. **ClickUp Folder Created:** ⬜ (leer lassen!)
7. **ClickUp Email Marketing Created:** ⬜ (leer lassen!)

### Schritt 4: Test starten

```bash
# Manuelle Test-Ausführung
~/.openclaw/workspace/scripts/clickup-coldmail-cron.sh
```

**Erwartetes Ergebnis:**
- Cron findet den Test-Kunden
- Erstellt Cold Mail Folder + 6 Tasks
- Erstellt Email Marketing Folder + 7 Tasks  
- Setzt beide Checkboxen in Airtable auf "true"

### Schritt 5: Aufräumen

Nach dem Test:
1. Test-Kunde in Airtable löschen
2. Test-Folder in ClickUp löschen (manuell)

## Troubleshooting

### "Feld nicht gefunden"
→ Feldnamen müssen exakt so heißen wie oben (inkl. Leerzeichen)

### "Kein Zugriff"
→ API Token braucht Rechte für die Base

### "Cron findet nichts"
→ Status muss exakt "Active" heißen (nicht "active" oder "Aktiv")
