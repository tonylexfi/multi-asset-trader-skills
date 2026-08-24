---
name: catalyst-discovery
description: Use when a trader asks what dated events are coming and what to do about them — "what catalysts are coming up", "any big events this week", "what's on the macro calendar", "upcoming CB meetings/IPOs/M&A", "what events could move my assets", "what is the market handicapping for the Fed". Event/calendar-first requests; open-ended idea requests without an event angle trigger opportunity-discovery.
license: MIT
---

# Catalyst Discovery

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Surface assets with dated upcoming catalysts and map each one:
catalyst → expected impact → direction skew → risk → timing. The trader gets
a tradeable event map, not a raw calendar dump. Output feeds
`risk-reward-analysis` and `thesis-builder`.

## Supported Assets

Cross-asset by design — macro events hit equities, crypto, and FX at once.
Equity-specific catalysts (earnings cadence, IPOs, M&A), CB meetings, and
macro data releases. NOT supported: undated "narrative" catalysts — those
belong to `opportunity-discovery` theme mode.

## Required Inputs

None. Defaults: next 4 trading days, major-economy events only (US, EA, UK,
JP, CN), top 5 catalysts, no asset filter.

## Optional Inputs

Horizon (up to ~6 trading days — the calendar trap caps reach), specific
assets or a watchlist to map events against, asset classes, event types to
include/exclude (macro data / CB / earnings / deals).

## Lexfi MCP Calls

**Budget: 8–12 calls, hard cap 12.** The design is governed by the
`get_economic_calendar` payload bomb: it is global and unfiltered, 7 days
≈ 140 KB. Hard rules: **1–2 day windows only, ≤3 iterations total**, scan
each payload for major-economy / high-importance events and discard the
rest immediately.

**Stage 1 — Calendar sweep (one parallel batch, 4–5 calls):**
`get_economic_calendar` (first 1–2 day window), `get_cb_calendar` (no
params), `get_ipo_calendar`, `get_mergers_acquisitions`. Additional
`get_economic_calendar` windows (max 2 more, sequential, only if the
requested horizon extends past the first window and the budget allows).

**Stage 2 — Handicapping (one parallel batch, 1–3 calls, only for
catalysts that survived triage):** `get_macro_prediction_markets` /
`get_stocks_prediction_markets` / `get_crypto_prediction_markets` — pick
per catalyst class; `get_rate_probabilities` (bank short code) when a CB
meeting made the map. All odds labeled market-implied, never forecasts.

**Stage 3 — Asset mapping (1–3 calls, only when the user named assets or a
setup needs confirmation):** `get_stock_quote` (ALL tickers in one
comma-separated call), `get_earnings_calls_by_ticker` (past call dates
establish reporting cadence — an inference, label it; never state an
unconfirmed earnings date as fact), `get_stock_news` (symbol) for
confirmed dates.

**Applicable traps (playbook, non-negotiable):** economic-calendar payload
bomb (windows + iteration cap above); `get_rate_probabilities` is a
snapshot with no history; `get_cb_insights`/transcripts are NOT called here
(that is `fx-macro-analysis` depth); quote batching; prediction-market odds
are market-implied probabilities.

## Workflow

1. **Parse scope** → horizon, assets/watchlist, event types. One compact
   clarifying question max.
2. **Stage 1 batch** → collect the raw event set within the iteration cap.
3. **Triage (the materiality test)** — keep an event only if (a)
   major-economy or high-importance, AND (b) it plausibly moves an asset
   class by a mechanism you can name in one line. Everything else is
   discarded silently; the map is a top-5, not a listing.
4. **Stage 2 batch** → attach market-implied odds to the kept catalysts
   that have a traded market; note "no market found" otherwise.
5. **Stage 3 calls** only where needed → map catalysts to the user's named
   assets or confirm a company-specific date.
6. **Build the map** — for each catalyst: date/time, affected assets,
   expected impact channel, direction skew (always `[interpretation]`,
   grounded in the odds or positioning evidence), and the two-sided risk
   (every catalyst can resolve either way).
7. **Deliver** — top 1–2 catalysts get a full setup with thesis +
   invalidation; the rest stay one-block entries.

## Output Format

```text
CATALYST MAP — <date>, horizon: <window>
Scope: <assets/classes>          Windows scanned: <dates, N calendar calls>

── <DATE> ──────────────────────────────────────────────
• <event> (<economy/ticker>, <time if known>)
  Affects: <assets/classes>   Impact channel: <one-line mechanism>
  Market-implied: <odds + venue, or "no traded market found">
  Skew: <direction + why> [interpretation]
  Two-sided risk: <what the adverse resolution does>

── <DATE> ──────────────────────────────────────────────
• …

TOP SETUPS (max 2)
1. <asset> into <event, date>          Conviction: <Low/Med>
   Why it surfaced: <named signals: odds asymmetry / positioning / cadence>
   Thesis (working): <one falsifiable line tied to the event> [interpretation]
   Invalidation: <observable condition — including the event resolving adverse>
   Key risks: <2–3, asset-appropriate>

Dropped in triage: <count + 1-line reason class, e.g. "minor-economy data">
Sources & data as-of: <tools used; windows covered; gaps: what was unavailable>
```

## Quality Controls

- Never more than 3 `get_economic_calendar` calls, never a window over 2
  days — an over-window call is a hard failure, re-plan.
- Every mapped catalyst has a DATE from a calendar tool; inferred earnings
  timing is labeled "estimated from cadence", never stated as scheduled.
- Every direction skew is `[interpretation]` and cites its grounding (odds,
  positioning, or pricing) — a skew with no evidence is a coin flip and
  must say so.
- Two-sided risk is mandatory per catalyst — event maps that only describe
  the favorable resolution are banned.
- Conviction on event setups caps at Medium — a dated binary inside the
  horizon is an unresolved opposing scenario by definition.
- Output ≤ ~90 lines; the map covers ≤5 catalysts + ≤2 setups.

## Failure Handling

- A calendar tool errors → deliver the map from the remaining sources and
  name the blind spot ("IPO calendar unavailable — deal-flow catalysts not
  covered").
- Prediction-market tools return nothing relevant → "no traded market
  found" per catalyst; skews then rest on remaining evidence or are
  reported as unhandicapped.
- Plan-gated tools (company transcripts, CB transcripts, quant models —
  Pro Max only) → cadence inference uses call listing dates only; CB tone
  context is skipped and noted. Never fill with model knowledge unlabeled.
- Horizon request beyond ~6 trading days → cover the first 6 within the
  iteration cap and state that the remainder was not scanned.

## Example Prompts

- "What catalysts are coming up this week that could move my positions?"
- "Any big macro events in the next few days?"
- "What's the market handicapping for the next Fed meeting?"
- "Upcoming IPOs or M&A worth watching?"
- "Map the next week's events against BTC, NVDA, and EURUSD."
