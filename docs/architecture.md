# Architecture

## Multi-asset model

Four surfaces, one loop. Asset classes are not silos — they are evidence
domains with different signal families, joined by macro transmission.

| Class | Universe | Primary signal families (Lexfi) |
|---|---|---|
| Equities | US stocks, ETFs, sectors | price/breadth, fundamentals, earnings & management tone, news sentiment, smart money (insider/congress/13F), prediction markets |
| Crypto | BTC, ETH, majors, tokens, chains | price/dominance, derivatives positioning (funding/OI/liquidations), on-chain (whales, exchange flows, TVL), narrative (news + social), crypto ETFs |
| FX | G10 pairs, crosses, liquid EM | policy paths (rate probabilities, CB tone), macro data momentum, news-derived currency strength, price history |
| Macro / cross-asset | rates, inflation, liquidity, USD, commodities | regime probabilities, yield curve, credit & liquidity, uncertainty indices, calendars |

### How the classes interact

Macro is the connective tissue; skills traverse these chains explicitly,
labeling each link on the evidence ladder:

```text
Fed expectations → USD → US equities → EM assets
Global liquidity → BTC/crypto → risk appetite → equities
Rates → financial conditions → sector rotation → equity leadership
Dollar regime → commodity currencies → commodity-linked equities
Crypto/equity correlation regime → diversification validity
```

Concretely: `market-regime` reads all four surfaces in one batch;
`macro-impact-analysis` walks a chain from a scenario to named assets;
`opportunity-discovery` scans all surfaces and lets convergence decide
where attention goes; FX skills difference two economies' evidence stacks.

## Repository layout

```text
multi-asset-trader-skills/
├── README.md · LICENSE · CONTRIBUTING.md · SECURITY.md · install.sh
├── skills/
│   ├── core/               ← substrate: playbook (+ tool-map reference), evidence-discipline
│   ├── discovery/          ← opportunity, stock, crypto, fx, catalyst, divergence
│   ├── research/           ← asset-deep-dive, earnings, crypto-intel, fx-macro
│   ├── thesis/             ← builder, challenger
│   ├── market/             ← market-regime, macro-impact-analysis
│   ├── risk/               ← risk-reward-analysis
│   └── monitoring/         ← watchlist-monitor
├── docs/                   ← strategy, benchmark, architecture, journey,
│                             discovery-framework, tier1 specs, lexfi-mcp,
│                             getting-started, skill-development, test-log
├── examples/               ← worked outputs from real Lexfi data
├── templates/              ← SKILL-template.md
└── scripts/                ← validate.py
```

Deviations from the original brief's sketch, and why:

- **`skills/core/` added.** The strongest benchmark pattern (Anthropic's
  core vertical, JoelLewis's core layer): tool knowledge and epistemic
  rules live once, referenced everywhere. Without it, 16 skills each carry
  a drifting copy of tool lore.
- **`catalysts/`, `macro/`, `portfolio/`, `communication/` folded in.**
  Catalyst work is discovery (`discovery/catalyst-discovery`); macro skills
  sit with market (`market/`); portfolio-monitoring is `monitoring/`;
  communication is a property of every output contract, not a category.
  Empty one-skill categories are navigation debt.
- **Flat two-level nesting** (`skills/<category>/<skill>/SKILL.md`) — no
  plugin manifests or build steps. `install.sh` symlinks skill dirs into
  `~/.claude/skills/`; marketplace packaging can be layered on later
  without moving files.

## Skill anatomy

Every workflow skill follows `templates/SKILL-template.md`:

- **Frontmatter** — `name` (= directory), trigger-only `description`
  (never a workflow summary — summaries get followed instead of the body),
  `license`.
- **REQUIRED BACKGROUND** — the two core skills, always.
- **Lexfi MCP Calls** — budget, staged funnel, parallel batches vs true
  sequences, applicable traps by name, plan-gated fallbacks.
- **Output contract** — fenced format; named sections the next loop stage
  consumes; theses paired with invalidation; Sources & as-of line.
- **Quality Controls / Failure Handling / Example Prompts.**

## Composition contract

Skills pass work forward through named output sections, not shared state:

```text
opportunity-discovery   emits → candidates with "Why it surfaced" + working thesis
asset-deep-dive         consumes a candidate; emits → FACT/SIGNAL/INTERPRETATION
thesis-builder          consumes the ladder; emits → thesis + INVALIDATION CONDITIONS
thesis-challenger       consumes a thesis; emits → graded challenges + verdict
risk-reward-analysis    consumes a thesis; emits → scenarios + invalidation levels
watchlist-monitor       consumes assets + invalidation conditions; emits → deltas + thesis status
```

The conversation is the bus: a user can enter the loop anywhere, and each
skill states which prior sections it will reuse instead of re-fetching.

## Efficiency architecture

Lexfi plans meter calls (Pro 1,000/mo, Pro Max 3,000/mo). Three mechanisms
keep skills inside budget:

1. **Funnel discipline** (playbook): broad layer uses only whole-market
   snapshot tools; depth is earned by passing filters.
2. **Cross-universe tools exploited**: funding/OI/liquidations/coin-markets
   cover the whole crypto universe in one call each; `get_stock_quote`
   batches a full watchlist per call; `get_ai_fx_ratio` per *currency*
   covers all its pairs.
3. **Budgets in the contract**: every skill declares its cap; validate.py
   checks the section exists; reviewers reject budget creep.
