---
name: thesis-builder
description: Use when a trader wants research formalized into a thesis — "build my thesis on X", "write up my thesis", "turn this research into a thesis", "formalize this idea" — or wants scenario framing — "bull bear case for X", "build scenarios", "bull base bear". Also when discovery or deep-dive output is already in context and the trader says "make this a thesis". Not for attacking an existing thesis (thesis-challenger) or sizing a trade (risk-reward-analysis).
license: MIT
---

# Thesis Builder

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Convert research already in context into a falsifiable thesis under a fixed
contract — direction, horizon, evidence, catalysts, counter-thesis, risks,
invalidation, confidence — so the idea can be challenged, sized, and
monitored. The contract is the product: **this skill refuses to emit a
thesis that has no invalidation conditions.**

## Supported Assets

US equities & ETFs, major crypto assets, G10 + liquid EM FX pairs. Any
single asset with a stated or inferable direction. Not for portfolios or
multi-asset baskets — one thesis per asset; run the skill per asset if
asked for several.

## Modes

| Mode | Trigger phrasing | Output shape |
|---|---|---|
| **Standard** (default) | "build/write my thesis" | Full thesis contract |
| **Scenario** | "bull bear case", "build scenarios", "bull base bear" | Contract + bull/base/bear scenario matrix |

## Required Inputs

An asset, and research to build from — either prior skill output in context
(discovery entry, deep-dive dossier, conversation research) or the trader's
own stated evidence. Direction and horizon are inferred from the research;
if direction is genuinely ambiguous, ask ONE compact question. Default
horizon: multi-week, stated explicitly in the output.

## Optional Inputs

Horizon override, conviction the trader already holds (tested, not
adopted), existing position (colors the invalidation framing), specific
catalysts the trader is anchored on.

## Lexfi MCP Calls

**Budget: gap-fill only, ≤4 calls. Zero calls is the expected case** when a
deep-dive or discovery output is in context. This skill synthesizes; it
does not re-research. If no research exists in context at all, say so and
offer `asset-deep-dive` first rather than improvising a thin evidence base.

Gap-fill categories — call only what is genuinely missing, one parallel
batch:

- **Price anchor** (no current level in context, or context is stale):
  `get_stock_quote` / `get_coin_market_chart` (CoinGecko id, `days: "30"`) /
  `get_daily_fx_pair` (1-month window).
- **Catalyst dating** (thesis leans on an undated event): `get_cb_calendar`;
  `get_economic_calendar` only in a 1–2 day window; equity report cadence
  via `get_earnings_calls_by_ticker`.
- **Missing counter-evidence family** (nothing in context speaks against the
  idea — suspicious): one class-appropriate call — equities
  `get_stocks_news_sentiment` or `get_insider_trades`; crypto
  `get_funding_rates` or `get_crypto_news_sentiment`; FX
  `get_rate_probabilities` or `get_ai_fx_ratio`.

**Skip conditions:** evidence already in context is never re-fetched; no
calls for conceptual restatement of research the trader just pasted.

**Applicable traps (playbook):** economic-calendar payload bomb;
`get_daily_fx_pair` changePercent-already-percent and weekend rows;
`get_coin_market_chart` coin_id + string-enum days; `get_funding_rates`
dirty symbol names; `get_analyst_estimates` far-future-first ordering;
`get_rate_probabilities` snapshot-only (no "pricing has shifted" claims).

## Workflow

1. **Inventory the evidence** in context onto the ladder: facts (with as-of
   dates), signals, interpretations. Note which of the 8 signal families
   are represented, which oppose, which are unknown.
2. **Gap-fill** (≤4 calls, one batch) only where step 1 exposed a hole that
   blocks the contract — usually price anchor, catalyst date, or an absent
   counter-evidence family.
3. **Draft the mechanism**: one causal sentence explaining *why* the asset
   should move — no mechanism, no thesis. Flow-driven is a valid mechanism
   if named as such.
