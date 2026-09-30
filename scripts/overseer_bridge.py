import datetime
import json
import os
import re
from typing import Dict, Any, Optional, Tuple
from fastapi import FastAPI, Request, Query, Header
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
import uvicorn

app = FastAPI(title="Project Overseer — Intelligent Content & Telemetry Engine")

VAULT_PATH = "C:/Users/omara/Desktop/vault/Aethelgard Vault"
LOG_FILE = os.path.join(VAULT_PATH, "log.md")
STATE_FILE = os.path.expanduser("~/.hermes/overseer_state.json")

# ==============================================================================
# 🧠 KNOWLEDGE & SEMANTIC TAXONOMY (Tailored to Omar Elnemr's Vault & Life)
# ==============================================================================

DOMAIN_TAXONOMY = {
    "AI_AND_AGENTS": {
        "label": "AI & Agent Systems",
        "keywords": [
            "ai", "agent", "agents", "llm", "hermes", "claude", "gpt", "deepseek", "openai", "anthropic",
            "machine learning", "deep learning", "neural", "rag", "langchain", "prompt", "prompting",
            "fine-tuning", "modernbert", "laya", "system 1", "rlcd", "rlhf", "rlvr", "omniroute",
            "transformer", "attention mechanism", "embedding", "vector database", "lora", "qlora",
            "onnx", "tensorrt", "cuda", "model architecture", "synthetic data"
        ],
        "weight": 1.2
    },
    "COMPUTER_VISION": {
        "label": "Computer Vision & Deep Learning",
        "keywords": [
            "computer vision", "opencv", "cv2", "yolo", "yolov8", "yolov9", "yolov10", "yolo11",
            "ultralytics", "object detection", "segmentation", "image processing", "mtcnn", "arcface",
            "facial recognition", "camera calibration", "bounding box", "feature matching", "canny",
            "optical flow", "image tensors"
        ],
        "weight": 1.3
    },
    "ENGINEERING_AND_CODE": {
        "label": "Software Engineering & Dev",
        "keywords": [
            "python", "javascript", "typescript", "linux", "bash", "shell scripting", "docker",
            "fastapi", "uvicorn", "n8n", "git", "github", "data structures", "algorithms", "dsa",
            "asymptotic complexity", "big o", "software architecture", "coding tutorial", "backend",
            "frontend", "api", "rest api", "system design", "wireshark", "packet analysis", "openvpn",
            "networking protocol", "tcp", "udp", "dns", "reverse proxy", "c++", "cpp"
        ],
        "weight": 1.1
    },
    "EMBEDDED_AND_ROBOTICS": {
        "label": "Robotics & Microcontrollers",
        "keywords": [
            "arduino", "microcontroller", "robotics", "servo", "sg90", "stepper motor", "uln2003",
            "lego spike", "spike prime", "sensors", "actuators", "pwm", "i2c", "spi", "breadboard",
            "embedded c", "embedded systems", "electronic circuit", "joystick hw-504", "cad design", "3d modeling"
        ],
        "weight": 1.3
    },
    "ACADEMIC_AND_STUDY": {
        "label": "Academic & Higher Education",
        "keywords": [
            "university of the people", "uopeople", "syrian virtual university", "svu", "discrete math",
            "linear algebra", "calculus", "operating systems", "database systems", "computer science degree",
            "exam preparation", "study with me", "lecture", "course", "textbook", "academic research", "arxiv"
        ],
        "weight": 1.2
    },
    "SKILL_AND_HOBBIES": {
        "label": "Targeted Craft & Hobbies",
        "keywords": [
            "speedcubing", "cfop", "f2l", "oll", "pll", "rubik", "fingertricks", "sub-15", "sub-12", "cube solve",
            "aviation", "dcs world", "flight simulator", "saudia", "ground handling", "airport check-in",
            "air traffic control", "flight ops", "we happy few", "rain world", "narrative design"
        ],
        "weight": 1.1
    }
}

