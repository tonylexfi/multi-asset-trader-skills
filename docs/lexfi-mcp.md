# Lexfi MCP Guide

## Connecting

Lexfi MCP is a hosted MCP server; get access at
[use.lexfi.ai](https://use.lexfi.ai) (MCP access is included in every paid
plan). Add the server to your Claude surface:

- **Claude Code / Desktop:** add the Lexfi server per the instructions in
  your Lexfi dashboard (custom connector / `.mcp.json` entry).
- **claude.ai:** Settings → Connectors → add Lexfi.

Sanity check after connecting — ask Claude:
*"Call get_market_overview and show me the raw result."*

## Plans and what skills expect

| Plan | MCP calls | Gated capabilities |
|---|---|---|
| Trial (7 days) | 50 total | no transcripts, quant models, news intelligence, CB transcripts, strategy holdings |
| Pro ($20/mo) | 1,000/mo | same gates as Trial |
| Pro Max ($50/mo) | 3,000/mo | everything unlocked |

Implications built into the skills:

- **Call budgets.** At Pro, 1,000 calls ≈ 60–120 skill runs. Skills declare
  budgets (quick answers 2–4, deep dives 6–10, scans 12–18) and use funnel
  discipline. On Trial, prefer quick modes and market-regime; a single
  cross-asset scan is ~30% of the whole trial quota.
- **Plan-gated degradation.** Earnings-call insights, CB conference
  transcripts, quant model outputs, and news intelligence are Pro Max.
  Every skill that uses them names a fallback (surprises + news instead of
  transcripts; CB insights indices instead of full transcripts) and reports
  what was skipped.
- **Capability discovery.** When unsure what a session exposes, skills use
  `list_market_datasets` / a cheap probe call rather than assuming.

## The knowledge layer

Tool routing, budgets, and the live-verified trap table live in ONE place:

- [skills/core/lexfi-trader-playbook/SKILL.md](../skills/core/lexfi-trader-playbook/SKILL.md)
- [tool-map.md](../skills/core/lexfi-trader-playbook/references/tool-map.md)
  — per-tool notes, each marked **[V]** live-verified or **[S]**
  schema-reviewed.

Highlights every user should know before trusting outputs:

- `get_forecast` is **weather**. `get_fear_greed_index` is **crypto**;
  equities use `get_cnn_fear_greed_index`. `get_etf_flows` is crypto spot
  ETFs only.
- `get_open_interest` includes gold/oil/tokenized-equity perps; crypto
  claims require filtering.
- `get_whale_alerts` repeats custody rotations; `get_onchain_flows` pairs
  market-maker churn — net and dedupe before reading direction.
- `get_economic_calendar` is a payload bomb; 1–2 day windows only.
- FX daily histories contain thin weekend rows; `get_ai_fx_ratio` is
  slow-moving with stale-day repeats.

When live behavior contradicts a schema, the trap table wins — and a PR
updating it (with evidence) is the most valuable contribution this repo
accepts (see docs/test-log.md for the verification record).

## Freshness & conflicts

Skills report as-of dates next to figures, treat data older than its
natural cadence as stale (quotes: minutes; sentiment: a day; 13F/congress:
weeks — disclosure-lagged by nature), and handle source conflicts by
reporting both sides with an explicit weighting, never averaging into
false neutrality.
