---
name: earnings-analysis
description: Use when a trader asks anything earnings-specific about a company — "how were NVDA's earnings?", "analyze AAPL's latest quarter", "did they beat or miss?", "what did management say on the call?", "has their tone changed?", "how did the stock react to the report?", "what's the setup into next quarter?". Also for beat/miss track records and guidance-versus-consensus questions. General "research this stock" requests belong to asset-deep-dive.
license: MIT
---

# Earnings Analysis

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

A complete earnings read for one company: beat/miss record, what management
actually said (and how the tone moved versus the prior call), how the market
priced the report, and the consensus bar for next quarter. Encodes the two
call plans users get wrong alone: the two-step transcript sequence and the
reaction-window price pull.

## Supported Assets

US-listed equities with earnings coverage. Not ETFs (no earnings calls), not
crypto or FX. Foreign listings: try `TICKER:CC`, warn that transcript
coverage thins outside the US.

## Required Inputs

The ticker. Default scope: the latest reported quarter, with the prior call
used for tone comparison and the last 4 quarters for the beat/miss record.
A specific past quarter ("their Q1 print") narrows the scope to that report.

## Optional Inputs

Existing position, the trader's specific worry (margins, guidance, a
segment), horizon into the next report.

## Lexfi MCP Calls

**Budget: 6–10 calls, hard cap 10.**

- **Batch 1 (parallel, 4 calls):** `get_earnings_calls_by_ticker` (transcript
  list + report dates), `get_earnings_surprises` (beat/miss history),
  `get_analyst_estimates` (**raise `limit`** — rows are ordered
  far-future-first and the near quarters you need sit deep in the list),
  `get_stock_news` (post-report narrative).
- **TRUE SEQUENCE — transcripts (2 calls, only after batch 1):**
  `get_earnings_calls_by_ticker` output supplies `transcriptId`s → then
  `get_earnings_call_insights` for the latest call AND the prior call (these
  two insight calls run parallel with each other). `tables:["ais","metrics"]`
  by default; `includeTranscript=true` (50–200 KB) only when the user asks
  for verbatim quotes. Never guess a transcriptId.
- **Reaction window (1 call):** `get_historical_prices` with `from` ≈ 3
  trading days before the report date (from batch 1) and `to` ≈ 5 trading
  days after. **The market reaction is NEVER today's quote** — unless the
  report was within the past week, in which case `get_stock_quote` is the
  reaction and replaces this call.
- **Conditional (0–2 calls):** `get_stocks_news_sentiment` (symbol) when
  post-report tone trend matters; `get_key_metrics` when the print moved the
  valuation debate.

**Applicable traps (from playbook):** `get_earnings_call_insights` requires
a real `transcriptId` (two-step, always); `get_analyst_estimates`
far-future-first ordering; reaction ≠ today's quote; transcripts and
insights are plan-gated (Pro Max).

## Workflow

1. **Scope**: which report, which comparison call, position context.
2. **Batch 1** → report dates, beat/miss table, near-quarter consensus rows
   (walk past the far-future rows), post-report headlines.
3. **Transcript sequence** → latest + prior call insights. Extract: guidance
   language, named risks, management confidence markers, recurring topics
   that appeared/disappeared between calls. The tone SHIFT is the signal —
   one call's tone alone is weak evidence.
4. **Reaction** → price path across the report: gap, follow-through or
   fade, versus the size of the surprise. A big beat + faded pop is a
   signal; label the reading [interpretation].
5. **Next-quarter setup** → consensus bar from the near-quarter estimate
   rows + whether management guided above/below it; note the next report's
   approximate date from call cadence (label as inferred).
6. **Deliver** — ladder-structured, thesis paired with invalidation.

## Output Format

```text
EARNINGS READ — <TICKER> — <quarter> (reported <date>) — <date>
Verdict: <2 lines — print quality + how the market took it>

Beat/miss record (last 4):
| Quarter | EPS est | EPS act | Surprise | 
|---|---|---|---|

Market reaction: <gap %, 5-day follow-through, vs surprise size, as-of>
Management tone: <latest vs prior call — what changed; quote only if pulled>
Guidance vs consensus: <above/in-line/below + the near-quarter bar>
Next-quarter setup: <consensus EPS/rev bar; approx next report date [inferred]>

FACT:            <numbered — call results only, with as-of dates>
SIGNAL:          <numbered — shifts/divergences, each citing its facts>
INTERPRETATION:  <numbered — labeled, each citing its signals>

Thesis (working): <one falsifiable line + horizon> [interpretation]
Invalidation: <observable condition>
Key risks: <2–3 — guidance, margin, macro-sensitivity as applicable>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Reaction claims cite the report-window price path, never the current
  quote, unless the report is <1 week old (then say the reaction is live).
- Tone claims always compare two calls; a single-call tone read is labeled
  "no prior-call baseline".
- Estimate figures state which quarter row they came from — a far-future
  row misread as next quarter is the banned failure mode.
- Beat/miss table covers 4 quarters or states why fewer exist.
- No verbatim "quotes" unless `includeTranscript=true` was actually run.

## Failure Handling

- **Transcripts plan-gated (Pro Max) or errored** → skip both insight
  calls; deliver surprises + estimates + reaction + news, with
  "Management tone: unavailable on this plan" in the output and Sources.
  Never reconstruct call content from model knowledge.
- No transcript list for the ticker → coverage gap; deliver the
  numbers-only read and say so.
- Report date unresolvable → no reaction window; use `get_stock_news`
  dating as a weak proxy, labeled as such.
- Empty estimates → next-quarter setup becomes "no consensus available".

## Example Prompts

- "How were NVDA's latest earnings?"
- "Did AAPL beat? How did the stock react?"
- "What did MSFT management say on the call, and has their tone changed?"
- "Analyze COST's earnings — I'm worried about margins."
- "What's the setup going into AMD's next report?"
