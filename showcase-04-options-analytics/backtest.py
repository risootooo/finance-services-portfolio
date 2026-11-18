#!/usr/bin/env python3
"""
backtest.py — Defined-risk weekly iron condor backtest on SYNTHETIC index data
==============================================================================

SAMPLE / EDUCATIONAL CODE. This script:

  * generates a synthetic "NIFTY-style" weekly index series in-code
    (geometric Brownian motion with a volatility regime switch) — it does
    NOT download, read or use any real market data;
  * backtests ONE client-supplied style of rule set — a weekly, defined-risk
    iron condor — exactly as specified in PARAMETERS below;
  * charges realistic frictions on every leg (brokerage + exchange-style
    charges modelled as a flat per-lot cost, plus slippage in points);
  * runs a WALK-FORWARD evaluation: strike-distance parameters are chosen
    on an in-sample window only, then applied untouched to the following
    out-of-sample window, repeatedly. Headline metrics are out-of-sample.

This is software and historical-simulation research. It is NOT investment
advice, NOT a trading signal, NOT a strategy recommendation, and it makes
NO claim or guarantee about future or live results. Past (simulated)
performance does not guarantee future results. Options trading involves
substantial risk of loss. See the report PDF and README for the full
compliance note (SEBI / platform rules: code & research only).

Usage:
    python3 backtest.py                # prints a summary, writes results/
    python3 backtest.py --seed 7       # different synthetic series

Outputs (in ./results/):
    trades.csv          every simulated weekly trade (in- and out-of-sample)
    equity_curve.csv    weekly out-of-sample cumulative P&L (INR)
    metrics.json        headline metrics used by the report PDF

Author: Samrat Banerjee — Finance Services (sample work product)
"""
from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.stats import norm

# ----------------------------------------------------------------------------
# PARAMETERS — the rule set under test (fixed a priori except where the
# walk-forward search below explicitly selects the short-strike distance
# on in-sample data only).
# ----------------------------------------------------------------------------
PARAMETERS = dict(
    start_spot=24_000.0,        # synthetic index level at t=0
    weeks=312,                  # 6 synthetic years of weekly expiries
    annual_drift=0.07,          # GBM drift of the synthetic series
    vol_low=0.11, vol_high=0.24,  # annualised vol regimes (switching)
    regime_p_stay=0.96,         # weekly prob. of staying in the vol regime
    risk_free=0.065,            # INR risk-free rate for Black-Scholes
    iv_markup=1.08,             # options are "sold" at IV = realised vol x this
    lot_size=25,                # index lot size (points -> INR per lot)
    lots=1,                     # position size: 1 lot per week (fixed)
    wing_width_pct=0.015,       # long wings sit this far beyond the shorts
    profit_exit=None,           # no early exit: hold every trade to expiry
    # frictions, charged per leg per lot:
    cost_per_leg_lot_inr=62.0,  # brokerage + exchange + taxes (flat model)
    slippage_points_per_leg=1.5,  # adverse slippage on entry AND exit, in points
    # walk-forward design:
    wf_insample_weeks=104,      # 2 years in-sample
    wf_outsample_weeks=52,      # 1 year out-of-sample, then roll
    grid_short_dist_pct=(0.015, 0.020, 0.025, 0.030),  # candidates for shorts
)

# ----------------------------------------------------------------------------
# Synthetic data
# ----------------------------------------------------------------------------

def generate_synthetic_series(p: dict, seed: int) -> pd.DataFrame:
    """Weekly spot series + the realised vol of each week (known to the
    'market maker' pricing the options, marked up by iv_markup).

    The series is generated, seeded and reproducible. It is deliberately
    labelled synthetic everywhere downstream.
    """
    rng = np.random.default_rng(seed)
    n = p["weeks"]
    high = np.zeros(n, dtype=bool)
    state = False
    for t in range(n):
        if rng.random() > p["regime_p_stay"]:
            state = not state
        high[t] = state
    annual_vol = np.where(high, p["vol_high"], p["vol_low"])
    weekly_vol = annual_vol / math.sqrt(52)
    weekly_drift = p["annual_drift"] / 52
    shocks = rng.normal(0.0, 1.0, n)
    log_ret = (weekly_drift - 0.5 * weekly_vol**2) + weekly_vol * shocks
    spot = p["start_spot"] * np.exp(np.cumsum(log_ret))
    spot = np.concatenate([[p["start_spot"]], spot[:-1]])  # spot at week open
    expiry_spot = p["start_spot"] * np.exp(np.cumsum(log_ret))  # at week close
    return pd.DataFrame({
        "week": np.arange(n),
        "spot_open": spot,
        "spot_expiry": expiry_spot,
        "annual_vol": annual_vol,
    })

