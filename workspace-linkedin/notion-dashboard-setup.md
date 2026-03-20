# Notion Dashboard Setup Guide

## Schritt 1: Datenbank erstellen

1. **Neue Seite in Notion erstellen** → "Iron Media Dashboard"
2. **Tabelle hinzufügen** → Leere Tabelle
3. **Titel:** "Meta Ads Metrics"

## Schritt 2: Properties einrichten

| Property Name | Type | Options / Formula |
|--------------|------|-------------------|
| **Metric** | Title | (Name der Metric) |
| **Gestern** | Number | Format: Number |
| **Letzte 7 Tage** | Number | Format: Number |
| **Letzte 30 Tage** | Number | Format: Number |
| **Ziel** | Number | Format: Number |
| **Status** | Formula | Siehe unten |
| **Trend** | Formula | Siehe unten |

## Schritt 3: Formeln

### Status Formula
```javascript
if(
  prop("Metric") == "Payback Period",
  if(prop("Gestern") < 30, "🟢 Gut", if(prop("Gestern") < 60, "🟡 Okay", "🔴 Kritisch")),
  if(prop("Gestern") > prop("Ziel"), "🟢 Gut", if(prop("Gestern") > prop("Ziel") * 0.8, "🟡 Okay", "🔴 Kritisch"))
)
```

### Trend Formula
```javascript
if(prop("Gestern") > prop("Letzte 7 Tage"), "📈", if(prop("Gestern") < prop("Letzte 7 Tage"), "📉", "➡️"))
```

## Schritt 4: Einträge erstellen

| Metric | Ziel | Notizen |
|--------|------|---------|
| ncROAS | 2.0 | New Customer ROAS |
| Payback Period | 30 | In Tagen, niedriger ist besser |
| LTV/CAC | 3.5 | Ratio |
| MER | 4.0 | Marketing Efficiency Ratio |
| Contribution Margin | 0.20 | 20% als 0.20 eingeben |

## Schritt 5: Views erstellen

### 1. Tabelle (Default)
- Alle Metrics mit allen Daten

### 2. Board View (nach Status)
- Gruppiert nach Status (🟢🟡🔴)
- Schneller Überblick, was kritisch ist

### 3. Gallery View
- Karten für jede Metric
- Großes Status-Emoji
- Gut für Mobile

## Schritt 6: Daily Check Template

**Erstelle eine wiederkehrende Aufgabe:**

```
🔍 Daily Metrics Check

□ Dashboard öffnen
□ Rote Felder identifizieren
□ Aktion für heute definieren
□ Team briefen falls nötig

Notizen:
- 
```

## Schritt 7: Automatisierung (Optional)

Mit Notion API + Make/Zapier:
- Tägliche Daten aus Meta Ads API ziehen
- Automatisch in Notion aktualisieren
- Alert bei kritischen Werten

## Finale Ansicht

```
┌─────────────────────────────────────────────────────────────┐
│  IRON MEDIA DASHBOARD                    🔄 Letztes Update  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🟢 ncROAS              2.3    📈    Ziel: >2.0            │
│  🟢 Payback Period      18T    📈    Ziel: <30T            │
│  🟢 LTV/CAC             4.2    📈    Ziel: >3.5            │
│  🟢 MER                 4.5    📈    Ziel: >4.0            │
│  🟢 Contribution Margin 28%    📈    Ziel: >20%            │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  ✅ Alle Metrics auf Kurs                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

1. **Jetzt:** Datenbank in 10 Minuten aufsetzen
2. **Heute:** Erste Daten eintragen
3. **Diese Woche:** Daily Check etablieren
4. **Nächste Woche:** Trends analysieren

---

Soll ich dir auch ein **Template-Link** erstellen, den du direkt in Notion duplizieren kannst? 📊
