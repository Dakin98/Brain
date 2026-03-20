# Klaviyo Skill

## Overview

Complete Klaviyo API v2024-10-15 integration for email marketing automation.

## Quick Start

```python
from scripts.klaviyo_manager import KlaviyoClient, KlaviyoConfig

config = KlaviyoConfig(api_key="pk_...")
client = KlaviyoClient(config)

# List all templates
templates = client.list_templates()

# Create newsletter
template, campaign = client.create_newsletter_workflow(newsletter_config)
```

## Base URL

```
https://a.klaviyo.com/api
```

## Authentication

- Header: `Authorization: Klaviyo-API-Key {api_key}`
- Revision Header: `revision: 2024-10-15` (required for all requests)

## Maton Gateway

```
https://gateway.maton.ai/klaviyo/v1/{endpoint}
```

Auth via: `Authorization: Bearer $MATON_API_KEY`

⚠️ **Note**: Currently redirects to login page - use direct API instead.

---

## API Endpoints

### Templates

#### Create Template
```bash
POST /api/templates
```

Request:
```json
{
  "data": {
    "type": "template",
    "attributes": {
      "name": "Template Name",
      "editor_type": "CODE",
      "html": "<html>...</html>",
      "text": "Plain text version"
    }
  }
}
```

Response:
```json
{
  "data": {
    "type": "template",
    "id": "RnsdjY",
    "attributes": {
      "name": "Template Name",
      "editor_type": "CODE",
      "html": "...",
      "text": "...",
      "created": "2026-02-23T15:46:45+00:00",
      "updated": "2026-02-23T15:46:45+00:00"
    },
    "links": {
      "self": "https://a.klaviyo.com/api/templates/RnsdjY/"
    }
  }
}
```

#### Get Template
```bash
GET /api/templates/{template_id}
```

#### List Templates
```bash
GET /api/templates?page[size]=100
```

#### Update Template
```bash
PATCH /api/templates/{template_id}
```

Request:
```json
{
  "data": {
    "type": "template",
    "id": "RnsdjY",
    "attributes": {
      "name": "New Name",
      "html": "<new html>..."
    }
  }
}
```

#### Delete Template
```bash
DELETE /api/templates/{template_id}
```

---

### Campaigns

#### Create Campaign
```bash
POST /api/campaigns
```

Request:
```json
{
  "data": {
    "type": "campaign",
    "attributes": {
      "name": "Campaign Name | 2026-02-26",
      "audiences": {
        "included": ["ThKApp"],
        "excluded": []
      },
      "send_strategy": {
        "method": "static",
        "options_static": {
          "datetime": "2026-02-26T09:00:00Z",
          "is_local": false
        }
      },
      "send_options": {
        "use_smart_sending": true,
        "ignore_unsubscribes": false
      },
      "tracking_options": {
        "add_tracking_params": false,
        "is_tracking_clicks": true,
        "is_tracking_opens": true
      },
      "campaign-messages": {
        "data": [{
          "type": "campaign-message",
          "attributes": {
            "channel": "email",
            "label": "Default",
            "content": {
              "subject": "Email Subject 🌱",
              "preview_text": "Preview text",
              "from_email": "hello@razeco.de",
              "from_label": "Razeco",
              "reply_to_email": null,
              "cc_email": null,
              "bcc_email": null
            }
          }
        }]
      }
    }
  }
}
```

Response:
```json
{
  "data": {
    "type": "campaign",
    "id": "01KJ5P46QY4H6PN32Q9RJE4F6N",
    "attributes": {
      "name": "Campaign Name | 2026-02-26",
      "status": "Draft",
      "archived": false,
      "audiences": {"included": ["ThKApp"], "excluded": []},
      "send_strategy": {
        "method": "static",
        "options_static": {
          "datetime": "2026-02-26T09:00:00+00:00",
          "is_local": false
        }
      },
      "created_at": "2026-02-23T16:43:08.417512+00:00",
      "updated_at": "2026-02-23T16:43:08.513728+00:00"
    },
    "relationships": {
      "campaign-messages": {
        "data": [{"type": "campaign-message", "id": "01KJ5P46RB1VPSPY500E7MKBMF"}]
      }
    }
  }
}
```

