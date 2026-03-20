# Session: 2026-03-20 12:33:45 UTC

- **Session Key**: agent:main:main
- **Session ID**: e6437350-7c95-48bc-85a3-550971b7d18b
- **Source**: webchat

## Conversation Summary

user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:03 UTC] okay wie ist die mofu campaign struktru
assistant: Die MOFU (Middle of Funnel) Campaign-Struktur:

## MOFU Retargeting

| Kampagne | Ad Set | Zielgruppe | Budget | Creative | Copy-Fokus |
|----------|--------|-----------|--------|----------|------------|
| **MOFU - Hot** | ATC 7D | AddToCart 7 Tage | 25-35€/Tag | 40% Hook Creative | Produkt-Fokus, keine Erklärung nötig |
| **MOFU - Warm** | ATC 30D exkl. 7D | AddToCart 30 Tage, exkl. ATC 7D + Purchasers | 20-25€/Tag | 40% Hook Creative | USPs, Social Proof |
| **MOFU - Checkout** | IC 30D exkl. Purchasers | InitiateCheckout 30 Tage, exkl. Purchasers 30D | 15-20€/Tag | 40% Hook Creative | Urgency, Rabatt, FOMO |

## Warum das funktioniert

| Zielgruppe | Mindset | Creative-Strategie |
|------------|---------|-------------------|
| ATC 7D | "Fast gekauft" | Direkter Produkt-Reminder |
| ATC 30D | "Interessiert, aber unsicher" | Vertrauen aufbauen (Testimonials) |
| IC 30D | "Wollte kaufen, abgebrochen" | Hindernis beseitigen (Versand, Garantie) |

## Exclusions (immer!)

- Purchasers 30D von allen MOFU-Kampagnen ausschließen
- ATC 7D von Warm-Kampagne ausschließen (keine Überschneidung)

Soll ich das als CSV speichern oder direkt mit dem Meta-Setup starten?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:03 UTC] ne ich will eine camapgin mit adset für mofu wie
assistant: Eine Kampagne, mehrere Ad Sets:

## MOFU Retargeting - Eine Kampagne

| Kampagne | Ziel | Budget |
|----------|------|--------|
| **MOFU Retargeting** | Verkauf | 60-80€/Tag gesamt |

### Ad Sets

| Ad Set | Zielgruppe | Budget | Creative | Copy |
|--------|-----------|--------|----------|------|
| **ATC 7D** | AddToCart 7 Tage | 25-30€ | 40% Hook Creative | Direkter Produkt-Reminder |
| **ATC 30D exkl. 7D** | AddToCart 30 Tage, exkl. ATC 7D + Purchasers | 20-25€ | 40% Hook Creative | USPs, Social Proof |
| **IC 30D exkl. Purchasers** | InitiateCheckout 30 Tage, exkl. Purchasers 30D | 15-20€ | 40% Hook Creative | Urgency, Rabatt |

### Exclusions pro Ad Set

| Ad Set | Ausschließen |
|--------|-------------|
| ATC 7D | Purchasers 30D |
| ATC 30D exkl. 7D | ATC 7D, Purchasers 30D |
| IC 30D | Purchasers 30D |

So hast du alles in einer Kampagne, aber getrennte Budgets und Zielgruppen. Soll ich das als CSV speichern?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:04 UTC] ich gebe cold 50 euro auswie viel in mofu stecken
assistant: Bei 50€ Cold Budget:

## Budget-Verteilung

| Funnel | Budget | Verhältnis |
|--------|--------|------------|
| **Cold Traffic** | 50€ | 50% |
| **MOFU Retargeting** | 25-35€ | 25-35% |
| **BOFU (Purchasers)** | 10-15€ | 10-15% |

## Empfohlene Aufteilung

| Kampagne | Budget |
|----------|--------|
| Cold Traffic | 50€ |
| MOFU Retargeting | **30€** |
| → ATC 7D | 12€ |
| → ATC 30D exkl. 7D | 10€ |
| → IC 30D exkl. Purchasers | 8€ |

**Faustregel:** MOFU = 50-70% vom Cold Budget. Weniger = verlierst potenzielle Käufer. Mehr = übersättigung.

Passt 30€ für MOFU?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:04 UTC] aber wir wollten webvisotr auch noch reetaegetn
assistant: Stimmt! Website Visitors mit rein:

## Neue Budget-Verteilung

| Kampagne | Budget |
|----------|--------|
| Cold Traffic | 50€ |
| **MOFU Retargeting** | **35-40€** |
| → **Website Visitors 7D** | 10€ |
| → ATC 7D | 12€ |
| → ATC 30D exkl. 7D | 10€ |
| → IC 30D exkl. Purchasers | 8€ |

## Ad Sets in MOFU

