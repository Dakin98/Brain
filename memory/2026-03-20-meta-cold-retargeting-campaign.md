# Session: 2026-03-20 11:08:13 UTC

- **Session Key**: agent:main:main
- **Session ID**: 790a767e-728b-476c-8336-887178e42f15
- **Source**: webchat

## Conversation Summary

assistant: Ich recherchiere aktuelle Best Practices für getrennte Cold/Retargeting Campaign Setups:
assistant: Lass mich noch mehr Details zu ASC (Advantage+ Shopping Campaigns) und der aktuellen Trennungs-Strategie recherchieren:
assistant: Perfekt! Hier ist das recherchierte Campaign Setup für getrennte Cold/Retargeting-Struktur:

---

## **Best Practice 2025: Getrennte Campaign-Struktur**

### **Warum getrennt?**
- CBO gibt Budget an die **größte/günstigste Audience** → Cold Traffic frisst Retargeting-Budget
- **ABO für Retargeting** = garantierter Spend auf profitable Audiences
- **CBO oder ASC für Cold** = Algorithmus kann skalieren

---

## **OPTION A: ABO + CBO (Klassisch)**

### **Campaign 1: RETARGETING (ABO)** 🔥
**Budget Type:** Ad Set Budget Optimization  
**Ziel:** Purchase

| Ad Set | Audience | Tägliches Budget | Optimierung |
|--------|----------|------------------|-------------|
| AS 1 | ATC 30 Tage | 20€ | Purchase |
| AS 2 | Website Visitors 30d | 15€ | Purchase |
| AS 3 | Video Views 50% 30d | 10€ | Purchase |

**Wichtig:** Keine CBO! Jede Ad Set bekommt festes Budget.

---

### **Campaign 2: COLD PROSPECTING (CBO)** 🌡️
**Budget Type:** Campaign Budget Optimization  
**Ziel:** Purchase  
**Campaign Budget:** 50-100€/Tag

| Ad Set | Audience | Min/Max Spend |
|--------|----------|---------------|
| AS 1 | Lookalike 1% Purchasers | 20% min |
| AS 2 | Lookalike 1-3% Purchasers | - |
| AS 3 | Broad (18-65+) | - |

---

## **OPTION B: ASC + Manual (Modern)**

### **Campaign 1: ASC (Advantage+ Shopping)** 🛒
- **Ziel:** Alles in einem (Cold + Retargeting)
- **Budget:** 70% des Gesamtbudgets
- **Einstellung:** Existing customers auf 0% setzen = Fokus auf Neukunden

### **Campaign 2: Manual Retargeting** 🔥
- **Ziel:** Purchase
- **Budget:** 30% für zusätzliches Retargeting
- **Nur:** ATC, Checkout Initiate

---

## **Empfehlung für dich**

Da du noch wenig Conversion-Daten hast:

```
START mit OPTION A (ABO + CBO getrennt):

Retargeting ABO:   30€/Tag (sicherer Profit)
Cold CBO:          50€/Tag (Testing & Skalierung)
```

**Wenn du 50+ Purchases hast:**
→ Auf OPTION B (ASC) umstellen

---

## **Exclusions (Kritisch!)**

| Campaign | Ausschluss |
|----------|------------|
| Cold CBO | Purchaser 180d, ATC 30d |
| Retargeting ABO | Purchaser 30d |

---

Soll ich dir das als konkreten ClickUp-Task oder Notion-Dokument anlegen?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 11:02 UTC] okay eine liste mit custom audiences bitte
assistant: Hier ist deine Custom Audiences Liste:

---

## **🔥 HOT (Höchste Conversion-Wahrscheinlichkeit)**

| Name | Quelle | Zeitfenster | Nutzung |
|------|--------|-------------|---------|
| Purchasers 30 Tage | Käufer | 30 Tage | Exclusion, Upsell |
| Purchasers 180 Tage | Käufer | 180 Tage | Lookalike-Source, Retention |
| Initiate Checkout 30 Tage | Checkout begonnen | 30 Tage | Hot Retargeting |
| Add to Cart 30 Tage | Warenkorb | 30 Tage | Hot Retargeting |
| Add to Cart 7 Tage | Warenkorb | 7 Tage | Sehr hot, hohe Priorität |

---

## **🌡️ WARM (Engagiert, kennen die Marke)**

