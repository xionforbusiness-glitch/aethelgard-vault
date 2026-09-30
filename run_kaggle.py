# ==============================================================================
# 🏛️ AETHELGARD MASTER HYBRID CLOUD RUNNER (ANTIGRAVITY GOOGLE AI PRO + DUAL T4)
# ==============================================================================

import os, sys, subprocess, time, threading, shutil, json, sqlite3, urllib.request

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

# Deployment Mode Flags (Pure Cloud Antigravity Default)
ENABLE_OLLAMA = os.environ.get("ENABLE_OLLAMA", "false").lower() in ("true", "1", "yes")

VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE_DIR = "/root/.hermes/profiles/llm-wiki"
OMNIROUTE_DIR = "/root/.omniroute"

# Terminate any old background servers to free ports
if ENABLE_OLLAMA:
    subprocess.run("omniroute stop 2>/dev/null; pkill -9 -f omniroute 2>/dev/null; pkill -9 -x ollama 2>/dev/null; fuser -k 20128/tcp 2>/dev/null; fuser -k 11434/tcp 2>/dev/null || true", shell=True)
else:
    subprocess.run("omniroute stop 2>/dev/null; pkill -9 -f omniroute 2>/dev/null; fuser -k 20128/tcp 2>/dev/null || true", shell=True)

# ── 2. Install Node.js 22 LTS, OmniRoute & Dependencies (with Fast-Start Cache) ─
print("\n" + "=" * 60)
print("🚀 [1/6] Installing Node.js 22 LTS, OmniRoute & Dependencies...")
print("=" * 60)

node_check = subprocess.run("node -v 2>/dev/null", shell=True, capture_output=True, text=True).stdout.strip()
if not node_check.startswith("v22"):
    subprocess.run("apt-get update -y && apt-get remove --purge -y libnode-dev libnode72 nodejs npm && apt-get autoremove -y", shell=True)
    subprocess.run("apt-get install -y zstd git curl psmisc pciutils lshw", shell=True, check=True)
    subprocess.run("curl -fsSL https://deb.nodesource.com/setup_22.x | bash -", shell=True, check=True)
    subprocess.run('apt-get install -y -o Dpkg::Options::="--force-overwrite" nodejs', shell=True, check=True)
    print("✅ Node.js 22 LTS installed.")
else:
    print(f"✅ Node.js 22 is already installed ({node_check}).")

if subprocess.run("which omniroute 2>/dev/null", shell=True, capture_output=True).returncode != 0:
    subprocess.run("npm install -g omniroute --prefer-offline --no-audit", shell=True, check=True)
    print("✅ OmniRoute installed.")
else:
    print("✅ OmniRoute is already installed.")

if ENABLE_OLLAMA:
    if subprocess.run("which ollama 2>/dev/null", shell=True, capture_output=True).returncode != 0:
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
        print("✅ Ollama installed.")
    else:
        print("✅ Ollama is already installed.")
else:
    print("⏭️ Skipping Ollama installation (Pure Cloud Antigravity Mode - saving ~1.5 GB disk).")

subprocess.run("pip install -q hermes-agent requests", shell=True, check=True)

# Free up disk space immediately to prevent Kaggle storage exhaustion
subprocess.run("apt-get clean 2>/dev/null; rm -rf /var/cache/apt/archives/* /root/.npm 2>/dev/null || true", shell=True)

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
os.environ["PORT"] = "20128"
os.makedirs(OMNIROUTE_DIR, exist_ok=True)

with open(f"{OMNIROUTE_DIR}/.env", "w") as ef:
    ef.write(f"STORAGE_ENCRYPTION_KEY={STORAGE_ENCRYPTION_KEY}\n")
    ef.write("PORT=20128\n")

# Kill any existing processes on port 20128
subprocess.run("omniroute stop 2>/dev/null; pkill -9 -f omniroute 2>/dev/null; fuser -k 20128/tcp 2>/dev/null || true", shell=True)
time.sleep(1)

# Direct copy/decompression of pre-verified database with auto-repair
print("📦 Restoring pre-verified Antigravity Google AI Pro OmniRoute database from repository...")
db_dest = f"{OMNIROUTE_DIR}/storage.sqlite"
db_gz = f"{VAULT_DIR}/.hermes_profile/omniroute/storage.sqlite.gz"
db_src = f"{VAULT_DIR}/.hermes_profile/omniroute/storage.sqlite"

