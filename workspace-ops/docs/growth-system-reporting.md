# Growth System — Reporting & Dashboards

---

## 1. Dashboard-Übersicht

| Dashboard | Frequenz | Zielgruppe | Ort |
|-----------|----------|------------|-----|
| Content Performance | Wöchentlich (Mo) | Deniz | ClickUp Dashboard |
| Outbound Performance | Wöchentlich (Mo) | Deniz | ClickUp Dashboard |
| Growth Overview | Monatlich (1. des Monats) | Deniz / Team | ClickUp Dashboard |
| Funnel Tracker | Live | Deniz | CRM Board View |

---

## 2. Content Performance Dashboard

### Widgets

**YouTube KPIs (Table Widget)**
| Metrik | Quelle | Custom Field |
|--------|--------|-------------|
| Videos Published (Woche) | YouTube Pipeline | Count tasks with status "Published" |
| Total Views (7d) | YouTube Pipeline | Sum of "Views (7 Tage)" |
| Avg. Watch Time | YouTube Pipeline | Avg of "Watch Time (h)" |
| Avg. CTR | YouTube Pipeline | Avg of "CTR (%)" |
| New Subscribers | YouTube Pipeline | Sum of "Subscriber Delta" |

**Reels KPIs (Table Widget)**
| Metrik | Quelle | Custom Field |
|--------|--------|-------------|
| Reels Published | Reels Pipeline | Count status "Published" |
| Total Views | Reels Pipeline | Sum of "Views" |
| Total Saves | Reels Pipeline | Sum of "Saves" |
| Total Shares | Reels Pipeline | Sum of "Shares" |
| Profile Visits | Reels Pipeline | Sum of "Profile Visits" |

**LinkedIn KPIs (Table Widget)**
| Metrik | Quelle | Custom Field |
|--------|--------|-------------|
| Posts Published | LinkedIn Pipeline | Count status "Published" |
| Total Impressions | LinkedIn Pipeline | Sum of "Impressions" |
| Avg. Engagement Rate | LinkedIn Pipeline | Avg of "Engagement Rate (%)" |
| Total Comments | LinkedIn Pipeline | Sum of "Comments" |

**Newsletter KPIs (Table Widget)**
| Metrik | Quelle | Custom Field |
|--------|--------|-------------|
| Newsletters Sent | Newsletter Pipeline | Count status "Sent" |
| Avg. Open Rate | Newsletter Pipeline | Avg of "Open Rate (%)" |
| Avg. Click Rate | Newsletter Pipeline | Avg of "Click Rate (%)" |
| Subscriber Count | Newsletter Pipeline | Latest "Subscriber Count" |

**Pipeline Status (Board Widget)**
- YouTube Pipeline Board — sieht man wo Videos stecken

**Calendar Widget**
- Publish Dates aller Plattformen

---

## 3. Outbound Performance Dashboard

### Widgets

**Campaign Overview (Table Widget)**
| Metrik | Quelle | Custom Field |
|--------|--------|-------------|
| Active Campaigns | Campaigns | Count status "Active" |
| Total Emails Sent | Campaigns | Sum of "Emails Sent" |
| Avg. Open Rate | Campaigns | Avg of "Open Rate (%)" |
| Avg. Reply Rate | Campaigns | Avg of "Reply Rate (%)" |
| Total Meetings | Campaigns | Sum of "Meetings Booked" |
| Avg. Meeting Rate | Campaigns | Avg of "Meeting Rate (%)" |

**Reply Breakdown (Pie Chart Widget)**
- Interested vs. Not Interested vs. OOO vs. Referral vs. Bounce

**Best/Worst Campaigns (Table Widget)**
- Top 3 Campaigns by Reply Rate
- Bottom 3 Campaigns by Reply Rate

**Domain Health (Table Widget)**
| Domain | Health Score | Daily Volume | Status |
|--------|------------|-------------|--------|
| domain1.com | 95% | 25/50 | 🟢 |
| domain2.com | 88% | 30/50 | 🟢 |

**Reply Pipeline (Board Widget)**
- Reply Management Kanban

---

## 4. Growth Overview Dashboard (Monatlich)

### Widgets

**Funnel Metrics (Custom Text/Table)**
```
Content Reach → Leads Generated → Quali Calls → Strategie Calls → Won

YouTube Views:  X,XXX
Reels Views:    X,XXX
LinkedIn Imp:   X,XXX
─────────────────────
Total Reach:    XX,XXX

Inbound Leads:     XX
Outbound Leads:    XX
─────────────────
Quali Calls:       XX
No-Shows:          XX (XX%)
─────────────────
Strategie Calls:   XX
Offers Made:       XX
─────────────────
Won:               XX
Revenue:           €XX,XXX
```

