# Getting Started

## 1. Prerequisites

- Claude with skills support (Claude Code, Claude Desktop, or claude.ai).
- A Lexfi plan with MCP access ([pricing](https://use.lexfi.ai/pricing)).
  Pro works; Pro Max unlocks transcripts, quant models, news intelligence.

## 2. Install the skills

```bash
git clone https://github.com/tonylexfi/multi-asset-trader-skills.git
cd multi-asset-trader-skills
./install.sh
```

`install.sh` symlinks every skill into `~/.claude/skills/`. Re-run after
`git pull`; pass `--copy` on systems where symlinks are inconvenient.

## 3. Connect Lexfi MCP

Follow [docs/lexfi-mcp.md](lexfi-mcp.md). Verify with:
*"Call get_market_overview and show me the result."*

## 4. First session (uses ~25–35 MCP calls total)

Walk the loop once:

1. *"What regime are we in?"* → market-regime (~10 calls, one batch)
2. *"Find me 5 interesting opportunities across stocks, crypto and FX."*
   → opportunity-discovery (12–18 calls)
3. Pick one: *"Why did this one surface? Quick version."* → asset-deep-dive
   fast mode (2–4 calls)
4. *"Research it properly."* → full deep dive (6–10 calls)
5. *"Challenge the bull case — what am I missing?"* → thesis-challenger
6. *"Write the thesis, bull/base/bear."* → thesis-builder (mostly reuses
   context)
7. *"Add it to my watchlist with that invalidation. What's changed?"*
   (tomorrow) → watchlist-monitor

## 5. Budget sense

| Plan | Calls/mo | Comfortable usage |
|---|---|---|
| Trial | 50 total | 1 regime read + 1 scan + 1 deep dive |
| Pro | 1,000 | ~2–4 full loop passes/week + daily monitoring |
| Pro Max | 3,000 | daily scans + monitoring + transcript-depth research |

Skills state their budget up front and will tell you when they skipped a
plan-gated source. If an output ever presents a number without a source, or
a thesis without an invalidation — that's a bug; please open an issue.

## 6. Where to go next

- [User journey](user-journey.md) — the loop in detail
- [Discovery framework](discovery-framework.md) — how ranking works
- [Skill development](skill-development.md) — build your own skill