| Name | Quelle | Zeitfenster | Nutzung |
|------|--------|-------------|---------|
| Website Visitors 30 Tage | Alle Seitenbesucher | 30 Tage | Warm Retargeting |
| Website Visitors 14 Tage | Alle Seitenbesucher | 14 Tage | Frischer, besser |
| Website Visitors 7 Tage | Alle Seitenbesucher | 7 Tage | Sehr warm |
| Product Page Viewers 30 Tage | Produktdetailseiten | 30 Tage | Hochinteressiert |
| Video Views 95% 30 Tage | Video fast ganz gesehen | 30 Tage | Lookalike-Source |
| Video Views 75% 30 Tage | Video 75% gesehen | 30 Tage | Engagiert |
| Video Views 50% 30 Tage | Video Hälfte gesehen | 30 Tage | Retargeting |
| Instagram Engager 30 Tage | Post-Interaktionen | 30 Tage | Günstiges Retargeting |
| Facebook Engager 30 Tage | Post-Interaktionen | 30 Tage | Günstiges Retargeting |
| Lead Form Opener 30 Tage | Formular geöffnet | 30 Tage | Lead-Nurturing |

---

## **❄️ COLD (Neukunden-Akquise)**

| Name | Quelle | Nutzung |
|------|--------|---------|
| Lookalike 1% Purchasers 180d | Käufer | Beste Cold-Audience |
| Lookalike 1-3% Purchasers 180d | Käufer | Größeres Volumen |
| Lookalike 5-10% Purchasers 180d | Käufer | Skalierung |
| Lookalike 1% Video 95% 30d | Video-Engager | Wenn wenig Käufer |
| Lookalike 1-3% Video 95% 30d | Video-Engager | Alternative Source |
| Interests: Fashion | Verhalten/Interessen | Testing |
| Interests: Online Shopping | Verhalten/Interessen | Testing |
| Interests: [Deine Nische] | Verhalten/Interessen | Nischen-Testing |
| Broad 18-65+ | Kein Targeting | ASC/Algorithmus-Test |

---

## **🚫 EXCLUSIONS (Ausschlüsse)**

| Name | Nutzung |
|------|---------|
| Purchasers 30 Tage | Von Cold & Warm ausschließen |
| Purchasers 7 Tage | Von Retargeting ausschließen |
| Add to Cart 30 Tage | Von Cold Traffic ausschließen |
| Website Visitors 30 Tage | Von Cold Lookalikes ausschließen |

---

## **Prioritäten für dein Setup**

```
1. Website Visitors 30 Tage (einfach, sofort nutzbar)
2. Add to Cart 30 Tage (hoher Impact)
3. Video Views 95% 30 Tage (für Lookalikes)
4. Lookalike 1% Purchasers (wenn du Sales hast)
5. Initiate Checkout 30 Tage (wenn vorhanden)
```

Soll ich dir die Pixel-Events dafür auch auflisten?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 11:03 UTC] kannst du mir die ganzen custom audiences erstellen?
assistant: Ich kann die Custom Audiences nicht direkt in Meta Ads erstellen — dafür bräuchte ich API-Zugriff auf deinen Ad Account.

Aber ich kann dir helfen, sie schnell manuell anzulegen. Hier ist der **Schritt-für-Schritt Plan**:

---

## **Schnell-Setup: Custom Audiences erstellen**

### **1. Meta Ads Manager öffnen**
→ Tools → Audiences → Create Audience → Custom Audience

---

### **2. Website Custom Audiences (Pixel-basiert)**

| Reihenfolge | Audience Name | Event | Zeitfenster |
|-------------|---------------|-------|-------------|
| 1 | `Purchasers 30D` | Purchase | 30 Tage |
| 2 | `Purchasers 180D` | Purchase | 180 Tage |
| 3 | `Initiate Checkout 30D` | InitiateCheckout | 30 Tage |
| 4 | `Add to Cart 30D` | AddToCart | 30 Tage |
| 5 | `Add to Cart 7D` | AddToCart | 7 Tage |
| 6 | `Website Visitors 30D` | All Website Visitors | 30 Tage |
| 7 | `Website Visitors 14D` | All Website Visitors | 14 Tage |
| 8 | `Website Visitors 7D` | All Website Visitors | 7 Tage |
| 9 | `Product Page Viewers 30D` | ViewContent (URL contains /product/) | 30 Tage |

---

### **3. Engagement Custom Audiences**

| Reihenfolge | Audience Name | Quelle | Engagement | Zeitfenster |
|-------------|---------------|--------|------------|-------------|
| 10 | `Video Views 95% 30D` | Videos | 95% gesehen | 30 Tage |
| 11 | `Video Views 75% 30D` | Videos | 75% gesehen | 30 Tage |
| 12 | `Video Views 50% 30D` | Videos | 50% gesehen | 30 Tage |
| 13 | `IG Engagers 30D` | Instagram | Alle Interaktionen | 30 Tage |
| 14 | `FB Engagers 30D` | Facebook | Alle Interaktionen | 30 Tage |

