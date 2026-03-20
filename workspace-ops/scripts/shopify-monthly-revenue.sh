#!/bin/bash
# Pull monthly revenue from Shopify and calculate commission
# Input: JSON via stdin with fields: shop_url, access_token, year, month
# Output: JSON with total_revenue, order_count

set -e

INPUT=$(cat)
SHOP_URL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('shop_url',''))")
ACCESS_TOKEN=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")
YEAR=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('year',''))")
MONTH=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('month',''))")

if [ -z "$SHOP_URL" ] || [ -z "$ACCESS_TOKEN" ]; then
  echo '{"error": "Missing shop_url or access_token"}' >&2
  exit 1
fi

# Clean shop URL (remove https:// and trailing /)
SHOP=$(echo "$SHOP_URL" | sed 's|https://||' | sed 's|/$||')

# Calculate date range
START_DATE="${YEAR}-$(printf '%02d' $MONTH)-01T00:00:00+00:00"
# Next month
if [ "$MONTH" -eq 12 ]; then
  END_DATE="$((YEAR + 1))-01-01T00:00:00+00:00"
else
  END_DATE="${YEAR}-$(printf '%02d' $((MONTH + 1)))-01T00:00:00+00:00"
fi

# Fetch orders with pagination
PAGE_URL="https://${SHOP}/admin/api/2024-01/orders.json?status=any&created_at_min=${START_DATE}&created_at_max=${END_DATE}&limit=250&fields=id,total_price,financial_status,created_at"

TOTAL_REVENUE=0
ORDER_COUNT=0
PAGE=1

while [ -n "$PAGE_URL" ]; do
  RESPONSE=$(curl -s "$PAGE_URL" \
    -H "X-Shopify-Access-Token: $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -D /tmp/shopify_headers_$$.txt)

  # Parse orders and sum revenue (only paid/partially_refunded, exclude cancelled/refunded)
  RESULT=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
orders = data.get('orders', [])
total = 0
count = 0
for o in orders:
    fs = o.get('financial_status', '')
    if fs in ('paid', 'partially_paid', 'partially_refunded'):
        total += float(o.get('total_price', 0))
        count += 1
print(f'{total:.2f},{count}')
")

  REV=$(echo "$RESULT" | cut -d, -f1)
  CNT=$(echo "$RESULT" | cut -d, -f2)
  TOTAL_REVENUE=$(python3 -c "print(round($TOTAL_REVENUE + $REV, 2))")
  ORDER_COUNT=$((ORDER_COUNT + CNT))

  # Check for next page (Link header)
  NEXT_URL=$(grep -i '^link:' /tmp/shopify_headers_$$.txt 2>/dev/null | grep 'rel="next"' | sed 's/.*<\(.*\)>.*/\1/' || echo "")
  PAGE_URL="$NEXT_URL"
  PAGE=$((PAGE + 1))
done

rm -f /tmp/shopify_headers_$$.txt

echo "✅ $SHOP: ${TOTAL_REVENUE}€ revenue, $ORDER_COUNT orders ($YEAR-$(printf '%02d' $MONTH))" >&2

cat << EOF
{
  "shop": "$SHOP",
  "year": $YEAR,
  "month": $MONTH,
  "total_revenue": $TOTAL_REVENUE,
  "order_count": $ORDER_COUNT
}
EOF
