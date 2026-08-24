# Skill Development Guidelines

How to create, test, evaluate, and improve skills in this library.

## The acceptance test

Before anything else, answer in writing:

> **Would an informed retail trader genuinely prefer this skill over asking
> Claude the same question in a plain conversation?**

A skill earns its place only through at least one of: a call plan the user
couldn't improvise (funnel + traps), a repeatable output contract, or a
quality mechanism (adversarial pass, delta-first diff, mandatory
invalidation). "It words the prompt nicely" fails the test.

## Authoring rules

1. Start from `templates/SKILL-template.md`. Every section, in order.
2. **Description = triggers only.** Third person, "Use when…", example
   phrasings, <500 chars. Never summarize the workflow — models follow
   description summaries instead of reading the body. Check trigger
   collisions against every existing skill's description.
3. **Tools come from the tool map.** If a tool isn't in
   `skills/core/lexfi-trader-playbook/references/tool-map.md`, either
   verify it live and add it there first (with [V]/[S] status), or don't
   use it. Never document a tool inside a workflow skill.
4. **Declare the call budget** and the funnel stages. Justify anything
   above playbook defaults.
5. **Check the trap table** and cite applicable traps by name.
6. **Output contract:** fenced format, most-important-thing first, named
   signals over scores, thesis ⇄ invalidation pairing, Sources & as-of
   line, plan-gating disclosures.
7. Failure handling: gaps reported, never silently filled.

## Testing (three layers, all required for a PR)

### Layer 1 — Structural: `python3 scripts/validate.py`

Checks frontmatter contract, name/directory match, trigger-style
description, required sections, core-skill references, and that every
`get_*`/`lexfi_*` token in a workflow skill exists in the tool map.

### Layer 2 — Live call-plan verification

Run the skill's call plan against real Lexfi MCP. Record in
`docs/test-log.md`: which calls ran, payload sizes, unit surprises,
ordering quirks, duplicate rows. **Any live behavior that contradicts the
schema becomes a trap-table entry** — that's the library's core asset
compounding (18 traps and counting; 11 found by testing, not reading).

### Layer 3 — Behavioral (RED → GREEN)

Skills are process documentation; test them like code, with the failing
test first:

- **RED (baseline):** run the skill's example prompts in a fresh session
  WITHOUT the skill. Save outputs. Document the failures the skill exists
  to fix (invented data, no invalidation, unbounded calls, opaque
  reasoning) — verbatim.
- **GREEN:** same prompts WITH the skill. Verify each documented baseline
  failure no longer occurs, budget respected, output contract honored.
- **Collision check:** run 3–5 prompts that *shouldn't* trigger this skill
  (they belong to siblings) and confirm the right skill wins. Discovery
  siblings are the highest-risk surface.
- **REFACTOR:** every workaround the model finds (skipping the funnel,
  "just one more call", unlabeled interpretation) gets an explicit counter
  in the skill (Quality Controls / Red Flags), then re-test.

## Evaluation rubric (PR review)

| Dimension | Failing smell |
|---|---|
| Trigger precision | fires on a sibling's prompts, or never fires |
| Budget honesty | "as needed" instead of a number; funnel skipped |
| Evidence ladder | interpretation in fact grammar; missing invalidation |
| Trap compliance | uses a trapped tool without the mitigation |
| Degradation | assumes Pro Max; silent gaps |
| Output contract | prose blob instead of the contract; no as-of line |
| Product test | plain Claude does it just as well |

## Improving existing skills

- Bug reports: any output with an unsourced number, a thesis without
  invalidation, or a busted budget is a defect — file with the transcript.
- Trap contributions: live evidence (tool, args, surprising payload) +
  the mitigation sentence.
- Keep skills lean: heavy reference goes to `references/` files loaded on
  demand; SKILL.md should stay scannable.
- One skill per PR, with all three test layers logged. Never batch
  untested skills.
