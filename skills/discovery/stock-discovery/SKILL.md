---
name: stock-discovery
description: Use when a trader asks for stock or ETF ideas by name of class — "find me stocks that…", "screen for equities with improving sentiment", "which stocks have insiders buying", "give me ideas in semis", "find quality names getting cheaper", "any ETFs worth a look". Equity-scoped requests only; mixed or open-ended cross-asset requests trigger opportunity-discovery instead.
license: MIT
---

# Stock Discovery

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Turn a criteria-driven "find stocks…" request into a ranked equity shortlist
where every candidate explains *why it surfaced* as named signals matched to
the stated criteria — not a screener dump. Output feeds `asset-deep-dive`
and `thesis-builder`.

## Supported Assets

US-listed equities and ETFs — Lexfi coverage is strongest there, and the
output says so. Non-US listings: attempt `TICKER:CC` suffix, flag reduced
coverage. NOT supported here: crypto (`crypto-discovery`), FX
(`fx-discovery`), cross-asset scans (`opportunity-discovery`).

## Criteria Archetypes

Map the user's criteria to an archetype; it decides stage-3 depth calls.

| Archetype | Trigger phrasing | Depth emphasis |
|---|---|---|
| **Sentiment-vs-price** | "sentiment improving but stock hasn't moved" | per-symbol sentiment + price |
| **Quality-improving** | "fundamentals getting better", "quality cheap" | key metrics + earnings surprises |
| **Insider conviction** | "insiders buying", "smart money" | insider trades + superinvestor activity |
| **Catalyst-rich** | "stocks with something coming up" | news + earnings cadence |
| **Rotation** | "sector leadership", "what's benefiting from rotation" | sector performance + movers |

No clean archetype → balanced convergence across families (default).

## Required Inputs

None. Defaults: US universe seeded from movers + sector leadership, 5
candidates (10 on request), multi-week horizon, long-biased unless the user
asks for shorts.

## Optional Inputs

Sectors to include/exclude, market-cap floor, direction, count, horizon,
positions already held (exclude or flag), risk appetite.

## Lexfi MCP Calls

**Budget: 8–12 calls, hard cap 12.** Three funnel stages; sentiment and
fundamentals are per-candidate calls, so they run ONLY after the breadth
filter — never against the whole universe.

**Stage 1 — Breadth (one parallel batch, 3–4 calls, whole-market):**
`get_market_movers` (type per requested direction), `get_sector_performance`,
`get_stocks_news_sentiment` (aggregate, no symbol), `get_cnn_fear_greed_index`
(the equities one — never `get_fear_greed_index`).

**Stage 2 — Candidate check (1–2 calls for ~10–15 candidates):**
`get_stock_quote` with ALL candidate tickers comma-separated — one call for
the whole set; add `get_stocks_news_sentiment` (symbol) only for candidates
whose case is sentiment-led.

**Stage 3 — Shortlist depth (3–5 names, 1–2 calls each, batched in
parallel):** by archetype — `get_key_metrics`, `get_earnings_surprises`,
`get_insider_trades`, `get_stock_news` (symbol), `get_analyst_estimates`
(raise `limit`; far-future-first ordering trap). `get_etf_holdings` only when
an ETF candidate's case depends on what's inside it.

**Applicable traps (playbook, non-negotiable):** CNN vs crypto fear/greed
assignment; `get_analyst_estimates` ordering; quote batching (one call, never
per-ticker); earnings transcript flow is two-step AND plan-gated — this skill
does not call it by default.

## Workflow

1. **Parse criteria** → archetype, sector scope, direction, count. One
   compact clarifying question max, only if criteria are contradictory.
2. **Stage 1 batch** → market and sector context; note which sectors lead,
   lag, and where breadth diverges from index moves.
3. **Nominate ~10–15 candidates**: movers matching criteria, leaders/laggards
   in relevant sectors, and non-movers in moving sectors when the archetype
   is sentiment-vs-price. Every nomination cites the stage-1 evidence that
   put it in.
4. **Stage 2 batch** → live quotes for all candidates in one call; drop
   names whose price action already contradicts the criteria (materiality
   test: a candidate advances only if ≥1 signal family concretely matches
   the stated criteria).
5. **Stage 3 batch on the top 3–5** → archetype depth calls; score signal
   families aligned / opposed / unknown per evidence-discipline.
6. **Rank** by aligned independent families, then catalyst presence, then
   absence of a strong opposing family (a strong opposing family caps
   conviction at Medium).
7. **Deliver** — every entry answers: why it matches the criteria, what
   converges, what breaks it.

## Output Format

```text
STOCK DISCOVERY SCAN — <date>
Criteria: <restated>            Archetype: <name>    Universe: US equities/ETFs
Market context: <1–2 lines: sector leadership, equity fear/greed, breadth>

1. <TICKER> — <name>            <sector> · Conviction: <Low/Med/High>
   Why it surfaced:
   • <signal family>: <specific evidence, as-of date>
   • <signal family>: <specific evidence>
   • <signal family>: <specific evidence>
   Criteria fit: <one line tying evidence to the user's stated criteria>
   Opposing: <strongest counter-signal, or "none found">
   Catalyst: <dated event or mechanism, or "none — flow-driven">
   Thesis (working): <one falsifiable line> [interpretation]
   Invalidation: <observable condition>
   Key risks: <2–3 equity-appropriate: valuation / guidance / balance sheet / macro>

2. …

Not surfaced but considered: <2–3 near-misses + the family that failed>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Every candidate's "Criteria fit" line must reference Lexfi evidence, not a
  restatement of the company's reputation.
- No candidate reaches the output without passing the stage-2 quote check.
- Quotes are fetched in ONE batched call — two `get_stock_quote` calls in a
  scan is a design failure.
- Insider/superinvestor/congress evidence carries its disclosure date; lagged
  filings never presented as current conviction.
- Conviction High requires ≥3 aligned independent families + catalyst + no
  strong opposing family.
- Output ≤ ~110 lines for 5 candidates; depth belongs in `asset-deep-dive`.

## Failure Handling

- A stage-3 tool errors for one candidate → drop that family for that name,
  note it inline, keep the candidate if others align.
- Plan-gated tools (company transcripts / earnings-call insights — Pro Max
  only) → the EARNINGS/MGMT family degrades to `get_earnings_surprises` +
  `get_stock_news`; state the degradation in Sources.
- Ticker resolution failure → try `TICKER:CC`; if still unresolved, report
  "Data unavailable" for that name rather than substituting a lookalike.
- Fewer than 3 candidates matching the criteria → say so and deliver the
  best 1–2 partial matches with the failed families named — never pad.

## Example Prompts

- "Find me stocks where sentiment is improving but the price hasn't moved yet."
- "Screen for quality names that got cheaper this quarter."
- "Which stocks have meaningful insider buying right now?"
- "Give me 5 equity ideas in semiconductors, long side."
- "Any ETFs positioned for the current sector rotation?"