# ----------------------------------------------------------------------------
# Black-Scholes pricing (European, no dividends — teaching-grade model)
# ----------------------------------------------------------------------------

def bs_price(spot: float, strike: float, t_years: float, r: float,
             sigma: float, kind: str) -> float:
    if t_years <= 0 or sigma <= 0:
        return max(spot - strike, 0.0) if kind == "call" else max(strike - spot, 0.0)
    d1 = (math.log(spot / strike) + (r + 0.5 * sigma**2) * t_years) / (sigma * math.sqrt(t_years))
    d2 = d1 - sigma * math.sqrt(t_years)
    if kind == "call":
        return spot * norm.cdf(d1) - strike * math.exp(-r * t_years) * norm.cdf(d2)
    return strike * math.exp(-r * t_years) * norm.cdf(-d2) - spot * norm.cdf(-d1)

# ----------------------------------------------------------------------------
# One weekly iron condor
# ----------------------------------------------------------------------------

@dataclass
class Trade:
    week: int
    short_dist_pct: float
    credit_inr: float
    payoff_inr: float
    costs_inr: float
    pnl_inr: float
    max_loss_inr: float
    spot_open: float
    spot_expiry: float

def run_condor(df_row, short_dist_pct: float, p: dict) -> Trade:
    """Sell a 1-week iron condor at the open; settle at expiry intrinsic.

    Legs: short call at S*(1+d), long call at S*(1+d+w),
          short put  at S*(1-d), long put  at S*(1-d-w).
    Premiums are Black-Scholes at IV = realised vol x iv_markup (the edge
    being tested is purely 'IV above realised vol on a synthetic series' —
    on real markets IV, realised vol and the settlement are all uncertain,
    which is one reason a simulation like this proves nothing about live
    trading).
    """
    S = float(df_row.spot_open); S_T = float(df_row.spot_expiry)
    sigma = float(df_row.annual_vol) * p["iv_markup"]
    T = 7 / 365.0
    d = short_dist_pct; w = p["wing_width_pct"]
    legs = [  # (kind, strike, sign)  sign +1 = long, -1 = short
        ("call", S * (1 + d), -1), ("call", S * (1 + d + w), +1),
        ("put",  S * (1 - d), -1), ("put",  S * (1 - d - w), +1),
    ]
    lot = p["lot_size"] * p["lots"]
    credit_pts = 0.0; payoff_pts = 0.0
    for kind, K, sign in legs:
        prem = bs_price(S, K, T, p["risk_free"], sigma, kind)
        intrinsic = max(S_T - K, 0.0) if kind == "call" else max(K - S_T, 0.0)
        # short legs: receive premium (less slippage), pay intrinsic (plus slippage)
        # long legs:  pay premium (plus slippage), receive intrinsic (less slippage)
        slip = p["slippage_points_per_leg"]
        if sign < 0:
            credit_pts += (prem - slip)
            payoff_pts -= (intrinsic + slip)
        else:
            credit_pts -= (prem + slip)
            payoff_pts += max(intrinsic - slip, 0.0) if intrinsic > 0 else 0.0
    costs = 4 * p["cost_per_leg_lot_inr"] * p["lots"] * 2  # entry + exit, 4 legs
    credit_inr = credit_pts * lot
    payoff_inr = payoff_pts * lot
    pnl = credit_inr + payoff_inr - costs
    width_inr = w * S * lot
    max_loss = width_inr - credit_inr + costs  # defined-risk cap (approx, at entry)
    return Trade(int(df_row.week), short_dist_pct, credit_inr, payoff_inr,
                 costs, pnl, max_loss, S, S_T)

# ----------------------------------------------------------------------------
# Walk-forward evaluation
# ----------------------------------------------------------------------------

def sharpe(weekly_pnl: np.ndarray) -> float:
    if len(weekly_pnl) < 8 or weekly_pnl.std(ddof=1) == 0:
        return 0.0
    return float(weekly_pnl.mean() / weekly_pnl.std(ddof=1) * math.sqrt(52))

