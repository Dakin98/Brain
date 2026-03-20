# Airtable Cleanup Plan — adsdrop

## IST-ZUSTAND (27 Felder)

### Unkritisch — Funktioniert
| Feld | Typ | Nutzung |
|------|-----|---------|
| Firmenname | string | ✅ |
| Status | string | ✅ Prospect/Onboarding/Aktiv |
| Hauptansprechpartner | string | ✅ |
| AP E-Mail | string | ✅ |
| Website | string | ✅ |
| Branche | string | ✅ |
| Retainer | number | ✅ |
| Vertragslaufzeit | number | ✅ Monate |
| Zahlungsweise | string | ✅ Überweisung/Stripe |
| Klaviyo API Key | string | ✅ |
| Klaviyo List ID | string | ✅ |
| Meta Ad Account ID | string | ✅ |
| Meta Zugang OK | boolean | ✅ |

### Services (Checkboxen)
| Feld | Status | Aktion |
|------|--------|--------|
| Cold Mail | boolean | ✅ Keep |
| Email Marketing | boolean | ✅ Keep |
| Paid Ads | boolean | ✅ Keep |
| Newsletter Service | boolean | ✅ Keep |

### Status-Tracking (Automation)
| Feld | Status | Aktion |
|------|--------|--------|
| ClickUp Folder Created | boolean | ✅ Keep (Cold Mail) |
| ClickUp Email Marketing Created | boolean | ✅ Keep |
| ClickUp Paid Ads Created | boolean | ✅ Keep |
| Newsletter Onboarding Done | boolean | ✅ Keep |
| ClickUp Folder ID | string | ⚠️ Umbenennen → "ClickUp Cold Mail Folder ID" |

### Datenfelder
| Feld | Typ | Status | Aktion |
|------|-----|--------|--------|
| Produkt-Info | array | 🟡 | Keep für Newsletter |
| Brand Assets | array | 🟡 | Keep für Newsletter |
| Reporting Sheet | string | 🟡 | Meta Ads URL |
| Email Sprache | string | 🟡 | DE/EN |
| Website Scan Date | string | 🟡 | Automatisch |

### Fehlt / Brauchen wir
| Feld | Grund |
|------|-------|
| Stripe Customer ID | Für Rechnungen |
| Setup Gebühr | Einmalzahlung |
| Startdatum | Vertragsbeginn |
| Provisionsmodell | % oder Fix |
| Provision Wert | Zahl |
| Google Drive Folder ID | Für Assets |
| Creatives Upload Link | Für Kunden |
| Meta BM ID | Business Manager |
| Meta Pixel ID | Tracking |
| Google Ads CID | Für Google |
| GA4 Property | Analytics |
| GTM Container | Tag Manager |

## EMPFEHLUNG

### SOFORT (Heute)
1. **Neue Felder erstellen:**
   - Stripe Customer ID (string)
   - Setup Gebühr (number)
   - Startdatum (date)
   - Provisionsmodell (single select: fix/%) 
   - Provision Wert (number)

2. **Feld umbenennen:**
   - "ClickUp Folder ID" → "ClickUp Cold Mail Folder ID"

### DIESE WOCHE
3. **Platform-Zugänge vervollständigen:**
   - Meta BM ID
   - Meta Pixel ID
   - Google Ads CID
   - GA4 Property
   - GTM Container

4. **Google Drive Integration:**
   - Google Drive Folder ID
   - Creatives Upload Link

## AUFGERÄUMTE STRUKTUR (Ziel: 35 Felder)

```
KUNDEN (35 Felder)
├── Basisdaten (7)
│   ├── Firmenname
│   ├── Status
│   ├── Hauptansprechpartner
│   ├── AP E-Mail
│   ├── Website
│   ├── Branche
│   └── Startdatum
│
├── Vertrag & Abrechnung (6)
│   ├── Retainer
│   ├── Vertragslaufzeit
│   ├── Setup Gebühr
│   ├── Provisionsmodell
│   ├── Provision Wert
│   └── Zahlungsweise
│
├── Services gebucht (4)
│   ├── Cold Mail
│   ├── Email Marketing
│   ├── Paid Ads
│   └── Newsletter Service
│
├── Status Automation (5)
│   ├── ClickUp Cold Mail Created
│   ├── ClickUp Email Marketing Created
│   ├── ClickUp Paid Ads Created
│   ├── Newsletter Onboarding Done
│   └── Klaviyo Segments Done
│
├── IDs & Links (7)
│   ├── Stripe Customer ID
│   ├── ClickUp Cold Mail Folder ID
│   ├── ClickUp Email Folder ID
│   ├── ClickUp Paid Ads Folder ID
│   ├── Google Drive Folder ID
│   ├── Creatives Upload Link
│   └── Reporting Sheet
│
├── Platform Zugänge (10)
│   ├── Meta BM ID
│   ├── Meta Ad Account ID
│   ├── Meta Pixel ID
│   ├── Meta Zugang OK
│   ├── Google Ads CID
│   ├── GA4 Property
│   ├── GTM Container
│   ├── Klaviyo API Key
│   ├── Klaviyo List ID
│   └── Shopify Token
│
└── Daten & Assets (6)
    ├── Produkt-Info
    ├── Brand Assets
    ├── Email Sprache
    ├── Website Scan Date
    └── [Reserve]
```

## DURCHFÜHRUNG

Soll ich die neuen Felder jetzt in Airtable erstellen?

### JA → Ich erstelle:
- [ ] Stripe Customer ID
- [ ] Setup Gebühr
- [ ] Startdatum
- [ ] Provisionsmodell
- [ ] Provision Wert

### NEIN → Du machst es manuell

Was willst du?
