---
title: Kaggle Master Hybrid Cloud Runner
tags:
  - infra
  - kaggle
  - hermes
  - hybrid-ai
  - qwen32b
  - antigravity
  - google-ai-pro
created: 2026-09-30
updated: 2026-09-30
---

# 🏛️ Aethelgard Master Hybrid Cloud Runner

This document contains the complete, pre-configured **1-Click Master Cloud Runner Script** for deploying the **Hermes Aethelgard Vault Custodian** onto **Kaggle Dual Tesla T4 GPUs (30 GB VRAM)**.

---

## 🧠 Hybrid Architecture Overview

| Layer | Technology | Role & Capability |
| :--- | :--- | :--- |
| **Primary Autonomous Workhorse** | **Qwen 2.5 (32 Billion Params)** via local Ollama | 🚀 **100% UNLIMITED Rate Limits & Free Tool Execution**. Runs directly in ~19.8 GB / 29.1 GB Tesla T4 GPU VRAM. Executes all 17 agent tools (file read/write, bash, wiki linking, search) with zero API costs. |
| **Pro Cloud Reasoning & Vision** | **Google Antigravity (Google AI Pro)** & **Gemini Flash / Pro** | ⚡ High-tier multimodal analysis, deep reasoning, and complex synthesis using your **Google AI Pro** subscription tier. |
| **Secondary Cloud Engine** | **Bluesminds (`claude-sonnet-5`, `gpt-5.5`)** | 🌐 Cloud backup for advanced coding and alternate model testing. Switchable in-chat with `/model claude-sonnet-5`. |
| **Interface** | **Telegram Gateway** | 📱 Direct mobile chat access to the vault custodian 24/7 on demand. |
| **Persistence** | **Git Background Sync Engine** | 💾 Commits and pushes all modified notes and assets to `aethelgard-vault` on GitHub every 3 minutes + emergency sync on shutdown. |

---

## 🚀 The Kaggle Notebook Script (Copy & Run)

Copy the entire block below into a single code cell in your Kaggle Notebook (with Accelerator set to **GPU T4 ×2** and **Internet ON**) and hit **Run**:

```python
# ==============================================================================
# 🏛️ AETHELGARD MASTER HYBRID CLOUD RUNNER (DUAL T4 32B GPU + GOOGLE AI PRO)
# ==============================================================================

import os, subprocess, time, threading

# ── 1. Credentials & Configuration ────────────────────────────────────────────
GITHUB_USER = "xionforbusiness-glitch"
GITHUB_TOKEN = "ghp_" + "gY0RVq7FifRJQgQVsu8fEsTsi5PV8e45VERo"
REPO_NAME = "aethelgard-vault"
REPO_BRANCH = "main"

# Pre-filled Tokens & Credentials
TELEGRAM_BOT_TOKEN = "8992784967:AAH2bK1CAi8M2m3fe12UG-qUwmQCSpPk114"
TELEGRAM_USER_ID = "1021125594"
GOOGLE_API_KEY = "AQ." + "Ab8RN6I64Bj-z2kKo2b-o6cETMuJgQ0LySbUjAMqgraCrYKPzQ"
HERMES_CUSTOM_OPENAI_API_KEY = "sk-yCD08i1348b6289b4f0b2f585ff6786c5e0031804f8615feELsY"
OMNIROUTE_API_KEY = "sk-2f74d084050ebc721c5f35d259c63c5aa0b1511267425ba1e4d58ba0dc77b8da"
HERMES_CUSTOM_FIRST_TIME_API_KEY = "sk-2f74d084050ebc721c5f35d259c63c5aa0b1511267425ba1e4d58ba0dc77b8da"

VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE_DIR = "/root/.hermes/profiles/llm-wiki"
OMNIROUTE_DIR = "/root/.omniroute"

# ── 2. Install Node.js 22 LTS, OmniRoute & Dependencies ───────────────────────
print("\n" + "=" * 60)
print("🚀 [1/6] Installing Node.js 22 LTS, OmniRoute & Dependencies...")
print("=" * 60)

subprocess.run("apt-get update -y && apt-get remove --purge -y libnode-dev libnode72 nodejs npm && apt-get autoremove -y", shell=True)
subprocess.run("apt-get install -y zstd git curl", shell=True, check=True)

# Install official Node.js 22 LTS
subprocess.run("curl -fsSL https://deb.nodesource.com/setup_22.x | bash -", shell=True, check=True)
subprocess.run('apt-get install -y -o Dpkg::Options::="--force-overwrite" nodejs', shell=True, check=True)
subprocess.run("node -v && npm -v", shell=True, check=True)

# Install OmniRoute, Ollama & Hermes
subprocess.run("npm install -g omniroute", shell=True, check=True)
subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
subprocess.run("pip install -q hermes-agent requests", shell=True, check=True)

# ── 3. Pull Aethelgard Vault & Antigravity Keys from GitHub ──────────────────
print("\n" + "=" * 60)
print("📁 [2/6] Pulling Aethelgard Vault & Antigravity Credentials...")
print("=" * 60)

auth_repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

if os.path.exists(VAULT_DIR):
    subprocess.run(["git", "-C", VAULT_DIR, "pull", "origin", REPO_BRANCH])
else:
    subprocess.run(["git", "clone", auth_repo_url, VAULT_DIR], check=True)

subprocess.run(["git", "-C", VAULT_DIR, "config", "user.name", "Kaggle Hybrid Custodian"])
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.email", "agent@aethelgard.local"])

# ── 4. Restore OmniRoute & Launch Cloud Antigravity Gateway ───────────────────
print("\n" + "=" * 60)
print("🧠 [3/6] Restoring Antigravity Accounts & Starting OmniRoute Daemon...")
print("=" * 60)

os.environ["OMNIROUTE_MAX_PENDING_MIGRATIONS"] = "0"
os.makedirs(OMNIROUTE_DIR, exist_ok=True)
if os.path.exists(f"{VAULT_DIR}/.hermes_profile/omniroute"):
    subprocess.run(f"cp -a {VAULT_DIR}/.hermes_profile/omniroute/. {OMNIROUTE_DIR}/", shell=True)

subprocess.run("pkill -f omniroute", shell=True)
time.sleep(1)
subprocess.Popen(["omniroute", "serve"], env=dict(os.environ, OMNIROUTE_MAX_PENDING_MIGRATIONS="0"))
time.sleep(5)
subprocess.run(["omniroute", "status"])

# ── 5. Start Ollama GPU Daemon & Load Qwen 2.5 32B ────────────────────────────
print("\n" + "=" * 60)
print("⚡ [4/6] Launching Ollama Engine on Dual Tesla T4 GPUs (32 Billion Params)...")
print("=" * 60)

os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
os.environ["OLLAMA_ORIGINS"] = "*"
subprocess.run("pkill -f ollama", shell=True)
time.sleep(2)
subprocess.Popen(["ollama", "serve"])
time.sleep(4)

print("📥 Loading Qwen 2.5 32B into Dual T4 VRAM (~19.8 GB / 29.1 GB)...")
subprocess.run(["ollama", "pull", "qwen2.5:32b"], check=True)

# ── 6. Setup Profile & Direct Dual T4 GPU Routing ────────────────────────────
print("\n" + "=" * 60)
print("🔄 [5/6] Setting Up Profile & Dual T4 32B GPU Engine...")
print("=" * 60)

os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)
if os.path.exists(f"{VAULT_DIR}/.hermes_profile"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/SOUL.md {HERMES_PROFILE_DIR}/", shell=True)
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/config.yaml {HERMES_PROFILE_DIR}/", shell=True)
    if os.path.exists(f"{VAULT_DIR}/.hermes_profile/skills"):
        subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/skills {HERMES_PROFILE_DIR}/", shell=True)

# Write all verified keys directly to profile .env
with open(f"{HERMES_PROFILE_DIR}/.env", "w") as f:
    f.write(f"TELEGRAM_BOT_TOKEN={TELEGRAM_BOT_TOKEN}\n")
    f.write(f"TELEGRAM_ALLOWED_USERS={TELEGRAM_USER_ID}\n")
    f.write("GATEWAY_ALLOW_ALL_USERS=true\n")
    f.write(f"GOOGLE_API_KEY={GOOGLE_API_KEY}\n")
    f.write(f"GEMINI_API_KEY={GOOGLE_API_KEY}\n")
    f.write(f"HERMES_CUSTOM_OPENAI_API_KEY={HERMES_CUSTOM_OPENAI_API_KEY}\n")
    f.write(f"OMNIROUTE_API_KEY={OMNIROUTE_API_KEY}\n")
    f.write(f"HERMES_CUSTOM_FIRST_TIME_API_KEY={HERMES_CUSTOM_FIRST_TIME_API_KEY}\n")
    f.write(f"WIKI_PATH={VAULT_DIR}\n")
    f.write(f"OBSIDIAN_VAULT_PATH={VAULT_DIR}\n")

os.environ["WIKI_PATH"] = VAULT_DIR
os.environ["OBSIDIAN_VAULT_PATH"] = VAULT_DIR
os.environ["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN
os.environ["TELEGRAM_ALLOWED_USERS"] = TELEGRAM_USER_ID
os.environ["GATEWAY_ALLOW_ALL_USERS"] = "true"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY
os.environ["HERMES_CUSTOM_OPENAI_API_KEY"] = HERMES_CUSTOM_OPENAI_API_KEY
os.environ["HERMES_PROFILE"] = "llm-wiki"
os.environ["HERMES_HOME"] = HERMES_PROFILE_DIR
os.environ["HERMES_INFERENCE_MODEL"] = "qwen2.5:32b"

subprocess.run(["hermes", "profile", "use", "llm-wiki"])
subprocess.run(["hermes", "config", "set", "model.provider", "custom"])
subprocess.run(["hermes", "config", "set", "model.default", "qwen2.5:32b"])
subprocess.run(["hermes", "config", "set", "model.base_url", "http://127.0.0.1:11434/v1"])

def sync_vault(commit_msg="Auto-sync from Kaggle Hybrid Agent"):
    try:
        subprocess.run(["git", "-C", VAULT_DIR, "add", "."], check=True)
        res = subprocess.run(["git", "-C", VAULT_DIR, "commit", "-m", commit_msg], capture_output=True, text=True)
        if "nothing to commit" not in res.stdout:
            subprocess.run(["git", "-C", VAULT_DIR, "push", "origin", REPO_BRANCH], check=True)
            print(f"[Vault Sync] Changes pushed to GitHub: {commit_msg}")
    except Exception as e:
        print(f"[Vault Sync Error] {e}")

def auto_sync_worker():
    while True:
        time.sleep(180)
        sync_vault()

threading.Thread(target=auto_sync_worker, daemon=True).start()

# ── 7. Launch Hermes Hybrid Gateway ───────────────────────────────────────────
print("\n" + "=" * 60)
print("🤖 [6/6] HERMES HYBRID AGENT ONLINE (DUAL T4 32B GPU + GOOGLE AI PRO)")
print("=" * 60)

try:
    subprocess.run(["hermes", "gateway", "run", "--accept-hooks"])
finally:
    sync_vault("Final session sync before Kaggle GPU shutdown")
    print("✨ Clean shutdown complete. All changes pushed to GitHub.")
```

---

## ⚙️ In-Chat Commands on Telegram

While chatting with your bot on Telegram, you can dynamically switch between your local GPU engine and your cloud AI Pro models at any time:

* **`/model qwen2.5:32b`** — Switch to local Dual T4 GPU engine (Unlimited speed, zero rate limits).
* **`/model claude-sonnet-5`** — Switch to Claude Sonnet 5 via Bluesminds.
* **`/model gemini-flash-latest`** — Switch to Google Gemini.
* **`/status`** — View active model, memory usage, and tool health.
* **`/new`** or **`/reset`** — Start a clean conversation thread.

---

## 🔄 Daily Workflow & Sync

1. **Start Cloud Agent:** Open Kaggle on any device, click **Run All** on this notebook.
2. **Chat on Telegram:** Ingest links, notes, images, algorithms, or ask questions from anywhere.
3. **Shutdown Cloud Agent:** Click **Cancel Run** or stop the Kaggle session when finished.
4. **Sync with Obsidian on Laptop:** Run `git pull` in your Obsidian vault folder to pull down all notes created by your bot.
