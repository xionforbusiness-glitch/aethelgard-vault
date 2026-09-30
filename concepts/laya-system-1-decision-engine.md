---
title: Laya — Open-Source System 1 Decision Engine
created: 2026-09-21
updated: 2026-09-21
type: concept
tags: [ai, ml, llm, open-source, python]
sources: [raw/articles/2026-09-21-laya-system1-decision-model-open-source.md]
confidence: high
contested: false
contradictions: []
---

# Laya: Open-Source System 1 Decision Engine

## 1. Overview
**Laya** is an open-source, non-autoregressive decision model family created by **Nandakishor Mukkunnoth** (Founder & CEO of ConvAI Innovations) and released under the **Apache 2.0 License** in September 2026. 

Laya is built specifically for **System 1 tasks**—instantaneous, reflex-level decisions that do not require multi-token natural language generation. Instead of generating text token by token like standard autoregressive LLMs (GPT-4, Claude, LLaMA), Laya evaluates structured or unstructured state against predefined typed schemas in a **single forward pass**, returning typed answers with calibrated probability distributions.

---

## 2. Core Architecture & Mechanisms

### 2.1 Bidirectional Encoder Backbone
Traditional generative LLMs use causal (decoder-only) attention, processing tokens sequentially from left to right. Laya instead uses **bidirectional encoder backbones**, allowing every token to attend to full context simultaneously:
- **English Base (`convaiinnovations/laya`):** Built on **ModernBERT-large** (421M parameters, 512 context length).
- **Multilingual Variant (`convaiinnovations/laya-multilingual`):** Built on **mmBERT-base** (322M parameters, 1024 context expandable up to 8K, covering 100+ languages).
- **Specialized Variant (`convaiinnovations/laya-typed-decisions`):** Fine-tuned ModernBERT-large (421M parameters) optimized for structured workflow benchmarks.

### 2.2 Non-Autoregressive Decision Heads
Laya attaches parallel classification and scoring heads directly onto pooled sequence representations:
- **Categorical Choices (`choice`):** Multi-class probability distribution over candidate categories.
- **Ordinal Scoring (`score`):** Continuous expectation value along an ordered rubric scale.
- **Binary/Boolean Decisions (`noul`):** Calibrated Bernoulli probability $P(\text{true}) \in [0.0, 1.0]$.

### 2.3 RLCD (Reinforcement Learning for Calibrated Decisions)
Trained against strictly proper scoring rules (Brier score and log-likelihood penalties). The model's loss landscape guarantees that the mathematically optimal strategy for the agent is to report its true epistemic uncertainty rather than overconfident guesses.

---

## 3. Performance & Benchmark Scorecard

| Metric / Dimension | Laya (Multilingual) | Laya (English) | TypeSafe Jev (1.13.0) | Standard Generative LLM |
| :--- | :--- | :--- | :--- | :--- |
| **Model Size** | 322M | 421M | Proprietary (~300M–1B est.) | 8B – 70B+ |
| **Inference Mode** | Non-autoregressive | Non-autoregressive | Non-autoregressive | Autoregressive (Token by Token) |
| **Single-GPU Latency (T4)** | **32.8 ms** | **39.5 ms** | 236 – 276 ms (API) | 500 – 2500 ms |
| **Batched Latency (10 Qs)** | **7.2 ms / Q** (72.3 ms) | 15.8 ms / Q (158.6 ms) | ~200+ ms | Multi-second queue |
| **Multilingual Reach** | 100+ languages (45/51) | Latin scripts (23/51) | English primary | Broad multilingual |
| **Typed-Decisions Benchmark** | 0.352 (zero-shot) / 0.766 (fine-tuned) | 0.362 (zero-shot) / 0.766 (fine-tuned) | 0.727 (API) | 0.678 – 0.741 |
| **Licensing** | **Apache 2.0 (Open Weights)** | **Apache 2.0 (Open Weights)** | Closed API | Commercial / Open Weights |
| **Inference Cost** | **$0 (Local Compute)** | **$0 (Local Compute)** | $0.042 / 1M Tokens | $0.20 – $15.00 / 1M Tokens |

---

## 4. Benchmark Nuances & Production Realities

1. **Zero-Shot vs. Fine-Tuned:**
   On cold zero-shot evaluation without prior training on the target schema, Laya's accuracy is ~0.35–0.36 (near baseline). The headline accuracy of **0.766** requires fine-tuning on domain data.
2. **Calibration Repair:**
   Out of the box, expected calibration error (ECE) can be ~0.466. Applying simple temperature scaling ($T$-scaling per head) drops ECE to **0.081**, making the probability numbers reliable.
3. **Primary Use Cases:**
   - LLM Guardrails & Injection Detection
   - High-throughput Ticket & Email Triage
   - Agent Routing (deciding which subagent or model to call next)
   - Real-time Moderation & SLA Priority Scoring

---

## 5. Ecosystem & SDK Availability

- **Python SDK:** `pip install laya>=0.3.3` (Hugging Face Hub integration, PyTorch, ONNX backend).
- **Node.js / TypeScript:** `npm install @receptron/laya` (via `onnxruntime-node`).
- **Hugging Face Repos:** `convaiinnovations/laya`, `convaiinnovations/laya-multilingual`, `convaiinnovations/laya-typed-decisions`.

---

## 6. Cross-References
- [[typesafe-ai-jev]] — The proprietary model that triggered the open-source release.
- [[laya-vs-typesafe-jev]] — Detailed comparative analysis between Jev and Laya.
- [[laya-system-1-installation-deployment-plan]] — Step-by-step engineering plan to install, test, and integrate Laya locally.
- [[01 Technical Skills]] — Omar's machine learning, Python, and systems engineering toolkit.
- [[ai_evaluation_annotation_handbook]] — Calibration, annotation schemas, and LLM evaluation benchmarks.
