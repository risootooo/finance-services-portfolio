# Financial Model Audit — Findings Report (SAMPLE)

**Client (fictional):** NorthPeak Traders Ltd · **As received:** `Broken_Model_BEFORE.xlsx` · **Corrected:** `Fixed_Model_AFTER.xlsx` · **Auditor:** Samrat Banerjee · Sample engagement, Nov 2026

## Executive summary

**11 findings: 4 Critical, 4 Major, 3 Minor.** Enterprise value as received **USD 52,267.7k** vs corrected **USD 24,541.9k** (overstated **113.0%**). Implied value per share as received **USD 0.0260** vs corrected **USD 12.1459**. Balance sheet out of balance by USD 7,442.4k by FY28 as received. All findings fixed in the corrected file; its 6 checks are all green.

## Scope & method

Mechanical/internal-consistency audit only: formula inspection, hardcode scan, reference tracing, sign/units checks, statement ties, WACC rebuild, independent recalculation. Assumption reasonableness not opined on. Standalone impacts measured one-error-at-a-time in a parallel calculation; both workbooks recalculated in LibreOffice and agreed to the decimal.

## Findings

| # | Finding | Location | Severity | Quantified impact | Fix applied |
|---|---|---|---|---|---|
| F-01 | WACC built from wrong cells — equity/debt weights transposed and pre-tax cost of debt used (tax shield dropped) | `Inputs!C22` | **Critical** | WACC 6.70% vs correct 8.50%. Standalone effect: enterprise value overstated +43.7%. | Rebuilt as E-weight × cost of equity + D-weight × cost of debt × (1 − tax). Independent WACC recompute check added (Checks sheet). |
| F-02 | Copy-across error — FY28 operating expenses linked to FY26 revenue instead of FY28 revenue | `IS!F7` | **Critical** | FY28 opex understated by 815.9 (2,530.0 vs 3,345.9). Standalone effect: EV overstated +35.3%. | Relinked to FY28 revenue; column-consistency check performed across all forecast years. |
| F-03 | Retained earnings frozen at the FY25 value — equity never rolls forward with profit | `BS!D12:F12` | **Critical** | Balance sheet out of balance by 1,260.0 (FY26), 2,752.9 (FY27), 4,513.6 (FY28) on a standalone basis. Statements unreliable as presented. | Retained earnings now roll (prior RE + net income). Balance check row and RE-walk check added. |
| F-04 | Units error — equity value held in USD $000s divided by the share count with no ×1,000 conversion | `Valuation!C20` | **Critical** | Headline implied price USD 0.0260 per share vs correct USD 12.1459 — understated 99.8%. | Conversion restored; units now stated on every sheet header and on the Inputs share count. |
| F-05 | Depreciation & amortisation added back twice in free cash flow | `Valuation!D6:F6` | **Major** | FCF overstated by 300.0 in every forecast year. Standalone effect: EV overstated +19.5%. | Single add-back; FCF build now foots line-by-line to the IS/CF. |
| F-06 | Sign error — capital expenditure entered as a cash inflow in the cash-flow statement | `CF!D9:F9` | **Major** | Cash overstated by 700.0 per year; standalone balance-sheet break reaches 2,100.0 by FY28. | Capex signed as an outflow; CF closing-cash ↔ BS cash tie check added. |
| F-07 | Tax charged on EBITDA instead of profit before tax (D&A and interest never deducted) | `IS!D13:F13` | **Major** | Tax overstated by 97.5 per year; net income and closing cash understated (292.5 cumulative by FY28, standalone). | Tax now charged on profit before tax, floored at zero. |
| F-08 | No checks anywhere in the file — no balance check, no cash tie, no independent recompute | `Whole workbook` | **Major** | Control failure: ten mechanical errors flowed into the valuation output with no tripwire. | Balance check row on BS, tie check on CF, and a 6-point Checks sheet added — all green in the corrected file. |
| F-09 | Hardcoded number typed inside a formula — FY27 revenue growth entered as 12% instead of the 15% assumption | `IS!E4` | **Minor** | FY27 revenue understated by 345.0 (12,880.0 vs 13,225.0). Standalone effect: EV −2.8%. | Linked to the Inputs growth assumption; formula audit confirmed no remaining hardcodes in forecast formulas. |
| F-10 | Wrong reference — FY26 COGS linked to prior-year (FY25) revenue | `IS!D5` | **Minor** | FY26 COGS understated by 900.0 (6,000.0 vs 6,900.0); gross profit overstated. Standalone effect: EV +2.5%. | Relinked to FY26 revenue. |
| F-11 | Working-capital movement in FCF ignores the liabilities side (only receivables/assets movement deducted) | `Valuation!D8:F8` | **Minor** | ΔNWC overstated every year. Standalone effect: EV −2.5%. | Full ΔNWC (current assets − current liabilities) now used. |

## Corrected headline outputs

| | As received | Corrected |
|---|---|---|
| WACC | 6.70% | 8.50% |
| Enterprise value (USD $000s) | 52,267.7 | 24,541.9 |
| Equity value (USD $000s) | 52,017.7 | 24,291.9 |
| Implied value per share (USD) | 0.0260 | 12.1459 |
| Balance-sheet imbalance FY28 (USD $000s) | 7,442.4 | 0.0 |
| Checks failing | n/a — no checks existed | 0 of 6 |


*SAMPLE work product — fictional company, invented data. Mechanics audit only: not investment advice and not an audit opinion under any auditing standard.*
