# Lexfi MCP Tool Map — Multi-Asset

Per-tool reference for composing call plans. Bare names — sessions prefix them
with `mcp__<server>__`. Verification status: **[V]** = live-verified against
Lexfi MCP (2026-08-24), **[S]** = schema-reviewed, not yet live-tested.

## Market State (Equities)

| Tool | Returns | Notes |
|---|---|---|
| `get_market_overview` [V] | Major index + ETF quotes | No params. Opening context for any brief. |
| `get_sector_performance` [V] | Cross-sector daily changes + valuation | No params. Rotation/leadership. |
| `get_market_movers` [V] | Gainers / losers / actives | `type` param. Cheap breadth layer for stock discovery. |
| `get_stock_quote` [V] | Real-time snapshot, comma-separated symbols | Batch ALL tickers in one call. |
| `get_historical_prices` [V] | Daily OHLCV, date range | Always `from`/`to`. |
| `get_intraday_prices` [S] | Intraday bars | Today-focused questions only. |

## Company Fundamentals (Equities)

| Tool | Returns | Notes |
|---|---|---|
| `get_company_profile` [V] | Sector, industry, CEO, description | Context before deep analysis. |
| `get_key_metrics` [V] | P/E, EV/EBITDA, ROE/ROA, leverage, FCF | `period` + `limit` for history. |
| `get_financial_statements` [S] | Full statements | Only when line items matter. |
| `get_analyst_estimates` [V] | Forward consensus EPS/revenue/EBITDA | Far-future-first ordering — raise `limit` for near quarters. |
| `get_analyst_ratings` [S] | Ratings | |
| `get_earnings_surprises` [V] | Estimated vs actual EPS history | Beat/miss consistency. |
| `get_earnings_calls_by_ticker` [V] → `get_earnings_call_insights` [V] | Transcript list → AI insights | Two-step, always. `tables:["ais","metrics"]` default; `includeTranscript=true` only for verbatim quotes (50–200 KB). Plan-gated (Pro Max). |
| `get_company_executives` / `get_company_compensations` / `get_employee_count` [S] | Management context | Tier-2 depth. |

## Crypto — Market

| Tool | Returns | Notes |
|---|---|---|
| `get_crypto_global_metrics` [V] | Total cap, 24h volume, BTC/ETH dominance | No params. Top-down crypto regime in one call. |
| `get_coin_markets` [V] | Price/mcap/volume/24h table, paginated | `per_page` ≤250, `category` filter (e.g. `decentralized-finance-defi`, `meme-token`). Top ranks include stablecoins/wrapped — filter before breadth claims. |
| `get_coin_market_chart` [V] | Price/mcap/volume history | `coin_id` is CoinGecko id (`bitcoin`, `ethereum`); `days` is a string enum ("1","7","30","90",…). |
| `get_coin_ohlcv` [S] | OHLCV candles | For technical structure. |
| `get_cmc100_index` [S] | CMC 100 index | Broad-market beta proxy. |
| `get_fear_greed_index` [V] | CRYPTO fear/greed | The crypto one. Equities = `get_cnn_fear_greed_index`. |

## Crypto — Derivatives & Positioning

| Tool | Returns | Notes |
|---|---|---|
| `get_open_interest` [V] | OI snapshot, ~20 top symbols, Δ1h/Δ24h + funding + volume | Contains NON-crypto perps (XAU, CL, tokenized equities SNDK/SPCX/SKHYNIX) — filter. OI rising + price rising = new longs; OI rising + price falling = new shorts (interpretation, label it). |
| `get_funding_rates` [V] | Per-coin avg funding across ~10 exchanges | No params, ~100 coins. Dirty symbol field — match on name. Per-interval rates; outliers and negative prints are the signal. |
| `get_liquidations` [V] | Long/short liquidations, 1h/4h/12h/24h windows | Squeeze detection: lopsided L/S ratio + price move = forced unwind fuel spent. |
| `get_etf_flows` [S] | Crypto spot ETF flows (BTC/ETH/SOL) | Institutional demand proxy. NOT equity funds. |

## Crypto — On-Chain & Narrative

| Tool | Returns | Notes |
|---|---|---|
| `get_whale_alerts` [V] | Large transfers (~$50M floor), 200 rows | Dedupe repeated identical-quantity rows (custody rotations). Direction only meaningful with exchange tags: → exchange = potential sell supply; ← exchange = withdrawal/custody. Date gaps exist. |
| `get_onchain_flows` [V] | Exchange inflow/outflow by token, ~$1M floor | Altcoin-heavy. NET per asset; paired same-size rows are churn. No timestamps. |
| `get_chains_tvl` [V] | Chain TVL leaderboard + change | Capital rotation across ecosystems. |
| `get_crypto_news_sentiment` [V] | Daily pos/neu/neg counts | `symbol` as `XXXUSD` or omit for aggregate. Compare proportions, not counts (volume swings 3x). |
| `get_crypto_x_highlights` / `get_crypto_reddit_highlights` / `get_crypto_stocktwits_highlights` [S] | Curated social chatter | Discourse, never fact. |
| `get_telegram_highlights` / `get_telegram_messages` [S] | Telegram intel | Discourse. |
| `get_crypto_prediction_markets` [S] (+ kalshi/polymarket/futuur variants) | Market-implied odds on crypto events | Label as market-implied. |

## FX & Rates

