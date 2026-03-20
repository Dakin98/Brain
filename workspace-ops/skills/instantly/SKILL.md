# Instantly Cold Email Platform Skill

## Overview

Instantly.ai is a cold email outreach platform with comprehensive API support for automation. The platform allows you to send cold emails at scale, manage campaigns, track leads, and handle replies.

## API Version

**Current Version:** API V2 (latest)  
**Authentication:** Bearer Token  
**Base URL:** `https://api.instantly.ai/api/v2`

⚠️ **Important:** API V1 will be deprecated in 2025. Migrate to V2 as soon as possible.

---

## Authentication

### Bearer Token Authentication

```bash
Authorization: Bearer <YOUR_API_TOKEN>
Content-Type: application/json
```

### API Key Format

API V2 uses UUID format:
```
a10ca1e8-1d6a-4ccc-8b84-84cfc06dcbc7:TjxDZBmsiWUZ
```

### API Scopes

Instantly V2 introduces API scopes for granular control:
- Read access
- Write access
- Campaign management
- Lead management
- Account management

---

## Core Endpoints

### Campaigns

**List Campaigns:**
```bash
GET /campaigns?page=1&limit=10
```

**Create Campaign:**
```bash
POST /campaigns
{
  "name": "My Campaign",
  "campaign_schedule": {
    "schedules": [{
      "name": "My Schedule",
      "timing": {
        "from": "09:00",
        "to": "17:00"
      },
      "days": {},
      "timezone": "Europe/Berlin"
    }]
  }
}
```

**Get Campaign:**
```bash
GET /campaigns/{campaign_id}
```

**Update Campaign:**
```bash
PATCH /campaigns/{campaign_id}
```

**Delete Campaign:**
```bash
DELETE /campaigns/{campaign_id}
```

### Sequences

**Note:** Sequences contain the actual email copy. Even though the field is an array, only the first element is used.

```bash
POST /campaigns/{campaign_id}/sequences
{
  "sequences": [{
    "steps": [
      {
        "step": 1,
        "wait_time": 0,
        "subject": "{{company}} + Meta Ads Question",
        "body": "Hi {{first_name}},..."
      },
      {
        "step": 2,
        "wait_time": 259200,
        "subject": "Re: {{company}} + Meta Ads Question",
        "body": "Quick follow-up..."
      }
    ]
  }]
}
```

### Leads

**Add Lead to Campaign:**
```bash
POST /leads
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "company_name": "Acme Inc",
  "campaign": "campaign_id"
}
```

**Update Lead Status:**
```bash
POST /leads/update-interest-status
{
  "lead_email": "john@example.com",
  "interest_value": 1
}
```

**List Leads:**
```bash
GET /leads?campaign={campaign_id}&page=1&limit=100
```

### Lead Lists

**Create Lead List:**
```bash
POST /lead-lists
{
  "name": "Fashion DACH Leads"
}
```

**Add Leads to List:**
```bash
POST /lead-lists/{list_id}/leads
{
  "leads": [
    {
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Smith"
    }
  ]
}
```

### Accounts (Email Accounts)

**List Accounts:**
```bash
GET /accounts?page=1&limit=10
```

**Get Account:**
```bash
GET /accounts/{account_id}
```

### Analytics

**Get Campaign Stats:**
```bash
GET /campaigns/{campaign_id}/analytics
```

**Search Campaign by Lead Email:**
```bash
GET /campaign/searchbycontact?email=john@example.com
```

---

## Webhooks

### Available Webhook Events

- `email_sent` - Email was sent
- `email_opened` - Lead opened email
- `email_replied` - Lead replied to email
- `email_bounced` - Email bounced
- `lead_interested` - Lead marked as interested
- `campaign_completed` - Campaign finished

### Webhook Payload Format

```json
{
  "timestamp": "2026-02-24T16:30:00.000Z",
  "event_type": "email_opened",
  "campaign_name": "Fashion DACH - März",
  "workspace": "workspace_id",
  "campaign_id": "campaign_id",
  "lead_email": "john@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "company_name": "Acme Inc",
  "website": "https://acme.com",
  "phone": "+1234567890",
  "step": 1,
  "email_account": "sender@yourdomain.com"
}
```

