---
name: macro-impact-analysis
description: Use when a trader names a macro scenario, event, or policy shift and asks what it means for specific assets or who wins/loses — "what does a Fed cut mean for my tech stocks?", "who benefits from falling rates?", "how would a hot CPI print hit BTC?", "if the dollar keeps strengthening, what suffers?", "trace the impact of QT ending". Scenario→asset questions, hypothetical or live.
license: MIT
---

# Macro Impact Analysis

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Turn "what does <macro scenario> mean for <assets>?" into explicit
transmission chains — each link a checkable claim labeled fact/signal/
interpretation — instead of the vague "risk assets should benefit" a plain
conversation produces. The chain diagram is the product: the trader sees
*where* the mechanism could break, not just the conclusion.

## Supported Assets

Endpoints can be US equities/sectors/ETFs, major crypto assets, G10 + liquid
EM FX, and commodities (via `get_macro_asset_prices` /
`get_daily_commodity_series`). NOT a regime dashboard ("what regime are we
in?" → `market-regime`) and NOT open-ended discovery ("find opportunities in
a falling-rate world" → `opportunity-discovery` with criteria).

## Required Inputs

The scenario. If the user names none, ask ONE compact question ("Which
scenario — e.g. Fed cuts faster than priced, dollar keeps rising, hot
inflation print?"). Asset endpoints are optional: if named, chains terminate
there; if not, the skill terminates chains at the 3–5 most exposed asset
groups and says so.

## Optional Inputs

Horizon (default: weeks–months), direction of interest (long/short/both),
existing positions (chains get tagged "affects your <X>"), severity
("mild repricing" vs "shock").

## Lexfi MCP Calls

**Budget: 8–12 calls, two batches max.** The scenario decides the macro
tools; endpoints decide the asset checks. Never call the full macro suite.

**Batch 1 — scenario state + market pricing (4–6 calls, parallel).**
Always: `get_rate_probabilities` (relevant CB short code — what's already
priced is the baseline every chain starts from) and `get_macro_asset_prices`
(cross-asset returns — how correlated legs have actually been trading).
Then 2–4 scenario-relevant tools only:

| Scenario family | Add |
|---|---|
| Rates/Fed path | `get_macro_yield_curve`, `get_cb_insights` (`fed`), `get_cb_calendar` |
| Inflation print | `get_macro_inflation`, `get_macro_news_sentiment` |
| Dollar move | `get_daily_dxy_index` (windowed), `get_ai_fx_ratio` (`USD`) |
| Liquidity/QT | `get_macro_credit_liquidity`, `get_crypto_global_metrics` |
| Growth scare | `get_us_macro_regime`, `get_macro_economic_growth` |
| Event handicapping | `get_macro_prediction_markets` (label market-implied) |

**Batch 2 — endpoint checks (2–5 calls, parallel), named beneficiaries/
victims ONLY:** equities: `get_stock_quote` (comma-batched, ONE call) and/or
`get_sector_performance`; crypto: `get_coin_markets` (one page) or
`get_coin_market_chart` for a single named coin; FX: `get_daily_fx_pair`.
Skip entirely when the user asked for the map, not current levels.

**Applicable traps (from playbook):** `get_rate_probabilities` is a
snapshot — never claim "pricing has shifted" from one call; `get_cb_insights`
bankId short codes + ignore quote-shorts rows; `get_daily_fx_pair` /
`get_daily_dxy_index` weekend rows excluded from range claims; `get_forecast`
is WEATHER — macro projections are `get_macro_forecasts`; economic-calendar
payload bomb (1–2 day windows) if event timing is checked.

## Workflow

1. **Pin the scenario** — restate it as a delta vs what's currently priced
   (from `get_rate_probabilities` / prediction markets). "Fed cuts" priced
   at 90% is a different scenario from the same cut priced at 40%.
2. **Draw the chains before judging them.** 2–4 chains, each 3–5 links,
   e.g. Fed expectations → USD → US multinationals' earnings → equities;
   liquidity → BTC → alt risk appetite; rates → financial conditions →
   sector rotation. Every link gets a label:
   - **[fact]** — a Lexfi call returned it (cite as-of),
   - **[signal]** — a change/divergence in the data,
   - **[interpretation]** — the mechanism claim connecting them.
   A chain of pure interpretations is a story — each chain needs ≥1 fact
   and ≥1 signal link or it is flagged "mechanism unverified in data".
3. **Batch 2** — check whether named endpoints are already moving/priced
   for the scenario (the boring "already priced" answer is considered
   first, per evidence-discipline).
4. **Rate each chain**: strength (are the middle links currently
   confirming?), speed (repricing vs earnings-lag), and the weakest link
   (where it breaks). Conflicting chains are reported, not averaged.
5. **Deliver** — chains, per-endpoint net exposure, and what would
   invalidate the transmission.

## Output Format

```text
MACRO IMPACT — <scenario> — <date>
Scenario vs market pricing: <what's priced now [fact] → what the scenario adds>

CHAIN 1: <A> → <B> → <C> → <endpoint>
  <A → B>   [fact|signal|interpretation]  <evidence, as-of>
  <B → C>   [fact|signal|interpretation]  <evidence>
  <C → end> [fact|signal|interpretation]  <evidence>
  Strength: <confirming/mixed/unverified>   Weakest link: <which + why>

CHAIN 2: …

Endpoint impact map:
Asset/group        Direction   Via chain   Already priced?      Conviction
<SYMBOL/group>     <+/−/±>     <1/2>       <yes/partly/no [signal]>  <L/M/H>

Conflicts: <chains pulling opposite ways on the same asset, weighting + why>
What breaks the transmission:
• <observable condition> → kills chain <n>
Research, not a recommendation.
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Every chain link carries exactly one label; banned: an unlabeled arrow or
  a chain stated only as its conclusion.
- No chain with zero [fact] links may drive a Medium+ conviction endpoint.
- "Already priced?" answered per endpoint from batch-1/2 data — never
  assumed either way.
- 2–4 chains, 3–5 links each; a 7-link chain is speculation stacking —
  split or cut it.
- Endpoint conviction High requires the chain's middle links confirming in
  current data AND no opposing chain — otherwise cap at Medium.
- Output ≤ ~60 lines; per-asset depth belongs to `asset-deep-dive`.

## Failure Handling

- A scenario-tool error → chain links that depended on it degrade to
  [interpretation] with "mechanism unverified in data"; say so in the
  chain rating.
- Plan-gated tools (`get_cb_insights` conferences, quant
  `get_macro_forecasts` models — Pro Max) absent → build chains from rate
  probabilities + market data, note the CB-tone/forecast leg was skipped.
- Endpoint symbol unresolved → per playbook symbol rules; if still
  unresolved, keep it in the impact map with "Data unavailable: quote".
- Scenario is pure hypothetical with no live pricing anchor (e.g. "oil at
  $200") → run the chains, label all baseline links [model knowledge —
  not Lexfi data], and say the market-pricing column is not applicable.

## Example Prompts

- "What does a Fed cut in September mean for my tech stocks?"
- "Who benefits from falling rates?"
- "How would a hot CPI print transmit to BTC?"
- "If the dollar keeps strengthening, which assets suffer most?"
- "Trace what the end of QT would mean for crypto and small caps."
