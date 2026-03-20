#!/bin/bash
# Quick Apollo Test - Simplified lead search

APOLLO_KEY="RoLkmFA66R7Dxk5nlnLy2g"

echo "🚀 Apollo Quick Test"
echo ""

# Test Search
echo "📡 Searching for Fashion CEOs in Germany..."
curl -s -X POST "https://api.apollo.io/api/v1/mixed_people/api_search" \
  -H "X-Api-Key: ${APOLLO_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "person_titles": ["CEO", "Founder"],
    "person_locations": ["Germany"],
    "per_page": 10
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"✅ Found {data.get('total_entries', 0)} total leads\")
print()
print('Sample leads:')
print('-' * 60)
for i, person in enumerate(data.get('people', [])[:5], 1):
    name = f\"{person.get('first_name', '')} {person.get('last_name', '')}\".strip()
    title = person.get('title', 'N/A')
    company = person.get('organization', {}).get('name', 'N/A')
    has_email = '✉️' if person.get('has_email') else '❌'
    print(f\"{i}. {name}\")
    print(f\"   Title: {title}\")
    print(f\"   Company: {company}\")
    print(f\"   Has Email: {has_email}\")
    print()
"