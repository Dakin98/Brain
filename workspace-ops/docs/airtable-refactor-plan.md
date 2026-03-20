# Airtable Refactor Plan

## Ziel: Kunden-Tabelle von 49 auf ~25 Felder reduzieren

### Neue Struktur Kunden-Tabelle

**1. Kerninfos (12 Felder)**
- Firmenname, Status, Website, Branche, Shop-System
- Hauptansprechpartner, AP E-Mail, AP Telefon
- Rechnungsadresse, E-Mail Rechnungen
- Notizen, Onboarding-Datum

**2. Vertragsdaten (7 Felder)**
- Retainer, Provisionsmodell, Provision Wert
- Vertragslaufzeit, Startdatum, Setup-Gebühr, Zahlungsweise

**3. System-IDs (8 Felder)**
- Stripe Customer ID
- Stripe Subscription ID, Stripe Abo-Status
- Shopify Shop URL, Shopify Access Token
- Klaviyo API Key, Klaviyo Segments Done
- Google Drive Ordner

**4. Plattform-IDs (10 Felder)**
- Meta BM ID, Meta Ad Account ID, Meta Pixel ID, Meta Zugang OK
- Google Ads CID, Google Ads Zugang OK
- GA4 Property ID, GA4 Zugang OK
- GTM Container ID, GTM Zugang OK

**Total: ~37 Felder** (statt 49)

### Zu löschende/löschende Tabellen
- Table 1 (ungebraucht)
- Klaviyo Accounts (wird in Kunden integriert)
- Stripe Kunden (wird in Kunden integriert)

### Zu behaltende verknüpfte Tabellen
- Produkt-Info
- Brand Assets
- Plattform-Zugänge (nur für Login-Daten, nicht IDs)
- Projekte
- Rechnungen
- Onboarding Checklist

### Scripts die angepasst werden müssen
- stripe-setup-invoice.sh
- shopify-monthly-revenue.sh
- klaviyo-setup-segments.sh
- check-platform-access.py
- Alle Cron-Jobs