| Tool | Returns | Notes |
|---|---|---|
| `get_daily_fx_pair` [V] | Daily OHLCV for any pair | Symbol `EURUSD` form. `changePercent` already percent. Weekend rows present with thin volume — exclude from vol/range claims. Newest-first keys. |
| `get_daily_fx_local_vs_usd` [S] | Local currency vs USD | EM coverage. |
| `get_daily_dxy_index` [V] | Dollar index history | Date-window. |
| `get_ai_fx_ratio` [V] | News-derived currency strength/weakness ratio + `diff_AI_FX_ratio` | Per currency (`USD`, `EUR`, `ARS`…). Slow-moving; stale-day repeats and missing dates. Weekly trend only. |
| `get_forex_news_sentiment` [S] | FX news tone counts | Same shape as other sentiment tools. |
| `get_macro_reddit_forex_highlights` / `get_macro_stocktwits_forex_highlights` [S] | Retail FX discourse | Discourse. |
| `get_current_market_rates` / `get_rate_curve` [S] | Rates | Rate-differential legwork. |
| `get_rate_probabilities` [V] | Market-implied CB move odds, ~10 meetings | Bank short code. Snapshot only — no history. |
| `get_cb_insights` [V] | Hawk/dove, sentiment, uncertainty indices per conference + rolling trend | `fed`/`ecb`/`boe`/`boj`. Decimal-string numerics. Ignore "quote shorts" clip rows. Plan-gated transcripts. |
| `get_cb_calendar` [V] | Upcoming CB meetings | No params. |
| `get_cb_conference_transcript` [S] | Full CB transcript | Plan-gated (Pro Max); verbatim only. |

## Macro

| Tool | Returns | Notes |
|---|---|---|
| `get_us_macro_regime` [V] | Regime probabilities | Probabilistic framing — never binary. |
| `get_macro_inflation` [V] | CPI + PCE families | Set `limit` (default 10 years). |
| `get_macro_economic_growth` / `get_quarterly_real_gdp_yoy` / `get_monthly_cpi_yoy` [S] | Growth/inflation series | |
| `get_macro_credit_liquidity` [S] | Credit & liquidity conditions | The liquidity leg of crypto/risk theses. |
| `get_macro_yield_curve` [V] | UST tenors 3M–30Y per date | Compare 2Y vs 10Y explicitly. |
| `get_macro_uncertainties` [V] | Policy/geopolitical uncertainty indices | `limit` in days. |
| `get_economic_calendar` [V] | Global events | PAYLOAD BOMB — 1–2 day windows only. |
| `get_macro_forecasts` / `get_macro_forecast_horizons` / `get_macro_forecast_country_ranking` / `get_macro_forecast_model_info` [S] | Model-based macro projections | The real forecast tools — NOT `get_forecast` (weather). Quant models plan-gated. |
| `get_macro_weekly_series_catalog` → `get_macro_weekly_snapshot` → `get_macro_weekly_series` [V] | EM/country weekly macro | Catalog first; exact sheet names. |
| `get_country_metrics` [S] | Country metrics | FX divergence work. |
| `get_macro_asset_prices` [S] | Sector/commodity/factor ETF returns | Cross-asset correlation layer. |
| `get_daily_commodity_series` / `get_daily_sp500_index` / `get_daily_vix_index` [V] | Series histories | VIX changePercent units trap. |
| `get_macro_news` / `get_macro_news_sentiment` / `get_general_news_sentiment` [S] | Macro headlines + tone | |
| `get_macro_x_highlights` / `get_macro_reddit_highlights` / `get_macro_stocktwits_highlights` [S] | Macro discourse | |
| `get_macro_housing` [S] | Housing data | |
| `get_us_macro_regime` + `get_macro_prediction_markets` [S] | Regime + market-implied odds | |

## Smart Money & Positioning (Equities)

| Tool | Returns | Notes |
|---|---|---|
| `get_insider_trades` [V] | Form 4 buys/sells per symbol | Conviction signal. |
| `get_congress_trading` [S] | Congressional trades | Disclosure-lagged — check dates. |
| `get_institutional_holders` [S] | 13F ownership | Quarterly lag. |
| `get_superinvestors` / `get_superinvestor_holdings` / `get_superinvestor_activity` [S] | Notable investor moves | Quarterly lag. |
| `get_fund_disclosures` / `search_fund_disclosures` / `get_stock_fund_exposure` [S] | Fund holdings | Which funds hold a stock. |
| `get_stocks_prediction_markets` [S] (+ venue variants) | Market-implied odds on stock events | |

## ETFs & Calendars

| Tool | Returns | Notes |
|---|---|---|
| `get_etf_holdings` / `get_etf_profile` / `get_etf_aum` [S/V] | ETF constituents/metadata | Exposure decomposition. |
| `get_ipo_calendar` / `get_mergers_acquisitions` [S] | Deal flow | Catalyst discovery. |
| `get_alerts` [S] | Lexfi alert stream | Check availability per session. |
| `list_market_datasets` [S] | Dataset catalog | Capability discovery — run when unsure what this user's plan exposes. |

## Argentina / Merval (specialist)

The `lexfi_macro_merval_*` family (bonds, breakevens, FX convertibility,
panels) plus `get_macro_merval_*` dashboards cover Argentine markets. Only
route here when the user asks about Argentina; see tool descriptions.

## Sentiment tools disambiguation

| Domain | Tool |
|---|---|
| Equities aggregate/per-ticker | `get_stocks_news_sentiment` |
| Crypto aggregate/per-coin | `get_crypto_news_sentiment` (`XXXUSD`) |
| FX | `get_forex_news_sentiment`, `get_ai_fx_ratio` |
| Macro | `get_macro_news_sentiment` |
| Everything | `get_general_news_sentiment` |
| Equity fear/greed | `get_cnn_fear_greed_index` |
| Crypto fear/greed | `get_fear_greed_index` |
