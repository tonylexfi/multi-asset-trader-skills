# Product Strategy

## Positioning

**An AI research operating system for informed retail traders** — where
Claude reasons over Lexfi's financial intelligence through repeatable,
budget-aware workflows. One sentence: *institutional research discipline,
retail access, multi-asset by default.*

Explicitly not: a prompt pack, a stock screener with AI paint, a signals
service, or an autonomous trading bot.

## The user and their alternative

The user is an active retail trader / self-directed investor who already
understands valuation, momentum, positioning, and catalysts, but whose
current stack is a broker app, TradingView, X/Reddit, and scattered news.
Their realistic alternative to this library is *asking Claude directly* —
which produces fluent but unaccountable answers: no current data, invented
specifics, no repeatability, no discipline about what's fact vs narrative.

Every skill therefore has to beat plain-Claude on at least one of:

1. **Data advantage** — a call plan over live Lexfi tools the user wouldn't
   compose themselves, with known traps avoided.
2. **Process advantage** — funnel discipline, evidence ladder, adversarial
   challenge, delta-first monitoring.
3. **Contract advantage** — an output the user can act on and re-run:
   ranked candidates with named signals, theses with invalidation, diffs
   instead of re-summaries.

This is the repo's acceptance test (see docs/skill-development.md).

## Product philosophy

- **The loop is the product.** Discover → Why? → Research → Challenge →
  Thesis → Risk → Monitor. Skills are stations on this loop and compose
  through named output sections, not standalone gadgets.
- **Transparent convergence over scores.** An opportunity is a set of named
  signal families pointing the same way plus a catalyst. If the system
  can't say *why* something surfaced, it doesn't surface.
- **Budget-aware by design.** Lexfi meters MCP calls (Pro 1,000/mo,
  Pro Max 3,000/mo). Treat calls like a trader treats capital: a monthly
  budget supports ~60–200 skill runs, so every skill declares and defends
  its budget. Efficiency is a feature users can feel.
- **Honesty as a feature.** "Data unavailable", "no strong convergence
  today", and "not surfaced but considered" are outputs, not failures.
  A research tool that always finds 10 opportunities is a content mill.
- **Discipline in structure, not disclaimers.** Invalidation conditions,
  labeled interpretation, and asset-appropriate risk are enforced by output
  contracts; no boilerplate paragraphs.

## Differentiation vs the field

| Field norm | This library |
|---|---|
| Prompt collections per topic | Workflow contracts with MCP call plans |
| Single-asset (usually equities) | Equities + crypto + FX + macro, cross-asset natively |
| Schema-assumed data behavior | Live-verified trap table (18 documented traps) |
| Opaque "AI score" screeners | Named signal-family convergence |
| Bullish content bias | Adversarial challenger + mandatory invalidation |
| Unbounded tool usage | Per-skill call budgets + funnel discipline |

## Scope discipline

~16 flagship skills, deliberately. Additions must displace or clearly
extend the loop; near-duplicate triggers are rejected (see the merges
documented in docs/tier1-skills.md). Depth over breadth: better one
discovery skill that honestly reports weak convergence than six that
hallucinate abundance.

## Relationship to Lexfi

The library is open-source and Lexfi-primary but honest about plan gating:
skills state what Pro Max unlocks (transcripts, quant models, news
intelligence, CB transcripts) and degrade cleanly on lower plans. The repo
is a demand driver for Lexfi MCP precisely because it treats users' call
quotas with respect.
