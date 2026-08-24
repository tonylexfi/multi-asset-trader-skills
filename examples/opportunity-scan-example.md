# Example — Multi-Asset Opportunity Scan

Produced from a **real Lexfi MCP session on 2026-08-24** (the repo's
bootstrap verification batch: crypto breadth, positioning, on-chain, FX,
sentiment — 10 calls). Equity broad-layer and calendar calls were not part
of that batch, so this example deliberately shows how the skill behaves
with **partial family coverage**: conviction capped, gaps named. Numbers
are genuine Lexfi output from that session.

```text
MULTI-ASSET OPPORTUNITY SCAN — 24 AUG 2026
Objective: general scan, no criteria          Mode: general
Market context: Crypto total cap $2.70T (+0.5% 24h), BTC dominance 59.1%
— majors bid (BTC +3.2%, ETH +2.3%) after a drawdown regime; dollar
news-tone mildly negative and drifting weaker.

1. BTC — Bitcoin                       Crypto · Conviction: Medium
   Why it surfaced:
   • Price/market action: +3.2% 24h to $79,753, leading a majors-wide bid
     (as-of 24 Aug)
   • Positioning/flows: 24h short liquidations $99.6M vs $45.5M longs —
     shorts forced 2:1; OI +5.2% 24h with price up = new longs entering;
     funding ~0.00% avg → rally not yet crowded
   • News/sentiment: 24 Aug counts 46 pos / 47 neu / 5 neg vs a
     negative-skewed mid-August (17–24 Aug trend improving)
   • Positioning/flows (on-chain): repeated large BTC transfers INTO
     Coinbase Institutional ($50–180M clips, 20–24 Aug) — two-sided
     reading, institutional custody activity [interpretation]
   Opposing: none found in fetched families; macro/liquidity leg NOT
   fetched this session (family unknown)
   Catalyst: none dated in this session (calendar not queried)
   Thesis (working): short-covering rally with room to become
   spot-led while funding stays flat [interpretation]
   Invalidation: funding >0.05% avg (crowding) with OI still rising, or
   sentiment proportion back below ~50% positive for 3+ days
   Key risks: high volatility regime; macro reversal untested (liquidity
   leg unverified); squeeze fuel partially spent after $100M covered

2. EUR/USD                             FX · Conviction: Low-Medium
   Why it surfaced:
   • Price/market action: 1.1543 → 1.1668 over two weeks (+1.1%), incl.
     a +0.87% single session on 19 Aug (weekend rows excluded)
   • News/sentiment: USD AI-FX ratio negative and drifting lower over the
     window (diff series −0.12) — dollar news tone weak, slow-moving
   Opposing: none found — but policy leg (rate probabilities, CB tone)
   NOT fetched this session (families unknown)
   Catalyst: unknown (CB calendar not queried)
   Thesis (working): dollar-softness continuation [interpretation —
   two families only; needs fx-macro-analysis before any conviction]
   Invalidation: AI-FX ratio trend flattening + EURUSD back below 1.1550
   Key risks: central-bank surprise (unassessed); thin-summer liquidity;
   single-session spike (19 Aug) may mark the move already made

3. NEAR — NEAR Protocol                Crypto · Conviction: Low
   Why it surfaced:
   • Price/market action: +3.5% 24h, top-quartile among majors
   • Positioning/flows: OI +8.6% 24h (largest OI build in the top-20
     snapshot, non-crypto perps excluded) with funding still ~0.01%
   Opposing: 24h long liquidations $617K vs shorts $257K — some longs
   already being punished intraday
   Catalyst: none identified
   Thesis (working): early leverage-led momentum, not yet crowded
   [interpretation]
   Invalidation: OI build reversing (Δ24h < 0) while price holds → longs
   exiting into strength
   Key risks: leverage-led moves unwind fast; narrative/on-chain families
   not fetched for NEAR; liquidity thinner than majors

Not surfaced but considered:
   ZEC — flat 24h after a big run; OI Δ24h negative → momentum family
   failed. PEPE — funding −0.06% (most negative in set) hints at squeeze
   setup, but no confirming family fetched → 1 family only.

Sources & data as-of: Lexfi MCP 24 Aug 2026 — coin markets, global
metrics, open interest, funding, liquidations, whale alerts, on-chain
flows, crypto news sentiment (BTCUSD), EURUSD daily, AI-FX ratio (USD).
Gaps: equity broad layer, macro/liquidity tools, calendars, prediction
markets not queried this session — conviction capped accordingly.
```

Two behaviors worth noticing, because they are the product:

1. **Conviction is capped by missing families**, and the output says which
   families are missing rather than padding with model knowledge.
2. **"Not surfaced but considered"** shows the funnel rejecting candidates
   (ZEC on momentum failure, PEPE on single-family evidence) — a scan that
   only ever promotes is not filtering.

Next step in the loop for entry #1: `asset-deep-dive` (fills macro +
narrative), then `thesis-builder`.
