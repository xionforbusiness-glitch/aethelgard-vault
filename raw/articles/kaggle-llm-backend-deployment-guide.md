---
source_url: local_deployment/kaggle-ollama-ngrok
ingested: 2026-09-30
sha256: 9aab07a8b1e55304175b64614edb78f8df48f87a399e0c3a3db75b23b4c47fe4
---

# Kaggle LLM Backend Deployment & Integration Guide

## 1. System Overview
* **Hosting Environment:** Kaggle Notebook (GPU T4 x2, ~29 GB total VRAM).
* **Model Engine:** Ollama (serving on port 11434 with open CORS/Origins).
* **Active LLM:** `qwen2.5:14b` (selected for logic, tool execution, and code synthesis).
* **Remote Access:** Ngrok HTTP reverse proxy tunnel exposing port 11434.
* **Target Objective:** Remote backend for an automation agent ("Hermes") interfacing with Telegram and an Obsidian vault without relying on local machine hardware.

## 2. Issues Encountered & Resolutions
* **Phone Verification:** Direct verification with Syrian phone numbers (+963) failed SMS delivery/verification checks, requiring fallback verification (e.g., Egyptian number / identity verification).
* **Missing System Dependency:** Ollama installer failed with an extraction error due to missing zstd. Fixed by running `apt-get install -y zstd` prior to installation.
* **Network & Security Restrictions:**
  * Notebook defaulted to Internet off, which initially blocked package downloads and Ngrok tunnel creation.
  * Windows command-line escaping stripped JSON strings, causing silent curl failures.
  * Ollama threw HTTP 403 Forbidden on remote calls due to host header filtering. Resolved by setting `OLLAMA_HOST=0.0.0.0:11434` and `OLLAMA_ORIGINS=*`.
  * Initial model load on dual T4 GPUs requires a 60–90 second warm-up window while weights load into VRAM.

## 3. Kaggle Startup Script
To resume this session whenever Kaggle shuts down, paste and execute the following single-cell script:

```python
# 1. Install prerequisites, Ollama, and pyngrok
!apt-get update -y && apt-get install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh
!pip install -q pyngrok

import os
import subprocess
import time
from pyngrok import ngrok

# 2. Set environment parameters for unrestricted network access
os.environ["OLLAMA_HOST"] = "0.0.0.0:11434"
os.environ["OLLAMA_ORIGINS"] = "*"

# 3. Termize stale processes and authenticate Ngrok
!pkill -f ollama
!pkill -f ngrok
ngrok.kill()
time.sleep(2)

NGROK_TOKEN = "PASTE_YOUR_NGROK_TOKEN_HERE"
ngrok.set_auth_token(NGROK_TOKEN)

# 4. Launch daemon
subprocess.Popen(["ollama", "serve"])
time.sleep(4)

# 5. Download model weights
!ollama pull qwen2.5:14b

# 6. Expose local port via Ngrok tunnel
tunnel = ngrok.connect(11434, "http")
print("\n" + "=" * 60)
print(f"ACTIVE ENDPOINT URL: {tunnel.public_url}")
print("=" * 60)
```

## 4. API Endpoints & Testing

### Verification Command (PowerShell)
```powershell
Invoke-RestMethod -Uri "https://<ngrok-id>.ngrok-free.app/api/generate" `
  -Method Post `
  -Headers @{"ngrok-skip-browser-warning"="true"} `
  -ContentType "application/json" `
  -Body '{"model": "qwen2.5:14b", "prompt": "Status check.", "stream": false}' `
  | Select-Object -ExpandProperty response
```

### Integration Parameters
* **Ollama Native Base URL:** `https://<ngrok-id>.ngrok-free.app`
* **OpenAI-Compatible Base URL:** `https://<ngrok-id>.ngrok-free.app/v1`
* **API Key:** `ollama` (placeholder string)
* **Required Header:** `ngrok-skip-browser-warning: true`
* **Model Identifier:** `qwen2.5:14b`

## 5. Next Steps for Cloud Independence (Hermes + Telegram + Obsidian)
* **Decouple Agent Storage from Kaggle:**
  Kaggle disk resets completely on shutdown. Obsidian markdown files, spreadsheets, and databases must be committed to a remote Git repository or synchronized with an external cloud service.
* **Execution Strategy:**
  * **Ephemeral Setup:** Run the Telegram listener directly inside a secondary Kaggle thread, cloning the Obsidian vault on startup and triggering automated git push updates after file changes.
  * **Persistent Setup:** Run Hermes on an always-on minimal CPU VPS or Raspberry Pi to handle incoming Telegram voice/text commands 24/7, routing LLM inference payloads to the active Kaggle Ngrok URL.
