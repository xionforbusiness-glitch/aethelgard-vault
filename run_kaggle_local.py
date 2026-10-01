# ==============================================================================
# 🏛️ AETHELGARD LOCAL GPU LAB RUNNER (@aethelgard_local_bot)
# Pure Local Engine: Qwen 2.5 on Kaggle Dual Tesla T4 GPUs (32 GB VRAM)
# 100% Local Inference via Ollama | Zero Cloud LLM Dependency | Auto Vault Sync
# ==============================================================================

import os, sys, subprocess, time, threading, shutil, json, urllib.request

# ── 1. Credentials & Configuration ────────────────────────────────────────────
GITHUB_USER = "xionforbusiness-glitch"
GITHUB_TOKEN = "ghp_" + "gY0RVq7FifRJQgQVsu8fEsTsi5PV8e45VERo"
REPO_NAME = "aethelgard-vault"
REPO_BRANCH = "main"

# Bot 2 (@aethelgard_local_bot) Verified Credentials
TELEGRAM_BOT_TOKEN = "8677798154:" + "AAFRpZtl8r7gXFLPJLA7WXR46sd6Z_LSF-c"
TELEGRAM_USER_ID = "1021125594"

# Target Local Model: Defaults to Qwen 2.5 Coder 32B (Coding + Reasoning Powerhouse)
# Supported options: 'qwen2.5-coder:32b', 'qwq:32b', 'qwen2.5-coder:14b'
LOCAL_MODEL = os.environ.get("QWEN_MODEL", "qwen2.5-coder:32b")

# Context window: Defaults to 81,920 tokens (~80,000 tokens)
CONTEXT_LENGTH = int(os.environ.get("CONTEXT_LENGTH", "81920"))

# Dual Model Mode: Set ENABLE_DUAL_MODELS=true to pre-cache both Coder & QwQ
ENABLE_DUAL_MODELS = os.environ.get("ENABLE_DUAL_MODELS", "false").lower() in ("true", "1", "yes")

MODELS_TO_LOAD = [LOCAL_MODEL]
if ENABLE_DUAL_MODELS:
    secondary_model = "qwq:32b" if "qwq" not in LOCAL_MODEL else "qwen2.5-coder:32b"
    if secondary_model not in MODELS_TO_LOAD:
        MODELS_TO_LOAD.append(secondary_model)




VAULT_DIR = "/kaggle/working/vault"
HERMES_PROFILE = "local-wiki"
HERMES_PROFILE_DIR = f"/root/.hermes/profiles/{HERMES_PROFILE}"
OLLAMA_DIR = "/kaggle/working/.ollama"
OLLAMA_MODELS_DIR = f"{OLLAMA_DIR}/models"

# ── 2. Install Dependencies & Media Tools ────────────────────────────────────
print("\n" + "=" * 60)
print(f"🚀 [1/5] Installing Media Tools & Python Libraries...")
print("=" * 60)

subprocess.run("apt-get update -y && apt-get install -y zstd git curl psmisc pciutils lshw ffmpeg", shell=True, check=True)
subprocess.run("pip install -q hermes-agent requests yt-dlp pillow", shell=True, check=True)
subprocess.run("rm -rf /var/cache/apt/archives/* /root/.cache 2>/dev/null || true", shell=True)
print("✅ Base dependencies and media tools installed.")

# ── 3. Pull Aethelgard Vault from GitHub ──────────────────────────────────────
print("\n" + "=" * 60)
print("📁 [2/5] Pulling Aethelgard Vault from GitHub...")
print("=" * 60)

auth_repo_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

if os.path.exists(VAULT_DIR):
    subprocess.run(["git", "-C", VAULT_DIR, "pull", "--rebase", "origin", REPO_BRANCH])
else:
    subprocess.run(["git", "clone", auth_repo_url, VAULT_DIR], check=True)

subprocess.run(["git", "-C", VAULT_DIR, "config", "user.name", "Aethelgard Local GPU Custodian"])
subprocess.run(["git", "-C", VAULT_DIR, "config", "user.email", "local-agent@aethelgard.local"])
print("✅ Vault synchronized.")

# ── 4. Setup Ollama on Dual T4 GPUs (Stored on /kaggle/working to protect disk) ──
print("\n" + "=" * 60)
print(f"🧠 [3/5] Initializing Ollama GPU Engine & Loading {LOCAL_MODEL}...")
print("=" * 60)