4. **Write the invalidation first.** Derive observable kill conditions from
   the evidence (level, dated event outcome, signal reversal). If no
   falsifiable invalidation can be written, STOP: deliver a pre-thesis
   diagnosis (what's missing, which calls or research would supply it)
   instead of a thesis.
5. **Build the counter-thesis** — the strongest opposing case a competent
   bear/bull would make, from the opposing evidence found in step 1. Never
   a strawman; if no opposing evidence exists in context, say the
   counter-thesis is untested and recommend `thesis-challenger`.
6. **Set confidence** by evidence-discipline rules: High needs ≥3
   independent aligned families, no unresolved contradiction, and a clear
   catalyst or mechanism. State the one thing limiting confidence.
7. **Scenario mode only:** define bull/base/bear as divergent paths of the
   same mechanism, each with its own trigger conditions and rough range
   (anchored to realized moves in context, labeled [interpretation]).
   Probabilities are judgment calls — label them and make them sum to ~100%.

## Output Format

```text
THESIS — <SYMBOL> <name>                              <date>
Asset: <symbol, class>       Direction: <Long/Short/Neutral-watch>
Time horizon: <explicit window>

Core Thesis: <one falsifiable sentence: direction + mechanism + horizon>

Supporting Evidence:
• <signal family>: <specific evidence, as-of date, source skill/call>
• <signal family>: <specific evidence>
• <signal family>: <specific evidence>

Catalysts:
• <dated event or mechanism — "none identified" is a valid entry>

Counter-Thesis: <the strongest opposing case, 2–3 lines, from real
opposing evidence — or "untested; run thesis-challenger">

Key Risks: <2–3, asset-appropriate per evidence-discipline>

Invalidation Conditions (thesis is DEAD if):
• <observable condition — level, event outcome, or signal reversal>
• <observable condition>

What would change my view?: <the single most decision-relevant datum
not yet observable, and when/where it arrives>

Confidence: <Low/Med/High> — <families aligned n/8; the one limiter>

[Scenario mode adds:]
SCENARIO MATRIX
Scenario | Trigger conditions | Path/range [interpretation] | Est. odds
Bull     | <what has to happen> | <range vs current>         | <~%>
Base     | <...>                | <...>                      | <~%>
Bear     | <...>                | <...>                      | <~%>
Base-case skew: <which tail the evidence currently favors, one line>

Sources & data as-of: <in-context research used; gap-fill calls; gaps>
Research, not a recommendation.
```

## Quality Controls

- **No invalidation, no thesis** — the refusal in workflow step 4 is
  non-negotiable; a pre-thesis diagnosis is the only alternative output.
- Every Supporting Evidence bullet names its signal family and traces to a
  specific call or in-context source — no bullet restatable as "setup looks
  good".
- Certainty language ban: no "will", "guaranteed", "inevitable"; ranges and
  conditionals only. Scenario odds always labeled as judgment.
- Counter-thesis must cite real opposing evidence or be flagged "untested"
  — never a token objection.
- Confidence High is impossible with an unresolved opposing family or <3
  aligned independent families; a strong opposing signal caps it at Medium.
- Output ≤ ~45 lines standard, ~60 in scenario mode.

## Failure Handling

- **No research in context:** don't fake one from ≤4 calls — name the gap,
  offer `asset-deep-dive`, or (if the trader insists) deliver a clearly
  labeled "thin-evidence thesis" capped at Confidence: Low.
- Gap-fill call errors → keep building from context; list the hole in
  Sources and reflect it in confidence.
- Plan-gated tools absent (transcripts, quant models — Pro Max) →
  earnings/management evidence degrades to `get_earnings_surprises` +
  news-derived tone; say so in Sources.
- Symbol resolution failure → playbook fallbacks (`TICKER:CC`, 6-char FX
  pair, CoinGecko id); if still unresolved, ask rather than guess.
- Stale in-context research (>1 week old facts) → refresh the price anchor
  within budget and date-stamp every reused fact.

## Example Prompts

- "Build my thesis on NVDA from that deep dive."
- "Turn this research into a formal thesis with invalidation levels."
- "Write up the bull bear case for ETH over the next quarter."
- "Build scenarios for EURUSD into the ECB meeting."
- "Formalize my long-gold idea — what would kill it?"
