---
title: TypeSafe AI & Jev (System 1 Decision Model)
created: 2026-09-21
updated: 2026-09-21
type: entity
tags: [ai, ml, llm]
sources: [raw/articles/2026-09-21-laya-system1-decision-model-open-source.md]
confidence: high
contested: true
contradictions: [laya-system-1-decision-engine]
---

# TypeSafe AI & Jev

## 1. Overview
**TypeSafe AI** is an AI startup founded by **Diogo Almeida** (a former OpenAI researcher involved in RLHF and ChatGPT). In mid-September 2026, TypeSafe emerged from stealth by launching **Jev**, marketed as a proprietary "System 1 Foundation Model."

Unlike conventional autoregressive Large Language Models (LLMs) that generate natural language tokens sequentially, Jev is designed to skip autoregression and output typed, structured schema decisions with calibrated probability distributions in a single step.

---

## 2. Key Architecture & Principles

- **Paradigm ("System 1"):** Inspired by Daniel Kahneman's cognitive framework, System 1 represents fast, reflex-driven, non-deliberative pattern recognition.
- **Input State:** Takes arbitrary unstructured text or program state (e.g., ticket descriptions, customer queries, server telemetry).
- **Output Schema:** Predefined typed primitives (such as booleans, categorical selections, ordinal scoring levels).
- **Optimization Strategy:** Trained using **RLCD** (*Reinforcement Learning for Calibrated Decisions*), optimizing for epistemically sound probability outputs rather than human conversational preference (RLHF) or verifiable string tokens (RLVR).
- **Hallucination Elimination:** By restricting the output space strictly to predefined schema options, the model structurally avoids verbal hallucinations and schema validation failures.

---

## 3. Commercial Model & Pricing

- **Delivery:** Closed API service (hosted by TypeSafe AI).
- **Pricing:** ~$0.042 per million input tokens.
- **Latency Profile:** ~150 ms to 276 ms end-to-end API response time.

---

## 4. Controversy & Prior Art

Shortly after its launch, TypeSafe AI faced public pushback from independent researcher Nandakishor Mukkunnoth (ConvAI Innovations), who demonstrated that the exact architecture (non-autoregressive reinforcement learning for schema-calibrated decisions) had already been published on arXiv in March 2025 (*arXiv:2503.23303*) and September 2025 (*arXiv:2510.01237*) with open-weight releases.

This controversy directly triggered the release of the open-source alternative [[laya-system-1-decision-engine]].

---

## 5. Cross-References
- [[laya-system-1-decision-engine]] — Open-source Apache 2.0 alternative built on ModernBERT.
- [[laya-vs-typesafe-jev]] — Comprehensive side-by-side performance and architecture comparison.
- [[ai_evaluation_annotation_handbook]] — Evaluation methodologies, calibration, and RLHF principles.