def run_backtest(p: dict, seed: int) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    df = generate_synthetic_series(p, seed)
    trades: list[Trade] = []
    selections = []
    start = 0
    n = len(df)
    while start + p["wf_insample_weeks"] < n:
        is_end = start + p["wf_insample_weeks"]
        oos_end = min(is_end + p["wf_outsample_weeks"], n)
        # --- in-sample: pick the short distance with the best Sharpe,
        #     requiring a positive total P&L (else fall back to the widest).
        best_d, best_key = p["grid_short_dist_pct"][-1], None
        for d in p["grid_short_dist_pct"]:
            pnl = np.array([run_condor(df.iloc[t], d, p).pnl_inr
                            for t in range(start, is_end)])
            key = (sharpe(pnl), pnl.sum())
            if pnl.sum() > 0 and (best_key is None or key > best_key):
                best_d, best_key = d, key
        selections.append(dict(insample_start=start, insample_end=is_end - 1,
                               oos_start=is_end, oos_end=oos_end - 1,
                               chosen_short_dist_pct=best_d))
        # --- out-of-sample: apply untouched.
        for t in range(is_end, oos_end):
            tr = run_condor(df.iloc[t], best_d, p)
            tr.week = int(df.iloc[t].week)
            trades.append(tr)
        start = oos_end
    tdf = pd.DataFrame([vars(t) for t in trades])
    tdf["cum_pnl_inr"] = tdf["pnl_inr"].cumsum()
    metrics = summarise(tdf, selections, p)
    return tdf, pd.DataFrame(selections), metrics

def summarise(tdf: pd.DataFrame, selections, p: dict) -> dict:
    pnl = tdf["pnl_inr"].to_numpy()
    eq = tdf["cum_pnl_inr"].to_numpy()
    peak = np.maximum.accumulate(np.concatenate([[0.0], eq]))[1:]
    dd = eq - peak
    years = len(tdf) / 52.0
    wins = pnl[pnl > 0]; losses = pnl[pnl <= 0]
    return dict(
        data="SYNTHETIC — generated in-code (GBM + vol regimes), seed-reproducible",
        trades=int(len(tdf)),
        period_weeks=int(len(tdf)),
        total_pnl_inr=float(pnl.sum()),
        mean_weekly_pnl_inr=float(pnl.mean()),
        sharpe_annualised=sharpe(pnl),
        sortino_annualised=float(pnl.mean() / (losses.std(ddof=1) if len(losses) > 1 else np.nan) * math.sqrt(52)) if len(losses) > 1 else None,
        max_drawdown_inr=float(dd.min()),
        win_rate=float((pnl > 0).mean()),
        avg_win_inr=float(wins.mean()) if len(wins) else 0.0,
        avg_loss_inr=float(losses.mean()) if len(losses) else 0.0,
        worst_week_inr=float(pnl.min()),
        best_week_inr=float(pnl.max()),
        total_costs_inr=float(tdf["costs_inr"].sum()),
        profit_factor=float(wins.sum() / abs(losses.sum())) if len(losses) and losses.sum() != 0 else None,
        walk_forward_selections=selections,
        parameters={k: (list(v) if isinstance(v, tuple) else v) for k, v in p.items()},
    )

# ----------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"))
    args = ap.parse_args()
    tdf, sdf, metrics = run_backtest(PARAMETERS, args.seed)
    os.makedirs(args.outdir, exist_ok=True)
    tdf.to_csv(os.path.join(args.outdir, "trades.csv"), index=False)
    tdf[["week", "pnl_inr", "cum_pnl_inr"]].to_csv(os.path.join(args.outdir, "equity_curve.csv"), index=False)
    sdf.to_csv(os.path.join(args.outdir, "walk_forward_selections.csv"), index=False)
    with open(os.path.join(args.outdir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2, default=float)
    print("SYNTHETIC-DATA SIMULATION — not advice, no guarantee of any live result.")
    print(f"Out-of-sample weeks: {metrics['trades']}  |  Total P&L: ₹{metrics['total_pnl_inr']:,.0f}"
          f"  |  Sharpe: {metrics['sharpe_annualised']:.2f}  |  Max DD: ₹{metrics['max_drawdown_inr']:,.0f}"
          f"  |  Win rate: {metrics['win_rate']:.1%}  |  Costs charged: ₹{metrics['total_costs_inr']:,.0f}")
    print("Walk-forward selections:", sdf.to_dict("records"))

if __name__ == "__main__":
    main()
