---
title: "Vercel Labs agent-desktop: Accessibility-Tree GUI Automation for AI Agents"
created: 2026-11-05
updated: 2026-11-05
type: concept
tags: [ai-agents, computer-use, desktop-automation, accessibility-tree, vercel-labs, claudecode, mcp, devtools]
sources: [vercel-labs/agent-desktop GitHub (16k+ stars), Wait What Did You Do Reel 1094072517018255]
confidence: high
contested: false
contradictions: []
---

# 🖥️ Vercel Labs agent-desktop: Accessibility-Tree Desktop Automation (16k+ Stars)

> **"400 invoices due by midnight. The legacy app is from 2009 and has no API. Clicking by pixel/screen position breaks the second a window moves. `agent-desktop` reads desktop apps through your operating system's native accessibility tree, giving every button and field a deterministic name your agent can click and type into—in the background without hijacking your mouse."**  
> Technical breakdown of **`vercel-labs/agent-desktop`**, an open-source tool and CLI (Apache-2.0) that enables true Computer Use across macOS, Windows, and Linux via OS accessibility trees instead of fragile computer-vision coordinates.

---

## ⚡ The Breakthrough: Accessibility Tree vs. Vision Coordinates

| Dimension | Vision / Pixel Clicking (Anthropic Computer Use / PyAutoGUI) | `agent-desktop` (OS Accessibility Tree) |
| :--- | :--- | :--- |
| **Window Movement** | 🚨 **Breaks instantly** if the window is resized, moved, or scaled. | 🟢 **100% Robust:** Identifies elements by internal semantic ID / ref. |
| **Mouse Hijacking** | Steals your physical mouse cursor; you cannot touch your PC while it runs. | 🟢 **Runs in Background:** Directly invokes OS UI events; your mouse stays free. |
| **Latency & Cost** | Requires full-resolution screenshot uploads to multi-modal vision LLMs ($$$). | Returns compact JSON trees (~100–300 tokens); 10x faster and cheaper. |
| **Headless / Virtual** | Needs an active virtual display frame buffer. | Reads native desktop handles across legacy Win32, AppKit, and GTK apps. |

---

## 🏗️ Architecture & Control Loop

```
┌────────────────────────────────────────────────────────┐
│           AI AGENT (Claude Code / Hermes / Codex)      │
└──────────────────────────┬─────────────────────────────┘
                           │ CLI JSON / MCP Commands
┌──────────────────────────▼─────────────────────────────┐
│          AGENT-DESKTOP RUNTIME (Vercel Labs)           │
├────────────────────────────────────────────────────────┤
│ • Windows: UI Automation (UIA)                         │
│ • macOS: AXUIElement (Accessibility API)               │
│ • Linux: AT-SPI2 DBus Tree                             │
└──────────────────────────┬─────────────────────────────┘
                           │ Semantic Reference (@ref)
┌──────────────────────────▼─────────────────────────────┐
│         LEGACY DESKTOP APP (ERP, Amadeus DCS, CRM)     │
├────────────────────────────────────────────────────────┤
│ [ Button: "Submit" @s8f3k:e8 ] [ Input: "Search" @e2 ] │
└────────────────────────────────────────────────────────┘
```

1. **Snapshot:**  
   The agent calls `agent-desktop snapshot --app <AppName> -i`.  
   The OS returns an accessibility hierarchy tree where every interactive element is assigned a stable reference handle (e.g. `@s8f3k:e8`).
2. **Deterministic Action:**  
   The agent sends `agent-desktop click @s8f3k:e8` or `agent-desktop type @input_ref "Text"`.
3. **State Verification:**  
   The agent requests a fresh snapshot to confirm the screen transitioned as intended before executing the next step.

---

## 🚀 Installation & Quick Start

### 1. Installation
```bash
npm install -g agent-desktop
# or
brew install agent-desktop
```

### 2. Verify System Permissions
```bash
agent-desktop status
agent-desktop permissions --guide
```

### 3. Usage Commands
```bash
# Snapshot all interactive fields in an active app
agent-desktop snapshot --app "BillingApp" -i

# Click a specific element ref
agent-desktop click @ref_id

# Type text into a focused field
agent-desktop type @field_ref "Invoice #20264"
```

---

## 💡 Practical Use Cases for Omar's Ecosystem

1. **Legacy Airport DCS & Station Portals (No APIs):**  
   * Automating routine passenger lookups or station roster inputs on legacy desktop Windows applications that lack modern REST/GraphQL APIs.
2. **Background Spreadsheet / Tool Automation:**  
   * Operating desktop accounting or timesheet software quietly in the background without locking your mouse or keyboard while pair-programming.
3. **Synergy with Local Agent Workflows:**  
   * Bridges with [[concepts/reverse-api-engineer-website-to-api]] (for web) and [[concepts/google-artemis-android-automation]] (for Android mobile), completing the trifecta: **Web + Mobile + Desktop GUI automation**.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/google-artemis-android-automation|Google ARTEMIS Android Automation]]
* [[concepts/reverse-api-engineer-website-to-api|Reverse API Engineer]]
* [[concepts/claude-code-boris-cherny-power-user-playbook|Claude Code Boris Cherny Playbook]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
