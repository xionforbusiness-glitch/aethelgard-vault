# OmniRoute diagnostics

OmniRoute is the local AI router (`localhost:20128`) that backs the user's Hermes profiles. It keeps its own state, separate from Hermes.

## Where state lives

- Data dir: `~/.omniroute/` — `storage.sqlite` (+ -wal/-shm), `call_logs/`, `logs/`, `.env` (holds `STORAGE_ENCRYPTION_KEY`).
- The `omniroute` CLI loads env from, in order: `~/.omniroute/.env`, the active Hermes profile `.env`, then the npm module `.env`; earlier sources win and later ones print "ignored, the environment set it first".
- Server binary: `C:\Users\<user>\AppData\Roaming\npm\omniroute(.cmd)`.
- Web Dashboard: `http://localhost:20128/dashboard` (or `omniroute dashboard` / `omniroute open`).

## Useful commands

Prefix with the router key: `omniroute --api-key "$(grep -oP '(?<=^OMNIROUTE_API_KEY=).*' ~/.omniroute/.env | head -1)" ...` (the CLI also picks it up from env).

| Command | Purpose |
|---|---|
| `status` | Health, data dir, installed CLI tools |
| `dashboard` / `open` | Launch or print the local OmniRoute Web UI |
| `providers list` | Active provider connections (id, provider, name, active status) |
| `providers available` | Catalog with auth type per provider (api-key / oauth / web-cookie / cloud-agent) |
| `providers add <p> --credential <key> [--default-model <id>] [--yes]` | Add an API-key provider connection |
| `providers auth <p> [--no-browser]` | Start/print an OAuth flow for a provider |
| `providers test <idOrName>` / `test-all` | Verify a connection upstream |
| `oauth status` | OAuth connections per provider |
| `combo list` / `combo switch <name>` | List or switch active routing combo |
| `combo create <name> --strategy <spath> --models "..."` | Create a combo with specific routing strategy and model list |
| `models` | Model catalog by provider — the authoritative list of LIVE model ids/names |
| `resilience status` / `breakers` / `reset` | Inspect circuit breakers, cooldowns, and resilience mechanisms |
| `logs` | Stream request logs (past failures show the 401/404/504 bodies with provider prefix) |

## Routing Combos & Automatic Fallback

Combos determine how OmniRoute distributes requests and fails over when errors occur (HTTP 503 Overloaded, HTTP 429 Rate Limit, HTTP 504 Timeout):

- **Strategies**:
  - `priority` (Recommended for fallback): Attempts the 1st model first; on failure, automatically fails over to model #2, #3, etc.
  - `round-robin`: Distributes calls evenly across models in the combo without strict fallback ordering.
  - `fill-first`, `weighted`, `auto`, `p2c`, `cost-optimized`.
- **Configuring Fallback via CLI**:
  ```bash
  omniroute combo create <combo-name> --strategy priority --models "provider/primary-model,provider/fallback-model"
  omniroute combo switch <combo-name>
  ```
- **Configuring Fallback via Dashboard**:
  In `http://localhost:20128/dashboard` → **Combos** → select combo → set Strategy to `priority`, sort models by desired fallback order, and ensure `maxRetries >= 1`.
- **Resilience Circuits**:
  When an upstream returns 503 or 429, OmniRoute initiates a temporary provider cooldown and uses the combo's retry configuration to seamlessly query the next candidate model before throwing an error to Hermes.

## Pitfalls

- The router's OpenAI-compatible endpoint (`/v1/...`) accepts any or no bearer token for listing and often for completion too — a 401 from IT means "no active upstream credentials for that provider", not a bad router key.
- Model names must match the router's live catalog (`omniroute models`); a name that worked in Hermes config before may have been renamed or EOL'd upstream.
- Adding a provider via `providers add --credential` stores the key in the router's own encrypted store — it neither needs nor reads Hermes `.env`.
- A model id present in several providers must be prefixed `provider/model` or the router answers "Ambiguous model".
- Transient HTTP 503 errors (`overloaded`, `Chat admission capacity is temporarily unavailable`) indicate temporary upstream saturation. Use `priority` combo strategy with `maxRetries >= 1` to fail over automatically instead of breaking client requests.

## Google (AI Studio / Gemini) direct probe

When the router's gemini provider is missing or the key is suspect, probe Google's own OpenAI-compatible endpoint first — it isolates Google-side auth from router-side config:

- OpenAI-compatible chat: `POST https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` with `Authorization: Bearer $GOOGLE_API_KEY`.
- `GET /v1beta/models` (plain REST, not /openai) echoes a 401 `API_KEY_SERVICE_BLOCKED` reason when the key is not authorized for the generativelanguage service — that's a key-permission problem, not a model problem.
- Distinguish the bodies: `404 "no longer available / use models/gemini-3.x-flash"` = stale model name; `503 high demand` = transient upstream, retry; `401` = key invalid/not enabled.
- Model names rotate fast (2.5 → 3.6/3.1-flash-lite within a year). Never hard-code a gemini model id from memory; check `omniroute models` or `GET /v1beta/models` for the current live id.

## Known-good baseline (this machine)

- Router: `http://localhost:20128/v1`, combo `FIRST-TIME` (round-robin) exposing `auto/*` and `kr/`, `kiro/`, `oc/`, `antigravity/`, `dva/` prefixed models.
- Working profile `resercher`: provider `first-time`, model `auto/best-coding`, `key_env: HERMES_CUSTOM_FIRST_TIME_API_KEY`, `base_url: http://localhost:20128/v1`, `api_mode: chat_completions`.
- Connected providers seen on this machine: kiro, antigravity (x2), opencode, openrouter, gemini, g4f-gemini (catalog).
