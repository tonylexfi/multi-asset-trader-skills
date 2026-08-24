---
name: watchlist-monitor
description: Use when a trader wants a delta update on a list of assets they follow — "what's changed in my watchlist?", "update me on my list", "anything new on my positions since yesterday?", "morning check on NVDA, BTC, EURUSD", "did anything move on my names?" — for any recurring check-in on a defined set of symbols, mixed asset classes included.
license: MIT
---

# Watchlist Monitor

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Answer "what's changed?" — and ONLY what's changed — across a watchlist.
The contract is the diff: no re-summarizing what a company does, no
restating a thesis the user already wrote, no filler rows for assets where
nothing happened. A plain conversation re-researches each name; this skill
amortizes shared calls across the whole list.

## Supported Assets

Mixed watchlists of US equities/ETFs, major crypto, and G10/liquid EM FX
pairs — the normal case, not an edge case. NOT initial research on a new
name (→ `asset-deep-dive`) and NOT open discovery (→
`opportunity-discovery`).

## Required Inputs

The watchlist (symbols, ≤10 for standard budget; >10 → say the budget
grows and offer to split). If no list is in context, ask ONE compact
question: "Which symbols, and since when?" Default comparison window:
since the last check-in if known, else 24h (weekdays) / since Friday's
close (Monday).

## Optional Inputs

Per-asset theses (unlocks the Thesis row), the last check-in date, entry
levels ("alert distance to my stop"), what counts as material for this
user (overrides the default test below).

## Lexfi MCP Calls

**Budget: 8–14 calls for ≤10 assets. Efficiency IS the design** — every
call must cover multiple assets unless triggered by materiality:

**Batch 1 — shared layer (5–7 calls, parallel, covers the WHOLE list):**

- `get_stock_quote` — comma-separated symbols: **ONE call for ALL
  equities/ETFs**, never per-symbol.
- `get_coin_markets` — **one page covers all crypto names** (per_page
  sized to reach the lowest-ranked holding); `get_coin_market_chart` only
  for a coin the page cannot reach.
- `get_daily_fx_pair` per FX pair (the one per-asset unavoidable; ≤2–3
  pairs typical).
- Crypto positioning, **amortized — one call each covers every coin on
  the list**: `get_funding_rates`, `get_open_interest`, `get_liquidations`
  (include only if ≥1 crypto name; all three only if ≥2 names or the
  user's theses are positioning-sensitive).
- Catalyst look-ahead: `get_cb_calendar`, or `get_economic_calendar` with
  a 1–2 day window (payload-bomb trap) — one shared call, mapped to
  affected assets afterward.

**Batch 2 — materiality-triggered depth (0–5 calls, parallel).**
**Materiality test — an asset earns a depth call only if:** |price move| >
2× its typical daily range (equities/FX) or >5% (crypto) since the window
start, OR the shared layer surfaced an asset-specific signal (funding sign
flip, liquidation spike, OI jump, calendar hit), OR the user flagged it.
Then ONE call for that asset: `get_stock_news` or `get_stocks_news_sentiment`
(equity), `get_crypto_news_sentiment` (`XXXUSD`) (crypto),
`get_forex_news_sentiment` or `get_ai_fx_ratio` (FX). Quiet assets get
ZERO per-asset calls — that is the design working, not a gap.

**Applicable traps (from playbook):** `get_stock_quote` symbol batching;
coin-markets stables/wrapped noise if reading breadth; open-interest
non-crypto perps filtered before claims; funding dirty symbol field (match
on name, per-interval rates, outliers/sign-flips are the signal);
`get_daily_fx_pair` changePercent already percent + weekend rows;
crypto-sentiment proportions not counts; economic-calendar 1–2 day windows.

## Workflow

1. **Resolve list + window + theses** from context; one question max.
2. **Batch 1** → compute per-asset price delta vs window and vs the
   asset's own typical range (a 1% BTC day is →, a 1% EURUSD day is ↑).
3. **Apply the materiality test** → name which assets earned depth and
   why; fire batch 2 for those only.
4. **Score each asset's rows** — every non-price row exists only if there
   is NEW evidence in the window; otherwise it is omitted, not padded:
   - Price ↑/↓/→ (vs own range, with the number)
   - Information Improving/Deteriorating/Stable (news/sentiment delta —
     trend vs window, never one day's counts as a trend)
   - Sentiment (only for depth-call assets)
   - Fundamentals (only if new data: earnings, filings, metric prints)
   - Macro (only if a shared-layer macro/positioning signal touches it)
   - Catalysts upcoming (from the shared calendar call)
   - Thesis Strengthening/Weakening/Unchanged — **only when the user has
     a stated thesis; otherwise the row is omitted entirely.** Judged
     against the thesis's own evidence and invalidation, labeled
     [interpretation].
5. **Deliver delta-first**: material changes on top, quiet assets in one
   compressed line each.

## Output Format

```text
WATCHLIST UPDATE — <date> (window: since <date/time>)
Material changes: <n> of <N> assets | Depth calls spent on: <symbols or "none">

▲ <SYMBOL> — <class>                         Price: <↑/↓/→> <Δ%> (vs typical <x%>)
  Information: <Improving/Deteriorating/Stable> — <the new item, as-of>
  Sentiment:   <read + evidence>            (only if depth call ran)
  Fundamentals: <new datum>                 (only if new data)
  Macro:       <shared-layer signal touching this asset>
  Catalysts:   <dated upcoming event, or omit>
  Thesis:      <Strengthening/Weakening/Unchanged> — <why> [interpretation]
  Why it was material: <which trigger fired>

▲ <next material asset…>

— Quiet (no material change, no new information):
<SYMBOL> <→ Δ%> · <SYMBOL> <→ Δ%> · <SYMBOL> <→ Δ%>

Watch next: <1–3 dated items across the list>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Zero static facts: banned anywhere in the output — company descriptions,
  what a token does, thesis restatement, or any fact deliverable
  identically yesterday.
- Exactly one `get_stock_quote` call and at most one `get_coin_markets`
  page regardless of list size; per-symbol quote calls are a design
  failure.
- The materiality test is stated in the output ("Why it was material") —
  every depth call is attributable to a named trigger.
- Quiet assets appear in the compressed line — silence on a symbol is
  never ambiguous between "unchanged" and "forgotten".
- Thesis row only for assets with a user-stated thesis; never invent a
  thesis to have something to grade.
- Output ≤ ~10 lines per material asset, one line per quiet asset.

## Failure Handling

- Shared-layer call fails → the corresponding row degrades for ALL assets
  evenly (e.g. no positioning rows); note it in Sources, continue.
- One symbol unresolved in the batch → per playbook symbol rules; if
  still failing, list it under Quiet as "Data unavailable: <symbol>"
  rather than dropping it.
- Plan-gated tools (Pro Max: transcripts, quant models) absent → the
  Fundamentals row degrades to surprises/news-derived evidence; say so
  once in Sources, not per asset.
- Comparison window unknowable (no last check-in) → state the assumed
  window in the header so deltas are interpretable.
- >10 assets → warn the budget scales, propose priority split; never
  silently exceed budget.

## Example Prompts

- "What's changed in my watchlist?"
- "Update me on my list since yesterday."
- "Morning check: NVDA, MSFT, BTC, SOL, EURUSD."
- "Anything new on my names? Thesis on NVDA is AI capex acceleration."
- "Did anything material happen on my positions over the weekend?"
