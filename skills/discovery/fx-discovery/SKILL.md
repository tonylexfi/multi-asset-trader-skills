---
name: fx-discovery
description: Use when a trader asks for currency or FX pair ideas by name of class — "find me FX trades", "which currency pairs look interesting", "where is the biggest policy divergence", "any G10 setups", "which currencies are strong/weak right now", "find pairs where rates and data line up". FX-scoped requests only; mixed or open-ended cross-asset requests trigger opportunity-discovery instead.
license: MIT
---

# FX Discovery

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Find FX pairs where macro/policy divergence or aligned rates + data +
sentiment create a setup — by scoring CURRENCIES first, not pairs. Scoring
N currencies covers N² pairs for the price of N calls; pair-level depth is
spent only on the best long/short combinations. Output feeds
`fx-macro-analysis` and `thesis-builder`.

## Supported Assets

G10 currencies and their crosses; liquid EM via `get_daily_fx_local_vs_usd`
on request (reduced signal coverage — say so). NOT supported here: crypto
pairs (`crypto-discovery`), equities (`stock-discovery`), cross-asset scans
(`opportunity-discovery`).

## Required Inputs

None. Defaults: USD, EUR, JPY, GBP + 1–2 currencies suggested by the
dollar-regime read (max 6 scored), 3 pair candidates, multi-week horizon.

## Optional Inputs

Currencies to include/exclude, EM interest, direction view already held
("I'm short EUR — what pairs it best?"), count, horizon, event-risk
tolerance.

## Lexfi MCP Calls

**Budget: 10–14 calls, hard cap 14.** Currency-level scan BEFORE pair-level
depth — never open with pair calls.

**Stage 1 — Currency scan (one parallel batch, 6–8 calls):**
`get_daily_dxy_index` (2-week window — dollar regime anchors every cross),
`get_ai_fx_ratio` per scored currency (≤6 calls; trend via
`diff_AI_FX_ratio` over weeks, never day-over-day), `get_forex_news_sentiment`
(aggregate tone, 1 call).

**Stage 2 — Policy leg (one parallel batch, 2–4 calls):**
`get_rate_probabilities` per relevant CB (`fed`, `ecb`, `boe`, `boj` short
codes) — only for CBs whose currencies scored at the extremes of stage 1.
Snapshot only: never claim "pricing has shifted" from one call.

**Stage 3 — Pair depth (top 2–3 pairs, one parallel batch, 2–4 calls):**
`get_daily_fx_pair` (6-char symbol `EURUSD`, date-windowed ~1 month) to
confirm the pair's price hasn't already fully expressed the divergence;
`get_cb_insights` (bankId short code) on the 1–2 CBs whose tone drives the
top thesis — use `summary` + full conferences, ignore "quote shorts" clips.

**Applicable traps (playbook, non-negotiable):** `get_ai_fx_ratio`
stale-day repeats and missing dates (weekly trend only); `get_daily_fx_pair`
`changePercent` already in percent + weekend/holiday rows excluded from
range/vol claims; `get_rate_probabilities` snapshot-only;
`get_cb_insights` decimal-string numerics and clip-row duplicates;
`get_forecast` is WEATHER — macro projections are `get_macro_forecasts`.

## Workflow

1. **Parse scope** → currencies (≤6), EM yes/no, count, existing views. One
   compact clarifying question max.
2. **Stage 1 batch** → per-currency news-strength trend + dollar regime.
3. **Build the divergence matrix** — the core artifact. Score each currency
   −2…+2 on each dimension; every cell cites its evidence:

```text
            NEWS STRENGTH   POLICY PATH     DOLLAR REGIME    NET
            (ai_fx trend)   (rate probs)    (DXY context)
USD             +1              +2            —              +3
EUR             -1              -1            n/a            -2
JPY             +1               0            n/a            +1
…
```

4. **Stage 2 batch** → fill the POLICY PATH column for extreme-scoring
   currencies (hawkish repricing = +, dovish = −).
5. **Nominate pairs** = strongest net-positive vs weakest net-negative
   currency, plus any pair where two dimensions diverge in the SAME
   direction (materiality test: |net difference| ≥ 3 or two independent
   dimensions aligned — otherwise the pair does not advance).
6. **Stage 3 batch on top 2–3 pairs** → price confirmation (has the pair
   already moved with the divergence? how far, over what window?) + CB tone
   check. A pair that has fully expressed the divergence is reported as
   "already moved", not as a fresh setup.
7. **Deliver** — matrix, then pairs, each with thesis + invalidation.

## Output Format

```text
FX DISCOVERY SCAN — <date>
Scope: <currencies scored>       Dollar regime: <1 line from DXY, as-of>

DIVERGENCE MATRIX (−2…+2 per cell; evidence in notes)
CCY   NEWS   POLICY   NET    Note
USD   <s>    <s>      <n>    <1-line evidence with as-of>
EUR   …
<N currencies → N² candidate pairs; scored: <list>>

1. <PAIR> — <direction>                    Conviction: <Low/Med/High>
   Why it surfaced:
   • Divergence: <base ccy score vs quote ccy score, which dimensions>
   • Policy: <rate-path evidence, as-of> 
   • Price check: <pair move over window — room left or already expressed>
   Opposing: <strongest counter-signal, or "none found">
   Event risk: <next CB meeting / major data in play, or "none dated">
   Thesis (working): <one falsifiable line with horizon> [interpretation]
   Invalidation: <observable condition — level, repricing, or tone shift>
   Key risks: <2–3 FX-appropriate: CB surprise / data surprise / correlation
   regime / political>

2. …

Not surfaced but considered: <1–2 pairs + why the matrix rejected them>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- The divergence matrix appears in every output — a pair recommendation
  without its currency-level scores is banned.
- Every matrix cell traces to a call; empty cells are marked "—" with the
  gap named, never scored from priors.
- `get_ai_fx_ratio` evidence always spans weeks; any day-over-day FX
  sentiment claim is a rewrite trigger.
- Stage 3 price check is mandatory before any pair is called a setup —
  "divergence" with no already-moved test is the classic false positive.
- Conviction High requires ≥3 aligned independent families (news, policy,
  price room count separately) + no dated event risk inside the horizon
  that could resolve either way.
- Output ≤ ~100 lines for 3 pairs; two-sided depth belongs in
  `fx-macro-analysis`.

## Failure Handling

- `get_ai_fx_ratio` missing/stale for one currency → score its NEWS cell
  "—", keep the currency if POLICY evidence exists; note in Sources.
- Plan-gated tools (CB conference transcripts, quant macro models — Pro Max
  only) → tone evidence degrades to `get_cb_insights` indices and
  `get_forex_news_sentiment`; macro projections degrade to rate
  probabilities + DXY facts; say what was skipped.
- `get_rate_probabilities` unavailable for a CB → the POLICY column for
  that currency is a gap; cap any pair using it at Conviction Low.
- No pair reaches |net difference| ≥ 3 → report "no strong FX divergence
  currently" with the closest 1–2 and what's missing — never force a pair.

## Example Prompts

- "Find me FX pairs with the biggest policy divergence right now."
- "Which G10 currencies are strongest and weakest — and what's the best pair?"
- "Any FX setups where rates and news flow line up?"
- "I think the dollar tops here — which pair expresses that best?"
- "Scan majors plus AUD and CAD for divergence trades."
