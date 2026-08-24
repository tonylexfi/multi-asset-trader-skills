---
name: fx-macro-analysis
description: Use when a trader wants a macro read on a currency pair or a currency matchup — "analyze EURUSD", "macro dossier on USDJPY", "GBP vs USD — which way is the divergence pointing?", "is the Fed/ECB divergence tradeable?", "bull and bear case for the yen", "should I be long or short this pair?". Owns two-sided policy/data/sentiment dossiers per pair. FX pair discovery and quick "why did EURUSD move" questions belong elsewhere.
license: MIT
---

# FX Macro Analysis

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

A currency pair is two economies in a tug-of-war: this skill builds the same
evidence stack for BOTH sides, lines the stacks up in one divergence table,
and nets them into a thesis direction. The two-sided discipline is the
product — a one-sided FX read ("the Fed is hawkish, so long USD") is the
failure mode this skill exists to prevent.

## Supported Assets

G10 pairs fully (both CBs and both economies covered). Liquid EM pairs with
a degraded EM leg (weekly-series data replaces CB tone — `get_cb_insights`
covers only `fed`/`ecb`/`boe`/`boj`). Crosses welcome (`EURGBP`, `AUDJPY`).
One pair per run.

## Required Inputs

The pair (6-char form `EURUSD`) or two currencies. A single currency
("dossier on the yen") defaults to its USD pair — say so. Defaults: 90-day
price window, multi-week horizon, latest policy snapshot.

## Optional Inputs