BRAINROT_INDICATORS = [
    # Short-form algorithms
    "shorts", "#shorts", "youtube shorts", "reels", "/reel/", "instagram reels", "tiktok", "tiktok compilation",
    # Low-signal / clickbait / drama tropes
    "prank", "funny meme", "meme review", "drama", "gossip", "exposed", "reacting to", "reaction video",
    "fails compilation", "try not to laugh", "challenge 24 hours", "satisfying soap", "subway surfers gameplay",
    "skibidi", "rage bait", "streamer drama", "influencer beef", "dating show", "asmr mukbang", "unboxing toys"
]

HIGH_RISK_APPS = ["instagram", "tiktok", "facebook", "snapchat", "tinder"]

UTILITY_APPS = [
    "clock", "calculator", "calendar", "settings", "files", "contacts",
    "dialer", "messages", "authenticator", "keepass", "bitwarden", "weather"
]

PRODUCTIVE_APPS = [
    "obsidian", "termux", "github", "slack", "vscode", "pycharm", "jupyter", "chatgpt", "claude", "anki"
]

# ==============================================================================
# 📊 PERSISTENT STATE MANAGEMENT
# ==============================================================================

def load_state() -> Dict[str, Any]:
    today_str = datetime.date.today().isoformat()
    default_state = {
        "date": today_str,
        "total_events": 0,
        "productive_events": 0,
        "distraction_events": 0,
        "neutral_events": 0,
        "current_streak_type": "none",
        "current_streak_count": 0,
        "max_productive_streak": 0,
        "max_distraction_streak": 0,
        "last_event_time": datetime.datetime.now().isoformat(),
        "recent_history": []
    }
    
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                # Reset if new day
                if state.get("date") != today_str:
                    state["date"] = today_str
                    state["total_events"] = 0
                    state["productive_events"] = 0
                    state["distraction_events"] = 0
                    state["neutral_events"] = 0
                    state["current_streak_type"] = "none"
                    state["current_streak_count"] = 0
                return state
        except Exception as e:
            print(f"Error reading state file: {e}")
            
    return default_state

def save_state(state: Dict[str, Any]):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Error saving state file: {e}")

# ==============================================================================
# 📝 VAULT LOGGING
# ==============================================================================

def log_to_vault(verdict: str, tag: str, app_name: str, title: str, streak: int, score: float):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_title = title.replace("\n", " ").strip() if title else "(No Title Provided)"
    
    entry = (
        f"\n## [{timestamp}] overseer | {verdict} | {tag}\n"
        f"- **App:** `{app_name}`\n"
        f"- **Content:** {clean_title}\n"
        f"- **Evaluation Score:** {score:+.2f} | **Current Streak:** {streak}\n"
    )
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"Error writing to log.md: {e}")

# ==============================================================================
# 🧠 SMART SEMANTIC CONTENT EVALUATOR
# ==============================================================================

