# Contributing

Contributions welcome — especially trap-table updates with live evidence,
which are this library's compounding asset.

## Ground rules

1. **One skill (or one focused change) per PR.**
2. **Structural validation must pass:** `python3 scripts/validate.py`.
3. **All three test layers logged** for new/changed skills (see
   [docs/skill-development.md](docs/skill-development.md)): structural,
   live call-plan verification (append findings to `docs/test-log.md`),
   and behavioral RED→GREEN with a trigger-collision check.
4. **The product test in the PR description:** why would an informed
   retail trader prefer this skill over asking Claude directly?
5. **Tool knowledge lives in one place.** New tools or behavior notes go
   in the playbook/tool-map (marked [V] or [S]) — never documented inside
   a workflow skill.
6. **Respect budgets.** PRs that raise a skill's call budget must justify
   it against the funnel alternatives.
7. **Evidence discipline is not optional.** Any output format lacking
   thesis⇄invalidation pairing, as-of sourcing, or labeled interpretation
   will be rejected.

## What we're most likely to merge

- Trap-table entries with reproduction evidence (tool, args, payload
  surprise, mitigation).
- Live verification of tools currently marked [S].
- Behavioral test suites (RED baselines) for existing skills.
- Sharper trigger descriptions that fix real collision cases.
- Worked examples produced from real sessions (redact nothing that isn't
  private; keep as-of dates).

## What we won't merge

- Skills that are prompts in a trench coat (fail the product test).
- Near-duplicate triggers of an existing skill (propose a mode instead).
- Anything that executes trades, promises returns, or prescribes position
  sizes in account percentages.
- Untested changes, including "obviously fine" documentation edits to
  call plans.

## Dev quickstart

```bash
git clone <your fork>
cd multi-asset-trader-skills
python3 scripts/validate.py       # must pass before and after your change
./install.sh                      # symlink into ~/.claude/skills for live testing
```

Commit style: imperative subject, body explains the why; reference the
test-log entry for any call-plan change.