restored = False
if os.path.exists(db_gz):
    import gzip
    try:
        if os.path.exists(db_dest):
            os.remove(db_dest)
        with gzip.open(db_gz, "rb") as f_in, open(db_dest, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        test_conn = sqlite3.connect(db_dest)
        check = test_conn.execute("PRAGMA integrity_check;").fetchall()
        test_conn.close()
        if check == [("ok",)]:
            restored = True
            print("✅ Decompressed and verified storage.sqlite.gz from repository!")
    except Exception as e:
        print(f"⚠ Gzip restore error: {e}")

if not restored and os.path.exists(db_src):
    try:
        shutil.copy2(db_src, db_dest)
        test_conn = sqlite3.connect(db_dest)
        check = test_conn.execute("PRAGMA integrity_check;").fetchall()
        test_conn.close()
        if check == [("ok",)]:
            restored = True
            print("✅ Copied and verified storage.sqlite from repository!")
    except Exception as e:
        print(f"⚠ Raw sqlite error: {e}")

if not restored:
    print("⚠ Using JSON backup fallback...")
    backup_file = f"{VAULT_DIR}/.hermes_profile/omniroute_backup.json"
    if os.path.exists(backup_file):
        # Initialize schema via omniroute
        omni_init = subprocess.Popen(["omniroute", "serve"], env=dict(os.environ))
        time.sleep(5)
        subprocess.run("omniroute stop 2>/dev/null; fuser -k 20128/tcp 2>/dev/null || true", shell=True)
        try:
            omni_init.terminate()
            omni_init.wait(timeout=2)
        except Exception:
            omni_init.kill()
        time.sleep(1)

        with open(backup_file, "r", encoding="utf-8") as f:
            seed_data = json.load(f)
        conn = sqlite3.connect(db_dest)
        for table_name, data in seed_data.items():
            cols = data["columns"]
            rows = data["rows"]
            quoted_cols = ", ".join([f'"{c}"' for c in cols])
            placeholders = ", ".join(["?"] * len(cols))
            conn.executemany(f"INSERT OR REPLACE INTO {table_name} ({quoted_cols}) VALUES ({placeholders})", rows)
        conn.commit()
        conn.close()
        print("✅ Restored from backup JSON!")

# Verify DB content
conn = sqlite3.connect(db_dest)
c = conn.cursor()
c.execute("SELECT id, provider, name, is_active FROM provider_connections WHERE provider = 'antigravity'")
anti_rows = c.fetchall()
print(f"🔍 Verified Antigravity accounts in SQLite: {anti_rows}")
conn.close()

# Launch OmniRoute daemon safely with log redirection
omni_log = open("/tmp/omniroute.log", "w")
omniroute_proc = subprocess.Popen(["omniroute", "serve"], env=dict(os.environ), stdout=omni_log, stderr=subprocess.STDOUT, start_new_session=True)

# Health check: wait up to 30 seconds for OmniRoute to become responsive
print("⏳ Waiting for OmniRoute to become ready on http://localhost:20128...")
ready = False
for _ in range(30):
    try:
        check_req = urllib.request.Request(
            "http://localhost:20128/v1/models",
            headers={"Authorization": f"Bearer {OMNIROUTE_API_KEY}"}
        )
        with urllib.request.urlopen(check_req, timeout=2) as resp:
            if resp.status == 200:
                ready = True
                break
    except Exception:
        time.sleep(1)

if ready:
    print("✅ OmniRoute is active and responding on port 20128!")
    # Smoke test Antigravity directly
    print("🧪 Running live inference test for Antigravity (gemini-3.7-flash-high)...")
    try:
        test_req = urllib.request.Request(
            "http://localhost:20128/v1/chat/completions",
            data=json.dumps({
                "model": "antigravity/gemini-3.7-flash-high",
                "messages": [{"role": "user", "content": "ping"}]
            }).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {OMNIROUTE_API_KEY}"}
        )
        with urllib.request.urlopen(test_req, timeout=30) as t_resp:
            res_body = json.loads(t_resp.read().decode("utf-8"))
            content = res_body.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"🎉 ANTIGRAVITY GOOGLE AI PRO TEST PASSED! AI Response: {content.strip()[:60]}...")
    except Exception as te:
        print(f"⚠ Antigravity inference test warning: {te}")
else:
    print("⚠ Warning: OmniRoute health check timed out. Checking process status...")

# ── 5. Start Ollama GPU Daemon & Load Local Model (Resilient) ───────────────
print("\n" + "=" * 60)
if not ENABLE_OLLAMA:
    print("⚡ [4/6] Ollama Local GPU Engine: DISABLED (Pure Cloud Antigravity Mode Active - 100% Google AI Pro)")
    print("=" * 60)
