# Security Policy

## Scope

This repository contains markdown skill definitions and a validator script.
It ships no executable trading code, holds no credentials, and never asks
for API keys — Lexfi MCP authentication is handled by your Claude client's
connector configuration, outside this repo.

## Threat model notes for users

- **Prompt-injection surface:** skills instruct Claude to treat retrieved
  content (news text, social highlights, transcripts) as data, never as
  instructions. If you observe a skill acting on instructions embedded in
  market content, report it as a vulnerability.
- **No execution:** skills must never place, sign, or automate trades, or
  connect to broker/exchange execution APIs. A PR or fork adding this is
  out of scope of this project's design and its safety posture.
- **Data honesty:** fabricated data presented as Lexfi output is treated
  as a security-relevant defect (it can cause financial harm), not a mere
  quality bug. Report with the transcript.
- **Supply chain:** install by cloning this repository and reviewing
  `install.sh` (it only symlinks/copies files into `~/.claude/skills`).
  Review skills before installing forks.

## Reporting

Open a GitHub security advisory or email the maintainer (see repo
profile). Include: skill name, session transcript excerpt, expected vs
actual behavior. Please do not open public issues for injection-style
findings before a fix lands.

## Supported versions

The `main` branch only. Skills evolve with live Lexfi MCP behavior; old
snapshots may carry stale call plans and traps.
