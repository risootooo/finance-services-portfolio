# Showcase 05 — Equity Research Pack + AI-Research QA

**SAMPLE WORK PRODUCT — illustrative sample on public data only. Not a recommendation to buy, sell or hold any security; not personalised investment advice.** No non-public information was used; no company contact was made.

## The client brief (fictional)

> A research buyer needs buy-side-quality company analysis — an initiation-style report where every number foots to a model — and, separately, their AI drafting tools produce fluent research with invented numbers and valuations that don't tie to anything. They want the report, the linked model behind it, and a QA pass that catches what the AI invents.

## What was delivered

| File | Contents |
|---|---|
| `Equity_Research_Report_SAMPLE.pdf` | 9-page initiation-style sample report on Apple Inc. (NASDAQ: AAPL): summary, business, industry, history, forecast, DCF, comps + football field, catalysts & risks, methodology/sources/disclosures |
| `Apple_Model_SAMPLE.xlsx` | The linked model — 7 tabs, live formulas: history + 5-year forecast, DCF with sensitivity grid, comps, checks ALL PASS |
| `AI_QA_Sample.pdf` | 2-page AI-research QA sample: a fictional AI-style draft seeded with 8 material errors, each annotated with type, correction and the source to check against. Verdict on the draft: DO NOT PUBLISH |

### The model

- **IS** — FY23–FY25A income statement as reported in Apple's Form 10-K filings (rounded to $bn): revenue $383.285bn / $391.035bn / $416.161bn; FY25 net income $112.010bn, EPS $7.48 on the model's rounded share count. FY26E–FY30E is a formula forecast.
- **Assumptions** — the only forecast dials: revenue growth 6.0% fading to 4.5%, gross margin 47.0% → 48.0%, R&D/SG&A ratios, normalised 16% tax, plus the valuation inputs (Rf 4.30%, β 1.09, ERP 5.00%, terminal growth 3.0%). None of this is company guidance.
- **BS_Aggregated / CF** — balance sheet and cash flow in **aggregated, rounded** form (labelled as such in the file; audited detail is the Form 10-K's). Totals are formulas, the sheet balances every year, forecast equity rolls forward (prior + net income − $105bn capital return), and closing cash ties CF ↔ BS in every year.
- **DCF** — CAPM WACC build (**9.51%**), FCF from the CF tab (FY26E $119.4bn → FY30E $148.4bn), Gordon terminal value; **implied value $128.93/share**. The 5×5 sensitivity grid (WACC ±1% × terminal growth 2–4%) recomputes the full DCF in every cell: range **$101–$182**, centre cell = base case (checked).
- **Comps** — Microsoft / Alphabet / NVIDIA / Meta / Samsung at rounded public-market multiples (labelled approximations, late Oct 2026 — verify on a live terminal before real use). Medians (EV/Rev 9.6×, EV/EBITDA 23.5×, P/E 28×) applied to FY26E imply **$223–$278/share**.
- **The honest tension the report is built around:** the conservative fade-model DCF ($129) sits far below trading multiples ($223–$278). The report names that gap as the investment debate — durability and optionality the market pays for that a fade-to-3% DCF does not credit — and takes no position. A research sample that hides its own valuation disagreement would be marketing, not research.

### The AI-QA sample

The fictional draft claims an "Apple Car" contributing $21bn (fabrication), FY25 revenue of $483bn at +18% (actual $416.161bn, +6.4%), a 31% net margin (actual 26.9%), services at 55% of revenue (actual ≈26.2%), invented 25% management guidance, a $512/share DCF at a 7.0% WACC that contradicts the model's 9.51% / $128.93, and "guaranteed upside… at any price" (prohibited language). All 8 are flagged with corrections and checkable sources — the same pass offered in the Pack + AI-QA tier of SERVICES.md. Note the standing rule for this product, taken from real buyer briefs: the QA deliverable is written by a human; AI drafts are the *input*, never the author.

## How this was verified

- The workbook was recalculated in LibreOffice headless; its Checks sheet reads **ALL PASS (10/10, every difference 0)** — including FY25 net income equalling the reported $112.010bn through the input chain, BS balancing in FY25 and FY28E, cash tying CF ↔ BS, and the sensitivity centre cell equalling the base DCF.
- **Report ↔ model tie-out:** the report PDF is generated from the recalculated workbook values (not re-typed), and a text-extraction check on the finished PDF confirmed the key figures appear exactly as in the model: revenue $416.2bn, growth +6.4%, net income $112.0bn, net margin 26.9%, EPS $7.48, WACC 9.51%, DCF $128.93, comps $223–$278, sensitivity $101–$182.
- **Page counts:** report 9 pages (the 8–10 page initiation format in SERVICES.md), AI-QA sample 2 pages.

## How a client version differs

The company, peer set and as-of dates are the client's; multiples are pulled from a terminal at a stated timestamp rather than rounded; segment analysis goes to the depth the filings support; and a distributed live product would carry the registrations and compliance review its market requires (see the report's disclosures — the author is a CFA Level 1 candidate, not a charterholder or a registered research analyst).

**Tools:** Excel (openpyxl-built, native formulas) · Python (verification + PDF generation) · Public filings (SEC EDGAR).
