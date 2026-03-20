# n8n Workflow: Newsletter-Automatisierung

Dieser Workflow automatisiert die wöchentliche Erstellung von personalisierten Newsletter-Kampagnen für alle aktiven Kunden mit Klaviyo-Integration. Er nutzt das verbesserte Python-Script und bietet zusätzliche Funktionen wie Benachrichtigungen und Fehlerbehandlung.

## Workflow-Übersicht

![Workflow-Übersicht](https://i.imgur.com/sEpyT4b.png)

## Grunddaten

- **Name**: Wöchentliche Newsletter-Vorbereitung
- **Aktiv**: Ja
- **Zeitplan**: Jeden Montag um 8:30 Uhr (Europe/Berlin)
- **Timeout**: 10 Minuten

## Nodes

### 1. Schedule Trigger

Dieser Trigger startet den Workflow automatisch.

- **Typ**: Schedule
- **Modus**: Basic
- **Intervall**: Weekly
- **Tag**: Monday
- **Zeit**: 08:30
- **Timezone**: Europe/Berlin

### 2. Airtable: Kunden abrufen

Holt alle aktiven Kunden mit Klaviyo-API-Keys aus der Airtable-Datenbank.

- **Typ**: Airtable
- **Operation**: List Records
- **Base ID**: appbGhxy9I18oIS8E
- **Table**: Kunden
- **Filter Formula**: AND(OR(Status='Aktiv',Status='Onboarding'),{Klaviyo API Key}!='')
- **Return All**: Aktiviert

### 3. Notion: Themen prüfen

Prüft, ob für die aktuelle Woche Newsletter-Themen in Notion vorhanden sind.

- **Typ**: HTTP Request
- **Method**: POST
- **URL**: https://api.notion.com/v1/data_sources/f973c96b-5659-4fd8-97c2-63984dbd89d9/query
- **Authentication**: Bearer Token (aus Notion API Key)
- **Headers**: 
  - `Notion-Version`: 2025-09-03
  - `Content-Type`: application/json
- **Request Body**: `{}`

### 4. Function: Themen filtern

Filtert die Notion-Ergebnisse nach Themen für die aktuelle Woche.

```javascript
const today = new Date();
const nextWeek = new Date();
nextWeek.setDate(today.getDate() + 7);

// Format dates for comparison
const startDate = today.toISOString().split('T')[0];
const endDate = nextWeek.toISOString().split('T')[0];

// Get all entries from Notion
const allEntries = $input.item.results;

// Filter to this week
const thisWeekTopics = [];
for (const entry of allEntries) {
  const props = entry.properties;
  const dateProps = props?.Date?.date;
  
  if (!dateProps || !dateProps.start) continue;
  
  // Map original date to current year
  const originalDate = new Date(dateProps.start);
  const mappedDate = new Date(today.getFullYear(), originalDate.getMonth(), originalDate.getDate());
  const mappedDateStr = mappedDate.toISOString().split('T')[0];
  
  // Check if in current week
  if (mappedDateStr >= startDate && mappedDateStr <= endDate) {
    const name = props?.Name?.title?.map(t => t.plain_text).join('') || '';
    
    thisWeekTopics.push({
      name: name,
      date: mappedDateStr,
      pageId: entry.id
    });
  }
}

// Return result
return { 
  topicsFound: thisWeekTopics.length > 0,
  topics: thisWeekTopics,
  topicsCount: thisWeekTopics.length
};
```

### 5. IF: Themen vorhanden?

Prüft, ob Themen für die aktuelle Woche gefunden wurden.

- **Typ**: IF
- **Condition**: `{{$node["Function: Themen filtern"].json["topicsFound"]}} == true`

### 6. Execute Command: Newsletter-Script

Führt das verbesserte Python-Script aus.

- **Typ**: Execute Command
- **Command**: `cd /Users/denizakin/.openclaw/workspace && python3 scripts/klaviyo-weekly-newsletters-improved.py`
- **Working Directory**: `/Users/denizakin/.openclaw/workspace`
- **Execution Timeout**: 300 (5 Minuten)

### 7. Function: Parse Results

Verarbeitet die Ergebnisse des Python-Scripts.

```javascript
let resultText = $input.item.stdout;

// Extract JSON part
let jsonMatch = resultText.match(/\{[\s\S]*\}/);
if (!jsonMatch) {
  return { 
    success: false, 
    error: "Could not parse JSON output" 
  };
}

try {
  const result = JSON.parse(jsonMatch[0]);
  
  // Create summary
  const summary = {
    success: result.successful > 0,
    topics: result.topics,
    clients: result.clients,
    campaigns: result.successful,
    failed: result.failed,
    campaignsList: result.campaigns.map(c => ({
      client: c.client,
      topic: c.topic,
      subject: c.subject,
      adminUrl: c.admin_url
    }))
  };
  
  return summary;
} catch (error) {
  return { 
    success: false, 
    error: "JSON parsing error: " + error.message 
  };
}
```

### 8. Telegram: Success

Sendet eine Erfolgsmeldung per Telegram.

- **Typ**: Telegram
- **Operation**: Send Message
- **Authentication**: Access Token
- **Chat ID**: 6607099798
- **Text**: 
```
📧 *Newsletter-Vorbereitung abgeschlossen!*

*Woche:* {{$today.format("DD.MM.YYYY")}}
*Themen:* {{$node["Function: Parse Results"].json["topics"]}}
*Kunden:* {{$node["Function: Parse Results"].json["clients"]}}

*Ergebnis:*
✅ {{$node["Function: Parse Results"].json["campaigns"]}} Campaigns erstellt
❌ {{$node["Function: Parse Results"].json["failed"]}} Fehler

Kampagnen-Links:
{% for campaign in $node["Function: Parse Results"].json["campaignsList"].slice(0, 5) %}
• [{{campaign.subject}}]({{campaign.adminUrl}})
{% endfor %}
```
- **Parse Mode**: Markdown

### 9. Telegram: No Topics

Sendet eine Benachrichtigung, wenn keine Themen für die aktuelle Woche gefunden wurden.

- **Typ**: Telegram
- **Operation**: Send Message
- **Authentication**: Access Token
- **Chat ID**: 6607099798
- **Text**: 
```
⚠️ *Keine Newsletter-Themen gefunden!*

Für diese Woche ({{$today.format("DD.MM.YYYY")}} - {{$today.plus(7, 'days').format("DD.MM.YYYY")}}) wurden keine Newsletter-Themen in Notion gefunden.

Bitte Themen im Notion-Kalender anlegen.
```
- **Parse Mode**: Markdown

### 10. Telegram: Error

Sendet eine Fehlermeldung, falls das Script fehlschlägt.

- **Typ**: Telegram
- **Operation**: Send Message
- **Authentication**: Access Token
- **Chat ID**: 6607099798
- **Text**: 
```
❌ *Newsletter-Automatisierung fehlgeschlagen!*

*Fehler:* {{$node["Execute Command: Newsletter-Script"].json["error"]}}

Bitte manuelle Überprüfung durchführen.
```
- **Parse Mode**: Markdown

## Workflow-Verbindungen

1. **Schedule Trigger** → **Airtable: Kunden abrufen**
2. **Airtable: Kunden abrufen** → **Notion: Themen prüfen**
3. **Notion: Themen prüfen** → **Function: Themen filtern**
4. **Function: Themen filtern** → **IF: Themen vorhanden?**
5. **IF: Themen vorhanden? (True)** → **Execute Command: Newsletter-Script**
6. **IF: Themen vorhanden? (False)** → **Telegram: No Topics**
7. **Execute Command: Newsletter-Script** → **Function: Parse Results**
8. **Execute Command: Newsletter-Script (Error)** → **Telegram: Error**
9. **Function: Parse Results** → **Telegram: Success**

## Installation

1. Öffne n8n (http://n8n.adsdrop.de)
2. Erstelle einen neuen Workflow
3. Importiere die JSON-Definition (siehe unten) oder erstelle die Nodes manuell
4. Aktiviere den Workflow

## Workflow-JSON

```json
{
  "name": "Wöchentliche Newsletter-Vorbereitung",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "weeks",
              "triggerAtDay": 1,
              "triggerAtHour": 8,
              "triggerAtMinute": 30
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [
        200,
        300
      ]
    },
    {
      "parameters": {
        "operation": "list",
        "application": "appbGhxy9I18oIS8E",
        "table": "Kunden",
        "filterByFormula": "AND(OR(Status='Aktiv',Status='Onboarding'),{Klaviyo API Key}!='')",
        "returnAll": true
      },
      "name": "Airtable: Kunden abrufen",
      "type": "n8n-nodes-base.airtable",
      "position": [
        400,
        300
      ],
      "credentials": {
        "airtableApi": "Airtable account"
      }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.notion.com/v1/data_sources/f973c96b-5659-4fd8-97c2-63984dbd89d9/query",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "headerParameters": {
          "parameters": [
            {
              "name": "Notion-Version",
              "value": "2025-09-03"
            },
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "options": {}
      },
      "name": "Notion: Themen prüfen",
      "type": "n8n-nodes-base.httpRequest",
      "position": [
        600,
        300
      ],
      "credentials": {
        "httpHeaderAuth": {
          "name": "Authorization",
          "value": "Bearer {{$credentials.notionApi}}"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "const today = new Date();\nconst nextWeek = new Date();\nnextWeek.setDate(today.getDate() + 7);\n\n// Format dates for comparison\nconst startDate = today.toISOString().split('T')[0];\nconst endDate = nextWeek.toISOString().split('T')[0];\n\n// Get all entries from Notion\nconst allEntries = $input.item.results;\n\n// Filter to this week\nconst thisWeekTopics = [];\nfor (const entry of allEntries) {\n  const props = entry.properties;\n  const dateProps = props?.Date?.date;\n  \n  if (!dateProps || !dateProps.start) continue;\n  \n  // Map original date to current year\n  const originalDate = new Date(dateProps.start);\n  const mappedDate = new Date(today.getFullYear(), originalDate.getMonth(), originalDate.getDate());\n  const mappedDateStr = mappedDate.toISOString().split('T')[0];\n  \n  // Check if in current week\n  if (mappedDateStr >= startDate && mappedDateStr <= endDate) {\n    const name = props?.Name?.title?.map(t => t.plain_text).join('') || '';\n    \n    thisWeekTopics.push({\n      name: name,\n      date: mappedDateStr,\n      pageId: entry.id\n    });\n  }\n}\n\n// Return result\nreturn { \n  topicsFound: thisWeekTopics.length > 0,\n  topics: thisWeekTopics,\n  topicsCount: thisWeekTopics.length\n};"
      },
      "name": "Function: Themen filtern",
      "type": "n8n-nodes-base.function",
      "position": [
        800,
        300
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json[\"topicsFound\"]}}",
              "operation": "equals",
              "value2": true
            }
          ]
        }
      },
      "name": "IF: Themen vorhanden?",
      "type": "n8n-nodes-base.if",
      "position": [
        1000,
        300
      ]
    },
    {
      "parameters": {
        "command": "cd /Users/denizakin/.openclaw/workspace && python3 scripts/klaviyo-weekly-newsletters-improved.py",
        "workingDirectory": "/Users/denizakin/.openclaw/workspace",
        "executionTimeout": 300
      },
      "name": "Execute Command: Newsletter-Script",
      "type": "n8n-nodes-base.executeCommand",
      "position": [
        1200,
        200
      ]
    },
    {
      "parameters": {
        "functionCode": "let resultText = $input.item.stdout;\n\n// Extract JSON part\nlet jsonMatch = resultText.match(/\\{[\\s\\S]*\\}/);\nif (!jsonMatch) {\n  return { \n    success: false, \n    error: \"Could not parse JSON output\" \n  };\n}\n\ntry {\n  const result = JSON.parse(jsonMatch[0]);\n  \n  // Create summary\n  const summary = {\n    success: result.successful > 0,\n    topics: result.topics,\n    clients: result.clients,\n    campaigns: result.successful,\n    failed: result.failed,\n    campaignsList: result.campaigns.map(c => ({\n      client: c.client,\n      topic: c.topic,\n      subject: c.subject,\n      adminUrl: c.admin_url\n    }))\n  };\n  \n  return summary;\n} catch (error) {\n  return { \n    success: false, \n    error: \"JSON parsing error: \" + error.message \n  };\n}"
      },
      "name": "Function: Parse Results",
      "type": "n8n-nodes-base.function",
      "position": [
        1400,
        200
      ]
    },
    {
      "parameters": {
        "chatId": "6607099798",
        "text": "📧 *Newsletter-Vorbereitung abgeschlossen!*\n\n*Woche:* {{$today.format(\"DD.MM.YYYY\")}}\n*Themen:* {{$node[\"Function: Parse Results\"].json[\"topics\"]}}\n*Kunden:* {{$node[\"Function: Parse Results\"].json[\"clients\"]}}\n\n*Ergebnis:*\n✅ {{$node[\"Function: Parse Results\"].json[\"campaigns\"]}} Campaigns erstellt\n❌ {{$node[\"Function: Parse Results\"].json[\"failed\"]}} Fehler\n\nKampagnen-Links:\n{% for campaign in $node[\"Function: Parse Results\"].json[\"campaignsList\"].slice(0, 5) %}\n• [{{campaign.subject}}]({{campaign.adminUrl}})\n{% endfor %}",
        "additionalFields": {
          "parse_mode": "Markdown"
        }
      },
      "name": "Telegram: Success",
      "type": "n8n-nodes-base.telegram",
      "position": [
        1600,
        200
      ],
      "credentials": {
        "telegramApi": "Telegram account"
      }
    },
    {
      "parameters": {
        "chatId": "6607099798",
        "text": "⚠️ *Keine Newsletter-Themen gefunden!*\n\nFür diese Woche ({{$today.format(\"DD.MM.YYYY\")}} - {{$today.plus(7, 'days').format(\"DD.MM.YYYY\")}}) wurden keine Newsletter-Themen in Notion gefunden.\n\nBitte Themen im Notion-Kalender anlegen.",
        "additionalFields": {
          "parse_mode": "Markdown"
        }
      },
      "name": "Telegram: No Topics",
      "type": "n8n-nodes-base.telegram",
      "position": [
        1200,
        400
      ],
      "credentials": {
        "telegramApi": "Telegram account"
      }
    },
    {
      "parameters": {
        "chatId": "6607099798",
        "text": "❌ *Newsletter-Automatisierung fehlgeschlagen!*\n\n*Fehler:* {{$node[\"Execute Command: Newsletter-Script\"].json[\"error\"]}}\n\nBitte manuelle Überprüfung durchführen.",
        "additionalFields": {
          "parse_mode": "Markdown"
        }
      },
      "name": "Telegram: Error",
      "type": "n8n-nodes-base.telegram",
      "position": [
        1400,
        400
      ],
      "credentials": {
        "telegramApi": "Telegram account"
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Airtable: Kunden abrufen",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Airtable: Kunden abrufen": {
      "main": [
        [
          {
            "node": "Notion: Themen prüfen",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Notion: Themen prüfen": {
      "main": [
        [
          {
            "node": "Function: Themen filtern",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Function: Themen filtern": {
      "main": [
        [
          {
            "node": "IF: Themen vorhanden?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "IF: Themen vorhanden?": {
      "main": [
        [
          {
            "node": "Execute Command: Newsletter-Script",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Telegram: No Topics",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Execute Command: Newsletter-Script": {
      "main": [
        [
          {
            "node": "Function: Parse Results",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Telegram: Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Function: Parse Results": {
      "main": [
        [
          {
            "node": "Telegram: Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {},
  "versionId": "",
  "id": "",
  "meta": {
    "instanceId": ""
  },
  "tags": []
}
```

## Optionale Erweiterungen

### 1. Kunden-spezifische Themen-Filter

Ein zusätzlicher Node, der Themen basierend auf Kundenbranchen filtert:

```javascript
// This would be added after Function: Themen filtern
const topics = $input.item.topics;
const clients = $input.items[0].json.records; // From Airtable

const clientTopics = [];

for (const client of clients) {
  const branche = client.fields.Branche || "";
  const filteredTopics = topics.filter(topic => {
    // Check if topic is relevant for this client's branche
    // Add your filtering logic here
    return true; 
  });
  
  clientTopics.push({
    client: client.fields.Firmenname,
    topics: filteredTopics
  });
}

return { clientTopicsMap: clientTopics };
```

### 2. Email-Benachrichtigungen

Eine Alternative zur Telegram-Benachrichtigung:

- **Typ**: Send Email
- **Operation**: Send an Email
- **From**: newsletter-system@adsdrop.de
- **To**: deniz@adsdrop.de
- **Subject**: Newsletter-Vorbereitung: {{$node["Function: Parse Results"].json["campaigns"]}} Kampagnen erstellt
- **HTML**: (Ähnlicher Inhalt wie Telegram-Message mit HTML-Formatierung)

### 3. Automatischer Retry bei Fehlern

Ein zusätzlicher Node, der bei bestimmten Fehlern automatisch einen erneuten Versuch startet:

```javascript
// Check error message
const errorMsg = $input.item.error || "";

// If error is related to API rate limiting or temporary network issues
if (errorMsg.includes("rate limit") || errorMsg.includes("network") || errorMsg.includes("timeout")) {
  return { shouldRetry: true, waitMinutes: 30 };
} else {
  return { shouldRetry: false };
}
```

Verbunden mit einem Wait-Node und einem IF-Node, der bei shouldRetry=true den Workflow nach 30 Minuten erneut ausführt.

## Wichtige Hinweise

1. **Pfade anpassen**: Die Pfade zum Python-Script müssen möglicherweise angepasst werden, je nachdem, wo n8n installiert ist und wo das Script liegt.

2. **API-Schlüssel**: Folgende API-Schlüssel müssen in n8n hinterlegt sein:
   - Notion API-Key (für Notion-Abfrage)
   - Telegram Bot Token (für Benachrichtigungen)
   - Airtable API-Key (für Kundendaten)

3. **Webhook-Aktivierung**: Wichtig! Der Workflow muss im n8n-UI aktiviert werden, nachdem er erstellt wurde. Die reine API-Aktivierung reicht nicht aus.

4. **Testing**: Vor der Produktiv-Schaltung sollte der Workflow mit einem einzelnen Kunden und --draft-only Option getestet werden.