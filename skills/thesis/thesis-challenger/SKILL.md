---
name: thesis-challenger
description: Use when a trader states a directional view and wants it attacked — "challenge my thesis", "stress-test this idea", "what am I missing?", "play devil's advocate", "red-team my NVDA long", "poke holes in this", "I'm bullish on X because… am I wrong?". Also after a thesis-builder output when the trader asks for the other side. Not for building a thesis from research (thesis-builder) or for sizing/downside math (risk-reward-analysis).
license: MIT
---

# Thesis Challenger

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Adversarial red-team of a stated thesis: actively retrieve the evidence
most likely to break it and answer "what am I missing?". The stance is
disconfirmation — every call is chosen to hurt the thesis — but the
objective is accuracy, not argument: a thesis that survives a genuine
attempt to break it is a valid, valuable result, and the skill says so.

## Supported Assets

US equities & ETFs, major crypto assets, G10 + liquid EM FX pairs. Needs a
thesis with at least an asset and a direction; a full thesis-builder
contract in context is the ideal input because its invalidation conditions
become test targets.

## Required Inputs

The thesis: asset + direction + at least one stated reason ("I'm bullish
on NVDA because inference demand is compounding"). If the trader gives only
asset + direction, proceed — but note the challenge can only attack the
generic case for that direction, not their specific reasoning. Horizon
defaults to multi-week if unstated.

## Optional Inputs

Horizon, entry level / current position, the evidence the trader is relying
on (each piece becomes a specific test target), prior thesis-challenger
runs (attack what changed since).

## Lexfi MCP Calls

**Budget: 6–10 calls, chosen adversarially** — decompose the thesis into
its load-bearing claims first, then buy the datasets most likely to
contradict them. Never a fixed checklist run blind: a valuation attack on
a meme coin or a tokenomics attack on EURUSD is wasted budget.

Challenge dimensions and their per-class ammunition:

| Dimension | Equities | Crypto | FX |
|---|---|---|---|
| Contrary sentiment trend | `get_stocks_news_sentiment` (symbol) | `get_crypto_news_sentiment` (`XXXUSD`) | `get_forex_news_sentiment` + `get_ai_fx_ratio` |
| Positioning crowding | `get_cnn_fear_greed_index` + `get_analyst_ratings` (consensus already all-in?) | `get_funding_rates` + `get_open_interest` (+ `get_liquidations` for recent unwinds) | `get_ai_fx_ratio` extremes + `get_rate_probabilities` (move already fully priced?) |
| Valuation / already-priced | `get_key_metrics` + `get_analyst_estimates` | *(no valuation leg — substitute price-vs-history via `get_coin_market_chart`)* | `get_rate_probabilities` per CB |
| Macro exposure | `get_us_macro_regime` / `get_macro_yield_curve` | `get_macro_credit_liquidity` + `get_daily_dxy_index` | `get_macro_forecasts` / `get_country_metrics` |
| Insider / whale behavior | `get_insider_trades` + `get_superinvestor_activity` or `get_congress_trading` | `get_whale_alerts` + `get_onchain_flows` | *(not available — say so, don't substitute)* |
| Upcoming event risk | `get_earnings_calls_by_ticker` (cadence) + `get_economic_calendar` (1–2 day window) | `get_cb_calendar` + `get_crypto_prediction_markets` | `get_cb_calendar` + `get_cb_insights` |

Pick 4–6 dimensions where the thesis is most exposed; batch all
independent calls in one round trip. Prediction-market tools
(`get_stocks_prediction_markets`, `get_macro_prediction_markets`,
`get_crypto_prediction_markets`) are a cheap "what does the market
handicap?" cross-check when the thesis hinges on a discrete event.

**Applicable traps (playbook):** `get_open_interest` non-crypto perps
filter; `get_funding_rates` dirty names, per-interval rates;
`get_whale_alerts` custody rotations — count unique tagged flows only;
`get_onchain_flows` net-per-asset; `get_analyst_estimates`
far-future-first ordering; `get_rate_probabilities` snapshot-only —
never claim "pricing has shifted"; economic-calendar payload bomb;
`get_ai_fx_ratio` weekly trend only; correct fear/greed tool per class.

## Workflow

1. **Decompose the thesis** into 2–4 load-bearing claims (mechanism,
   evidence legs, implied assumptions the trader didn't state — the
   unstated ones are often weakest).
2. **Map each claim to its best disconfirming dataset** from the dimension
   table; select 4–6 dimensions within budget, skipping dimensions that
   cannot apply to the asset class.
3. **Execute** — one parallel batch (plus a dependent second batch only for
   true sequences like transcript-list → insights).
4. **Grade every finding that cuts against the thesis:**
   - **Serious** — current data directly contradicts a load-bearing claim,
     or reveals a risk that breaks the mechanism.
   - **Notable** — weakens a supporting leg, shows crowding/already-priced
     conditions, or surfaces a dated risk inside the horizon.
   - **Minor** — friction worth knowing; doesn't change the expected value
     much.
   Evidence that *supports* the thesis is reported too (one line each) —
   suppressing it would be arguing for its own sake.
5. **Verdict** by rule, not vibe:
   - **SURVIVES** — no Serious challenge after ≥4 dimensions genuinely
     tested.
   - **WEAKENED** — one Serious with a partial rebuttal, or several
     Notables compounding.
   - **BROKEN** — a Serious challenge invalidates the core mechanism or an
     invalidation condition has already triggered.
6. **Answer "what am I missing?"** explicitly: the strongest single
   challenge, plus any invalidation condition the original thesis should
   add or tighten.

## Output Format

```text
THESIS CHALLENGE — <SYMBOL> <direction>                 <date>
Stated thesis: <trader's claim, restated in one line>
Dimensions tested: <n of 6 — list; note any not applicable to class>

CHALLENGES (strongest first)
1. [SERIOUS] <dimension> — <finding, specific evidence + as-of>
   Why it matters: <which load-bearing claim it hits> [interpretation]
2. [NOTABLE] <dimension> — <finding, evidence>
3. [MINOR]  <dimension> — <finding, evidence>

WHERE THE THESIS HELD UP
• <dimension>: <supporting evidence found while trying to break it>

VERDICT: <SURVIVES / WEAKENED / BROKEN>
Strongest single challenge: <one line — the thing the trader is most
likely missing>
Suggested invalidation update: <condition to add/tighten, or "existing
invalidation adequate">

Sources & data as-of: <tools used; dimensions untestable + why>
Research, not a recommendation.
```

## Quality Controls

- Every challenge carries evidence from a specific call — a challenge with
  no data behind it is model opinion and must be labeled
  `[model knowledge — not Lexfi data]` and graded no higher than Minor.
- ≥4 dimensions genuinely tested before any SURVIVES verdict; fewer means
  the verdict line reads "insufficient test — n dimensions only".
- Grades follow the step-4 definitions — never inflate a Minor to make the
  output look rigorous, never soften a Serious to be agreeable.
- Supporting evidence found en route is reported, not buried; a challenge
  run that finds the thesis strong says so plainly.
- One strongest-challenge line is mandatory in every verdict, even
  SURVIVES.
- Output ≤ ~50 lines.

## Failure Handling

- A dimension's tool errors or returns empty → mark that dimension
  "untestable — <reason>" in the output; never fill it from model
  knowledge and never let it silently count toward SURVIVES.
- Plan-gated tools absent (transcripts, CB transcripts, quant models — Pro
  Max) → degrade: earnings-tone attacks use `get_earnings_surprises` +
  `get_stock_news`; CB-tone attacks use `get_cb_insights` summary rows;
  state the degradation.
- Thesis too vague to decompose (no reason given) → run the generic
  directional attack, and say the trader's actual reasoning went untested.
- More than half of chosen dimensions untestable → report "challenge not
  supportable today" with what was found, rather than a hollow verdict.

## Example Prompts

- "I'm bullish on NVDA because inference demand keeps compounding — what am I missing?"
- "Challenge my thesis that ETH outperforms BTC this quarter."
- "Stress-test this: short EURUSD into the ECB meeting."
- "Play devil's advocate on my long-uranium idea."
- "Red-team the thesis you just built for me."
