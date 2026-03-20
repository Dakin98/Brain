# 📊 PROJEKTPLAN: Kunden-Dashboard (Streamlit)

**Projekt:** Razeco Performance Dashboard  
**Ziel:** Live-Dashboard für Kunden, selbst gehostet, automatisiert  
**Zeitraum:** 24.02.2026 - 26.02.2026 (2 Tage)  
**Status:** 🟡 Genehmigt & Ready to Start

---

## 🎯 PROJEKTZIELE

### Primäre Ziele (MVP)
- [ ] Dashboard läuft auf Server (82.165.169.97:8501)
- [ ] Zeigt Razeco Meta Ads Performance
- [ ] Automatische Updates 2x täglich (9 Uhr, 17 Uhr)
- [ ] Einfache Passwort-Authentifizierung
- [ ] Professionelles Design (Razeco Branding)

### Sekundäre Ziele (Optional)
- [ ] ClickUp Creative Status Integration
- [ ] Budget vs. Spend Tracking
- [ ] PDF Export Funktion
- [ ] Mobile Responsive

---

## 📋 PHASE 1: ENTWICKLUNG (24.02.2026)

### 1.1 Setup & Installation (14:00-15:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 1.1.1 | Python Environment prüfen | 10min | - |
| 1.1.2 | Streamlit installieren | 10min | 1.1.1 |
| 1.1.3 | Plotly installieren | 10min | 1.1.2 |
| 1.1.4 | Test-App laufen lassen | 15min | 1.1.3 |
| 1.1.5 | Projektstruktur erstellen | 15min | 1.1.4 |

**Output:** `dashboard/` Ordner mit funktionierender Streamlit-App

---

### 1.2 Daten-Layer (15:00-16:30)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 1.2.1 | Meta API Verbindung testen | 30min | - |
| 1.2.2 | Razeco Account Daten pullen | 30min | 1.2.1 |
| 1.2.3 | Daten transformieren (pandas) | 30min | 1.2.2 |
| 1.2.4 | Caching implementieren | 30min | 1.2.3 |

**Output:** `data/meta_ads.py` - Funktionierender Daten-Pull

---

### 1.3 Dashboard UI (16:30-18:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 1.3.1 | Sidebar Navigation | 15min | - |
| 1.3.2 | KPI Cards (Spend, ROAS, CTR) | 30min | 1.2.4 |
| 1.3.3 | Spend Chart (Zeitverlauf) | 30min | 1.3.2 |
| 1.3.4 | ROAS Chart | 30min | 1.3.3 |
| 1.3.5 | Campaign Tabelle | 30min | 1.3.4 |
| 1.3.6 | "Last Updated" Zeitstempel | 15min | 1.3.5 |

**Output:** `app.py` - Funktionierendes Dashboard

---

### 1.4 Styling & Branding (18:00-18:30)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 1.4.1 | Razeco Brand Colors | 15min | - |
| 1.4.2 | Custom CSS einfügen | 15min | 1.4.1 |

**Output:** `.streamlit/config.toml` + `assets/style.css`

---

### 1.5 Lokaler Test (18:30-19:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 1.5.1 | Dashboard lokal starten | 10min | 1.4.2 |
| 1.5.2 | Mit echten Daten testen | 20min | 1.5.1 |

**Output:** Dashboard läuft auf `localhost:8501`

---

## 📋 PHASE 2: DEPLOYMENT (25.02.2026)

### 2.1 Server Vorbereitung (09:00-10:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 2.1.1 | SSH Verbindung testen | 15min | - |
| 2.1.2 | Python/Streamlit auf Server installieren | 30min | 2.1.1 |
| 2.1.3 | Projekt auf Server kopieren | 15min | 2.1.2 |

**Output:** Projekt liegt auf Server

---

### 2.2 Automatisierung (10:00-11:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 2.2.1 | Daten-Update Script bauen | 30min | 2.1.3 |
| 2.2.2 | Cronjob einrichten (9 Uhr, 17 Uhr) | 15min | 2.2.1 |
| 2.2.3 | Cronjob testen | 15min | 2.2.2 |

