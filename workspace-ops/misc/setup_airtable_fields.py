#!/usr/bin/env python3
"""
Airtable: Neue Felder in Kunden-Tabelle anlegen
"""
import urllib.request, os, json

BASE_ID = "appbGhxy9I18oIS8E"
TABLE_ID = "tbluuOSL8CTyIo0Ng"

def create_field(name, field_type, options=None):
    """Erstellt ein neues Feld in Airtable"""
    url = f'https://gateway.maton.ai/airtable/v0/meta/bases/{BASE_ID}/tables/{TABLE_ID}/fields'
    
    data = {
        "name": name,
        "type": field_type
    }
    
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

print("🚀 Erstelle neue Felder in Kunden-Tabelle...\n")

# 1. ClickUp Folder ID
print("📋 ClickUp Folder ID...")
result = create_field("ClickUp Folder ID", "singleLineText")
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 2. ClickUp List IDs
print("📋 ClickUp List IDs...")
result = create_field("ClickUp List IDs", "multilineText")
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 3. Services (Multi-Select)
print("📋 Services...")
result = create_field("Services", "multipleSelects", {
    "choices": [
        {"name": "Email Marketing", "color": "blueBright2"},
        {"name": "Paid Ads", "color": "greenBright2"},
        {"name": "Website", "color": "purpleBright2"},
        {"name": "Cold Mail", "color": "orangeBright2"}
    ]
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 4. Health Score
print("📋 Health Score...")
result = create_field("Health Score", "number", {
    "precision": 0,
    "min": 1,
    "max": 10
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 5. Churn Risk
print("📋 Churn Risk...")
result = create_field("Churn Risk", "singleSelect", {
    "choices": [
        {"name": "Low", "color": "greenBright2"},
        {"name": "Medium", "color": "yellowBright2"},
        {"name": "High", "color": "redBright2"}
    ]
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 6. Letzte Aktivität
print("📋 Letzte Aktivität...")
result = create_field("Letzte Aktivität", "date", {
    "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"}
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 7. Nächstes Meeting
print("📋 Nächstes Meeting...")
result = create_field("Nächstes Meeting", "date", {
    "dateFormat": {"name": "iso", "format": "YYYY-MM-DD"}
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

# 8. Assigned Team
print("📋 Assigned Team...")
result = create_field("Assigned Team", "multipleSelects", {
    "choices": [
        {"name": "Deniz", "color": "blueBright2"},
        {"name": "VA", "color": "greenBright2"},
        {"name": "Freelancer", "color": "purpleBright2"}
    ]
})
print(f"   {'✅' if 'id' in result else '❌'} {result.get('name', result.get('error', 'Fehler'))}")

print("\n🎉 Alle Felder erstellt!")
