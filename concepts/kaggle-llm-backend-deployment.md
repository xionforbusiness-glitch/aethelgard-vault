---
title: Kaggle LLM Backend Deployment & Integration Guide
created: 2026-09-30
updated: 2026-09-30
type: concept
tags: [llm, ollama, ngrok, python, bash, linux, hermes-agent, telegram-bot]
sources: [raw/articles/kaggle-llm-backend-deployment-guide.md]
confidence: high
contested: false
contradictions: []
---

# Kaggle LLM Backend Deployment & Integration Guide

## 1. Overview & Architecture
This architecture provides a zero-cost, high-performance remote cloud inference backend for [[01 Technical Skills|Hermes Agent]] and Telegram bot automation without relying on local machine hardware resources.

By leveraging a **Kaggle Notebook instance** equipped with **Dual NVIDIA Tesla T4 GPUs (~29 GB combined VRAM)**, we host **Ollama** serving `qwen2.5:14b` and expose it securely to the internet via an **Ngrok reverse proxy tunnel**.

```
┌─────────────────────────────────────────────────────────────┐
│                    Client / Edge Layer                      │
│                                                             │
│   Telegram Bot Client ◄──► Hermes Agent (Local / VPS)      │
│                                  │                          │
│                                  │ (REST API / JSON)        │
│                                  ▼                          │
│                      Ngrok Secure HTTP Tunnel               │
│                  (https://<ngrok-id>.ngrok-free.app)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Kaggle Cloud Environment                  │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ pyngrok Tunnel Agent (Port 11434 Reverse Proxy)     │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│   ┌──────────────────────────▼──────────────────────────┐   │
│   │ Ollama Daemon (OLLAMA_HOST=0.0.0.0, ORIGINS=*)     │   │
│   └──────────────────────────┬──────────────────────────┘   │
│                              │                              │
│   ┌──────────────────────────▼──────────────────────────┐   │
│   │ Dual NVIDIA Tesla T4 GPUs (~29 GB VRAM Total)       │   │
│   │ Active Model: Qwen 2.5 (14B Parameters)            │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Infrastructure & System Specifications

| Component | Specification / Setting | Purpose |
| :--- | :--- | :--- |
| **Compute Host** | Kaggle Notebook Environment | Cloud GPU execution runtime |
| **Hardware Accelerator** | Dual NVIDIA Tesla T4 GPUs (2x 15 GB ≈ 29 GB VRAM) | Parallel tensor execution & multi-layer offloading |
| **Inference Engine** | [[technical_skills_knowledge_base|Ollama]] (`0.0.0.0:11434`) | High-throughput model execution daemon & REST API |
| **Target LLM** | `qwen2.5:14b` | Optimal balance of reasoning, tool use, and coding precision |
| **Ingress / Reverse Proxy** | `pyngrok` (Ngrok HTTP Tunnel) | Exposes internal Kaggle port 11434 to public HTTPS endpoint |
| **Agent Consumer** | [[00 Profile|Hermes Agent]] (llm-wiki profile) / Telegram Gateway | Autonomous vault management and assistant workflows |

---

## 3. Issues Encountered & Resolution Runbook

During deployment and remote integration, several critical operational hurdles were identified and resolved:

| Category | Problem / Root Cause | Engineered Resolution |
| :--- | :--- | :--- |
| **Account Verification** | Direct SMS verification failed with Syrian phone country codes (`+963`). | Used fallback international SMS / identity verification (e.g., Egyptian line) to unlock full GPU quota. |
| **Package Dependencies** | Ollama binary installer failed during extraction due to missing compression utility. | Pre-installed `zstd` prior to installer execution: `apt-get install -y zstd`. |
| **Network Egress** | Kaggle notebooks default to "Internet Off", breaking downloads and Ngrok handshakes. | Explicitly toggled **Internet ON** in the Kaggle Notebook sidebar settings. |
| **CLI String Escaping** | Windows PowerShell/CMD string quoting mangled curl JSON payloads, causing silent failures. | Switched to native PowerShell `Invoke-RestMethod` with structured JSON body strings. |
| **CORS / Host Headers** | Ollama rejected remote Ngrok requests with `HTTP 403 Forbidden` due to host filtering. | Exported `OLLAMA_HOST=0.0.0.0:11434` and `OLLAMA_ORIGINS=*` prior to daemon launch. |
| **Cold-Start Latency** | First prompt invocation on dual T4 GPUs experienced timeout / lag. | Permitted a 60–90 second warm-up window for initial weight allocation across dual VRAM banks. |

---

## 4. Kaggle Startup & Automation Script

To initialize or resume the remote backend session whenever Kaggle spins down, run the following unified Python cell:

```python
# ==========================================================
# Kaggle LLM Backend Deployment Script: Ollama + Qwen 2.5 + Ngrok
# ==========================================================