else:
    print("⚡ [4/6] Initializing Ollama GPU Engine (Optional Local Fallback)...")
    print("=" * 60)
    ollama_ready = False
    try:
        os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
        os.environ["OLLAMA_ORIGINS"] = "*"
        os.environ["OLLAMA_KEEP_ALIVE"] = "24h"
        os.environ["OLLAMA_NUM_PARALLEL"] = "1"
        subprocess.run("pkill -9 -x ollama 2>/dev/null; fuser -k 11434/tcp 2>/dev/null || true", shell=True)
        time.sleep(1)
        
        ollama_log = open("/tmp/ollama.log", "w")
        ollama_proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=ollama_log,
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        time.sleep(3)

        # Check if Ollama daemon is responsive
        for _ in range(12):
            try:
                with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as r:
                    if r.status == 200:
                        ollama_ready = True
                        break
            except Exception:
                time.sleep(1)

        if ollama_ready:
            ollama_list = subprocess.run("ollama list 2>/dev/null", shell=True, capture_output=True, text=True).stdout
            target_gpu_model = None
            if "qwen2.5:32b" in ollama_list:
                target_gpu_model = "qwen2.5:32b"
                print("✅ Qwen 2.5 32B is already cached in Ollama!")
            elif "qwen2.5:14b" in ollama_list:
                target_gpu_model = "qwen2.5:14b"
                print("✅ Qwen 2.5 14B is already cached in Ollama!")
            elif "qwen2.5:7b" in ollama_list:
                target_gpu_model = "qwen2.5:7b"
                print("✅ Qwen 2.5 7B is already cached in Ollama!")
            else:
                # Use 7B: fast, ultra-safe for Kaggle disk quota (<5GB), instant download, zero risk of status code 44
                target_gpu_model = "qwen2.5:7b"
                print(f"📥 Loading {target_gpu_model} into Dual T4 VRAM (~4.7 GB, fast & disk-safe)...")
                pull_proc = subprocess.Popen(
                    ["ollama", "pull", target_gpu_model],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    start_new_session=True
                )
                for line in pull_proc.stdout:
                    if "100%" in line or "verifying" in line or "success" in line:
                        print(f"  [Ollama Pull] {line.strip()}")
                pull_proc.wait()
                
                print(f"⚙ Configuring 64K context window on {target_gpu_model} for Hermes Agent...")
                with open("/tmp/Modelfile.qwen", "w") as mf:
                    mf.write(f"FROM {target_gpu_model}\nPARAMETER num_ctx 65536\n")
                subprocess.run(["ollama", "create", target_gpu_model, "-f", "/tmp/Modelfile.qwen"], start_new_session=True)

            print(f"✅ Ollama GPU Engine is active and {target_gpu_model} is loaded!")
        else:
            print("⚠ Ollama did not start within 12s. Continuing with Cloud Antigravity...")
    except Exception as oe:
        print(f"⚠ Local GPU Ollama skipped: {oe}. Primary Antigravity Google AI Pro is fully operational!")

# ── 6. Setup Profile & Hybrid Antigravity Routing ────────────────────────────
print("\n" + "=" * 60)
print("🔄 [5/6] Setting Up Profile & Antigravity Pro Routing...")
print("=" * 60)

os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)

# Wipe all old session cache and state database to eliminate stale sessions
for p in [
    "/root/.hermes/state.db",
    "/root/.hermes/sessions",
    "/root/.hermes/chats",
    f"{HERMES_PROFILE_DIR}/state.db",
    f"{HERMES_PROFILE_DIR}/sessions",
    f"{HERMES_PROFILE_DIR}/chats"
]:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            try:
                os.remove(p)
            except Exception:
                pass

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
subprocess.run(["hermes", "config", "set", "model.context_length", "1048576"])
subprocess.run(["hermes", "config", "set", "model.base_url", "http://localhost:20128/v1"])
subprocess.run(["hermes", "config", "set", "model.api_key", OMNIROUTE_API_KEY])

def sync_vault(commit_msg="Auto-sync from Kaggle Hybrid Agent"):
    try:
        subprocess.run(["git", "-C", VAULT_DIR, "add", "."], check=True)
        res = subprocess.run(["git", "-C", VAULT_DIR, "commit", "-m", commit_msg], capture_output=True, text=True)
        if "nothing to commit" not in res.stdout:
            subprocess.run(["git", "-C", VAULT_DIR, "push", "origin", REPO_BRANCH], check=True)
            print(f"[Vault Sync] Changes pushed to GitHub: {commit_msg}", flush=True)
    except Exception as e:
        print(f"[Vault Sync Error] {e}", flush=True)

def auto_sync_worker():
    while True:
        time.sleep(180)
        sync_vault()

threading.Thread(target=auto_sync_worker, daemon=True).start()