#### Get Campaign
```bash
GET /api/campaigns/{campaign_id}
```

#### List Campaigns
```bash
GET /api/campaigns?page[size]=100
```

Query params:
- `page[size]`: Items per page (default: 100)
- `page[cursor]`: Pagination cursor
- `filter`: Filter results

#### Update Campaign
```bash
PATCH /api/campaigns/{campaign_id}
```

Updateable fields:
- `name`
- `audiences`
- `send_strategy`
- `send_options`
- `tracking_options`

#### Delete Campaign
```bash
DELETE /api/campaigns/{campaign_id}
```

#### Schedule Campaign
```bash
POST /api/campaign-send-jobs
```

Request:
```json
{
  "data": {
    "type": "campaign-send-job",
    "attributes": {
      "campaign_id": "01KJ5P46QY4H6PN32Q9RJE4F6N"
    }
  }
}
```

---

### Campaign Messages

#### Get Message
```bash
GET /api/campaign-messages/{message_id}
```

Response:
```json
{
  "data": {
    "type": "campaign-message",
    "id": "01KJ5P46RB1VPSPY500E7MKBMF",
    "attributes": {
      "label": "Default",
      "channel": "email",
      "content": {
        "subject": "Subject",
        "preview_text": "Preview",
        "from_email": "hello@razeco.de",
        "from_label": "Razeco"
      },
      "send_times": [],
      "render_options": null,
      "created_at": "2026-02-23T16:43:08.432012+00:00",
      "updated_at": "2026-02-23T16:43:08.524179+00:00"
    },
    "relationships": {
      "campaign": {"data": {"type": "campaign", "id": "01KJ5P46QY4H6PN32Q9RJE4F6N"}},
      "template": {"data": {"type": "template", "id": "RnsdjY"}}
    }
  }
}
```

#### Assign Template to Campaign Message ⭐
```bash
POST /api/campaign-message-assign-template
```

⚠️ **IMPORTANT**: This is the ONLY way to link a template via API!

Request:
```json
{
  "data": {
    "type": "campaign-message",
    "id": "01KJ5P46RB1VPSPY500E7MKBMF",
    "relationships": {
      "template": {
        "data": {
          "type": "template",
          "id": "RnsdjY"
        }
      }
    }
  }
}
```

Response:
```json
{
  "data": {
    "type": "campaign-message",
    "id": "01KJ5P46RB1VPSPY500E7MKBMF",
    "relationships": {
      "template": {
        "data": {
          "type": "template",
          "id": "UVasWZ"
        }
      }
    }
  },
  "included": [{
    "type": "template",
    "id": "UVasWZ",
    "attributes": {
      "name": "Clone of RnsdjY",
      "html": "...",
      "text": "..."
    }
  }]
}
```

Note: Klaviyo creates a CLONE of your template, the ID will be different!

#### Update Message Content
```bash
PATCH /api/campaign-messages/{message_id}
```

Allowed fields:
```json
{
  "data": {
    "type": "campaign-message",
    "id": "01KJ5P46RB1VPSPY500E7MKBMF",
    "attributes": {
      "content": {
        "subject": "New Subject",
        "preview_text": "New Preview",
        "from_email": "new@razeco.de",
        "from_label": "New Label"
      }
    }
  }
}
```

---

### Lists/Audiences

#### List Lists
```bash
GET /api/lists?page[size]=100
```

Response:
```json
{
  "data": [{
    "type": "list",
    "id": "ThKApp",
    "attributes": {
      "name": "Newsletter",
      "created": "2024-01-15T10:30:00+00:00",
      "updated": "2026-02-20T14:22:00+00:00"
    }
  }]
}
```