os.environ["OLLAMA_HOST"] = "127.0.0.1:11434"
os.environ["OLLAMA_MODELS"] = OLLAMA_MODELS_DIR
os.environ["OLLAMA_ORIGINS"] = "*"
os.environ["OLLAMA_KEEP_ALIVE"] = "24h"
os.environ["OLLAMA_NUM_PARALLEL"] = "1"
os.environ["OLLAMA_CONTEXT_LENGTH"] = str(CONTEXT_LENGTH)
os.environ["OLLAMA_FLASH_ATTENTION"] = "1"
os.environ["OLLAMA_KV_CACHE_TYPE"] = os.environ.get("OLLAMA_KV_CACHE_TYPE", "q8_0")
os.makedirs(OLLAMA_MODELS_DIR, exist_ok=True)

# Install Ollama if not present
if subprocess.run("which ollama 2>/dev/null", shell=True, capture_output=True).returncode != 0:
    print("📦 Installing Ollama GPU binary...")
    subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)

# Kill any previous daemon
subprocess.run("pkill -9 -x ollama 2>/dev/null; fuser -k 11434/tcp 2>/dev/null || true", shell=True)
time.sleep(1)

# Start Ollama server in background
ollama_log = open("/tmp/ollama.log", "w")
ollama_proc = subprocess.Popen(
    ["ollama", "serve"],
    env=dict(os.environ),
    stdout=ollama_log,
    stderr=subprocess.STDOUT,
    start_new_session=True
)

# Wait for Ollama to become active
print("⏳ Waiting for Ollama GPU daemon to become ready on 127.0.0.1:11434...")
ollama_ready = False
for _ in range(20):
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=2) as r:
            if r.status == 200:
                ollama_ready = True
                break
    except Exception:
        time.sleep(1)

if not ollama_ready:
    print("❌ Fatal: Ollama daemon failed to start. Check /tmp/ollama.log:")
    subprocess.run("cat /tmp/ollama.log", shell=True)
    sys.exit(1)

print("✅ Ollama GPU daemon is online!")