**Channel ROI (Table Widget)**
| Channel | Effort (h/Woche) | Leads | Meetings | Won | Revenue | ROI |
|---------|-------------------|-------|----------|-----|---------|-----|
| YouTube | 8h | - | - | - | - | - |
| Cold Email | 5h | - | - | - | - | - |
| LinkedIn | 3h | - | - | - | - | - |
| Newsletter | 2h | - | - | - | - | - |

**Month-over-Month Trends**
- Line Chart: Key metrics over time (requires manual data entry or Airtable)

---

## 5. Datenquellen & Integration

### Manuelles Tracking (Phase 1 — Sofort)

| Plattform | Wie | Frequenz | Wo eintragen |
|-----------|-----|----------|-------------|
| YouTube | YouTube Studio | Nach 7 Tagen pro Video | YouTube Pipeline Custom Fields |
| Instagram | Insights App | Nach 7 Tagen pro Reel | Reels Pipeline Custom Fields |
| LinkedIn | Post Analytics | Nach 7 Tagen pro Post | LinkedIn Pipeline Custom Fields |
| Klaviyo | Campaign Reports | 48h nach Send | Newsletter Pipeline Custom Fields |
| Apollo | Campaign Dashboard | Wöchentlich | Campaigns Custom Fields |

### Semi-Automatisch (Phase 2 — Woche 3+)

| Integration | Tool | Was |
|-------------|------|-----|
| YouTube API → ClickUp | Node.js Script | Views, Watch Time, CTR auto-pull nach 7 Tagen |
| Apollo API → ClickUp | Node.js / Make | Campaign stats sync |

### Voll-Automatisch (Phase 3 — Optional)

| Integration | Tool | Was |
|-------------|------|-----|
| YouTube Analytics API | Google Cloud + Cron | Täglicher Stats-Pull |
| Klaviyo API | Webhook/Cron | Open/Click Rates auto-fill |
| Apollo API | Webhook | Neue Replies → ClickUp Tasks |

---

## 6. KPI-Ziele (Templates zum Ausfüllen)

### Content KPIs

| Metrik | Aktuell | Ziel (3 Monate) | Ziel (6 Monate) |
|--------|---------|-----------------|-----------------|
| YouTube Videos / Monat | ? | 4 | 4-8 |
| Avg. Views / Video | ? | 500 | 2.000 |
| Reels / Monat | ? | 12 | 20 |
| LinkedIn Posts / Woche | ? | 3 | 5 |
| Newsletter Open Rate | ? | 35% | 40% |
| Newsletter Subscribers | ? | ? | +500 |

### Outbound KPIs

| Metrik | Aktuell | Ziel (3 Monate) | Ziel (6 Monate) |
|--------|---------|-----------------|-----------------|
| Emails Sent / Woche | ? | 200 | 500 |
| Open Rate | ? | 60% | 65% |
| Reply Rate | ? | 5% | 8% |
| Positive Reply Rate | ? | 2% | 4% |
| Meetings / Monat | ? | 8 | 20 |
| Meeting → Won Rate | ? | 25% | 30% |

### Revenue KPIs

| Metrik | Aktuell | Ziel (3 Monate) | Ziel (6 Monate) |
|--------|---------|-----------------|-----------------|
| Leads / Monat (gesamt) | ? | 30 | 60 |
| Quali Calls / Monat | ? | 15 | 30 |
| Strategie Calls / Monat | ? | 8 | 16 |
| Won Deals / Monat | ? | 2 | 4 |
| Avg. Deal Value | ? | €3.000 | €5.000 |
| Monthly Revenue (New) | ? | €6.000 | €20.000 |

---

## 7. Reporting Workflow

### Wöchentlich (Montag, 30 Min)

```
09:00  Öffne Content Dashboard
       → YouTube Stats der letzten Woche nachtragen
       → Reels Stats nachtragen
       → LinkedIn Stats nachtragen
       → Newsletter Stats nachtragen (falls gesendet)

09:15  Öffne Outbound Dashboard
       → Apollo Campaign Stats aktualisieren
       → Neue Replies in Reply Management eintragen
       → Domain Health checken

09:25  Review
       → Was lief gut? Was nicht?
       → Nächste Woche: Welche Content-Stücke, welche Campaigns?
       → Tasks für die Woche priorisieren
```

### Monatlich (1. des Monats, 1h)

```
→ Growth Overview Dashboard updaten
→ Alle KPIs gegen Ziele vergleichen
→ Funnel-Analyse: Wo sind die Bottlenecks?
→ Channel ROI berechnen
→ Entscheidungen treffen: Mehr/weniger in welchen Channel?
→ Ziele für nächsten Monat setzen
```