**Output:** Automatische Updates laufen

---

### 2.3 Security (11:00-11:30)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 2.3.1 | Passwort-Authentifizierung einbauen | 20min | - |
| 2.3.2 | Test Login | 10min | 2.3.1 |

**Output:** Passwort geschütztes Dashboard

---

### 2.4 Launch (11:30-12:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 2.4.1 | Dashboard als Service starten | 15min | 2.3.2 |
| 2.4.2 | Externer Zugriff testen | 15min | 2.4.1 |

**Output:** Dashboard live auf `http://82.165.169.97:8501`

---

## 📋 PHASE 3: FINALISIERUNG (25.02.2026 Nachmittag)

### 3.1 Testing & Bugfixing (14:00-15:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 3.1.1 | End-to-End Test | 30min | 2.4.2 |
| 3.1.2 | Bugs fixen | 30min | 3.1.1 |

---

### 3.2 Dokumentation (15:00-15:30)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 3.2.1 | README.md erstellen | 15min | - |
| 3.2.2 | MEMORY.md aktualisieren | 15min | 3.2.1 |

---

### 3.3 Übergabe (15:30-16:00)

| Task | Beschreibung | Zeit | Abhängigkeit |
|------|-------------|------|--------------|
| 3.3.1 | Link & Passwort an Razeco senden | 15min | 3.1.2 |
| 3.3.2 | Kurze Anleitung schreiben | 15min | 3.3.1 |

---

## 🛠️ TECH STACK

| Komponente | Technologie | Version |
|------------|-------------|---------|
| Framework | Streamlit | Latest |
| Charts | Plotly | Latest |
| Daten | Pandas | Latest |
| API | Meta Marketing API | v18.0 |
| Server | Python HTTP Server | Built-in |
| Auth | Streamlit-Authenticator | Latest |

---

## 📁 DATEISTRUKTUR

```
~/.openclaw/workspace/dashboard/
├── app.py                    # Hauptanwendung
├── requirements.txt          # Python Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit Config
├── assets/
│   └── style.css            # Custom CSS
├── data/
│   ├── __init__.py
│   ├── meta_ads.py          # Meta API Integration
│   └── cache.py             # Daten-Caching
├── components/
│   ├── __init__.py
│   ├── kpis.py              # KPI Cards
│   ├── charts.py            # Charts
│   └── tables.py            # Tabellen
├── utils/
│   ├── __init__.py
│   └── auth.py              # Authentifizierung
└── README.md                # Dokumentation
```

---

## ⚠️ RISIKEN & MITIGATION

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Meta API Rate Limits | Mittel | Hoch | Caching, nicht zu oft pullen |
| Server nicht erreichbar | Niedrig | Kritisch | Monitoring, Alert auf Telegram |
| Daten inkonsistent | Mittel | Mittel | Validierung, Error Handling |
| Razeco findet Dashboard kompliziert | Niedrig | Mittel | Einfaches Design, Anleitung |

---

## ✅ AKZEPTANZKRITERIEN

Das Projekt ist erfolgreich wenn:

1. ✅ Dashboard ist unter `http://82.165.169.97:8501` erreichbar
2. ✅ Passwort-Login funktioniert
3. ✅ Razeco Meta Ads Daten werden angezeigt
4. ✅ Charts sind interaktiv
5. ✅ Daten aktualisieren sich automatisch 2x täglich
6. ✅ Design ist professionell (Razeco Branding)
7. ✅ Keine Errors im Log

---

## 📞 KOMMUNIKATION

| Was | Wann | Wie |
|-----|------|-----|
| Täglicher Stand | 18:00 Uhr | Update hier im Chat |
| Bei Blockern | Sofort | Nachricht |
| Fertigstellung | 25.02. 16:00 | Demo + Link |

---

## 🎯 NÄCHSTER SCHRITT

**Sofort starten mit Phase 1.1?**

Zeit: Jetzt (12:00) - 19:00 Uhr heute
Oder: Morgen früh beginnen?

**Sag "Start" und ich fange an!** 🚀
