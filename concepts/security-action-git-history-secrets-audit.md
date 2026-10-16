---
title: "Security Action Item: Git History Secret Scrubbing & Token Rotation Protocol"
created: 2026-10-16
updated: 2026-10-16
type: security-advisory
tags: [security, audit, git, tokens, secrets-management, github, devops, pending-action]
confidence: high
contested: false
contradictions: []
---

# 🚨 Security Advisory: Secrets in Public Git History & Remediation Runbook

> **Status:** ⚠️ **PENDING OMAR'S MANUAL EXECUTION**  
> **Origin:** Audit triggered by Deploy Skool security reel on Git history commit persistence.  
> **Risk Level:** **HIGH** (Repository is currently Public on GitHub; tokens exist in both active files and past Git commit trees).

---

## 🔍 Vulnerability Summary

During the October 16, 2026 audit, the following secrets were discovered exposed in both working tree files and historical Git commit snapshots in `xionforbusiness-glitch/aethelgard-vault`:

1. **GitHub Personal Access Token (PAT):**
   * Pattern: `ghp_gY...`
   * Files containing key:
     * `run_kaggle.py`
     * `run_kaggle_local.py`
     * `scripts/kaggle_on_demand_cloud_runner.py`
     * `kaggle_hybrid_cloud_runner.md`
2. **Telegram Bot Token:**
   * Pattern: `8992784967:AAH2bK...`
   * Files containing token:
     * `run_kaggle.py`
     * `scripts/kaggle_on_demand_cloud_runner.py`
     * `kaggle_hybrid_cloud_runner.md`
3. **Repository Visibility:** Currently configured as **PUBLIC** on GitHub (`https://github.com/xionforbusiness-glitch/aethelgard-vault`).

---

## 📋 Step-by-Step Remediation Runbook (When Ready to Execute)

To avoid breaking the live GCP VM or interrupting the active Telegram bot connection, execute these steps in order when scheduled:

### Step 1: Make Repository Private (Zero Risk to VM)
* Go to GitHub: `https://github.com/xionforbusiness-glitch/aethelgard-vault/settings`
* Scroll to the **Danger Zone** at the bottom.
* Click **Change visibility** ➔ Select **Make Private**.
* *Impact:* Instant protection against external crawlers/bots without breaking local git pushes (the local token already has write permissions).

---

### Step 2: Environment Variable Refactor (Code Cleanup)
* Replace hardcoded strings in Python files with environment lookups:
  ```python
  import os
  GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
  TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
  ```
* Store actual secrets securely in `~/.bashrc` or an untracked `.env` file added to `.gitignore`.

---

### Step 3: Git History Purge (Removing Historical Snapshots)
* Use `git-filter-repo` on the local repository to purge historical references without resetting branch tracking:
  ```bash
  # Install tool if missing
  pip install git-filter-repo
  
  # Purge sensitive files or patterns across all commits
  git filter-repo --replace-text <(echo "OLD_EXPOSED_GITHUB_TOKEN==>REDACTED_GH_TOKEN")
  ```
* Force push sanitized branch to GitHub:
  ```bash
  git push origin --force --all
  ```

---

### Step 4: Token Rotation (Final Invalidation)
Once the repo is private and code is refactored:
1. **GitHub PAT:** GitHub Settings ➔ Developer Settings ➔ Personal Access Tokens ➔ Generate new token with `repo` scope ➔ Update remote URL in VM (`git remote set-url origin ...`) ➔ Revoke old token.
2. **Telegram Bot Token:** Message `@BotFather` ➔ `/revoke` ➔ Select `@aethelgard_local_bot` ➔ Paste new token into VM environment.

---

## 🔗 Related Notes
* [[concepts/vibe-coder-security-fix-kit|The Vibe Coder's Security Fix Kit]]
* [[concepts/ai-red-teaming-and-llm-hacking-playbook|AI Red Teaming Playbook]]
* [[log|Operational Log]]
