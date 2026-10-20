---
title: "Unlazy: Anti-Laziness & Runnable Gates Skill for AI Coding Agents"
created: 2026-10-20
updated: 2026-10-20
type: concept
tags: [ai-agents, prompt-engineering, claude-code, codex, hermes-agent, completion-discipline, git-worktrees, devtools, skills]
sources: [Leonxlnx/unlazy GitHub (https://github.com/Leonxlnx/unlazy), Nathan Hodgson Facebook Reel 2020000352021571]
confidence: high
contested: false
contradictions: []
---

# 🛑 Unlazy: Anti-Laziness & Completion Discipline Skill (Leonxlnx/unlazy)

> **"Your AI tells you a job is done when it quietly skipped three steps. The technical term is 'partial compliance' or model laziness. Unlazy fixes it with runnable gates, Depth Trees, and parallel Git worktrees."**  
> Operational breakdown of **Unlazy**, an open-source agent skill designed for Claude Code, Codex, and Hermes Agent that enforces rigorous task completion by requiring empirical proof before declaring any job finished.

---

## ⚡ The Partial Compliance Problem

When users give AI coding agents complex or multi-step tasks (e.g., refactoring a database schema, building an end-to-end authentication pipeline, or running a 15-file migration), models routinely exhibit **premature completion**:
* The model implements the happy path, leaves edge cases unhandled, and concludes: *"All done! Everything is working."*
* The model generates TODO stubs, doesn't actually run unit tests, and hallucinates that tests passed.
* As context grows, earlier instructions are neglected due to attention dilution.

**Unlazy eliminates this by treating completion as a formal cryptographic/empirical contract: No task is marked complete without a green, runnable verification gate.**

---

## 🏗️ Core Architecture: The Depth Tree Method

```
┌────────────────────────────────────────────────────────────────────────┐
│                        UNLAZY EXECUTION PIPELINE                       │
├─────────────────────┬──────────────────────────────────────────────────┤
│ 1. Acceptance Ledger│ Writes explicit, testable criteria before coding │
│ 2. Depth Tree       │ Splits problem N layers deep (e.g., tree 3 or 5) │
│ 3. Runnable Gates   │ Unit test, terminal command, or regex check      │
│ 4. Git Worktrees    │ Dispatches sub-agents in parallel branches       │
│ 5. Empirical Proof  │ Output must match proof ledger before finishing  │
└─────────────────────┴──────────────────────────────────────────────────┘
```

### 1. Depth Tree Decomposition
Instead of handing the agent a monolithic prompt, Unlazy splits the task into a tree structure with explicit depth parameters:
```bash
/unlazy tree 3 "Refactor the payment module and verify all edge cases"
```
* Every leaf of the tree receives its own dedicated focus and time budget.
* The agent cannot jump to child tasks until parent constraints are verified.

### 2. Runnable Gates (The Gate Contract)
Every task requires a machine-checkable gate:
* A shell exit code (`pytest tests/test_payments.py` ➔ `exit 0`).
* A regex or schema verification check.
* If a gate fails, the agent is strictly prohibited from declaring success or apologizing—it must diagnose and patch until green.

### 3. Parallel Execution via Git Worktrees
For massive projects, Unlazy instructs the agent to spawn multiple sub-agents in parallel using **Git Worktrees**:
* Prevents file-lock collisions.
* Allows Agent A to write database migrations on branch `feat/db` while Agent B builds API route handlers on branch `feat/api`.

---

## 🚀 Installation & Setup

### 1. Universal Install via Skills CLI
```bash
npx skills add Leonxlnx/unlazy -g
```

### 2. Claude Code / Codex / Hermes Locations
```bash
# Claude Code:
~/.claude/skills/unlazy

# Hermes Agent:
~/.hermes/profiles/llm-wiki/skills/unlazy
```

---

## 🔗 Related Notes & Vault Assets

* [[concepts/earshot-audio-toolkit-for-ai-agents|Earshot: Audio Intelligence for AI Agents]]
* [[concepts/rea-reverse-engineer-anything-mcp|REA: Reverse Engineer Anything (MCP)]]
* [[concepts/vibe-coder-security-fix-kit|The Vibe Coder's Security Fix Kit]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