#### Get List
```bash
GET /api/lists/{list_id}
```

#### Create List
```bash
POST /api/lists
```

Request:
```json
{
  "data": {
    "type": "list",
    "attributes": {
      "name": "New List Name"
    }
  }
}
```

---

### Images

#### List Images
```bash
GET /api/images?page[size]=100
```

Response:
```json
{
  "data": [{
    "type": "image",
    "id": "165129455",
    "attributes": {
      "name": "Logo Stacked",
      "image_url": "https://d3k81ch9hvuctc.cloudfront.net/company/XjLDhQ/images/2488aa86-d9b4-44f6-abe2-278a70f1ee0e.png",
      "format": "png",
      "size": 2251,
      "hidden": false,
      "updated_at": "2024-08-22T10:55:55+00:00"
    }
  }]
}
```

#### Upload Image
```bash
POST /api/images
```

Requires multipart/form-data:
```bash
curl -X POST 'https://a.klaviyo.com/api/images' \
  -H "Authorization: Klaviyo-API-Key ${KLAVIYO_API_KEY}" \
  -H 'revision: 2024-10-15' \
  -F 'file=@/path/to/image.png' \
  -F 'name=My Image'
```

---

### Metrics

#### Get Metrics
```bash
GET /api/metrics?page[size]=100
```

#### Query Metric Aggregates
```bash
POST /api/metric-aggregates
```

---

### Profiles

#### List Profiles
```bash
GET /api/profiles?page[size]=100
```

#### Get Profile
```bash
GET /api/profiles/{profile_id}
```

#### Create/Update Profile
```bash
POST /api/profile-import
```

---

### Segments

#### List Segments
```bash
GET /api/segments?page[size]=100
```

#### Create Segment
```bash
POST /api/segments
```

---

## Email Design Standards

### Layout
```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
</head>
<body style="margin:0;padding:0;background-color:#F5F4F0;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
    <tr>
      <td align="center">
        <table width="600" style="background-color:#FFFFFF;max-width:600px;">
          <!-- Content -->
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

### Width
- Desktop: 600px max
- Mobile: 100% fluid

### Razeco Brand Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Primary Green | `#0C5132` | CTAs, headers |
| Dark Brown | `#48413C` | Headlines, dark sections |
| Light Beige | `#F5F4F0` | Background, light text |
| Medium Gray | `#696255` | Body text |
| Light Gray | `#C7C5BB` | Secondary text |
| Border | `#ECEAE4` | Borders, dividers |

### Typography
- Headlines: `Georgia, 'DM Serif Display', serif`
- Body: `Arial, 'Plus Jakarta Sans', sans-serif`
- Tagline: `'DM Sans', Arial, sans-serif`

### Klaviyo Variables
```html
{{first_name|default:"Freund"}}
{{email}}
{{organization.name}}
{% unsubscribe_link %}
{% update_preferences_link %}
```

---

## Workflow: Complete Newsletter Creation - FULLY AUTOMATED ⭐

### Complete Workflow (3 Steps)

