---
name: crypto-discovery
description: Use when a trader asks for crypto ideas by name of class — "find me coins/tokens…", "what crypto looks interesting", "any setups in DeFi or memecoins", "which coins have whales accumulating", "where is funding stretched", "find altcoins with momentum". Crypto-scoped requests only; mixed or open-ended cross-asset requests trigger opportunity-discovery instead.
license: MIT
---

# Crypto Discovery

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Find crypto assets where market structure, positioning, on-chain, and
narrative signals converge — exploiting the fact that Lexfi's positioning
tools are cross-coin snapshots, so one call scores the whole universe.
Output feeds `crypto-intelligence` and `thesis-builder`.

## Supported Assets

Major and mid-cap crypto assets covered by `get_coin_markets` (top ~250),
including category slices (DeFi, memecoins, L1s). NOT supported here:
micro-caps outside coverage, equities (`stock-discovery`), FX
(`fx-discovery`), cross-asset scans (`opportunity-discovery`).

## Required Inputs

None. Defaults: top-100 universe (stables and wrapped assets filtered out),
5 candidates (10 on request), multi-week horizon, no direction constraint.

## Optional Inputs

Category (`decentralized-finance-defi`, `meme-token`, …), direction, count,
horizon, market-cap floor, coins already held (exclude or flag), risk
appetite (memecoins excluded by default unless asked).

## Lexfi MCP Calls

**Budget: 8–12 calls, hard cap 12.** The signal layer is nearly free in
call terms because every positioning tool is a cross-coin snapshot — spend
the saved budget on shortlist depth, never on widening the universe.

**Stage 1 — Breadth (one parallel batch, 2–3 calls):**
`get_crypto_global_metrics` (regime: total cap, dominance),
`get_coin_markets` (`per_page` 100; add `category` when the user scopes),
`get_fear_greed_index` (the crypto one — never `get_cnn_fear_greed_index`).

**Stage 2 — Cross-coin signal layer (one parallel batch, 3–5 calls, each
covering the whole universe):** `get_funding_rates` (match on name column;
outliers and sign flips are the signal), `get_open_interest` (filter
non-crypto perps: XAU, CL, tokenized equities), `get_liquidations`
(lopsided L/S by window), `get_crypto_news_sentiment` (aggregate, no
symbol); `get_chains_tvl` when the criteria touch ecosystems/DeFi rotation.

**Stage 3 — Shortlist depth (3–5 coins, 1–2 calls each, batched):**
`get_crypto_news_sentiment` (symbol `XXXUSD`), `get_whale_alerts` +
`get_onchain_flows` (one call each covers all coins — dedupe and net per
the traps), `get_coin_market_chart` (`coin_id` CoinGecko id, `days` "30")
only when the thesis needs price structure; `get_crypto_x_highlights` /
`get_crypto_reddit_highlights` for narrative — discourse, never fact.

**Applicable traps (playbook, non-negotiable):** stables/wrapped filtered
before any breadth or leadership claim; `get_open_interest` non-crypto
symbols; `get_funding_rates` dirty symbol field + per-interval units;
`get_whale_alerts` custody rotations (count unique flows; direction only
with exchange tags); `get_onchain_flows` churn pairs (net per asset, no
timestamps); sentiment proportions over raw counts; both fear/greed tools
correctly assigned.

## Workflow

1. **Parse criteria** → category, direction, count, risk appetite. One
   compact clarifying question max.
2. **Stage 1 batch** → regime (cap trend, BTC/ETH dominance direction,
   fear/greed) and the filtered universe table.
3. **Nominate ~10–20 candidates**: unusual 24h/7d movers, dominance-rotation
   beneficiaries, category leaders/laggards — and non-movers in a moving
   category (divergence seeds). Cite the stage-1 evidence for each.
4. **Stage 2 batch** → score every candidate from the SAME four snapshots:
   funding (crowding/sign), OI direction vs price (new longs vs new shorts —
   interpretation, label it), liquidation asymmetry, sentiment proportion
   trend. Record families aligned / opposed / unknown.
5. **Materiality test** — a candidate advances only if ≥2 independent
   families align AND its evidence survives the trap filters (a whale
   "accumulation" made of repeated identical-quantity transfers is zero
   families, not one).
6. **Stage 3 batch on the top 3–5** → on-chain confirmation, per-coin
   sentiment, narrative check; find the catalyst or mechanism; write the
   invalidation.
7. **Deliver** — why now, what converges, what breaks it, per coin.

## Output Format

```text
CRYPTO DISCOVERY SCAN — <date>
Criteria: <restated>        Category: <all/slice>     Direction: <any/long/short>
Regime: <1–2 lines: total cap trend, dominance shift, crypto fear/greed>

1. <SYMBOL> — <name>            <category> · Conviction: <Low/Med/High>
   Why it surfaced:
   • <signal family>: <specific evidence, as-of date>
   • <signal family>: <specific evidence>
   • <signal family>: <specific evidence>
   Positioning read: <funding/OI/liquidation state in one line> [interpretation]
   Opposing: <strongest counter-signal, or "none found">
   Catalyst: <dated event or mechanism, or "none — flow-driven">
   Thesis (working): <one falsifiable line> [interpretation]
   Invalidation: <observable condition>
   Key risks: <2–3 crypto-appropriate: liquidity / unlocks / concentration /
   regulatory / narrative reversal>

2. …

Not surfaced but considered: <2–3 near-misses + the family that failed>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- The universe table is stables/wrapped-filtered BEFORE any claim about
  breadth, leadership, or "top movers".
- Every on-chain claim states which trap filter it survived (deduped,
  netted, exchange-tagged) — an unfiltered whale bullet is banned.
- Funding/OI evidence names the coin via the name column, never the raw
  symbol field.
- Sentiment evidence uses proportions across a window, never one day's raw
  counts.
- Conviction High requires ≥3 aligned independent families + catalyst + no
  strong opposing family; positioning and liquidations together count as
  ONE family (both are derivatives-crowding evidence).
- Output ≤ ~110 lines for 5 candidates; depth belongs in `crypto-intelligence`.

## Failure Handling

- A stage-2 snapshot errors → that family drops for ALL candidates (level
  field), note it in Sources, continue.
- Plan-gated tools (quant Lexfi models — Pro Max only) → macro-forecast
  context degrades to `get_crypto_global_metrics` regime facts; say so.
  Transcript-class tools are not used by this skill.
- `coin_id` resolution failure on chart calls → use the CoinGecko id form
  (`bitcoin`, not `BTC`); if unresolved, deliver without price structure and
  flag the gap.
- Fewer than 3 candidates with ≥2 aligned families → report "no strong
  convergence in crypto today" with the best 1–2 partial setups — never
  inflate.

## Example Prompts

- "Find me interesting crypto setups right now."
- "Which coins have whales accumulating and positive funding divergence?"
- "Any DeFi tokens worth a look this week?"
- "Where is the memecoin froth — anything shortable?"
- "Find altcoins with momentum that isn't just BTC beta."
