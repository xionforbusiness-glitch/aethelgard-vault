---
source_url: https://www.facebook.com/share/r/1K9aNy13hD/
ingested: 2026-10-01
title: "Running 744B Parameter AI Models on Laptops via SSD Streaming (Colibri / AirLLM Analysis)"
uploader: "Alan Brown | AI & Robotics"
---

# Running 744B+ Models via SSD Streaming (Colibri / AirLLM) — Feasibility & Bottleneck Analysis

- **Source URL:** https://www.facebook.com/share/r/1K9aNy13hD/
- **Featured Project:** **Colibri** (and similar frameworks like **AirLLM** / **KTransformers** / **MoE Offloading**)
- **Claimed Feasibility:** Running a 744-Billion parameter Mixture-of-Experts (MoE) model on a standard laptop with zero dedicated GPUs by streaming ~10 GB of active weights from SSD to RAM per forward step.
- **Hardware Requirement:** ~370 GB of fast local SSD storage and ~16–32 GB system RAM.

## Engineering Takeaways:
1. **How it works:** MoE architecture routing activates only a subset of experts per token (e.g. 10–20 GB active weights per step). Colibri streams these layers sequentially from NVMe SSD into RAM, executes the calculation on CPU, and drops them.
2. **The Bandwidth Bottleneck:** High-speed NVMe SSD read throughput (3.5–7.0 GB/s) is 100x–500x slower than GPU VRAM bandwidth (600–3,350 GB/s).
3. **Generation Speed:** Translates to ~0.2 to 0.8 tokens/second (~15 to 30 minutes for a single 500-token answer).
4. **Cloud / Kaggle Constraints:** Kaggle scratch disk storage is capped at ~20–70 GB, making it impossible to download a 370 GB model weight file into ephemeral storage.
