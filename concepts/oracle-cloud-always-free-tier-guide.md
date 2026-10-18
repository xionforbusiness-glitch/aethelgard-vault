---
title: "Oracle Cloud Infrastructure (OCI) Always Free Tier Architecture Guide"
created: 2026-10-18
updated: 2026-10-18
type: concept
tags: [cloud, infrastructure, oci, oracle, free-tier, devops, hosting, vps, llm-hosting]
sources: [Hyperautomation Labs (Facebook Reel 1905455427101888), Oracle Cloud Always Free Documentation]
confidence: high
contested: false
contradictions: []
---

# ☁️ Oracle Cloud Always Free Tier Architecture Guide

> **"Oracle gives you 3 to 4 servers, 2 autonomous databases, and 10 TB of egress traffic free forever."**  
> Operational breakdown of Oracle Cloud Infrastructure (OCI) Always Free resources and how to architect self-hosted bots, personal APIs, and small LLM inference nodes.

---

## 🎁 What You Actually Get (Always Free Specs)

Oracle Cloud's Always Free tier is widely considered the most generous free compute offering among major cloud hyperscalers (surpassing AWS Free Tier and Google Cloud e2-micro):

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ORACLE CLOUD ALWAYS FREE COMPUTE POOL                │
├─────────────────────┬──────────────────────────────────────────────────┤
│ 1. Ampere ARM Pool  │ Up to 4 OCPUs (cores) & 24 GB RAM (Total)        │
│                     │ Can be split into 1–4 instances (e.g. 1x 24GB or │
│                     │ 2x 12GB or 4x 6GB).                              │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 2. AMD Micro VMs    │ 2x x86_64 Instances (VM.Standard.E2.1.Micro)    │
│                     │ 1 OCPU & 1 GB RAM each. Ideal for low-load bots. │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 3. Storage          │ 200 GB Total Block Volume (shared across VMs)    │
│                     │ 10 GB Object Storage + 10 GB Archive Storage     │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 4. Autonomous DBs   │ 2x Oracle Autonomous Databases (20 GB each)      │
├─────────────────────┼──────────────────────────────────────────────────┤
│ 5. Network Egress   │ 10 TB outbound bandwidth per month               │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

## 🏗️ Optimal Multi-Server Deployment Blueprint

For a personal tech stack (like hosting Telegram bots, web scrapers, and local LLMs):

```
┌────────────────────────────────────────────────────────────────────────┐
│                    PROPOSED 3-INSTANCE ARCHITECTURE                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│  SERVER 1    │             │  SERVER 2    │             │  SERVER 3    │
│ (Ampere ARM) │             │ (AMD Micro)  │             │ (AMD Micro)  │
├──────────────┤             ├──────────────┤             ├──────────────┤
│ • 4 OCPUs    │             │ • 1 OCPU     │             │ • 1 OCPU     │
│ • 24 GB RAM  │             │ • 1 GB RAM   │             │ • 1 GB RAM   │
│ • 100 GB SSD │             │ • 50 GB SSD  │             │ • 50 GB SSD  │
├──────────────┤             ├──────────────┤             ├──────────────┤
│ Role:        │             │ Role:        │             │ Role:        │
│ Ollama LLMs, │             │ Telegram Bot │             │ Uptime Kuma, │
│ Hermes Agent,│             │ (Aethelgard) │             │ WireGuard,   │
│ Heavy Python │             │ & Redis Hub  │             │ Vault Backup │
└──────────────┘             └──────────────┘             └──────────────┘
```

* **Server 1 (The Powerhouse - Ampere ARM A1):** With **24 GB of RAM**, this instance can comfortably run quantized open-source LLMs via Ollama/llama.cpp (e.g., Llama 3 8B Q4, Mistral 7B, or Gemma 2 9B), heavy vector embeddings, and web agents.
* **Server 2 & 3 (The AMD Micros):** Perfect for persistent lightweight background daemons (Telegram webhook receivers, reverse proxies, and cron scripts) that run 24/7 without consuming significant resources.

---

## ⚠️ The Fine Print & Potential Pitfalls

1. **Credit Card Verification:**
   * Requires a valid credit/debit card during registration to verify identity.
   * Oracle places a temporary ~$1 USD authorization hold, which is immediately reversed. You are **not** billed unless you manually click "Upgrade to Paid Account".
2. **ARM Capacity Out-of-Stock ("Out of host capacity"):**
   * Ampere A1 ARM compute is extremely popular. Certain OCI regions (e.g., Frankfurt, Ashburn) frequently run out of free ARM capacity.
   * *Pro-tip:* Select regions with lower contention, or automate a script to periodically poll the OCI API until an instance successfully launches.
3. **Idle Instance Reclamation (Oracle Inactivity Rule):**
   * Oracle monitors free instances for idle metrics. If CPU utilization is under 20% and memory usage is low for 7 consecutive days, Oracle may mark the instance idle and reclaim it.
   * *Mitigation:* Keep regular cron jobs or container workloads active so the instance maintains genuine baseline telemetry.

---

## 🔗 Related Notes & Vault Assets

* [[concepts/kaggle-hybrid-cloud-runner|Kaggle Hybrid Cloud Runner]]
* [[01 Technical Skills|Technical Skills Knowledge Base]]
* [[log|Operational Log]]
