# 📊 KUNDEN-DASHBOARD Konzept

**Datum:** 24. Februar 2026  
**Ziel:** Kunden Einblick in Performance & Projektstatus geben

---

## 🎯 ZWEI OPTIONEN IM VERGLEICH

### Option 1: ClickUp View/Folder Freigabe (Native)

**Wie es funktioniert:**
- Kunde bekommt ClickUp Gast-Zugang (kostenlos)
- Sieht nur seinen eigenen Folder
- Sieht Listen: Creative Pipeline, Campaigns, Reporting
- Kann Tasks kommentieren, aber nicht bearbeiten

**Vorteile:**
- ✅ Nativ in ClickUp (euer PM-Tool)
- ✅ Echtzeit Updates
- ✅ Kommentar-Funktion für Feedback
- ✅ Kunde sieht genau was ihr seht

**Nachteile:**
- ❌ ClickUp Lernkurve für Kunden
- ❌ Kunde sieht interne Details (Assignees, interne Notizen)
- ❌ Keine schöne Visualisierung (nur Listen/Boards)
- ❌ Teuer bei vielen Kunden (Business Plan nötig)

**Kosten:** ClickUp Business Plan (~$19/Monat) für Guest Access Features

---

### Option 2: Automatisierte Reports (Empfohlen)

**Wie es funktioniert:**
- n8n generiert wöchentlich/monatlich Report
- Google Sheets oder PDF
- Automatisch per Email an Kunden
- Schöne Visualisierung mit Charts

**Vorteile:**
- ✅ Professionelle Präsentation
- ✅ Kein Tool-Wechsel für Kunden
- ✅ Kontrollierbar (ihr bestimmt was drin steht)
- ✅ Automatisierbar (kein manuelles Erstellen)
- ✅ Archivierbar (Kunde hat Historie)

**Nachteile:**
- ❌ Nicht Echtzeit (wöchentlich/monatlich)
- ❌ Keine direkte Kommentar-Funktion

**Kosten:** $0 (n8n + Google Sheets sind bereits vorhanden)

---

### Option 3: Hybrid-Lösung (BEST PRACTICE)

**Kombination aus beidem:**

**Für laufende Projekte (Echtzeit):**
- ClickUp View mit beschränkten Rechten
- Nur: Creative Status, Campaign Overview
- Keine internen Details

**Für Reports (Strategie):**
- Wöchentlicher/Monatlicher automatisierter Report
- Performance Daten, KPIs, Insights
- Per Email als PDF oder Link zu Sheet

---

## 🏆 MEINE EMPFEHLUNG: Option 2 (Automatisierte Reports)

**Warum:**
1. **Euer Stack ist darauf ausgelegt** (n8n, Google Sheets laufen)
2. **Skalierbar** (keine ClickUp-Lizenzen pro Kunde)
3. **Professioneller** (PDF/Sheet sieht besser aus als ClickUp)
4. **Automatisierbar** (einmal bauen, läuft für alle Kunden)
5. **Kontrollierbar** (ihr bestimmt was Kunde sieht)

---

## 📋 KONKRETER PLAN

### Phase 1: Kunden-Report bauen (1-2 Tage)

**Was drin sein sollte:**

| Bereich | Inhalt | Datenquelle |
|---------|--------|-------------|
| **Campaign Performance** | Spend, ROAS, CTR, Conversions | Meta/Google API |
| **Creative Overview** | Aktuelle Creatives, Status, Results | ClickUp |
| **Wöchentliche Highlights** | Beste Creatives, Learnings | Manuell/Auto |
| **Next Steps** | Was passiert diese Woche | ClickUp Tasks |
| **Budget Status** | Spend vs. Budget | Meta/Google API |

**Format:**
- Google Sheet (interaktiv) ODER
- PDF (automatisch generiert) ODER
- Beides

---

### Phase 2: ClickUp View für aktive Zusammenarbeit (Optional)

**Wenn Kunde Echtzeit-Einblick braucht:**
- Eingeschränkter Folder-Zugang
- Nur: Creative Status, Campaign Overview
- Keine internen Tasks/Notizen

---

## 🛠️ TECHNISCHE UMSETZUNG

### Automatisierter Report (Empfohlene Lösung)

```
Wöchentlich (z.B. Freitag 17 Uhr):
  ↓
n8n Workflow:
  1. Pull Meta Ads Daten (letzte 7 Tage)
  2. Pull Google Ads Daten (letzte 7 Tage)
  3. Pull ClickUp Creative Status
  4. Generiere Google Sheet
  5. Erstelle Charts (ROAS, CTR, Spend)
  6. Exportiere als PDF
  7. Sende Email an Kunden
     Subject: "Weekly Performance Report - [Kunde] - KWXX"
     Attachment: PDF oder Link zu Sheet
```

**Aufwand:** 1-2 Tage

---

## 🎯 LETZTE FRAGE

**Welche Variante passt besser zu deinen Kunden?**

**A) Automatisierter Report (PDF/Sheet per Email)**
- Professionell, skalierbar, automatisierbar
- Kein Klick-Training für Kunden nötig

**B) ClickUp View (Echtzeit-Zugang)**
- Kunde sieht live was passiert
- Kann direkt kommentieren
- Aber: Interne Details sichtbar

**C) Hybrid (Beides)**
- Report für Strategie/Performance
- ClickUp für operative Zusammenarbeit

**Sag mir welche Variante du willst, dann baue ich das!** 🚀