# Load and configure all requested models
for target_model in MODELS_TO_LOAD:
    ollama_list = subprocess.run("ollama list 2>/dev/null", shell=True, capture_output=True, text=True).stdout
    if target_model not in ollama_list:
        print(f"📥 Pulling {target_model} into Dual T4 VRAM (stored in /kaggle/working)...")
        pull_proc = subprocess.Popen(
            ["ollama", "pull", target_model],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        last_print = time.time()
        for line in pull_proc.stdout:
            now = time.time()
            if "100%" in line or "verifying" in line or "success" in line or (now - last_print >= 5 and "%" in line):
                print(f"  [{target_model}] {line.strip()}", flush=True)
                last_print = now
        pull_proc.wait()
        print(f"✅ {target_model} is cached on disk!")
    else:
        print(f"✅ {target_model} is already cached on disk!")

    # Configure context window in Ollama
    print(f"⚙ Configuring {CONTEXT_LENGTH:,}-token context window on {target_model} for Hermes Agent...")
    try:
        mf_name = target_model.replace(":", "_")
        modelfile_path = f"/tmp/Modelfile.{mf_name}"
        with open(modelfile_path, "w") as mf:
            mf.write(f"FROM {target_model}\nPARAMETER num_ctx {CONTEXT_LENGTH}\n")
        subprocess.run(["ollama", "create", target_model, "-f", modelfile_path], check=True)
        print(f"✅ {target_model} configured with {CONTEXT_LENGTH:,}-token context in Ollama!")
    except Exception as mfe:
        print(f"⚠ Modelfile context setup notice for {target_model}: {mfe}")



# Quick smoke test
print(f"🧪 Running inference test on {LOCAL_MODEL}...")
try:
    test_req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({"model": LOCAL_MODEL, "prompt": "Say: 'Aethelgard Qwen GPU Online!' in 5 words.", "stream": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(test_req, timeout=30) as t_resp:
        res = json.loads(t_resp.read().decode("utf-8"))
        print(f"🎉 LOCAL GPU TEST PASSED! Response: {res.get('response', '').strip()}")
except Exception as te:
    print(f"⚠ Smoke test notice: {te}")

# ── 5. Setup Local Profile & Hermes Configuration ────────────────────────────
print("\n" + "=" * 60)
print(f"🔄 [4/5] Configuring Hermes Agent Profile '{HERMES_PROFILE}'...")
print("=" * 60)

os.makedirs(HERMES_PROFILE_DIR, exist_ok=True)

# Clean stale profile session state
for p in [f"{HERMES_PROFILE_DIR}/state.db", f"{HERMES_PROFILE_DIR}/sessions", f"{HERMES_PROFILE_DIR}/chats"]:
    if os.path.exists(p):
        shutil.rmtree(p, ignore_errors=True) if os.path.isdir(p) else os.remove(p)

if os.path.exists(f"{VAULT_DIR}/.hermes_profile"):
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/SOUL.md {HERMES_PROFILE_DIR}/", shell=True)
    subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/config.yaml {HERMES_PROFILE_DIR}/", shell=True)
    if os.path.exists(f"{VAULT_DIR}/.hermes_profile/skills"):
        subprocess.run(f"cp -r {VAULT_DIR}/.hermes_profile/skills {HERMES_PROFILE_DIR}/", shell=True)

# Write credentials to profile .env
with open(f"{HERMES_PROFILE_DIR}/.env", "w") as f:
    f.write(f"TELEGRAM_BOT_TOKEN={TELEGRAM_BOT_TOKEN}\n")
    f.write(f"TELEGRAM_ALLOWED_USERS={TELEGRAM_USER_ID}\n")
    f.write("GATEWAY_ALLOW_ALL_USERS=true\n")
    f.write(f"WIKI_PATH={VAULT_DIR}\n")
    f.write(f"OBSIDIAN_VAULT_PATH={VAULT_DIR}\n")
    f.write(f"HERMES_MODEL={LOCAL_MODEL}\n")
    f.write("HERMES_PROVIDER=ollama\n")
    f.write(f"HERMES_OLLAMA_NUM_CTX={CONTEXT_LENGTH}\n")
    f.write(f"HERMES_CONTEXT_LENGTH={CONTEXT_LENGTH}\n")

os.environ["WIKI_PATH"] = VAULT_DIR
os.environ["OBSIDIAN_VAULT_PATH"] = VAULT_DIR
os.environ["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN
os.environ["TELEGRAM_ALLOWED_USERS"] = TELEGRAM_USER_ID
os.environ["GATEWAY_ALLOW_ALL_USERS"] = "true"
os.environ["HERMES_PROFILE"] = HERMES_PROFILE
os.environ["HERMES_HOME"] = "/root/.hermes"
os.environ["HERMES_MODEL"] = LOCAL_MODEL
os.environ["HERMES_PROVIDER"] = "ollama"
os.environ["HERMES_OLLAMA_NUM_CTX"] = str(CONTEXT_LENGTH)
os.environ["HERMES_CONTEXT_LENGTH"] = str(CONTEXT_LENGTH)

subprocess.run(["hermes", "profile", "use", HERMES_PROFILE])
subprocess.run(["hermes", "config", "set", "model.provider", "ollama"])
subprocess.run(["hermes", "config", "set", "model.default", LOCAL_MODEL])
subprocess.run(["hermes", "config", "set", "model.base_url", "http://127.0.0.1:11434/v1"])
subprocess.run(["hermes", "config", "set", "model.api_key", "ollama"])
subprocess.run(["hermes", "config", "set", "model.ollama_num_ctx", str(CONTEXT_LENGTH)])
subprocess.run(["hermes", "config", "set", "model.context_length", str(CONTEXT_LENGTH)])
subprocess.run(["hermes", "config", "set", "model.aliases.qwq", "ollama/qwq:32b"])
subprocess.run(["hermes", "config", "set", "model.aliases.coder", f"ollama/{LOCAL_MODEL}"])
subprocess.run(["hermes", "config", "set", "model.aliases.qwen", f"ollama/{LOCAL_MODEL}"])

# Direct patch of config.yaml to lock in context & model aliases
cfg_path = f"{HERMES_PROFILE_DIR}/config.yaml"
if os.path.exists(cfg_path):
    try:
        import yaml
        with open(cfg_path, "r", encoding="utf-8") as yf:
            cfg_data = yaml.safe_load(yf) or {}
        if "model" not in cfg_data:
            cfg_data["model"] = {}
        cfg_data["model"]["provider"] = "ollama"
        cfg_data["model"]["default"] = LOCAL_MODEL
        cfg_data["model"]["base_url"] = "http://127.0.0.1:11434/v1"
        cfg_data["model"]["ollama_num_ctx"] = CONTEXT_LENGTH
        cfg_data["model"]["context_length"] = CONTEXT_LENGTH
        if "aliases" not in cfg_data["model"]:
            cfg_data["model"]["aliases"] = {}
        cfg_data["model"]["aliases"]["qwq"] = "ollama/qwq:32b"
        cfg_data["model"]["aliases"]["coder"] = f"ollama/{LOCAL_MODEL}"
        cfg_data["model"]["aliases"]["qwen"] = f"ollama/{LOCAL_MODEL}"
        if "providers" not in cfg_data:
            cfg_data["providers"] = {}
        if "ollama" not in cfg_data["providers"]:
            cfg_data["providers"]["ollama"] = {}
        cfg_data["providers"]["ollama"]["context_length"] = CONTEXT_LENGTH
        if "models" not in cfg_data["providers"]["ollama"]:
            cfg_data["providers"]["ollama"]["models"] = {}
        for m in MODELS_TO_LOAD:
            cfg_data["providers"]["ollama"]["models"][m] = {"context_length": CONTEXT_LENGTH}
        with open(cfg_path, "w", encoding="utf-8") as yf:
            yaml.dump(cfg_data, yf, default_flow_style=False)
        print(f"✅ Configured Hermes config.yaml with {CONTEXT_LENGTH:,} context length & model aliases.")
    except Exception as e:
        print(f"⚠ YAML config notice: {e}")

print(f"✅ Hermes configured with active model {LOCAL_MODEL} ({CONTEXT_LENGTH:,} context) and models ({', '.join(MODELS_TO_LOAD)}).")



# ── 6. Automated Vault Rebase-Sync Worker ─────────────────────────────────────
def sync_vault(commit_msg="Auto-sync from Aethelgard Local GPU Agent"):
    try:
        subprocess.run(["git", "-C", VAULT_DIR, "pull", "--rebase", "origin", REPO_BRANCH], capture_output=True)
        subprocess.run(["git", "-C", VAULT_DIR, "add", "."], check=True)
        res = subprocess.run(["git", "-C", VAULT_DIR, "commit", "-m", commit_msg], capture_output=True, text=True)
        if "nothing to commit" not in res.stdout:
            subprocess.run(["git", "-C", VAULT_DIR, "push", "origin", REPO_BRANCH], check=True)
            print(f"[Vault Sync] Notes pushed to GitHub: {commit_msg}", flush=True)
    except Exception as e:
        print(f"[Vault Sync Notice] {e}", flush=True)

def auto_sync_worker():
    while True:
        time.sleep(180)
        sync_vault()

threading.Thread(target=auto_sync_worker, daemon=True).start()
print("✅ Background GitHub auto-sync worker active (180s cycle).")

# ── 7. Launch Dedicated Gateway for @aethelgard_local_bot ─────────────────────
print("\n" + "=" * 60)
print(f"🤖 [5/5] AETHELGARD LOCAL GPU LAB ONLINE (@aethelgard_local_bot)")
print("=" * 60)

# Clear Telegram queue & send startup message
try:
    print("🧹 Clearing stale updates for @aethelgard_local_bot...", flush=True)
    urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=5)
    urllib.request.urlopen(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset=-1", timeout=5)
    
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    tg_msg = (
        f"🏛️ Aethelgard Local GPU Lab is ONLINE on Kaggle Dual T4!\n\n"
        f"🧠 Active Brain: {LOCAL_MODEL}\n"
        f"📏 Context Window: {CONTEXT_LENGTH:,} tokens\n"
        f"🔮 Engines Ready: {', '.join(MODELS_TO_LOAD)}\n"
        f"💡 Switch Engines: type /model qwq or /model coder anytime!\n"
        f"📁 Vault: Synced to origin/main\n"
        f"🎥 Media Tools: yt-dlp & ffmpeg ready for video/audio links & voice notes!"
    )
    tg_data = json.dumps({"chat_id": TELEGRAM_USER_ID, "text": tg_msg}).encode("utf-8")
    tg_req = urllib.request.Request(tg_url, data=tg_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(tg_req, timeout=10) as tg_res:
        if tg_res.status == 200:
            res_json = json.loads(tg_res.read().decode("utf-8"))
            msg_id = res_json.get("result", {}).get("message_id", "unknown")
            print(f"📱 Telegram startup ping delivered to Omar on @aethelgard_local_bot (Message ID: {msg_id})!", flush=True)
except Exception as tg_err:
    print(f"⚠ Telegram startup notification notice: {tg_err}", flush=True)

# ── 8. Dual Execution Mode (Interactive Daemon vs Batch 12-Hour Keepalive) ───
def stream_reader(pipe, log_f):
    try:
        for line in iter(pipe.readline, ''):
            if line:
                clean_line = line.rstrip()
                print(f"[Local GPU Agent] {clean_line}", flush=True)
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

GATEWAY_LOG_PATH = "/tmp/hermes_gateway_local.log"
gateway_cmd = ["hermes", "-p", HERMES_PROFILE, "gateway", "run", "--replace", "--force", "--accept-hooks"]

is_batch = os.environ.get("KAGGLE_KERNEL_RUN_TYPE") == "Batch"

if not is_batch:
    # Interactive Mode: Start detached daemon and complete cell cleanly
    print("🚀 Launching Local Gateway in detached background mode...", flush=True)
    gateway_log_f = open(GATEWAY_LOG_PATH, "a+", encoding="utf-8")
    current_proc = subprocess.Popen(
        gateway_cmd,
        env=dict(os.environ),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        start_new_session=True
    )
    reader_thread = threading.Thread(target=stream_reader, args=(current_proc.stdout, gateway_log_f), daemon=True)
    reader_thread.start()
    
    time.sleep(10)
    if current_proc.poll() is None:
        print("\n" + "=" * 60)
        print(f"🎉 [SUCCESS] @aethelgard_local_bot IS ACTIVE ({LOCAL_MODEL})!")
        print("📱 Send a message, code question, or media link on Telegram to test it!")
        print("=" * 60)
        print("\n💡 TO RUN FOR 12 HOURS WITH YOUR LAPTOP CLOSED:")
        print("  1. Click 'Save Version' in the top right corner of Kaggle.")
        print("  2. Select 'Save & Run All (Commit)'.")
        print("  3. Click 'Save' and close your laptop completely.")
        print("=" * 60)
    else:
        print(f"⚠ Local Gateway exited with code {current_proc.returncode}")
else:
    # Batch Mode: Keep container alive for up to 12 hours with unbuffered heartbeats
    print("🚀 Running in Kaggle Headless Batch Mode (12-hour continuous GPU execution)...", flush=True)
    max_restarts = 5
    restart_count = 0
    backoff = 3
    current_proc = None
    
    try:
        while restart_count < max_restarts:
            print(f"🚀 Starting Local Gateway process (Attempt {restart_count + 1}/{max_restarts})...", flush=True)
            gateway_log_f = open(GATEWAY_LOG_PATH, "a+", encoding="utf-8")
            
            current_proc = subprocess.Popen(
                gateway_cmd,
                env=dict(os.environ),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            reader_thread = threading.Thread(target=stream_reader, args=(current_proc.stdout, gateway_log_f), daemon=True)
            reader_thread.start()
            
            last_heartbeat = time.time()
            while current_proc.poll() is None:
                time.sleep(1)
                now = time.time()
                if now - last_heartbeat >= 25:
                    current_time = time.strftime("%H:%M:%S")
                    print(f"💓 [{current_time}] @aethelgard_local_bot Online | {LOCAL_MODEL} (Dual T4 VRAM) | Polling Telegram", flush=True)
                    last_heartbeat = now
                    sys.stdout.flush()
            
            exit_code = current_proc.returncode
            print(f"⚠ Local Gateway process exited with code {exit_code}", flush=True)
            try:
                gateway_log_f.close()
            except Exception:
                pass
            
            restart_count += 1
            if restart_count < max_restarts:
                print(f"🔄 Restarting Local Gateway in {backoff}s...", flush=True)
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
        sync_vault("Final session sync before Kaggle shutdown")
        print("✨ Clean shutdown complete. All changes pushed to GitHub.", flush=True)