def evaluate_smart_content(app_name: str, title: str, url: str = "", extra_text: str = "") -> Dict[str, Any]:
    """
    Evaluates mobile telemetry using contextual pattern matching,
    keyword density, app reputation, and domain weighting.
    """
    state = load_state()
    
    # Clean up unresolved MacroDroid magic text tokens like [not_title], [media_track], etc.
    def clean_token(val: str) -> str:
        if not val:
            return ""
        s = str(val).strip()
        if re.match(r"^\[.*?\]$", s) or re.match(r"^\{.*?\}$", s):
            return ""
        return s

    app_clean = clean_token(app_name) or app_name or "Unknown"
    title_clean = clean_token(title)
    url_clean = clean_token(url)
    extra_clean = clean_token(extra_text)
    
    app_lower = app_clean.lower().strip()
    title_lower = title_clean.lower().strip()
    url_lower = url_clean.lower().strip()
    extra_lower = extra_clean.lower().strip()
    
    full_text = f"{app_lower} {title_lower} {url_lower} {extra_lower}"
    
    # 1. Check for utility apps first
    if any(u in app_lower for u in UTILITY_APPS) and not title_lower:
        verdict = "utility"
        domain_tag = "System Utility"
        speech = f"{app_name.capitalize()} open."
        score = 0.0
        state["neutral_events"] += 1
        state["current_streak_type"] = "neutral"
        state["current_streak_count"] = 1
        save_state(state)
        return {
            "verdict": verdict,
            "tag": domain_tag,
            "score": score,
            "speak": speech,
            "streak": state["current_streak_count"],
            "streak_type": state["current_streak_type"]
        }

    # 2. Check for explicit Productive Workspaces (Obsidian, Termux, Anki, GitHub)
    is_dedicated_productive_app = any(p in app_lower for p in PRODUCTIVE_APPS)
    
    # 3. Calculate Domain Alignment Scores
    matched_domains = []
    productive_score = 0.0
    
    for domain_key, domain_data in DOMAIN_TAXONOMY.items():
        matches = [kw for kw in domain_data["keywords"] if re.search(r'\b' + re.escape(kw) + r'\b', full_text)]
        if matches:
            weight = domain_data["weight"]
            pts = len(matches) * weight
            productive_score += pts
            matched_domains.append((domain_data["label"], matches, pts))
            
    # 4. Calculate Brainrot & Distraction Signals
    brainrot_matches = [bw for bw in BRAINROT_INDICATORS if bw in full_text]
    is_high_risk_app = any(hr in app_lower for hr in HIGH_RISK_APPS)
    
    distraction_penalty = len(brainrot_matches) * 2.0
    if is_high_risk_app:
        # If strong technical keywords match and NO brainrot indicator is present, allow the educational exception
        if productive_score >= 1.5 and not brainrot_matches:
            distraction_penalty += 0.0
        else:
            distraction_penalty += 3.0
            
    if "shorts" in full_text or "reels" in full_text or "/reel/" in full_text:
        distraction_penalty += 4.0
        
    net_score = productive_score - distraction_penalty
    
    # 5. Determine Final Verdict
    if is_dedicated_productive_app or (productive_score >= 1.2 and distraction_penalty < 3.0):
        # High-Value Learning / Deep Work
        primary_domain = matched_domains[0][0] if matched_domains else "Productive Engineering"
        verdict = "productive"
        domain_tag = primary_domain
        
        state["productive_events"] += 1
        if state["current_streak_type"] == "productive":
            state["current_streak_count"] += 1
        else:
            state["current_streak_type"] = "productive"
            state["current_streak_count"] = 1
            
        state["max_productive_streak"] = max(state["max_productive_streak"], state["current_streak_count"])
        
        # Build natural spoken coaching message
        clean_title = title[:45] if title else primary_domain
        streak = state["current_streak_count"]
        
        if streak == 1:
            speech = f"Study topic recognized: {clean_title}. High value focus, Omar."
        elif streak in [3, 5, 10]:
            speech = f"Excellent consistency! {streak} productive study milestones in a row."
        else:
            speech = f"Continuing deep work on {clean_title}."
            
    elif distraction_penalty > productive_score or is_high_risk_app or brainrot_matches:
        # Distraction / Doomscrolling
        verdict = "distraction"
        domain_tag = "Doomscrolling / Distraction"
        
        state["distraction_events"] += 1
        if state["current_streak_type"] == "distraction":
            state["current_streak_count"] += 1
        else:
            state["current_streak_type"] = "distraction"
            state["current_streak_count"] = 1
            
        state["max_distraction_streak"] = max(state["max_distraction_streak"], state["current_streak_count"])
        streak = state["current_streak_count"]
        
        clean_title = title[:35] if title else app_name
        
        # Escalating coaching intervention tone
        if streak == 1:
            speech = f"Notice: you just opened {clean_title}. Keep your daily engineering goals in mind."
        elif streak == 2:
            speech = f"Second distraction detected. Step away from {app_name} and protect your focus."
        elif streak == 3:
            speech = f"Warning: 3 consecutive distractions. You have active builds in the vault. Let's return to code."
        else:
            speech = f"Attention: Streak is at {streak}. Close {app_name} immediately and resume your priority roadmap."
            
    else:
        # Neutral / Exploration
        verdict = "neutral"
        domain_tag = "General Exploration"
        speech = f"Active on {app_name}."
        state["neutral_events"] += 1
        state["current_streak_type"] = "neutral"
        state["current_streak_count"] = 1

    state["total_events"] += 1
    state["last_event_time"] = datetime.datetime.now().isoformat()
    state["recent_history"].insert(0, {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "app": app_name,
        "title": title[:60],
        "verdict": verdict,
        "score": round(net_score, 2)
    })
    state["recent_history"] = state["recent_history"][:25]
    
    save_state(state)
    log_to_vault(verdict, domain_tag, app_name, title, state["current_streak_count"], net_score)
    
    return {
        "verdict": verdict,
        "tag": domain_tag,
        "score": round(net_score, 2),
        "speak": speech,
        "streak": state["current_streak_count"],
        "streak_type": state["current_streak_type"]
    }

