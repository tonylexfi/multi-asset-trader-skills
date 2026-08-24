---
name: asset-deep-dive
description: Use when a trader names one specific asset and wants it researched — "research NVDA", "deep dive on Ethereum", "give me the full picture on AAPL", "what's going on with GBPUSD", "should I be looking at SOL?" — or wants a fast move explanation — "why did TSLA drop today?", "why is BTC up 5%?". Any single stock, ETF, coin, or FX pair. Not for earnings-specific reads, deep crypto positioning/on-chain structure, or two-sided currency macro dossiers.
license: MIT
---

# Asset Deep Dive

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Route any named symbol to the correct per-class evidence stack and return a
dossier that ends in the FACT → SIGNAL → INTERPRETATION ladder
`thesis-builder` consumes directly. Fast mode answers "why did X move?" from
one cheap parallel batch instead of a full workup.

## Supported Assets

US-listed equities & ETFs (Lexfi coverage strongest), major crypto assets,
G10 + liquid EM FX pairs. One asset per run — a list of symbols belongs in
`watchlist-monitor`. Handoffs: earnings-centric questions →
`earnings-analysis`; deep positioning/on-chain structure on a coin →
`crypto-intelligence`; two-sided currency macro dossier →
`fx-macro-analysis`; no asset named → discovery skills.

## Modes

| Mode | Trigger phrasing | Budget |
|---|---|---|
| **Deep** (default) | "research X", "full picture on X" | 6–10 calls, two batches max |
| **Fast** | "why did X move/drop/pump?" | 2–4 calls, ONE parallel batch |

## Required Inputs

The asset. Class detection: 1–5 char ticker → equity/ETF; known coin name or
CoinGecko id → crypto; 6-char pair (`EURUSD`) or two currency names → FX.
Genuinely ambiguous symbol (e.g. a ticker that is also a coin) → one compact
question, never a guess. Defaults: multi-week research horizon, 30–90 day
price windows, no direction assumed.

## Optional Inputs

Horizon, an existing position (long/short/watching), the specific question
behind the request ("thinking of adding"), risk tolerance.

## Lexfi MCP Calls

**Budget: Deep 6–10, Fast 2–4. Hard cap 10.** Pick per branch; skip any call
whose question the user did not raise.

**Deep — Equity branch:**
- Batch 1 (parallel): `get_stock_quote`, `get_company_profile`,
  `get_stock_news`, `get_key_metrics`
- Batch 2 (parallel, shaped by batch 1): `get_stocks_news_sentiment`
  (symbol), `get_earnings_surprises`, `get_insider_trades`; add
  `get_analyst_estimates` (raise `limit` — far-future-first ordering trap)
  only when the forward view matters; `get_historical_prices` (`from`/`to`)
  only when recent price structure is part of the question.

**Deep — Crypto branch:**
- Batch 1 (parallel): `get_coin_market_chart` (CoinGecko id, `days` "30" or
  "90"), `get_crypto_news_sentiment` (`XXXUSD`), `get_crypto_global_metrics`,
  `get_fear_greed_index` (the crypto one — never `get_cnn_fear_greed_index`)
- Batch 2 (parallel): `get_funding_rates`, `get_open_interest`,
  `get_liquidations`; `get_whale_alerts` / `get_onchain_flows` only for
  majors likely present in those feeds. If the user's question is mostly
  batch 2, hand off to `crypto-intelligence` instead.

**Deep — FX branch:**
- Batch 1 (parallel): `get_daily_fx_pair` (60-day window),
  `get_ai_fx_ratio` for base and quote currencies,
  `get_forex_news_sentiment`
- Batch 2 (parallel): `get_rate_probabilities` for each pair CB; add
  `get_cb_insights` (bankId `fed`/`ecb`/`boe`/`boj` only) when policy tone
  is the open question. A full policy/data divergence dossier → hand off to
  `fx-macro-analysis`.

