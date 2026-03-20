# Airtable Cleanup Phase 1 — Anleitung

**Datum:** 25.02.2026
**Ziel:** Kunden-Tabelle von 83 → 70 Felder

## ✅ Bereits erledigt (automatisch)

### Daten kopiert nach Brand Assets
Neuer Record: `recnNaVVi5mXJ8hAd` (Razeco UG — Brand Kit)
- Brand Colors ✅
- Brand Fonts ✅
- Brand Tone ✅
- Brand Tagline ✅
- Logo URL (= Klaviyo Logo URL) ✅
- Lifestyle Images ✅

### Daten kopiert nach Produkt-Info
Neuer Record: `rec84GSKUWX6be8ys` (Razeco UG — Produktdaten)
- Produkte JSON ✅
- Social Proof ✅
- USPs / Vorteile ✅

### Duplikat gefixt
- Klaviyo Newsletter List ID Wert → Klaviyo List ID kopiert ✅

## 🔧 Manuell in Airtable UI löschen (Rechtsklick → Delete field)

Die Airtable API erlaubt Field-Deletion nur mit Personal Access Token, nicht OAuth.

### Sicher löschbar (Daten kopiert / Legacy):
1. ❌ **Brand Colors** — kopiert nach Brand Assets
2. ❌ **Brand Fonts** — kopiert nach Brand Assets
3. ❌ **Brand Tone** — kopiert nach Brand Assets
4. ❌ **Brand Tagline** — kopiert nach Brand Assets
5. ❌ **Klaviyo Logo URL** — kopiert nach Brand Assets → Logo URL
6. ❌ **Lifestyle Images** — kopiert nach Brand Assets
7. ❌ **USPs** — kopiert nach Produkt-Info → USPs / Vorteile
8. ❌ **Produkte JSON** — kopiert nach Produkt-Info
9. ❌ **Social Proof** — kopiert nach Produkt-Info
10. ❌ **Stripe Kunden** (Text) — Legacy, Tabelle existiert nicht mehr
11. ❌ **Klaviyo Accounts** (Text) — Legacy, Tabelle existiert nicht mehr
12. ❌ **Google Drive Ordner** — Duplikat von "Google Drive", leer
13. ❌ **Klaviyo Newsletter List ID** — Duplikat von "Klaviyo List ID", Wert kopiert

**→ 13 Felder löschen = 83 - 13 = 70 Felder**

## ⚠️ NICHT löschen (in Scripts genutzt)

Diese Felder werden aktiv in Automatisierungen referenziert:
- Firmenname, Status, Cold Mail, Email Marketing, Paid Ads
- ClickUp Folder ID/Created, ClickUp Email/Paid Ads Created
- Meta Ad Account ID, Meta Zugang OK
- Newsletter Service, Newsletter Onboarding Done
- Klaviyo API Key, Klaviyo List ID, Klaviyo Account ID, Klaviyo Segments Done
- Weekly Newsletter Day, Email Sprache
- Reporting Sheet, Google Drive, Creatives Upload
- Stripe Customer ID, Stripe Subscription ID, Stripe Abo-Status, Stripe Monatlicher Betrag
- Shopify Shop URL, Shopify Access Token
- Retainer, Provisionsmodell, Provision Wert, Setup-Gebühr

## 📋 Phase 2 (optional, später)

Weitere 8 Felder verschiebbar mit mehr Aufwand:
- Rechnungsadresse → Rechnungen-Tabelle
- E-Mail Rechnungen → Rechnungen-Tabelle
- Setup-Gebühr → Rechnungen-Tabelle
- Zahlungsweise → Rechnungen-Tabelle
- Onboarding-Datum → Onboarding Checklist
- AP Back-Office → Kontakte (neue Tabelle)
- Weitere AP → Kontakte (neue Tabelle)
- Website Scan Date → Meta/Integrationen
