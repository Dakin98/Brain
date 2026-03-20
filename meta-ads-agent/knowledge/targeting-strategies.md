# Meta Ads Targeting Strategien 2025

> Von CBO bis Advantage+: Die besten Targeting-Ansätze

---

## 1. Advantage+ Shopping Campaigns (ASC)

### Was ist ASC?
Meta's KI-gesteuerte E-Commerce Kampagnen-Automatisierung

**Features:**
- Kombiniert Prospecting + Retargeting in einer Kampagne
- Automatische Budget-Allokation
- Dynamische Creative-Optimierung
- Cross-Platform (FB, IG, WhatsApp, Audience Network)

**Wann nutzen?**
- E-Commerce mit Produkt-Katalog
- Mindestens 50 Conversions/Monat
- Skalierung ist Ziel

**Setup-Checkliste:**
- [ ] Produkt-Katalog optimiert (Bilder, Preise, Verfügbarkeit)
- [ ] Pixel + CAPI eingerichtet
- [ ] Mindestens 50 historische Conversions
- [ ] Budget mindestens $50/Tag
- [ ] Kreative Assets hochgeladen (Video + Static)

**Best Practices:**
- Produkt-Feed täglich aktualisieren
- Mindestens 3 Video-Creatives
- Audience-Suggestions als Input (nicht als Limit)
- Exclusions setzen (bestehende Käufer)

---

## 2. Campaign Budget Optimization (CBO)

### Was ist CBO?
Meta verteilt Budget automatisch auf beste Ad Sets

**Vorteile:**
- Bessere Performance durch KI-Optimierung
- Weniger manuelles Management
- Schnellere Learning Phase

**Wann CBO nutzen?**
- Mehrere Ad Sets in einer Kampagne
- Mindestens $50/Tag Gesamtbudget
- Gleiches Optimierungs-Ziel

**CBO-Struktur:**
```
Kampagne (CBO: $100/Tag)
├── Ad Set 1: Lookalike 1% ($40-50)
├── Ad Set 2: Lookalike 3% ($30-40)
└── Ad Set 3: Broad + Interests ($20-30)
```

**CBO Limits:**
- Cost Cap: Setze Max-Cost-Per-Result
- Min/Max Budget: Pro Ad Set (optional)

---

## 3. Ad Set Budget Optimization (ABO)

### Wann ABO nutzen?
- Testing-Phase
- Neue Audiences testen
- Wenn CBO nicht funktioniert
- Volle Budget-Kontrolle nötig

**ABO-Struktur:**
```
Kampagne
├── Ad Set 1: $30/Tag
├── Ad Set 2: $30/Tag
└── Ad Set 3: $30/Tag
```

**ABO Best Practices:**
- Mindestens $20/Tag pro Ad Set
- Max 3-5 Ad Sets pro Kampagne
- Nach 50 Conversions → CBO evaluieren

---

## 4. Audience-Typen

### A) Advantage+ Audiences (Empfohlen)
**Was:** Meta's vollautomatisches Targeting

**Wann:**
- ASC Kampagnen
- Wenn du keine klare Audience hast
- Skalierung ist Ziel

**Input (optional):**
- Audience-Suggestions
- Exclusions

### B) Lookalike Audiences
**Was:** Meta findet Nutzer, die deinen Kunden ähneln

**Quellen (nach Qualität):**
1. **Käufer (Purchase)** → Beste Qualität
2. **Add to Cart** → Gute Qualität
3. **Website-Besucher** → Mittlere Qualität
4. **Video-Viewer (75%)** → Niedrigere Qualität

**Lookalike-Größen:**
- **1%** = Engste Ähnlichkeit, höchste Qualität
- **3%** = Gute Balance Qualität/Reach
- **5%** = Breitere Reichweite

**Best Practices:**
- Mindestens 100 Personen in Quell-Audience
- 1% Lookalikes = beste Performance
- Mehrere Lookalikes testen (1%, 3%, 5%)

### C) Custom Audiences (Retargeting)

**Website Custom Audiences:**
- 7 Tage: Heißeste Audience
- 30 Tage: Warme Audience
- 90 Tage: Kalt-Warm

**Engagement Custom Audiences:**
- Video-Viewer (25%, 50%, 75%, 95%)
- Instagram-Engager
- Facebook-Engager
- Lead Form Opener

**Customer List Audiences:**
- Email-Liste hochladen
- Phone-Liste hochladen
- Für Lookalikes + Retargeting