### Setting Up Webhooks

1. Go to Instantly Settings
2. Navigate to Webhooks
3. Add your endpoint URL
4. Select events to listen for

---

## Best Practices

### Cold Email Strategy

**1. Keep Emails Short**
- 50-125 words for best response rates
- Maximum 200 words
- No links in first email
- Pattern interrupts work well

**2. Deliverability First**
- Fix deliverability before testing copy
- Use custom tracking domains
- Set up SPF, DKIM, DMARC
- Warm up accounts before sending

**3. Personalization**
- Reference specific company milestones
- Mention LinkedIn posts
- Use pattern interrupts
- Avoid generic intros like "I noticed your company is growing"

**4. Sequence Structure**
- 3-step sequence recommended
- Step 1: Initial cold email
- Step 2: Follow-up (3 days later)
- Step 3: Break-up (7 days later)

### Technical Best Practices

**1. Rate Limiting**
- Respect rate limits
- Use pagination (limit=100 max)
- Implement exponential backoff

**2. Error Handling**
- Handle 401 (Unauthorized) - Check API key
- Handle 404 (Not Found) - Resource doesn't exist
- Handle 429 (Rate Limited) - Slow down
- Handle 500 (Server Error) - Retry with backoff

**3. Data Management**
- Validate emails before adding
- Use lead lists for organization
- Tag campaigns by ICP/segment
- Regular cleanup of bounced leads

---

## Common Variables for Personalization

Available in email templates:
- `{{first_name}}` - First name
- `{{last_name}}` - Last name
- `{{email}}` - Email address
- `{{company}}` - Company name
- `{{website}}` - Company website
- `{{phone}}` - Phone number
- `{{title}}` - Job title

---

## Benchmarks

### Reply Rates
- **Good:** >5%
- **Average:** 3-5%
- **Poor:** <3%

### Meeting Rates
- **Good:** >1%
- **Average:** 0.5-1%
- **Poor:** <0.5%

### Email Length
- **Best Response:** 50-125 words
- **Good CTR:** ~200 words, 20 lines

---

## Troubleshooting

### 401 Unauthorized
- Check if API key is valid
- Ensure you're using V2 API key
- Verify Bearer token format

### 404 Not Found
- Endpoint doesn't exist
- Check API version
- Verify URL path

### Rate Limiting
- Default limits apply
- Use pagination
- Implement caching

### Deliverability Issues
- Check domain reputation
- Verify SPF/DKIM/DMARC
- Use custom tracking domain
- Warm up new accounts

---

## Integration Examples

### ClickUp Integration

```bash
# When lead replies, create ClickUp task
curl -X POST "https://api.clickup.com/api/v2/list/{list_id}/task" \
  -H "Authorization: {clickup_token}" \
  -d '{
    "name": "🔥 Lead: {{first_name}} {{last_name}}",
    "description": "Reply: {{message}}",
    "custom_fields": [
      {"name": "Email", "value": "{{email}}"},
      {"name": "Company", "value": "{{company}}"}
    ]
  }'
```

### n8n/Make Integration

Use native Instantly modules:
- Add a Lead
- Update Lead Status
- Watch Events (webhooks)

### API + Webhooks Flow

```
1. Add leads via API
2. Campaign sends emails
3. Webhook triggers on reply
4. Automation creates task
5. User follows up manually
```

---

## Resources

- **API Docs:** https://developer.instantly.ai
- **Help Center:** https://help.instantly.ai
- **Blog:** https://instantly.ai/blog

---

## Migration from V1 to V2

1. Generate new V2 API key
2. Update authentication header
3. Update endpoint URLs
4. Test with small batch
5. Migrate gradually

---

**Version:** 1.0  
**Last Updated:** 2026-02-24  
**Skill Location:** `~/.openclaw/workspace/skills/instantly/SKILL.md`
