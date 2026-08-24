# Test Log

## 2026-08-24 — Crypto/FX tool live verification (repo bootstrap)

Environment: Claude (Fable 5) + live Lexfi MCP. One parallel batch,
10 calls, targeting the discovery-path tools not previously verified in
the sibling advisor library.

| Tool | Result | Findings |
|---|---|---|
| `get_crypto_global_metrics` | ✅ | Clean snapshot (total cap, dominance, 24h Δ). |
| `get_coin_markets` (per_page 20) | ✅ | Top ranks polluted by stablecoins/wrapped/illiquid oddities → filter trap added. |
| `get_funding_rates` | ✅ | ~100 coins × ~10 exchanges. **Dirty symbol field** (`XRPXRP`, `TRONTRX`, CJK dupes) → match on name. Per-interval rates; outliers are the signal. |
| `get_open_interest` | ✅ | **Non-crypto perps present** (XAU, CL, SNDK, SPCX, SKHYNIX) → filter trap added. Δ1h/Δ24h useful. |
| `get_liquidations` | ✅ | 4 windows, L/S split per coin. Clean. |
| `get_whale_alerts` | ✅ | ~$50M floor, 200 rows. **Same 5,441 WBTC moving hourly** (custody rotation) → dedupe trap added. Date gaps (24th → 20th). Direction only via exchange tags. |
| `get_onchain_flows` | ✅ | Altcoin-heavy; **paired same-size inflow/outflow churn**; no timestamps → net-per-asset trap added. |
| `get_daily_fx_pair` (EURUSD, windowed) | ✅ | `changePercent` already percent. **Weekend rows with thin volume** (Sun 08-23, 08-16) → exclusion trap added. Newest-first keys. |
| `get_crypto_news_sentiment` (BTCUSD, 14d) | ✅ | `XXXUSD` symbol format confirmed. Daily volume swings 3x (56–187) → proportions-not-counts trap added. |
| `get_ai_fx_ratio` (USD, 14d) | ✅ | Slow cumulative ratio; **stale-day repeats** (08-21 ≡ 08-23) and missing dates (08-22) → weekly-trend-only trap added. `diff_AI_FX_ratio` is the usable series. |

Net: 10/10 tools live, **6 new traps** documented in the playbook, all
marked **[V]** in the tool map.

## Inherited verification (2026-08-24, advisor library)

Equity/macro tools verified the same day in the sibling
financial-advisor-skills repo (shared MCP server), whose defects are
carried into this playbook's trap table: VIX `changePercent` unit
mismatch, `get_economic_calendar` 140 KB payload bomb, `get_cb_insights`
duplicate "quote shorts" rows, `get_analyst_estimates` far-future-first
ordering, and reaction-vs-today's-quote (`get_historical_prices` around
report date).

## Open items (before public launch tag)

- Layer-3 behavioral tests (RED baselines + collision matrix) per
  docs/skill-development.md for all 16 workflow skills.
- Live verification of remaining **[S]** tools (notably `get_etf_flows`,
  `get_coin_ohlcv`, prediction-market family, `get_congress_trading`,
  `get_alerts`, `list_market_datasets`).
- End-to-end execution of `opportunity-discovery` within budget on a live
  session, logged here (the examples/ scan was produced from the
  bootstrap verification batch).

## 2026-08-24 — First live opportunity-discovery run (dogfood)

Full cross-asset scan executed end-to-end following the skill verbatim:
13 new calls + 10 reused from session context (cap 18) across all three
funnel stages. Output honored the contract (named signal families,
opposing signals, invalidation per entry, "not surfaced but considered",
conviction capped where families were unknown).

New defect found and fixed: **`get_cb_calendar` `next_meeting` staleness**
— returned Mar 2026 as the Fed's next meeting while `get_rate_probabilities`
(fresher, as-of 23–24 Aug) carried the real Sep 2026 meetings. Trap added
to playbook + tool map: dates from rate_probabilities, calendar for
rates/last-change only. Also verified live: `get_rate_probabilities` with
bank omitted returns ALL banks in one call (cheaper than per-bank calls
for FX divergence work); `get_daily_dxy_index` changePercent confirmed
DECIMAL per schema (0.049 = +0.05%) — unlike get_daily_fx_pair (percent).