### D) Interest Targeting
**Status:** Weniger effektiv seit iOS 14

**Wann nutzen:**
- Neue Nischen testen
- Keine Conversion-Daten verfügbar
- Spezifische Interessen (z.B. "Baby-Produkte")

**Best Practices:**
- Breitere Interessen > spezifische
- "And/Or" Logik nutzen
- Advantage+ Expansion aktivieren

---

## 5. Funnel-Struktur

### Top of Funnel (Prospecting)
**Ziel:** Neue Kunden erreichen

**Audiences:**
- Advantage+ Shopping
- Lookalike 1-3%
- Broad Targeting (Meta's AI)
- Interest Targeting (optional)

**Budget:** 70% des Gesamtbudgets

### Middle of Funnel (Engagement)
**Ziel:** Interessierte Nutzer erneut erreichen

**Audiences:**
- Video-Viewer (50%+)
- Website-Besucher (ohne Kauf)
- Instagram-Engager

**Budget:** 15% des Gesamtbudgets

### Bottom of Funnel (Retargeting)
**Ziel:** Kauf abschließen

**Audiences:**
- Add to Cart (ohne Kauf)
- Initiate Checkout (ohne Kauf)
- 7-Tage Website-Besucher

**Budget:** 15% des Gesamtbudgets

---

## 6. Exclusions (Wichtig!)

### Warum Exclusions?
- Budget nicht an bestehende Käufer verschwenden
- Frequency cappen
- Relevanz erhöhen

### Was ausschließen?
- **Käufer** (letzte 30-90 Tage)
- **Offline-Käufer** (wenn CAPI eingerichtet)
- **Unqualifizierte Leads**
- **Churned Customers**

---

## 7. Campaign-Struktur Templates

### Template A: E-Commerce Starter
```
Kampagne 1: ASC (70% Budget)
└── ASC mit Katalog

Kampagne 2: Retargeting (30% Budget)
├── Ad Set 1: Add to Cart 7 Tage
├── Ad Set 2: Website 7 Tage
└── Ad Set 3: Video 75% 7 Tage
```

### Template B: Lead Gen
```
Kampagne 1: Prospecting (70% Budget)
├── Ad Set 1: Lookalike 1% (Kunden)
├── Ad Set 2: Lookalike 3% (Kunden)
└── Ad Set 3: Interest Targeting

Kampagne 2: Retargeting (30% Budget)
├── Ad Set 1: Website 7 Tage
├── Ad Set 2: Video 50% 7 Tage
└── Ad Set 3: Lead Form Opener
```

### Template C: Testing
```
Kampagne: TESTING (separates Budget)
├── Ad Set 1: Creative Test A
├── Ad Set 2: Creative Test B
├── Ad Set 3: Audience Test 1
└── Ad Set 4: Audience Test 2
```

---

## 8. Troubleshooting Targeting

### Hohe CPMs
- Audience verbreitern
- Placements überprüfen
- CBO statt ABO testen

### Niedriger Reach
- Audience vergrößern (Lookalike 3% statt 1%)
- Interessen hinzufügen
- Advantage+ Expansion aktivieren

### Keine Conversions
- Conversion Event überprüfen
- Pixel-Tracking testen
- Audience-Qualität checken
- Creative überprüfen

### Ad Fatigue
- Frequency checken (>5 = Problem)
- Neue Audience
- Neue Creative
- Exclusions aktualisieren

---

## 9. Quick Reference

| Audience-Typ | Budget-Share | CPM | Conversion-Rate |
|--------------|--------------|-----|-----------------|
| ASC | 50-70% | Mittel | Hoch |
| Lookalike 1% | 20-30% | Mittel-Hoch | Hoch |
| Lookalike 3% | 10-20% | Niedrig | Mittel |
| Retargeting 7d | 10-15% | Niedrig | Sehr hoch |
| Retargeting 30d | 5-10% | Sehr niedrig | Hoch |

---

## 10. Targeting-Checkliste

- [ ] Ziel-Audience definiert (Demografie, Interessen)
- [ ] Lookalike-Quelle ausgewählt (Käufer > ATC > Besucher)
- [ ] Lookalike-Größe festgelegt (1% für Qualität, 3% für Scale)
- [ ] Retargeting-Windows gesetzt (7d, 30d, 90d)
- [ ] Exclusions definiert (Käufer, Churned)
- [ ] CBO vs ABO entschieden
- [ ] Budget pro Ad Set kalkuliert
- [ ] ASC evaluiert (falls E-Commerce)
