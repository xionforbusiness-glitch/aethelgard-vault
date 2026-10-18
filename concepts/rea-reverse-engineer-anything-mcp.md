---
title: "REA: Reverse Engineer Anything (AI Agent MCP for Binary & App Decompilation)"
created: 2026-10-18
updated: 2026-10-18
type: concept
tags: [security, reverse-engineering, ai-agents, mcp, binary-analysis, hopper, ghidra, decompiler, appsec, offensive-security]
sources: [morluto/rea GitHub (309k+ stars), Tech Secured Facebook Reel 2682011585592823]
confidence: high
contested: false
contradictions: []
---

# 🕵️ REA: Reverse Engineer Anything (morluto/rea)

> **"See a feature you like in any software or binary. Understand how it works and clone its logic down to the assembly level using AI agents."**  
> Operational technical brief on **REA (Reverse Engineer Anything)**—the viral Model Context Protocol (MCP) tool with over **300,000 GitHub stars** that bridges disassemblers (Hopper, Ghidra) directly with AI coding agents (Claude Code, Codex, Hermes).

---

## ⚡ What Is REA?

**Repository:** `https://github.com/morluto/rea` (Homepage: `https://rea.tools`)  
**Core Thesis:** Traditional reverse engineering requires hours of manually tracing disassembly graphs, decompiled C pseudocode, and API hooks in Ghidra/IDA Pro/Hopper. **REA turns this into an automated conversational pipeline for AI agents.**

REA implements an **MCP (Model Context Protocol)** server that lets LLMs directly drive disassemblers, inspect native binaries, trace API hooks, extract cryptographic algorithms, and reconstruct the business logic of proprietary software (Clean-room behavioral cloning).

---

## 🛠️ Key Capabilities & Architecture

```
┌────────────────────────────────────────────────────────┐
│             AI AGENT (Claude Code / Codex)             │
└──────────────────────────┬─────────────────────────────┘
                           │ MCP Protocol
┌──────────────────────────▼─────────────────────────────┐
│                 REA MCP SERVER (morluto/rea)            │
├──────────────────────────┬─────────────────────────────┤
│ • Hopper Python Bridge   │ • Ghidra Headless Bridge    │
│ • Runtime API Hooking    │ • Web / Electron Inspector  │
└──────────────────────────┴─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│      TARGET SOFTWARE (Native .exe / Mach-O / Web)      │
└────────────────────────────────────────────────────────┘
```

1. **Native Disassembler Bridges:**
   * Direct Python IPC bridge into **Hopper Disassembler** and **Ghidra**.
   * The AI agent can query functions (`rea.get_function_cfg`), read data segments (`__const`, `__data`), trace xrefs, and request automated decompilation passes.
2. **Behavioral Cloning (Clean-Room Design):**
   * Instead of copying copyrighted source code, REA inspects how proprietary software handles state, network payloads, file formats, or proprietary encryption, then generates standard, idiomatic open-source code in Python, TypeScript, or Rust.
3. **Cross-Platform Target Inspection:**
   * Desktop binaries: Windows PE (`.exe`, `.dll`), macOS Mach-O, Linux ELF.
   * Mobile / Web: React Native apps, Electron apps, browser-based SPA obfuscated code.

---

## 🚀 How It Works (Quick Start)

### 1. Installation
```bash
npx rea-agents setup
```

### 2. Integration with AI Coding Agents (Claude Code / Codex / Hermes)
Add REA to your MCP configuration (`claude.json` or `hermes` tools):
```json
{
  "mcpServers": {
    "rea": {
      "command": "npx",
      "args": ["-y", "rea-agents", "mcp"]
    }
  }
}
```

### 3. Usage Pattern
You give your AI agent a binary or app target:
> *"Inspect `original.exe`. Find where the license check / encryption key derivation occurs in the `__text` segment, explain the algorithm, and write an equivalent clean Python implementation."*

The AI agent invokes REA's MCP tools, steps through the disassembly in Hopper/Ghidra in the background, extracts the assembly logic, and writes the clean-room reimplementation for you.

---

## 🛡️ Impact on Cybersecurity & Software Monetization

As highlighted by *Tech Secured*:
1. **Death of "Security through Obscurity":** Proprietary licensing checks, local DRM, and undocumented client-side protocols can now be dissected and understood by AI agents in minutes.
2. **The Open-Source Acceleration:** Closed-source desktop utilities and micro-SaaS features can be rapidly cloned into open-source equivalents.
3. **Defensive Implication:** Developers must assume their client-side binaries are completely transparent to AI agents; all security, licensing, and business-critical validations must remain strictly on verified cloud backends.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/ai-red-teaming-and-llm-hacking-playbook|AI Red Teaming & LLM Hacking Playbook]]
* [[concepts/ai-powered-offensive-security-and-osint-playbook|AI-Powered Offensive Security Playbook]]
* [[concepts/vibe-coder-security-fix-kit|The Vibe Coder's Security Fix Kit]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
