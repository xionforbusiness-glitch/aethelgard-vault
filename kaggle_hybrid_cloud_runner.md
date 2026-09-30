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
| **Google AI Pro (Antigravity)** | **Claude Opus 4.6 / Claude Sonnet 4.6 / Gemini 3.7 Flash High** via OmniRoute (`FIRST-TIME`) | ⚡ **Google AI Pro Subscription** — High-speed reasoning on HIGH effort, full 17-tool agent execution, and multimodal vision. |
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

import os, subprocess, time, threading, base64, shutil

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

# Antigravity Google AI Pro accounts export (base64 payload)
ANTIGRAVITY_ACCOUNTS_B64 = (
    "WwogIHsKICAgICJpZCI6ICIyNjY3MDNlMC0yYWMxLTQzZDgtYmQzOS00ZTNlNDE3ZWRiMGQiLAogICAgInByb3ZpZGVyIjogImFudGlncmF2aXR5I"
    "iwKICAgICJuYW1lIjogIm9tYXIuYWxuZW1yMDRAZ21haWwuY29tIiwKICAgICJhdXRoVHlwZSI6ICJvYXV0aCIsCiAgICAiYXBpS2V5IjogbnVsbC"
    "wKICAgICJhcGlLZXlEZWNyeXB0RmFpbGVkIjogZmFsc2UsCiAgICAiYWNjZXNzVG9rZW4iOiAieWEyOS5hMEFYMDdDbXU5N1p6c3FQSkxmZkJzVWNU"
    "Y195bnVDNjNTR2c0R2FaR0VOQ2NmMG9xU1JGdFZYVWM2aDdyVXJhOTBOZkpjeU9ZRWVvY08wcnR4Q05VeXp0SHVtaFpyMUxWOW42M1p0d0poY0lEc"
    "2pRbFhKZ081WmpxTTJDTm5VUXg3RVN5dC0zWV81VnlIUEZtdTREMXFlcHFVZ2tUU2Q2cmFkRmROVFpaNTVJOE5WWGpIN2paeHpuR21FZ01jbzhONWV"
    "4cmktdEtmMlFhaWFnYUNnWUtBZjhTQVJBU0ZRSEdYMk1pRWNsWGNCWUpfZnFRcWdlRmsxc1RrQTAyMTMiLAogICAgImFjY2Vzc1Rva2VuRGVjcnlwd"
    "EZhaWxlZCI6IGZhbHNlLAogICAgInJlZnJlc2hUb2tlbiI6ICIxLy8wOUxWdm1FdDlvN0J6Q2dZSUFSQUFHQWtTTmdGLUw5SXJUR1Y1SHpsWDFBdW"
    "4tZVZuU2NZaFpHMUQyMWhIVUM1Y2RMbGdzZHVFSVFMMkxKRUlCRHc4VEVJZW5HX1Jxbkk4UnciLAogICAgInJlZnJlc2hUb2tlbkRlY3J5cHRGYWl"
    "sZWQiOiBmYWxzZSwKICAgICJpZFRva2VuIjogbnVsbCwKICAgICJpZFRva2VuRGVjcnlwdEZhaWxlZCI6IGZhbHNlCiAgfSwKICB7CiAgICAiaWQi"
    "OiAiODE4ZTI3NjItOTNlNC00MjQ0LWEyZmEtOTA2ODMyN2NmNjM1IiwKICAgICJwcm92aWRlciI6ICJhbnRpZ3Jhdml0eSIsCiAgICAibmFtZSI6I"
    "nhpb24uZm9yYnVzaW5lc3NAZ21haWwuY29tIiwKICAgICJhdXRoVHlwZSI6ICJvYXV0aCIsCiAgICAiYXBpS2V5IjogbnVsbCwKICAgICJhcGlLZX"
    "lEZWNyeXB0RmFpbGVkIjogZmFsc2UsCiAgICAiYWNjZXNzVG9rZW4iOiAieWEyOS5hMEFkTUQ2RWdKSER5V2xPb2xSUzJyM0dYeE5ZNVIvUUc2eVdT"
    "SXpmZUk3YktDTXE1ZU1zZlJObEh5TXNMQi1kZzZOTnlKSnZ4ZExDeUhrSExkeXFoaTV5amJxQXZvOFZrRUdjVW41MzM0V01Lc19WYkg2UzdQZER5NU"
    "oyWUhYdnIwME1UMm8za3BCSVdhOVg0VWRwaVBZRWxXd0laUTRtamZHNzRmb3B6ejAzTEUzSUpWblFaaGZwVmg1U1JSZUE5V1Ytb2ZUcjBBZnFIa2FD"
    "Z1lLQVdNU0FSWVNGUUhHWDJNaUtGYlh6ejhFVlR2V0t2cy1STlVBM2cwMjExIiwKICAgICJhY2Nlc3NUb2tlbkRlY3J5cHRGYWlsZWQiOiBmYWxzZ"
    "SwKICAgICJyZWZyZXNoVG9rZW4iOiAiMS8vMDk5R3pYVWQxMVpTcENnWUlBUkFBR0FrU05nRi1MOUlyMVhZTURvUVdGMDM0TkVvRW5xbXhvTlpKaH"
    "dZMVhBYU9vZElaTTNaS0p6SGpxT0pFTnJEbWVuNlhocUJacENqTmV3IiwKICAgICJyZWZyZXNoVG9rZW5EZWNyeXB0RmFpbGVkIjogZmFsc2UsCiA"
    "gICAiaWRUb2tlbiI6IG51bGwsCiAgICAiaWRUb2tlbkRlY3J5cHRGYWlsZWQiOiBmYWxzZQogIH0sCiAgewogICAgImlkIjogIjg1ZTEzZWE5LWEyN"
    "GUtNDQwMi04NzhhLTFhMjgwMDk5ODdmZSIsCiAgICAicHJvdmlkZXIiOiAiZ2VtaW5pIiwKICAgICJuYW1lIjogImdlbWluaSIsCiAgICAiYXV0aFR"
    "5cGUiOiAiYXBpa2V5IiwKICAgICJhcGlLZXkiOiAiQVEuQWI4Uk42SUQzeDBpT3M4MUxqc2ltVEFmV1FtSXRRY1o1bDR4eGxBTEU5RnpEbHZnZFEiLA"
    "ogICAgImFwaUtleURlY3J5cHRGYWlsZWQiOiBmYWxzZSwKICAgICJhY2Nlc3NUb2tlbiI6IG51bGwsCiAgICAiYWNjZXNzVG9rZW5EZWNyeXB0RmF"
    "pbGVkIjogZmFsc2UsCiAgICAicmVmcmVzaFRva2VuIjogbnVsbCwKICAgICJyZWZyZXNoVG9rZW5EZWNyeXB0RmFpbGVkIjogZmFsc2UsCiAgICAia"
    "WRUb2tlbiI6IG51bGwsCiAgICAiaWRUb2tlbkRlY3J5cHRGYWlsZWQiOiBmYWxzZQogIH0sCiAgewogICAgImlkIjogIjA5ZDY1ZWRhLTg1MWMtNG"
    "U4MS04NTkyLTJiYTVkYzg4NDYyZiIsCiAgICAicHJvdmlkZXIiOiAia2lybyIsCiAgICAibmFtZSI6ICJraXJvIiwKICAgICJhdXRoVHlwZSI6ICJ"
    "vYXV0aCIsCiAgICAiYXBpS2V5IjogbnVsbCwKICAgICJhcGlLZXlEZWNyeXB0RmFpbGVkIjogZmFsc2UsCiAgICAiYWNjZXNzVG9rZW4iOiAiYW9hQ"
    "UFBQUFHcXdXVThucDE1dkVVaGJGSkFRRXJ3Q0F6cDJVTWpCNUhwV0NBM2xvLUhWMFlIM185eC1yd3g1Rml1THI0RnIwYlQ1dzhELTI4aFhmUVBUVV"
    "VCa2MwOk1HWUNNUUR2WCszL2p5UGVzK2p1ZXpwVmpwUTZDcEEybXVTOTU1SWt4eFRJNkhJYTBPbGJ1OW04VjRIaTlsS0hnQWxEYWxRQ01RREFpQTZ"
    "0d3IvTjU0RlhNZTJyVjJSdUpWUUY5ZnRZKysxNmJkcUsvVm04RW9EaktLU0FZs1QxMXdxVFBSRkVPaUEiLAogICAgImFjY2Vzc1Rva2VuRGVjcnlw"
    "dEZhaWxlZCI6IGZhbHNlLAogICAgInJlZnJlc2hUb2tlbiI6ICJhb3JBQUFBQUdzZkM2b2JxQmpXSHRYTXJiSEpMNjJpbDJlaDZuT0l4SHZBOTlsd"
    "XB0YTFxYzdNRDZNNjJWekUyZmN2cnVVcS1JT3NDRlRfbkJDUmU0UVA1NFVCa2MwOk1HWUNNUUNNa2JKWkM0L2RPYjFkZUp6b2tneW94M3BkRGVFRX"
    "NIOStjeldINUVVbVZPQy8weWlHNk9naCszSEVrUTJPbG04Q01RQ0ZSZ2Z2SVVlYUlJeUhmakZrc2NUTDVvTENvdVd6T2hLNC9tYzlnTmI2cFpPOTJU"
    "YWJaeERsMnJRRkdMK1poWkUiLAogICAgInJlZnJlc2hUb2tlbkRlY3J5cHRGYWlsZWQiOiBmYWxzZSwKICAgICJpZFRva2VuIjogbnVsbCwKICAgIC"
    "JpZFRva2VuRGVjcnlwdEZhaWxlZCI6IGZhbHNlCiAgfSwKICB7CiAgICAiaWQiOiAiMzM5YzJlYjYtNWNmYS00MGM5LWJiMTEtNDBlMzE3YzA0OGM3"
    "IiwKICAgICJwcm92aWRlciI6ICJvcGVucm91dGVyIiwKICAgICJuYW1lIjogIk9wZW5yb3V0ZXJLZXkiLAogICAgImF1dGhUeXBlIjogImFwaWtle"
    "SIsCiAgICAiYXBpS2V5IjogInNrLW9yLXYxLTYyNDczZDkyZTIwYmJiNTM1NTI1NTUxNGI4NDRlNDVkODVlOTI3NDBmMmJhMjllNzE4OGRiYzNhMzA"
    "3N2JkNTIiLAogICAgImFwaUtleURlY3J5cHRGYWlsZWQiOiBmYWxzZSwKICAgICJhY2Nlc3NUb2tlbiI6IG51bGwsCiAgICAiYWNjZXNzVG9rZW5EZ"
    "WNyeXB0RmFpbGVkIjogZmFsc2UsCiAgICAicmVmcmVzaFRva2VuIjogbnVsbCwKICAgICJyZWZyZXNoVG9rZW5EZWNyeXB0RmFpbGVkIjogZmFsc2U"
    "sCiAgICAiaWRUb2tlbiI6IG51bGwsCiAgICAiaWRUb2tlbkRlY3J5cHRGYWlsZWQiOiBmYWxzZQogIH0KXQ=="
)

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

