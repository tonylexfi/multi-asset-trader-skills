# Tier 1 Skills — Selection & Specifications

Sixteen flagship workflow skills plus a two-skill core substrate. Selection
principle: each skill must pass the product test — *"would an informed
retail trader genuinely prefer this over asking Claude the same question in
a plain conversation?"* A skill passes when it encodes at least one of:
a call plan a user couldn't improvise (funnel discipline, verified traps),
a repeatable output contract, or an adversarial/quality mechanism.

Changes vs the initial brief:

- **Merged** `bull-bear-case` into `thesis-builder` as a scenario mode — a
  bull/base/bear matrix is an output shape of thesis building, not a
  separate workflow. This avoids two skills with colliding triggers.
- **Merged** momentum-discovery and theme-discovery into
  `opportunity-discovery` as named modes — same funnel, different signal
  weights. Dedicated skills would be trigger-collision hazards.
- **Added** `risk-reward-analysis` (in the brief's composable chain but not
  its Tier 1 list) — risk assessment is a core loop stage and deserves its
  own contract.
- **Added** the core substrate (`lexfi-trader-playbook`,
  `evidence-discipline`) — not workflow skills, but the shared routing
  table, trap list, and epistemic ladder every workflow depends on. This is
  the strongest pattern from the benchmark repos (a "core" layer) pushed
  further: ours is live-verified against the real MCP server.

## Core substrate (2)

| Skill | Role |
|---|---|
| `core/lexfi-trader-playbook` | Tool routing, call budgets, funnel discipline, 18 live-verified traps, plan-tier degradation |
| `core/evidence-discipline` | Fact→Signal→Interpretation→Thesis→Invalidation ladder, anti-hallucination, conflict handling, asset-appropriate risk |

## Workflow skills (16)

Spec fields: Purpose · Trigger · Assets · Inputs · MCP dependencies ·
Workflow · Output · Differentiation · Efficiency.

### 1. discovery/opportunity-discovery — FLAGSHIP
- **Purpose:** "Find me interesting opportunities right now" across stocks,
  crypto, and FX via transparent signal convergence.
- **Trigger:** open-ended opportunity requests; "what's interesting today";
  momentum or theme requests (modes).
- **Assets:** cross-asset (routes to per-class discovery when the user
  scopes to one class).
- **Inputs:** none required; optional criteria, count (default 5–10),
  horizon, asset classes, risk appetite.
- **MCP:** broad layer `get_market_overview` `get_sector_performance`
  `get_market_movers` `get_coin_markets` `get_crypto_global_metrics`
  `get_daily_dxy_index`; signal layer per candidate class (sentiment,
  positioning, flows); depth layer on shortlist (news, catalysts).
- **Workflow:** criteria → universe → 3-stage funnel → convergence scoring
  by named signal families → rank → explain "why surfaced" + risks +
  invalidation each.
