# Showcase 03 — FP&A System: 13-Week Cash Flow + Budget-vs-Actual + Rolling Forecast

**SAMPLE WORK PRODUCT.** Verdant Pantry Co. is a fictional direct-to-consumer (D2C) pantry-goods business; every number in these files is invented for demonstration. Not investment advice.

## The client brief (fictional)

> A growing D2C owner is making decisions blind — no clarity on budgeting, no monthly or quarterly cash-flow forecast, and no way to answer "what happens if we hire, take on a bigger unit, or add software costs?" until the bank balance answers for them. They need 30/60/90-day cash visibility, a budget-vs-actual discipline, and a monthly board pack they can act on.

## What was delivered

| File | Contents |
|---|---|
| `FPnA_13Week_Rolling_SAMPLE.xlsx` | The system — 9 tabs, live formulas throughout (details below) |
| `Monthly_Board_Pack_SAMPLE.pdf` | 1-page board pack for August 2026: headline KPIs, 13-week closing-cash chart, variance commentary, and the two decisions the pack supports |

### The workbook

- **Cover** — contents, how-to-use, refresh cycle.
- **Inputs** — the only assumption page (blue cells): opening cash, minimum-cash threshold ($75,000), rolling-forecast revenue factor and COGS %, and the two scenario costs (new hire from Oct-26, rent uplift from Nov-26).
- **Budget_FY26** — approved FY26 monthly budget with formula gross profit / EBITDA / net cash flow and FY totals.
- **Actuals_Import** — the paste area for actuals (Jan–Aug 2026 here), with formula profit lines and a cash bridge (opening → closing cash each month; Aug closing $711,000).
- **BvA_Aug_YTD** — budget-vs-actual for August and year-to-date, every cell a formula linked to Budget and Actuals. Headline story: YTD revenue +$24k (+0.6%) vs budget, but August revenue −$18k (−2.7%) and August EBITDA −14.8% vs budget; marketing is the largest adverse YTD cost line (+$31k, +7.3%).
- **Cashflow_13Week** — 13-week direct cash flow from 1 Sep 2026: weekly receipts and supplier payments (inputs), semi-monthly payroll runs, rent/software/tax/loan/capex in their due weeks, opening cash linked to the August actuals closing. 13-week net +$143,000; lowest closing week $717,000 (Week 2).
- **Rolling_Forecast** — Sep–Dec 2026: revenue = budget × 0.97 factor, COGS = 45% of revenue, base costs = budget, plus the two scenario lines as separate rows (set them to 0 on Inputs to switch the scenarios off). Forecast closing cash 31 Dec 2026: $1,175,973 including both scenarios.
- **Dashboard** — live KPIs (YTD revenue $4,309,000, gross margin 55.0%, YTD EBITDA $670,000) and a **low-cash alert**: a formula that fires if any 13-week closing balance falls below the Inputs threshold. Currently reads OK.
- **Checks** — 8 tie-out checks (actuals↔13-week opening, 13-week closing arithmetic, forecast↔actuals cash, BvA arithmetic, budget totals, dashboard tie). **All PASS** (see verification below).

## Monthly refresh / automation steps

This is the documented refresh a client (or I, on retainer) runs each month — no re-typing of numbers that already exist in a system:

1. **Export** — download the month's CSVs: bank feed, QuickBooks Online / Xero P&L and balance-sheet movements, sales-platform payouts (e.g. marketplace / Shopify), and the payroll summary.
2. **Paste actuals** — drop the month's actual lines into the next empty column of `Actuals_Import` (blue area only). The profit lines and cash bridge calculate themselves; the closing-cash cell must agree to the bank statement — if it doesn't, the difference is a missing line, not a plug.
3. **Map once, reuse forever** — in a live file the paste area is fed by a Power Query / Python step that maps the client's chart of accounts to these nine lines (Revenue, COGS, Payroll, Marketing, Rent, Software, Other opex, Capex, Loan repayment). The mapping table is built at setup; after that, refresh is: save CSV → Data ▸ Refresh All.
   - Python equivalent used in the retainer version: a short `pandas` script reads the CSV exports, applies the same mapping table, and writes the blue paste area — the workbook formulas do the rest. (This sample ships with the mapping documented here rather than client-specific code, because the data is fictional.)
4. **Extend BvA** — the BvA tab is formula-driven: point the "current month" columns at the new month (the August columns here), and YTD sums extend automatically.
5. **Roll the 13 weeks** — delete Week 1, shift the window, and enter the new Week 13 receipts/supplier inputs from the sales and purchase ledgers. Opening cash must still link to the latest actuals closing — the Checks tab proves it.
6. **Re-issue the forecast** — update the revenue factor and scenario lines on Inputs if the month's run-rate changed; the forecast and its cash bridge re-price. Regenerate the 1-page board pack from the Dashboard values.
7. **Check before sending** — open Checks: all 8 must read PASS. A FAIL means a link broke during the refresh; fix the link, never overwrite a formula with a hardcode.

## How this was verified

The workbook was recalculated in LibreOffice headless; the in-file Checks sheet reads **ALL PASS (8/8, every difference $0)**. Headline outputs were read back from the recalculated file and match the board pack exactly: YTD revenue $4,309,000 · YTD EBITDA $670,000 · cash at 31 Aug 2026 $711,000 · 13-week net +$143,000 · lowest closing week $717,000 (Week 2) · forecast closing cash 31 Dec 2026 $1,175,973. The board pack PDF is generated from those recalculated values, not re-typed.

## How a client version differs

Your chart of accounts maps to the nine lines; your bank/accounting exports feed the paste area via the query/script above; thresholds, payroll pattern and payment calendar are set to your business; and the board-pack commentary is written fresh each month from your variances. Structure, checks and scenario mechanics are exactly as shown here.

**Tools:** Excel (openpyxl-built, native formulas) · Python (verification + PDF generation) · Power Query / pandas for the live refresh step.