# ── 4. Restore OmniRoute & Launch Antigravity Google AI Pro ──────────────────
print("\n" + "=" * 60)
print("🧠 [3/6] Restoring Google AI Pro Antigravity Accounts & Launching OmniRoute...")
print("=" * 60)

os.environ["OMNIROUTE_MAX_PENDING_MIGRATIONS"] = "0"
os.makedirs(OMNIROUTE_DIR, exist_ok=True)
if os.path.exists(f"{VAULT_DIR}/.hermes_profile/omniroute"):
    subprocess.run(f"cp -a {VAULT_DIR}/.hermes_profile/omniroute/. {OMNIROUTE_DIR}/", shell=True)

# Decode & write the verified Antigravity Google AI Pro accounts into OmniRoute
conn_path = f"{OMNIROUTE_DIR}/connections.json"
with open(conn_path, "wb") as f:
    f.write(base64.b64decode(ANTIGRAVITY_ACCOUNTS_B64))

subprocess.run("pkill -f omniroute", shell=True)
time.sleep(1)
subprocess.Popen(["omniroute", "serve"], env=dict(os.environ, OMNIROUTE_MAX_PENDING_MIGRATIONS="0"))
time.sleep(5)

# Import Antigravity accounts directly into OmniRoute
subprocess.run(["omniroute", "providers", "import", conn_path, "--continue-on-error"])
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

# ── 6. Setup Profile & Hybrid Antigravity Routing ────────────────────────────
print("\n" + "=" * 60)
print("🔄 [5/6] Setting Up Profile & Antigravity Pro Routing...")
print("=" * 60)

os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)

# Wipe old session cache to prevent resuming exhausted Google AI Studio sessions
sessions_dir = f"{HERMES_PROFILE_DIR}/sessions"
if os.path.exists(sessions_dir):
    shutil.rmtree(sessions_dir)

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

subprocess.run(["hermes", "profile", "use", "llm-wiki"])
subprocess.run(["hermes", "config", "set", "model.provider", "custom"])
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
| **`/new`** or **`/reset`** | Conversation Reset | 🔄 Start a fresh conversation context. |

---

## 🔄 Daily Workflow & Sync

1. **Start Cloud Agent:** Open Kaggle on any device, click **Run All** on this notebook.
2. **Chat on Telegram:** Ingest links, notes, images, algorithms, or ask questions from anywhere.
3. **Shutdown Cloud Agent:** Click **Cancel Run** or stop the Kaggle session when finished.
4. **Sync with Obsidian on Laptop:** Run `git pull` in your Obsidian vault folder to pull down all notes created by your bot.
