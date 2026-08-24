---
name: skill-name-kebab-case
description: Use when [triggering situations, symptoms, and example trader phrasings — NEVER a summary of the workflow. Third person. Under 500 chars.]
license: MIT
---

# Skill Title

**REQUIRED BACKGROUND:** core:lexfi-trader-playbook, core:evidence-discipline

## Purpose

One or two sentences: what the trader gets and why it beats asking the same
question in a plain conversation. If you can't say it in two sentences, the
skill is probably two skills.

## Supported Assets

Equities / Crypto / FX / Cross-asset — be explicit; name what is NOT
supported if a user would plausibly try it.

## Required Inputs

The minimum the trader must provide. Define defaults for everything you can
(universe, lookback windows, count of results). If input is missing, ask ONE
compact question — never interrogate.

## Optional Inputs

What sharpens the output if provided (horizon, risk tolerance, sectors to
exclude, existing positions).

## Lexfi MCP Calls

The call plan — the heart of an MCP-native skill:

- **Call budget** for this skill (see playbook budgets; justify if higher)
- Which tools, with which parameters (windows, limits, per_page, table subsets)
- What runs in ONE parallel batch vs what genuinely must be sequenced
- Funnel stages for discovery skills: broad (cheap) → candidates → shortlist
- Conditional calls ("only if X") and explicit skip conditions
- Which playbook traps apply (check lexfi-trader-playbook → Known Traps)

## Workflow

Numbered steps from inputs → funnel/analysis → ranking/synthesis. State the
materiality test if the skill triages. State where interpretation happens so
the evidence ladder is enforced by structure.

## Output Format

A purpose-built format for THIS workflow — not a generic brief. Show it as a
fenced block. Rules of thumb:

- Verdict / most-important-thing first
- "Why it surfaced" as named signals, never an opaque score
- Tables for ≥3 comparable items
- Thesis lines always paired with invalidation lines
- End with one compact "Sources & data as-of" line, including any gaps

## Quality Controls

3–6 checks specific to this skill (coverage guarantees, banned failure
modes, length caps). Generic rules live in core skills — don't repeat them.

## Failure Handling

What to do on tool errors, unresolvable symbols, empty results, partial
data, plan-gated tools. Default: report gaps honestly, deliver everything
else.

## Example Prompts

3–5 natural phrasings that should trigger this skill.
