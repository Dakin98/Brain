#!/bin/bash
# Create Stripe customer + send setup invoice
# Input: JSON via stdin with fields: firmenname, ansprechpartner, email, setup_gebuehr (cents), retainer (cents)
# Output: JSON with stripe_customer_id, invoice_id, invoice_url

set -e
STRIPE_KEY="${STRIPE_API_KEY:-YOUR_STRIPE_API_KEY_HERE}"

INPUT=$(cat)
FIRMENNAME=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('firmenname',''))")
ANSPRECHPARTNER=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ansprechpartner',''))")
EMAIL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('email',''))")
SETUP_GEBUEHR=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); v=d.get('setup_gebuehr',300000); print(int(float(v)*100) if float(v) < 10000 else int(float(v)))")

if [ -z "$EMAIL" ] || [ -z "$FIRMENNAME" ]; then
  echo '{"error": "Missing email or firmenname"}' >&2
  exit 1
fi

# 1. Create Stripe Customer
CUSTOMER=$(curl -s https://api.stripe.com/v1/customers \
  -u "$STRIPE_KEY:" \
  -d "name=$FIRMENNAME" \
  -d "email=$EMAIL" \
  -d "metadata[ansprechpartner]=$ANSPRECHPARTNER" \
  -d "metadata[source]=adsdrop-onboarding")

CUSTOMER_ID=$(echo "$CUSTOMER" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

if [ -z "$CUSTOMER_ID" ] || [ "$CUSTOMER_ID" = "None" ]; then
  echo "{\"error\": \"Failed to create Stripe customer\", \"details\": $(echo $CUSTOMER)}" >&2
  exit 1
fi

echo "✅ Stripe Customer: $CUSTOMER_ID" >&2

# 2. Create Invoice Item (Setup-Gebühr)
ITEM=$(curl -s https://api.stripe.com/v1/invoiceitems \
  -u "$STRIPE_KEY:" \
  -d "customer=$CUSTOMER_ID" \
  -d "amount=$SETUP_GEBUEHR" \
  -d "currency=eur" \
  -d "description=Einmalige Setup-Gebühr – $FIRMENNAME" \
  -d "metadata[type]=setup")

ITEM_ID=$(echo "$ITEM" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "✅ Invoice Item: $ITEM_ID" >&2

# 3. Create Invoice
INVOICE=$(curl -s https://api.stripe.com/v1/invoices \
  -u "$STRIPE_KEY:" \
  -d "customer=$CUSTOMER_ID" \
  -d "collection_method=send_invoice" \
  -d "days_until_due=14" \
  -d "metadata[type]=setup" \
  -d "metadata[firmenname]=$FIRMENNAME")

INVOICE_ID=$(echo "$INVOICE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "✅ Invoice: $INVOICE_ID" >&2

# 4. Finalize Invoice
curl -s -X POST "https://api.stripe.com/v1/invoices/$INVOICE_ID/finalize" \
  -u "$STRIPE_KEY:" > /dev/null

# 5. Send Invoice to customer
SENT=$(curl -s -X POST "https://api.stripe.com/v1/invoices/$INVOICE_ID/send" \
  -u "$STRIPE_KEY:")

INVOICE_URL=$(echo "$SENT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('hosted_invoice_url',''))")
echo "✅ Invoice sent to $EMAIL" >&2

# Output JSON
cat << EOF
{
  "stripe_customer_id": "$CUSTOMER_ID",
  "invoice_id": "$INVOICE_ID",
  "invoice_url": "$INVOICE_URL",
  "email": "$EMAIL",
  "firmenname": "$FIRMENNAME",
  "setup_gebuehr_cents": $SETUP_GEBUEHR
}
EOF
