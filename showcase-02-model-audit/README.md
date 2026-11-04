# Showcase 02 — Financial Model Audit, Fix & Rescue

**SAMPLE WORK PRODUCT.** NorthPeak Traders Ltd is a fictional company; the "client file" below was built with deliberate errors of the kinds found in real inherited models. Not investment advice; a mechanics audit is not an audit opinion under any auditing standard.

## The offer (fixed fee, 48–72 hours)

Your investor, lender or buyer is about to diligence your model. Before they find what's wrong with it, I do:

1. **Audit** — every forecast formula inspected: hardcode scan, reference tracing, sign and units checks, statement ties, discount-rate rebuild.
2. **Report** — each error located by sheet and cell, rated Critical / Major / Minor, with its financial impact quantified (standalone and combined).
3. **Fix** — corrected workbook returned with a checks dashboard (balance check, cash ties, independent recomputes) that fails loudly if the error classes return.

Packages from **$175** (report only) to **$500** (audit + fix + hardening) — see [../SERVICES.md](../SERVICES.md). Almost nobody sells this as a standalone product; it's the fastest way to make a model diligence-safe.

## Files in this showcase

| File | What it is |
|---|---|
| `Broken_Model_BEFORE.xlsx` | The model "as received" — 10 planted mechanical errors + 1 missing control (no checks) |
| `AUDIT-REPORT.pdf` / `AUDIT-REPORT.md` | The findings report: 11 findings, locations, severities, quantified impacts, fixes |
| `Fixed_Model_AFTER.xlsx` | The corrected model — balance check row and a 6-point Checks sheet added, all green |

## What the audit found (summary)

**As received:** enterprise value $52,267.7k, implied price **$0.0260/share**, balance sheet out of balance by $7,442.4k.
**Corrected:** enterprise value $24,541.9k (**−53%**; the as-received figure was overstated by 113.0%), implied price **$12.1459/share**, balance sheet balances, 0 of 6 checks failing.

| Severity | Count | Headline errors |
|---|---|---|
| Critical | 4 | WACC built from transposed weights with the tax shield dropped (6.70% vs 8.50% → EV +43.7% alone) · FY28 opex copy-across to FY26 revenue (EV +35.3%) · retained earnings frozen — balance sheet never balances · units error cutting the headline share price by 99.8% |
| Major | 4 | D&A added back twice in FCF (EV +19.5%) · capex signed as a cash inflow · tax charged on EBITDA instead of PBT · no checks anywhere in the file |
| Minor | 3 | Hardcoded 12% growth typed over the 15% assumption · COGS linked to prior-year revenue · FCF working capital ignoring the liabilities side |

Each error is real in `Broken_Model_BEFORE.xlsx` — open it, trace the precedents, and check the numbers yourself.

## How this was verified

Both workbooks were recalculated in LibreOffice headless and compared against an independent parallel Python calculation in which each error can be toggled individually (that is how the standalone impacts in the report were measured). The BEFORE file reproduces the broken outputs exactly (EV $52,267.7k, WACC 6.70%, $0.0260/share, balance-sheet breaks of 2,537.5 / 4,586.3 / 7,442.4 across FY26–28). The AFTER file reproduces the corrected outputs exactly and its Checks sheet reads **✓ ALL CHECKS PASS**.
