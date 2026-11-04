# Showcase 01 — Investor-Ready SaaS Financial Model

**SAMPLE WORK PRODUCT.** CloudLedger Inc is a fictional company; every number in these files is invented for demonstration. Not investment advice.

## The client brief (fictional)

> A seed-stage SaaS founder (subscription bookkeeping-automation for SMB accounting firms) is preparing for investor discussions. Their existing spreadsheet doesn't link — change an assumption and the statements disagree — and there is no defensible valuation. They need: a structured, fully linked model with DCF + comparables, clear financial slides for the deck, and something an investor can stress-test in diligence without it falling apart.

## What was delivered

| File | Contents |
|---|---|
| `CloudLedger_SaaS_Model_SAMPLE.xlsx` | The model — 8 tabs, live formulas throughout (details below) |
| `deliverables/CloudLedger_Model_Summary.pdf` | 2-page summary: snapshot, Base forecast, scenario outcomes, valuation bridge, sensitivity extract, football field |
| `deliverables/CloudLedger_Deck_Extract.pdf` | 5-slide deck extract: title, the problem, model snapshot, valuation football field, the ask |

### The workbook

- **Cover** — contents, how-to-use, live checks status.
- **Assumptions** — every input on one page (blue cells only). Scenario table for Bear/Base/Bull (growth path, gross margin, opex ratios), operating ratios (tax, D&A, capex, working-capital drivers), SaaS context (4,850 logos, $119 ARPU, 2.1% monthly churn, 108% NRR), valuation inputs (Rf 4.30%, β 1.25, ERP 5.50%, terminal growth 3.0%, 10.0m shares).
- **IS / BS / CF** — linked 3 statements, FY23–FY25 actuals + FY26–FY30 forecast. Balance sheet balances in all 8 years; closing cash ties CF ↔ BS.
- **DCF** — CAPM WACC build (11.18%), free cash flow from the statements, Gordon-growth terminal value, and a live 9 × 7 sensitivity grid (WACC × terminal growth) computed on the active scenario.
- **Comps** — six fictional peers (labelled SAMPLE), median EV/Revenue 4.75× and EV/EBITDA 37.6× applied to FY26E.
- **Dashboard** — headline outputs, revenue/EBITDA chart (native Excel chart), SaaS KPIs, and the checks panel.

### Headline outputs (Base scenario, valuation date 31 Dec 2025)

| Metric | Value |
|---|---|
| FY30E revenue | $30,728k (FY25: $6,900k; CAGR 34.8%) |
| Enterprise value (DCF) | $19,094k |
| Implied value per share — DCF | **$2.43** |
| Scenario range (Bear – Bull) | $0.91 – $5.23 |
| Sensitivity range (WACC ±2%, g 1.5–4.5%) | $1.86 – $3.85 |
| Implied value per share — comps (EV/Revenue) | $5.27 |
| Checks | Balance ✓ · Cash tie ✓ · Sensitivity tie ✓ — all PASS |

Try it: set the scenario switch (Assumptions, cell C6) to 1 or 3 — statements, DCF, comps and dashboard all re-price, and the checks stay green.

## How this was verified

The workbook was recalculated in LibreOffice headless and every key output was compared against an independent parallel Python model: all statement values, the DCF, and **all 63 sensitivity cells matched to the decimal**, in all three scenarios (Bear $0.91 / Base $2.43 / Bull $5.23 per share reproduced exactly both ways). The dashboard checks panel is itself part of the file, so the same verification runs every time a client opens it.

## How a client version differs

Your actuals replace the fictional history; your chart of accounts maps to the statement lines; each assumption is documented with its source and your sign-off; the peer set is real, named and sourced; and the deck extract is built on your real cap table and raise terms. Structure, checks and scenario mechanics are exactly as shown here.

**Tools:** Excel (openpyxl-built, native formulas & chart) · Python (verification model, PDF generation).
