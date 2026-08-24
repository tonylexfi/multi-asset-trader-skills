---
name: crypto-intelligence
description: Use when a trader asks deep structural questions about one named crypto asset — "what's the positioning in ETH?", "is BTC crowded right now?", "are whales accumulating SOL?", "on-chain picture for LINK", "funding and open interest on bitcoin", "full structure read on this coin", "is this rally spot-led or leverage-led?". Owns derivatives positioning, on-chain flows, and narrative depth for a named coin. Coin discovery or a simple price question belongs elsewhere.
license: MIT
---

# Crypto Intelligence

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

The full structure read on one crypto asset: market structure, derivatives
positioning, on-chain movement, narrative, and the macro-liquidity backdrop
— with the on-chain trap set enforced at every step. Raw whale feeds and
flow tables are the most misread data in this library; this skill's value is
that every claim survives the filters.

## Supported Assets

Major crypto assets — those present in Lexfi's positioning and flow feeds
(BTC, ETH, SOL, top-100 alts; feed coverage thins fast below that).
Long-tail tokens: market chart + sentiment still work; positioning/on-chain
sections degrade to "not covered in feeds". One asset per run.

## Required Inputs

The coin. Symbol forms per tool: CoinGecko id for `get_coin_market_chart`
(`bitcoin`), `XXXUSD` for sentiment (`BTCUSD`), name-column match for
funding/OI. Defaults: 90-day structure window, positioning read on the
latest snapshot, narrative over the recent window.

## Optional Inputs

Existing position and side, horizon, the specific worry ("is the rally
leveraged?", "are unlocks being dumped?"), whether narrative/social depth
is wanted.

## Lexfi MCP Calls

**Budget: 6–10 calls, two batches max, hard cap 10.**

- **Batch 1 — market + narrative (parallel, 4 calls):**
  `get_coin_market_chart` (`days` "90"), `get_crypto_news_sentiment`
  (symbol `XXXUSD`), `get_crypto_global_metrics` (asset vs market beta
  context), `get_fear_greed_index` (crypto one).
- **Batch 2 — structure (parallel, 3–5 calls):** `get_open_interest`,
  `get_funding_rates`, `get_liquidations` (all cross-coin snapshots — one
  call each covers the universe; extract this asset's rows);
  `get_whale_alerts` + `get_onchain_flows` for feed-covered majors.
- **Conditional (0–2):** `get_chains_tvl` when the asset is an L1/L2 chain
  token; `get_macro_credit_liquidity` when the question touches the macro
  bid; ONE of `get_crypto_x_highlights` / `get_crypto_reddit_highlights` /
  `get_telegram_highlights` when narrative depth was requested (discourse,
  never fact).

**THE TRAP GAUNTLET — non-negotiable, run BEFORE interpreting batch 2.**
Every structure claim must pass all four filters; a claim that skips one is
wrong by default:

1. **Whale custody rotations** (`get_whale_alerts`): dedupe repeated
   identical-quantity transfers (e.g. the same 5,441 WBTC hourly — that is
   custody/collateral rotation, not accumulation). Count unique flows only;
   direction is meaningful ONLY on rows with a tagged exchange entity
   (→ exchange = potential sell supply; ← exchange = withdrawal). Untagged
   or repeated rows support no directional claim, ever.
2. **Churn pairs** (`get_onchain_flows`): paired same-size inflow+outflow
   rows are market-maker churn. NET the flows per asset before any
   accumulation/distribution statement; no timestamps — present as a
   recent-window snapshot, never "today".
3. **Non-crypto perps** (`get_open_interest`): the snapshot includes XAU
   (gold), CL (oil), and tokenized equities (SNDK, SPCX, SKHYNIX). Filter
   them out before any positioning or market-wide claim.
4. **Dirty funding symbols** (`get_funding_rates`): symbol field is dirty
   (`XRPXRP`, `TRONTRX`, CJK duplicates) — match this asset on the NAME
   column. Rates are per-funding-interval, not annualized; near-zero
   average is normal — the signal is outliers and sign flips.

## Workflow

1. **Resolve** the coin across the three symbol forms; confirm feed
   coverage expectations for its size.
2. **Batch 1** → price structure (trend, drawdown, volume pattern), tone
   proportions (never raw counts), asset-vs-market context.
3. **Batch 2 → run the trap gauntlet**, then read positioning: OI change ×
   price direction (rising OI + rising price = new longs; rising OI +
   falling price = new shorts — label [interpretation]); funding outliers
   and sign flips; liquidation asymmetry (lopsided long/short wipes = fuel
   spent).
4. **On-chain read** on netted, deduped flows only: direction, size versus
   the asset's norm, exchange-tagged movements.
5. **Synthesize**: do market, positioning, on-chain, and narrative agree?
   Spot-led vs leverage-led is the classic call: price up + OI flat/down +
   spot outflows from exchanges = spot-led; price up + OI surging + funding
   spiking = leverage-led [interpretation]. Conflicts reported per
   evidence-discipline.
6. **Deliver** — ladder-structured, thesis with invalidation.

## Output Format

```text
CRYPTO STRUCTURE READ — <COIN> — <date>
Verdict: <2 lines — structure state + the single most important finding>

Market structure: <trend, key levels, volume, vs total-market, as-of>
Derivatives positioning: <OI Δ × price, funding outliers/flips, liq asymmetry>
On-chain (netted & deduped): <net flow direction + tagged exchange moves,
  or "no clean signal after filtering — raw feed was rotation/churn">
Narrative: <tone proportions trend + discourse themes [discourse]>
Macro/liquidity backdrop: <one line, or "not examined">

FACT:            <numbered — call results only, with as-of dates>
SIGNAL:          <numbered — each citing its facts; post-filter only>
INTERPRETATION:  <numbered — labeled, each citing its signals>

Thesis (working): <one falsifiable line + horizon> [interpretation]
Invalidation: <observable condition — a positioning or flow reversal counts>
Key risks: <2–3 — leverage, liquidity, unlocks, narrative reversal as apply>
Sources & data as-of: <tools used; gaps: what was unavailable>
```

## Quality Controls

- Zero directional whale claims from untagged or repeated-quantity
  transfers — the banned failure mode of this skill.
- Every flow figure is a NET figure; if netting kills the signal, the
  output says so rather than quoting gross rows.
- OI and market-wide claims state that non-crypto perps were filtered.
- Funding cited per-interval with the interval named; never annualized
  silently, never averaged into meaninglessness.
- Sentiment claims use proportions across a window, never one day's counts.
- The spot-led vs leverage-led call, when made, cites at least OI + one
  flow leg — and is always labeled [interpretation].

## Failure Handling

- Asset absent from positioning/flow feeds → those sections read "not
  covered in Lexfi feeds at this size", and conviction caps at Medium.
- `get_whale_alerts` / `get_onchain_flows` return only rotation/churn after
  filtering → report "no clean on-chain signal" — an honest null beats a
  forced read.
- Plan-gated tools absent (quant models, strategy holdings) → skip; note in
  Sources. Social highlights unavailable → narrative degrades to news
  sentiment only.
- Chart tool fails on the CoinGecko id → retry the obvious id form once,
  then deliver without price structure and say so.

## Example Prompts

- "What's the positioning in ETH right now — is it crowded?"
- "Are whales actually accumulating SOL or is that feed noise?"
- "Full structure read on bitcoin."
- "Is this LINK rally spot-led or leverage-driven?"
- "What does on-chain look like for AAVE?"
