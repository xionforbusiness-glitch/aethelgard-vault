---
title: "Google ARTEMIS: Autonomous Android Mobile Automation Framework for AI Agents"
created: 2026-10-24
updated: 2026-10-24
type: concept
tags: [ai-agents, google, artemis, android, automation, mobile, mcp, claude-code, hermes-agent, adb]
sources: [google/artemis GitHub (https://github.com/google/artemis), Nick Saraev Facebook Reel 1126982336915129]
confidence: high
contested: false
contradictions: []
---

# 📱 Google ARTEMIS: Autonomous Android Mobile Automation Framework

> **"Hand your Android phone to a tireless AI assistant. Google open-sourced ARTEMIS—turning natural-language instructions into reliable real-device automation with a 99%+ success rate on the AndroidWorld benchmark."**  
> Operational technical brief on **Google ARTEMIS** (`google/artemis`), a native mobile agent framework that connects AI assistants (Claude Code, Codex, Hermes Agent, Antigravity) directly to Android hardware via ADB and MCP.

---

## ⚡ What Is Google ARTEMIS?

**Repository:** `https://github.com/google/artemis` (14,000+ GitHub Stars)  
**Core Purpose:** While web agents (Playwright, Puppeteer) automate desktop browsers, automating mobile native apps has historically been brittle. ARTEMIS bridges LLMs directly to Android devices (physical hardware or emulators), interpreting visual UI hierarchies and executing gestures just like human thumbs:
* Tapping buttons, swiping feeds, filling inputs, and toggling system settings.
* Authenticating accounts, solving UI flows, and extracting on-screen telemetry.
* Achieving a **99%+ task completion success rate** on Google's rigorous **AndroidWorld Benchmark**.

---

## 🏗️ Architecture & How It Works

```
┌────────────────────────────────────────────────────────┐
│     AI AGENT (Claude Code / Hermes / Antigravity)      │
└──────────────────────────┬─────────────────────────────┘
                           │ MCP Protocol / Python SDK
┌──────────────────────────▼─────────────────────────────┐
│                 GOOGLE ARTEMIS RUNTIME                 │
├──────────────────────────┬─────────────────────────────┤
│ • UI Hierarchy Parser    │ • Vision & OCR Grounding    │
│ • Gesture Engine (Tap)   │ • Benchmark Telemetry Logs  │
└──────────────────────────┴─────────────────────────────┘
                           │ Android Debug Bridge (ADB)
┌──────────────────────────▼─────────────────────────────┐
│       ANDROID DEVICE (Physical Phone or Emulator)      │
└────────────────────────────────────────────────────────┘
```

1. **Dual Inspection (UI Tree + Vision):**
   * Combines accessibility node inspection (lightweight XML UI trees) with computer vision screenshot grounding to locate UI elements with near-zero hallucination.
2. **Native MCP Server & Python SDK:**
   * Ships out of the box with an MCP server interface, allowing coding agents like Claude Code, Codex, and Hermes to invoke phone actions as standard tool calls.
3. **On-Demand Skill Execution (Hermes Integration):**
   * Can be run on-demand via private virtualenvs (`uv`) without polluting permanent agent context with heavy tool schemas until a mobile automation task is explicitly triggered.

---

## 🛠️ Setup & Prerequisites

### 1. Requirements
* Linux, macOS, or Windows WSL2.
* An Android device with **USB Debugging** enabled (or an active Android Studio AVD emulator).
* `adb` (Android Debug Bridge) installed and paired:
  ```bash
  adb devices
  ```

### 2. MCP Integration (Claude Code / Hermes)
To plug ARTEMIS into Claude Code or Hermes via MCP:
```json
{
  "mcpServers": {
    "artemis": {
      "command": "python3",
      "args": ["-m", "artemis.mcp_server"]
    }
  }
}
```

### 3. Hermes Native Skill Installation
```bash
git clone https://github.com/pank-su/artemis-android-skill.git \
  ~/.hermes/profiles/llm-wiki/skills/autonomous-ai-agents/artemis-android
```

---

## 💡 Practical Applications for Omar's Ecosystem

1. **Automated Mobile Testing:**
   * Testing Android apps, web apps, or MacroDroid integrations on a real device.
2. **Autonomous Routine Offloading:**
   * Handing off repetitive mobile workflows (e.g., checking flight ground rosters on mobile DCS portals, taking screenshots, or clearing notifications).
3. **Synergy with MacroDroid Overseer:**
   * Pairing ARTEMIS with Omar's existing [[concepts/macrodroid-doomscroll-overseer|MacroDroid Overseer]] to create two-way mobile intelligence—detecting phone events and autonomously executing physical remediation on the device.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/macrodroid-doomscroll-overseer|MacroDroid Doomscroll Overseer]]
* [[concepts/rea-reverse-engineer-anything-mcp|REA: Reverse Engineer Anything (MCP)]]
* [[concepts/unlazy-anti-laziness-agent-skill|Unlazy: Completion Discipline Skill]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
