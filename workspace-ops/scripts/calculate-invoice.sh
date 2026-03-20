#!/bin/bash
# Calculate monthly invoice: MAX(retainer, provision)
# Input: JSON via stdin
# Output: JSON with invoice_amount, is_provision, provision_amount, retainer

set -e
INPUT=$(cat)

echo "$INPUT" | python3 -c "
import sys, json

data = json.load(sys.stdin)
revenue = float(data.get('revenue', 0))
retainer = float(data.get('retainer', 0))
modell = data.get('provisionsmodell', '')
wert = data.get('provision_wert', '0')

try:
    wert_num = float(str(wert).replace(',', '.').replace('%', '').strip())
except:
    wert_num = 0

provision = 0
if modell == '% vom Umsatz' and revenue > 0:
    provision = revenue * (wert_num / 100)
elif modell == 'Fixbetrag pro Monat':
    provision = wert_num
elif modell == 'Keine Provision':
    provision = 0

is_provision = provision > retainer
invoice_amount = max(retainer, provision)

result = {
    'invoice_amount': round(invoice_amount, 2),
    'is_provision': is_provision,
    'provision_amount': round(provision, 2),
    'retainer': retainer,
    'revenue': revenue,
    'description': f'Provision ({wert}% von {revenue:.0f}€ = {provision:.0f}€)' if is_provision else f'Retainer ({retainer:.0f}€ > Provision {provision:.0f}€)'
}
print(json.dumps(result, indent=2))
"