# 1. Install system prerequisites, Ollama binary, and pyngrok
!apt-get update -y && apt-get install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh
!pip install -q pyngrok

import os
import subprocess
import time
from pyngrok import ngrok

# 2. Configure unrestricted network access & binding
os.environ["OLLAMA_HOST"] = "0.0.0.0:11434"
os.environ["OLLAMA_ORIGINS"] = "*"

# 3. Clean stale processes and authenticate Ngrok
!pkill -f ollama
!pkill -f ngrok
ngrok.kill()
time.sleep(2)

NGROK_TOKEN = "PASTE_YOUR_NGROK_TOKEN_HERE"
ngrok.set_auth_token(NGROK_TOKEN)

# 4. Launch Ollama background daemon
subprocess.Popen(["ollama", "serve"])
time.sleep(4)

# 5. Download model weights
!ollama pull qwen2.5:14b

# 6. Establish Ngrok public HTTP tunnel on port 11434
tunnel = ngrok.connect(11434, "http")
print("\n" + "=" * 60)
print(f"ACTIVE ENDPOINT URL: {tunnel.public_url}")
print("=" * 60)
```

---

## 5. API Verification & Testing

### 5.1 PowerShell Health Check
Verify live generation and tunnel connectivity directly from Windows terminal:

```powershell
Invoke-RestMethod -Uri "https://<ngrok-id>.ngrok-free.app/api/generate" `
  -Method Post `
  -Headers @{"ngrok-skip-browser-warning"="true"} `
  -ContentType "application/json" `
  -Body '{"model": "qwen2.5:14b", "prompt": "Status check.", "stream": false}' `
  | Select-Object -ExpandProperty response
```

### 5.2 Integration Parameters

| Parameter | Configuration Value | Notes |
| :--- | :--- | :--- |
| **Native Base URL** | `https://<ngrok-id>.ngrok-free.app` | Ollama native REST API endpoints |
| **OpenAI-Compatible Base URL** | `https://<ngrok-id>.ngrok-free.app/v1` | Compatible with OpenAI SDK & Hermes gateways |
| **API Key** | `ollama` | Dummy bearer token string |
| **Required Header** | `ngrok-skip-browser-warning: true` | Bypasses Ngrok free-tier interstitial page |
| **Model Identifier** | `qwen2.5:14b` | Target LLM model name |

---

## 6. Architecture Evolution & Cloud Independence

Because Kaggle container disks reset upon session termination, persistent data and agent memory must be decoupled from the compute instance:

```
┌─────────────────────────────────────────────────────────────┐
│                    Persistence Strategies                   │
├──────────────────────────────┬──────────────────────────────┤
│ 1. Ephemeral Execution       │ 2. Persistent Orchestration  │
│    (Self-Contained Kaggle)   │    (Decoupled Agent & Cloud) │
├──────────────────────────────┼──────────────────────────────┤
│ • Run Telegram listener in   │ • Run Hermes Agent on 24/7   │
│   secondary Kaggle thread    │   low-power VPS or local box │
│ • Clone Obsidian vault on    │ • Keep Obsidian vault and    │
│   startup                    │   vector stores persistent   │
│ • Automated `git push` on    │ • Route inference requests   │
│   every note modification    │   to active Kaggle Ngrok URL │
└──────────────────────────────┴──────────────────────────────┘
```

1. **Decouple Vault Storage:** All [[vault_index_dashboard|Aethelgard Vault]] markdown files, assets, and logs remain synchronized via Git / cloud storage.
2. **Hybrid Cloud Strategy:** Local/VPS host manages file I/O, scheduled cron tasks, and Telegram webhooks, while heavy LLM tensor computations are offloaded to Kaggle's dual T4 GPU cluster.

---

## 7. Cross-References
- [[01 Technical Skills]] — Primary overview of technical stack and model routing.
- [[technical_skills_knowledge_base]] — Core programming languages, Linux administration, and ML pipelines.
- [[02 Projects]] — Summary of portfolio builds and engineering projects.
- [[detailed_project_documentation]] — Architectural documentation for software systems.
- [[linux_cli_bash_automation_reference]] — Shell automation, process management, and daemon scripts.
- [[openvpn_network_tunneling_architecture]] — Network tunneling, proxies, and remote access patterns.
- [[SCHEMA]] — LLM Wiki standards, metadata, and taxonomy rules.
- [[log]] — Chronological log of vault modifications and ingests.