---

### **4. Lookalike Audiences (nach Custom Audiences)**

| Basierend auf | Lookalike Name | Location | Größe |
|---------------|----------------|----------|-------|
| Purchasers 180D | `LL 1% Purchasers 180D` | Deutschland | 1% |
| Purchasers 180D | `LL 1-3% Purchasers 180D` | Deutschland | 1-3% |
| Video 95% 30D | `LL 1% Video 95% 30D` | Deutschland | 1% |

---

## **Alternative: CSV für Bulk-Upload**

Soll ich dir eine CSV-Datei erstellen, die du importieren kannst? Oder ein Google Sheet mit allen Details?

Oder hast du Zugriff auf die Meta Marketing API? Dann könnte ich ein n8n-Workflow bauen, der die Audiences automatisch erstellt.
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 11:04 UTC] mach mir ein google sheet
assistant: Ich erstelle dir ein Google Sheet mit allen Custom Audiences. Dafür brauche ich aber den Google Workspace Skill:
assistant: Ich sehe, `gog` braucht OAuth-Setup. Da das nicht konfiguriert ist, erstelle ich dir stattdessen eine CSV-Datei, die du einfach in Google Sheets importieren kannst:
assistant: Fertig! 📊

Ich habe dir eine CSV-Datei erstellt: `meta-ads-custom-audiences.csv`

**So importierst du sie in Google Sheets:**

1. Google Sheets öffnen
2. Datei → Importieren → Upload
3. CSV hochladen
4. Trennzeichen: Komma
5. Fertig!

**Die Datei enthält:**
- 19 Custom Audiences (Hot/Warm/Cold)
- 4 Exclusion-Audiences
- Alle Details: Typ, Quelle, Zeitfenster, Nutzung, Priorität

**Spalten:**
- Audience Name
- Typ (Website/Engagement/Lookalike)
- Quelle/Event
- Zeitfenster
- Location
- Größe (bei Lookalikes)
- Nutzung
- Priorität
- Exclusions

Soll ich noch ein zweites Sheet mit der Campaign-Struktur dazu packen?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 11:05 UTC] https://docs.google.com/spreadsheets/d/11kOXYGGO7HoJMa2jQdgd1A0a0WSwHK7vuU56JKWT_UQ/edit?usp=sharing
assistant: Ich sehe den Link zu deinem Google Sheet. Soll ich die Custom Audiences Daten direkt in dein Sheet schreiben?

Dafür bräuchte ich aber entweder:
1. **gog** eingerichtet (Google Workspace CLI) — ist nicht konfiguriert
2. Oder du gibst mir **Schreibzugriff** auf das Sheet und ich erstelle dir die Struktur manuell

**Alternative:** Ich erstelle dir hier ein komplettes Setup-Dokument mit allen Tabellen, das du kopieren & einfügen kannst:

- Tab 1: Custom Audiences
- Tab 2: Campaign Struktur  
- Tab 3: Creative Testing Matrix
- Tab 4: KPI Benchmarks

Was bevorzugst du?
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Fri 2026-03-20 11:05 UTC] richte gog ein
assistant: Ich richte gog für dich ein. Dafür brauchen wir ein Google Cloud Projekt mit OAuth Credentials.

Hier ist der Schritt-für-Schritt Plan:

---

## **Google Cloud Setup für gog**

### **Schritt 1: Google Cloud Console**
1. Gehe zu https://console.cloud.google.com/
2. Erstelle ein neues Projekt (z.B. "openclaw-gog")
3. Aktiviere die APIs:
   - Google Sheets API
   - Google Drive API
   - Gmail API (optional)
   - Google Calendar API (optional)

### **Schritt 2: OAuth Credentials erstellen**
1. APIs & Services → Credentials
2. Create Credentials → OAuth client ID
3. Application type: **Desktop app**
4. Name: "gog-cli"
5. Download → `client_secret.json`

### **Schritt 3: gog konfigurieren**
```bash
gog auth credentials /path/to/client_secret.json
gog auth add deine.email@gmail.com --services drive,sheets
```

---

**Hast du bereits:**
- Ein Google Cloud Projekt?
- OAuth Credentials erstellt?
- Die APIs aktiviert?

Oder soll ich dir bei einem der Schritte helfen?

Sobald das läuft, kann ich direkt in dein Sheet schreiben! 🚀
