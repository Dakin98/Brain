#!/usr/bin/env python3
"""
Airtable: Fehlende Felder mit korrekten Farben anlegen
"""
import urllib.request, os, json

BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tbluuOSL8CTyIo0Ng"

def create_field(name, field_type, options=None):
    url = f'https://gateway.maton.ai/airtable/v0/meta/bases/{BASE_ID}/tables/{TABLE_ID}/fields'
    
    data = {"name": name, "type": field_type}
    if options:
        data["options"] = options
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method='POST')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())
    except Exception as e:
        return {"error": str(e)}

print("🔄 Erstelle fehlende Felder...\n")

# Services (korrekte Airtable Farben)
print("📋 Services...")
result = create_field("Services", "multipleSelects", {
    "choices": [
        {"name": "Email Marketing", "color": "blueLight2"},
        {"name": "Paid Ads", "color": "greenLight2"},
        {"name": "Website", "color": "purpleLight2"},
        {"name": "Cold Mail", "color": "orangeLight2"}
    ]
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# Health Score (einfacher Number ohne min/max)
print("📋 Health Score...")
result = create_field("Health Score", "number")
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# Churn Risk
print("📋 Churn Risk...")
result = create_field("Churn Risk", "singleSelect", {
    "choices": [
        {"name": "Low", "color": "greenLight2"},
        {"name": "Medium", "color": "yellowLight2"},
        {"name": "High", "color": "redLight2"}
    ]
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# Assigned Team
print("📋 Assigned Team...")
result = create_field("Assigned Team", "multipleSelects", {
    "choices": [
        {"name": "Deniz", "color": "blueLight2"},
        {"name": "VA", "color": "greenLight2"},
        {"name": "Freelancer", "color": "purpleLight2"}
    ]
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

print("\n✅ Fertig!")
