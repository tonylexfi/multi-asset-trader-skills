---
name: risk-reward-analysis
description: Use when a trader asks about the risk side of a named candidate trade — "what's the risk/reward on X?", "how much could I lose?", "what's the downside here?", "help me size this", "is the asymmetry worth it?", "where am I wrong on this trade?", "what could hit this position before earnings?". Applies to a stated long/short idea in equities, crypto, or FX, often following thesis-builder or discovery output. Not for building or challenging the thesis itself.
license: MIT
---

# Risk-Reward Analysis

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Structure the risk side of a candidate trade: realized-volatility-anchored
scenario ranges, an explicit asymmetry read, crowding and event-risk
checks, invalidation levels that sit outside noise, and volatility-aware
position-sizing **frameworks**. Hard boundary: frameworks and scenario
math only — never "risk X% of your account", never a prescribed size or
leverage, never a guaranteed outcome.

## Supported Assets

US equities & ETFs, major crypto assets, G10 + liquid EM FX pairs. One
trade per run. Not for portfolio-level risk, options greeks, or margin
math — say so if asked.

## Required Inputs

Asset + direction. An entry zone or current reference level sharpens every
number; if absent, the current price from the vol-context call becomes the
reference. If direction is missing, ask ONE compact question — asymmetry
has no meaning without it.

## Optional Inputs

Horizon (default multi-week), intended invalidation level (tested against
noise rather than assumed), existing correlated positions (named as a
concentration flag, not computed), the thesis it derives from (its
invalidation conditions are reused, not reinvented).

## Lexfi MCP Calls

**Budget: ≤6 calls, typically 4–5, two batches max.**

1. **Realized-vol context (1 call, mandatory):**
   `get_historical_prices` (equities, `from`/`to` ~6 months) /
   `get_coin_market_chart` (CoinGecko id, `days: "90"`) /
   `get_daily_fx_pair` (6-char pair, ~3-month window). Extract: typical
   daily and weekly move, realized range, worst drawdown in window,
   current level.
2. **Crowding check (1–2 calls, class-appropriate):** crypto —
   `get_funding_rates` + `get_open_interest`; equities —
   `get_cnn_fear_greed_index` and/or `get_analyst_ratings` (unanimous
   consensus = crowded); FX — `get_ai_fx_ratio` (extremes) or
   `get_rate_probabilities` (move already fully priced).
3. **Event-risk check (1–2 calls):** `get_cb_calendar` (no params) and/or
   `get_economic_calendar` in 1–2 day windows around known risk dates;
   equities add `get_earnings_calls_by_ticker` for report cadence when the
   horizon could contain a report.
4. **Optional refresh (≤1 call):** `get_stock_quote` only if the vol-context
   series is a day stale and precision at entry matters.

Skip conditions: thesis-builder output in context supplies invalidation
and catalysts — reuse them, don't re-derive; crowding tools already
fetched this session are read from context.

**Applicable traps (playbook):** `get_daily_fx_pair` weekend/holiday rows
EXCLUDED from vol and range math, changePercent already in percent;
`get_coin_market_chart` coin_id + string-enum days; `get_open_interest`
non-crypto perps filtered before crowding claims; `get_funding_rates`
dirty names, per-interval rates — outliers and sign flips are the signal;
economic-calendar payload bomb; correct fear/greed tool per class; VIX
changePercent units if VIX is consulted.

## Workflow

1. **Frame the trade**: asset, direction, reference level, horizon; pull
   any in-context thesis invalidation.
2. **Vol context call** → compute typical 1-day / 1-week move and the
   realized range for the window. These are facts; everything built on
   them is labeled [interpretation].
3. **Scenario ranges**: favorable / base / adverse zones expressed as
   multiples of the typical weekly move over the horizon — ranges, never
   point targets, never probabilities dressed as facts.
4. **Invalidation level**: the observable level or event outcome where the
   trade idea is wrong. **Noise test**: an invalidation inside ~1 typical
   weekly move of entry will likely trigger on noise, not on the thesis
   failing — flag it and show the nearest level that clears the test.
