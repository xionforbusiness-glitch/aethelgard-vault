# ==============================================================================
# 🏛️ AETHELGARD MASTER HYBRID CLOUD RUNNER
# ==============================================================================
# Architecture:
# 1. 🧠 High-IQ Brain: OmniRoute Cloud Daemon -> Antigravity (Claude Sonnet 4.6 / Gemini 3.7 Flash)
# 2. ⚡ Local GPU Engine: Ollama Dual Tesla T4 GPUs -> Qwen 2.5 (32B / 14B)
# 3. 🤖 Autonomous Agent: Hermes Agent (llm-wiki) listening on Telegram 24/7 on-demand
# 4. 📁 Data Persistence: Automatic 3-minute Git Sync to Private GitHub Repo
# ==============================================================================

import os
import subprocess
import time
import threading

# ── 1. Credentials & Configuration ────────────────────────────────────────────
GITHUB_USER = "xionforbusiness-glitch"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "PASTE_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE")
REPO_NAME = "aethelgard-vault"
REPO_BRANCH = "main"

# Paste your Telegram Bot Token from @BotFather below:
TELEGRAM_BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"

VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE_DIR = "/root/.hermes/profiles/llm-wiki"
OMNIROUTE_DIR = "/root/.omniroute"

# ── 2. System Prerequisites & Node.js ─────────────────────────────────────────
print("\n" + "=" * 60)
print("🚀 [1/6] Installing System Dependencies, Node.js & OmniRoute...")
print("=" * 60)

subprocess.run("apt-get update -y && apt-get install -y zstd git curl nodejs npm", shell=True, check=True)
subprocess.run("npm install -g omniroute", shell=True, check=True)
subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
subprocess.run("pip install -q hermes-agent requests", shell=True, check=True)

# ── 3. Clone / Sync Aethelgard Vault from GitHub ──────────────────────────────
print("\n" + "=" * 60)
print("📁 [2/6] Pulling Aethelgard Vault, Profiles & Antigravity Keys...")
print("=" * 60)

auth_repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

if os.path.exists(VAULT_DIR):
    subprocess.run(["git", "-C", VAULT_DIR, "pull", "origin", REPO_BRANCH])
else:
    subprocess.run(["git", "clone", auth_repo_url, VAULT_DIR], check=True)

subprocess.run(["git", "-C", VAULT_DIR, "config", "user.name", "Kaggle Hybrid Custodian"])
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.email", "agent@aethelgard.local"])

# ── 4. Restore OmniRoute & Start Cloud Antigravity Gateway ────────────────────
print("\n" + "=" * 60)
print("🧠 [3/6] Restoring Antigravity Connections & Launching OmniRoute...")
print("=" * 60)

os.makedirs(OMNIROUTE_DIR, exist_ok=True)
if os.path.exists(f"{VAULT_DIR}/.hermes_profile/omniroute"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/omniroute/* {OMNIROUTE_DIR}/", shell=True)

# Start OmniRoute Server in Background
subprocess.run("pkill -f omniroute", shell=True)
time.sleep(1)
subprocess.Popen(["omniroute", "serve"])
time.sleep(5)

# Verify OmniRoute Status
subprocess.run(["omniroute", "status"])

# ── 5. Start Ollama GPU Daemon & Pull Qwen 2.5 ─────────────────────────────────
print("\n" + "=" * 60)
print("⚡ [4/6] Launching Ollama Engine on Dual Tesla T4 GPUs...")
print("=" * 60)

os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
os.environ["OLLAMA_ORIGINS"] = "*"
subprocess.run("pkill -f ollama", shell=True)
time.sleep(2)
subprocess.Popen(["ollama", "serve"])
time.sleep(4)

print("📥 Loading Qwen 2.5 into Dual T4 VRAM (~29 GB)...")
subprocess.run(["ollama", "pull", "qwen2.5:14b"], check=True)  # Or switch to "qwen2.5:32b"

# ── 6. Setup Hermes Profile & Environment ─────────────────────────────────────
os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)
if os.path.exists(f"{VAULT_DIR}/.hermes_profile"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/SOUL.md {HERMES_PROFILE_DIR}/", shell=True)
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/config.yaml {HERMES_PROFILE_DIR}/", shell=True)
    if os.path.exists(f"{VAULT_DIR}/.hermes_profile/skills"):
        subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/skills {HERMES_PROFILE_DIR}/", shell=True)

os.environ["WIKI_PATH"] = VAULT_DIR
os.environ["OBSIDIAN_VAULT_PATH"] = VAULT_DIR
os.environ["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN

# ── 7. Auto-Sync Worker (Pushes to GitHub every 3 minutes) ────────────────────
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

# ── 8. Launch Hermes Telegram Gateway ─────────────────────────────────────────
print("\n" + "=" * 60)
print("🤖 [6/6] HERMES HYBRID TELEGRAM GATEWAY ONLINE (ANTIGRAVITY + DUAL T4 GPU)")
print("=" * 60)

try:
    subprocess.run(["hermes", "gateway", "--profile", "llm-wiki", "--platform", "telegram"])
finally:
    print("\n[Shutdown] Performing final vault backup to GitHub...")
    sync_vault("Final session sync before Kaggle GPU shutdown")
    print("✨ Clean shutdown complete. 0 quota wasted.")
