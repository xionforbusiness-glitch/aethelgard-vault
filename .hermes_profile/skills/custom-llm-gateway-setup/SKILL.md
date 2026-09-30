---
name: custom-llm-gateway-setup
description: "Use when configuring custom LLM gateways."
---

# Custom LLM Gateway Setup

Standard procedure for configuring Hermes to use a custom LLM provider (e.g., OmniRoute, self-hosted proxies).

## Procedure

1. **Set API Key**: Append the key to `~/.hermes/.env` (use `$HERMES_HOME/.env` if `HERMES_HOME` is set).
   ```bash
   echo "PROVIDER_API_KEY=your_key_here" >> "$HERMES_HOME/.env"
   ```
2. **Configure Hermes**: Use `hermes config` for setting properties.
   ```bash
   hermes config set model.provider custom
   hermes config set model.base_url "<your-base-url>"
   hermes config set model.default "<model-id>"
   hermes config set model.api_key "${PROVIDER_API_KEY}"
   ```
3. **Clear Cache**: If switching providers or base URLs, clear the model provider cache to force a re-fetch.
   ```bash
   rm -f "$HERMES_HOME/provider_models_cache.json"
   ```
4. **Validate**: 
   ```bash
   hermes config show
   hermes chat -q "Hi"
   ```

## Diagnosing a broken profile

When one profile works (e.g. `resercher`) but others fail, run these in order — each step isolates a different failure mode:

1. **Inventory**: `hermes profile list` shows every profile's model/provider/gateway at a glance.
2. **Read each profile's config**: its own `config.yaml` under `~/.hermes/profiles/<name>/` — the `model:` block (default, provider, base_url, api_mode, api_key vs key_env) and its `providers:` block.
3. **Read each profile's `.env`** (same directory): compare which keys are present across profiles — a profile missing the key its config references fails auth.
4. **Probe every endpoint with curl**: `GET <base_url>/models` plus a one-shot `/chat/completions` against each base_url the profiles use (local router, remote API host, upstream provider). The HTTP status + JSON error body separates "endpoint dead" (000/connection refused) from "model dead" (410/404) from "credential broken" (401) from "upstream overloaded" (504) in one step.
5. **Grep the logs instead of guessing**: `~/.hermes/logs/errors.log` and `agent.log` record `provider=`, `base_url=`, and `model=` on every failed call, so a given error maps straight back to the profile that produced it.
6. **Check the router's own state** (OmniRoute): the `omniroute` CLI and its credential store — see references/omniroute.md.

Typical failure modes and what they mean:

- **HTTP 410** — the model hit end-of-life; re-check the provider's live `/models` list before re-picking a default.
- **HTTP 504** — upstream proxy overloaded (even "live" heavy models time out); prefer a lighter model or re-route.
- **HTTP 404 "no longer available, use <new model>"** — providers rename models without warning; the model id in config is stale.
- **HTTP 401** — credential failure. With a routing gateway, this is usually the ROUTER lacking upstream credentials, not the Hermes `.env`.
- **`api_key: OMNIROUTE_API_KEY=sk-...` (a `NAME=value` blob)** — malformed: Hermes sends the whole string as the bearer token. Use the bare key value or a `key_env` reference.
- **connection refused (curl 000)** — the base_url host is down; test the local router (`localhost:PORT`) separately from any remote host (`api.omniroute.com`) the config may be drifting to.

## Pitfalls

* **`hermes config set` edits the ACTIVE profile only.** The target comes from `$HERMES_HOME` (the profile the process was launched under), NOT the current working directory — running it with `cwd` inside another profile's folder still rewrites the active profile's config. To edit profile X, prefix with `HERMES_HOME=".../profiles/X"` and verify afterwards with `hermes config show` + a diff of the file.
* **A routing gateway keeps its OWN credential store.** Putting a provider key in Hermes `.env` does nothing for a router that authenticates upstream providers itself (OmniRoute stores credentials in `~/.omniroute`). A profile routed through the gateway fails with 401 "No active credentials for provider: X" until the provider is added on the router side (`omniroute providers add X --credential ...` — see references/omniroute.md), regardless of what Hermes `.env` holds.
* **Cache Persistence**: The CLI and gateway cache provider data. If settings change and the agent seems to use old provider metadata or invalid model names, clear `provider_models_cache.json`.
* **Endpoint URL**: The `base_url` must be the *full* path to the completion endpoint (often ending in `/v1` or `/v1/chat/completions` depending on the provider). Check the provider's API docs.
* **Placeholder Keys**: Editing `.env` with `***` placeholders will not work. You must paste the actual credential into the file. Likewise, a profile whose `model.api_key` literally contains `OMNIROUTE_API_KEY=sk-...` sends that whole name=value string as the bearer token — use the bare key value or a `key_env` reference.
* **Models get retired and renamed.** A default model can return HTTP 410 (end of life) while the rest of the endpoint works; `GET /models` on the provider reveals the live set. Big providers also rename without warning (e.g. gemini-2.5-flash → gemini-3.6-flash → 404 "no longer available"). Re-pick defaults against the CURRENT `/models` output, never against what an old config file claims.
* **Ambiguous model names on multi-provider routers**: when a model id exists in several providers, the router rejects it with "Ambiguous model ... Use provider/model prefix" — send `provider/model` (e.g. `gemini/gemini-2.0-flash`).
* **`/models` lists catalog entries, not live availability**: A custom provider endpoint or router catalog often includes models that are deprecated (HTTP 410 EOL), heavily throttled (HTTP 429), or timing out (HTTP 504). Always verify candidate models with a minimal one-token `/chat/completions` probe rather than trusting the `/models` list alone.
* **Gateway failover strategies**: Multi-model gateways (e.g. OmniRoute) support `priority` combo strategies with automatic retry and fallback on transient errors (HTTP 503/429/504) — see references/omniroute.md for configuration workflows.
* **Connectivity**: If `APIConnectionError` persists, ensure the gateway/proxy server is actively running and reachable at the configured `base_url`. Use `curl` or a browser to verify the endpoint is listening.
