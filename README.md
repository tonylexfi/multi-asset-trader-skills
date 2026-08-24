# Multi-Asset Trader Skills

**The open-source AI research toolkit for informed retail traders.**

A curated library of Claude Skills that turns Claude + [Lexfi MCP](https://use.lexfi.ai)
into a research operating system for self-directed market participants —
across **stocks, crypto, FX, and macro**.

```text
DISCOVER → WHY? → RESEARCH → CHALLENGE → THESIS → RISK → MONITOR
```

## What it is

Not a collection of prompts. Each skill is a repeatable research workflow
with a specified data plan: which Lexfi tools to call, in what order, within
what call budget, with which known data traps avoided, and what the output
must contain (every thesis ships with its invalidation condition).

- **Claude** provides reasoning and synthesis.
- **Lexfi MCP** provides the financial intelligence: market data, news
  sentiment, earnings-call insights, macro indicators, central-bank
  communication, insider/congressional/superinvestor activity, prediction
  markets, crypto on-chain and derivatives positioning, FX intelligence.
- **Skills** provide the workflows that make the two reliable together.

## Who it's for

Informed retail traders and self-directed investors — people who know what
earnings surprises, funding rates, macro regimes, and invalidation levels
are, but don't have a Bloomberg terminal or a research desk. Not optimized
for complete beginners, and not an autonomous trading system: these are
research and decision-support workflows. Nothing here executes trades or
guarantees outcomes.

## Try it

```text
"Find 5 interesting opportunities across stocks, crypto and FX today."
"Find stocks where fundamentals are improving but price hasn't reacted."
"Find crypto assets with improving on-chain activity and sentiment."
"Find FX pairs with the strongest macro divergence."
"Why did BTC move today?"
"Challenge my thesis on NVDA."
"What's changed across my watchlist this week?"
"Find assets that could benefit from falling rates."
"Find upcoming catalysts worth watching."
"Build a bull/base/bear case for this trade."
```

## The skills

**Core substrate** (loaded by everything)
| Skill | What it holds |
|---|---|
| [lexfi-trader-playbook](skills/core/lexfi-trader-playbook/SKILL.md) | Tool routing across 4 asset classes, call budgets, funnel discipline, 18 live-verified data traps |
| [evidence-discipline](skills/core/evidence-discipline/SKILL.md) | The Fact → Signal → Interpretation → Thesis → Invalidation ladder |

**Discovery**
| Skill | Ask it |
|---|---|
| [opportunity-discovery](skills/discovery/opportunity-discovery/SKILL.md) | "Find me opportunities right now" (cross-asset, momentum & theme modes) |
| [stock-discovery](skills/discovery/stock-discovery/SKILL.md) | "Find stocks with improving sentiment and weak price" |
| [crypto-discovery](skills/discovery/crypto-discovery/SKILL.md) | "Find tokens where whales are buying but price hasn't moved" |
| [fx-discovery](skills/discovery/fx-discovery/SKILL.md) | "Find pairs where central-bank paths are diverging" |
| [catalyst-discovery](skills/discovery/catalyst-discovery/SKILL.md) | "What catalysts are coming up worth watching?" |
| [divergence-discovery](skills/discovery/divergence-discovery/SKILL.md) | "Where are price and information disagreeing?" |

**Research**
| Skill | Ask it |
|---|---|
| [asset-deep-dive](skills/research/asset-deep-dive/SKILL.md) | "Research this" / "Why did X move?" — any asset class |
| [earnings-analysis](skills/research/earnings-analysis/SKILL.md) | "What did the quarter really say?" |
| [crypto-intelligence](skills/research/crypto-intelligence/SKILL.md) | "Full read on SOL: positioning, on-chain, narrative" |
| [fx-macro-analysis](skills/research/fx-macro-analysis/SKILL.md) | "EUR/USD macro dossier, both sides" |

**Thesis & Risk**
| Skill | Ask it |
|---|---|
| [thesis-builder](skills/thesis/thesis-builder/SKILL.md) | "Turn this into a thesis" / "bull, base, bear case" |
| [thesis-challenger](skills/thesis/thesis-challenger/SKILL.md) | "I'm bullish on NVDA because… what am I missing?" |
| [risk-reward-analysis](skills/risk/risk-reward-analysis/SKILL.md) | "What's the downside? Is this asymmetric?" |

**Market & Monitoring**
| Skill | Ask it |
|---|---|
| [market-regime](skills/market/market-regime/SKILL.md) | "Risk-on or risk-off right now?" |
| [macro-impact-analysis](skills/market/macro-impact-analysis/SKILL.md) | "What does a Fed cut mean for my assets?" |
| [watchlist-monitor](skills/monitoring/watchlist-monitor/SKILL.md) | "What's changed across my watchlist?" |

## Why Lexfi

Skills are only as good as their data layer. Lexfi MCP exposes, through one
server: equities market data and fundamentals; earnings-call AI insights;
news sentiment across stocks/crypto/FX/macro; central-bank hawk/dove
indices and rate probabilities; macro regimes, forecasts, and liquidity;
insider, congressional, institutional, and superinvestor activity;
prediction markets; crypto derivatives positioning (funding, OI,
liquidations), whale alerts, exchange flows, and chain TVL; FX histories
and a news-derived currency strength ratio.

Plans differ ([pricing](https://use.lexfi.ai/pricing)): every skill declares
its MCP dependencies and degrades gracefully when a tool is plan-gated or
unavailable — gaps are reported, never silently filled.

## Why this is different

1. **Live-verified data layer.** The playbook's trap table comes from
   running these tools against the real server — not from reading schemas.
   (Examples: the crypto whale feed repeats custody rotations that look
   like whale signals; `get_open_interest` includes gold, oil, and
   tokenized-equity perps; FX histories include thin weekend rows;
   `get_forecast` is literally the weather.)
2. **Call-budget engineering.** Lexfi plans meter MCP calls. Every skill
   has a budget and a funnel: filter cheaply → shortlist → deep-dive.
   A cross-asset scan costs 12–18 calls, not hundreds.
3. **Transparent convergence, no black-box scores.** Opportunities surface
   because named signal families align; every entry says why it surfaced,
   what opposes it, and what invalidates it.
4. **Built-in research discipline.** The evidence ladder
   (Fact → Signal → Interpretation → Thesis → Invalidation) is enforced by
   output structure, not by disclaimer paragraphs.
5. **Composable loop.** Discovery output feeds deep-dive; deep-dive feeds
   thesis-builder; thesis-challenger attacks it; watchlist-monitor tracks
   the invalidation conditions you committed to.

## Install

```bash
git clone https://github.com/tonylexfi/multi-asset-trader-skills.git
cd multi-asset-trader-skills
./install.sh          # symlinks skills into ~/.claude/skills
```

Then connect Lexfi MCP (see [docs/lexfi-mcp.md](docs/lexfi-mcp.md)) and ask:
*"Find me opportunities."*

Requirements: Claude (Code, Desktop, or claude.ai with skills), a Lexfi
plan with MCP access. Works partially without Pro Max — skills tell you
what they skipped.

## Docs

- [Getting started](docs/getting-started.md)
- [Product strategy](docs/product-strategy.md) · [Competitive benchmark](docs/benchmark.md)
- [Architecture](docs/architecture.md) · [User journey](docs/user-journey.md) · [Discovery framework](docs/discovery-framework.md)
- [Tier 1 skill specs](docs/tier1-skills.md) · [Lexfi MCP guide](docs/lexfi-mcp.md)
- [Skill development & testing](docs/skill-development.md) · [Test log](docs/test-log.md)

## Compliance

Research and decision-support tools, not investment advice and not an
autonomous trading system. Skills never execute trades, never guarantee
returns, always separate facts from interpretation, and always state
uncertainty and invalidation. Verify anything important before acting on it.

## License

MIT — see [LICENSE](LICENSE). Contributions welcome: [CONTRIBUTING.md](CONTRIBUTING.md).