```python
#!/usr/bin/env python3
import json
import urllib.request

API_KEY = "pk_..."

# Step 1: Create Template
req = urllib.request.Request(
    'https://a.klaviyo.com/api/templates',
    data=json.dumps({
        "data": {
            "type": "template",
            "attributes": {
                "name": "Newsletter | 2026-02-26",
                "editor_type": "CODE",
                "html": "<html>...</html>",
                "text": "Plain text..."
            }
        }
    }).encode(),
    headers={'Authorization': f'Klaviyo-API-Key {API_KEY}', 'revision': '2024-10-15', 'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    template_id = json.loads(resp.read())['data']['id']

# Step 2: Create Campaign
req = urllib.request.Request(
    'https://a.klaviyo.com/api/campaigns',
    data=json.dumps({
        "data": {
            "type": "campaign",
            "attributes": {
                "name": "Newsletter | 2026-02-26",
                "audiences": {"included": ["ThKApp"], "excluded": []},
                "send_strategy": {"method": "static", "options_static": {"datetime": "2026-02-26T09:00:00Z"}},
                "campaign-messages": {
                    "data": [{
                        "type": "campaign-message",
                        "attributes": {
                            "channel": "email",
                            "label": "Default",
                            "content": {
                                "subject": "Subject",
                                "preview_text": "Preview",
                                "from_email": "hello@razeco.de",
                                "from_label": "Razeco"
                            }
                        }
                    }]
                }
            }
        }
    }).encode(),
    headers={'Authorization': f'Klaviyo-API-Key {API_KEY}', 'revision': '2024-10-15', 'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    campaign_id = result['data']['id']
    message_id = result['data']['relationships']['campaign-messages']['data'][0]['id']

# Step 3: Assign Template to Campaign Message ⭐ THE KEY STEP!
req = urllib.request.Request(
    'https://a.klaviyo.com/api/campaign-message-assign-template',
    data=json.dumps({
        "data": {
            "type": "campaign-message",
            "id": message_id,
            "relationships": {
                "template": {
                    "data": {
                        "type": "template",
                        "id": template_id
                    }
                }
            }
        }
    }).encode(),
    headers={'Authorization': f'Klaviyo-API-Key {API_KEY}', 'revision': '2024-10-15', 'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    print("✅ Template assigned successfully!")
```

### Result
- ✅ Template created
- ✅ Campaign created  
- ✅ Template linked to campaign
- ✅ Ready to schedule in Klaviyo UI

---

## CLI Usage

### Setup
```bash
export KLAVIYO_API_KEY="pk_dfc4dd8deb22827d0244a251f315db13c3"
```

### List Resources
```bash
# List templates
python scripts/klaviyo_manager.py list templates

# List campaigns
python scripts/klaviyo_manager.py list campaigns

# List lists
python scripts/klaviyo_manager.py list lists

# List images
python scripts/klaviyo_manager.py list images
```

### Create Newsletter
```bash
python scripts/klaviyo_manager.py create \
  --name "Razeco | Empfehlungen" \
  --subject "Unsere Empfehlungen für dich 🌱" \
  --preview "Die besten Produkte" \
  --date "2026-02-26" \
  --time "09:00" \
  --html-file "newsletters/razeco_recommended_products.html" \
  --list-id "ThKApp"
```

### Delete Resources
```bash
# Delete template
python scripts/klaviyo_manager.py delete template RnsdjY

# Delete campaign
python scripts/klaviyo_manager.py delete campaign 01KJ5P46...
```

### Campaign Report
```bash
python scripts/klaviyo_manager.py report 01KJ5P46...
```

---

## Common Issues & Solutions

### Issue: `campaign-messages is a required field`
**Solution**: Include `campaign-messages` in create request

### Issue: `Method PATCH not allowed` for template linking
**Solution**: Use `POST /api/campaign-message-assign-template` (not PATCH on relationships!)

### Issue: Cannot update HTML content via API
**Solution**: Use templates - update template HTML, then re-link in UI

### Issue: Datetime timezone confusion
**Solution**: Always use UTC (Z suffix) - Klaviyo converts automatically

### Issue: Campaign stuck in Draft
**Solution**: Must manually schedule or send from Klaviyo UI (safety feature)

### Issue: Template ID changes after assignment
**Solution**: Klaviyo creates a CLONE of your template. The returned ID in the response is the one you need.

---

## API Limits

- Rate limit: 1000 requests/minute
- Max page size: 100
- Max HTML template size: 1MB

---

## References

- [Klaviyo API Docs](https://developers.klaviyo.com/en/reference/api_overview)
- [Template Editor](https://www.klaviyo.com/templates)
- [Campaign Editor](https://www.klaviyo.com/campaigns)
- [Changelog](https://developers.klaviyo.com/en/docs/changelog_)