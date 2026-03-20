---
name: cal-com-api
description: Cal.com API integration for booking management, availability, and event types. Use when users want to manage appointments, check availability, or handle bookings.
metadata:
  openclaw:
    emoji: 🗓️
    requires:
      env:
        - CALCOM_API_KEY
---

# Cal.com API Integration

Access Cal.com bookings, availability, event types, and user management via REST API.

## Setup

1. Get your API key from [Cal.com Settings → Developer → API Keys](https://app.cal.com/settings/developer/api-keys)
2. Set the environment variable:
   ```bash
   export CALCOM_API_KEY=your-api-key-here
   ```

## Base URL

```
https://api.cal.com/v1
```

## Authentication

All requests require the API key as a query parameter:
```
?apiKey=${CALCOM_API_KEY}
```

## Common Operations

### Get User Profile
```bash
curl "https://api.cal.com/v1/me?apiKey=${CALCOM_API_KEY}"
```

### List Event Types
```bash
curl "https://api.cal.com/v1/event-types?apiKey=${CALCOM_API_KEY}"
```

### List Bookings
```bash
curl "https://api.cal.com/v1/bookings?apiKey=${CALCOM_API_KEY}"
```

### Get Availability
```bash
curl "https://api.cal.com/v1/availability?apiKey=${CALCOM_API_KEY}&dateFrom=2024-01-01&dateTo=2024-01-31"
```

### Create Booking
```bash
curl -X POST "https://api.cal.com/v1/bookings?apiKey=${CALCOM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "eventTypeId": 123,
    "start": "2024-01-15T10:00:00Z",
    "end": "2024-01-15T11:00:00Z",
    "attendee": {
      "email": "client@example.com",
      "name": "John Doe"
    }
  }'
```

### Update Booking
```bash
curl -X PATCH "https://api.cal.com/v1/bookings/{bookingId}?apiKey=${CALCOM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "cancelled"
  }'
```

## Use Cases

### For Performance Marketing Agency:
- **Client Onboarding Calls** - Schedule discovery meetings
- **Strategy Sessions** - Recurring client check-ins  
- **Report Reviews** - Monthly performance meetings
- **Team Availability** - Internal coordination

## Error Handling

- 401: Invalid or missing API key
- 403: Insufficient permissions
- 404: Resource not found
- 429: Rate limit exceeded

## Rate Limits

Cal.com API has rate limiting. Respect the limits and implement proper error handling.