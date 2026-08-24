---
name: divergence-discovery
description: Use when a trader asks for mismatches between price and information — "find divergences", "where is sentiment positive but price flat", "strong flows but the price hasn't moved", "what is the market missing", "price and fundamentals disagree", "who's lagging their news". Price-vs-information mismatch phrasings; open-ended idea requests without a mismatch angle trigger opportunity-discovery.
license: MIT
---

# Divergence Discovery

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

Find assets where price and information disagree — positive sentiment with
weak price, strong flows with flat price, deteriorating fundamentals with a
strong tape — and type each divergence honestly, testing the boring
explanations (already priced, stale leg, data artifact) BEFORE calling
anything an opportunity. Output feeds `asset-deep-dive` and
`thesis-challenger`.

## Supported Assets

US equities & ETFs, major crypto assets, G10 FX pairs. Cross-asset seeding
by default; the user may scope to one class without leaving this skill —
the divergence angle, not the asset class, is what routes here.

## Divergence Types

| Type | Leg A (information) | Leg B (price) | Classic false positive |
|---|---|---|---|
| **Sentiment↔price** | news sentiment trend | price window | price moved BEFORE the sentiment window |
| **Flows↔price** | funding/OI/on-chain flows | price window | custody churn read as accumulation |
| **Fundamentals↔price** | metrics / surprises trend | price window | stale quarterly data vs current tape |

Every surfaced divergence is assigned exactly one type; both legs carry
as-of dates.

## Required Inputs

None. Defaults: cross-asset seed, 4 divergences (both directions —
information-ahead AND price-ahead), sentiment/price windows of 2 weeks vs
trailing month.

## Optional Inputs

Asset class scope, direction preference (only "market hasn't caught up"
longs, or only "price is ahead of reality" shorts), count, watchlist to
check for divergences, minimum liquidity.

## Lexfi MCP Calls

**Budget: 10–14 calls, hard cap 14.** Divergence needs BOTH legs from
Lexfi — never pair a fresh Lexfi leg with a remembered one.

**Stage 1 — Cross-asset seed (one parallel batch, 5 calls):**
`get_market_movers`, `get_sector_performance`, `get_coin_markets`
(`per_page` 50, filter stables/wrapped), `get_stocks_news_sentiment`
(aggregate), `get_crypto_news_sentiment` (aggregate). Seeds come from
mismatch hints: non-movers in moving sectors, sentiment-heavy names absent
from movers, movers with no sentiment support.

**Stage 2 — Cross-universe information legs (one parallel batch, 2–3
calls, each covers many assets):** `get_funding_rates`, `get_open_interest`
(filter non-crypto perps), `get_onchain_flows` (net per asset, churn pairs
discarded). FX candidates: `get_ai_fx_ratio` for 1–2 currencies instead.

**Stage 3 — Leg verification on shortlist (3–5 assets, 2 calls each max,
batched):** the PRICE leg per class — `get_historical_prices` (equities,
`from`/`to` covering both windows), `get_coin_market_chart` (`days` "30"),
`get_daily_fx_pair` (weekend rows excluded); the INFORMATION leg per
symbol — `get_stocks_news_sentiment` / `get_crypto_news_sentiment`
(symbol), or `get_key_metrics` + `get_earnings_surprises` for
fundamentals↔price, or `get_whale_alerts` (deduped) for flow claims.

**Applicable traps (playbook, non-negotiable):** whale custody rotations
and on-chain churn pairs (a deduped-away flow leg = no divergence);
funding dirty names; coin-markets stable/wrapped filter; FX pair
weekend rows and percent units; `get_ai_fx_ratio` weekly-trend-only;
sentiment proportions over raw counts.

## Workflow

1. **Parse scope** → classes, direction, count, watchlist. One compact
   clarifying question max.
2. **Stage 1 batch** → nominate ~8–15 mismatch seeds, each with the hint
   that nominated it.
