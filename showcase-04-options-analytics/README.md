# Showcase 04 — Options & Trading Analytics: Python Backtest + Payoff/Greeks Explorer

**SAMPLE WORK PRODUCT — HISTORICAL SIMULATION ON SYNTHETIC DATA. NOT INVESTMENT ADVICE, NOT A TRADING SIGNAL, NO GUARANTEE OF ANY RESULT.** The backtest below *lost money* out-of-sample and says so in its headline. Past or simulated performance does not guarantee future results. Options trading involves substantial risk of loss.

## The client brief (fictional)

> A trader has a weekly options rule set in their head and a platform backtest that shows "000 P&L and no trades execute". They want their rules coded properly, tested honestly — with real costs, slippage and no peeking at the future — plus a tool that shows what a position can actually make or lose and what its Greeks are.

## What was delivered

| File | Contents |
|---|---|
| `backtest.py` | Documented, reproducible Python backtest (generates its own synthetic data in-code; no real market data used) |
| `Backtest_Report_SAMPLE.pdf` | 3-page tear-sheet: headline result, mechanics, friction model, walk-forward design, results, sensitivity, limitations, compliance |
| `Payoff_Greeks_Explorer_SAMPLE.xlsx` | Single-position payoff & Greeks tool — 4 tabs, live Black–Scholes formulas, payoff grid + chart, checks ALL PASS |
| `results/` | `trades.csv` (every simulated week), `equity_curve.csv`, `metrics.json`, `sensitivity.json`, `walk_forward_selections.csv` |

### The backtest

- **Strategy under test (client-supplied style rules, fixed a priori):** weekly defined-risk iron condor — short call/put at ±d% from spot, wings 1.5% beyond, held to expiry, 1 lot of 25.
- **Data: synthetic only** — a seeded GBM series (start 24,000, drift 7% p.a., two-state volatility regime 11%/24%) generated inside the script. It verifies code honesty and mechanics; it does not describe any real market or period, and cannot validate a strategy for live use.
- **Frictions on every trade:** flat ₹62/leg/lot charges on entry and exit (₹496/week) + 1.5 pts/leg adverse slippage, entry and exit.
- **Walk-forward:** the only free parameter (strike distance d ∈ {1.5%, 2%, 2.5%, 3%}) is chosen by in-sample Sharpe on 104 weeks and applied untouched to the next 52; two folds → 104 out-of-sample weeks.
- **Headline result (out-of-sample): total P&L −₹55,094 · Sharpe −0.94 · max drawdown −₹79,653 · win rate 45.2% · frictions charged ₹51,584. Verdict in the report: on this evidence, do not trade this parameterisation.** The report shows why: in 36 of 104 weeks the credit collected was less than the week's fixed frictions, so those weeks lost even when every option expired worthless; 65% of weeks sat in the high-volatility regime where ±3% strikes are under one weekly standard deviation away; and every strike distance in the grid lost out-of-sample (sensitivity table in the report).

Reproduce it: `python3 backtest.py` (seed 42) regenerates `results/` and prints the same headline numbers.

### The payoff/Greeks explorer

- **Inputs_Legs** — spot, days to expiry, rate, IV, lot size (blue inputs) and a 4-leg iron condor (strikes ±3%, wings ±4.5% at the sample inputs). Premiums default to Black–Scholes formula prices; overwrite with traded premiums in live use. Net credit at sample inputs: **₹392**.
- **Greeks** — per-leg and portfolio Delta / Gamma / Vega / Theta / Rho, all live formulas (legacy `NORMSDIST`/`NORMDIST` functions so the file calculates identically in Excel and LibreOffice). Portfolio at sample inputs: delta −0.40 (₹ per point, position-scaled), vega −136.39 per 1% IV.
- **Payoff_at_Expiry** — P&L for terminal levels 20,000–29,600 with a native Excel chart; max profit ₹392 (= the credit), max loss ₹8,608 (= 360-pt wing width × 25 − credit), lower grid breakeven 23,600.
- **Checks** — 5 checks: put–call parity at the short-call strike, portfolio delta = Σ leg deltas, payoff-grid total vs direct recomputation, max grid profit = net credit, grid max loss vs theoretical max loss. **ALL PASS** (see verification).

## How this was verified

- `backtest.py` was executed end-to-end (exit 0); `metrics.json`, the trade file and the report's numbers are the run's own outputs — the report PDF is generated from `metrics.json`/`sensitivity.json`, not typed by hand. The sensitivity table was computed on the same out-of-sample weeks, one change at a time.
- The explorer workbook was recalculated in LibreOffice headless: its Checks sheet reads **ALL PASS (5/5, every difference 0)**, and its four Black–Scholes leg prices match the independent Python implementation in `backtest.py` to 4 decimal places (10.8607 / 1.2916 / 6.6907 / 0.5670).
- One modelling quirk is disclosed, not hidden: exit slippage is charged on short legs even when they expire worthless (a conservative convention — you would not normally pay to close a worthless option), and §5 of the report quantifies how much of the loss frictions explain (removing slippage entirely still leaves a −₹31,169 loss).

## Compliance

This is a software and research service: *your rules, coded*. I do not provide trading strategies, signals, personalised investment advice or profit expectations, I do not manage accounts or place trades, and I am not a SEBI-registered investment adviser or research analyst. Showcase data is synthetic and labelled SAMPLE throughout.

**Tools:** Python (numpy / pandas / scipy) · Excel (openpyxl-built, native formulas & chart).