**Fast mode (one parallel batch, 2–4 calls):**
- Equity: `get_stock_quote` + `get_stock_news`; add
  `get_stocks_news_sentiment` for tone trend or `get_intraday_prices` for
  today's shape.
- Crypto: `get_coin_market_chart` (`days` "1" or "7") +
  `get_crypto_news_sentiment` + `get_liquidations` (squeeze check).
- FX: `get_daily_fx_pair` (2-week window) + `get_forex_news_sentiment`; add
  `get_rate_probabilities` only if a CB is in the headlines.

**Applicable traps (from playbook):** analyst-estimates far-future-first
ordering; fear/greed tool swap; open-interest non-crypto perps; funding
dirty symbol field; whale custody rotations; on-chain churn pairs;
crypto-sentiment proportions over counts; `get_daily_fx_pair` weekend rows
and percent-units `changePercent`; `get_ai_fx_ratio` weekly-trend-only.

## Workflow

1. **Classify** the asset → branch and mode; resolve the symbol form the
   branch's tools expect (playbook Failure Handling).
2. **Plan the call set** against the budget; drop calls that don't serve the
   user's actual question.
3. **Run batch 1** → establish price/state context and the news picture.
4. **Run batch 2** (deep mode only) → positioning, smart money, forward
   view, policy — whichever the branch prescribes.
5. **Build the ladder**: facts with as-of dates → signals (window
   comparisons, divergences) → labeled interpretations. Conflicting signals
   are reported per evidence-discipline, never averaged away.
6. **Deliver.** Fast mode delivers after step 3 with a compact answer:
   the move, the best-supported driver(s), and what is NOT explained.

## Output Format

Deep mode:

```text
DEEP DIVE — <SYMBOL> (<class>) — <date>
Verdict: <2 lines — current state + the single most decision-relevant finding>

Snapshot: <price, chg, key level/metric, as-of>
What's driving it: <2–4 bullets, each naming its evidence + as-of>
Positioning / smart money: <branch-appropriate; or "not examined — <why>">
Forward view: <estimates / policy path / funding regime, per branch>

FACT:            <numbered list — only what calls returned, with as-of dates>
SIGNAL:          <numbered — changes/divergences, each citing its facts>
INTERPRETATION:  <numbered — each labeled, each citing its signals>

Thesis (working): <one falsifiable line + horizon> [interpretation]
Invalidation: <observable condition that kills it>
Key risks: <2–3, asset-appropriate>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

Fast mode: 6–12 lines — move size + window, ranked drivers with evidence,
one line on what remains unexplained, Sources line. No thesis unless asked.

## Quality Controls

- Every driver bullet cites a specific call result; "market weakness" with
  no evidence is banned.
- FACT contains zero interpretive grammar; INTERPRETATION contains zero
  unlabeled certainty. The three sections must be present and non-empty in
  every deep-mode output.
- Fast mode never exceeds 4 calls or grows a thesis section — if the user
  wants more, offer the deep dive rather than padding.
- A move explanation that finds no supporting evidence says "no identifiable
  driver in the data — likely flow/positioning driven [interpretation]",
  never a retrofitted story.
- Deep output ≤ ~60 lines; depth is density, not length.

## Failure Handling

- Symbol resolution fails after the playbook retry forms → ask one compact
  question with the closest matches found.
- A branch tool errors or returns empty → drop that evidence family, name
  it in Sources, continue with the rest.
- Plan-gated tools absent (transcripts, quant models) → the management-tone
  and model-forecast angles degrade to news-derived evidence; state it.
- More than half the planned evidence unavailable → say the dossier is not
  supportable today and deliver the fast-mode answer instead.

## Example Prompts

- "Research NVDA for me — thinking about a position."
- "Deep dive on Ethereum."
- "Why did TSLA drop today?"
- "What's going on with GBPUSD this week?"
- "Give me the full picture on Coinbase stock."
