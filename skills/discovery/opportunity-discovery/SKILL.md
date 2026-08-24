---
name: opportunity-discovery
description: Use when a trader asks for interesting opportunities, ideas, or setups without naming a specific asset — "find me opportunities", "what's interesting right now", "where are the setups today", "what's accelerating", "find emerging themes" — across stocks, crypto, FX, or all three. Also for momentum-focused or theme-focused scans.
license: MIT
---

# Opportunity Discovery

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Turn "find me opportunities" into a ranked, evidence-backed candidate list
where every entry explains *why it surfaced* as named converging signals —
not an opaque score. This is the entry point of the product loop; its output
feeds `asset-deep-dive` and `thesis-builder`.

## Supported Assets

US equities & ETFs, major crypto assets, G10 + liquid EM FX pairs.
Cross-asset by default. If the user scopes to one class ("find stocks…"),
hand off to `stock-discovery` / `crypto-discovery` / `fx-discovery` — this
skill owns the cross-asset and mixed cases.

## Modes

| Mode | Trigger phrasing | Signal weighting |
|---|---|---|
| **General** (default) | "find opportunities" | balanced convergence |
| **Momentum** | "what's accelerating / strongest momentum" | price + information momentum; require both accelerating |
| **Theme** | "emerging themes before they're obvious" | clustered signals across ≥3 related assets; name the theme, not just tickers |

## Required Inputs

None. Defaults: all three asset classes, 5 opportunities (10 on request),
multi-week horizon, no direction constraint.

## Optional Inputs

Criteria ("benefiting from falling rates"), count, horizon, classes to
include/exclude, risk appetite, assets already held (exclude or flag).

## Lexfi MCP Calls

**Budget: 12–18 calls, hard cap 18.** Three funnel stages; never skip stage
order, never deep-dive an asset that hasn't passed stage 2.

**Stage 1 — Broad layer (one parallel batch, 6 calls, whole-market):**
`get_market_overview`, `get_sector_performance`, `get_market_movers`,
`get_crypto_global_metrics`, `get_coin_markets` (per_page 50),
`get_daily_dxy_index` (2-week window).

**Stage 2 — Signal layer (one parallel batch, 4–7 calls, cross-universe
snapshots — each covers many assets in one call):**
`get_funding_rates`, `get_open_interest`, `get_liquidations` (crypto
positioning, filter non-crypto perps), `get_stocks_news_sentiment`
(aggregate), `get_crypto_news_sentiment` (aggregate), `get_cnn_fear_greed_index`
+ `get_fear_greed_index`; add `get_ai_fx_ratio` for USD + 1–2 currencies
when FX is in scope.

**Stage 3 — Depth layer (shortlist of 3–6 only, 1–2 calls each, batched):**
per candidate class — equities: `get_stock_news` (symbol filter) or
`get_stocks_news_sentiment` (symbol); crypto: `get_crypto_news_sentiment`
(symbol) or `get_whale_alerts`/`get_onchain_flows` (traps apply); FX:
`get_rate_probabilities` or `get_daily_fx_pair`. Calendar check
(`get_cb_calendar`, or `get_economic_calendar` 1-day window) only when a
candidate's case leans on a dated catalyst.

**Applicable traps (from playbook, non-negotiable):** coin-markets
stable/wrapped filtering; open-interest non-crypto symbols; funding dirty
names; whale custody rotations; calendar payload bomb; both fear/greed
tools correctly assigned.

## Workflow

1. **Parse criteria** → mode, classes, count, horizon. One clarifying
   question max, only if the request is contradictory.
2. **Stage 1 calls** → build the market picture: leadership, laggards,
   breadth, dominance shifts, dollar direction.
3. **Nominate candidates (~10–20)** from stage 1: unusual movers, sector
   leaders/laggards, dominance rotation, and — mattering as much —
   *non-movers* in moving sectors (divergence seeds).
4. **Stage 2 calls** → score each candidate on the signal families:

```text
PRICE/MARKET ACTION + FUNDAMENTALS + NEWS/SENTIMENT + EARNINGS/MGMT
+ POSITIONING/FLOWS + MACRO + CATALYSTS + ALT DATA  →  OPPORTUNITY
```

   A family counts only when its evidence is current and independent
   (evidence-discipline rules). Record for each candidate: families
   aligned, families opposed, families unknown.
5. **Rank** by (a) count of independent aligned families, (b) presence of
   an identifiable catalyst or mechanism, (c) absence of a strong opposing
   family. A strong opposing family caps conviction at Medium.
6. **Stage 3 calls** on the top 3–6 → confirm the story, find the catalyst,
   name the risks, write the invalidation.
7. **Deliver** — every entry must answer: why now, what converges, what
   breaks it.

## Output Format

```text
MULTI-ASSET OPPORTUNITY SCAN — <date>
Objective: <restated criteria>          Mode: <general/momentum/theme>
Market context: <2 lines from stage 1>

1. <SYMBOL> — <name>            <class> · Conviction: <Low/Med/High>
   Why it surfaced:
   • <signal family>: <specific evidence, as-of> 
   • <signal family>: <specific evidence>
   • <signal family>: <specific evidence>
   Opposing: <the strongest counter-signal, or "none found">
   Catalyst: <dated event or mechanism, or "none — flow-driven">
   Thesis (working): <one falsifiable line> [interpretation]
   Invalidation: <observable condition>
   Key risks: <2–3, asset-appropriate>

2. …

Not surfaced but considered: <2–3 near-misses + the family that failed>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Every "why surfaced" bullet names its signal family AND its evidence — no
  bullet may be restatable as "it looks good".
- ≥2 asset classes represented in a cross-asset scan unless the data
  genuinely concentrates opportunity in one (say so if it does).
- "Not surfaced but considered" is mandatory — it proves a funnel ran.
- No candidate promoted from stage 1 straight to the output.
- Conviction High requires ≥3 aligned independent families + catalyst +
  no strong opposing family.
- Output ≤ ~120 lines for 5 candidates; depth belongs in `asset-deep-dive`.

## Failure Handling

- A stage-2 tool errors → drop that family for all candidates (level
  field), note it in Sources, continue.
- Plan-gated tools absent (transcripts, quant models) → the
  EARNINGS/MGMT and ALT DATA families degrade to news-derived evidence;
  say so.
- Fewer than 3 candidates with ≥2 aligned families → report "no strong
  convergence today" honestly with the 1–2 best partial setups, rather
  than inflating weak candidates.

## Example Prompts

- "Find 10 interesting opportunities across US stocks, crypto and FX right now."
- "What's showing the strongest convergence of macro and market signals?"
- "Find opportunities that could benefit from a falling-rate environment."
- "What's accelerating right now?" (momentum mode)
- "Any emerging themes before they become obvious?" (theme mode)
