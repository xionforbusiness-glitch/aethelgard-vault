---
title: "Top 10 Claude Code Power-User Workflows (Boris Cherny Creator Playbook)"
created: 2026-10-24
updated: 2026-10-24
type: concept
tags: [claudecode, anthropic, ai-coding, agentic-coding, boris-cherny, plan-mode, git-worktrees, best-practices]
sources: [Boris Cherny (Creator of Claude Code), Nick Saraev Reel 2995313617476965]
confidence: high
contested: false
contradictions: []
---

# ⚡ Top 10 Claude Code Power-User Workflows (Boris Cherny Creator Playbook)

> **"Boris Cherny created Claude Code at Anthropic. Here is exactly how the creator uses his own tool to build 3× to 5× faster."**  
> Operational playbook detailing the high-leverage mental models, keyboard shortcuts, multi-agent parallelism, and terminal discipline shared directly by Claude Code's author.

---

## 🧭 The Core Philosophy: "Draw the Map Before You Walk"

Most engineers open an AI coding agent and immediately start throwing implementation prompts at it. The model charges ahead, guesses file paths, misinterprets state, and creates compound bugs that take hours to untangle.

Boris's fundamental rule: **Never write a line of code until the plan is battle-tested.**

---

## 🛠️ The 10 Essential Power-User Practices

```
┌────────────────────────────────────────────────────────────────────────┐
│                   BORIS CHERNY'S CLAUDE CODE PROTOCOL                   │
├─────────────────────┬──────────────────────────────────────────────────┤
│ 1. Plan Mode First  │ Shift+Tab before touching code; iterate on specs │
│ 2. Parallel Agents  │ Run 3–5 simultaneous sessions via Git worktrees  │
│ 3. Automated Merge  │ Let Claude reconcile and rebase multi-branch work│
│ 4. Compact Context  │ Clear session or compact state after big passes  │
│ 5. Test Gates       │ Force runnable exit codes before declaring done  │
│ 6. CLAUDE.md Rules  │ Pin repository invariants, test scripts & lint   │
└─────────────────────┴──────────────────────────────────────────────────┘
```

### 1. Always Start in Plan Mode (`Shift + Tab`)
* **How it works:** Hitting `Shift + Tab` in Claude Code toggles **Plan Mode**.
* In Plan Mode, Claude is restricted from modifying files or executing destructive commands. It reads the codebase, diagrams dependency graphs, and outputs a concrete step-by-step RFC.
* **Why it matters:** Iterate on the plan *first*. Change requirements, debate edge cases, and refine the architecture while it costs zero code refactors. Only switch to execution mode when the plan is 100% green.

### 2. Multi-Session Parallelism (The 3×–5× Multiplier)
* Instead of running one sequential task, Boris runs **3 to 5 Claude Code sessions simultaneously** in separate terminal tabs or tmux panes.
* Assign each session a specific sub-system:
  * *Session 1:* Writing database schema migrations & seeders.
  * *Session 2:* Building backend API route handlers.
  * *Session 3:* Implementing frontend React components & styles.
  * *Session 4:* Writing end-to-end integration tests.

### 3. Git Worktrees & AI-Powered Merging
* Pair multi-session agents with **Git Worktrees** (`git worktree add ../feature-api feat/api`).
* Each agent operates on its own dedicated working tree without file collisions or git lock errors.
* When finished, invoke Claude in the primary repo to perform the rebase and resolve any merge conflicts automatically.

### 4. Continuous Context Discipline
* Long transcripts degrade model attention ("context rot").
* After a major milestone is tested and committed to Git, use `/clear` or `/compact` to drop stale tool outputs and start fresh with an updated prompt.

### 5. Runnable Verification Gates (Proof Over Apologies)
* Never accept *"I fixed that file, it should work now."*
* Always require an explicit verification command in your prompt:
  ```text
  Run `pytest tests/` or `npm test` and show me the clean exit code 0 before concluding.
  ```

### 6. The `CLAUDE.md` Institutional Memory
* Keep a high-signal `CLAUDE.md` in the root of your project specifying:
  * Exact build and test commands (`npm run build`, `pytest -v`).
  * Architecture conventions (e.g., "Use Next.js Server Actions, not raw API routes").
  * Forbidden patterns (e.g., "Never edit files inside `dist/` or `raw/` directly").

---

## 👑 The Master Boris-Style Implementation Prompt

```text
Activate Plan Mode. Do not modify any code yet.

Review the existing implementation of [Feature / Bug]. Produce a phased execution plan including:
1. Architectural analysis and files to touch.
2. Anticipated edge cases and regression risks.
3. Verification criteria: exact test command that must pass exit 0.

Wait for my review and explicit approval of the plan before proceeding to code.
```

---

## 🔗 Related Notes & Vault Assets

* [[concepts/unlazy-anti-laziness-agent-skill|Unlazy: Anti-Laziness & Runnable Gates Skill]]
* [[concepts/vibe-coder-security-fix-kit|The Vibe Coder's Security Fix Kit]]
* [[concepts/google-artemis-android-automation|Google ARTEMIS Android Automation]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