3. **Stage 2 batch** → attach cheap cross-universe information legs;
   discard seeds whose "information" evaporates under the trap filters.
4. **Stage 3 batch on the top 3–5** → fetch BOTH legs properly.
   **As-of gate (hard):** each leg must be current — price leg within 1
   trading day, information leg within its tool's normal cadence. A stale
   leg kills the divergence; it is reported in "Dismissed", not surfaced.
5. **Boring-explanation gate (hard, before typing anything a divergence):**
   - *Already priced?* Extend the price window — did price move before the
     information window started? If yes → not a divergence, price led.
   - *Stale leg?* As-of check from step 4.
   - *Data artifact?* Does the leg survive the applicable trap filter?
   Only survivors are typed and ranked. This gate is the skill.
6. **Rank survivors** by magnitude of the gap × freshness of the
   information leg × liquidity. For each, state BOTH resolution paths:
   price closes the gap, or the information leg was wrong.
7. **Deliver** — every entry: type, both legs with as-of, boring
   explanations ruled out, thesis + invalidation.

## Output Format

```text
DIVERGENCE SCAN — <date>
Scope: <classes>      Direction: <both/info-ahead/price-ahead>    Windows: <A vs B>

1. <SYMBOL> — <name>        <class> · Type: <sentiment/flows/fundamentals↔price>
   Information leg: <specific evidence + trend window> (as-of <date>)
   Price leg: <move over window vs trailing baseline> (as-of <date>)
   Gap: <one line stating the mismatch in plain terms>
   Boring explanations ruled out:
   • Already priced: <what the extended window showed>
   • Stale data: <both legs current — dates>
   • Artifact: <trap filter applied and survived>
   Resolution paths: <price closes gap> vs <information leg proves wrong>
   Thesis (working): <one falsifiable line naming the favored path> [interpretation]
   Invalidation: <observable condition — typically the opposite leg confirming>
   Conviction: <Low/Med/High> — <one line on what limits it>
   Key risks: <2–3, asset-appropriate>

2. …

Dismissed as boring: <2–3 seeds + which explanation killed each — this
section is mandatory>
Sources & data as-of: <tools used per leg; gaps: what was unavailable>
```

## Quality Controls

- Both legs of every surfaced divergence come from Lexfi calls in THIS
  session, each with an as-of date printed — one-legged divergences are
  banned.
- "Dismissed as boring" is mandatory and non-empty in any scan that
  nominated more seeds than it surfaced — it proves the gate ran.
- The already-priced test always extends the price window beyond the
  information window; a divergence claimed on matching windows alone is a
  rewrite trigger.
- Flow-based divergences state the surviving NET figure after
  dedupe/netting, never the raw transfer sum.
- Conviction High additionally requires a mechanism for WHY the market is
  mispricing (illiquidity, attention gap, disclosure lag) — a gap with no
  mechanism caps at Medium.
- Output ≤ ~110 lines for 4 divergences.

## Failure Handling

- One leg's tool errors for a candidate → the candidate cannot be surfaced;
  move it to "Dismissed" with "leg unavailable", never substitute model
  knowledge for a leg.
- Plan-gated tools (company transcripts / quant models — Pro Max only) →
  fundamentals legs degrade to `get_key_metrics` + `get_earnings_surprises`
  + news; label the degradation in Sources.
- Stage-2 snapshot errors → flows↔price type drops from the scan; deliver
  the other types and say so.
- Zero survivors of the boring-explanation gate → that IS the finding:
  report "no genuine divergences — the apparent ones were <explanations>"
  with the dismissed list. An empty scan delivered honestly beats a forced
  one.

## Example Prompts

- "Find assets where sentiment is positive but the price hasn't moved."
- "Where are flows strong but price flat — anything the market's missing?"
- "Any stocks priced like nothing's wrong while fundamentals deteriorate?"
- "Check my watchlist for price-vs-news divergences."
- "What's lagging its own news flow right now?"
