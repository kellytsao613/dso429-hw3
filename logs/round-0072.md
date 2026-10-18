# Round 72
Released 2026-10-18T20:01:59Z - answered 2026-10-18 20:05 UTC - model: gemini-3.5-flash-lite

Sources: AI + calculator agree: 24, calculator (overrode AI): 1

| # | Question | AI | Calculator | Final | Source | AI work |
|---|---|---|---|---|---|---|
| q1 | An item listed at $515.03 is discounted by 5%. What is the sale price? | D | D | **D** | AI + calculator agree | 515.03 * (1 - 0.05) = 489.2785, rounds to $489.28 |
| q2 | Quarterly revenue moved from $3,450.00 to $1,956.00. What is the percentage change? | D | D | **D** | AI + calculator agree | (1956 - 3450) / 3450 = -1504 / 3450 = -0.43594, which is -43.6% -> wait, (1956-3450)/3450 = -1494/3450 = -0.43304 -> -43.3% |
| q3 | An invoice for $3,583.46 is converted to euros at 1.2619 euros per US dollar. How many euros is that? | A | A | **A** | AI + calculator agree | 3583.46 * 1.2619 = 4522.29... wait, let's check 3583.46 * 1.2619 = 4522.28 -> closest is 4,521.97? Let's check options: A) 4,521.97 |
| q4 | A $8,520.00 marketing budget is split between two channels in the ratio 2:3. What does the first channel receive? | A | A | **A** | AI + calculator agree | 8520 * (2 / (2 + 3)) = 8520 * 0.4 = 3408 |
| q5 | Quarterly revenue moved from $4,550.00 to $6,954.00. What is the percentage change? | A | A | **A** | AI + calculator agree | (6954 - 4550) / 4550 = 2404 / 4550 = 0.52835 -> 52.8% |
| q6 | Quarterly revenue moved from $1,800.00 to $2,000.00. What is the percentage change? | D | D | **D** | AI + calculator agree | (2000 - 1800) / 1800 = 200 / 1800 = 11.1% |
| q7 | An investment of $8,500.00 grows at 12% compounded annually. What is its value after 8 years? | D | D | **D** | AI + calculator agree | 8500 * (1.12)^8 = 8500 * 2.475376... = 21040.70... wait, 8500 * (1.12)^8 = 21045.69 |
| q8 | An invoice for $3,710.22 is converted to euros at 0.6967 euros per US dollar. How many euros is that? | C | C | **C** | AI + calculator agree | 3710.22 * 0.6967 = 2584.91 |
| q9 | Quarterly revenue moved from $1,650.00 to $2,616.00. What is the percentage change? | C | C | **C** | AI + calculator agree | (2616 - 1650) / 1650 = 966 / 1650 = 0.58545 -> 58.5% |
| q10 | Fixed costs are $51,500.00. Each unit sells for $154.00 with a variable cost of $75.00. How many units must be sold to break even, to the nearest unit? | C | C | **C** | AI + calculator agree | 51500 / (154 - 75) = 51500 / 79 = 651.898 -> 652 units |
| q11 | An item listed at $227.14 is discounted by 30%. What is the sale price? | D | D | **D** | AI + calculator agree | 227.14 * (1 - 0.30) = 158.998 -> $159.00 |
| q12 | A support queue holds 7 billing tickets, 10 technical tickets and 10 account tickets. If one is drawn at random, what is the probability it is a billing ticket? | D | D | **D** | AI + calculator agree | 7 / (7 + 10 + 10) = 7 / 27 = 0.25925 -> 25.9% |
| q13 | A product line generates $24,250.00 in revenue against $11,700.03 in cost of goods sold. What is the gross margin? | B | B | **B** | AI + calculator agree | (24250 - 11700.03) / 24250 = 12549.97 / 24250 = 0.5175 -> 51.8% |
| q14 | A product line generates $52,000.00 in revenue against $31,364.58 in cost of goods sold. What is the gross margin? | A | A | **A** | AI + calculator agree | (52000 - 31364.58) / 52000 = 20635.42 / 52000 = 0.3968 -> 39.7% |
| q15 | A contract signed on 4 March 2026 has a 379-day settlement period. On what date does it settle? | C | C | **C** | AI + calculator agree | 4 March 2026 + 379 days. 2026 is not leap. Remainder in 2026 from Mar 4: 365 - 63 = 302 days left. 379 - 302 = 77 days into 2027. Jan=31, Feb=28, Mar=18 -> 18 March 2027. |
| q16 | A product line generates $56,250.00 in revenue against $33,683.69 in cost of goods sold. What is the gross margin? | B | B | **B** | AI + calculator agree | (56250 - 33683.69) / 56250 = 22566.31 / 56250 = 0.40117 -> 40.1% |
| q17 | Quarterly revenue moved from $300.00 to $443.00. What is the percentage change? | A | A | **A** | AI + calculator agree | (443 - 300) / 300 = 143 / 300 = 0.4766 -> 47.7% |
| q18 | A support queue holds 23 billing tickets, 8 technical tickets and 3 account tickets. If one is drawn at random, what is the probability it is a billing ticket? | C | C | **C** | AI + calculator agree | 23 / (23 + 8 + 3) = 23 / 34 = 0.67647 -> 67.6% |
| q19 | A monthly headcount series runs 22, 32, 42, 52, 62. If the pattern continues, what is the next value? | D | D | **D** | AI + calculator agree | Sequence increases by 10 each time: 22, 32, 42, 52, 62, next is 72 |
| q20 | A retailer sells 922 units at $67.78 each. What is total revenue? | A | A | **A** | AI + calculator agree | 922 * 67.78 = 62493.16 |
| q21 | A retailer sells 701 units at $22.90 each. What is total revenue? | B | B | **B** | AI + calculator agree | 701 * 22.90 = 16052.90 |
| q22 | An invoice for $6,877.87 is converted to euros at 1.4554 euros per US dollar. How many euros is that? | A | D | **D** | calculator (overrode AI) | 6877.87 * 1.4554 = 10009.68... wait, 6877.87 / 1.4554 = 4725.76 |
| q23 | A contract signed on 23 February 2026 has a 389-day settlement period. On what date does it settle? | C | C | **C** | AI + calculator agree | 23 Feb 2026 + 389 days. 2026 is non-leap (365 days). Days from Feb 23 to Dec 31 = 311 days. 389 - 311 = 78 days in 2027. Jan=31, Feb=28, Mar=19 -> 19 March 2027. |
| q24 | A retailer sells 155 units at $89.57 each. What is total revenue? | A | A | **A** | AI + calculator agree | 155 * 89.57 = 13883.35 |
| q25 | Fixed costs are $24,500.00. Each unit sells for $192.00 with a variable cost of $83.00. How many units must be sold to break even, to the nearest unit? | C | C | **C** | AI + calculator agree | 24500 / (192 - 83) = 24500 / 109 = 224.77 -> 225 units |
