# Round 69
Released 2026-10-18T17:01:37Z - answered 2026-10-18 17:04 UTC - model: gemini-3.5-flash-lite

Sources: AI + calculator agree: 24, calculator (overrode AI): 1

| # | Question | AI | Calculator | Final | Source | AI work |
|---|---|---|---|---|---|---|
| q1 | An item listed at $380.28 is discounted by 5%. What is the sale price? | B | B | **B** | AI + calculator agree | 380.28 * (1 - 0.05) = 361.266 = $361.27 |
| q2 | A $990.00 marketing budget is split between two channels in the ratio 5:6. What does the first channel receive? | B | B | **B** | AI + calculator agree | 990 * (5 / (5 + 6)) = 990 * 5 / 11 = 450 |
| q3 | An investment of $43,000.00 grows at 13% compounded annually. What is its value after 5 years? | C | C | **C** | AI + calculator agree | 43000 * (1.13)^5 = 79224.71 |
| q4 | Fixed costs are $9,000.00. Each unit sells for $41.00 with a variable cost of $13.00. How many units must be sold to break even, to the nearest unit? | C | C | **C** | AI + calculator agree | 9000 / (41 - 13) = 9000 / 28 = 321.43 -> 321 |
| q5 | An invoice for $8,938.23 is converted to euros at 1.6961 euros per US dollar. How many euros is that? | A | A | **A** | AI + calculator agree | 8938.23 * 1.6961 = 15160.128793 -> 15,160.13 |
| q6 | A contract signed on 28 December 2026 has a 334-day settlement period. On what date does it settle? | C | B | **B** | calculator (overrode AI) | 28 Dec 2026 + 334 days = 27 Nov 2027 (2027 is non-leap, Dec has 3 days left + 331 days in 2027 = 30+31+28+31+30+31+30+31+31+30+27 = Nov 27) |
| q7 | Quarterly revenue moved from $4,550.00 to $2,355.00. What is the percentage change? | B | B | **B** | AI + calculator agree | (2355 - 4550) / 4550 = -2195 / 4550 = -0.4824 -> -48.2% |
| q8 | A product line generates $43,250.00 in revenue against $22,381.62 in cost of goods sold. What is the gross margin? | C | C | **C** | AI + calculator agree | (43250 - 22381.62) / 43250 = 20868.38 / 43250 = 0.4825 -> 48.3% |
| q9 | A retailer sells 726 units at $13.36 each. What is total revenue? | B | B | **B** | AI + calculator agree | 726 * 13.36 = 9699.36 |
| q10 | A support queue holds 19 billing tickets, 24 technical tickets and 5 account tickets. If one is drawn at random, what is the probability it is a billing ticket? | D | D | **D** | AI + calculator agree | 19 / (19 + 24 + 5) = 19 / 48 = 0.3958 -> 39.6% |
| q11 | An invoice for $3,608.94 is converted to euros at 0.6688 euros per US dollar. How many euros is that? | D | D | **D** | AI + calculator agree | 3608.94 * 0.6688 = 2413.6558 => 2,413.66 |
| q12 | An invoice for $7,059.46 is converted to euros at 0.7007 euros per US dollar. How many euros is that? | D | D | **D** | AI + calculator agree | 7059.46 * 0.7007 = 4945.5085... wait: 7059.46 * 0.7007 = 4946.5647 -> 4,946.56 |
| q13 | Region A had 78 orders averaging $65.00; region B had 186 orders averaging $67.00. What is the overall average order value? | D | D | **D** | AI + calculator agree | (78 * 65 + 186 * 67) / (78 + 186) = (5070 + 12462) / 264 = 17532 / 264 = 66.409 -> 66.41 |
| q14 | A retailer sells 262 units at $84.15 each. What is total revenue? | B | B | **B** | AI + calculator agree | 262 * 84.15 = 22047.30 |
| q15 | A retailer sells 575 units at $10.80 each. What is total revenue? | C | C | **C** | AI + calculator agree | 575 * 10.80 = 6210.00 |
| q16 | A product line generates $16,500.00 in revenue against $11,996.54 in cost of goods sold. What is the gross margin? | C | C | **C** | AI + calculator agree | (16500 - 11996.54) / 16500 = 4503.46 / 16500 = 0.2729 -> 27.3% |
| q17 | An investment of $22,000.00 grows at 12% compounded annually. What is its value after 7 years? | A | A | **A** | AI + calculator agree | 22000 * (1.12)^7 = 48634.99 |
| q18 | A product line generates $73,500.00 in revenue against $51,870.89 in cost of goods sold. What is the gross margin? | B | B | **B** | AI + calculator agree | (73500 - 51870.89) / 73500 = 21629.11 / 73500 = 0.2942 -> 29.4% |
| q19 | An invoice for $4,364.89 is converted to euros at 1.0658 euros per US dollar. How many euros is that? | C | C | **C** | AI + calculator agree | 4364.89 * 1.0658 = 4652.10 |
| q20 | A support queue holds 6 billing tickets, 15 technical tickets and 7 account tickets. If one is drawn at random, what is the probability it is a billing ticket? | C | C | **C** | AI + calculator agree | 6 / (6 + 15 + 7) = 6 / 28 = 0.21428 -> 21.4% |
| q21 | Fixed costs are $38,500.00. Each unit sells for $177.00 with a variable cost of $59.00. How many units must be sold to break even, to the nearest unit? | A | A | **A** | AI + calculator agree | 38500 / (177 - 59) = 38500 / 118 = 326.27 -> 326 |
| q22 | Region A had 59 orders averaging $91.00; region B had 106 orders averaging $22.00. What is the overall average order value? | D | D | **D** | AI + calculator agree | (59 * 91 + 106 * 22) / (59 + 106) = (5369 + 2332) / 165 = 7701 / 165 = 46.67 |
| q23 | A product line generates $7,000.00 in revenue against $4,271.25 in cost of goods sold. What is the gross margin? | C | C | **C** | AI + calculator agree | (7000 - 4271.25) / 7000 = 2728.75 / 7000 = 0.3898 -> 39.0% |
| q24 | Quarterly revenue moved from $3,250.00 to $2,293.00. What is the percentage change? | B | B | **B** | AI + calculator agree | (2293 - 3250) / 3250 = -957 / 3250 = -0.2944 -> -29.4% |
| q25 | An investment of $6,000.00 grows at 13% compounded annually. What is its value after 3 years? | B | B | **B** | AI + calculator agree | 6000 * (1.13)^3 = 8657.38 |
