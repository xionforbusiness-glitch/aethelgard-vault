---
title: "Reverse API Engineer: Autonomous Network Traffic to Typed API Client Generator"
created: 2026-10-25
updated: 2026-10-25
type: concept
tags: [web-scraping, api-engineering, reverse-engineering, har-parser, claude-code, mcp, devtools, osint]
sources: [kalil0321/reverse-api-engineer GitHub (https://github.com/kalil0321/reverse-api-engineer), Nick Saraev Reel 1624631516070485]
confidence: high
contested: false
contradictions: []
---

# 🌐 Reverse API Engineer: Turning Any Website into a Native Typed API

> **"Traditional scrapers break every time a website changes its HTML or CSS classes. Reverse API Engineer watches the kitchen instead of reading the menu: it captures the internal JSON/GraphQL traffic the frontend uses, then synthesizes a bulletproof, typed client in seconds."**  
> Technical breakdown of **Reverse API Engineer** (`kalil0321/reverse-api-engineer`), an open-source tool and MCP server that bridges headless browsers with AI coding agents to reverse-engineer private endpoints on modern web apps.

---

## ⚡ The DOM Scraping vs. API Sniffing Paradigm

| Dimension | Traditional DOM Scraping (Cheerio / BS4 / Selenium) | Reverse API Engineering |
| :--- | :--- | :--- |
| **Fragility** | 🚨 **Extremely High:** Breaks when class names or layouts update | 🟢 **Ultra-Stable:** Uses the site's own internal production endpoints |
| **Payload Weight** | Heavy HTML/DOM trees (megabytes of bloat) | Pure structured JSON / GraphQL responses |
| **Bypassing Paywalls & WAFs** | Blocked easily by Cloudflare/DataDome DOM checks | Reuses authenticated session tokens & internal headers |
| **Speed** | Slow multi-element parsing loops | Sub-second raw HTTP calls directly to API gateways |

---

## 🏗️ Architecture & Execution Flow

```
┌────────────────────────────────────────────────────────┐
│           USER / AI AGENT GOAL (e.g. "Fetch Jobs")     │
└──────────────────────────┬─────────────────────────────┘
                           │ Agent Navigation / User Browsing
┌──────────────────────────▼─────────────────────────────┐
│          BROWSER AUTOMATION & TRAFFIC CAPTURE          │
├────────────────────────────────────────────────────────┤
│ • Headless Chromium intercepts XHR / Fetch requests    │
│ • Captures headers, auth bearer tokens, query params   │
│ • Streams full session traffic into structured HAR     │
└──────────────────────────┬─────────────────────────────┘
                           │ LLM Analysis (Claude / GPT)
┌──────────────────────────▼─────────────────────────────┐
│             SYNTHESIZED NATIVE CLIENT CODE             │
├────────────────────────────────────────────────────────┤
│ Output: Fully typed client (Python Pydantic, TS/Zod,   │
│ Go structs) handling session tokens, cookies & schemas  │
└────────────────────────────────────────────────────────┘
```

1. **Autonomous AutoScout Mode:**
   * An autonomous agent browses the target website (scrolling, clicking, toggling filters) while an HTTP proxy records every internal API request into an HTTP Archive (`.har`).
2. **HAR Telemetry Analysis:**
   * The AI parses through the network dump, filters out tracking telemetry (Google Analytics, Sentry, Datadog), and pinpoints the exact backend data endpoint (REST/GraphQL).
3. **Automated Client Code Generation:**
   * Compiles the endpoint schema into an idiomatic, production-ready client in **Python, TypeScript, Go, or Rust**, complete with automatic authentication header handling, pagination logic, and Pydantic models.

---

## 🚀 Installation & Agent MCP Setup

### 1. Installation
```bash
# Via uv (recommended) or pip
uv tool install reverse-api-engineer
# or
pip install reverse-api-engineer
```

### 2. Integration with AI Coding Agents (Claude Code / Hermes MCP)
Add the MCP configuration to your agent:
```json
{
  "mcpServers": {
    "reverse-api-engineer": {
      "command": "reverse-api-engineer",
      "args": ["mcp"]
    }
  }
}
```

### 3. Usage Pattern
```bash
# Interactive CLI mode
rae "https://example.com/careers" --goal "Extract all airport ground ops openings" --lang python
```

---

## 💡 High-Value Use Cases for Omar's Stack

1. **Aviation & Airport Flight Radars:**
   * Extracting real-time flight telemetry from regional airline dashboards or ground handler portals that do not offer public developer APIs.
2. **Market & Real Estate Reconnaissance:**
   * Pulling live rental listings and computer hardware classifieds (Dubizzle, OpenSooq) directly from their internal GraphQL backends with zero DOM-parsing failures.
3. **Synergy with Second Brain Research:**
   * Automating data ingestion from paywalled news feeds, paper archives, or internal knowledge hubs directly into `$VAULT_DIR/raw/`.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/rea-reverse-engineer-anything-mcp|REA: Reverse Engineer Anything (MCP)]]
* [[concepts/claude-code-boris-cherny-power-user-playbook|Claude Code Creator Playbook]]
* [[concepts/vibe-coder-security-fix-kit|The Vibe Coder's Security Fix Kit]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
