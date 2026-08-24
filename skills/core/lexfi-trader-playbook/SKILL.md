---
name: lexfi-trader-playbook
description: Use when any trader skill needs current market, crypto, FX, macro, sentiment, positioning, or on-chain data — before calling any Lexfi MCP tool, when unsure which tool answers a question, when planning a discovery funnel, when a tool name looks ambiguous, or when a Lexfi call fails, returns unexpected units, or returns suspicious duplicates.
license: MIT
---

# Lexfi Trader Playbook

## Overview

Lexfi MCP is the financial intelligence layer behind every skill in this
library. This playbook is the routing table: which tool answers which trader
question, across equities, crypto, FX, and macro; in what order; within what
call budget; and which traps to avoid. Workflow skills reference this playbook
instead of re-documenting tools.

**Core principle: fewest calls that fully answer the question.** MCP calls are
metered (Pro: 1,000/month, Pro Max: 3,000/month). A discovery scan that burns
40 calls is a design failure, not thoroughness. Plan the call set before the
first call, batch independent calls in parallel, never re-fetch what is
already in context.

## Tool Availability & Plans

Lexfi tools may be **deferred** in a session (visible by name only). Load every
tool you plan to use in ONE ToolSearch batch — never one at a time. Tool names
carry an `mcp__<server>__` prefix; bare names below are the suffix.

Not every user has every tool. Plan-gated capabilities (Pro Max only):
**News Intelligence, Quant Lexfi Models, Company Transcripts, Central Bank
Transcripts, Strategy holdings.** If a gated tool is absent or errors with a
plan message, degrade per the skill's Fallbacks section and say what was
skipped — never silently substitute model knowledge.

## Call Budgets (defaults; skills may tighten)

| Workflow type | Budget | Notes |
|---|---|---|
| Quick answer ("why did X move?") | 2–4 calls | One parallel batch |
| Single-asset deep dive | 6–10 calls | Two batches max |
| Discovery scan (one asset class) | 8–12 calls | Funnel discipline below |
| Cross-asset discovery scan | 12–18 calls | Broad layer is cheap snapshot tools |
| Watchlist monitor (≤10 assets) | 8–14 calls | Batch symbols; delta-focus |

**Discovery funnel discipline** — never deep-research a universe:

```text
Broad universe        → cheap breadth tools only (1 call each:
                        get_coin_markets, get_market_movers,
                        get_sector_performance, get_crypto_global_metrics)
Candidate set (~10–20)→ one signal tool per dimension, batched
Shortlist (3–5)       → targeted depth (news, positioning, catalysts)
```

## Routing by Trader Question

### Market state & regime
| Question | Tool sequence |
|---|---|
| "Where is the market today?" | `get_market_overview` + `get_sector_performance` (parallel) |
| "Risk-on or risk-off?" | `get_daily_vix_index` + `get_cnn_fear_greed_index` + `get_crypto_global_metrics` + `get_daily_dxy_index` (parallel) |
| "What macro regime are we in?" | `get_us_macro_regime`; add `get_macro_inflation` / `get_macro_credit_liquidity` for detail |
| "What's moving right now?" | `get_market_movers` (equities) + `get_coin_markets` (crypto) |

### Equities
| Question | Tool sequence |
|---|---|
| "Why did X move?" | `get_stock_quote` + `get_stock_news` (parallel); add `get_stocks_news_sentiment` for tone trend |
| "Is X expensive?" | `get_key_metrics`; add `get_analyst_estimates` for forward view |
| "What did management say?" | `get_earnings_calls_by_ticker` → `get_earnings_call_insights` (two-step, always) |
| "Beat/miss history?" | `get_earnings_surprises` |
| "Smart-money view?" | `get_insider_trades` + `get_superinvestor_activity` + `get_congress_trading` (parallel) |
| "What's inside this ETF?" | `get_etf_holdings` |

### Crypto
| Question | Tool sequence |
|---|---|
| "State of crypto?" | `get_crypto_global_metrics` + `get_coin_markets` (parallel) |
| "Why did BTC move?" | `get_coin_market_chart` + `get_crypto_news_sentiment` + `get_liquidations` (parallel) |
| "Positioning crowded?" | `get_open_interest` + `get_funding_rates` (parallel) |
| "Whales accumulating?" | `get_whale_alerts` + `get_onchain_flows` (parallel) — read traps first |
| "Where is DeFi capital rotating?" | `get_chains_tvl` |
| "Crypto narrative?" | `get_crypto_x_highlights` / `get_crypto_reddit_highlights` / `get_telegram_highlights` |
| "Crypto fear/greed?" | `get_fear_greed_index` (this one IS the crypto one) |

### FX & rates
| Question | Tool sequence |
|---|---|
| "How has EUR/USD traded?" | `get_daily_fx_pair` (symbol `EURUSD`, date-windowed) |
| "Dollar regime?" | `get_daily_dxy_index` + `get_ai_fx_ratio` (currency `USD`) |
| "Is the market pricing cuts?" | `get_rate_probabilities` (bank short code) |
| "Has the Fed/ECB tone changed?" | `get_cb_insights` (bankId `fed`, `ecb`, `boe`, `boj`) |
| "Currency news tone?" | `get_forex_news_sentiment` + `get_ai_fx_ratio` per currency |
| "Macro divergence between two economies?" | `get_macro_forecasts` / `get_country_metrics` per country + `get_rate_probabilities` per CB |
| "EM currency snapshot?" | `get_macro_weekly_series_catalog` → `get_macro_weekly_snapshot`; `get_daily_fx_local_vs_usd` |