5. **Asymmetry assessment**: distance to the favorable zone vs distance to
   invalidation, in units of typical weekly move. State the ratio and what
   would have to be true for the favorable leg to be reachable within the
   horizon. A ratio near or below 1:1 is stated bluntly, not massaged.
6. **Crowding check** → is the trade consensus? Crowded-with-the-trade
   raises unwind risk (adverse gaps); crowded-against can mean squeeze
   fuel. Labeled interpretation either way.
7. **Event-risk check** → dated events inside the horizon that can gap the
   asset through the invalidation level; note which scenario each event
   feeds.
8. **Sizing frameworks (concepts only)**: present 2–3 volatility-aware
   frameworks with the trader's own parameters left as variables — e.g.
   size inversely proportional to realized vol so different trades carry
   comparable risk; risk-per-unit defined by entry-to-invalidation
   distance so acceptable-loss (trader's choice) determines units;
   correlation haircut when an existing position shares the same driver.
   No filled-in percentages of anyone's account. Ever.

## Output Format

```text
RISK/REWARD — <SYMBOL> <Long/Short>                      <date>
Reference: <entry or current level, as-of>   Horizon: <window>
Vol context: typical day ±<x>%, typical week ±<y>%, <n>-period range
<lo>–<hi>, worst drawdown in window <z>% (as-of <date>)

SCENARIOS [interpretation — realized-vol-anchored, not forecasts]
Favorable: <zone> (~<n>x weekly move) — needs: <condition>
Base:      <zone> — <what no-news drift looks like>
Adverse:   <zone> (~<n>x weekly move) — driven by: <condition/event>

Invalidation: <level or event outcome>
Noise test: <PASSES / FAILS — sits <n>x typical weekly move from entry;
if FAILS: nearest level that clears the test>

Asymmetry: <favorable distance> vs <invalidation distance> ≈ <a:b>
Read: <one blunt line — attractive / marginal / poor, and why>

Crowding: <evidence + as-of> → <crowded with / against / neutral>
[interpretation]
Event risk inside horizon:
• <date — event — which scenario it feeds>

SIZING FRAMEWORKS (concepts — parameters are yours)
• <framework>: <one-line mechanic with variables, no filled numbers>
• <framework>: <one-line mechanic>

Sources & data as-of: <tools used; gaps>
Research, not a recommendation.
```

## Quality Controls

- Every scenario zone traces arithmetically to the vol-context call —
  no range that can't be reproduced from typical-move multiples.
- The noise test runs on every invalidation level, including one the
  trader supplied; a FAIL is reported, never silently repaired.
- **Sizing boundary is absolute**: no account percentages, no dollar
  amounts, no leverage suggestions, no "conservative traders should…" —
  frameworks with unbound variables only.
- No guarantees or certainty language anywhere; adverse scenarios are as
  fully specified as favorable ones.
- Crowding and event-risk each get a finding even when clean ("no crowding
  evidence found", "no dated events inside horizon") — absence is a
  result, not an omission.
- Output ≤ ~45 lines.

## Failure Handling

- Vol-context call fails → the skill cannot do its job honestly: report
  "Data unavailable: price history" and stop short of scenario math rather
  than inventing ranges; deliver crowding/event findings that did succeed.
- Crowding tools empty or class has no positioning tool (FX has no
  whale/insider leg) → state the dimension as untestable; never proxy from
  model knowledge.
- Calendar unavailable → event-risk section reads "calendar unavailable —
  dated-event risk unassessed"; confidence in the adverse scenario is
  widened, not narrowed.
- Plan-gated tools absent (Pro Max: quant models, transcripts) → not core
  to this skill; if an earnings-tone check was requested, degrade to
  `get_earnings_surprises` cadence and say so.
- Symbol resolution failure → playbook fallbacks (`TICKER:CC`, 6-char FX
  pair, CoinGecko id) before asking the trader.

## Example Prompts

- "What's the risk/reward on going long NVDA here?"
- "How much could I lose on this SOL position over a month?"
- "What's the downside if I short EURUSD before the Fed?"
- "Help me think about sizing this copper-miner trade."
- "Is the asymmetry on that thesis you built actually any good?"
