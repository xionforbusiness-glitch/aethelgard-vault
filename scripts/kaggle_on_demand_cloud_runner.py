# ==============================================================================
# AETHELGARD CLOUD RUNNER — ON-DEMAND SMART NOTEBOOK SCRIPT
# ==============================================================================
# Usage:
# 1. Open Kaggle Notebook (GPU: Dual T4, Internet: ON).
# 2. Paste this entire script into a single cell.
# 3. Fill in your GITHUB_TOKEN, GITHUB_USER, REPO_NAME, and TELEGRAM_BOT_TOKEN.
# 4. Click "Run All" whenever you want to activate your AI Wiki Agent.
# 5. When finished, send "/shutdown" on Telegram or click "Stop" on Kaggle.
# ==============================================================================

import os
import subprocess
import time
import threading
import signal
import sys

# ------------------------------------------------------------------------------
# 1. Configuration & Credentials
# ------------------------------------------------------------------------------
GITHUB_USER = "PASTE_YOUR_GITHUB_USERNAME_HERE"
GITHUB_TOKEN = "PASTE_YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE"
REPO_NAME = "aethelgard-vault"
REPO_BRANCH = "master"  # or "main"

TELEGRAM_BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "PASTE_YOUR_TELEGRAM_CHAT_ID_OPTIONAL"

IDLE_TIMEOUT_MINUTES = 30  # Auto-shuts down if inactive to preserve weekly quota

VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE_DIR = "/root/.hermes/profiles/llm-wiki"

# ------------------------------------------------------------------------------
# 2. Prerequisites & Ollama GPU Engine
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("🚀 [Step 1/5] Initializing Environment & Installing Dependencies...")
print("=" * 60)

subprocess.run("apt-get update -y && apt-get install -y zstd git curl", shell=True, check=True)
subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
subprocess.run("pip install -q hermes-agent requests", shell=True, check=True)

# ------------------------------------------------------------------------------
# 3. Launch Ollama Daemon & Load Model
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("⚡ [Step 2/5] Launching Ollama Daemon on Dual Tesla T4 GPUs...")
print("=" * 60)

os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
os.environ["OLLAMA_ORIGINS"] = "*"

subprocess.run("pkill -f ollama", shell=True)
time.sleep(2)

ollama_proc = subprocess.Popen(["ollama", "serve"])
time.sleep(4)

print("📥 Pulling Qwen 2.5 14B weights into VRAM...")
subprocess.run(["ollama", "pull", "qwen2.5:14b"], check=True)

# ------------------------------------------------------------------------------
# 4. Clone / Sync Obsidian Vault & Profile
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("📁 [Step 3/5] Synchronizing Aethelgard Vault & Profile from GitHub...")
print("=" * 60)

auth_repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

if os.path.exists(VAULT_DIR):
    print("Pulling latest vault changes from remote...")
    subprocess.run(["git", "-C", VAULT_DIR, "pull", "origin", REPO_BRANCH])
else:
    print("Cloning private repository...")
    subprocess.run(["git", "clone", auth_repo_url, VAULT_DIR], check=True)

# Set Git Identity for Auto-Commits
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.name", "Kaggle Cloud Agent"])
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.email", "agent@aethelgard.local"])

# Copy Profile Configuration
os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)
if os.path.exists(f"{VAULT_DIR}/.hermes_profile"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/* {HERMES_PROFILE_DIR}/", shell=True)

# Set Vault Environment
os.environ["WIKI_PATH"] = VAULT_DIR
os.environ["OBSIDIAN_VAULT_PATH"] = VAULT_DIR
os.environ["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN

# ------------------------------------------------------------------------------
# 5. Git Auto-Sync Engine
# ------------------------------------------------------------------------------
def sync_vault(commit_msg="Auto-sync from Kaggle Cloud Agent"):
    try:
        subprocess.run(["git", "-C", VAULT_DIR, "add", "."], check=True)
        res = subprocess.run(["git", "-C", VAULT_DIR, "commit", "-m", commit_msg], capture_output=True, text=True)
        if "nothing to commit" not in res.stdout:
            subprocess.run(["git", "-C", VAULT_DIR, "push", "origin", REPO_BRANCH], check=True)
            print(f"[Vault Sync] Changes pushed to GitHub: {commit_msg}")
            return True
    except Exception as e:
        print(f"[Vault Sync Error] {e}")
    return False

def auto_sync_worker():
    while True:
        time.sleep(180)  # Check every 3 minutes
        sync_vault()

sync_thread = threading.Thread(target=auto_sync_worker, daemon=True)
sync_thread.start()

# ------------------------------------------------------------------------------
# 6. Telegram Startup Ping
# ------------------------------------------------------------------------------
def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID or "PASTE_" in TELEGRAM_CHAT_ID:
        return
    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[Telegram Alert Error] {e}")

send_telegram_alert("🏛️ *Aethelgard Vault Agent is Online!*\nDual Tesla T4 GPUs activated on Kaggle. You can send queries, notes, and media now.")

# ------------------------------------------------------------------------------
# 7. Start Hermes Gateway
# ------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("🤖 [Step 5/5] Launching Hermes Telegram Gateway...")
print("=" * 60)

try:
    # Run the gateway
    hermes_proc = subprocess.run(["hermes", "gateway", "--profile", "llm-wiki", "--platform", "telegram"])
except KeyboardInterrupt:
    print("\nSession interrupted by user.")
finally:
    print("\n[Shutdown] Performing final vault backup to GitHub...")
    sync_vault("Final sync before Kaggle session termination")
    send_telegram_alert("💤 *Aethelgard Vault Agent Session Ended.*\nAll changes synced to GitHub. GPU shutdown to preserve quota.")
    print("✨ Clean shutdown complete.")
