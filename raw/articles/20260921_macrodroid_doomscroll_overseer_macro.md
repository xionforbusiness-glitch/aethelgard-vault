---
source_url: null
ingested: 2026-09-21
image_file: raw/assets/20260921_macrodroid_doomscroll_macro_config.jpg
type: raw
tags: [macrodroid, automation, android, doomscroll, overseer]
---

# MacroDroid "App Usage / Doomscroll" Macro — Raw Screenshot Transcription

## Source
- **Origin:** Screenshot sent by Omar via Telegram (2026-09-21)
- **App:** MacroDroid (Android automation)
- **Image:** `raw/assets/20260921_macrodroid_doomscroll_macro_config.jpg`

## Full Transcription

### Macro Title
**App Usage / Doomscroll**

### Triggers (3 configured)

1. **Application Launched** — [YouTube, Facebook]
   - Fires when either YouTube or Facebook is opened/launched.

2. **Media Track Changed**
   - Fires on any media track change (e.g. new video starts playing).

3. **Notification Received** — Any Content [Telegram, Facebook, YouTube, WhatsApp]
   - Fires when a notification with any content is received from Telegram, Facebook, YouTube, or WhatsApp.

### Actions (partially visible behind dialog)

- **Click (Current focus)**
  - A UI Interaction action that clicks the currently focused element.
  - Dialog box: **"Click Result"**
    - **Block until result available** — selected (radio button)
    - **Save to variable:** `video_title`
  - This extracts the title of the currently viewed video/content into a variable.

### Constraints (1 configured)

- **Macro(s) Not Invoked [This Macro]:** Not Invoked For 15s
  - 15-second cooldown/debounce to prevent rapid re-triggering.

### Local Variables
- `video_title` — stores the extracted content/video title from the focused UI element.

### Status Bar Context
- Battery: 20% (red)
- Network: 4.5G
- Time: 4:50
- Active notifications: Messenger, chat apps
