#!/bin/bash
# Create Stripe subscription for monthly retainer
# Input: JSON via stdin with fields: stripe_customer_id, retainer (EUR amount), laufzeit (months), startdatum (YYYY-MM-DD)
# Creates a price + subscription that auto-cancels after laufzeit months

set -e
STRIPE_KEY="${STRIPE_API_KEY:-YOUR_STRIPE_API_KEY_HERE}"

INPUT=$(cat)
CUSTOMER_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stripe_customer_id',''))")
RETAINER=$(echo "$INPUT" | python3 -c "import sys,json; print(int(float(json.load(sys.stdin).get('retainer', 0)) * 100))")
LAUFZEIT=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('laufzeit', 0))")
STARTDATUM=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('startdatum',''))")
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")

if [ -z "$CUSTOMER_ID" ] || [ "$RETAINER" = "0" ]; then
  echo '{"error": "Missing stripe_customer_id or retainer"}' >&2
  exit 1
fi

# 1. Create a Price (recurring monthly)
PRICE=$(curl -s https://api.stripe.com/v1/prices \
  -u "$STRIPE_KEY:" \
  -d "unit_amount=$RETAINER" \
  -d "currency=eur" \
  -d "recurring[interval]=month" \
  -d "product_data[name]=Monatlicher Retainer - $FIRMENNAME")

PRICE_ID=$(echo "$PRICE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "✅ Price: $PRICE_ID ($RETAINER cents/month)" >&2

# 2. Calculate cancel_at timestamp (startdatum + laufzeit months)
CANCEL_AT=$(python3 -c "
from datetime import datetime, timedelta
import calendar
start = '${STARTDATUM}'
laufzeit = int('${LAUFZEIT}')
if start and laufzeit > 0:
    d = datetime.strptime(start, '%Y-%m-%d')
    # Add laufzeit months
    month = d.month + laufzeit
    year = d.year + (month - 1) // 12
    month = ((month - 1) % 12) + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    end = datetime(year, month, day)
    print(int(end.timestamp()))
else:
    print('')
")

# 3. Calculate billing_cycle_anchor (start date timestamp)
ANCHOR=$(python3 -c "
from datetime import datetime
start = '${STARTDATUM}'
if start:
    d = datetime.strptime(start, '%Y-%m-%d')
    print(int(d.timestamp()))
else:
    print('')
")

# 4. Create Subscription
SUB_ARGS="-d customer=$CUSTOMER_ID -d items[0][price]=$PRICE_ID -d collection_method=send_invoice -d days_until_due=14"

# Add billing anchor if start date is in the future
NOW=$(date +%s)
if [ -n "$ANCHOR" ] && [ "$ANCHOR" -gt "$NOW" ]; then
  SUB_ARGS="$SUB_ARGS -d billing_cycle_anchor=$ANCHOR"
fi

# Add cancel_at if laufzeit is set
if [ -n "$CANCEL_AT" ]; then
  SUB_ARGS="$SUB_ARGS -d cancel_at=$CANCEL_AT"
fi

SUBSCRIPTION=$(eval curl -s https://api.stripe.com/v1/subscriptions \
  -u "$STRIPE_KEY:" \
  $SUB_ARGS)

SUB_ID=$(echo "$SUBSCRIPTION" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id', d.get('error',{}).get('message','UNKNOWN')))")
SUB_STATUS=$(echo "$SUBSCRIPTION" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','error'))")

echo "✅ Subscription: $SUB_ID (status: $SUB_STATUS)" >&2

# Output
cat << EOF
{
  "subscription_id": "$SUB_ID",
  "subscription_status": "$SUB_STATUS",
  "price_id": "$PRICE_ID",
  "retainer_cents": $RETAINER,
  "laufzeit_months": $LAUFZEIT,
  "cancel_at": "$CANCEL_AT",
  "customer_id": "$CUSTOMER_ID"
}
EOF