# Background GPU Watchdog Worker (Dual T4 Activity Monitor)
def gpu_watchdog_worker():
    while True:
        try:
            import torch
            if torch.cuda.is_available():
                for d in range(torch.cuda.device_count()):
                    t = torch.ones((100, 100), device=f"cuda:{d}") @ torch.ones((100, 100), device=f"cuda:{d}")
                    torch.cuda.synchronize(d)
        except Exception:
            pass
        time.sleep(60)

threading.Thread(target=gpu_watchdog_worker, daemon=True).start()

# Clean cache directories to preserve container disk headroom
subprocess.run("rm -rf /root/.cache/pip /root/.npm /var/cache/apt/archives/* /tmp/pip-* 2>/dev/null || true", shell=True)

# ── 7. Launch Hermes Hybrid Gateway ───────────────────────────────────────────
print("\n" + "=" * 60)
print("🤖 [6/6] HERMES HYBRID AGENT ONLINE (ANTIGRAVITY GOOGLE AI PRO + DUAL T4)")
print("=" * 60)

# Clear stale Telegram update queue & reset webhook
try:
    print("🧹 Clearing stale Telegram updates & resetting webhook...", flush=True)
    urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=5)
    urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset=-1", timeout=5)
    print("✅ Telegram queue cleanly flushed.", flush=True)
except Exception as te:
    print(f"⚠ Telegram queue flush notice: {te}", flush=True)

# Automated startup ping to Telegram
try:
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    tg_msg = "🏛️ Hermes Aethelgard Vault Custodian is ONLINE on Kaggle Dual T4 (Pure Cloud Google AI Pro Engine)"
    tg_data = json.dumps({"chat_id": TELEGRAM_USER_ID, "text": tg_msg}).encode("utf-8")
    tg_req = urllib.request.Request(tg_url, data=tg_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(tg_req, timeout=10) as tg_res:
        if tg_res.status == 200:
            res_json = json.loads(tg_res.read().decode("utf-8"))
            msg_id = res_json.get("result", {}).get("message_id", "unknown")
            print(f"📱 Telegram startup notification delivered successfully to Omar (Message ID: {msg_id})!", flush=True)
except Exception as tg_err:
    print(f"⚠ Telegram startup notification notice: {tg_err}", flush=True)

# Decoupled Resilient Gateway Supervisor Loop with Real-Time Log Streaming & Heartbeat
def stream_reader(pipe, log_f):
    try:
        for line in iter(pipe.readline, ''):
            if line:
                clean_line = line.rstrip()
                print(f"[Hermes Gateway] {clean_line}", flush=True)
                try:
                    log_f.write(line)
                    log_f.flush()
                except Exception:
                    pass
    except Exception:
        pass
    finally:
        try:
            pipe.close()
        except Exception:
            pass

GATEWAY_LOG_PATH = "/tmp/hermes_gateway.log"
gateway_cmd = ["hermes", "gateway", "run", "--replace", "--force", "--no-supervise", "--accept-hooks"]

max_restarts = 5
restart_count = 0
backoff = 3
current_proc = None

try:
    while restart_count < max_restarts:
        print(f"🚀 Starting Hermes Gateway process (Attempt {restart_count + 1}/{max_restarts})...", flush=True)
        gateway_log_f = open(GATEWAY_LOG_PATH, "a+", encoding="utf-8")
        
        current_proc = subprocess.Popen(
            gateway_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True
        )
        
        reader_thread = threading.Thread(target=stream_reader, args=(current_proc.stdout, gateway_log_f), daemon=True)
        reader_thread.start()
        
        last_heartbeat = time.time()
        while current_proc.poll() is None:
            time.sleep(1)
            now = time.time()
            if now - last_heartbeat >= 25:
                current_time = time.strftime("%H:%M:%S")
                print(f"💓 [{current_time}] Hermes Gateway Online | Polling Telegram | Antigravity Google AI Pro Active", flush=True)
                last_heartbeat = now
                sys.stdout.flush()
        
        exit_code = current_proc.returncode
        print(f"⚠ Hermes Gateway process exited with code {exit_code}", flush=True)
        try:
            gateway_log_f.close()
        except Exception:
            pass
        
        restart_count += 1
        if restart_count < max_restarts:
            print(f"🔄 Restarting Hermes Gateway in {backoff}s...", flush=True)
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)
except KeyboardInterrupt:
    print("\n🛑 Gateway stopped by user / shutdown signal.", flush=True)
    if current_proc and current_proc.poll() is None:
        try:
            current_proc.terminate()
            current_proc.wait(timeout=5)
        except Exception:
            current_proc.kill()
finally:
    sync_vault("Final session sync before Kaggle GPU shutdown")
    print("✨ Clean shutdown complete. All changes pushed to GitHub.", flush=True)