Existing position and side, horizon, the hinge question ("is the BoJ hike
priced?"), risk appetite.

## Lexfi MCP Calls

**Budget: 8–12 calls, hard cap 12** — above the single-asset 6–10 because a
pair is two economies, each owed its own evidence stack; the overage is the
second stack, nothing else.

- **Batch 1 — pair + policy + sentiment (parallel, 6–7 calls):**
  `get_daily_fx_pair` (symbol `EURUSD` form, 90-day window);
  `get_rate_probabilities` ×2 (each CB's short code);
  `get_ai_fx_ratio` ×2 (each currency); `get_forex_news_sentiment`; add
  `get_daily_dxy_index` (2-week window) when USD is one leg.
- **Batch 2 — economy fundamentals + tone (parallel, 2–4 calls):**
  `get_cb_insights` ×0–2 (only for `fed`/`ecb`/`boe`/`boj`; skip others);
  `get_country_metrics` or `get_macro_forecasts` per economy for
  growth/inflation momentum.
- **EM leg (TRUE SEQUENCE, replaces that side's batch-2 calls):**
  `get_macro_weekly_series_catalog` → `get_macro_weekly_snapshot` (exact
  sheet names from the catalog — never guessed); `get_daily_fx_local_vs_usd`
  if the pair tool lacks the pair.
- **Conditional (0–1):** `get_economic_calendar` (1–2 day window ONLY) when
  the thesis hinges on an imminent data print; `get_cb_calendar` when it
  hinges on a meeting date.

**Applicable traps (from playbook):** `get_daily_fx_pair` `changePercent`
already in percent + weekend/holiday rows excluded from range/vol claims;
`get_ai_fx_ratio` slow-moving with stale-day repeats — trend via
`diff_AI_FX_ratio` over weeks, never day-over-day; `get_rate_probabilities`
snapshot-only — never claim "pricing has shifted" from one call;
`get_cb_insights` four bankIds only, decimal-string numerics, ignore "quote
shorts" clip rows; weekly-snapshot catalog-first; economic-calendar payload
bomb.

## Workflow

1. **Parse** the pair → base/quote currencies, their CBs, G10-vs-EM path
   per side.
2. **Batch 1** → price regime (trend, range, weekday-only volatility),
   market-implied policy path per CB, news-derived strength trend per
   currency (weeks, not days), FX news tone.
3. **Batch 2 / EM sequence** → CB tone (hawk/dove trend from `summary` and
   full conferences only) and growth/inflation momentum per economy.
4. **Build the divergence table** — every dimension scored for BOTH sides
   before any edge is assigned. A dimension with data for only one side
   gets edge "n/a (one-sided data)", never a default win.
5. **Net the edges** into a thesis direction: policy path and CB tone weigh
   most, data momentum next, sentiment least. A 4–1 table is a directional
   thesis; 3–2 with the policy rows split is "no clear edge" — say so
   rather than manufacturing a lean. Conflicts carried into risks per
   evidence-discipline.
6. **Check the price**: does the pair already reflect the edge? An edge the
   market has fully run with is a weaker entry than a fresh divergence —
   label the judgment [interpretation].
7. **Deliver** — table, net direction, thesis with invalidation.

## Output Format

```text
FX MACRO DOSSIER — <PAIR> — <date>
Verdict: <2 lines — net direction (or "no edge") + the hinge factor>

Price regime: <trend, range, position in range, weekday vol, as-of>

Divergence table (edge = which CURRENCY the row favors):
| Dimension            | <BASE / CB>       | <QUOTE / CB>      | Edge |
|---|---|---|---|
| Policy path (mkt-implied) | <next meetings>  | <next meetings>  | <ccy/split> |
| CB tone (trend)      | <hawk/dove drift> | <hawk/dove drift> | <ccy/n-a> |
| Growth momentum      | <direction>       | <direction>       | <ccy> |
| Inflation momentum   | <direction>       | <direction>       | <ccy> |
| News-derived strength (wks) | <trend>    | <trend>           | <ccy> |
| News tone            | <tone>            | <tone>            | <ccy> |

Net: <N–M for <currency>> → <direction on the pair, or "no clear edge">
Already priced? <price-vs-edge read> [interpretation]

FACT:            <numbered — call results only, with as-of dates>
SIGNAL:          <numbered — divergences/trends, each citing its facts>
INTERPRETATION:  <numbered — labeled, each citing its signals>

Thesis (working): <direction + horizon + mechanism, falsifiable> [interpretation]
Invalidation: <observable condition — a repricing, a data print, a CB shift>
Key risks: <2–3 — CB surprise, data surprise, positioning, political as apply>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Every table row is filled for both sides or its edge is "n/a" — no row
  may award an edge from one-sided evidence.
- Policy-path rows come from the current `get_rate_probabilities` snapshot
  and are never phrased as a shift versus the past.
- AI-FX-ratio rows cite a multi-week trend; any day-over-day strength claim
  is a rewrite trigger.
- Range/volatility statements exclude weekend/holiday rows and say so once.
- The net score's arithmetic is visible in the table — the thesis direction
  must be reproducible from the printed edges.
- "No clear edge" is a first-class verdict, delivered with the same table.

## Failure Handling

- CB outside `fed`/`ecb`/`boe`/`boj` → CB-tone row reads "n/a (bank not
  covered)"; policy path may still come from `get_rate_probabilities` if
  that bank's code resolves, else n/a.
- EM weekly catalog/snapshot fails → that side's data-momentum rows go n/a
  and conviction caps at Medium.
- Plan-gated CB transcripts (Pro Max) absent → tone rows degrade to the
  non-verbatim `get_cb_insights` indices; if those are also gated, tone
  rows are n/a and the output says which plan unlocks them.
- Pair symbol unresolved → retry the 6-char form, then the local-vs-USD
  tool; if both fail, deliver the two one-sided stacks without price
  context and say so.
- Both policy rows unavailable → the dossier is not supportable (policy is
  the spine); say so instead of delivering a sentiment-only thesis.

## Example Prompts

- "Analyze EURUSD — which way does the macro point?"
- "Macro dossier on USDJPY."
- "Is the Fed/ECB divergence still tradeable?"
- "GBP vs USD: build me the two-sided case."
- "Bull and bear case for the yen over the next quarter."
