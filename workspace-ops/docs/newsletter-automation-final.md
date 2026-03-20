# Newsletter Automation - Final Documentation

## Status: ✅ WORKING (as of 2026-02-24)

## Overview

Automated weekly newsletter creation for Razeco via Notion → Klaviyo → ClickUp pipeline.

## Architecture

```
Notion (eCom Email Calendar)
  ↓ Themes/Topics per week
Airtable (adsdrop Hub)
  ↓ Client data, Klaviyo API keys, Brand Assets
Klaviyo API
  ↓ Template → Campaign → Assign Template
ClickUp
  ↓ Task with checklist for manual review
```

## Components

### 1. Notion Calendar
- **DB ID**: `3465a32b-e5e0-4d52-bec3-c24ff39e1507`
- **Fields**: Name (title), Date (date), Email Type (multi_select)
- **Content**: 177 newsletter themes as yearly calendar

### 2. Airtable (Client Data)
- **Base**: `appbGhxy9I18oIS8E`
- **Table**: Kunden
- **Key Fields**: Firmenname, Klaviyo API Key, Klaviyo Newsletter List ID, Brand Colors, Brand Fonts, Brand Tone, USPs, Produkte JSON, Lifestyle Images, Klaviyo Logo URL

### 3. Klaviyo Campaign Creation
- **Script**: `scripts/klaviyo_create_campaign_complete.py`
- **Automation**: `scripts/newsletter_automation_v3.py`
- **API**: Direct Klaviyo API v2024-10-15
- **Workflow**: Create Template → Create Campaign → Assign Template to Campaign Message
- **Important**: Campaigns are created as DRAFT — must be scheduled manually in Klaviyo UI

### 4. ClickUp Task Management
- **Script**: `scripts/newsletter-weekly-task.sh`
- **Razeco Folder**: 901514522405
- **Email Content List**: 901521370174
- **Checklist**: 9 items covering full review → send → performance cycle

### 5. HTML Templates
- **Location**: `newsletters/`
- **Razeco Templates**:
  - `razeco_recommended_products.html` — Product recommendations
  - `razeco_faq.html` — FAQ email
  - `razeco_show_the_future.html` — Brand story / sustainability
  - `razeco_womens_day_2026.html` — International Women's Day (March 8)
- **Design**: Razeco brand colors (#0C5132 primary, #48413C dark, #F5F4F0 bg), Georgia + Plus Jakarta Sans fonts

## Razeco Configuration

| Setting | Value |
|---------|-------|
| Klaviyo API Key | `pk_dfc4dd8deb22827d0244a251f315db13c3` |
| Newsletter List ID | `ThKApp` |
| From Email | `hello@razeco.de` |
| From Label | `Razeco` |
| Logo URL | `https://d3k81ch9hvuctc.cloudfront.net/company/XjLDhQ/images/cf8d0958-9062-4a99-aea3-fe36c89695ae.png` |
| Brand Tagline | shave the future. |

## Current Campaign (Created 2026-02-24)

| Field | Value |
|-------|-------|
| Campaign Name | Razeco \| Internationaler Frauentag \| 2026-03-08 |
| Campaign ID | `01KJ7HFVZ4TG6RSVRC0D9VJ45A` |
| Template ID | `QZRBrh` (assigned clone: `TkFhcZ`) |
| Message ID | `01KJ7HFVZ4TG6RSVRC0D9VJ45A` |
| Subject | Für starke Frauen, die Zukunft gestalten 💚 |
| Preview | Heute feiern wir dich — und deine bewussten Entscheidungen |
| Send Date | 2026-03-08 09:00 UTC |
| Status | DRAFT |
| Klaviyo URL | https://www.klaviyo.com/campaign/01KJ7HFVZ4TG6RSVRC0D9VJ45A/edit |
| ClickUp Task | https://app.clickup.com/t/86c8e3yqw |

## Cron Jobs

### Newsletter Weekly Automation
- **Schedule**: Every Monday 9:00 AM
- **Cron ID**: `dbcb229e` (from MEMORY.md)
- **Script**: `scripts/notion-weekly-newsletters.sh`
- **What it does**: Pulls Notion themes → generates personalized newsletters → creates Klaviyo campaigns

### Newsletter Weekly Task Creation
- **Script**: `scripts/newsletter-weekly-task.sh`
- **What it does**: Creates ClickUp tasks with checklists for each active newsletter client
- **Requires**: Airtable fields `Newsletter Service`, `Newsletter Onboarding Done`, `Status = Aktiv`

## Manual Steps Required

1. **Before send date**: Open Klaviyo campaign → Review content → Click "Schedule"
2. **After sending**: Check performance (Opens, Clicks, Revenue) within 48h
3. **Weekly**: Review Notion calendar for upcoming themes

## Known Issues

- Klaviyo API `page[size]` parameter causes 400 error (use URL-encoded `page%5Bsize%5D` or omit)
- Campaigns can only be scheduled/sent from Klaviyo UI (safety feature)
- Template gets cloned when assigned — the returned template ID differs from the original
