---
title: Free Claude Code Proxy Engine
created: 2026-09-30
updated: 2026-09-30
type: entity
tags: [ai, coding-agent, claude-code, proxy, opensource, llm-inference, python, agpl]
sources: [raw/articles/2026-09-30-facebook-reels-ingest-batch.md, https://github.com/alishahryar1/free-claude-code]
confidence: high
contested: false
contradictions: []
---

# Free Claude Code (`free-claude-code`)

## 1. Overview & Core Mission
`free-claude-code` (authored by **Ali Shahryar Khokhar / Alishahryar1**) is a high-performance open-source proxy and client harness designed to liberate Anthropic's **Claude Code** CLI and modern agentic development environments from closed billing locks.

With over **56.2k GitHub stars** and **9k forks**, `free-claude-code` acts as an intelligent intermediary proxy daemon that translates Claude Code CLI and Anthropic protocol requests into standard OpenAI-compatible API schemas, enabling developers to route coding agent queries through zero-cost cloud backends, free-tier API endpoints, or private self-hosted inference clusters (such as [[kaggle-llm-backend-deployment|Kaggle Dual T4 Ollama Server]]).

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Workstation                    │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Claude Code CLI / Cursor / Codex / Hermes Agent     │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │ (Anthropic Protocol / REST)  │
│                              ▼                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Free Claude Code Proxy (Port 8000 / Uvicorn Server) │   │
│   │ - SQLite Connection QueuePool (8.65x I/O speedup)   │   │
│   │ - Model Schema Adaptation & Tool Mapping Engine    │   │
│   │ - Provider Health Checks & Fallback Failover        │   │
│   └──────────────────────────┬──────────────────────────┘   │
└──────────────────────────────┼──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌──────────────────────┐              ┌──────────────────────┐
│  Free-Tier API Hub   │              │  Private GPU Cluster │
│  (134+ Free APIs)    │              │  (Kaggle Dual T4)    │
│  - Gemini 2.5/Flash  │              │  - Ollama Daemon     │
│  - Grok / Cerebras   │              │  - Qwen 2.5 (32B)    │
│  - NVIDIA NIM        │              │  - Ngrok Tunnel      │
└──────────────────────┘              └──────────────────────┘
```

---

## 2. Technical Architecture & Performance Enhancements

### A. SQLite QueuePool Connection Architecture
In recent releases (September 2026, PR `#1939`), the proxy transitioned from sequential single-transaction SQLite opens to a multi-connection `SQLAlchemy QueuePool` architecture:
- **1 Dedicated Writer Connection + 4 Reader Connections** operating through asynchronous AnyIO workers.
- **Throughput Improvements:**
  - Mixed SQL read/write: **764 ops/s → 6,608 ops/s** (**8.65x speedup**).
  - Messaging tree persistence & history restoration: **104 cycles/s → 706 cycles/s** (**6.79x speedup**).
  - p99 Latency dropped from **569 ms to 15 ms**.

### B. Multi-Provider Compatibility
The proxy supports direct configuration and seamless fallback across:
- **Free Cloud Providers:** Google Gemini API, Grok API, Groq Cloud, DeepInfra, Cerebras, Sambanova, OpenRouter free tiers.
- **Self-Hosted Backends:** [[kaggle_hybrid_cloud_runner|Kaggle GPU Runner]], vLLM, Ollama, SGLang, Aphrodite Engine.
- **Local Tool Access:** Windows & Linux socket parity, Playwright Chromium Admin UI, Loguru JSON streaming.

---

## 3. Key Specifications

| Attribute | Specification |
| :--- | :--- |
| **Repository** | `alishahryar1/free-claude-code` |
| **License** | GNU AGPL-3.0 (`AGPL-3.0-only`) |
| **Language & Toolchain** | Python 3.14 / 3.11+, `uv` package manager, Ty type checker, Ruff |
| **Web Server / Async Core** | Uvicorn + FastAPI / Starlette, AnyIO async workers |
| **Compatible Clients** | Claude Code CLI, Cursor, Windsurf, Codex, [[00 Profile|Hermes Agent]], Kiro |
| **Admin UI** | Native web dashboard with live provider checks and credential shielding |

---

## 4. Integration with Aethelgard & Hermes LLM Wiki
`free-claude-code` complements the existing [[kaggle-llm-backend-deployment|Kaggle Hybrid Cloud Runner]] and [[laya-system-1-decision-engine|Laya Decision Engine]]:
1. **Zero Billing Guard:** Acts as a local/edge adapter when running Claude Code CLI workflows on local codebases.
2. **Kaggle Tunnel Bridge:** Directly connects to Kaggle Ngrok URLs (`https://<id>.ngrok-free.app/v1`) using `qwen2.5:32b` or `qwen2.5:14b`.
3. **OmniRoute Parity:** Works alongside [[00 Profile|OmniRoute]] for load balancing high-reasoning vs fast-execution coding tasks.

---

## 5. Related Notes & References
- [[kaggle-llm-backend-deployment]] — Zero-cost cloud LLM inference on Kaggle Dual Tesla T4 GPUs.
- [[free-tier-llm-api-endpoints-routing]] — Catalog of 134 permanent free AI APIs and routing patterns.
- [[claude-code-plugins-ecosystem]] — 34 Claude Code plugin collections and skills marketplace.
- [[01 Technical Skills]] — Primary overview of Omar Elnemr's technical stack.
- [[technical_skills_knowledge_base]] — Comprehensive technical reference.
