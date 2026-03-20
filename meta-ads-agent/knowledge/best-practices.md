# Meta Ads Best Practices 2025

> Aktuelle Strategien für Performance & Compliance

---

## 1. iOS 14.5+ & Privacy Changes

### Was sich geändert hat
- **ATT (App Tracking Transparency):** Nutzer müssen aktiv Tracking erlauben
- **Attribution Window:** 28-Tage → 7-Tage View
- **Conversion Events:** Werden nach Event-Zeit (nicht Impression) gemessen

### Lösungen & Workarounds

#### First-Party Data nutzen
- Eigene Kundenlisten hochladen
- CRM-Daten für Lookalikes nutzen
- Email-Listen für Custom Audiences

#### Conversions API (CAPI)
- Server-Side Tracking implementieren
- Pixel + CAPI kombinieren für bessere Attribution
- Offline Conversions integrieren

#### Aggregated Event Measurement (AEM)
- 8 Conversion Events priorisieren
- Domain verifizieren (DNS TXT Record)
- Meta Tag oder HTML-File Upload

#### Simplified Targeting
- Statt detaillierter Interessen → breitere Audience
- Advantage+ Targeting nutzen
- Meta's AI die Optimierung überlassen

---

## 2. Campaign Structure

### Empfohlene Account-Struktur

```
Kampagne (Objective: Sales/Leads)
├── Ad Set 1: Advantage+ Shopping (ASC)
├── Ad Set 2: Retargeting 7 Tage
├── Ad Set 3: Retargeting 30 Tage
└── Ad Set 4: Lookalike 1-3%
```

### Budget Allocation
- **70%** Prospecting (ASC, Lookalikes)
- **20%** Retargeting (7-30 Tage)
- **10%** Testing (neue Creatives, Audiences)

---

## 3. Bidding & Optimization

### Bid Strategies

| Strategie | Wann nutzen |
|-----------|-------------|
| **Lowest Cost** | Neue Kampagnen, Learning Phase |
| **Cost Cap** | Skalierung mit CPA-Ziel |
| **ROAS Goal** | Etablierte Kampagnen mit ROAS-Target |
| **Advantage+ Shopping** | E-Commerce mit Katalog |

### Optimization Events
1. **Purchase** (Gold-Standard für E-Commerce)
2. **Initiate Checkout** (Für niedriges Budget)
3. **Add to Cart** (Nur wenn Purchase zu teuer)
4. **Lead** (Für Lead-Gen Kampagnen)

---

## 4. Targeting Strategien

### CBO (Campaign Budget Optimization)
- Meta verteilt Budget automatisch auf beste Ad Sets
- **Empfohlen:** Für die meisten Kampagnen aktivieren
- Min. 50 Conversions/Woche pro Ad Set für stabile Optimierung

### ABO (Ad Set Budget Optimization)
- Manuelle Budget-Kontrolle
- **Nutzen:** Für Tests oder wenn CBO nicht funktioniert

### Audience-Typen (Priorität)

1. **Advantage+ Shopping (ASC)**
   - Kombiniert Prospecting + Retargeting
   - AI optimiert automatisch
   - 70% YoY Wachstum

2. **Lookalike Audiences**
   - 1% = engste Ähnlichkeit (höchste Qualität)
   - 3-5% = breitere Reichweite
   - Quelle: Käufer, nicht nur Website-Besucher

3. **Retargeting**
   - 7 Tage: Heißeste Audience
   - 30 Tage: Warme Audience
   - 90 Tage: Kalt-Warm (nur bei Budget)

4. **Interest Targeting**
   - Weniger effektiv seit iOS 14
   - Nur für Testing oder spezifische Nischen

---

## 5. Placements

### Automatic Placements (Empfohlen)
- Meta optimiert automatisch
- 90%+ der Advertiser nutzen dies
- Bessere CPMs durch mehr Inventory

### Manual Placements (Wenn...)
- Spezifische Format-Tests (nur Reels)
- Budget-Kontrolle für teure Placements
- Brand Safety Anforderungen

