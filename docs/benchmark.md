# Competitive Benchmark

Three reference repositories studied for architecture, conventions, and
usability. Patterns adopted, adapted, or rejected — content not copied.

## anthropics/financial-services

**What it is:** Anthropic's official financial-services library: agent
plugins + vertical skill bundles (financial-analysis, IB, equity research,
PE, wealth) + partner MCP connectors, with slash commands and managed-agent
deployment.

**Strongest patterns (adopted/adapted):**
- **A core substrate vertical** everything else depends on
  (financial-analysis) → our `skills/core/` (playbook + evidence
  discipline), pushed further: ours is live-verified against the MCP server.
- **Skill + command duality** — skills auto-trigger, commands invoke
  explicitly → our trigger-first descriptions with example prompts serve
  both paths.
- **Centralized MCP configuration** → our single playbook/tool-map as the
  one place tool knowledge lives; workflow skills reference it instead of
  re-documenting tools.
- **Self-contained plugins, no build step** → plain markdown everywhere.

**Weaknesses we avoid:** frontmatter/trigger conventions undocumented (we
ship a template + validator); skill-sync drift across bundled copies (we
keep one copy per skill); no graceful degradation story when a connector is
missing (our skills specify fallbacks per plan tier).

## himself65/finance-skills

**What it is:** community marketplace of ~35 finance skills in plugin
groups (market-analysis, social readers, data providers), multi-adapter
(OpenCLI + MCP), npm-installable.

**Strongest patterns:**
- **Marketplace packaging & granular install** → our category layout +
  `install.sh`; single-library install because traders want the whole loop,
  not à la carte fragments.
- **MCP-first with fallbacks** per data provider → generalized into our
  per-skill Fallbacks/plan-gating sections.
- **Perspective-based analysis** (one skill, multiple stakeholder lenses)
  → echoed in thesis-challenger's multiple attack lenses.

**Weaknesses we avoid:** no documented SKILL.md standard; skills organized
by data source rather than by user workflow (we organize by loop stage —
users think "find me opportunities", not "query provider X"); no efficiency
or rate-limit discipline.

## JoelLewis/finance_skills

**What it is:** 91-skill advisor-oriented library in dependency-layered
plugins (core math → wealth-management → advisory-practice), with worked
examples and Python reference implementations.

**Strongest patterns:**
- **Layered dependency graph** (core concepts feed specialized skills) →
  our REQUIRED BACKGROUND convention pointing every workflow at the core
  substrate.
- **Cross-References sections** creating a navigable graph → our
  composability contract (named output sections consumed by the next
  skill), which is stronger than links: skills compose at the data level.
- **Consistent per-skill template** with Purpose/When to Use/Pitfalls →
  our SKILL-template.md.
- **Worked examples** → our `examples/` built from real, current Lexfi data.

**Weaknesses we avoid:** 91 skills dilute quality and create trigger
collisions (we cap at ~16 and document merges); knowledge-heavy but
data-layer-free (skills teach formulas but fetch nothing — ours are
MCP-native); no validation tooling (we ship `scripts/validate.py`).

## Net design position

From Anthropic: the core-substrate + bundle architecture and command
ergonomics. From himself65: marketplace packaging and MCP-first pragmatism.
From JoelLewis: layered dependencies, template rigor, worked examples.
Added on top, found in none of them: **live-verified data traps, per-skill
call budgets with funnel discipline, transparent signal-convergence
discovery, mandatory invalidation, and an adversarial challenger stage.**