# ==============================================================================
# 🌐 API ENDPOINTS
# ==============================================================================

@app.post("/webhook/phone-event")
async def phone_event(request: Request, format: Optional[str] = Query(None)):
    """
    Main webhook handler for Android MacroDroid / Tasker.
    Accepts app_name, media_track, not_title, not_text, and content_title.
    Combines available telemetry into full semantic context.
    """
    try:
        data = await request.json()
    except Exception:
        data = {}
        
    def clean_val(v):
        if not v:
            return ""
        s = str(v).strip()
        if re.match(r"^\[.*?\]$", s) or re.match(r"^\{.*?\}$", s):
            return ""
        return s

    # Extract all possible fields sent by MacroDroid triggers
    raw_app_input = data.get("app_name") or data.get("not_app") or data.get("package_name") or ""
    app_raw = clean_val(raw_app_input)
    if not app_raw or app_raw.lower() in ["unknown", "foreground_app_name"]:
        # Try to infer app from raw input string or other payload fields
        raw_str = str(raw_app_input) + " " + str(data.get("not_title", "")) + " " + str(data.get("extra", ""))
        raw_lower = raw_str.lower()
        if "youtube" in raw_lower:
            app_raw = "YouTube"
        elif "facebook" in raw_lower:
            app_raw = "Facebook"
        elif "telegram" in raw_lower:
            app_raw = "Telegram"
        elif "whatsapp" in raw_lower:
            app_raw = "WhatsApp"
        elif "instagram" in raw_lower:
            app_raw = "Instagram"
        elif "tiktok" in raw_lower:
            app_raw = "TikTok"
        else:
            app_raw = "YouTube" if "youtube" in str(request.url).lower() else "Phone Active"
    media_track = clean_val(data.get("media_track")) or clean_val(data.get("content_title")) or clean_val(data.get("title"))
    not_title = clean_val(data.get("not_title"))
    not_text = clean_val(data.get("not_text")) or clean_val(data.get("extra"))
    url = clean_val(data.get("url"))
    
    # Compose composite title from whichever trigger supplied info
    titles = [t for t in [media_track, not_title] if t]
    combined_title = " - ".join(titles) if titles else ""
    
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📲 Phone Event Received:")
    print(f"   -> App: '{app_raw}' | Title: '{combined_title}' | Extra: '{not_text}'")
    
    analysis = evaluate_smart_content(app_raw, combined_title, url, not_text)
    
    # Check if client expects plain text (default for mobile MacroDroid TTS)
    accept = request.headers.get("accept", "")
    if format == "json" or (format is None and "application/json" in accept and "text/plain" not in accept):
        return JSONResponse(content={
            "status": "received",
            "verdict": analysis["verdict"],
            "tag": analysis["tag"],
            "score": analysis["score"],
            "streak": analysis["streak"],
            "speak": analysis["speak"]
        })
    return PlainTextResponse(content=analysis["speak"])

