---
title: "MacroDroid Doomscroll Overseer Macro"
created: 2026-09-21
updated: 2026-09-21
type: concept
tags: [automation, android, tool, hermes-agent, telegram-bot]
sources: [raw/articles/20260921_macrodroid_doomscroll_overseer_macro.md]
confidence: high
contested: false
contradictions: []
---

# MacroDroid Doomscroll Overseer Macro

Omar's **"App Usage / Doomscroll"** macro in [[MacroDroid]] is the Android-side automation that powers the `overseer` pipeline logged in [[log]]. It detects social media usage, extracts app context, and relays telemetry to the [[hermes-agent]] webhook endpoint (`http://10.117.196.61:5678/webhook/phone-event`) for classification and AI text-to-speech feedback.

![[20260921_macrodroid_doomscroll_macro_config.jpg]]

## Architecture

```
┌────────────────────────────────────────┐
│         MacroDroid (Android)           │
│ ┌────────────────────────────────────┐ │
│ │ Triggers:                          │ │
│ │  • App Launch (YT, FB, TG, WA)     │ │
│ │  • Media Track Changed             │ │
│ │  • Notification Rx                 │ │       ┌────────────────────────┐
│ └──────────┬─────────────────────────┘ │       │  Hermes Agent / n8n    │
│            ▼                           │       │  (Webhook: 5678)       │
│ ┌────────────────────────────────────┐ │       │                        │
│ │ Actions:                           │ │──────▶│  overseer pipeline     │
│ │  1. Wait 2s                        │ │ HTTP  │  • classify app usage  │
│ │  2. Set app_name = [App Name]      │ │ POST  │  • generate ai_response│
│ │  3. UI Interaction (Copy)          │ │       └────────────────────────┘
│ │  4. Set video_title = [clipboard]  │ │                   │
│ │  5. HTTP Request (POST webhook)    │ │                   ▼
│ │  6. Speak Text ({lv=ai_response})  │ │       ┌────────────────────────┐
│ └──────────┬─────────────────────────┘ │       │  Audio Feedback        │
│            ▼                           │       │  (Text-to-Speech)      │
│ ┌────────────────────────────────────┐ │       └────────────────────────┘
│ │ Constraint: 15s cooldown           │ │
│ └────────────────────────────────────┘ │
└────────────────────────────────────────┘
```

## Triggers & Constraints

| Type | Name | Scope | Purpose |
|------|------|-------|---------|
| **Trigger** | Application Launched | YouTube, Facebook, Telegram, WhatsApp | Detects app entry |
| **Trigger** | Media Track Changed | Any media | Catches playback changes |
| **Trigger** | Notification Received | Telegram, Facebook, YouTube, WhatsApp | Detects push alerts |
| **Constraint** | Macro Not Invoked | `[This Macro]: Not Invoked For 15s` | Debounce cooldown preventing spam |

## Action Sequence

1. **Wait 2 seconds** — Buffer time for app rendering and focus.
2. **Set Variable (`app_name`)** — Captured via trigger-specific `[App Name]` to avoid foreground launcher lag.
3. **UI Interaction (Copy)** — Copies active screen text/title to system clipboard.
4. **Set Variable (`video_title`)** — Captures clipboard content via `[clipboard]`.
5. **HTTP Request (POST)** — Sends JSON payload to `http://10.117.196.61:5678/webhook/phone-event`:
   ```json
   {
     "event": "app_launched",
     "app_name": "{lv=app_name}",
     "content_title": "{lv=video_title}",
     "extra": ""
   }
   ```
6. **Speak Text** — Reads aloud `{lv=ai_response}` returned by the webhook server.

## See Also

- [[linux_cli_bash_automation_reference]] — CLI automation patterns
- [[gear_hobbies_lifestyle]] — Omar's device and tool ecosystem
- [[04 Interests & Gear]] — Broader hobbies and tools overview
