---
title: "Earshot: Open-Source Audio Intelligence & Sound Synthesis Toolkit for AI Agents"
created: 2026-10-19
updated: 2026-10-19
type: concept
tags: [ai-agents, audio, sound-design, sound-effects, foley, mcp, python, leonxlnx, devtools, multimodal]
sources: [Leonxlnx/earshot GitHub (https://github.com/Leonxlnx/earshot), Techinsixty Facebook Reel 1587638229319094]
confidence: high
contested: false
contradictions: []
---

# 🎧 Earshot: Ears for AI Coding Agents (Leonxlnx/earshot)

> **"AI coding agents can write code to render animations, demos, or games, but they cannot hear what they made. Earshot gives them ears to analyze sound, critique video-audio sync, and synthesize sound effects natively in code."**  
> Technical architecture and operational breakdown of **Earshot**, an open-source audio perception and DSP synthesis toolkit designed for AI coding agents via MCP and Python.

---

## ⚡ The Audio Gap in AI Development

LLMs with multimodal capabilities (vision, text, code) can generate UI animations, Remotion video scripts, or game engines, but they lack audio feedback loops:
* They cannot tell if a UI click sound feels tactile or muffled.
* They cannot detect if an impact audio transient lands 80ms out of sync with a video cut.
* They cannot programmatically synthesize high-fidelity Foley sound effects without relying on static external stock audio assets.

**Earshot solves this by turning sound into structured evidence and executable DSP synthesis code that LLM agents can inspect, critique, and generate.**

---

## 🛠️ Core Capabilities

```
┌────────────────────────────────────────────────────────┐
│            AI CODING AGENT (Claude Code / Hermes)      │
└──────────────────────────┬─────────────────────────────┘
                           │ MCP Protocol / Python API
┌──────────────────────────▼─────────────────────────────┐
│                 EARSHOT TOOLKIT (Leonxlnx/earshot)     │
├──────────────────────────┬─────────────────────────────┤
│ 1. Perception & Auditing │ • Semantic audio description│
│                          │ • Text-to-audio match & find│
│                          │ • Video/Audio sync critique │
├──────────────────────────┼─────────────────────────────┤
│ 2. Procedural Synthesis  │ • earshot forge (code DSP)  │
│                          │ • Bank of 201 code-made SFX │
│                          │ • Reverse audio into code   │
└──────────────────────────┴─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│    OUTPUT: Local CPU Execution • Offline • Zero Latency │
└────────────────────────────────────────────────────────┘
```

### 1. Audio Perception & Semantic Analysis
* **`earshot describe <file>`**: Analyzes transient attacks, decay, spectral brightness, and outputs structured semantic descriptions (e.g., *"0.56s short transient; sounds like a mechanical keyboard switch click; brightness 1.5 kHz"*).
* **`earshot match <file> <prompt>`**: Computes how well an audio file matches a textual descriptor compared to competing alternatives.
* **`earshot find <audio> <prompt>`**: Scans long recordings and extracts exact millisecond timestamps where specific events occur.
* **`earshot critique <video.mp4>`**: Performs full automated audio-visual sync audits, measuring whether hits align with picture cuts and grading against professional mixing standards.

### 2. Code-Generated Sound Effects (Procedural DSP)
* **Zero Stock Asset Dependencies:** Generates whooshes, UI clicks, risers, impacts, and ambient tones purely using mathematical Python DSP recipes (NumPy/SciPy waveforms).
* **Bank of 201 Parametric SFX:** Includes an offline library of procedural sound effects rendered instantly by ID.
* **`earshot fit` (Audio Reverse-Engineering):** Analyzes an existing recorded `.wav`/`.ogg` sample and reverses it into an editable Python synthesis recipe.

---

## 🚀 Installation & Agent MCP Setup

### 1. Installation
```bash
pip install earshot
```
*(Runs 100% locally on CPU without requiring an external GPU)*.

### 2. Connect to AI Agents (Claude Code / Hermes MCP)
Add Earshot to your agent configuration:
```json
{
  "mcpServers": {
    "earshot": {
      "command": "earshot",
      "args": ["mcp"]
    }
  }
}
```

---

## 💡 Practical Use Cases for Aethelgard & Omar's Stack

1. **FUI & Motion Graphics Sound Design:**
   * Pairing with [[neuron_visuals_fui_motion_style]] to automatically generate matching sci-fi UI blips, data chirps, and telemetry risers directly in Python.
2. **Automated Video Sync Verification:**
   * Validating that audio voice memos, sound cues, and visual cuts align with zero millisecond drift.
3. **Autonomous Audio Creation:**
   * Giving Hermes the ability to forge UI sound effects on demand without downloading third-party MP3 files.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/rea-reverse-engineer-anything-mcp|REA: Reverse Engineer Anything (MCP)]]
* [[concepts/vibe-coder-security-fix-kit|Vibe Coder Security Fix Kit]]
* [[concepts/ai-red-teaming-and-llm-hacking-playbook|AI Red Teaming Playbook]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
