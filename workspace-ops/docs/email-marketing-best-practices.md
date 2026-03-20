# Email Marketing Best Practices — adsdrop

> Zusammengefasst aus dem Monkeflow eCom Email Bible ($25M+ Email Revenue Erfahrung)
> Erstellt: 23.02.2026 | Gültig für: Klaviyo, E-Commerce DTC Brands

---

## 📋 Inhaltsverzeichnis

1. [Account Setup & Grundlagen](#1-account-setup--grundlagen)
2. [Deliverability & Inbox Placement](#2-deliverability--inbox-placement)
3. [Flows & Automatisierungen](#3-flows--automatisierungen)
4. [Campaigns & Newsletter](#4-campaigns--newsletter)
5. [Pop-ups & Lead Generation](#5-pop-ups--lead-generation)
6. [Design & Content](#6-design--content)
7. [Testing & Optimierung](#7-testing--optimierung)
8. [KPIs & Benchmarks](#8-kpis--benchmarks)

---

## 1. Account Setup & Grundlagen

### Die wichtigsten Einstellungen

| Setting | Empfehlung | Impact |
|---------|-----------|--------|
| **Double Opt-in** | AUS in allen Listen | 🔴 Kritisch |
| **Smart Sending** | AUS in Flows, AN in Campaigns | 🟡 Wichtig |
| **Attribution Window** | 5 Tage | 🟢 Nützlich |
| **UTM Tracking** | Aktiviert | 🟢 Nützlich |
| **Master List** | Eine Liste für alle Subscriber | 🟢 Nützlich |

### Setup Checklist

- [ ] **Klaviyo** als primäres Tool nutzen (fortschrittlichste Features für DTC)
- [ ] **Dedicated Sending Domain** einrichten
- [ ] **Dynamic Coupons** in Flows verwenden (static in Campaigns OK)
- [ ] **Pre-select signup at checkout** aktivieren [US only]
- [ ] Pop-ups mit **10% Opt-in Rate** als Ziel
- [ ] Campaign Kalender vor jedem Monat erstellen

### Was du NICHT tun solltest

❌ **Double Opt-in** — ruiniert Listenwachstum
❌ Listen **kaufen** — ruiniert Domain Reputation
❌ An die **ganze Liste** senden — immer segmentieren
❌ **Image-only Emails** — Deliverability Killer
❌ Zu viele **Links** — sieht spammy aus
❌ **ALL CAPS** in Subject Lines — Spam-Trigger
❌ Zu viele **Emojis** in Subject Lines — unprofessionell

---

## 2. Deliverability & Inbox Placement

### Die goldenen Regeln

> 📊 **Kernmetrik**: Open Rate unter 20-30% = Deliverability Problem!

### Technische Setup

- [ ] **Dedicated Sending Domain** einrichten
- [ ] **ANIBIMI** erstellen
- [ ] Bei großen Providern **Whitelist** beantragen
- [ ] **Mail-tester.com** für Spam-Score Tests
- [ ] Bei akuten Problemen: **inboxally.com** (teuer aber effektiv)

### Content-Optimierung für Deliverability

| Element | Best Practice |
|---------|---------------|
| **Bildgröße** | Max 500kb (1mb absolute Obergrenze) |
| **Bild/Text Ratio** | Nicht zu viele Bilder |
| **Links** | Weniger ist mehr |
| **Subject Lines** | Kein CAPS, wenige Emojis, keine Spam-Wörter |
| **List Hygiene** | Monatlich bereinigen |

### List Hygiene

- Bounces entfernen
- Unsubscribes respektieren
- Inaktive User segmentieren
- **Niemals** gekaufte Listen verwenden

---

## 3. Flows & Automatisierungen

### Core Flows (Muss)

| Flow | Trigger | Exclusions | Tipps |
|------|---------|------------|-------|
| **Welcome** | List订阅 | Placed Order = 0, Checkout Started = 0 | 4-8 Emails, A/B Testing |
| **Abandoned Cart** | Abandoned Checkout | Placed Order = 0 | Dynamic Product Images |
| **Browse Abandonment** | Viewed Product | Checkout Started = 0, Placed Order = 0 | 7 Tage Cooldown |
| **Post-Purchase** | Placed Order | Refunded = 0 | 8-10 Emails möglich |
| **Win-Back** | Placed Order (alt) | Placed Order seit Flow-Start = 0 | Höherer Discount |

### Flow Setup Best Practices

- [ ] **Nur EINE Master-Liste** für Welcome Flow
- [ ] **Double Opt-in AUS** in allen Listen
- [ ] **Flow Exclusions** korrekt setzen:
  - "Placed order zero times since starting this flow"
  - "Checkout started zero times since starting this flow"
- [ ] **Conditional Logic**: Exclude wenn "Viewed product at least once since starting flow"
- [ ] **A/B/C/D Testing** für "Sending Times" (Quick, Mid, Long, Random)
- [ ] **Subject Line A/B Tests** für jeden Flow-Email

### Subject Line Tricks für Flows

- `Fwd: message from the founder`
- `[see more inside]`
- `[action required]`
- `Re: about your order`
- `We see you browsing`
- `We miss you`

### "Winner" Sequenzen

#### Welcome Flow (4-5 Emails)
1. **Email #1**: Welcome discount + Brand story & Promise
2. **Email #2**: Plain text "welcome from founder" + personal story
3. **Email #3**: 10% off last chance + best sellers (Urgency, Timer)
4. **Email #4**: New discount (Free shipping) + Reviews
5. **Email #5**: Discount last-chance + "never told" founder story

#### Abandoned Cart (4-5 Emails)
1. **Email #1**: Simple reminder + 10% OFF
2. **Email #2**: Plain text from founder + story + discount follow-up
3. **Email #3**: Discount last chance + scarcity + reviews
4. **Email #4**: Better offer + brand benefits + BNPL
5. **Email #5**: Plain text "last chance" urgency

#### Browse Abandonment (3 Emails)
1. **Email #1**: Reminder + "selling fast" urgency + 10% OFF
2. **Email #2**: Plain text founder + product benefits
3. **Email #3**: Discount last chance + check out best-sellers

#### Post-Purchase (8-10 Emails)
1. **Email #1**: Funny plain text order confirmation
2. **Email #2**: Designed order confirmation + how-to/FAQ
3. **Email #3**: Founder thank you + story
4. **Email #4**: Tips on how to use product
5. **Email #5**: Useful blog posts
6. **Email #6**: "How is it going?" plain text
7. **Email #7**: Customer special discount
8. **Email #8**: Discount expiring
9. **Email #9**: Ask for UGC
10. **Email #10**: Purchase survey

---

## 4. Campaigns & Newsletter

### Campaign Setup

- [ ] **Campaign Kalender** vor jedem Monat erstellen
- [ ] **Default Segmentation Exclusion** hinzufügen
- [ ] **3x pro Woche** senden (Wochentage > Wochenende)
- [ ] **Segmente**: Engaged (30d, 60d, 90d, 120d)

### Segmentation

**Niemals an die ganze Liste senden!**

Verwende Engaged Segmente:
- Opened Email in last 30 days
- Opened Email in last 60 days
- Opened Email in last 90 days
- Opened Email in last 120 days

### Sendezeiten

| Zeit | Performance |
|------|-------------|
| **11am** (lokale Zeit) | 🟢 Gut |
| **8pm** (lokale Zeit) | 🟢 Gut |
| Wochenende | 🟡 Testen (meist schlechter) |
| Freitag Abend | 🔴 Vermeiden |

### Subject Lines

#### Formeln die funktionieren
- `Re: / Fwd:`
- `[action required]`
- `[more info inside]`
- `⬆️ / ↑ ↑ ↑ ↑ ↑`
- `[important]`
- `important email:`

#### Testing
- Long vs. Short Subject Lines
- Mit/Ohne Emoji
- Personalisierung ({{first_name}})

### Campaign Best Practices

- [ ] **Button auf First Fold** UND am Ende
- [ ] **Plain Text Campaigns** senden ("from founder")
- [ ] **Resend** an Unopener mit anderer Subject Line
- [ ] **Absender-Namen** testen
- [ ] **Apple vs. Android** splitten
- [ ] **Smart Send Time** nutzen
- [ ] **Advanced Analytics** aktivieren

### Campaign Ideen

Google Suche: `"important dates during [month]"`
- Spezielle/Internationale Tage nutzen
- Saisonale Themen
- Produkt-Launches

### Kampagnen-Resend Strategie

1. Original Campaign senden
2. 48h warten
3. An Unopener resenden mit:
   - Anderer Subject Line
   - Gleichem Content
   - Oder: "Did you miss this?"

---

## 5. Pop-ups & Lead Generation

### Setup

- [ ] Pop-up mit **Klaviyo Liste** verbinden
- [ ] **Double Opt-in entfernen**
- [ ] Mit **Welcome Flow** verknüpfen

### Beste Angebote

| Angebot | Conversion |
|---------|------------|
| **10% OFF** | 🟢 Hoch |
| **Free Shipping** | 🟢 Hoch |
| **Freebie/Gift** | 🟢 Hoch |
| **Free PDF/Guide** | 🟢 Hoch |
| **Enter to Win Contest** | 🟢 Hoch |

### Trigger

- **20s nach Landing** (empfohlen)
- **Exit Intent** (nur Desktop)
- **70% Scroll** (als Alternative)

### Pro Tips

- [ ] **2-Step Pop-up** für SMS + Email (Trojan Horse)
- [ ] **Gamified Pop-ups** testen (Spin-wheel)
- [ ] **Bild vs. Non-Bild** Pop-ups testen
- [ ] **Timer** für Urgency
- [ ] **Bubble** auf der Seite lassen (für später)
- [ ] Code **NICHT** im Thank-you Page anzeigen (in Email!)
- [ ] Nach Schließen: **7 Tage** warten bis wieder anzeigen

### Exclusions

- Checkout Page
- Cart Page
- Educational Pages
- Bestehende Email Subscriber

### Testing

Teste alles:
- Bilder
- Headlines
- Angebote
- Positioning
- Emojis
- Timer

**Tool Empfehlung**: Optimonk (besserer Testing als Klaviyo)

---

## 6. Design & Content

### Mobile First

> 📱 **85%** öffnen Emails auf Mobile!

- Mobile First designen
- Desktop Second
- Preview auf echten Geräten testen

### Dark Mode

> 🌙 **44%** nutzen Dark Mode!

- Emails müssen in Dark Mode gut aussehen
- Farben testen
- Bilder mit transparentem Hintergrund vermeiden

### Bilder

| Regel | Wert |
|-------|------|
| **Max Größe** | 500kb |
| **Absolute Obergrenze** | 1mb (selten) |
| **Format** | JPG für Fotos, PNG für Logos |
| **Alt-Text** | Immer setzen |

### Content-Typen

- [ ] **Designed Emails** (Brand-Heavy)
- [ ] **Plain Text Emails** (Personal, Founder)
- [ ] **GIFs** für Interaktivität
- [ ] **Dynamic Banners**

### Buttons & Links

- **Button auf First Fold** (ohne Scrollen sichtbar)
- **Button am Ende** (nach dem Content)
- **Text-Links** zusätzlich (nicht nur Buttons)
- Alle Links **testen** vor Senden

### Copy Writing

- Kurze Sätze
- Ein klarer CTA
- Persönlicher Ton ("Ich" statt "Wir")
- Storytelling

---

## 7. Testing & Optimierung

### Was testen?

| Element | Test-Varianten |
|---------|----------------|
| **Subject Lines** | Long vs. Short, Emojis, Personalisierung |
| **Sending Times** | Quick, Mid, Long, Random |
| **Sende-Namen** | Brand vs. Person |
| **Design** | Bild vs. Text, Button Placement |
| **Pop-ups** | Alles (Headlines, Angebote, Bilder) |

### Testing Regeln

> 🧪 **Nur EINE Sache** gleichzeitig testen!

### A/B Testing in Flows

- **A/B/C/D Testing** für Sending Times
- Subject Line Tests für **jeden Email**
- Mindestens **1 Monat** laufen lassen (oder bis genug Daten)

### Resend Strategien

1. **Campaign Resend**: An Unopener mit neuer Subject Line
2. **Flow Resend**: Nicht empfohlen (zu aufdringlich)

---

## 8. KPIs & Benchmarks

### Ziele

| Metrik | Ziel | Gut | Sehr Gut |
|--------|------|-----|----------|
| **Open Rate** | 20% | 25% | 30%+ |
| **CTR** | 1% | 2% | 3%+ |
| **Pop-up Opt-in** | 5% | 8% | 10%+ |
| **Revenue from Email** | 20% | 30% | 40%+ |

### Deliverability Warnings

⚠️ **Open Rate <20%** = Deliverability Problem
- Liste bereinigen
- Inaktive ausschließen
- Domain Health checken

### Monthly Review

- [ ] Open Rates analysieren
- [ ] CTR analysieren
- [ ] Revenue from Email
- [ ] Beste Campaigns identifizieren
- [ ] Underperformers analysieren
- [ ] Flow Performance (Revenue per Recipient)
- [ ] List Hygiene durchführen
- [ ] A/B Test Ergebnisse dokumentieren

### Tools

| Tool | Zweck |
|------|-------|
| **Klaviyo** | Email Marketing Platform |
| **Optimonk** | Pop-ups & Testing |
| **Postscript** | SMS |
| **Mail-tester.com** | Spam-Score Check |
| **Inboxally.com** | Deliverability Fix (teuer) |
| **Sendtric.com** | Countdown Timer |
| **Notion** | Dokumentation |
| **Loom** | Video Guides |

---

## 🎯 Quick Wins

Die 10 wichtigsten Änderungen für sofortige Impact:

1. ✅ **Double Opt-in entfernen**
2. ✅ **Smart Sending**: AUS in Flows, AN in Campaigns
3. ✅ **Dedicated Sending Domain** einrichten
4. ✅ **Pop-up Trigger** auf 20s setzen
5. ✅ **Subject Lines** mit `Re:` / `Fwd:` testen
6. ✅ **Plain Text Campaigns** senden
7. ✅ **Button auf First Fold** setzen
8. ✅ **Mobile First** designen
9. ✅ **Dynamic Coupons** in Flows
10. ✅ **Nie an ganze Liste** senden

---

## 📚 Weiterführende Ressourcen

- [Monkeflow Discord Community](https://discord.gg/monkeflow)
- [Klaviyo Academy](https://academy.klaviyo.com)
- [Really Good Emails](https://reallygoodemails.com) — Inspiration
- [Notion Template](https://notion.so) — für eigene Dokumentation

---

> 💡 **Letzter Tipp**: Teste alles. Was für eine Marke funktioniert, funktioniert nicht automatisch für eine andere. Daten sind dein bester Freund.

*Erstellt von Brain für adsdrop | Quelle: Monkeflow eCom Email Bible*