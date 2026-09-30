---
source_url: https://www.facebook.com/helloluis/posts/jev-by-typesafe-ai-is-less-than-a-week-old-and-its-already-being-hit-with-contro/10166104412386518/
additional_sources:
  - https://laya.convaiinnovations.com/
  - https://huggingface.co/convaiinnovations/laya
  - https://typesafe.ai/blog/introducing-system-one-models-and-jev
  - https://github.com/receptron/laya
ingested: 2026-09-21
image_file: raw/assets/20260921_laya_vs_jev_system1_decision_model.jpg
sha256: e2548591870c2ddfd5a389674c66e78f9fd25d83104f9cd485e24aeca64cb108
type: raw_source
tags: [ai, ml, llm, open-source]
---

# Raw Source: Laya vs TypeSafe Jev & System 1 Decision Models Controversy

## 1. Primary Ingested Image Screenshot
![[20260921_laya_vs_jev_system1_decision_model.jpg]]

## 2. Full OCR & Visual Content Transcription

- **Source Platform:** Facebook Mobile (Android UI)
- **Author:** Luis Buenaventura (Verified)
- **Date/Timestamp:** September 20–21, 2026 (~23h post age)
- **Engagement:** 303 reactions, 27 comments, 50 shares

### Post Body:
> "Jev by TypeSafe AI is less than a week old and it's already being hit with controversy: the team supposedly stole the idea from another researcher, so now that guy is open-sourcing a better version!
>
> Instead of staying bitter, I decided to take everything I learned, fix every architectural limitation of the old approach, and build a completely open, horizontal System 1 decision model family: **Laya**.
>
> And because we built it properly on bidirectional encoders, our models run in **32.8 milliseconds on a single GPU (7.2 ms/question batched)**, making it **6 to 8 times faster than Jev**, with full support for **over 100 languages**, **zero API subscription costs**, and **100% open-source Apache 2.0 weights**."

---

## 3. Investigated Technical Context & Provenance

### The Context & Dispute:
1. **TypeSafe AI Launch:** On September 15, 2026, TypeSafe AI (founded by Diogo Almeida, former OpenAI researcher and co-creator of ChatGPT / RLHF) launched **Jev**, a proprietary, non-autoregressive "System 1" model that takes structured/unstructured state and outputs typed decisions with calibrated probabilities rather than generating text token-by-token.
2. **Prior Art & Callout:** Nandakishor Mukkunnoth (Founder & CEO of ConvAI Innovations) called out the announcement, citing his prior publications:
   - March 2025 arXiv paper: *arXiv:2503.23303* on sequence conversion trajectories
   - Hugging Face model: `DeepMostInnovations/sales-conversion-model-reinf-learning`
   - Open dataset: `DeepMostInnovations/saas-sales-conversations`
   - September 2025 arXiv paper: *arXiv:2510.01237* on schema-based decisions guided by reinforcement learning.
3. **Open-Source Response (Laya):** ConvAI Innovations released **Laya** under the Apache 2.0 license as a 100% open-weights, open-source horizontal System 1 decision engine family.
4. **Amplification:** Tech commentator Luis Buenaventura summarized and shared Nandakishor's response on social media.

---

## 4. Key Architectural & Benchmark Specifications

- **Architecture:** Non-autoregressive classification & regression heads atop bidirectional transformer encoders:
  - `convaiinnovations/laya`: ModernBERT-large (421M params, 512 context)
  - `convaiinnovations/laya-multilingual`: mmBERT-base (322M params, 1024 context, 100+ languages)
  - `convaiinnovations/laya-typed-decisions`: ModernBERT-large (421M params, fine-tuned on benchmark split)
- **Training Method:** Reinforcement Learning for Calibrated Decisions (RLCD) with strictly proper scoring rules.
- **Latency Claim:** 32.8 ms single GPU (Tesla T4) / 7.2 ms per question batched.
- **Honest Benchmark Reality:**
  - Zero-shot typed decisions accuracy: ~0.35–0.36 (close to baseline).
  - Fine-tuned benchmark accuracy: 0.766 (vs Jev 1.13.0's 0.727).
  - Designed as an ultra-fast base for domain specialization/fine-tuning (ticket triage, intent routing, moderation, guardrails).