- **Output:** ranked scan (the brief's MULTI-ASSET OPPORTUNITY SCAN shape).
- **Differentiation:** transparent convergence (named signals), never an
  opaque score; modes: general / momentum / theme.
- **Efficiency:** 12–18 calls hard cap; broad layer is 5–6 cheap snapshot
  calls.

### 2. discovery/stock-discovery
- **Purpose:** criteria-driven equity discovery (sentiment-vs-price,
  quality-improving, catalyst-rich…).
- **Trigger:** any "find stocks…" request.
- **Assets:** US-listed equities and ETFs (Lexfi coverage strongest there;
  say so).
- **MCP:** `get_market_movers` `get_sector_performance` breadth;
  `get_stocks_news_sentiment` `get_key_metrics` `get_earnings_surprises`
  `get_insider_trades` per shortlist; `get_stock_quote` batched.
- **Efficiency:** batch quotes; sentiment per-candidate only after breadth
  filter. 8–12 calls.

### 3. discovery/crypto-discovery
- **Purpose:** find crypto assets where market, positioning, on-chain, and
  narrative signals converge.
- **MCP:** `get_crypto_global_metrics` `get_coin_markets` (category filters)
  breadth; `get_funding_rates` `get_open_interest` `get_liquidations` one
  call each (cross-coin already); `get_crypto_news_sentiment` `get_whale_alerts`
  `get_onchain_flows` `get_chains_tvl` targeted.
- **Differentiation:** positioning tools are cross-coin snapshots — one call
  covers the whole universe; the skill exploits this for a cheap signal
  layer. All on-chain traps enforced.
- **Efficiency:** 8–12 calls.

### 4. discovery/fx-discovery
- **Purpose:** find FX pairs with macro/policy divergence or aligned
  rates+data+sentiment setups.
- **MCP:** `get_daily_dxy_index` `get_ai_fx_ratio` per G10 currency (cheap
  loop over ≤6), `get_rate_probabilities` per relevant CB,
  `get_cb_insights` on shortlist, `get_daily_fx_pair` for confirmation,
  `get_forex_news_sentiment`.
- **Differentiation:** divergence matrix built currency-by-currency (not
  pair-by-pair) — N currencies cover N² pairs.
- **Efficiency:** currency-level scan before pair-level depth. 10–14 calls.

### 5. discovery/catalyst-discovery
- **Purpose:** surface assets with dated upcoming catalysts and map
  catalyst → expected impact → direction → risk → timing.
- **MCP:** `get_economic_calendar` (1–2 day windows, iterated ≤3),
  `get_cb_calendar`, `get_ipo_calendar`, `get_mergers_acquisitions`,
  prediction-market tools for handicapping, `get_earnings_calls_by_ticker`
  for cadence inference.
- **Trap discipline:** economic-calendar payload bomb governs the design.
- **Efficiency:** 8–12 calls.

### 6. discovery/divergence-discovery
- **Purpose:** find price↔information divergences (positive sentiment +
  weak price; strong flows + flat price; weak fundamentals + strong price).
- **MCP:** paired evidence per divergence type: sentiment tools + price
  history; flows/positioning + price; fundamentals + price.
- **Differentiation:** both legs must be current (as-of check enforced);
  each divergence typed and explained, with the boring explanation (already
  priced, stale data) considered first.
- **Efficiency:** 10–14 calls.

### 7. research/asset-deep-dive
- **Purpose:** "research this" for ANY symbol — routes to the right
  evidence stack per asset class; also fast-mode "why did X move?".
- **Assets:** cross-asset router (equity/crypto/FX branches).
- **MCP:** per-class stacks as in the playbook routing table.
- **Output:** deep-dive dossier ending in FACT/SIGNAL/INTERPRETATION
  sections feeding thesis-builder.
- **Efficiency:** 6–10 calls; fast mode 2–4.

### 8. research/earnings-analysis
- **Purpose:** earnings deep read — surprises history, call insights,
  management tone shifts, market reaction, next-quarter setup.
- **MCP:** two-step transcript flow, `get_earnings_surprises`,
  `get_analyst_estimates` (ordering trap), `get_historical_prices` around
  report date (reaction ≠ today's quote trap), `get_stock_news`.
- **Plan-gating:** transcripts are Pro Max — degrade to surprises + news +
  estimates and say so.

### 9. research/crypto-intelligence
- **Purpose:** deep crypto read on one asset: structure, positioning,
  on-chain, narrative, macro sensitivity.
- **MCP:** `get_coin_market_chart` `get_coin_ohlcv` `get_open_interest`
  `get_funding_rates` `get_liquidations` `get_whale_alerts`
  `get_onchain_flows` `get_crypto_news_sentiment` + social highlights;
  `get_macro_credit_liquidity` for the liquidity leg.
- **Differentiation:** the on-chain trap set (custody rotations, churn
  pairs, non-crypto perps) is enforced here hardest.

### 10. research/fx-macro-analysis
- **Purpose:** two-sided macro dossier for a currency pair: policy paths,
  data momentum, sentiment, positioning proxies.
- **MCP:** `get_rate_probabilities` ×2, `get_cb_insights` ×2,
  `get_country_metrics` / `get_macro_forecasts` per economy,
  `get_daily_fx_pair`, `get_ai_fx_ratio` ×2, `get_forex_news_sentiment`.
- **Output:** side-by-side divergence table → net thesis direction.

### 11. thesis/thesis-builder
- **Purpose:** convert research into a falsifiable thesis using the
  standard contract (direction, horizon, evidence, catalysts,
  counter-thesis, risks, invalidation, confidence); bull/base/bear mode.
- **MCP:** mostly reuses in-context research; gap-fills only (≤4 calls).
- **Differentiation:** refuses to emit a thesis without invalidation
  conditions; confidence rules from evidence-discipline enforced.

### 12. thesis/thesis-challenger
- **Purpose:** adversarial red-team of a user's thesis — actively retrieve
  contradicting evidence and answer "what am I missing?".
- **MCP:** targeted retrieval AGAINST the thesis: contrary sentiment trend,
  positioning crowding, valuation, macro exposure, insider/whale behavior,
  upcoming event risk.
- **Differentiation:** the skill's stance is disconfirmation — it may
  conclude the thesis survives, but only after genuine attempts to break
  it; each challenge graded (Serious / Notable / Minor).

### 13. market/market-regime
- **Purpose:** one-screen cross-asset regime read: equity vol, breadth,
  crypto conditions, dollar, rates, liquidity — and what the regime favors.
- **MCP:** `get_daily_vix_index` `get_cnn_fear_greed_index`
  `get_market_overview` `get_sector_performance`
  `get_crypto_global_metrics` `get_fear_greed_index` `get_daily_dxy_index`
  `get_macro_yield_curve` `get_us_macro_regime`
  `get_macro_credit_liquidity` — one parallel batch.
- **Efficiency:** ~10 calls, all parallel, no depth layer.

### 14. market/macro-impact-analysis
- **Purpose:** trace a macro scenario or event through transmission chains
  to specific assets ("who benefits from falling rates?").
- **MCP:** scenario-relevant macro tools + `get_macro_asset_prices` +
  `get_rate_probabilities`; asset checks on the named beneficiaries only.
- **Differentiation:** explicit transmission-chain diagrams (rates → USD →
  EM; liquidity → BTC → risk appetite) with each link labeled
  fact/signal/interpretation.

### 15. risk/risk-reward-analysis
- **Purpose:** structure the risk side of a candidate trade: scenario
  ranges, asymmetry, position-sizing considerations, correlation/crowding
  checks, invalidation levels.
- **MCP:** price history for realized-vol context, positioning tools for
  crowding, catalyst check for event risk (≤6 calls).
- **Boundary:** frameworks and scenario math, never "risk X% of your
  account" prescriptions.

### 16. monitoring/watchlist-monitor
- **Purpose:** "what's changed?" across a saved watchlist — delta-first,
  never re-summarizing static facts; thesis status per asset when a thesis
  exists.
- **MCP:** batched quotes (`get_stock_quote` comma-list, `get_coin_markets`
  page), per-asset sentiment deltas, calendar look-ahead; positioning
  snapshot tools amortized across all crypto names.
- **Differentiation:** the output contract is the diff (↑/↓/→, Improving/
  Deteriorating/Stable, thesis Strengthening/Weakening/Unchanged).
- **Efficiency:** 8–14 calls for ≤10 assets via batching.

## Composability

```text
opportunity-discovery → asset-deep-dive → thesis-builder → thesis-challenger
        → risk-reward-analysis → watchlist-monitor
```

Each skill's output sections are named so the next skill can consume them
(discovery emits candidates with "why surfaced"; deep-dive emits the
evidence ladder; thesis-builder emits invalidation conditions that
watchlist-monitor tracks).