| Ad Set | Zielgruppe | Budget | Intention |
|--------|-----------|--------|-----------|
| **WV 7D** | Website Visitors 7 Tage | 10€ | Frisch warm, nur gesehen |
| **ATC 7D** | AddToCart 7 Tage | 12€ | Produkt-Interesse |
| **ATC 30D exkl.** | ATC 30D exkl. 7D + Purchasers | 10€ | Überlegt noch |
| **IC 30D exkl.** | InitiateCheckout 30D exkl. Purchasers | 8€ | Fast gekauft |

## Exclusions

| Ad Set | Ausschließen |
|--------|-------------|
| WV 7D | ATC 7D, ATC 30D, Purchasers |
| ATC 7D | ATC 30D, Purchasers |
| ATC 30D | ATC 7D, Purchasers |
| IC 30D | Purchasers |

So decken wir den ganzen Funnel ab — von "nur gesehen" bis "fast gekauft".

Passt das?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:09 UTC] okay guck dir die audicne an die wir zusammen erstllt haben und sag mir wie wir die adsets struktuirternsollen
assistant: Lass mich die Audiences aus der CSV nochmal anschauen:
assistant: Basierend auf unseren Audiences — hier die Ad Set-Struktur:

## MOFU Retargeting - Ad Sets

| # | Ad Set | Audience | Budget | Exclusions | Creative-Fokus |
|---|--------|----------|--------|------------|----------------|
| 1 | **WV 7D** | Website Visitors 7D | 8€ | ATC 7D, ATC 30D, IC 30D, Purchasers | Brand Awareness, erstes Interesse wecken |
| 2 | **Product Viewers 30D** | Product Page Viewers 30D | 8€ | ATC 7D, ATC 30D, IC 30D, Purchasers | Produkt-spezifisch, was sie angeschaut haben |
| 3 | **ATC 7D** | Add to Cart 7D | 12€ | IC 30D, Purchasers | Direkter Produkt-Reminder |
| 4 | **ATC 30D exkl.** | Add to Cart 30D | 8€ | ATC 7D, IC 30D, Purchasers | USPs, Social Proof, Zweifel beseitigen |
| 5 | **IC 30D exkl.** | Initiate Checkout 30D | 6€ | Purchasers | Urgency, Rabatt, Checkout abschließen |

**Gesamt: 42€** (passend zu deinen 50€ Cold)

## Warum diese Reihenfolge?

```
WV 7D → Product Viewers → ATC 7D → ATC 30D → IC 30D
  ↓           ↓            ↓          ↓          ↓
"Gesehen"  "Produkt"   "Interesse"  "Zögert"   "Fast gekauft"
```

Jede Stufe schließt die nächste aus — keine Überschneidung, kein Budget-Verschwendung.

Passt das? Oder willst du Video Viewers auch noch mit rein?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:09 UTC] und dann lieber cbo oder abo
assistant: Bei diesem Setup: **CBO** (Campaign Budget Optimization)

## Warum CBO?

| Aspekt | CBO | ABO |
|--------|-----|-----|
| **Budget** | 42€ auf Kampagne, Meta verteilt | Feste Budgets pro Ad Set |
| **Vorteil** | Meta schiebt Geld zum besten Ad Set | Volle Kontrolle |
| **Hier besser?** | ✅ Ja | ❌ Nein |

## CBO-Setup

| Kampagne | Budget | Bid Strategy |
|----------|--------|--------------|
| **MOFU Retargeting** | 42€/Tag | Lowest Cost oder Cost Cap |

### Ad Sets (ohne feste Budgets)

| Ad Set | Audience | Exclusions |
|--------|----------|------------|
| WV 7D | Website Visitors 7D | ATC 7D, ATC 30D, IC 30D, Purchasers |
| Product Viewers 30D | Product Page Viewers 30D | ATC 7D, ATC 30D, IC 30D, Purchasers |
| ATC 7D | Add to Cart 7D | IC 30D, Purchasers |
| ATC 30D exkl. | Add to Cart 30D | ATC 7D, IC 30D, Purchasers |
| IC 30D exkl. | Initiate Checkout 30D | Purchasers |

## Warum CBO hier?

- **Unterschiedliche Audience-Größen** → CBO gleicht aus
- **Verschiedene Conversion-Rates** → CBO fördert beste Performer
- **Keine Budget-Fetzen** → Ein Ad Set kann mehr bekommen wenn's läuft

Meta wird automatisch mehr Budget in **ATC 7D** und **IC 30D** stecken (höhere Intent = bessere ROAS).

Einwand?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 12:33 UTC] top
assistant: Perfekt! 🎯

Zusammenfassung:

**MOFU Retargeting CBO**
- Budget: 42€/Tag
- 5 Ad Sets mit korrekten Exclusions
- Meta verteilt Budget automatisch zu den besten Performern

Nächster Schritt: Willst du die Kampagne direkt in Meta aufsetzen oder soll ich dir eine Checkliste/CSV zum Abhaken machen?
