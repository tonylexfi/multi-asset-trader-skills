---
name: evidence-discipline
description: Use when any trader workflow presents data, signals, opportunities, theses, or risk — before writing any analytical output, when tempted to state a view as fact, when data is missing or stale, when signals conflict, or when an output needs a confidence or invalidation statement.
license: MIT
---

# Evidence Discipline

## Overview

Every analytical output in this library is built on one ladder. Each rung is a
different epistemic claim, and mixing rungs is how research becomes fiction:

```text
FACT            what a Lexfi call directly returned (with as-of date)
   ↓
SIGNAL          what changed, diverged, or is statistically notable
   ↓
INTERPRETATION  what the signal may mean (always labeled, always tentative)
   ↓
THESIS          a falsifiable directional hypothesis with a horizon
   ↓
INVALIDATION    the observable condition that kills the thesis
```

**Core principle: a thesis without an invalidation is a story, not research.**

## Labeling Rules

- Facts carry their source implicitly (the output's Sources line) and their
  as-of date when staleness matters.
- Interpretations are labeled inline: `[interpretation]` or "pattern
  consistent with…". Never present an interpretation with fact grammar.
- Discourse sources (X, Reddit, StockTwits, Telegram highlights) are always
  "what people are saying" — never evidence that the claim itself is true.
- Prediction-market odds are market-implied probabilities, not forecasts.
- Model knowledge used for context (sector norms, historical episodes) is
  labeled `[model knowledge — not Lexfi data]`.

## Anti-Hallucination (hard rules)

Never invent: prices, earnings dates, financial metrics, economic data,
analyst expectations, on-chain statistics, FX positioning, or MCP results.
If a needed datum is unavailable after the planned calls: write
**"Data unavailable: <what>"** and continue with what exists. An honest gap
outranks a plausible fill. If more than half the planned evidence is
unavailable, say the analysis is not supportable rather than delivering a
hollow one.

## Signal Standards

- A single day is rarely a signal. Trend claims compare windows (this week vs
  trailing month), not points.
- Proportions over raw counts when volume fluctuates (news counts, social).
- Convergence = several **independent** signal families pointing the same way
  (price/flows/sentiment/fundamentals/macro). Two sentiment tools agreeing is
  one signal, not two.
- Divergence is only meaningful when both legs are current — check as-of
  dates before claiming "price hasn't reacted yet".

## Conflict Handling

When signals disagree (e.g. positive sentiment, negative flows): report both
sides, say which you weight more and why, and carry the conflict into the
risk section. Never average a conflict into false neutrality, and never drop
the inconvenient leg.

## Confidence & Uncertainty

- Conviction scale: **Low / Medium / High** — with one line on what limits it.
- High conviction requires: ≥3 independent signal families aligned, no
  unresolved contradicting signal, and a clear catalyst or mechanism.
- Never manufacture certainty: no "will", "guaranteed", "inevitable" for
  market outcomes. Ranges and conditionals over point predictions.

## Risk Sections (asset-appropriate, never boilerplate)

Pick the categories that actually apply — an FX pair does not have tokenomics
risk and a stablecoin does not have valuation risk:

- **Equities:** valuation, earnings/guidance, balance sheet, macro
  sensitivity, event risk.
- **Crypto:** volatility, liquidity, tokenomics/unlocks, on-chain
  concentration, regulatory, narrative reversal.
- **FX:** central-bank surprise, macro data surprise, rate differentials,
  political risk, liquidity, correlation regime.

Every named risk should be concrete ("ECB cuts faster than priced") — a risk
that could be pasted under any asset is filler.

## Compliance Posture

These are research and decision-support workflows, not advice or execution.
Built into structure, not disclaimers: no return guarantees, no trade
execution, facts separated from interpretation, uncertainty stated,
invalidation always present. Do not append generic disclaimer paragraphs —
the discipline is the disclaimer. One line at most when the user asks for an
actionable-sounding output: "Research, not a recommendation."

## Red Flags — Rewrite Before Delivering

- A number without a source call behind it
- A thesis section with no invalidation condition
- "Sentiment is improving" from one day of counts
- An interpretation phrased as fact ("the market is rotating into…")
- Risk lists identical across different assets
- Conviction: High with fewer than three independent signal families
