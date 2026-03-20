=HYPERLINK("https://docs.google.com/spreadsheets/d/1TEMPLATE_ID/edit?usp=sharing","Iron Media Dashboard - Template")

INSTRUCTIONS:
1. Open Google Sheets
2. Create new spreadsheet
3. Copy the structure below into Sheet1
4. Set up conditional formatting as described
5. Save and use!

---

SHEET STRUCTURE:

Row 1 (Headers):
A1: Metric | B1: Gestern | C1: Letzte 7 Tage | D1: Letzte 30 Tage | E1: Ziel | F1: Status | G1: Trend

Row 2 (ncROAS):
A2: ncROAS
B2: 2.3
C2: 2.1
D2: 2.0
E2: 2.0
F2: =IF(B2>E2,"🟢 Gut",IF(B2>E2*0.8,"🟡 Okay","🔴 Kritisch"))
G2: =IF(B2>C2,"📈",IF(B2<C2,"📉","➡️"))

Row 3 (Payback Period):
A3: Payback Period (Tage)
B3: 18
C3: 22
D3: 25
E3: 30
F3: =IF(B3<E3,"🟢 Gut",IF(B3<E3*2,"🟡 Okay","🔴 Kritisch"))
G3: =IF(B3<C3,"📈",IF(B3>C3,"📉","➡️"))

Row 4 (LTV/CAC):
A4: LTV/CAC Ratio
B4: 4.2
C4: 4.0
D4: 3.8
E4: 3.5
F4: =IF(B4>E4,"🟢 Gut",IF(B4>E4*0.8,"🟡 Okay","🔴 Kritisch"))
G4: =IF(B4>C4,"📈",IF(B4<C4,"📉","➡️"))

Row 5 (MER):
A5: MER
B5: 4.5
C5: 4.2
D5: 4.0
E5: 4.0
F5: =IF(B5>E5,"🟢 Gut",IF(B5>E5*0.8,"🟡 Okay","🔴 Kritisch"))
G5: =IF(B5>C5,"📈",IF(B5<C5,"📉","➡️"))

Row 6 (Contribution Margin):
A6: Contribution Margin (%)
B6: 0.28
C6: 0.26
D6: 0.24
E6: 0.20
F6: =IF(B6>E6,"🟢 Gut",IF(B6>E6*0.8,"🟡 Okay","🔴 Kritisch"))
G6: =IF(B6>C6,"📈",IF(B6<C6,"📉","➡️"))

---

CONDITIONAL FORMATTING (Optional but recommended):

For Column F (Status):
- Format cells containing "🟢" → Green background
- Format cells containing "🟡" → Yellow background  
- Format cells containing "🔴" → Red background

For Column B (Gestern):
- Apply color scale from red (low) to green (high)
- Except for Payback Period (reverse: green = low, red = high)

---

DASHBOARD VIEW:

Add a second sheet called "Dashboard" with this formula:

A1: IRON MEDIA DASHBOARD
A3: Last Updated: =NOW()

A5: Metric
B5: Current
C5: Target
D5: Status
E5: Trend

A6: =Sheet1!A2
B6: =Sheet1!B2
C6: =Sheet1!E2
D6: =Sheet1!F2
E6: =Sheet1!G2

(Copy down for rows 6-10)

---

CHARTS:

Insert → Chart:
- Type: Line chart
- Data range: Sheet1!A1:D6
- Title: "30-Day Trend"

Insert → Chart:
- Type: Gauge chart
- Data range: Sheet1!A2:B6
- Title: "Current Performance"

---

USAGE:

1. Every morning, update column B (Gestern) with yesterday's data
2. Columns F and G update automatically
3. Check for any 🔴 (Kritisch) metrics
4. Take action on red metrics
5. Review trends (📈📉➡️)

---

EXAMPLE DATA:

ncROAS: 2.3 | 2.1 | 2.0 | 2.0 | 🟢 | 📈
Payback: 18 | 22 | 25 | 30 | 🟢 | 📈
LTV/CAC: 4.2 | 4.0 | 3.8 | 3.5 | 🟢 | 📈
MER: 4.5 | 4.2 | 4.0 | 4.0 | 🟢 | 📈
Margin: 28% | 26% | 24% | 20% | 🟢 | 📈

All green = All good! 🎉