### Top Placements 2025
1. **Reels** (höchstes Engagement)
2. **Stories** (gute Conversion)
3. **Feed** (höchste Reichweite)
4. **Marketplace** (günstige CPMs)

---

## 6. Tracking & Attribution

### Must-Have Setup
- [ ] Meta Pixel installiert
- [ ] Conversions API aktiv
- [ ] Domain verifiziert
- [ ] 8 Conversion Events priorisiert
- [ ] Offline Conversions (falls relevant)

### Attribution Modelle
- **7-Day Click + 1-Day View** (Standard)
- **1-Day Click** (konservativer)
- **Compare Windows** für bessere Analyse

### Key Metrics überwachen
- **ROAS** (Return on Ad Spend)
- **MER** (Marketing Efficiency Ratio)
- **CPP** (Cost Per Purchase)
- **Thumb-Stop Rate** (Video)
- **Add-to-Cart Rate**

---

## 7. Compliance & Policy

### Landing Page Requirements
- [ ] Ad Promise = Landing Page Content
- [ ] Schnelle Ladezeit (<3 Sekunden)
- [ ] Aktuelle Privacy Policy
- [ ] Klare Contact Information
- [ ] Keine Deceptive Practices

### Ad Creative Guidelines
- [ ] Max 20% Text auf Bildern (Empfehlung)
- [ ] Keine sensationalistischen Claims
- [ ] Keine before/after ohne Kontext
- [ ] Keine personal attributes ("Are you...?")

---

## 8. Testing Framework

### 70/20/10 Regel
- **70%** Proven Creatives/Formats
- **20%** Neue Tests (Format, Hook, CTA)
- **10%** Experimental (Trends, Memes, Voiceovers)

### Testing-Struktur
```
Kampagne: TESTING
├── Ad Set A: Creative Variation 1
├── Ad Set B: Creative Variation 2
└── Ad Set C: Creative Variation 3
```

### Was testen?
1. **Hooks** (erste 3 Sekunden)
2. **CTAs** ("Shop Now" vs "Learn More")
3. **Formats** (Video vs Carousel vs Static)
4. **Audiences** (Lookalike vs Interest vs Broad)
5. **Placements** (Reels vs Feed vs Stories)

---

## 9. Skalierung

### Wann skalieren?
- 50+ Conversions in Learning Phase
- Stabiler ROAS über 7 Tage
- Frequency < 3

### Wie skalieren?
1. **Vertical:** Budget um 20% erhöhen (alle 3-4 Tage)
2. **Horizontal:** Neue Ad Sets/ Audiences
3. **Creative:** Winning Creatives duplizieren

### Was vermeiden?
- Zu schnelle Budget-Erhöhungen (>30%)
- Zu viele Änderungen gleichzeitig
- Learning Phase unterbrechen

---

## 10. Troubleshooting

### Niedriger CTR
- Hook verbessern (erste 3 Sekunden)
- Thumbnail/Text Overlay testen
- Audience überprüfen

### Hoher CPC/CPM
- Placements überprüfen
- Audience verbreitern
- Creative Fatigue checken

### Niedrige CVR
- Landing Page optimieren
- Preis/Angebot testen
- Retargeting-Strategie anpassen

### Ad Fatigue (Frequency > 5)
- Neue Creative hochladen
- Audience ausschließen
- Pausieren und neu starten

---

## Quick Reference: Checkliste neuer Kampagne

- [ ] Ziel definiert (Sales/Leads/Traffic)
- [ ] Pixel + CAPI eingerichtet
- [ ] Domain verifiziert
- [ ] Katalog verbunden (für E-Commerce)
- [ ] Conversion Event ausgewählt
- [ ] Budget festgelegt (min. $20/Tag)
- [ ] Audience definiert
- [ ] Creative hochgeladen (min. 3 Varianten)
- [ ] Tracking getestet
- [ ] Learning Phase geplant (7 Tage)
