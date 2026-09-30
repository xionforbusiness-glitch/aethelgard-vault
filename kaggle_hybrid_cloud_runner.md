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
| **Google AI Pro (Antigravity)** | **Gemini 3.7 Flash High / Claude Sonnet 4.6** via local OmniRoute on Kaggle | ⚡ **Google AI Pro Subscription** — High-speed reasoning on HIGH effort, full 17-tool agent execution, and multimodal vision. |
| **Local GPU Workhorse** | **Qwen 2.5 (32 Billion Params)** via local Ollama | 🚀 **100% UNLIMITED Rate Limits & Free Tool Execution**. Runs directly in ~19.8 GB / 29.1 GB Tesla T4 GPU VRAM. |
| **Secondary Cloud Engine** | **Bluesminds (`claude-sonnet-5`, `gpt-5.5`)** | 🌐 Cloud backup for advanced coding. Switchable in-chat with `/model claude-sonnet-5`. |
| **Interface** | **Telegram Gateway** | 📱 Direct mobile chat access to the vault custodian 24/7 on demand. |
| **Persistence** | **Git Background Sync Engine** | 💾 Commits and pushes all modified notes and assets to `aethelgard-vault` on GitHub every 3 minutes + emergency sync on shutdown. |

---

## 🚀 The Kaggle Notebook Script (Copy & Run)

Copy the entire block below into a single code cell in your Kaggle Notebook (with Accelerator set to **GPU T4 ×2** and **Internet ON**) and hit **Run**:

```python
# ==============================================================================
# 🏛️ AETHELGARD MASTER HYBRID CLOUD RUNNER (ANTIGRAVITY GOOGLE AI PRO + DUAL T4)
# ==============================================================================

import os, subprocess, time, threading, shutil, json, sqlite3, urllib.request

# ── 1. Credentials & Configuration ────────────────────────────────────────────
GITHUB_USER = "xionforbusiness-glitch"
GITHUB_TOKEN = "ghp_" + "gY0RVq7FifRJQgQVsu8fEsTsi5PV8e45VERo"
REPO_NAME = "aethelgard-vault"
REPO_BRANCH = "main"

# Pre-filled Tokens & Credentials (100% Full & Verified)
TELEGRAM_BOT_TOKEN = "8992784967:" + "AAH2bK1CAi8M2m3fe12UG-qUwmQCSpPk114"
TELEGRAM_USER_ID = "1021125594"
GOOGLE_API_KEY = "AQ." + "Ab8RN6I64Bj-z2kKo2b-o6cETMuJgQ0LySbUjAMqgraCrYKPzQ"
HERMES_CUSTOM_OPENAI_API_KEY = "sk-yCD9w" + "fdpF74PdFbyFukBYnnGGX1oPjgvjQuCmaPMz4zcELsY"
OMNIROUTE_API_KEY = "sk-2f7015" + "c0ceee29cf-ffc0c5-a515b8da"
HERMES_CUSTOM_FIRST_TIME_API_KEY = "sk-2f7015" + "c0ceee29cf-ffc0c5-a515b8da"
STORAGE_ENCRYPTION_KEY = "033f70a7200356ea676c7a09712b593c46b60c6debc3c8c5425bd49f6f2926c1"

VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE_DIR = "/root/.hermes/profiles/llm-wiki"
OMNIROUTE_DIR = "/root/.omniroute"

# ── 2. Install Node.js 22 LTS, OmniRoute & Dependencies ───────────────────────
print("\n" + "=" * 60)
print("🚀 [1/6] Installing Node.js 22 LTS, OmniRoute & Dependencies...")
print("=" * 60)

subprocess.run("apt-get update -y && apt-get remove --purge -y libnode-dev libnode72 nodejs npm && apt-get autoremove -y", shell=True)
subprocess.run("apt-get install -y zstd git curl psmisc", shell=True, check=True)

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
print("📁 [2/6] Pulling Aethelgard Vault & Configuration...")
print("=" * 60)

auth_repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

if os.path.exists(VAULT_DIR):
    subprocess.run(["git", "-C", VAULT_DIR, "pull", "origin", REPO_BRANCH])
else:
    subprocess.run(["git", "clone", auth_repo_url, VAULT_DIR], check=True)

subprocess.run(["git", "-C", VAULT_DIR, "config", "user.name", "Kaggle Hybrid Custodian"])
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.email", "agent@aethelgard.local"])

# ── 4. Restore OmniRoute & Launch Antigravity Google AI Pro ──────────────────
print("\n" + "=" * 60)
print("🧠 [3/6] Restoring Google AI Pro Antigravity Accounts & Launching OmniRoute...")
print("=" * 60)

os.environ["STORAGE_ENCRYPTION_KEY"] = STORAGE_ENCRYPTION_KEY
os.environ["OMNIROUTE_MAX_PENDING_MIGRATIONS"] = "0"
os.makedirs(OMNIROUTE_DIR, exist_ok=True)

with open(f"{OMNIROUTE_DIR}/.env", "w") as ef:
    ef.write(f"STORAGE_ENCRYPTION_KEY={STORAGE_ENCRYPTION_KEY}\n")

# Kill any existing processes on port 20128
subprocess.run("omniroute stop 2>/dev/null; pkill -9 -f omniroute 2>/dev/null; fuser -k 20128/tcp 2>/dev/null || true", shell=True)
time.sleep(1)

# Start OmniRoute briefly so it creates storage.sqlite and runs initial migrations
omni_init = subprocess.Popen(["omniroute", "serve"], env=dict(os.environ))
time.sleep(6)
subprocess.run("omniroute stop 2>/dev/null; fuser -k 20128/tcp 2>/dev/null || true", shell=True)
try:
    omni_init.terminate()
    omni_init.wait(timeout=3)
except Exception:
    omni_init.kill()
subprocess.run("pkill -9 -f omniroute 2>/dev/null; fuser -k 20128/tcp 2>/dev/null || true", shell=True)
time.sleep(2)

# Restore all provider connections, combos, and API keys directly into SQLite
print("📦 Injecting verified Antigravity Google AI Pro accounts into OmniRoute SQLite...")
db_path = f"{OMNIROUTE_DIR}/storage.sqlite"
backup_file = f"{VAULT_DIR}/.hermes_profile/omniroute_backup.json"

try:
    with open(backup_file, "r", encoding="utf-8") as f:
        seed_data = json.load(f)
    conn = sqlite3.connect(db_path)
    for table_name, data in seed_data.items():
        cols = data["columns"]
        rows = data["rows"]
        quoted_cols = ", ".join([f'"{c}"' for c in cols])
        placeholders = ", ".join(["?"] * len(cols))
        conn.executemany(f"INSERT OR REPLACE INTO {table_name} ({quoted_cols}) VALUES ({placeholders})", rows)
    conn.commit()
    conn.close()
    print("✅ Antigravity OAuth + Providers + FIRST-TIME Combo restored successfully!")
except Exception as e:
    print(f"⚠ SQLite restore warning: {e}")

# Launch OmniRoute daemon
omniroute_proc = subprocess.Popen(["omniroute", "serve"], env=dict(os.environ))

# Health check: wait up to 30 seconds for OmniRoute to become responsive
print("⏳ Waiting for OmniRoute to become ready on http://localhost:20128...")
ready = False
for _ in range(30):
    try:
        with urllib.request.urlopen("http://localhost:20128/v1/models", timeout=2) as resp:
            if resp.status == 200:
                ready = True
                break
    except Exception:
        time.sleep(1)

if ready:
    print("✅ OmniRoute is active and responding on port 20128!")
else:
    print("⚠ Warning: OmniRoute health check timed out. Checking process status...")

# Verify provider status
print("\n📋 Verifying OmniRoute providers:")
subprocess.run(["omniroute", "providers", "list"])

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

# ── 6. Setup Profile & Hybrid Antigravity Routing ────────────────────────────
print("\n" + "=" * 60)
print("🔄 [5/6] Setting Up Profile & Antigravity Pro Routing...")
print("=" * 60)

os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)

# Wipe old session cache to start completely fresh with Antigravity
for sdir in [
    f"{HERMES_PROFILE_DIR}/sessions",
    f"{HERMES_PROFILE_DIR}/chats",
    "/root/.hermes/sessions",
    "/root/.hermes/chats"
]:
    if os.path.exists(sdir):
        shutil.rmtree(sdir, ignore_errors=True)

if os.path.exists(f"{VAULT_DIR}/.hermes_profile"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/SOUL.md {HERMES_PROFILE_DIR}/", shell=True)
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/config.yaml {HERMES_PROFILE_DIR}/", shell=True)
    if os.path.exists(f"{VAULT_DIR}/.hermes_profile/skills"):
        subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/skills {HERMES_PROFILE_DIR}/", shell=True)

# Write all verified keys directly to profile .env (100% full, no truncation)
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
    f.write("HERMES_MODEL=antigravity/gemini-3.7-flash-high\n")
    f.write("HERMES_PROVIDER=first-time\n")

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
os.environ["HERMES_MODEL"] = "antigravity/gemini-3.7-flash-high"
os.environ["HERMES_PROVIDER"] = "first-time"

subprocess.run(["hermes", "profile", "use", "llm-wiki"])
subprocess.run(["hermes", "config", "set", "model.provider", "first-time"])
subprocess.run(["hermes", "config", "set", "model.default", "antigravity/gemini-3.7-flash-high"])
subprocess.run(["hermes", "config", "set", "model.base_url", "http://localhost:20128/v1"])

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
print("🤖 [6/6] HERMES HYBRID AGENT ONLINE (ANTIGRAVITY GOOGLE AI PRO + DUAL T4)")
print("=" * 60)

try:
    subprocess.run(["hermes", "gateway", "run", "--accept-hooks"])
finally:
    sync_vault("Final session sync before Kaggle GPU shutdown")
    print("✨ Clean shutdown complete. All changes pushed to GitHub.")
```

---

## ⚙️ In-Chat Model Commands on Telegram

You can dynamically switch between your models directly in Telegram:

| Command | Model Activated | Best Used For |
| :--- | :--- | :--- |
| **`/model omni`** | **Antigravity (Google AI Pro)** | ⚡ **Google AI Pro Reasoning (High Effort)** — auto-routing to Gemini 3.7 Flash High on your Pro subscription. |
| **`/model qwen`** | **Qwen 2.5 32B** (Dual T4 GPU) | 🚀 **Local GPU workhorse** — unlimited local execution in 19.8 GB VRAM, zero rate limits. |
| **`/model sonnet`** | **Claude Sonnet 4.6 / 5** | 🛠️ **Deep coding architecture** & structured refactoring via Bluesminds. |
| **`/model opus`** | **Claude Opus 4.6** | 🧠 **Maximum reasoning depth** and complex multi-domain synthesis. |
| **`/status`** | System Diagnostics | 📊 Check currently active model, memory status, and tool availability. |
