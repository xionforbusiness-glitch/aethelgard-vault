---
title: "Karpathy's CLAUDE.md: 10 Coding Rules & Surgical Changes Protocol"
created: 2026-10-31
updated: 2026-10-31
type: concept
tags: [claudecode, karpathy, best-practices, devtools, surgical-changes, agent-discipline, prompts]
sources: [Andrej Karpathy, Nyanpasspassu/karpathy-claude-md, Wait What Did You Do Reel 2324132145065517]
confidence: high
contested: false
contradictions: []
---

# 🛡️ Karpathy's CLAUDE.md: The Surgical Changes Protocol

> **"I asked my AI to fix one typo. It opened a pull request with 214 files. While it was in there, it upgraded React, renamed the database, and deleted every comment."**  
> Behavioral guidelines distilled from **Andrej Karpathy's personal CLAUDE.md** to stop AI coding agents from overcomplicating code, bloating abstractions, and refactoring things they don't understand.

---

## ⚡ The Core Problem: "While I Was in There" Syndrome

AI agents don't stop at the assigned task. By default, they attempt to "improve" adjacent code, reformat styles, delete comments, and add speculative abstractions.

Karpathy’s 4 core guardrails:
1. **Surgical Changes:** Your diff must be as small as possible. Never touch what wasn't requested.
2. **Read Before Writing:** The biggest source of broken code is writing before reading existing patterns.
3. **Simplicity:** No speculative architecture. If the only reason something was abstracted is "just in case," revert it.
4. **Verification Gates:** Reproduce the bug first; verify with automated exit codes before concluding.

---

## 📋 The 10 Invariant Rules

| Rule | Principle | The Test |
| :--- | :--- | :--- |
| **1. Read Before Writing** | Copy existing naming, error handling & dependencies | Did you read the full file, or skim? |
| **2. Think Before Coding** | Surface assumptions & tradeoffs before implementing | Did you declare your interpretation explicitly? |
| **3. Simplicity** | Minimum code solving today's problem; zero speculation | Is this abstraction needed today? |
| **4. Surgical Changes** | Diff as small as possible; match exact style | Can you justify every single line by the prompt? |
| **5. Verification** | Gap between working code and assumed code is tests | Did you watch a test fail first? |
| **6. Goal-Driven Execution** | Set verifiable success criteria before coding | Does each step have a machine check? |
| **7. Debugging** | Root-cause analysis over guessing; check stack traces | Did you paper over an unexpected null? |
| **8. Dependencies** | Every dependency is permanent unowned code | Does the standard library already do this? |
| **9. Communication** | Surface uncertainty and tradeoffs clearly | Did you disclose edge-case risks? |
| **10. Halt on Runaway Refactors** | Stop immediately if an edit sprawls into other files | Did a 1-line fix touch 5 files? Stop. |

---

## 🔗 Related Notes & Vault Assets

* [[concepts/claude-code-boris-cherny-power-user-playbook|Claude Code Boris Cherny Playbook]]
* [[concepts/unlazy-anti-laziness-agent-skill|Unlazy: Completion Discipline Skill]]
* [[concepts/vibe-coder-security-fix-kit|Vibe Coder Security Fix Kit]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