### Catalysts & events
| Question | Tool sequence |
|---|---|
| "What's on the calendar?" | `get_economic_calendar` (1–2 day windows ONLY) + `get_cb_calendar` (parallel) |
| "Upcoming earnings for X?" | `get_earnings_calls_by_ticker` (dates of past calls establish cadence) + `get_stock_news` |
| "What is the market handicapping?" | `get_stocks_prediction_markets` / `get_macro_prediction_markets` / `get_crypto_prediction_markets` |
| "IPO / M&A flow?" | `get_ipo_calendar` / `get_mergers_acquisitions` |

Full per-tool notes: `references/tool-map.md`. Read it before composing a call
plan for a workflow not listed above.

## Known Traps (live-verified — check every one that applies)

| Trap | Reality |
|---|---|
| `get_forecast` | **Weather**, not financial. Macro projections = `get_macro_forecasts`. |
| `get_fear_greed_index` vs `get_cnn_fear_greed_index` | First is **crypto**, second is **equities**. Never swap. |
| `get_etf_flows` | **Crypto spot ETFs only** (BTC/ETH/SOL). Not equity fund flows. |
| `get_open_interest` symbols | Includes **non-crypto perps**: XAU (gold), CL (oil), tokenized equities (SNDK, SPCX, SKHYNIX). Filter before making crypto-wide claims. |
| `get_funding_rates` symbols | Symbol field is dirty (`XRPXRP`, `TRONTRX`, CJK duplicates). Match on the name column; rates are per-funding-interval, not annualized. Near-zero average is normal — the signal is outliers and sign flips. |
| `get_whale_alerts` | ~$50M floor, 200 rows, with **repeated identical-quantity transfers** (custody/collateral rotations, e.g. the same 5,441 WBTC hourly). Count unique flows only; direction is meaningful only when an exchange entity is tagged. History has date gaps. |
| `get_onchain_flows` | Altcoin-heavy (AAVE/LINK/UNI/gold tokens), paired same-size inflow+outflow rows are market-maker churn. **Net the flows per asset**; no timestamps — treat as recent-window snapshot. |
| `get_daily_fx_pair` | `changePercent` already in percent units. Includes weekend/holiday rows with thin volume — exclude from range/volatility claims. Dates keyed newest-first. |
| `get_ai_fx_ratio` | Slow-moving cumulative news ratio; values repeat on stale days and dates can be missing. Trend via `diff_AI_FX_ratio` over weeks, never day-over-day claims. |
| `get_crypto_news_sentiment` | Symbol format `BTCUSD`. Daily article counts swing 3x (weekends thin) — compare **proportions**, not raw counts. |
| `get_coin_markets` | Top ranks include stablecoins, wrapped assets, and illiquid oddities. Filter stables/wrapped before breadth or leadership claims. |
| VIX `changePercent` | Schema says decimal; live data returns percent. Sanity-check against change/prior close before scaling. |
| `get_earnings_call_insights` | Requires `transcriptId` from `get_earnings_calls_by_ticker` first. Never guess IDs. `tables:["ais","metrics"]` covers most needs; `includeTranscript=true` is a 50–200 KB payload — verbatim quotes only. |
| `get_cb_insights` | bankId short codes only (`fed`, `ecb`, `boe`, `boj`). Numerics arrive as decimal strings. One date can carry duplicate "quote shorts" clip rows — use `summary` + full conferences only. |
| `get_rate_probabilities` | Latest snapshot only, ~10 forward meetings, no history — never claim "pricing has shifted" from one call. |
| `get_economic_calendar` | Global, unfiltered payload bomb: 7 days ≈ 140 KB. Use 1–2 day windows; scan for major-economy events only. |
| `get_analyst_estimates` | Rows ordered far-future-first — raise `limit` to reach near quarters. |
| `get_macro_weekly_snapshot` | Needs exact sheet names — discover via `get_macro_weekly_series_catalog` first. |
| `get_cb_calendar` | `next_meeting` dates can be badly stale (months old). Take meeting dates from `get_rate_probabilities`; use the calendar only for current rates / last change. |

## Call Discipline

1. **Plan before calling.** List needed facts → map to fewest tools → mark
   parallel-safe calls → check budget.
2. **Batch parallel calls.** Quotes, sentiment, positioning, calendars have no
   interdependencies — one round trip.
3. **Sequence only true dependencies.** transcript listing → insights;
   catalog → snapshot.
4. **Subset when the tool allows it.** Date-window every history tool; table
   subsets on transcript insights; `per_page` on coin markets.
5. **Batch symbols.** `get_stock_quote` takes comma-separated symbols — one
   call for a whole watchlist.
6. **Do not call Lexfi at all when** the question is conceptual ("what is
   funding rate?"), the user wants reformatting, or the data is already in
   context.

## Failure Handling

- Tool error or empty result → state it in the output ("Data unavailable:
  X"), never fill the gap silently. Model knowledge used for context must be
  labeled `[model knowledge — not Lexfi data]`.
- Ticker/symbol resolution failure → equities: try `TICKER:CC` country
  suffix; FX: 6-char pair form (`EURUSD`); crypto: CoinGecko id for chart
  tools (`bitcoin`), `XXXUSD` for sentiment.
- Partial data → use what returned; list gaps in the Sources line.
- Stale timestamps → report the as-of date next to the figure; never present
  old data as current.

## Red Flags — Stop and Re-plan

- Same tool, same arguments, twice
- More than the budgeted calls without a written plan
- A number you can't attribute to a specific call
- Crypto-wide claims from unfiltered `get_open_interest` / `get_coin_markets`
- Directional whale claims from untagged or repeated transfers
- `get_forecast`, wrong fear/greed tool, or `get_etf_flows` for equities