@app.get("/status")
async def get_status():
    state = load_state()
    total = state.get("total_events", 0)
    prod = state.get("productive_events", 0)
    dist = state.get("distraction_events", 0)
    focus_ratio = round((prod / total * 100), 1) if total > 0 else 100.0
    
    return {
        "status": "online",
        "date": state.get("date"),
        "focus_score_percent": focus_ratio,
        "total_events": total,
        "productive_events": prod,
        "distraction_events": dist,
        "current_streak": {
            "type": state.get("current_streak_type"),
            "count": state.get("current_streak_count")
        },
        "recent_history": state.get("recent_history", [])[:10]
    }

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Project Overseer — Cozy Telemetry Hub</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #12131c;
                --card-bg: rgba(28, 30, 45, 0.75);
                --card-border: rgba(255, 255, 255, 0.08);
                --text-main: #f1f5f9;
                --text-muted: #94a3b8;
                --accent-emerald: #10b981;
                --accent-emerald-soft: rgba(16, 185, 129, 0.15);
                --accent-sky: #38bdf8;
                --accent-sky-soft: rgba(56, 189, 248, 0.15);
                --accent-purple: #c084fc;
                --accent-purple-soft: rgba(192, 132, 252, 0.15);
                --accent-rose: #fb7185;
                --accent-rose-soft: rgba(251, 113, 133, 0.15);
                --accent-amber: #fbbf24;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--bg);
                background-image: 
                    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.06) 0px, transparent 50%),
                    radial-gradient(at 50% 50%, rgba(16, 185, 129, 0.04) 0px, transparent 50%);
                background-attachment: fixed;
                color: var(--text-main);
                min-height: 100vh;
                padding: 30px 20px;
                display: flex;
                justify-content: center;
                -webkit-font-smoothing: antialiased;
            }

            .container {
                width: 100%;
                max-width: 960px;
            }

            /* Header */
            .header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 24px;
                padding-bottom: 16px;
                border-bottom: 1px solid var(--card-border);
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 14px;
            }

            .brand-icon {
                width: 44px;
                height: 44px;
                border-radius: 14px;
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
                box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
            }

            .brand-title {
                font-size: 20px;
                font-weight: 800;
                letter-spacing: -0.4px;
            }

            .brand-subtitle {
                font-size: 12.5px;
                color: var(--text-muted);
                font-weight: 500;
                margin-top: 2px;
            }

            .status-pill {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 6px 14px;
                border-radius: 9999px;
                background: var(--accent-emerald-soft);
                border: 1px solid rgba(16, 185, 129, 0.3);
                font-size: 11.5px;
                font-weight: 700;
                color: var(--accent-emerald);
                letter-spacing: 0.4px;
            }

            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--accent-emerald);
                box-shadow: 0 0 10px var(--accent-emerald);
                animation: pulse 2s infinite ease-in-out;
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.5; transform: scale(0.85); }
            }

            /* Metric Grid */
            .metric-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 14px;
                margin-bottom: 24px;
            }

            .metric-card {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 16px;
                padding: 18px 20px;
                backdrop-filter: blur(16px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }

            .metric-card:hover {
                transform: translateY(-2px);
                border-color: rgba(255, 255, 255, 0.16);
            }

            .metric-label {
                font-size: 11.5px;
                color: var(--text-muted);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                margin-bottom: 6px;
            }

            .metric-val {
                font-size: 28px;
                font-weight: 800;
                letter-spacing: -0.5px;
                line-height: 1.1;
            }

            .metric-sub {
                font-size: 11.5px;
                margin-top: 6px;
                font-weight: 500;
            }

            /* Simulation Actions */
            .quick-actions {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 16px;
                padding: 16px 20px;
                margin-bottom: 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                backdrop-filter: blur(16px);
            }

            .actions-label {
                font-size: 12.5px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .btn-group {
                display: flex;
                gap: 10px;
            }

            .btn {
                padding: 8px 14px;
                border-radius: 10px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                border: 1px solid transparent;
                transition: all 0.15s ease;
                display: flex;
                align-items: center;
                gap: 6px;
                font-family: inherit;
            }

            .btn-study {
                background: var(--accent-emerald-soft);
                color: var(--accent-emerald);
                border-color: rgba(16, 185, 129, 0.25);
            }
            .btn-study:hover { background: rgba(16, 185, 129, 0.25); }

            .btn-distraction {
                background: var(--accent-rose-soft);
                color: var(--accent-rose);
                border-color: rgba(251, 113, 133, 0.25);
            }
            .btn-distraction:hover { background: rgba(251, 113, 133, 0.25); }

            .btn-social {
                background: var(--accent-sky-soft);
                color: var(--accent-sky);
                border-color: rgba(56, 189, 248, 0.25);
            }
            .btn-social:hover { background: rgba(56, 189, 248, 0.25); }

            /* Feed Table */
            .feed-card {
                background: var(--card-bg);
                border: 1px solid var(--card-border);
                border-radius: 16px;
                overflow: hidden;
                backdrop-filter: blur(16px);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            }

            .feed-header {
                padding: 16px 22px;
                background: rgba(255, 255, 255, 0.02);
                border-bottom: 1px solid var(--card-border);
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .feed-title {
                font-size: 13px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.6px;
            }

            .table-container {
                width: 100%;
                overflow-x: auto;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
            }

            th {
                text-align: left;
                padding: 12px 20px;
                font-size: 11px;
                font-weight: 700;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border-bottom: 1px solid var(--card-border);
            }

            td {
                padding: 14px 20px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.04);
                color: #cbd5e1;
            }

            tr:last-child td { border-bottom: none; }
            tr:hover td { background: rgba(255, 255, 255, 0.02); }

            .app-badge {
                font-weight: 700;
                color: #e2e8f0;
            }

            .score-badge {
                padding: 4px 10px;
                border-radius: 9999px;
                font-size: 11.5px;
                font-weight: 700;
                font-family: 'JetBrains Mono', monospace;
                display: inline-block;
            }

            .score-productive {
                background: var(--accent-emerald-soft);
                color: var(--accent-emerald);
                border: 1px solid rgba(16, 185, 129, 0.25);
            }

            .score-distraction {
                background: var(--accent-rose-soft);
                color: var(--accent-rose);
                border: 1px solid rgba(251, 113, 133, 0.25);
            }

            .score-neutral {
                background: rgba(148, 163, 184, 0.12);
                color: #cbd5e1;
                border: 1px solid rgba(148, 163, 184, 0.2);
            }

            /* Live Toast for simulated events */
            #toast {
                position: fixed;
                bottom: 24px;
                right: 24px;
                padding: 14px 20px;
                background: #1e293b;
                border: 1px solid var(--card-border);
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                font-size: 13px;
                color: #f8fafc;
                display: none;
                align-items: center;
                gap: 10px;
                z-index: 1000;
                backdrop-filter: blur(20px);
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <div class="brand">
                    <div class="brand-icon">🛡️</div>
                    <div>
                        <div class="brand-title">Project Overseer</div>
                        <div class="brand-subtitle">Cozy Telemetry Hub • Aethelgard Vault</div>
                    </div>
                </div>
                <div class="status-pill">
                    <span class="status-dot"></span>
                    <span>LIVE STREAM ON PORT 5678</span>
                </div>
            </div>

            <!-- KPI Cards -->
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Focus Ratio</div>
                    <div class="metric-val" id="val-focus" style="color: var(--accent-sky);">--%</div>
                    <div class="metric-sub" id="sub-focus" style="color: var(--accent-emerald);">✨ Calculating flow</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Deep Work</div>
                    <div class="metric-val" id="val-prod" style="color: var(--accent-emerald);">--</div>
                    <div class="metric-sub" style="color: var(--accent-emerald);">🎓 High-value events</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Distractions</div>
                    <div class="metric-val" id="val-dist" style="color: var(--accent-rose);">--</div>
                    <div class="metric-sub" style="color: var(--accent-rose);">🛡️ Guarded events</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Study Streak</div>
                    <div class="metric-val" id="val-streak" style="color: var(--accent-purple);">--</div>
                    <div class="metric-sub" style="color: var(--accent-purple);">🔥 Active momentum</div>
                </div>
            </div>

            <!-- Quick Simulator Bar -->
            <div class="quick-actions">
                <div class="actions-label">⚡ Test Mobile Telemetry Triggers</div>
                <div class="btn-group">
                    <button class="btn btn-study" onclick="sendSimulated('YouTube', 'ModernBERT Architecture & Laya System 1 Decisions')">
                        <span>🎓</span> Simulate CV/AI Study
                    </button>
                    <button class="btn btn-social" onclick="sendSimulated('Facebook', 'Luis Buenaventura: Jev vs Laya Open Source Models')">
                        <span>💡</span> Simulate Tech Post
                    </button>
                    <button class="btn btn-distraction" onclick="sendSimulated('TikTok', 'Funny Memes 2026 Compilation')">
                        <span>🚨</span> Simulate Distraction
                    </button>
                </div>
            </div>

            <!-- Feed Table -->
            <div class="feed-card">
                <div class="feed-header">
                    <div class="feed-title">🧠 Real-Time Evaluator Stream</div>
                    <div style="font-size: 11.5px; color: var(--text-muted);">Auto-updating every 3s</div>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 90px;">Time</th>
                                <th style="width: 130px;">App</th>
                                <th>Content Title</th>
                                <th style="width: 140px;">Verdict</th>
                                <th style="width: 90px; text-align: right;">Score</th>
                            </tr>
                        </thead>
                        <tbody id="feed-tbody">
                            <tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 24px;">Loading live stream...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <div id="toast"></div>

        <script>
            async function fetchStatus() {
                try {
                    const res = await fetch('/status');
                    if (!res.ok) return;
                    const data = await res.json();
                    
                    document.getElementById('val-focus').innerText = data.focus_score_percent + '%';
                    document.getElementById('val-prod').innerText = data.productive_events + ' ev';
                    document.getElementById('val-dist').innerText = data.distraction_events + ' ev';
                    
                    const streakCount = data.current_streak ? data.current_streak.count : 0;
                    const streakType = data.current_streak ? data.current_streak.type : 'none';
                    document.getElementById('val-streak').innerText = streakCount + ' (' + streakType + ')';
                    
                    const tbody = document.getElementById('feed-tbody');
                    if (data.recent_history && data.recent_history.length > 0) {
                        let html = '';
                        for (const item of data.recent_history) {
                            const isProd = item.verdict === 'productive';
                            const isDist = item.verdict === 'distraction';
                            const badgeClass = isProd ? 'score-productive' : (isDist ? 'score-distraction' : 'score-neutral');
                            const icon = isProd ? '🎓' : (isDist ? '🚨' : '⚡');
                            const scoreFormatted = (item.score >= 0 ? '+' : '') + item.score.toFixed(2);
                            
                            html += `
                            <tr>
                                <td style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: var(--text-muted);">${item.time}</td>
                                <td><span class="app-badge">${item.app}</span></td>
                                <td style="color: #f1f5f9;">${item.title || '(No title)'}</td>
                                <td><span class="score-badge ${badgeClass}">${icon} ${item.verdict.toUpperCase()}</span></td>
                                <td style="text-align: right; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: ${isProd ? 'var(--accent-emerald)' : (isDist ? 'var(--accent-rose)' : 'var(--text-muted)')};">${scoreFormatted}</td>
                            </tr>
                            `;
                        }
                        tbody.innerHTML = html;
                    }
                } catch (e) {
                    console.error("Status fetch error", e);
                }
            }

            async function sendSimulated(appName, title) {
                try {
                    const res = await fetch('/webhook/phone-event?format=json', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            event: 'simulated_trigger',
                            app_name: appName,
                            content_title: title
                        })
                    });
                    const data = await res.json();
                    showToast(data.speak);
                    fetchStatus();
                } catch (e) {
                    showToast("Failed to simulate event");
                }
            }

            function showToast(text) {
                const toast = document.getElementById('toast');
                toast.innerText = '🗣️ ' + text;
                toast.style.display = 'flex';
                setTimeout(() => { toast.style.display = 'none'; }, 4500);
            }

            fetchStatus();
            setInterval(fetchStatus, 3000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    print("🚀 Starting Smart Overseer Bridge on port 5678...")
    uvicorn.run(app, host="0.0.0.0", port=5678)

