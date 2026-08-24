---
name: market-regime
description: Use when a trader asks what regime the market is in, whether conditions are risk-on or risk-off, or for a one-screen state-of-the-market read — "what regime are we in", "risk-on or risk-off right now?", "how's the overall market looking", "give me a market dashboard", "is this a good environment for risk?" — without naming a specific asset or macro scenario.
license: MIT
---

# Market Regime

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Answer "what kind of market is this?" in one screen: equity volatility and
breadth, crypto conditions, dollar, yield curve, liquidity, and macro regime
probabilities — synthesized into a single labeled read that a plain
conversation would assemble slowly and inconsistently. Output feeds
`opportunity-discovery` (context) and `macro-impact-analysis` (scenarios).

## Supported Assets

Cross-asset by construction: US equities (vol, breadth, sectors), crypto
(cap, dominance, fear/greed), USD, US rates, US macro. NOT a per-asset
diagnosis — hand a named-asset question to `asset-deep-dive`, and a "what
does scenario X mean for Y" question to `macro-impact-analysis`.

## Required Inputs

None. The skill runs on defaults: today's snapshot, 2-week windows for the
history tools (VIX, DXY, yield curve) so day-vs-trend can be stated.

## Optional Inputs

Emphasis ("focus on crypto conditions", "I care about rates"), a holding
context ("I'm mostly long tech") — shifts the favors/disfavors section, not
the call plan.

## Lexfi MCP Calls

**Budget: 10 calls, ALL in one parallel batch. No depth layer, no
follow-ups** — this skill is a snapshot, and every tool below is either
param-free or cheaply windowed:

| Dimension | Tool | Params |
|---|---|---|
| Equity vol | `get_daily_vix_index` | 2-week window |
| Equity fear/greed | `get_cnn_fear_greed_index` | — |
| Index/ETF tape | `get_market_overview` | — |
| Breadth & rotation | `get_sector_performance` | — |
| Crypto regime | `get_crypto_global_metrics` | — |
| Crypto fear/greed | `get_fear_greed_index` | — |
| Dollar | `get_daily_dxy_index` | 2-week window |
| Curve | `get_macro_yield_curve` | latest dates |
| Macro regime | `get_us_macro_regime` | — |
| Liquidity | `get_macro_credit_liquidity` | recent limit |

**Applicable traps (from playbook, non-negotiable):** VIX `changePercent`
returns percent despite a decimal schema — sanity-check against
change/prior-close before scaling; `get_fear_greed_index` is the CRYPTO
gauge and `get_cnn_fear_greed_index` the EQUITY one — never swap; regime
probabilities from `get_us_macro_regime` are probabilistic — never collapse
to a binary label.

## Workflow

1. **Fire the full batch** — all 10 calls in one parallel round trip.
2. **Read each dimension independently** and state it as level + direction
   (today vs its 2-week window where history exists). One line each:
   vol, sentiment (both gauges), breadth (leaders vs laggards count),
   crypto (cap trend + BTC dominance direction), dollar, curve (**compare
   2Y vs 10Y explicitly** — state the spread and its sign), liquidity,
   macro regime (top 2 probabilities, never just the winner).
3. **Synthesize** — the regime call is the *intersection* of dimensions,
   labeled `[interpretation]`. Where dimensions conflict (e.g. calm VIX +
   greedy crypto + inverting curve), report the conflict per
   evidence-discipline: both sides, which is weighted more, why.
4. **Map to positioning context** — what this regime configuration has
   historically favored/disfavored, each line labeled `[interpretation]`
   or `[model knowledge — not Lexfi data]`. Descriptive, never a
   recommendation.
5. **State what would change the read** — the 2–3 observable prints that
   would flip the regime call (falsifiability applied to a regime, not a
   thesis).

## Output Format

```text
MARKET REGIME READ — <date>
Regime call: <one line, probabilistic> [interpretation]

Dimension          Now                    vs 2-wk        Read
Equity vol         VIX <level>            <↑/↓/→>        <calm/elevated/stressed>
Equity sentiment   CNN F/G <score/label>  —              <read>
Breadth/rotation   <n>/11 sectors green   —              <leadership: ...>
Crypto             cap <Δ%>, BTC dom <%>  <dom ↑/↓>      <read>
Crypto sentiment   F/G <score/label>      —              <read>
Dollar             DXY <level>            <↑/↓/→>        <read>
Yield curve        2Y <x> / 10Y <y>       spread <bp>    <steep/flat/inverted, direction>
Liquidity          <key series>           <easing/tightening>
US macro regime    <top regime p%> / <2nd regime p%>     (probabilities, not a verdict)

Conflicts: <dimensions disagreeing + which is weighted more and why, or "aligned">

This regime has historically favored:    <2–3 lines, each labeled>
This regime has historically disfavored: <2–3 lines, each labeled>

What would change the read:
• <observable print/level>  → <which dimension flips>
• <observable print/level>  → <which dimension flips>

Sources & data as-of: <tools + as-of dates; gaps: what was unavailable>
```

## Quality Controls

- All 10 dimensions present in the table — a failed call shows as "Data
  unavailable", never as a silently dropped row.
- The 2Y/10Y comparison is explicit (both yields + spread in bp), not
  "the curve is inverted" asserted bare.
- Macro regime always reported as ≥2 probabilities; banned: "we are in a
  recession regime" as a flat claim.
- Every favors/disfavors line carries its label; none may be phrased with
  fact grammar.
- Output ≤ ~45 lines — this is a one-screen product; depth belongs to
  `macro-impact-analysis` or `asset-deep-dive`.
- Zero follow-up calls: if the batch leaves a question open, name it in
  "What would change the read" rather than burning budget.

## Failure Handling

- Any single tool errors → its row reads "Data unavailable: <dimension>";
  synthesize from the remaining dimensions and lower the stated confidence
  of the regime call.
- ≥5 dimensions unavailable → per evidence-discipline, report that a
  regime read is not supportable today; deliver the surviving rows only.
- `get_us_macro_regime` or `get_macro_credit_liquidity` gated/absent on
  this plan → degrade: infer nothing in their place, note the gap, and
  say the macro-regime row would need Pro Max (Quant Lexfi Models).
- Stale as-of dates (weekend/holiday) → print the as-of date next to the
  figure; never present Friday's close as "today" without saying so.

## Example Prompts

- "What regime are we in right now?"
- "Risk-on or risk-off today?"
- "Give me a one-screen state of the market."
- "Is this a good environment for risk assets?"
- "How do equity vol, crypto, the dollar and the curve line up right now?"
