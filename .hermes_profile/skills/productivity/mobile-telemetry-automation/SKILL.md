---
name: mobile-telemetry-automation
description: "Use when building mobile telemetry triggers and webhooks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mobile, android, macrodroid, tasker, webhook, telemetry, proactive-agent, tts]
    category: productivity
    related_skills: [hermes-agent, n8n-workflow-automation]
---

# Mobile Telemetry & Webhook Automation

Connect mobile device event streams (Android MacroDroid/Tasker) to local AI agents and webhook bridges for real-time activity tracking, doomscroll filtration, proactive spoken interventions, and welfare checks.

## Architecture

```
Android Device (MacroDroid/Tasker)
  │ (HTTP POST JSON payload with app_name, content_title, url, extra)
  ▼
Local Webhook Bridge (FastAPI on port 5678)
  │ 🧠 Smart Content Evaluator (Domain Taxonomy + Brainrot Weights + Streak Escalation)
  ├─► Appends structured telemetry to Obsidian Vault Log (log.md)
  ├─► Maintains daily focus score in ~/.hermes/overseer_state.json
  ├─► Serves real-time HTML telemetry dashboard (/dashboard)
  └─► Returns Clean Plain Text response body
        │
        ▼
Android Device Action (Speak Text via Phone Speaker)
```

## Smart AI Content Evaluation (Beyond App Names)

Relying solely on app names causes false positives (e.g. YouTube could be a 3-hour computer vision lecture or a brainrot shorts compilation; Facebook could be an AI research post or doomscrolling).

### Semantic Evaluator Rules:
1. **Weighted Domain Taxonomy:** Assign high positive weights (+1.1 to +1.3) to Omar's engineering pillars: AI/LLMs (`ModernBERT`, `Laya`, `YOLO`, `OpenCV`), embedded systems (`Arduino`, `SG90`, `SPIKE`), dev tools (`Linux`, `FastAPI`, `Git`), academics (`UoPeople`, `SVU`), and crafts (`CFOP`, `DCS`).
2. **Brainrot & Algorithmic Penalties:** Heavy negative penalties (-2.0 to -4.0) for shorts indicators (`#shorts`, `reels`, `/reel/`), clickbait keywords (`prank`, `drama`, `skibidi`, `challenge 24h`).
3. **Educational Social Exceptions:** If a high-risk social app (Facebook, Twitter, Reddit) contains strong technical keywords and no brainrot markers, classify it as productive study rather than penalizing it.
4. **Escalating Coaching Interventions:**
   - **Productive Streaks:** Encouraging, brief validation (`"Study topic recognized: {topic}. High value focus."`).
   - **Distraction Streak 1:** Gentle awareness check (`"Notice: you just opened {topic}. Keep your daily goals in mind."`).
   - **Distraction Streak 2:** Direct warning (`"Second distraction detected. Step away from {app}."`).
   - **Distraction Streak 3+:** Urgent intervention (`"Distraction streak is at {N}. You have active builds in the vault. Let's return to code."`).

## Step-by-Step Implementation

### 1. Webhook Bridge Server (FastAPI)
Run a lightweight FastAPI bridge rather than heavy orchestration engines when disk space or RAM is constrained:

```python
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn, datetime

app = FastAPI(title="Overseer Bridge")

@app.post("/webhook/phone-event")
async def phone_event(request: Request):
    data = await request.json()
    app_name = data.get("app_name", "Unknown")
    
    # Classification logic
    brainrot = ["Instagram", "TikTok", "Facebook", "Snapchat"]
    if any(b.lower() in app_name.lower() for b in brainrot):
        msg = f"Opened {app_name}. Let's stay proactive and return to your builds."
    else:
        msg = f"Active on {app_name}. Keep learning."
        
    return PlainTextResponse(content=msg)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5678)
```

### 2. MacroDroid Configuration Rules

#### Trigger Setup (Red Box)
- **Correct Trigger:** `Applications` → `Application Launched/Closed` → `Application Launched` → Select target apps.
- ❌ **Pitfall:** Do not select `App Activity Launched/Closed` (prompts for internal class names) or `Application Installed` (only triggers on APK download from Play Store).

#### HTTP Request Action (Blue Box - Action 1)
- **Method:** `POST`
- **URL:** `http://<HOST_LOCAL_IP>:5678/webhook/phone-event`
- **Content Type:** `application/json`
- **Request Body (Text):**
  ```json
  {"event": "app_launched", "app_name": "[app_name]", "content_title": "[video_title]", "extra": "[not_text]"}
  ```
- **Response Options:**
  - Check **Block next actions until complete**
  - Check **Save HTTP response in string variable** → name it `ai_response` (Local scope).
- ❌ **Pitfall:** Ensure variables match their trigger contexts. Using `[media_track]` during app launch or notification events will leave titles empty if media is not playing; use UI Interaction click results stored in `[video_title]` for screen content, and `[notification_app_name]` for notification sources rather than generic `[app_name]` which defaults to `Unknown` on background alerts.

#### Speak Text Action (Blue Box - Action 2)
- **Action:** `Device Actions` → `Speak Text`
- **Text to speak:** `[lv=ai_response]` (or `{lv=ai_response}`) — **never wrap in quotes** (`'[lv=ai_response]'`). MacroDroid treats literal quotes as text to vocalize, making TTS say "single quote".
- **Audio Stream:** `Media` (or Notification)

#### Constraints Setup (Green Box - Optional Rate-Limiting)
- **Cooldown Constraint:** `MacroDroid Specific` → `Macro(s) Invoked/Not Invoked Recently` → `This Macro` → `Not invoked in last...` (set 15–30 seconds) to prevent chatter loops during rapid group notifications or video scrolling.
- ❌ **Pitfall:** Do not select `Macro Invocation Method` (which only checks how the macro was launched, e.g. shortcut vs drawer) when attempting to set a cooldown timer.

## Pitfalls & Best Practices

- **Never Quote Speak Text Variables:** Use `[lv=ai_response]`. Surrounding single or double quotes are spoken literally by the Android TTS engine.
- **Sanitize Unresolved MacroDroid Tokens on Server:** When a payload combines multi-trigger variables (e.g. `[not_title]` in an `app_launched` trigger), MacroDroid outputs the literal placeholder string `"[not_title]"`. Clean tokens matching `r"^\[.*?\]$"` to empty strings before running evaluation logic.
- **Magic Text Casing:** Use `[app_name]` (all lowercase). Capitalized variants like `[_AppName]` do not expand dynamically.
- **Plain Text for Speech:** Return `PlainTextResponse` from FastAPI instead of JSON dictionaries (`{"speak": "..."}`) so the mobile TTS engine does not speak out curly braces or quotation marks.
- **Local Network Binding:** Bind the server to `0.0.0.0:5678` and verify phone Wi-Fi reaches the PC's Wi-Fi IPv4 address (test via `http://<IP>:5678/status` in the mobile browser first).
- **Cozy Telemetry Dashboard Design:** Telemetry dashboards monitored during deep work should use soft, low-contrast dark themes (warm obsidian/slate `#12131c`, soft pastel badges `#34d399`, `#38bdf8`, `#c084fc`, `#fb7185`, rounded cards) and lightweight polling (`setInterval(fetchStatus, 3000)`) to remain relaxing to the eyes.
