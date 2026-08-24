#!/usr/bin/env python3
"""Structural validator for multi-asset-trader-skills.

Checks every skills/**/SKILL.md for:
  - YAML frontmatter with name, description, license
  - name matches directory, kebab-case
  - description: third-person trigger style ("Use when"), <500 chars,
    no workflow-summary tells
  - required sections present (workflow skills)
  - REQUIRED BACKGROUND references both core skills (workflow skills)
  - every Lexfi tool token used in a workflow skill exists in the tool map
  - call-budget statement present in the MCP section

Exit 0 on pass, 1 on any failure. Run before every commit.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
TOOL_MAP = SKILLS / "core" / "lexfi-trader-playbook" / "references" / "tool-map.md"

CORE_SKILLS = {"lexfi-trader-playbook", "evidence-discipline"}
REQUIRED_SECTIONS = [
    "## Purpose",
    "## Lexfi MCP Calls",
    "## Workflow",
    "## Output Format",
    "## Quality Controls",
    "## Failure Handling",
    "## Example Prompts",
]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOOL_TOKEN = re.compile(r"\b((?:get|list|search|lexfi)_[a-z0-9_]+)\b")

errors: list[str] = []


def err(path: Path, msg: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def parse_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def known_tools() -> set[str]:
    tools = set(TOOL_TOKEN.findall(TOOL_MAP.read_text()))
    # Playbook may mention tools too; both files are the knowledge layer.
    playbook = SKILLS / "core" / "lexfi-trader-playbook" / "SKILL.md"
    tools |= set(TOOL_TOKEN.findall(playbook.read_text()))
    return tools


def main() -> int:
    if not TOOL_MAP.exists():
        print(f"FATAL: tool map missing at {TOOL_MAP}")
        return 1
    tools = known_tools()

    skill_files = sorted(SKILLS.glob("*/*/SKILL.md"))
    if len(skill_files) < 18:
        errors.append(f"expected >= 18 skills, found {len(skill_files)}")

    for path in skill_files:
        text = path.read_text()
        fm = parse_frontmatter(text)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        dirname = path.parent.name
        is_core = dirname in CORE_SKILLS

        if not fm:
            err(path, "missing frontmatter")
            continue
        if name != dirname:
            err(path, f"frontmatter name '{name}' != directory '{dirname}'")
        if not KEBAB.match(name or "x"):
            err(path, f"name not kebab-case: '{name}'")
        if fm.get("license") != "MIT":
            err(path, "license must be MIT")
        if not desc.startswith("Use when"):
            err(path, "description must start with 'Use when'")
        if len(desc) > 520:
            err(path, f"description too long ({len(desc)} chars)")
        for tell in ("then ", "step 1", "first it", "workflow:"):
            if tell in desc.lower():
                err(path, f"description smells like a workflow summary ('{tell.strip()}')")

        if not is_core:
            if "REQUIRED BACKGROUND" not in text:
                err(path, "missing REQUIRED BACKGROUND line")
            else:
                for core in CORE_SKILLS:
                    if core not in text:
                        err(path, f"REQUIRED BACKGROUND must reference {core}")
            for section in REQUIRED_SECTIONS:
                if section not in text:
                    err(path, f"missing section '{section}'")
            mcp = text.split("## Lexfi MCP Calls", 1)[-1].split("\n## ", 1)[0]
            if not re.search(r"[Bb]udget", mcp):
                err(path, "Lexfi MCP Calls section must state a call budget")
            for tok in sorted(set(TOOL_TOKEN.findall(text))):
                if tok not in tools:
                    err(path, f"unknown Lexfi tool '{tok}' (not in tool map)")

    if errors:
        print(f"FAIL — {len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS — {len(skill_files)} skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
